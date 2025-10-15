"""Configuration and environment management"""
import os
import sys
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# Test mode flag - set via command line
DRY_RUN = '--dry-run' in sys.argv or '--test' in sys.argv
TEST_CONNECTION = '--test-connection' in sys.argv

def get_env_var(key, required=True):
    """Get environment variable with optional requirement check"""
    value = os.environ.get(key)
    if required and not value:
        raise KeyError(f"Missing required environment variable: {key}")
    return value

def get_api_credentials():
    """Get all API credentials from environment"""
    return {
        'gemini_api_key': get_env_var('GEMINI_API_KEY'),
        'x_api_key': get_env_var('X_API_KEY'),
        'x_api_secret': get_env_var('X_API_SECRET'),
        'x_access_token': get_env_var('X_ACCESS_TOKEN'),
        'x_access_token_secret': get_env_var('X_ACCESS_TOKEN_SECRET'),
        'news_api_key': get_env_var('NEWS_API_KEY', required=False),
        'discord_webhook_url': get_env_var('DISCORD_WEBHOOK_URL', required=False)
    }
