# Deep Newsletter

AI-powered research bot that generates comprehensive newsletter reports on any topic using two different approaches:

1. **Deep Research** (`deep_research_bot.py`) - OpenAI's o4-mini-deep-research model for comprehensive analysis
2. **News API** (`search_api_bot.py`) - News API + Google Gemini for recent news summaries

## Features

- 🤖 **Two Research Methods**: Deep research or news-focused analysis
- 📧 **Email Reports**: Automatically sends formatted reports to your inbox
- 📊 **Newsletter Format**: Structured reports with headlines, analysis, and takeaways
- ⚙️ **Modern Configuration**: Type-safe environment variable management

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:

```bash
# Required for deep research
OPENAI_API_KEY=your_openai_api_key_here

# Required for news research  
GOOGLE_API_KEY=your_google_gemini_api_key_here
NEWS_API_KEY=your_news_api_key_here

# Optional: Email notifications
RESEND_API_KEY=re_your_resend_api_key_here
EMAIL_FROM=onboarding@resend.dev
EMAIL_TO=your-email@gmail.com
```

### 3. Get API Keys
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- **News API**: [newsapi.org/register](https://newsapi.org/register)
- **Resend** (optional): [resend.com](https://resend.com)

### 4. Run
```bash
# Deep research (recommended)
python deep_research_bot.py

# News-focused research
python search_api_bot.py
```

## Email Setup (Optional)

For email notifications:

1. **Create Resend account** at [resend.com](https://resend.com)
2. **Get API key** from dashboard (starts with `re_`)
3. **Add to .env**:
   ```bash
   RESEND_API_KEY=re_your_key_here
   EMAIL_FROM=onboarding@resend.dev  # or your verified domain
   EMAIL_TO=your-email@gmail.com
   ```
4. **Test**: `python test_email.py`

## Troubleshooting

**Configuration Issues:**
- Check `.env` file format and required variables
- Ensure email addresses contain "@"

**API Issues:**
- Verify API keys are correct and active
- Check rate limits (try News API method for lighter usage)

**Email Issues:**
- Run `python test_email.py` to debug
- Use `onboarding@resend.dev` for testing
- Check spam folder

## License

MIT License - see [LICENSE](LICENSE) file for details.