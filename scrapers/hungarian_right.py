"""Hungarian right-leaning news scrapers"""
import requests
from bs4 import BeautifulSoup
from .utils import is_political_or_economic


def scrape_mandiner():
    """Scrape Mandiner (Right-wing Hungarian)"""
    try:
        response = requests.get("https://mandiner.hu", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        seen_titles = set()
        
        for headline in soup.find_all(['h2', 'h3', 'h4'])[:60]:
            title = headline.get_text(strip=True)
            if not title or len(title) < 15 or title in seen_titles:
                continue
            
            parent_link = headline.find_parent('a')
            url = None
            if parent_link and parent_link.get('href'):
                href = parent_link['href']
                url = href if href.startswith('http') else 'https://mandiner.hu' + href
            else:
                parent = headline.find_parent()
                if parent:
                    nearby_link = parent.find('a', href=True)
                    if nearby_link:
                        href = nearby_link['href']
                        url = href if href.startswith('http') else 'https://mandiner.hu' + href
            
            if not is_political_or_economic(url or '', title):
                continue
            
            seen_titles.add(title)
            articles.append({
                'title': title,
                'url': url,
                'source': 'Mandiner (HU-Right)'
            })
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ Mandiner Error: {e}")
        return []


def scrape_magyarnemzet():
    """Scrape Magyar Nemzet (Right-wing Hungarian)"""
    try:
        response = requests.get("https://magyarnemzet.hu", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        seen_titles = set()
        
        for headline in soup.find_all(['h2', 'h3', 'h4'])[:60]:
            title = headline.get_text(strip=True)
            if not title or len(title) < 15 or title in seen_titles:
                continue
            
            parent_link = headline.find_parent('a')
            url = None
            if parent_link and parent_link.get('href'):
                href = parent_link['href']
                url = href if href.startswith('http') else 'https://magyarnemzet.hu' + href
            else:
                parent = headline.find_parent()
                if parent:
                    nearby_link = parent.find('a', href=True)
                    if nearby_link:
                        href = nearby_link['href']
                        url = href if href.startswith('http') else 'https://magyarnemzet.hu' + href
            
            if not is_political_or_economic(url or '', title):
                continue
            
            seen_titles.add(title)
            articles.append({
                'title': title,
                'url': url,
                'source': 'Magyar Nemzet (HU-Right)'
            })
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ Magyar Nemzet Error: {e}")
        return []
