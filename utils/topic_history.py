"""Topic history tracking to avoid duplicate posts"""
import os
import json
from datetime import datetime, timedelta, UTC


HISTORY_FILE = 'data/topic_history.json'
DAYS_TO_REMEMBER = 7  # Don't repeat topics from last 7 days


def load_topic_history():
    """Load previously used topics from JSON file"""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('topics', [])
    except:
        return []


def save_topic_history(topics):
    """Save topic history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({'topics': topics}, f, indent=2)
    except Exception as e:
        print(f"⚠️  Failed to save topic history: {e}")


def clean_old_topics(topics):
    """Remove topics older than DAYS_TO_REMEMBER"""
    cutoff_date = datetime.now(UTC) - timedelta(days=DAYS_TO_REMEMBER)
    
    cleaned = []
    for topic in topics:
        try:
            topic_date = datetime.fromisoformat(topic['timestamp'])
            if topic_date > cutoff_date:
                cleaned.append(topic)
        except:
            # Skip malformed entries
            continue
    
    return cleaned


def is_topic_recent(topic_text, history):
    """Check if topic was used recently"""
    # Clean the topic text for comparison
    topic_lower = topic_text.lower().strip()
    
    for entry in history:
        historical_topic = entry.get('topic', '').lower().strip()
        
        # Check for exact match or significant overlap
        if topic_lower == historical_topic:
            return True
        
        # Check if topics share significant keywords (>70% overlap)
        topic_words = set(topic_lower.split())
        hist_words = set(historical_topic.split())
        
        if len(topic_words) > 3 and len(hist_words) > 3:
            common = topic_words & hist_words
            overlap = len(common) / min(len(topic_words), len(hist_words))
            if overlap > 0.7:
                return True
    
    return False


def filter_recent_topics(available_topics):
    """Remove recently used topics from available list"""
    history = load_topic_history()
    history = clean_old_topics(history)
    
    if not history:
        print("ℹ️  No topic history found, all topics available\n")
        return available_topics
    
    # Filter out recent topics
    filtered = []
    removed = []
    
    for topic in available_topics:
        if is_topic_recent(topic, history):
            removed.append(topic)
        else:
            filtered.append(topic)
    
    if removed:
        print(f"🚫 Filtered out {len(removed)} recently used topics:")
        for topic in removed[:3]:  # Show first 3
            print(f"   - {topic}")
        if len(removed) > 3:
            print(f"   ... and {len(removed) - 3} more")
        print()
    
    # If all topics were filtered, return original list (edge case)
    if not filtered:
        print("⚠️  All topics recently used, allowing repeats\n")
        return available_topics
    
    print(f"✅ {len(filtered)} fresh topics available\n")
    return filtered


def add_topic_to_history(topic_text, source):
    """Add a topic to the history after posting"""
    history = load_topic_history()
    history = clean_old_topics(history)
    
    # Add new topic
    history.append({
        'topic': topic_text,
        'source': source,
        'timestamp': datetime.now(UTC).isoformat()
    })
    
    save_topic_history(history)
    print(f"💾 Added topic to history: {topic_text[:50]}...\n")
