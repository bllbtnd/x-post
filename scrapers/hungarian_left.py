"""Hungarian left-leaning news scrapers"""
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from .utils import is_political_or_economic


def scrape_telex():
    """Scrape Telex.hu (Left-leaning)"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print("  Loading...")
            page.goto("https://telex.hu", wait_until="domcontentloaded", timeout=30000)
            
            try:
                if page.locator('button:has-text("ELFOGADÁS ÉS BEZÁRÁS")').count() > 0:
                    page.locator('button:has-text("ELFOGADÁS ÉS BEZÁRÁS")').first.click(timeout=2000)
                time.sleep(2)
            except:
                pass
            
            time.sleep(3)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            time.sleep(1)
            
            html = page.content()
            browser.close()
            
            soup = BeautifulSoup(html, 'html.parser')
            articles = []
            seen_titles = set()
            
            items = soup.find_all(class_=lambda x: x and ('latest' in str(x).lower() or 'article' in str(x).lower()))
            
            for item in items[:50]:
                for link in item.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    if not text or len(text) < 20 or text in seen_titles:
                        continue
                    
                    href = link['href']
                    url = href if href.startswith('http') else 'https://telex.hu' + href
                    
                    if not is_political_or_economic(url, text):
                        continue
                    
                    seen_titles.add(text)
                    articles.append({
                        'title': text,
                        'url': url,
                        'source': 'Telex (HU-Left)'
                    })
                    
                    if len(articles) >= 15:
                        break
                if len(articles) >= 15:
                    break
            
            return articles
    except Exception as e:
        print(f"  ❌ Telex Error: {e}")
        return []


def scrape_index():
    """Scrape Index.hu (Center-left)"""
    try:
        response = requests.get("https://index.hu", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        seen_titles = set()
        
        for headline in soup.find_all(['h2', 'h3'])[:50]:
            title = headline.get_text(strip=True)
            if not title or len(title) < 15 or title in seen_titles:
                continue
            
            parent_link = headline.find_parent('a')
            url = None
            if parent_link and parent_link.get('href'):
                href = parent_link['href']
                url = href if href.startswith('http') else 'https://index.hu' + href
            
            if not is_political_or_economic(url or '', title):
                continue
            
            seen_titles.add(title)
            articles.append({
                'title': title,
                'url': url,
                'source': 'Index (HU-Center)'
            })
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ Index Error: {e}")
        return []


def scrape_444():
    """Scrape 444.hu (Left-leaning)"""
    try:
        response = requests.get("https://444.hu", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = []
        seen_titles = set()
        
        for headline in soup.find_all(['h1', 'h2', 'h3', 'h4'])[:60]:
            title = headline.get_text(strip=True)
            if not title or len(title) < 15 or title in seen_titles:
                continue
            
            parent_link = headline.find_parent('a')
            url = None
            
            if parent_link and parent_link.get('href'):
                href = parent_link['href']
                url = href if href.startswith('http') else 'https://444.hu' + href
            else:
                parent = headline.find_parent()
                if parent:
                    nearby_link = parent.find('a', href=True)
                    if nearby_link:
                        href = nearby_link['href']
                        url = href if href.startswith('http') else 'https://444.hu' + href
            
            if is_political_or_economic(url or '', title):
                seen_titles.add(title)
                articles.append({
                    'title': title,
                    'url': url,
                    'source': '444 (HU-Left)'
                })
                
                if len(articles) >= 15:
                    break
        
        return articles
    except Exception as e:
        print(f"  ❌ 444 Error: {e}")
        return []
