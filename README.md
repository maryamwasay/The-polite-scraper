# FlyRank A9 - The Polite Scraper

A production-style Python web scraper built for the FlyRank Backend AI Engineering track.  
The project scrapes structured book data from [Books to Scrape](https://books.toscrape.com/) while implementing polite crawling, caching, validation, error handling, and reporting.

## Features

- Polite sequential web scraping with configurable request delays
- Catalogue pagination and book URL discovery
- URL normalization and deduplication
- Book detail-page scraping
- HTML parsing and structured data extraction
- Data validation
- Local response caching to avoid unnecessary requests
- Cache-hit tracking and cache clearing
- HTTP error handling and failure isolation
- Structured error reporting
- JSON and CSV output
- Run statistics and execution timing
- Automated tests with `pytest`

## Scraping Pipeline

```text
Catalogue Pages
      ↓
Discover Book URLs
      ↓
Normalize & Deduplicate
      ↓
Fetch Detail Pages
      ↓
Cache Hit / HTTP Request
      ↓
Parse HTML
      ↓
Validate Data
      ↓
Valid Records / Errors
      ↓
JSON + CSV + Reports
Project Structure
flyrank-a9-polite-scraper/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── models.py
│   └── ...
│
├── tests/
├── output/
│   ├── books.json
│   ├── books.csv
│   ├── errors.json
│   └── run-report.json
│
├── cache/
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Technology Stack
Python
Requests
BeautifulSoup
lxml
Pydantic
pytest
JSON / CSV
python-dotenv
Installation

Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
Run the Scraper
python run.py

The scraper processes catalogue pages, discovers unique book URLs, fetches detail pages, validates records, and generates output files.

Verified Successful Run
Catalogue pages: 3
Discovered URLs: 60
Valid records: 60
Invalid records: 0
Failed pages: 0
Cache hits: 62
Pages fetched: 1

A cached run also successfully produced:

Catalogue pages: 3
Discovered URLs: 60
Valid records: 60
Invalid records: 0
Failed pages: 0
Cache hits: 63
Pages fetched: 0
Duration: 0.76 seconds
Caching

Responses are stored locally in the cache/ directory.

Cached requests appear as:

CACHE HIT: https://books.toscrape.com/
CACHE HIT: https://books.toscrape.com/catalogue/page-2.html
CACHE HIT: https://books.toscrape.com/catalogue/page-3.html

To clear the cache in PowerShell:

Remove-Item -Recurse -Force .\cache\*

Then run:

python run.py
Error Handling

The scraper was tested with an intentionally invalid URL:

https://books.toscrape.com/catalogue/this-page-does-not-exist-999999/index.html

It correctly returned:

FAILED: ... status=404

The scraper continued processing the remaining URLs instead of crashing.

Result:

Catalogue pages: 3
Discovered URLs: 60
Valid records: 59
Invalid records: 0
Failed pages: 1

Errors are stored in:

output/errors.json
Output Files
output/
├── books.json        # Scraped book records in JSON
├── books.csv         # Scraped book records in CSV
├── errors.json       # Invalid records and failed pages
└── run-report.json   # Complete execution statistics

Example run-report.json:

{
  "started_at": "2026-08-10T11:22:37.348882+00:00",
  "finished_at": "2026-08-10T11:22:38.100951+00:00",
  "duration_seconds": 0.76,
  "catalogue_pages": 3,
  "discovered_urls": 60,
  "detail_pages": 60,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
Testing

Run the automated test suite:

pytest -q

Expected result:

12 passed
Verify JSON Reports

Run report:

python -m json.tool output/run-report.json

Error report:

python -c "import json; d=json.load(open('output/errors.json', encoding='utf-8')); print(json.dumps(d, indent=2))"

Expected successful error report:

{
  "invalid_records": [],
  "failed_pages": []
}
Assignment Verification

The implementation covers:

Catalogue crawling and pagination
URL discovery, normalization, and deduplication
Detail-page scraping
Polite request handling
Local caching
Data validation
HTTP error handling
Failure isolation
Error reporting
JSON and CSV output
Run statistics
Automated testing

Final verified result:

60 discovered URLs
60 valid records
0 invalid records
0 failed pages
12 automated tests passed
Git Submission

Before submission, make sure sensitive/local files are excluded:

venv/
__pycache__/
*.pyc
.env

Check the repository:

git status

Commit and push:

git add .
git commit -m "Complete FlyRank A9 polite scraper"
git push
Author

Maryam Wasay
FlyRank Backend AI Engineering Track
Assignment A9 - The Polite Scraper


This version is much more suitable for GitHub: **short enough to read, but still documents all the important assignment features and your verification results.**
