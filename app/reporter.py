import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_json(
    path: Path,
    data: Any,
):
    """
    Write JSON with readable formatting.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def create_run_report(
    started_at: str,
    duration_seconds: float,
    catalogue_pages: int,
    discovered_urls: int,
    detail_pages: int,
    pages_fetched: int,
    cache_hits: int,
    valid_records: int,
    invalid_records: int,
    failed_pages: int,
) -> dict[str, Any]:

    return {
        "started_at": started_at,
        "finished_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "duration_seconds": round(
            duration_seconds,
            2,
        ),
        "catalogue_pages": catalogue_pages,
        "discovered_urls": discovered_urls,
        "detail_pages": detail_pages,
        "pages_fetched": pages_fetched,
        "cache_hits": cache_hits,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "failed_pages": failed_pages,
    }