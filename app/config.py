from pathlib import Path


# --------------------------------------------------
# Project directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE_DIR = BASE_DIR / "cache"
BOOK_CACHE_DIR = CACHE_DIR / "books"

OUTPUT_DIR = BASE_DIR / "output"


# --------------------------------------------------
# Target website
# --------------------------------------------------

BASE_URL = "https://books.toscrape.com/"
ROBOTS_URL = "https://books.toscrape.com/robots.txt"


# --------------------------------------------------
# Scraper settings
# --------------------------------------------------

USER_AGENT = (
    "FlyRankInternship-A9/1.0 "
    "(https://github.com/your-github-username/flyrank-a9-polite-scraper)"
)

REQUEST_TIMEOUT = 10

# Assignment requires at least 500 ms between real requests.
REQUEST_DELAY = 0.5

# Maximum retry attempts for temporary failures.
MAX_RETRIES = 1


# --------------------------------------------------
# Create required directories
# --------------------------------------------------

CACHE_DIR.mkdir(parents=True, exist_ok=True)
BOOK_CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)