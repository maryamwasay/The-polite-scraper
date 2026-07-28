import requests
import time
import logging

from config.settings import BASE_URL, RATE_LIMIT
from config.headers import HEADERS


def fetch_html():
    """
    Sends an HTTP request and returns the HTML.
    """

    try:
        logging.info(f"Fetching: {BASE_URL}")

        response = requests.get(BASE_URL, headers=HEADERS)

        # Respect rate limit
        time.sleep(RATE_LIMIT)

        response.raise_for_status()

        logging.info("Page fetched successfully.")

        return response.text

    except requests.exceptions.RequestException as e:
        logging.error(f"Fetch Error: {e}")
        return None
