# X Automated Posting Bot

Automated Twitter/X bot that posts viral-optimized content daily using AI. Fetches trending topics, uses Gemini to select the best one, generates controversial tweets, and posts automatically.

## Features

- **Smart Topic Selection**: Fetches trending news via NewsAPI, lets Gemini AI pick the most viral-worthy topic
- **AI Tweet Generation**: Uses Gemini to write controversial, engaging tweets (200-280 chars)
- **Automated Scheduling**: Runs daily via GitHub Actions with randomized posting times
- **Duplicate Prevention**: Tracks last 7 days of topics to avoid repeating content
- **Fallback Topics**: Curated strategic topics if trending fetch fails
- **Multiple Testing Modes**: Dry run, connection testing, live posting

## Setup

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/x-post.git
cd x-post
pip install -r requirements.txt
```

### 2. Get API Keys

**Required:**
- **Gemini API**: https://ai.google.dev/gemini-api/docs/api-key (free tier: 50 requests/day)
- **X/Twitter API**: https://developer.x.com/en/portal/dashboard (free tier works)

**Optional:**
- **NewsAPI**: https://newsapi.org/ (free tier: 100 requests/day)

### 3. Local Testing

Create `.env` file:
```bash
GEMINI_API_KEY=your_gemini_key_here
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
X_ACCESS_TOKEN=your_x_access_token
X_ACCESS_TOKEN_SECRET=your_x_access_token_secret
NEWS_API_KEY=your_newsapi_key  # Optional
```

Test locally:
```bash
python main.py --dry-run           # Generate tweet without posting
python main.py --test-connection   # Verify all APIs work
python main.py                     # Post for real
```

### 4. GitHub Actions Setup

**Enable Actions:**
1. Go to repo **Settings** → **Actions** → **General**
2. Select "Allow all actions and reusable workflows"
3. Under "Workflow permissions" select "Read and write permissions"
4. Click **Save**

**Add Secrets:**
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each key:
   - `GEMINI_API_KEY`
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_TOKEN_SECRET`
   - `NEWS_API_KEY` (optional)

**Test Workflow:**
1. Go to **Actions** tab
2. Click "Post Daily Tweet" (left sidebar)
3. Click "Run workflow" → Run workflow
4. Watch it execute

## Configuration

### Posting Schedule

Edit `.github/workflows/daily_tweet.yml`:
```yaml
schedule:
  - cron: '0 12 * * *'  # Daily at 12:00 PM UTC
```

**Random Delay**: Bot adds 0-12 hours random delay after trigger. Adjust in `main.py`:
```python
max_delay = 43200  # 12 hours (change to: 1800=30min, 3600=1hr, 21600=6hr)
```

### Tweet Requirements

Edit prompt in `gemini.py` to customize tone/style:
```python
prompt = f"""Write a single tweet about: {selected_topic}

Requirements:
- 200-280 characters
- Strong opinion that splits audience 50/50
- Make ONE enemy clearly defined
- End with practical insight
- 1-2 emojis max
- British spelling
...
```

### Curated Topics

Create `trending_topics.txt` for manual topic curation (optional):
```
# Updated: 2025-10-15
Trump tariffs debate
AI regulation Europe
Housing market collapse
Remote work mandates
Crypto regulation
```

Bot checks this file first, then falls back to NewsAPI.

### Topic History & Duplicate Prevention

The bot automatically tracks used topics in `topic_history.json` to prevent posting about the same thing multiple times:

- Remembers topics for **7 days**
- Filters out topics with >70% keyword overlap
- Auto-commits history file via GitHub Actions
- If all topics are recent, will allow repeats (edge case)

To manually reset history:
```bash
echo '{"topics": []}' > topic_history.json
git add topic_history.json
git commit -m "Reset topic history"
git push
```

## File Structure
```
x-post/
├── .github/
│   └── workflows/
│       └── daily_tweet.yml    # GitHub Actions config
├── main.py                    # Main orchestration script
├── config.py                  # Environment & configuration
├── notifications.py           # Discord notifications
├── trending.py                # Topic fetching & selection
├── validation.py              # Tweet validation
├── gemini.py                  # AI model & generation
├── testing.py                 # API connection tests
├── topic_history.py           # Duplicate prevention
├── topic_history.json         # Recent topics tracking (auto-updated)
├── requirements.txt           # Dependencies
├── .env                       # Local API keys (gitignored)
├── .gitignore
├── README.md
├── test_tweets.txt           # Dry run output log
└── posted_tweets.txt         # Live post history log
```

## Usage

**Local:**
```bash
python main.py --dry-run           # Test without posting
python main.py --test-connection   # Check API connectivity
python main.py                     # Post immediately (no delay)
```

**Automated:**
- Runs daily at scheduled time (default: 12:00 PM UTC ± 0-6 hours)
- Check **Actions** tab for run history
- View logs to debug failures

## Troubleshooting

**"No workflow runs yet"**
- Actions not enabled in Settings → Actions → General
- YAML syntax error (test at yamllint.com)

**"Quota exceeded" error**
- Free Gemini tier = 50 requests/day (25 tweets since bot uses 2 calls)
- Upgrade to paid Gemini tier OR reduce to 1 API call by removing topic selection

**"403 Forbidden" from X API**
- Elevated access required for some endpoints ($100/month)
- NewsAPI or manual curation works fine on free tier

**"ResourceExhausted" error**
- Wait 24 hours for quota reset
- Upgrade to paid API tier
- Stop testing so much

**Posts not appearing**
- Check Actions logs for errors
- Verify X API credentials in Secrets
- Test locally first with `--dry-run`

## Costs

**Free tier (50 tweets/month max):**
- Gemini: Free tier (50 requests/day)
- X API: Free
- NewsAPI: Free (100 requests/day)
- GitHub Actions: Free (2000 minutes/month)

**Paid tier (unlimited):**
- Gemini Pro: ~$0.10-0.50/day (~$3-15/month)
- X API: Free (or $100/month for premium features)
- NewsAPI: Free works fine
- GitHub Actions: Free

## License

MIT - Do whatever you want with it.

## Warning

**Don't be stupid:**
- Monitor your bot - automated posting can get your account banned
- Follow X's automation rules
- Don't spam
- This generates controversial content by design - review output regularly
- You're responsible for what your bot posts

## Contributing

PRs welcome. Keep it simple and functional.