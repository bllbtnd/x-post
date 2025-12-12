"""Hungarian right-leaning news scrapers using RSS feeds"""
from .utils import fetch_rss_feed, is_political_or_economic


def scrape_mandiner():
    """Scrape Mandiner via RSS (Right-wing Hungarian)"""
    try:
        # Mandiner RSS feed - using their public API
        articles = fetch_rss_feed('https://mandiner.hu/publicapi/hu/rss/mandiner/articles', max_items=30)
        
        filtered_articles = []
        for article in articles:
            if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                filtered_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': 'Mandiner (HU-Right)'
                })
            
            if len(filtered_articles) >= 15:
                break
        
        return filtered_articles
    except Exception as e:
        print(f"  ❌ Mandiner Error: {e}")
        return []


def scrape_magyarnemzet():
    """Scrape Magyar Nemzet via RSS (Right-wing Hungarian)"""
    try:
        # Magyar Nemzet RSS feed
        articles = fetch_rss_feed('https://magyarnemzet.hu/feed/', max_items=30)
        
        filtered_articles = []
        for article in articles:
            if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                filtered_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': 'Magyar Nemzet (HU-Right)'
                })
            
            if len(filtered_articles) >= 15:
                break
        
        return filtered_articles
    except Exception as e:
        print(f"  ❌ Magyar Nemzet Error: {e}")
        return []

