"""International left-leaning news scrapers using RSS feeds"""
from .utils import fetch_rss_feed, is_political_or_economic


def scrape_bbc():
    """Scrape BBC News via RSS (Center-left)"""
    try:
        # BBC provides comprehensive RSS feeds
        feeds = [
            'http://feeds.bbci.co.uk/news/world/rss.xml',
            'http://feeds.bbci.co.uk/news/business/rss.xml',
            'http://feeds.bbci.co.uk/news/politics/rss.xml',
        ]
        
        all_articles = []
        seen_titles = set()
        
        for feed_url in feeds:
            articles = fetch_rss_feed(feed_url, max_items=20)
            for article in articles:
                if article['title'] in seen_titles:
                    continue
                
                # Filter for political/economic content
                if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                    seen_titles.add(article['title'])
                    all_articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        'source': 'BBC News (Center-Left)'
                    })
                
                if len(all_articles) >= 15:
                    break
            
            if len(all_articles) >= 15:
                break
        
        return all_articles
    except Exception as e:
        print(f"  ❌ BBC Error: {e}")
        return []


def scrape_aljazeera():
    """Scrape Al Jazeera via RSS (Left-leaning)"""
    try:
        # Al Jazeera RSS feed
        articles = fetch_rss_feed('https://www.aljazeera.com/xml/rss/all.xml', max_items=30)
        
        filtered_articles = []
        for article in articles:
            if is_political_or_economic(article['title'], article['url'], article.get('summary', '')):
                filtered_articles.append({
                    'title': article['title'],
                    'url': article['url'],
                    'source': 'Al Jazeera (Left)'
                })
            
            if len(filtered_articles) >= 15:
                break
        
        return filtered_articles
    except Exception as e:
        print(f"  ❌ Al Jazeera Error: {e}")
        return []


def scrape_france24():
    """Scrape France24 via RSS (Center-left)"""
    try:
        # France24 RSS feeds
        feeds = [
            'https://www.france24.com/en/rss',
            'https://www.france24.com/en/europe/rss',
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
                        'source': 'France24 (Center-Left)'
                    })
                
                if len(all_articles) >= 15:
                    break
            
            if len(all_articles) >= 15:
                break
        
        return all_articles
    except Exception as e:
        print(f"  ❌ France24 Error: {e}")
        return []

