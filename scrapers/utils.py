"""Utility functions for news scraping"""

def is_political_or_economic(url, title, source=''):
    """Check if article is about politics or economy"""
    if not url and not title:
        return False
    
    url_lower = url.lower() if url else ''
    title_lower = title.lower() if title else ''
    
    # Hungarian URL patterns
    hungarian_patterns = [
        '/belfold/', '/kulfold/', '/gazdasag/', '/g7/', '/politika/',
    ]
    
    # International URL patterns
    international_patterns = [
        '/politics/', '/business/', '/economy/', '/finance/',
        '/world/', '/international/', '/government/', '/election/',
        '/economic/', '/market/', '/trade/', '/policy/', '/markets/',
        '/legal/', '/breakingviews/', '/technology/',
    ]
    
    # Check URL
    for keyword in hungarian_patterns + international_patterns:
        if keyword in url_lower:
            return True
    
    # Universal keywords (works for Hungarian and English)
    keywords = [
        # Hungarian politics
        'kormány', 'parlament', 'miniszter', 'fidesz', 'dk', 'momentum',
        'orbán', 'választás', 'törvény',
        # Hungarian economy
        'gazdaság', 'infláció', 'forint', 'mnb', 'gdp', 'költségvetés',
        'adó', 'befektetés', 'bank', 'tőzsde', 'vállalat',
        # English politics
        'government', 'parliament', 'congress', 'senate', 'minister',
        'president', 'election', 'vote', 'law', 'policy', 'bill',
        'democrat', 'republican', 'labour', 'conservative', 'party',
        'trump', 'biden', 'putin', 'xi', 'modi', 'macron', 'scholz',
        'nato', 'eu', 'un', 'white house', 'kremlin', 'brussels',
        # English economy
        'economy', 'inflation', 'gdp', 'recession', 'market', 'stock',
        'trade', 'tariff', 'fed', 'central bank', 'interest rate',
        'investment', 'fiscal', 'budget', 'tax', 'unemployment',
        'currency', 'dollar', 'euro', 'yuan', 'imf', 'world bank',
        'oil', 'energy', 'prices', 'debt', 'bonds', 'equity',
    ]
    
    for keyword in keywords:
        if keyword in title_lower or keyword in url_lower:
            return True
    
    return False
