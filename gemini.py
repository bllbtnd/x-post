"""Gemini AI model configuration and tweet generation"""
import os
from datetime import datetime
import google.generativeai as genai


def configure_gemini():
    """Configure and return Gemini model"""
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    
    # Use the same model as NewsScraper
    model_name = 'models/gemini-2.5-pro'
    
    print(f"🤖 Using Gemini model: {model_name}\n")
    return genai.GenerativeModel(model_name), model_name


def generate_tweet(model, selected_topic, all_topics):
    """Generate tweet content using Gemini"""
    # Build context for AI
    trends_context = ""
    if len(all_topics) > 1:
        other_topics = [t for t in all_topics[:8] if t != selected_topic]
        trends_context = f"\n\nOther current trending topics for context: {', '.join(other_topics)}"
    
    prompt = f"""Write a single tweet about: {selected_topic}
{trends_context}

VOICE & PERSPECTIVE:
You are a centre-right European conservative capitalist. Your worldview:
- Free markets and family stability fuel prosperity
- Institutions, sovereignty, and personal responsibility deserve defence
- Enterprise should beat bureaucracy, innovation should beat ideology

WRITING REQUIREMENTS:
- 215-265 characters (enough substance, zero fluff)
- Start with a six-word hook that uses everyday language
- Keep every sentence under 18 words and avoid jargon or acronyms (spell them out)
- Name one clear villain: bloated bureaucracy, ideological crusades, corporate cronyism, or moral laziness
- Give one concrete example that affects normal people (households, small firms, commuters, savers)
- Blacklisted words: ideological
- Show what the audience can still control or gain — highlight agency, not despair
- Finish with a crisp call-to-action or question that invites a share or answer
- Optional: use at most one emoji near the end if it strengthens the punchline
- No ALL CAPS, no links, no mentions, no hashtags, no special formatting
- No NSFW, violence, illegality
- Make sure the text is complete, and is not cut in half, does not end with "..."
- Flags only if: EU, Hungary, UK, US, Russia, Poland, Greece, UAE, Albania
- Accurate dates/times if mentioned
- Current date: {datetime.now().strftime('%d %B %Y')}

Output only the tweet text, nothing else."""
    
    print("🤖 Generating tweet with Gemini...")
    response = model.generate_content(prompt)
    tweet = response.text.strip().replace('"', '').replace('\n', ' ')
    
    # Ensure it's not too long
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    
    return tweet
