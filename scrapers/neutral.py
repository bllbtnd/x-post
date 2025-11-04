"""AP News scraper (Neutral)"""
import requests
from bs4 import BeautifulSoup


def scrape_ap():
    """Scrape Associated Press (Neutral)"""
    try:
        articles = []
        seen_titles = set()
        
        # Try politics and business sections directly
        sections = [
            'https://apnews.com/politics',
            'https://apnews.com/business'
        ]
        
        for section_url in sections:
            response = requests.get(section_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # AP uses specific classes for article cards
            for card in soup.find_all('div', class_=lambda x: x and ('PagePromo' in x or 'FeedCard' in x))[:30]:
                link = card.find('a', href=True)
                if not link:
                    continue
                
                headline = link.find(['h2', 'h3', 'span'])
                if not headline:
                    # Try getting text from link itself
                    text = link.get_text(strip=True)
                    if len(text) < 20:
                        continue
                    title = text
                else:
                    title = headline.get_text(strip=True)
                
                if not title or len(title) < 20 or title in seen_titles:
                    continue
                
                href = link['href']
                url = f"https://apnews.com{href}" if href.startswith('/') else href
                
                # Skip non-articles
                if '/article/' not in url and '/hub/' in url:
                    continue
                
                seen_titles.add(title)
                articles.append({
                    'title': title,
                    'url': url,
                    'source': 'AP News (Neutral)'
                })
                
                if len(articles) >= 15:
                    break
            
            if len(articles) >= 15:
                break
        
        return articles
    except Exception as e:
        print(f"  ❌ AP Error: {e}")
        return []
