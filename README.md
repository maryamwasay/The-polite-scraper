# FlyRank A9 - The Polite Scraper

A production-style, polite web scraper built in Python for extracting book data from [Books to Scrape](https://books.toscrape.com/).

The scraper demonstrates:

- Respectful crawling with request delays
- Catalogue pagination
- Detail-page discovery
- URL normalization and deduplication
- HTTP error handling
- Local response caching
- Retry and failure handling
- Structured data validation
- JSON/CSV output
- Run statistics and reporting
- Automated tests with pytest

---

## Project Structure

```text
flyrank-a9-polite-scraper/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── models.py
│   ├── cache.py
│   ├── crawler.py
│   └── utils.py
│
├── tests/
│   ├── test_cache.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   └── test_crawler.py
│
├── output/
│   ├── books.json
│   ├── books.csv
│   ├── errors.json
│   └── run-report.json
│
├── cache/
│
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
