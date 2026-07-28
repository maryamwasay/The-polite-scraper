from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Website URL
BASE_URL = os.getenv("BASE_URL")

# Delay between requests (seconds)
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 2))

# Output folders
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
RAW_FOLDER = os.getenv("RAW_FOLDER")

# Log file
LOG_FILE = os.getenv("LOG_FILE")
