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
        time.sleep(0.2)
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
date_formatted = date.strftime("%Y-%m-%d")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

system_message = """
You are a professional journalist and researcher preparing a structured, data-driven report on behalf of your client. 

Your task is to research the user's provided topic and return a newsletter style report on news and trends in the topic within 
the user's provided time frame. The report should be in a format that is easy to read and understand.

The report should be in the following format:
- Title
- Top 3 headlines with 1 sentence summary
- For each headline topic, 1-2 paragraphs of analysis
- Key takeaways
- Sources

Be analytical, avoid generalities, and ensure that each section is supported by by reputable sources.
"""

user_query = f"Research the latest news and trends in the field of {topic} on {date_formatted}"

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
        },
        {
          "type": "code_interpreter",
          "container": {
            "type": "auto",
            "file_ids": []
          }
        }
      ]
    )
finally:
    # Stop the spinner animation
    stop_spinner()

print(response.output[-1].content[0].text)