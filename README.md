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

The bot can automatically send research reports to your email inbox. This feature is optional but highly recommended.

#### Step-by-Step Email Setup:

**1. Create a Resend Account:**
- Go to [Resend.com](https://resend.com) and sign up for a free account
- Verify your email address

**2. Get Your API Key:**
- In your Resend dashboard, go to "API Keys" section
- Click "Create API Key"
- Copy the generated API key (it starts with `re_`)

**3. Configure Your Email Settings:**

You have two options for the `EMAIL_FROM` address:

**Option A: Use Resend's Sandbox Domain (Recommended for Testing)**
```env
EMAIL_FROM=onboarding@resend.dev
```

**Option B: Use Your Own Domain (For Production)**
- In Resend dashboard, go to "Domains" section
- Add and verify your domain (e.g., `yourdomain.com`)
- Use your verified email: `your-email@yourdomain.com`

**4. Update Your `.env` File:**
```env
# Email Configuration
RESEND_API_KEY=re_your_actual_api_key_here
EMAIL_FROM=onboarding@resend.dev  # or your verified email
EMAIL_FROM_NAME=Deep Newsletter
EMAIL_TO=your-email@gmail.com
```

**5. Test Your Email Configuration:**
```bash
python test_email.py
```

You should see:
```
✅ Email configuration found
✅ Connection successful!
✅ Test email sent successfully!
📬 Check your inbox for the test email.
```

**6. Troubleshooting Email Issues:**

- **"Email not configured"**: Check that all email variables are set in `.env`
- **"Connection failed"**: Verify your Resend API key is correct
- **"Failed to send email"**: 
  - Check your internet connection
  - Ensure `EMAIL_FROM` is verified in Resend
  - Try using `onboarding@resend.dev` for testing
- **Email not received**: Check spam folder and verify `EMAIL_TO` address

**7. Email Features:**
- ✅ Beautiful HTML formatting with professional styling
- ✅ Clickable links from research sources
- ✅ Responsive design (works on mobile and desktop)
- ✅ Fallback plain text for email clients that don't support HTML
- ✅ Automatic markdown to HTML conversion

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

**What happens when you run the bot:**
1. Enter your research topic when prompted
2. The AI generates a comprehensive report
3. The report is displayed in the console
4. **If email is configured**: A beautifully formatted email is automatically sent to your inbox
5. **If email is not configured**: You'll see a helpful tip about setting up email notifications

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

4. **Email Issues**:
   - **"Email service not configured"**: Add email variables to your `.env` file
   - **"Connection failed"**: Check your Resend API key
   - **"Failed to send email"**: Verify your `EMAIL_FROM` address is verified in Resend
   - **Email not received**: Check spam folder and verify `EMAIL_TO` address
   - **Test email fails**: Run `python test_email.py` to debug email configuration

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