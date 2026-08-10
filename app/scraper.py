from pathlib import Path
from typing import Any

from .config import (
    BASE_URL,
    BOOK_CACHE_DIR,
    CACHE_DIR,
)
from .fetcher import Fetcher
from .normalizer import normalize_record
from .parser import (
    parse_book,
    parse_catalogue_links,
    parse_next_page,
)
from .validator import validate_record


class PoliteScraper:

    def __init__(self):
        self.fetcher = Fetcher()

        self.failed_pages: list[dict[str, Any]] = []

        self.invalid_records: list[dict[str, Any]] = []

    # --------------------------------------------------
    # Catalogue discovery
    # --------------------------------------------------

    def discover_books(self):

        current_url = BASE_URL

        catalogue_pages = []

        book_urls = []

        for page_number in range(1, 4):

            cache_path = (
                CACHE_DIR
                / f"catalogue-page-{page_number}.html"
            )

            html, source, status = (
                self.fetcher.fetch(
                    current_url,
                    cache_path,
                )
            )

            if html is None:

                self.failed_pages.append(
                    {
                        "url": current_url,
                        "type": "catalogue",
                        "status": status,
                    }
                )

                break

            catalogue_pages.append(
                current_url
            )

            links = parse_catalogue_links(
                html,
                current_url,
            )

            book_urls.extend(
                links
            )

            next_url = parse_next_page(
                html,
                current_url,
            )

            if not next_url:
                break

            current_url = next_url

        # Remove duplicates while preserving order.
        unique_urls = list(
            dict.fromkeys(book_urls)
        )

        return (
            catalogue_pages,
            unique_urls,
        )

    # --------------------------------------------------
    # Cache filename for detail pages
    # --------------------------------------------------

    def book_cache_path(
        self,
        index: int,
    ) -> Path:

        return (
            BOOK_CACHE_DIR
            / f"book-{index:03d}.html"
        )

    # --------------------------------------------------
    # Process one book
    # --------------------------------------------------

    def process_book(
        self,
        index: int,
        product_url: str,
        source_page: str,
    ):
    

        cache_path = self.book_cache_path(
            index
        )

        html, source, status = (
            self.fetcher.fetch(
                product_url,
                cache_path,
            )
        )

        if html is None:

            self.failed_pages.append(
                {
                    "url": product_url,
                    "type": "detail",
                    "status": status,
                }
            )

            return None

        try:

            raw_record = parse_book(
                html,
                product_url,
                source_page,
            )

            normalized = normalize_record(
                raw_record
            )

            valid_record, error = (
                validate_record(
                    normalized
                )
            )

            if error:

                self.invalid_records.append(
                    {
                        "url": product_url,
                        "error": error,
                    }
                )

                return None

            return valid_record

        except Exception as exc:

            self.invalid_records.append(
                {
                    "url": product_url,
                    "error": str(exc),
                }
            )

            return None

    # --------------------------------------------------
    # Run the scraper
    # --------------------------------------------------

    def run(self):

        catalogue_pages, book_urls = (
            self.discover_books()
        )

        print()
        print(
            f"catalogue_pages={len(catalogue_pages)}"
        )

        print(
            f"discovered={len(book_urls)}"
        )

        print(
            f"unique_urls={len(set(book_urls))}"
        )

        # --------------------------------------------------
        # We only expect 60 real books.
        # --------------------------------------------------

        if len(book_urls) > 60:

            book_urls = book_urls[:60]

        # --------------------------------------------------
        # Process all books
        # --------------------------------------------------

        valid_records = []

        for index, product_url in enumerate(
            book_urls,
            start=1,
        ):

            # Determine catalogue page.
            #
            # The first 20 books belong to page 1,
            # next 20 to page 2,
            # next 20 to page 3.
            #
            # This is only used as provenance.
            page_number = (
                (index - 1) // 20
            ) + 1

            source_page = (
                f"https://books.toscrape.com/"
                f"catalogue/page-{page_number}.html"
            )

            record = self.process_book(
                index,
                product_url,
                source_page,
            )

            if record is not None:
                valid_records.append(
                    record
                )

        # --------------------------------------------------
        # Remove duplicate records by product URL.
        # --------------------------------------------------

        unique_records = {}

        for record in valid_records:

            product_url = str(
                record["product_url"]
            )

            unique_records[
                product_url
            ] = record

        valid_records = list(
            unique_records.values()
        )

        return {
            "catalogue_pages": catalogue_pages,
            "book_urls": book_urls,
            "valid_records": valid_records,
            "invalid_records": self.invalid_records,
            "failed_pages": self.failed_pages,
            "pages_fetched": self.fetcher.pages_fetched,
            "cache_hits": self.fetcher.cache_hits,
        }