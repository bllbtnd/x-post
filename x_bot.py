import tweepy
import google.generativeai as genai
import os
import random
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Test mode flag - set via command line
DRY_RUN = '--dry-run' in sys.argv or '--test' in sys.argv

def get_best_gemini_model():
    """Get the best available Gemini model"""
    try:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        available = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available.append(m.name)
        
        if not available:
            return None
        
        # Prefer these models in order
        preferred = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        for pref in preferred:
            for model in available:
                if pref in model:
                    return model.replace('models/', '')
        
        # Return first available if no preferred found
        return available[0].replace('models/', '')
    except Exception as e:
        print(f"Error getting models: {e}")
        return None

def get_trending_topics():
    """
    Fetch trending topics from multiple sources via web scraping.
    This function should be called from a script that has web search capabilities.
    
    For your Python bot, you have a few options:
    1. Use newsapi.org (free tier: 100 requests/day)
    2. Scrape Google Trends
    3. Use trending-api libraries
    4. Manual weekly curation
    """
    
    # Option 1: Use NewsAPI (recommended - free tier available)
    # Sign up at https://newsapi.org/ for free API key
    
    try:
        import requests
        
        # Check if NewsAPI key exists
        news_api_key = os.environ.get('NEWS_API_KEY')
        
        if news_api_key:
            # Get top headlines
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])[:15]
                
                trends = []
                for article in articles:
                    title = article.get('title', '')
                    # Extract key topic from headline
                    if title and title != '[Removed]':
                        # Clean up title
                        topic = title.split(' - ')[0].strip()
                        trends.append(topic)
                
                return trends
        
        # Fallback: Try Google Trends via pytrends
        try:
            from pytrends.request import TrendReq
            pytrends = TrendReq(hl='en-US', tz=360)
            trending = pytrends.trending_searches(pn='united_states')
            return trending[0].tolist()[:15]
        except:
            pass
            
    except Exception as e:
        print(f"⚠️  Trending fetch error: {e}")
    
    return []

def load_curated_trends():
    """
    Load manually curated trending topics from a file.
    Update this file weekly with hot topics.
    """
    try:
        if os.path.exists('trending_topics.txt'):
            with open('trending_topics.txt', 'r', encoding='utf-8') as f:
                trends = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                return trends
    except:
        pass
    return []

def select_best_topic(model, all_topics):
    """
    Ask Gemini to analyze all available topics and choose the one 
    that would get the most attention and engagement globally.
    """
    try:
        topics_list = '\n'.join([f"{i+1}. {topic}" for i, topic in enumerate(all_topics)])
        
        selection_prompt = f"""You are a viral content strategist. Analyze these topics and choose ONE that would get the most attention and engagement on X (Twitter) globally.

Available topics:
{topics_list}

Consider:
- Global relevance (matters to most people on Earth)
- Controversy potential (splits opinion 50/50)
- Current timeliness (happening NOW)
- Emotional impact (makes people react)
- Shareability (people will repost takes on this)

Current date: {datetime.now().strftime('%d %B %Y')}

Output ONLY the exact topic text from the list above that would hit hardest. No explanation, no numbering, just the topic text."""

        print("🎯 Asking Gemini to select best topic...")
        response = model.generate_content(selection_prompt)
        selected = response.text.strip().strip('"').strip("'")
        
        # Try to match the selected topic to one in our list
        # Clean up any numbering or formatting Gemini might have added
        selected_clean = re.sub(r'^\d+\.\s*', '', selected)
        
        # Find closest match
        for topic in all_topics:
            if selected_clean.lower() in topic.lower() or topic.lower() in selected_clean.lower():
                return topic
        
        # If no match, return the cleaned response anyway
        return selected_clean
        
    except Exception as e:
        print(f"⚠️  Topic selection failed: {e}")
        # Fallback to random selection
        return random.choice(all_topics)

def test_api_connections():
    """Test if API credentials are valid"""
    print("🔍 Testing API connections...\n")
    
    # Test Gemini
    try:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        
        # List available models
        print("Available Gemini models:")
        available = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name.replace('models/', '')
                available.append(model_name)
                print(f"   - {model_name}")
        
        if not available:
            print("❌ No models available with your API key\n")
            return False
        
        # Test with best available model
        model_name = get_best_gemini_model()
        print(f"\n🧪 Testing with: {model_name}")
        test_model = genai.GenerativeModel(model_name)
        test_response = test_model.generate_content("Say 'OK' if you can read this")
        print(f"✅ Gemini API: Connected")
        print(f"   Response: {test_response.text.strip()}\n")
    except Exception as e:
        print(f"❌ Gemini API: Failed - {e}\n")
        return False
    
    # Test X API v2
    try:
        client = tweepy.Client(
            consumer_key=os.environ['X_API_KEY'],
            consumer_secret=os.environ['X_API_SECRET'],
            access_token=os.environ['X_ACCESS_TOKEN'],
            access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET']
        )
        me = client.get_me()
        print(f"✅ X API v2: Connected")
        print(f"   Account: @{me.data.username}\n")
    except Exception as e:
        print(f"❌ X API v2: Failed - {e}\n")
        return False
    
    # Test NewsAPI if key exists
    news_api_key = os.environ.get('NEWS_API_KEY')
    if news_api_key:
        try:
            import requests
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ NewsAPI: Connected\n")
            else:
                print(f"⚠️  NewsAPI: Status {response.status_code}\n")
        except Exception as e:
            print(f"⚠️  NewsAPI: {e}\n")
    else:
        print("ℹ️  NewsAPI: Not configured (optional)\n")
    
    return True

def validate_tweet(tweet):
    """Check if tweet meets requirements"""
    issues = []
    
    if len(tweet) > 280:
        issues.append(f"Too long: {len(tweet)} chars")
    if len(tweet) < 50:
        issues.append(f"Too short: {len(tweet)} chars")
    if tweet.count('#') > 2:
        issues.append(f"Too many hashtags: {tweet.count('#')}")
    if tweet.count('http') > 1:
        issues.append("Too many links")
    
    return issues

def main():
    print("=" * 60)
    print("X AUTOMATED POSTING SCRIPT")
    print("=" * 60)
    
    if DRY_RUN:
        print("🧪 DRY RUN MODE - Will NOT post to X\n")
    else:
        print("🚀 LIVE MODE - Will post to X\n")
    
    # Test connections first
    if '--test-connection' in sys.argv:
        if test_api_connections():
            print("✅ All API connections working!\n")
            return
        else:
            print("❌ API connection failed. Fix credentials.\n")
            sys.exit(1)
    
    # Configure Gemini
    try:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        model_name = get_best_gemini_model()
        
        if not model_name:
            print("❌ No Gemini models available. Check your API key.")
            sys.exit(1)
        
        print(f"🤖 Using Gemini model: {model_name}\n")
        model = genai.GenerativeModel(model_name)
        
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
        print("Make sure your .env file has all required keys.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Gemini configuration failed: {e}")
        sys.exit(1)
    
    # Configure X API v2 (for posting)
    try:
        client = tweepy.Client(
            consumer_key=os.environ['X_API_KEY'],
            consumer_secret=os.environ['X_API_SECRET'],
            access_token=os.environ['X_ACCESS_TOKEN'],
            access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET']
        )
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
        sys.exit(1)
    
    # Fetch trending topics
    print("📊 Fetching trending topics...")
    
    # Try multiple sources in priority order
    trending = []
    
    # 1. Try curated file first (best quality)
    trending = load_curated_trends()
    if trending:
        print(f"✅ Loaded {len(trending)} curated topics")
    
    # 2. Try NewsAPI or other services
    if not trending:
        trending = get_trending_topics()
        if trending:
            print(f"✅ Found {len(trending)} trending topics from news")
    
    # Fallback topic pool
    fallback_topics = [
        "US politics and policy debates",
        "European economic challenges",
        "AI replacing white collar jobs",
        "mens health and masculinity crisis",
        "productivity and hustle culture",
        "climate policy vs economic growth",
        "social media addiction",
        "housing affordability crisis",
        "fitness and body composition",
        "remote work vs office mandates",
        "crypto regulation",
        "free speech vs moderation",
        "dating apps ruining relationships",
        "college debt and ROI of degrees"
    ]
    
    # Combine all available topics
    all_topics = []
    
    if trending:
        all_topics.extend(trending[:10])  # Top 10 trending
    
    # Always add fallback topics to give AI more options
    all_topics.extend(fallback_topics)
    
    if not all_topics:
        print("❌ No topics available. Check your setup.\n")
        sys.exit(1)
    
    # DISPLAY ALL TOPICS BEING SENT TO GEMINI
    print(f"\n{'='*60}")
    print(f"ALL TOPICS SENT TO GEMINI FOR SELECTION ({len(all_topics)} total):")
    print(f"{'='*60}")
    
    for i, topic in enumerate(all_topics, 1):
        # Mark if it's from trending or fallback
        if trending and topic in trending:
            print(f"   {i}. 🔥 {topic}")
        else:
            print(f"   {i}. 📋 {topic}")
    
    print(f"{'='*60}\n")
    print("Legend: 🔥 = Trending topic | 📋 = Strategic fallback\n")
    
    # STEP 1: Let Gemini choose the best topic
    selected_topic = select_best_topic(model, all_topics)
    
    print(f"✅ Gemini selected: {selected_topic}\n")
    
    # Determine source
    topic_source = "trending" if (trending and selected_topic in trending) else "strategic"
    
    # Build context for AI
    trends_context = ""
    if trending:
        trends_context = f"\n\nOther current trending topics for context: {', '.join(trending[:8])}"
    
    # STEP 2: Generate tweet on the selected topic
    prompt = f"""Write a single tweet about: {selected_topic}
{trends_context}

Requirements:

- 200-280 characters (full depth, still punchy)
- Do not attack a specific country directly
- Strong clear opinion that pisses off exactly half the room
- Make ONE enemy clearly defined (weak people, fake entrepreneurs, whatever)
- End with practical insight they'll steal and repost
- British spelling fine, keeps it classy
- Strategic emojis (1-2 max) for visual break in feed
- No ALL CAPS
- No links
- No bald characters
- If there is something big happening in the world currently, use it as topic
- No mentions
- No bold or special characters
- One niche hashtag if it's trending and relevant
- Do not post anything illegal
- Do not add flags or political symbols (unless it is EU, Hungary, UK, US, Russia, Poland, Greece, UAE, Albania)
- Make sure you use the correct date and time if you mention it.
- Current date: {datetime.now().strftime('%d %B %Y')}

Output only the tweet text, nothing else."""
    
    try:
        print("🤖 Generating tweet with Gemini...")
        response = model.generate_content(prompt)
        tweet = response.text.strip().replace('"', '').replace('\n', ' ')
        
        # Ensure it's not too long
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        print(f"\n{'='*60}")
        print("GENERATED TWEET:")
        print(f"{'='*60}")
        print(tweet)
        print(f"{'='*60}")
        print(f"Length: {len(tweet)} characters")
        print(f"Source: {topic_source}\n")
        
        # Validate tweet
        issues = validate_tweet(tweet)
        if issues:
            print("⚠️  Validation warnings:")
            for issue in issues:
                print(f"   - {issue}")
            print()
        else:
            print("✅ Tweet validation passed\n")
        
        # Post to X (or skip if dry run)
        if DRY_RUN:
            print("🧪 DRY RUN: Would post this tweet to X")
            print("   Run without --dry-run or --test to post for real\n")
            
            # Save to file for review
            with open('test_tweets.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{datetime.now()} | Source: {topic_source} | Topic: {selected_topic}\n")
                f.write(f"{tweet}\n")
                f.write("-" * 60 + "\n")
            print("💾 Saved to test_tweets.txt for review\n")
            
        else:
            print("📤 Posting to X...")
            result = client.create_tweet(text=tweet)
            tweet_id = result.data['id']
            print(f"✅ Posted successfully!")
            print(f"   Tweet ID: {tweet_id}")
            print(f"   URL: https://x.com/i/web/status/{tweet_id}\n")
            
            # Log successful post
            with open('posted_tweets.txt', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()} | {tweet_id} | {topic_source} | {selected_topic} | {tweet}\n")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print(f"   Error type: {type(e).__name__}")
        raise

if __name__ == "__main__":
    main()