# Deep Newsletter

AI-powered research bot that generates comprehensive newsletter reports on user-provided topics using two different approaches:

1. **Deep Research Method** (`deep_research_bot.py`) - Uses OpenAI's o4-mini-deep-research model for comprehensive analysis
2. **News API Method** (`search_api_bot.py`) - Uses News API + Google Gemini for news-focused summaries

## Features

- 🤖 **Two Research Methods**: Choose between deep research or news-focused analysis
- 📧 **Email Notifications**: Automatically sends research reports to your inbox
- 📊 **Structured Reports**: Newsletter-style output with headlines, analysis, and key takeaways
- 🎨 **Beautiful Emails**: HTML email templates with modern styling
- 🔗 **Working Links**: Properly formatted clickable links in emails

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```bash
# Required for deep_research_bot.py
OPENAI_API_KEY=your_openai_api_key_here

# Required for search_api_bot.py
GOOGLE_API_KEY=your_google_gemini_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

### 3. Get API Keys

- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **News API Key**: Get from [NewsAPI.org](https://newsapi.org/register)

### 4. Email Configuration (Optional)

To enable email notifications, add these to your `.env` file:

```env
# Email Configuration
RESEND_API_KEY=your_resend_api_key_here
EMAIL_FROM=your-verified-email@domain.com
EMAIL_FROM_NAME=Deep Newsletter
EMAIL_TO=recipient@example.com
```

**To get your Resend API key:**
1. Sign up at [Resend](https://resend.com)
2. Verify your domain or use the sandbox domain (`onboarding@resend.dev`)
3. Go to API Keys section and create a new key
4. Add the key to your `.env` file

**Test email functionality:**
```bash
python test_email.py
```

## Usage

### Method 1: Deep Research (Recommended)

For comprehensive, AI-powered research using OpenAI's latest deep research model:

```bash
python deep_research_bot.py
```

**Features:**
- Uses OpenAI's o4-mini-deep-research model
- Web search and code interpretation capabilities
- Email notifications with formatted reports

### Method 2: News API Research

For news-focused research using News API + Google Gemini:

```bash
python search_api_bot.py
```

**Features:**
- Searches recent news articles via News API
- Summarizes using Google Gemini 2.5 Flash
- Focuses on recent news and trends
- Lightweight and fast processing

## Output Format

Both methods generate structured newsletter reports with:

- **Title**: Descriptive report title
- **Top 3 Headlines**: Key findings with brief summaries
- **Analysis**: 1-2 paragraphs per headline topic
- **Key Takeaways**: Main insights and conclusions
- **Sources**: Attribution and references

## Troubleshooting

### Common Issues

1. **Rate Limit Errors**: 
   - Consider using the News API method for lighter research

2. **Missing API Keys**:
   - Ensure all required keys are in your `.env` file
   - Keys will be prompted for if not found in environment

3. **Token Usage High**:
   - The deep research method uses more tokens
   - Try the News API method for simpler queries

### Performance Tips

- Use specific, focused topics for better results
- The News API method is faster and uses fewer tokens
- Deep research is best for complex, multi-faceted topics

## Security

- The `.env` file is already added to `.gitignore`
- API keys are never logged or displayed
- Use environment variables for all sensitive data

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.