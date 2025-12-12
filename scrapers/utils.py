"""Utility functions for RSS feed parsing"""
import feedparser
import requests


def fetch_rss_feed(url, max_items=15):
    """
    Fetch and parse an RSS feed, returning a list of articles.
    
    Args:
        url: RSS feed URL
        max_items: Maximum number of items to return
        
    Returns:
        List of dicts with 'title', 'url', 'summary' keys
    """
    try:
        # Set timeout for the request
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'
        })
        feed = feedparser.parse(response.content)
        
        articles = []
        for entry in feed.entries[:max_items]:
            # Get title
            title = entry.get('title', '').strip()
            if not title or len(title) < 15:
                continue
            
            # Get link
            link = entry.get('link', '')
            if not link:
                continue
            
            # Get summary/description (optional)
            summary = entry.get('summary', '') or entry.get('description', '')
            
            articles.append({
                'title': title,
                'url': link,
                'summary': summary
            })
        
        return articles
    except Exception as e:
        print(f"  ❌ RSS Feed Error ({url}): {e}")
        return []


def is_political_or_economic(title, url='', summary=''):
    """Check if article is about politics or economy based on title and content"""
    if not title:
        return False
    
    text = (title + ' ' + url + ' ' + summary).lower()
    
    # Political and economic keywords
    keywords = [
        # Hungarian politics
        'kormány', 'parlament', 'miniszter', 'fidesz', 'dk', 'momentum',
        'orbán', 'választás', 'törvény', 'politika', 'belfold', 'kulfold',
        # Hungarian economy
        'gazdaság', 'infláció', 'forint', 'mnb', 'gdp', 'költségvetés',
        'adó', 'befektetés', 'bank', 'tőzsde', 'vállalat',
        # English politics
        'government', 'parliament', 'congress', 'senate', 'minister',
        'president', 'election', 'vote', 'law', 'policy', 'bill',
        'democrat', 'republican', 'labour', 'conservative', 'party',
        'trump', 'biden', 'putin', 'xi jinping', 'modi', 'macron', 'scholz',
        'nato', 'european union', 'united nations', 'white house', 'kremlin', 'brussels',
        'politics', 'political', 'diplomacy', 'sanctions', 'treaty',
        # English economy
        'economy', 'inflation', 'gdp', 'recession', 'market', 'stock',
        'trade', 'tariff', 'fed', 'central bank', 'interest rate',
        'investment', 'fiscal', 'budget', 'tax', 'unemployment',
        'currency', 'dollar', 'euro', 'yuan', 'imf', 'world bank',
        'oil', 'energy', 'prices', 'debt', 'bonds', 'equity', 'business',
        'economic', 'finance', 'financial', 'cryptocurrency', 'bitcoin',
    ]
    
    return any(keyword in text for keyword in keywords)
