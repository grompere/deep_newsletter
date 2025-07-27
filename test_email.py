#!/usr/bin/env python3
"""
Test script for email functionality
Run this to test if your email configuration is working correctly
"""

import os
from dotenv import load_dotenv
from email_service.email_manager import EmailManager
from config.email_config import print_email_setup_instructions

# Load environment variables
load_dotenv()

def test_email_functionality():
    """Test the email functionality"""
    print("🧪 Testing Email Functionality")
    print("="*50)
    
    # Initialize email manager
    email_manager = EmailManager()
    
    # Check if email is configured
    if not email_manager.is_available():
        print("❌ Email not configured!")
        print_email_setup_instructions()
        return False
    
    print("✅ Email configuration found")
    
    # Test connection
    print("🔗 Testing connection to Resend...")
    if email_manager.test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed! Check your API key.")
        return False
    
    # Test email sending
    print("📧 Sending test email...")
    
    # Test with markdown content that includes links
    test_content = """
    # AI Research Report

    - **DeepMind's Gemini AI clinches gold at International Mathematical Olympiad** ([www.reuters.com](https://www.reuters.com/technology/ai-intelligencer-how-ai-won-math-gold-2025-07-24/#:~:text=In%20July%202025%2C%20Google%20DeepMind,benchmark%20for%20true%20AI%20reasoning)).

    This is a **bold text** with *italic text* and some `code` formatting.

    Here's another link: [OpenAI](https://openai.com) and [Google](https://google.com).

    1. **First headline** with a link to [GitHub](https://github.com)
    2. **Second headline** with *emphasis* and `inline code`
    """
    
    # Import the formatting function from the main bot
    from deep_research_bot import format_report_for_email
    
    # Format the content for email
    formatted_content = format_report_for_email(test_content)
    
    success = email_manager.send_research_report(
        topic="Markdown Test",
        date="2024-01-01",
        content=formatted_content
    )
    
    if success:
        print("✅ Test email sent successfully!")
        print("📬 Check your inbox for the test email.")
        return True
    else:
        print("❌ Failed to send test email!")
        return False

if __name__ == "__main__":
    test_email_functionality() 