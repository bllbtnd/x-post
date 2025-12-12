"""Trending topics fetching and selection"""
import os
import re
import random
from datetime import datetime


def get_trending_topics():
    """
    Fetch trending topics using news scrapers from multiple sources.
    Uses the same scrapers as NewsScraper for consistency.
    """
    try:
        from scrapers.neutral import scrape_ap
        from scrapers.international_left import scrape_bbc, scrape_aljazeera, scrape_france24
        from scrapers.international_right import scrape_fox
        from scrapers.hungarian_left import scrape_telex, scrape_index, scrape_444
        from scrapers.hungarian_right import scrape_mandiner, scrape_magyarnemzet
        
        all_articles = []
        
        # Scrape from all sources
        sources = [
            # International
            ("AP News (Neutral)", scrape_ap),
            ("BBC News (Center-Left)", scrape_bbc),
            ("Al Jazeera (Left)", scrape_aljazeera),
            ("France24 (Center-Left)", scrape_france24),
            ("Fox News (Right)", scrape_fox),
            # Hungarian
            ("Telex (HU-Left)", scrape_telex),
            ("Index (HU-Center)", scrape_index),
            ("444 (HU-Left)", scrape_444),
            ("Mandiner (HU-Right)", scrape_mandiner),
            ("Magyar Nemzet (HU-Right)", scrape_magyarnemzet),
        ]
        
        for source_name, scraper_func in sources:
            try:
                articles = scraper_func()
                if articles:
                    all_articles.extend(articles)
                    print(f"  ✅ {source_name}: {len(articles)} articles")
                    # Display each headline
                    for i, article in enumerate(articles, 1):
                        print(f"     {i}. {article['title']}")
                else:
                    print(f"  ⚠️  {source_name}: No articles found")
            except Exception as e:
                print(f"  ⚠️  {source_name}: {e}")
        
        # Extract just the titles as topics
        topics = [article['title'] for article in all_articles]
        
        return topics
        
    except Exception as e:
        print(f"⚠️  Scraper error: {e}")
        return []


def select_best_topic(model, all_topics):
    """
    Ask Gemini to analyze all available topics and choose the one 
    that would get the most attention and engagement from a center-right 
    European conservative capitalist perspective.
    """
    try:
        topics_list = '\n'.join([f"{i+1}. {topic}" for i, topic in enumerate(all_topics)])
        
        selection_prompt = f"""You are a viral content strategist with a Civil Libertarian, Cultural Centrist, and pro-technology worldview. 

Analyze these topics and choose ONE that would generate the most engagement on X (Twitter) from this perspective.

Available topics:
{topics_list}

SELECTION CRITERIA:
From a Civil Libertarian, Cultural Centrist, and pro-technology perspective, choose the topic that:
1. Has global relevance (matters beyond one country)
2. Allows for a strong individual liberty, privacy rights, or technological innovation angle
3. Creates genuine opinion split across the political spectrum
4. Is timely and currently unfolding
5. Challenges government overreach, surveillance, or innovation-stifling policies
6. Has emotional resonance (people care deeply)
7. Offers space for a contrarian but defendable libertarian take
8. Europeans would find particularly interesting

Prioritize topics where you can defend:
- Individual freedom and personal autonomy
- Privacy rights and civil liberties
- Technological innovation and progress (AI, crypto, biotech, space)
- Free markets and minimal government interference
- Free speech and digital rights
- Opposition to surveillance and authoritarianism
- Cultural moderation and pragmatic compromise
- Decentralization and personal empowerment

Current date: {datetime.now().strftime('%d %B %Y')}

Output ONLY the exact topic text from the list above that offers the strongest opportunity for viral libertarian engagement. No explanation, no numbering, just the topic text."""

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
