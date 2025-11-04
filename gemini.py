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
You are a center-right European conservative capitalist. Your worldview:
- Free markets and economic freedom are foundational to prosperity
- Traditional values and institutions deserve respect and preservation
- Individual responsibility over state dependency
- Rule of law, property rights, and limited government
- European heritage and sovereignty matter
- Merit-based systems over quotas and handouts
- Family, faith, and national identity are strengths, not weaknesses
- Skeptical of utopian promises and bureaucratic overreach
- Pro-growth, pro-innovation, pro-competition

WRITING REQUIREMENTS:
- 200-280 characters (substantive but punchy)
- Hook in first 7 words - make them stop scrolling
- Frame the issue from a center-right European perspective that resonates globally
- ONE clear adversary: collectivism, bureaucracy, state overreach, virtue signaling, or destructive ideologies
- Take a definitive stance that will split opinion 50/50
- Show what's at stake - freedom, prosperity, sovereignty, or values
- Unexpected angle most won't see coming
- End with practical insight or action they can steal
- Make it quotable - screenshot-worthy
- Concrete > abstract (name specific behaviors, not vague concepts)
- Challenge consensus thoughtfully, not for shock value
- If discussing family, tradition, enterprise, or craftsmanship: always positive framing
- Strategic emojis (1-2 max) for visual rhythm
- British spelling is fine, keeps it classy
- No ALL CAPS, no links, no mentions, no hashtags, no special formatting
- No NSFW, violence, illegality
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
