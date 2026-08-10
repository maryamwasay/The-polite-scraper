import json
import time
from datetime import datetime, timezone

from .config import OUTPUT_DIR
from .reporter import (
    create_run_report,
    write_json,
)
from .scraper import PoliteScraper


def main():

    started_timestamp = time.monotonic()

    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    print("=" * 60)
    print("FlyRank A9 - The Polite Scraper")
    print("=" * 60)

    print()

    scraper = PoliteScraper()

    result = scraper.run()

    # --------------------------------------------------
    # Extract results
    # --------------------------------------------------

    valid_records = result[
        "valid_records"
    ]

    invalid_records = result[
        "invalid_records"
    ]

    failed_pages = result[
        "failed_pages"
    ]

    # --------------------------------------------------
    # Write books.json
    # --------------------------------------------------

    books_path = (
        OUTPUT_DIR
        / "books.json"
    )

    write_json(
        books_path,
        valid_records,
    )

    # --------------------------------------------------
    # Write errors.json
    # --------------------------------------------------

    errors_path = (
        OUTPUT_DIR
        / "errors.json"
    )

    write_json(
        errors_path,
        {
            "invalid_records": invalid_records,
            "failed_pages": failed_pages,
        },
    )

    # --------------------------------------------------
    # Run report
    # --------------------------------------------------

    duration = (
        time.monotonic()
        - started_timestamp
    )

    report = create_run_report(
        started_at=started_at,
        duration_seconds=duration,
        catalogue_pages=len(
            result["catalogue_pages"]
        ),
        discovered_urls=len(
            result["book_urls"]
        ),
        detail_pages=len(
            result["book_urls"]
        ),
        pages_fetched=result[
            "pages_fetched"
        ],
        cache_hits=result[
            "cache_hits"
        ],
        valid_records=len(
            valid_records
        ),
        invalid_records=len(
            invalid_records
        ),
        failed_pages=len(
            failed_pages
        ),
    )

    report_path = (
        OUTPUT_DIR
        / "run-report.json"
    )

    write_json(
        report_path,
        report,
    )

    # --------------------------------------------------
    # Final output
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("RUN COMPLETE")
    print("=" * 60)

    print(
        f"Catalogue pages: "
        f"{report['catalogue_pages']}"
    )

    print(
        f"Discovered URLs: "
        f"{report['discovered_urls']}"
    )

    print(
        f"Valid records: "
        f"{report['valid_records']}"
    )

    print(
        f"Invalid records: "
        f"{report['invalid_records']}"
    )

    print(
        f"Failed pages: "
        f"{report['failed_pages']}"
    )

    print(
        f"Cache hits: "
        f"{report['cache_hits']}"
    )

    print(
        f"Pages fetched: "
        f"{report['pages_fetched']}"
    )

    print(
        f"Duration: "
        f"{report['duration_seconds']} seconds"
    )

    print()
    print(
        f"Books: {books_path}"
    )

    print(
        f"Errors: {errors_path}"
    )

    print(
        f"Report: {report_path}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()