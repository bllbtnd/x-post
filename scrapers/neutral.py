"""Neutral news scrapers using RSS feeds"""
from .utils import fetch_rss_feed, is_political_or_economic


def scrape_ap():
    """Scrape Associated Press via RSS (Neutral)"""
    try:
        # Using Google News RSS for AP content (more reliable)
        feeds = [
            'https://news.google.com/rss/search?q=source:ap+when:1d&hl=en-US&gl=US&ceid=US:en',
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
                        'source': 'AP News (Neutral)'
                    })
                
                if len(all_articles) >= 15:
                    break
            
            if len(all_articles) >= 15:
                break
        
        return all_articles
    except Exception as e:
        print(f"  ❌ AP Error: {e}")
        return []

