"""Tweet validation utilities"""


def validate_tweet(tweet):
    """Check if tweet meets requirements"""
    issues = []
    
    if len(tweet) > 280:
        issues.append(f"Too long: {len(tweet)} chars")
    if len(tweet) < 50:
        issues.append(f"Too short: {len(tweet)} chars")
    if tweet.count('#') > 2:
        issues.append(f"Too many hashtags: {tweet.count('#')}")
    if tweet.count('http') > 1:
        issues.append("Too many links")
    
    return issues
