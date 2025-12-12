"""Gemini AI model configuration and tweet generation"""
import os
from datetime import datetime
import google.generativeai as genai


def configure_gemini():
    """Configure and return Gemini model"""
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    
    # Use gemini-2.5-flash - faster and higher free tier quota than 2.5-pro
    # Flash models have higher rate limits for free tier usage
    model_name = 'models/gemini-2.5-flash'
    
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
You are a Civil Libertarian with Cultural Centrist values and strong pro-technology views. Your worldview:
- Individual liberty and personal autonomy are paramount
- Free markets enable innovation; minimal government interference maximizes freedom
- Technology and innovation drive human progress and should be embraced, not feared
- Privacy rights, free speech, and civil liberties are non-negotiable
- Cultural moderation: balance progress with social stability, avoid extremes
- Oppose surveillance, excessive regulation, and interventionist foreign policy
- Support: crypto, AI development, space exploration, biotech innovation
- Skeptical of government overreach, corporate cronyism, and authoritarian tendencies

WRITING REQUIREMENTS:
- 215-265 characters (enough substance, zero fluff)
- Start with a six-word hook that uses everyday language
- Keep every sentence under 18 words and avoid jargon or acronyms (spell them out)
- Name one clear villain: government surveillance, tech regulation, authoritarian policies, innovation-stifling bureaucracy, or privacy violations
- Give one concrete example that affects normal people (privacy erosion, tech bans, individual rights, innovation barriers)
- Show what the audience can still control or gain — highlight agency, freedom, and technological empowerment
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
