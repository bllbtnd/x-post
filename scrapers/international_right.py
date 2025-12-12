"""International right-leaning news scrapers using RSS feeds"""
from .utils import fetch_rss_feed, is_political_or_economic


def scrape_fox():
    """Scrape Fox News via RSS (Right-wing)"""
    try:
        # Fox News RSS feeds
        feeds = [
            'https://moxie.foxnews.com/google-publisher/politics.xml',
            'https://moxie.foxnews.com/google-publisher/world.xml',
            'https://moxie.foxnews.com/google-publisher/latest.xml',
        ]
        
        all_articles = []
        seen_titles = set()
        
        for feed_url in feeds:
            articles = fetch_rss_feed(feed_url, max_items=20)
            for article in articles:
                if article['title'] in seen_titles:
                    continue
                
                if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                    seen_titles.add(article['title'])
                    all_articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': 'Fox News (Right)'
                    })
                
                if len(all_articles) >= 15:
                    break
            
            if len(all_articles) >= 15:
                break
        
        return all_articles
    except Exception as e:
        print(f"  ❌ Fox Error: {e}")
        return []

