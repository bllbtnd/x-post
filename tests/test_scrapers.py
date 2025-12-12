"""Test all news scrapers to verify RSS feeds are working"""
from scrapers.neutral import scrape_ap
from scrapers.international_left import scrape_bbc, scrape_aljazeera, scrape_france24
from scrapers.international_right import scrape_fox
from scrapers.hungarian_left import scrape_telex, scrape_index, scrape_444
from scrapers.hungarian_right import scrape_mandiner, scrape_magyarnemzet


def test_all_scrapers():
    """Test all news scrapers and report results"""
    print("🧪 Testing All News Scrapers (RSS Feeds)\n")
    print("=" * 60)
    
    scrapers = [
        # International
        ("AP News (Neutral)", scrape_ap),
        ("BBC News (Center-Left)", scrape_bbc),
        ("Al Jazeera (Left)", scrape_aljazeera),
        ("France24 (Center-Left)", scrape_france24),
        ("Fox News (Right)", scrape_fox),
        # Hungarian
        ("Telex (HU-Left)", scrape_telex),
        ("Index (HU-Center)", scrape_index),
        ("444 (HU-Left)", scrape_444),
        ("Mandiner (HU-Right)", scrape_mandiner),
        ("Magyar Nemzet (HU-Right)", scrape_magyarnemzet),
    ]
    
    results = []
    total_articles = 0
    
    for source_name, scraper_func in scrapers:
        print(f"\n📰 Testing {source_name}...")
        try:
            articles = scraper_func()
            if articles:
                total_articles += len(articles)
                results.append((source_name, len(articles), True))
                print(f"   ✅ Success: {len(articles)} articles")
                # Show first 3 headlines as sample
                for i, article in enumerate(articles[:3], 1):
                    print(f"      {i}. {article['title'][:80]}...")
            else:
                results.append((source_name, 0, False))
                print(f"   ⚠️  No articles found")
        except Exception as e:
            results.append((source_name, 0, False))
            print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for _, _, success in results if success)
    failed = len(results) - successful
    
    print(f"\n✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print(f"📄 Total articles fetched: {total_articles}")
    
    if failed > 0:
        print("\n⚠️  Failed sources:")
        for name, count, success in results:
            if not success:
                print(f"   - {name}")
    
    print("\n" + "=" * 60)
    
    return successful == len(results)


if __name__ == "__main__":
    success = test_all_scrapers()
    exit(0 if success else 1)
