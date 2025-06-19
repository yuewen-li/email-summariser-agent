import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Microsoft Graph API settings
OUTLOOK_CLIENT_ID = os.getenv('OUTLOOK_CLIENT_ID')  # From Azure App Registration
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

# Email settings
NEWSLETTER_FILTERS = [
    "dan@tldrnewsletter.com",
]

# Scheduling settings
DAILY_RUN_TIME = "08:00"  # Run at 8 AM daily

# Summarization settings
MAX_SUMMARY_LENGTH = 200  # Maximum words per summary
MAX_EMAILS_PER_DAY = 10   # Maximum number of emails to process per day 