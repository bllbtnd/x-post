"""Gemini AI model configuration and tweet generation"""
import os
from datetime import datetime
import google.generativeai as genai


def get_last_posts(num_posts=5):
    """Read the last N posts from posted_tweets.txt"""
    try:
        with open('data/posted_tweets.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Get only non-empty lines and take the last num_posts
        posts = [line.strip() for line in lines if line.strip()]
        last_posts = posts[-num_posts:] if len(posts) >= num_posts else posts
        
        # Extract just the tweet text (everything after the last '|')
        tweet_texts = []
        for post in last_posts:
            parts = post.split(' | ')
            if len(parts) >= 2:
                tweet_text = parts[-1]  # Last part is the tweet text
                tweet_texts.append(tweet_text)
        
        return tweet_texts
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"⚠️  Warning: Could not read past posts: {e}")
        return []


def configure_gemini():
    """Configure and return Gemini model"""
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    
    # Use gemini-2.5-flash - faster and higher free tier quota than 2.5-pro
    # Flash models have higher rate limits for free tier usage
    model_name = 'models/gemini-2.5-flash'
    
    print(f"🤖 Using Gemini model: {model_name}\n")
    return genai.GenerativeModel(model_name), model_name


def generate_tweet(model, selected_topic, all_topics, past_posts=None):
    """Generate tweet content using Gemini"""
    if past_posts is None:
        past_posts = get_last_posts(5)
    # Build context for AI
    trends_context = ""
    if len(all_topics) > 1:
        other_topics = [t for t in all_topics[:8] if t != selected_topic]
        trends_context = f"\n\nOther current trending topics for context: {', '.join(other_topics)}"
    
    # Add past posts context to avoid repetition
    past_posts_context = ""
    if past_posts:
        past_posts_context = "\n\nYOUR RECENT POSTS (avoid repeating these patterns, structures, punchlines, or schemas):\n"
        for i, post in enumerate(past_posts, 1):
            past_posts_context += f"{i}. {post}\n"
        past_posts_context += "\nDO NOT reuse the same opening hooks, closing questions, emoji placement patterns, or rhetorical structures from above. VARY your approach significantly."
    
    prompt = f"""Write a single tweet about: {selected_topic}
{trends_context}{past_posts_context}

VOICE & PERSPECTIVE:
You are a Civil Libertarian with Cultural Centrist values and strong pro-technology views. Your worldview:
- Individual liberty and personal autonomy are paramount
- Free markets enable innovation; minimal government interference maximizes freedom
- Technology and innovation drive human progress and should be embraced, not feared
- Privacy rights, free speech, and civil liberties are non-negotiable
- Cultural moderation: balance progress with social stability, avoid extremes
- Oppose surveillance, excessive regulation, and interventionist foreign policy
- Support: crypto, AI development, space exploration, biotech innovation
- Skeptical of government overreach, corporate cronyism, and authoritarian tendencies

WRITING REQUIREMENTS - BE PUNCHY AND VIRAL:
- 210-230 characters max. Finish every thought completely. Zero fluff, maximum impact.
- START STRONG: Open with a bold claim, provocative question, or shocking statement that stops the scroll
- BE CONTROVERSIAL: Take a clear stance that will get people nodding OR furious - neutrality is death
- NAME THE VILLAIN: Call out specific entities - bureaucrats, regulators, politicians, or broken systems
- MAKE IT PERSONAL: Show how this hits people's wallets, freedom, safety, or family RIGHT NOW
- CREATE URGENCY: Use "now", "today", "finally", "still" to emphasize timeliness
- END WITH A HOOK: Ask a question that demands a response, or make a statement people can't help but share/argue with
- VARY YOUR STRUCTURE: Don't always use the same formula - mix up your openings, middles, and endings
- Use ONE emoji maximum, only if it amplifies emotion or controversy
- Keep sentences sharp and under 18 words
- No ALL CAPS, links, mentions, hashtags
- No NSFW, violence, or illegality
- Flags only if: EU, Hungary, UK, US, Russia, Poland, Greece, UAE, Albania
- Current date: {datetime.now().strftime('%d %B %Y')}

GOAL: Make people CLICK, SHARE, and ARGUE. Polarization drives engagement. Be bold, be sharp, be memorable.

Output only the tweet text, nothing else."""
    
    print("🤖 Generating tweet with Gemini...")
    print("\n" + "="*80)
    print("FULL PROMPT SENT TO GEMINI:")
    print("="*80)
    print(prompt)
    print("="*80 + "\n")
    
    response = model.generate_content(prompt)
    tweet = response.text.strip().replace('"', '').replace('\n', ' ')
    
    # Ensure it's not too long
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    
    return tweet
