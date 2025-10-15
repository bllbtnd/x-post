"""API connection testing utilities"""
import os
import tweepy
import google.generativeai as genai
from gemini import get_best_gemini_model


def test_api_connections():
    """Test if API credentials are valid"""
    print("🔍 Testing API connections...\n")
    
    # Test Gemini
    try:
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        
        # List available models
        print("Available Gemini models:")
        available = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name.replace('models/', '')
                available.append(model_name)
                print(f"   - {model_name}")
        
        if not available:
            print("❌ No models available with your API key\n")
            return False
        
        # Test with best available model
        model_name = get_best_gemini_model()
        print(f"\n🧪 Testing with: {model_name}")
        test_model = genai.GenerativeModel(model_name)
        test_response = test_model.generate_content("Say 'OK' if you can read this")
        print(f"✅ Gemini API: Connected")
        print(f"   Response: {test_response.text.strip()}\n")
    except Exception as e:
        print(f"❌ Gemini API: Failed - {e}\n")
        return False
    
    # Test X API v2
    try:
        client = tweepy.Client(
            consumer_key=os.environ['X_API_KEY'],
            consumer_secret=os.environ['X_API_SECRET'],
            access_token=os.environ['X_ACCESS_TOKEN'],
            access_token_secret=os.environ['X_ACCESS_TOKEN_SECRET']
        )
        me = client.get_me()
        print(f"✅ X API v2: Connected")
        print(f"   Account: @{me.data.username}\n")
    except Exception as e:
        print(f"❌ X API v2: Failed - {e}\n")
        return False
    
    # Test NewsAPI if key exists
    news_api_key = os.environ.get('NEWS_API_KEY')
    if news_api_key:
        try:
            import requests
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ NewsAPI: Connected\n")
            else:
                print(f"⚠️  NewsAPI: Status {response.status_code}\n")
        except Exception as e:
            print(f"⚠️  NewsAPI: {e}\n")
    else:
        print("ℹ️  NewsAPI: Not configured (optional)\n")
    
    # Test Discord webhook if configured
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        try:
            import requests
            test_payload = {
                "content": "✅ Discord webhook test successful! X Bot is connected."
            }
            response = requests.post(webhook_url, json=test_payload, timeout=5)
            if response.status_code == 204:
                print(f"✅ Discord Webhook: Connected\n")
            else:
                print(f"⚠️  Discord Webhook: Status {response.status_code}\n")
        except Exception as e:
            print(f"⚠️  Discord Webhook: {e}\n")
    else:
        print("ℹ️  Discord Webhook: Not configured (optional)\n")
    
    return True
