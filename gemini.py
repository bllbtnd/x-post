"""Gemini AI model configuration and tweet generation"""
import os
from datetime import datetime
import google.generativeai as genai


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


def configure_gemini():
    """Configure and return Gemini model"""
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model_name = get_best_gemini_model()
    
    if not model_name:
        raise RuntimeError("No Gemini models available. Check your API key.")
    
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

Requirements:

- 200-280 characters (full depth, still punchy)
- Do not just talk about something. Be exactly clear what you think about it.
- Always conservative, can be a bit provocative, but never extreme.
- If you need to mention family, tradition, craftsmanship or similar, always talk positive about them.
- Do not attack a specific country directly
- Strong clear opinion that pisses off exactly half the room
- Make ONE enemy clearly defined
- End with practical insight they'll steal and repost
- British spelling fine, keeps it classy, but do not overdo it
- Strategic emojis (1-2 max) for visual break in feed
- No ALL CAPS
- No links
- No mentions
- No bold or special characters
- Absolutely no hashtags
- Do not post anything NSFW or adult
- Do not post anything violent or gory  
- Do not post anything illegal
- Do not add flags or political symbols (unless it is EU, Hungary, UK, US, Russia, Poland, Greece, UAE, Albania)
- Make sure you use the correct date and time if you mention it.
- Current date: {datetime.now().strftime('%d %B %Y')}

Output only the tweet text, nothing else."""
    
    print("🤖 Generating tweet with Gemini...")
    response = model.generate_content(prompt)
    tweet = response.text.strip().replace('"', '').replace('\n', ' ')
    
    # Ensure it's not too long
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    
    return tweet
