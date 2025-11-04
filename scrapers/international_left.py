"""International left-leaning news scrapers"""
import requests
from bs4 import BeautifulSoup
from .utils import is_political_or_economic


def scrape_bbc():
    """Scrape BBC News (Center-left)"""
    try:
        articles = []
        seen_titles = set()
        
        sections = [
            'https://www.bbc.com/news/world',
            'https://www.bbc.com/news/business'
        ]
        
        for section_url in sections:
            response = requests.get(section_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for headline in soup.find_all(['h2', 'h3'])[:30]:
                title = headline.get_text(strip=True)
                if not title or len(title) < 20 or title in seen_titles:
                    continue
                
                parent = headline.find_parent('a')
                if not parent or not parent.get('href'):
                    continue
                
                href = parent['href']
                url = f"https://www.bbc.com{href}" if href.startswith('/') else href
                
                if '/news/' not in url:
                    continue
                
                seen_titles.add(title)
                articles.append({
                    'title': title,
                    'url': url,
                    'source': 'BBC News (Center-Left)'
                })
                
                if len(articles) >= 15:
                    break
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ BBC Error: {e}")
        return []


def scrape_aljazeera():
    """Scrape Al Jazeera (Left-leaning)"""
    try:
        articles = []
        seen_titles = set()
        
        sections = [
            'https://www.aljazeera.com/news/',
            'https://www.aljazeera.com/economy/'
        ]
        
        for section_url in sections:
            response = requests.get(section_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True)[:40]:
                headline_elem = link.find(['h3', 'h2', 'span'])
                if not headline_elem:
                    continue
                
                title = headline_elem.get_text(strip=True)
                if not title or len(title) < 20 or title in seen_titles:
                    continue
                
                url = link['href']
                if url.startswith('/'):
                    url = f"https://www.aljazeera.com{url}"
                
                if not any(x in url for x in ['/news/', '/economy/']):
                    continue
                
                seen_titles.add(title)
                articles.append({
                    'title': title,
                    'url': url,
                    'source': 'Al Jazeera (Left)'
                })
                
                if len(articles) >= 15:
                    break
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ Al Jazeera Error: {e}")
        return []


def scrape_france24():
    """Scrape France24 (Center-left)"""
    try:
        articles = []
        seen_titles = set()
        
        response = requests.get("https://www.france24.com/en/", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for link in soup.find_all('a', href=True)[:60]:
            headline = link.find(['h2', 'h3', 'h4'])
            if not headline:
                continue
            
            title = headline.get_text(strip=True)
            if not title or len(title) < 20 or title in seen_titles:
                continue
            
            href = link['href']
            url = f"https://www.france24.com{href}" if href.startswith('/') else href
            
            if not is_political_or_economic(url, title):
                continue
            
            seen_titles.add(title)
            articles.append({
                'title': title,
                'url': url,
                'source': 'France24 (Center-Left)'
            })
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ France24 Error: {e}")
        return []
