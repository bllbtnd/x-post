"""Hungarian left-leaning news scrapers using RSS feeds"""
from .utils import fetch_rss_feed, is_political_or_economic


def scrape_telex():
    """Scrape Telex.hu via RSS (Left-leaning)"""
    try:
        # Telex RSS feed
        articles = fetch_rss_feed('https://telex.hu/rss', max_items=30)
        
        filtered_articles = []
        for article in articles:
            if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                filtered_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': 'Telex (HU-Left)'
                })
            
            if len(filtered_articles) >= 15:
                break
        
        return filtered_articles
    except Exception as e:
        print(f"  ❌ Telex Error: {e}")
        return []


def scrape_index():
    """Scrape Index.hu via RSS (Center-left)"""
    try:
        # Index.hu RSS feeds
        feeds = [
            'https://index.hu/24ora/rss/',
            'https://index.hu/belfold/rss/',
            'https://index.hu/kulfold/rss/',
            'https://index.hu/gazdasag/rss/',
        ]
        
        all_articles = []
        seen_titles = set()
        
        for feed_url in feeds:
            articles = fetch_rss_feed(feed_url, max_items=15)
            for article in articles:
                if article['title'] in seen_titles:
                    continue
                
                if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                    seen_titles.add(article['title'])
                    all_articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': 'Index (HU-Center)'
                    })
                
                if len(all_articles) >= 15:
                    break
            
            if len(all_articles) >= 15:
                break
        
        return all_articles
    except Exception as e:
        print(f"  ❌ Index Error: {e}")
        return []


def scrape_444():
    """Scrape 444.hu via RSS (Left-leaning)"""
    try:
        # 444.hu RSS feed
        articles = fetch_rss_feed('https://444.hu/feed', max_items=30)
        
        filtered_articles = []
        for article in articles:
            if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                filtered_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': '444 (HU-Left)'
                })
            
            if len(filtered_articles) >= 15:
                break
        
        return filtered_articles
    except Exception as e:
        print(f"  ❌ 444 Error: {e}")
        return []

