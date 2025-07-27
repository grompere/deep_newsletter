# This script is used to search the news API for the latest news on a given topic
# It then uses the Google Gemini API to summarize the news articles in a newsletter style report
# It then sends the report to the user via email

import os
import getpass
from dotenv import load_dotenv
import requests
import warnings
from datetime import datetime, timedelta
from google import genai
from google.genai import types

# Suppress the LibreSSL warning
warnings.filterwarnings('ignore', message='.*LibreSSL.*')

# Load environment variables from .env file
load_dotenv()

# Get Google Gemini API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Get News API key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# If API key is not in environment, prompt user to enter it
if not GOOGLE_API_KEY:
    print("GOOGLE API key not found in environment variables.")
    print("Please create a .env file with your GOOGLE_API_KEY or enter it below.")
    GOOGLE_API_KEY = getpass.getpass("Enter your Google API key: ")

if not NEWS_API_KEY:
    print("News API key not found in environment variables.")
    print("Please create a .env file with your NEWS_API_KEY or enter it below.")
    NEWS_API_KEY = getpass.getpass("Enter your News API key: ")

# Validate that we have an API key
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is required. Please set GOOGLE_API_KEY in your .env file or provide it when prompted.")

if not NEWS_API_KEY:
    raise ValueError("News API key is required. Please set NEWS_API_KEY in your .env file or provide it when prompted.")

# Get the latest news on the user's provided topic
topic = input("Enter a topic to research: ")
date = datetime.now() - timedelta(days=1)
date_formatted = date.strftime("%Y-%m-%d")

url = ('https://newsapi.org/v2/everything?'
       f'q={topic}&'
       f'from={date_formatted}&'
       'sortBy=popularity&'
       f'apiKey={NEWS_API_KEY}')

response = requests.get(url)

# Initialize the  model
client = genai.Client(
    api_key=os.environ.get("GOOGLE_API_KEY"),
)
model = "gemini-2.5-flash"

system_instruction = """
You are a professional journalist and researcher preparing a structured, data-driven report on behalf of your client. 

You will be given a json object with the following containing news articles on the user's provided topic.

Your task is to summarize the news articles in a newsletter style report.

The report should be in the following format:
- Title of the report
- Top 3 headlines with 1 sentence summary
- For each headline topic, 1-2 paragraphs of analysis
- Key takeaways
- Sources
"""

user_query = str(response.json())

response = client.models.generate_content(
    model=model,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction
    ),
    contents=user_query
)

print(response.text)