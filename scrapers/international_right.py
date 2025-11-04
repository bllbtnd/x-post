"""International right-leaning news scrapers"""
import requests
from bs4 import BeautifulSoup
from .utils import is_political_or_economic


def scrape_fox():
    """Scrape Fox News (Right-wing)"""
    try:
        articles = []
        seen_titles = set()
        
        # Try homepage instead of specific sections
        response = requests.get("https://www.foxnews.com/", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Fox uses article tags and specific classes
        for article in soup.find_all('article')[:50]:
            # Look for headlines
            headline = article.find(['h2', 'h3', 'h4'])
            if not headline:
                continue
            
            title = headline.get_text(strip=True)
            if not title or len(title) < 20 or title in seen_titles:
                continue
            
            # Find link
            link = article.find('a', href=True)
            if not link:
                # Try finding link from headline's parent
                link = headline.find_parent('a')
            
            if not link or not link.get('href'):
                continue
            
            href = link['href']
            url = href if href.startswith('http') else f"https://www.foxnews.com{href}"
            
            # Filter for politics/economy
            if not is_political_or_economic(url, title):
                continue
            
            seen_titles.add(title)
            articles.append({
                'title': title,
                'url': url,
                'source': 'Fox News (Right)'
            })
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ Fox Error: {e}")
        return []
