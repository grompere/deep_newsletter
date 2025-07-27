# This script is used to run deep research on a given topic
# It then uses the OpenAI API to run deep research on a topic and summarize the results in a newsletter style report

from openai import OpenAI
import os
import getpass
from dotenv import load_dotenv
import warnings
from datetime import datetime, timedelta
import threading
import time
import sys
from email_service.email_manager import EmailManager
from config.email_config import print_email_setup_instructions

# Suppress the LibreSSL warning
warnings.filterwarnings('ignore', message='.*LibreSSL.*')

# Load environment variables from .env file
load_dotenv()

# Global variable to control spinner
spinner_running = False

def spinner_animation():
    """Display a spinner animation while the model is thinking"""
    global spinner_running
    spinner_chars = ['/', '-', '\\', '|']
    i = 0
    
    while spinner_running:
        sys.stdout.write(f'\rThinking ... {spinner_chars[i]}')
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(spinner_chars)
    
    # Clear the spinner line
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def start_spinner():
    """Start the spinner animation in a separate thread"""
    global spinner_running
    spinner_running = True
    spinner_thread = threading.Thread(target=spinner_animation)
    spinner_thread.daemon = True
    spinner_thread.start()
    return spinner_thread

def stop_spinner():
    """Stop the spinner animation"""
    global spinner_running
    spinner_running = False

def format_report_for_email(report_text: str) -> str:
    """
    Format the report text for HTML email display
    
    Args:
        report_text: Raw report text from OpenAI
        
    Returns:
        str: HTML formatted report
    """
    import re
    
    def convert_markdown_links(text):
        """Convert markdown links to HTML links"""
        # Pattern to match markdown links: [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        def replace_link(match):
            link_text = match.group(1)
            link_url = match.group(2)
            return f'<a href="{link_url}" style="color: #007bff; text-decoration: none;">{link_text}</a>'
        
        return re.sub(pattern, replace_link, text)
    
    def convert_markdown_formatting(text):
        """Convert basic markdown formatting to HTML"""
        # Convert **bold** to <strong>
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        
        # Convert *italic* to <em>
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        
        # Convert `code` to <code>
        text = re.sub(r'`(.*?)`', r'<code style="background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: monospace;">\1</code>', text)
        
        return text
    
    # Split the report into lines
    lines = report_text.strip().split('\n')
    html_parts = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Convert markdown formatting first
        line = convert_markdown_formatting(line)
        
        # Convert markdown links
        line = convert_markdown_links(line)
        
        # Check if it's a title (usually in all caps or has special formatting)
        if line.isupper() or line.startswith('#') or len(line) < 100:
            html_parts.append(f'<h2 style="color: #007bff; margin-top: 20px; margin-bottom: 10px;">{line}</h2>')
        # Check if it's a headline (starts with number or bullet)
        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
            html_parts.append(f'<div class="headline"><h3>{line}</h3></div>')
        # Regular paragraph
        else:
            html_parts.append(f'<p style="margin-bottom: 15px; line-height: 1.6;">{line}</p>')
    
    return '\n'.join(html_parts)

def main():
    """Main function to run the deep research bot"""
    
    # Initialize email manager
    email_manager = EmailManager()
    
    # Show email setup instructions if email is not configured
    if not email_manager.is_available():
        print_email_setup_instructions()
    
    # Get OpenAI API key from environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # If API key is not in environment, prompt user to enter it
    if not OPENAI_API_KEY:
        print("OpenAI API key not found in environment variables.")
        print("Please create a .env file with your OPENAI_API_KEY or enter it below.")
        OPENAI_API_KEY = getpass.getpass("Enter your OpenAI API key: ")

    # Validate that we have an API key
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY in your .env file or provide it when prompted.")

    # Get the latest news on the user's provided topic
    topic = input("Enter a topic to research: ")
    date = datetime.now() - timedelta(days=1)
    date_cutoff = date - timedelta(days=7)
    date_formatted = date.strftime("%Y-%m-%d")
    date_cutoff_formatted = date_cutoff.strftime("%Y-%m-%d")

    # Initialize the OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_message = """
    You are a professional journalist and researcher preparing a structured, data-driven report on behalf of your client. 

    Your task is to research the user's provided topic and return a newsletter style report on news and trends in the topic within 
    the user's provided time frame. The report should be in a format that is easy to read and understand.

    The report should be in the following format:
    - Title
    - Top 3 headlines with 1 sentence summary for each headline
    - For each headline topic, max 200 words of analysis

    Be very concise and analytical. Avoid generalities, and ensure that each section is supported by by reputable sources.

    Constrain the output to within 1 week of the user's provided date. 
    If there is no news in the last week, return a message saying that there is no news in the last week.
    """

    user_query = f"Research the latest news and trends in the field of {topic} between {date_cutoff_formatted} and {date_formatted}"

    print(f"\n🔍 Researching: {topic}")
    print(f"📅 Date range: {date_cutoff_formatted} to {date_formatted}")
    print()

    # Start the spinner animation
    spinner_thread = start_spinner()

    try:
        response = client.responses.create(
          model="o4-mini-deep-research-2025-06-26",
          input=[
            {
              "role": "developer",
              "content": [
                {
                  "type": "input_text",
                  "text": system_message,
                }
              ]
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "input_text",
                  "text": user_query,
                }
              ]
            }
          ],
          reasoning={
            "summary": "auto"
          },
          tools=[
            {
              "type": "web_search_preview"
            }
          ]
        )
    finally:
        # Stop the spinner animation
        stop_spinner()

    # Get the research report
    report_text = response.output[-1].content[0].text
    
    # Display the report
    print("\n" + "="*60)
    print("RESEARCH REPORT")
    print("="*60)
    print(report_text)
    print("="*60)
    
    # Send email notification if configured
    if email_manager.is_available():
        print("\n📧 Sending email notification...")
        
        # Format the report for email
        html_content = format_report_for_email(report_text)
        
        # Send the email
        email_sent = email_manager.send_research_report(
            topic=topic,
            date=date_formatted,
            content=html_content
        )
        
        if email_sent:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email. Check your configuration.")
    else:
        print("\n💡 Tip: Configure email notifications to receive reports in your inbox!")
        print("   Add RESEND_API_KEY, EMAIL_FROM, and EMAIL_TO to your .env file.")

if __name__ == "__main__":
    main()