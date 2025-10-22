"""Trending topics fetching and selection"""
import os
import re
import random
from datetime import datetime


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
- Make sure it is a topic that can generate a strong, clear opinion

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
