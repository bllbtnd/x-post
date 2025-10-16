"""Discord notification functions"""
import os
from datetime import datetime, UTC


def send_discord_start_notification(post_time_utc, delay_hours, delay_minutes, selected_topic=None, topic_source=None):
    """Send notification when GitHub Action starts"""
    try:
        import requests
        
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        
        if not webhook_url:
            print("⚠️  Discord webhook not configured, skipping notification\n")
            return
        
        # Build description
        description = "GitHub Action has been triggered. Post will be created after random delay."
        if selected_topic:
            description += f"\n\n**Selected Topic:** {selected_topic}"
        
        # Build embed
        embed = {
            "title": "🚀 X Bot Started",
            "description": description,
            "color": 3447003,  # Blue color
            "fields": [
                {
                    "name": "Start Time (UTC)",
                    "value": datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC'),
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
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        # Add topic source field if available
        if topic_source:
            embed["fields"].insert(1, {
                "name": "Topic Source",
                "value": topic_source.capitalize(),
                "inline": True
            })
        
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
            "timestamp": datetime.now(UTC).isoformat()
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


def send_discord_scheduled_notification(post_time_utc, delay_hours, delay_minutes, selected_topic, topic_source, tweet_text):
    """Send notification when post is scheduled (before delay)"""
    try:
        import requests
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("⚠️  Discord webhook not configured, skipping notification\n")
            return
        description = f"**Scheduled Tweet Preview**\n\n**Selected Topic:** {selected_topic}\n\n**Generated Tweet:**\n{tweet_text}"
        embed = {
            "title": "📝 X Bot Scheduled Tweet",
            "description": description,
            "color": 3447003,  # Blue color
            "fields": [
                {"name": "Topic Source", "value": topic_source.capitalize(), "inline": True},
                {"name": "Random Delay", "value": f"{delay_hours}h {delay_minutes}m", "inline": True},
                {"name": "Expected Post Time (UTC)", "value": post_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'), "inline": False}
            ],
            "footer": {"text": "X Bot Automation"},
            "timestamp": datetime.now(UTC).isoformat()
        }
        payload = {"embeds": [embed]}
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Discord scheduled notification sent\n")
        else:
            print(f"⚠️  Discord scheduled notification failed: {response.status_code}\n")
    except Exception as e:
        print(f"⚠️  Discord scheduled notification error: {e}\n")


def send_discord_posted_notification(tweet_data):
    """Send notification to Discord webhook when tweet is posted (with tick)"""
    try:
        import requests
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("⚠️  Discord webhook not configured, skipping notification\n")
            return
        embed = {
            "title": "✅ X Bot Tweet Posted",
            "description": tweet_data['tweet_text'],
            "color": 5814783,  # Green color
            "fields": [
                {"name": "Tweet ID", "value": tweet_data['tweet_id'], "inline": True},
                {"name": "Length", "value": f"{tweet_data['length']} chars", "inline": True},
                {"name": "Topic Source", "value": tweet_data['topic_source'].capitalize(), "inline": True},
                {"name": "Selected Topic", "value": tweet_data['selected_topic'], "inline": False},
                {"name": "Tweet URL", "value": tweet_data['tweet_url'], "inline": False},
                {"name": "Posted At (UTC)", "value": tweet_data['timestamp'], "inline": True},
                {"name": "Model Used", "value": tweet_data['model_name'], "inline": True}
            ],
            "footer": {"text": "X Bot Automation"},
            "timestamp": datetime.now(UTC).isoformat()
        }
        payload = {"embeds": [embed]}
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Discord posted notification sent\n")
        else:
            print(f"⚠️  Discord posted notification failed: {response.status_code}\n")
    except Exception as e:
        print(f"⚠️  Discord posted notification error: {e}\n")
