"""X Bot - Automated Twitter posting with AI-generated content"""
import tweepy
import random
import sys
import time
from datetime import datetime, timedelta, UTC

# Import our modules
from config import DRY_RUN, TEST_CONNECTION
from notifications import (
    send_discord_scheduled_notification,
    send_discord_posted_notification,
    send_discord_start_notification,  # legacy, can be removed later
    send_discord_notification         # legacy, can be removed later
)
from trending import get_trending_topics, load_curated_trends, select_best_topic
from validation import validate_tweet
from gemini import configure_gemini, generate_tweet
from testing import test_api_connections
from topic_history import filter_recent_topics, add_topic_to_history


def main():
    print("=" * 60)
    print("X AUTOMATED POSTING SCRIPT")
    print("=" * 60)
    
    if DRY_RUN:
        print("🧪 DRY RUN MODE - Will NOT post to X\n")
    else:
        print("🚀 LIVE MODE - Will post to X\n")
    
    # Test connections first
    if TEST_CONNECTION:
        if test_api_connections():
            print("✅ All API connections working!\n")
            return
        else:
            print("❌ API connection failed. Fix credentials.\n")
            sys.exit(1)
    
    # Configure Gemini
    try:
        model, model_name = configure_gemini()
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
        print("Make sure your .env file has all required keys.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Gemini configuration failed: {e}")
        sys.exit(1)
    
    # Configure X API v2 (for posting)
    try:
        import os
        client = tweepy.Client(
            consumer_key=os.environ['X_API_KEY'],
            consumer_secret=os.environ['X_API_SECRET'],
            access_token=os.environ['X_ACCESS_TOKEN'],
            access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET']
        )
    except KeyError as e:
        print(f"❌ Missing environment variable: {e}")
        sys.exit(1)
    
    # Fetch trending topics
    print("📊 Fetching trending topics...")
    
    # Try multiple sources
    all_topics = []
    
    # 1. Try curated file first (best quality)
    curated = load_curated_trends()
    if curated:
        print(f"✅ Loaded {len(curated)} curated topics")
        all_topics.extend(curated)
    
    # 2. Try NewsAPI or other services
    trending = get_trending_topics()
    if trending:
        print(f"✅ Found {len(trending)} trending topics from news")
        all_topics.extend(trending[:15])
    
    # Check if we have any topics at all
    if not all_topics:
        print("❌ No topics available. Add topics to trending_topics.txt or configure NewsAPI.\n")
        sys.exit(1)
    
    # Filter out recently used topics
    all_topics = filter_recent_topics(all_topics)
    
    if not all_topics:
        print("❌ All topics recently used. Add more topics or wait.\n")
        sys.exit(1)
    
    # DISPLAY ALL TOPICS BEING SENT TO GEMINI
    print(f"\n{'='*60}")
    print(f"ALL TOPICS SENT TO GEMINI FOR SELECTION ({len(all_topics)} total):")
    print(f"{'='*60}")
    
    for i, topic in enumerate(all_topics, 1):
        # Mark if it's from curated file or news API
        if curated and topic in curated:
            print(f"   {i}. 📋 {topic}")
        else:
            print(f"   {i}. 🔥 {topic}")
    
    print(f"{'='*60}\n")
    print("Legend: 🔥 = News trending | 📋 = Curated topic\n")
    
    # STEP 1: Let Gemini choose the best topic BEFORE delay
    selected_topic = select_best_topic(model, all_topics)
    
    print(f"✅ Gemini selected: {selected_topic}\n")
    
    # Determine source
    if curated and selected_topic in curated:
        topic_source = "curated"
    else:
        topic_source = "trending"
    
    # STEP 2: Generate tweet on the selected topic (before delay)
    tweet = generate_tweet(model, selected_topic, all_topics)

    # Calculate random delay and post time
    delay = 0
    post_time_utc = datetime.now(UTC)
    if not (DRY_RUN or TEST_CONNECTION):
        max_delay = 21600
        delay = random.randint(0, max_delay)
        post_time_utc = datetime.now(UTC) + timedelta(seconds=delay)
    delay_hours = delay // 3600
    delay_minutes = (delay % 3600) // 60

    # Send scheduled notification with tweet preview (only for real posts)
    if not (DRY_RUN or TEST_CONNECTION):
        print(f"⏱️  Random delay: {delay_hours}h {delay_minutes}m")
        print(f"   Will post at: {post_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"   Current time: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        send_discord_scheduled_notification(
            post_time_utc, delay_hours, delay_minutes, selected_topic, topic_source, tweet
        )
        print(f"⏳ Waiting {delay_hours}h {delay_minutes}m...\n")
        time.sleep(delay)
        print(f"✅ Delay complete! Posting now at {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}...\n")
    
    # Validate tweet
    issues = validate_tweet(tweet)
    if issues:
        print("⚠️  Validation warnings:")
        for issue in issues:
            print(f"   - {issue}")
        print()
    else:
        print("✅ Tweet validation passed\n")
    
    # Post to X (or skip if dry run)
    if DRY_RUN:
        print("🧪 DRY RUN: Would post this tweet to X")
        print("   Run without --dry-run or --test to post for real\n")
        
        # Save to file for review
        with open('test_tweets.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{datetime.now(UTC)} | Source: {topic_source} | Topic: {selected_topic}\n")
            f.write(f"{tweet}\n")
            f.write("-" * 60 + "\n")
        print("💾 Saved to test_tweets.txt for review\n")
        
    else:
        print("📤 Posting to X...")
        result = client.create_tweet(text=tweet)
        tweet_id = result.data['id']
        tweet_url = f"https://x.com/i/web/status/{tweet_id}"
        
        print(f"✅ Posted successfully!")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   URL: {tweet_url}\n")
        timestamp = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')
        with open('posted_tweets.txt', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {tweet_id} | {topic_source} | {selected_topic} | {tweet}\n")
        add_topic_to_history(selected_topic, topic_source)
        tweet_data = {
            'tweet_text': tweet,
            'tweet_id': tweet_id,
            'tweet_url': tweet_url,
            'length': len(tweet),
            'topic_source': topic_source,
            'selected_topic': selected_topic,
            'timestamp': timestamp,
            'model_name': model_name
        }
        send_discord_posted_notification(tweet_data)
    


if __name__ == "__main__":
    main()
