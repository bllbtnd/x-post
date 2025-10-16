"""Discord notification with message editing support"""
import os
import json
from datetime import datetime, UTC

MESSAGE_ID_FILE = 'discord_message_id.json'


def save_message_id(message_id):
    """Save Discord message ID for later editing"""
    try:
        with open(MESSAGE_ID_FILE, 'w') as f:
            json.dump({'message_id': message_id, 'timestamp': datetime.now(UTC).isoformat()}, f)
    except Exception as e:
        print(f"⚠️  Failed to save message ID: {e}")


def load_message_id():
    """Load Discord message ID"""
    try:
        if os.path.exists(MESSAGE_ID_FILE):
            with open(MESSAGE_ID_FILE, 'r') as f:
                data = json.load(f)
                return data.get('message_id')
    except:
        pass
    return None


def send_discord_scheduled_notification_editable(webhook_url, post_time_utc, delay_hours, delay_minutes, selected_topic, topic_source, tweet_text):
    """Send notification and return message ID for later editing"""
    try:
        import requests
        
        description = f"**📝 Scheduled Tweet Preview**\n\n**Selected Topic:** {selected_topic}\n\n**Generated Tweet:**\n{tweet_text}"
        
        embed = {
            "title": "🕒 X Bot - Tweet Scheduled",
            "description": description,
            "color": 16776960,  # Yellow/Orange color (pending)
            "fields": [
                {"name": "Topic Source", "value": topic_source.capitalize(), "inline": True},
                {"name": "Random Delay", "value": f"{delay_hours}h {delay_minutes}m", "inline": True},
                {"name": "Status", "value": "⏳ Waiting to post...", "inline": False},
                {"name": "Expected Post Time (UTC)", "value": post_time_utc.strftime('%Y-%m-%d %H:%M:%S UTC'), "inline": False}
            ],
            "footer": {"text": "X Bot Automation"},
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        payload = {"embeds": [embed], "wait": True}  # wait=True returns message details
        
        response = requests.post(f"{webhook_url}?wait=true", json=payload, timeout=10)
        
        if response.status_code == 200:
            message_data = response.json()
            message_id = message_data.get('id')
            save_message_id(message_id)
            print(f"✅ Discord scheduled notification sent (ID: {message_id})\n")
            return message_id
        else:
            print(f"⚠️  Discord scheduled notification failed: {response.status_code}\n")
            return None
            
    except Exception as e:
        print(f"⚠️  Discord scheduled notification error: {e}\n")
        return None


def update_discord_message_posted(webhook_url, message_id, tweet_data):
    """Edit the existing Discord message to show it's been posted"""
    try:
        import requests
        
        description = f"**✅ Tweet Posted Successfully**\n\n**Selected Topic:** {tweet_data['selected_topic']}\n\n**Posted Tweet:**\n{tweet_data['tweet_text']}"
        
        embed = {
            "title": "✅ X Bot - Tweet Posted",
            "description": description,
            "color": 5814783,  # Green color (success)
            "fields": [
                {"name": "Topic Source", "value": tweet_data['topic_source'].capitalize(), "inline": True},
                {"name": "Length", "value": f"{tweet_data['length']} chars", "inline": True},
                {"name": "Tweet ID", "value": tweet_data['tweet_id'], "inline": True},
                {"name": "Status", "value": "✅ Posted!", "inline": False},
                {"name": "Tweet URL", "value": f"[View on X/Twitter]({tweet_data['tweet_url']})", "inline": False},
                {"name": "Posted At (UTC)", "value": tweet_data['timestamp'], "inline": True},
                {"name": "Model Used", "value": tweet_data['model_name'], "inline": True}
            ],
            "footer": {"text": "X Bot Automation"},
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        payload = {"embeds": [embed]}
        
        # Edit the message using message ID
        edit_url = f"{webhook_url}/messages/{message_id}"
        response = requests.patch(edit_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Discord message updated (ID: {message_id})\n")
            return True
        else:
            print(f"⚠️  Discord message update failed: {response.status_code}\n")
            # Fallback: send new message
            print("📤 Sending new message instead...")
            return False
            
    except Exception as e:
        print(f"⚠️  Discord message update error: {e}\n")
        return False
