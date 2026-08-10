import time
from pathlib import Path
from typing import Optional

import requests

from .config import (
    MAX_RETRIES,
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    USER_AGENT,
)


class Fetcher:
    """
    Handles polite HTTP requests and local caching.
    """

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
            }
        )

        self.last_request_time = 0.0

        self.pages_fetched = 0
        self.cache_hits = 0

    def _wait_before_request(self):
        """
        Ensure at least REQUEST_DELAY seconds between
        real requests.
        """

        elapsed = time.monotonic() - self.last_request_time

        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)

    def fetch(
        self,
        url: str,
        cache_path: Optional[Path] = None,
    ) -> tuple[Optional[str], str, Optional[int]]:
        """
        Fetch a URL.

        Returns:
            (content, source, status_code)

        source is either:
            "fetch"
            "cache"
            "error"
        """

        # --------------------------------------------------
        # Use cache if available
        # --------------------------------------------------

        if cache_path and cache_path.exists():
            try:
                content = cache_path.read_text(
                    encoding="utf-8"
                )

                self.cache_hits += 1

                print(f"CACHE HIT: {url}")

                return content, "cache", 200

            except OSError as exc:
                print(
                    f"WARNING: Could not read cache "
                    f"{cache_path}: {exc}"
                )

        # --------------------------------------------------
        # Real request
        # --------------------------------------------------

        for attempt in range(MAX_RETRIES + 1):

            self._wait_before_request()

            print(f"FETCH: {url}")

            self.last_request_time = time.monotonic()

            try:
                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                )

                status_code = response.status_code

                self.pages_fetched += 1

                # --------------------------------------------------
                # Successful response
                # --------------------------------------------------

                if status_code == 200:

                    content = response.text

                    if cache_path:
                        try:
                            cache_path.parent.mkdir(
                                parents=True,
                                exist_ok=True,
                            )

                            cache_path.write_text(
                                content,
                                encoding="utf-8",
                            )

                        except OSError as exc:
                            print(
                                f"WARNING: Could not save cache "
                                f"{cache_path}: {exc}"
                            )

                    return content, "fetch", status_code

                # --------------------------------------------------
                # Retry temporary server failures
                # --------------------------------------------------

                if 500 <= status_code <= 599:

                    if attempt < MAX_RETRIES:
                        print(
                            f"SERVER ERROR {status_code}. "
                            f"Retrying once..."
                        )

                        time.sleep(1)

                        continue

                    print(
                        f"FAILED: {url} "
                        f"status={status_code}"
                    )

                    return None, "error", status_code

                # --------------------------------------------------
                # Do NOT retry 403 / 404
                # --------------------------------------------------

                print(
                    f"FAILED: {url} "
                    f"status={status_code}"
                )

                return None, "error", status_code

            except requests.Timeout:

                if attempt < MAX_RETRIES:
                    print(
                        "TIMEOUT. Retrying once..."
                    )

                    time.sleep(1)

                    continue

                print(
                    f"FAILED: {url} timeout"
                )

                return None, "error", None

            except requests.RequestException as exc:

                print(
                    f"FAILED: {url} "
                    f"request error: {exc}"
                )

                return None, "error", None

        return None, "error", None