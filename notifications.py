"""Discord notification functions"""
import os
from datetime import datetime


def send_discord_start_notification(post_time_utc, delay_hours, delay_minutes):
    """Send notification when GitHub Action starts"""
    try:
        import requests
        
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            print("⚠️  Discord webhook not configured, skipping notification\n")
            return
        
        # Build embed
        embed = {
            "title": "🚀 X Bot Started",
            "description": "GitHub Action has been triggered. Post will be created after random delay.",
            "color": 3447003,  # Blue color
            "fields": [
                {
                    "name": "Start Time (UTC)",
                    "value": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "inline": False
                },
                {
                    "name": "Random Delay",
                    "value": f"{delay_hours}h {delay_minutes}m",
                    "inline": True
                },
                {
                    "name": "Expected Post Time (UTC)",
                    "value": post_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "inline": False
                }
            ],
            "footer": {
                "text": "X Bot Automation"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print("✅ Discord start notification sent\n")
        else:
            print(f"⚠️  Discord start notification failed: {response.status_code}\n")
            
    except Exception as e:
        print(f"⚠️  Discord start notification error: {e}\n")


def send_discord_notification(tweet_data):
    """Send notification to Discord webhook when tweet is posted"""
    try:
        import requests
        
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            print("⚠️  Discord webhook not configured, skipping notification\n")
            return
        
        # Build embed
        embed = {
            "title": "✅ New Tweet Posted",
            "description": tweet_data['tweet_text'],
            "color": 5814783,  # Green color
            "fields": [
                {
                    "name": "Tweet ID",
                    "value": tweet_data['tweet_id'],
                    "inline": True
                },
                {
                    "name": "Length",
                    "value": f"{tweet_data['length']} chars",
                    "inline": True
                },
                {
                    "name": "Topic Source",
                    "value": tweet_data['topic_source'].capitalize(),
                    "inline": True
                },
                {
                    "name": "Selected Topic",
                    "value": tweet_data['selected_topic'],
                    "inline": False
                },
                {
                    "name": "Tweet URL",
                    "value": tweet_data['tweet_url'],
                    "inline": False
                },
                {
                    "name": "Posted At (UTC)",
                    "value": tweet_data['timestamp'],
                    "inline": True
                },
                {
                    "name": "Model Used",
                    "value": tweet_data['model_name'],
                    "inline": True
                }
            ],
            "footer": {
                "text": "X Bot Automation"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 204:
            print("✅ Discord post notification sent\n")
        else:
            print(f"⚠️  Discord post notification failed: {response.status_code}\n")
            
    except Exception as e:
        print(f"⚠️  Discord post notification error: {e}\n")
