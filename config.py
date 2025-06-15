import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load links and payment information for the main application
API_TOKEN = os.getenv("API_TOKEN")
TELEGRAM_CHANNEL_LINK = os.getenv("TELEGRAM_CHANNEL_LINK")
FREE_GUIDE_LINK = os.getenv("FREE_GUIDE_LINK")
CONTACT_LINK = os.getenv("CONTACT_LINK")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
PAYMENT_SUM = os.getenv("PAYMENT_SUM")
PAYMENT_RECEIVER = os.getenv("PAYMENT_RECEIVER")
PAYMENT_TARGETS = os.getenv("PAYMENT_TARGETS")