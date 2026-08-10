from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_catalogue_links(
    html: str,
    page_url: str,
) -> list[str]:
    """
    Extract all book links from a catalogue page.

    Relative URLs are converted to absolute URLs.
    Duplicate URLs are removed.
    """

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    links = []

    for article in soup.select(
        "article.product_pod"
    ):
        anchor = article.select_one(
            "h3 a"
        )

        if not anchor:
            continue

        href = anchor.get("href")

        if not href:
            continue

        absolute_url = urljoin(
            page_url,
            href,
        )

        links.append(absolute_url)

    # Preserve order while removing duplicates.
    return list(dict.fromkeys(links))


def parse_next_page(
    html: str,
    page_url: str,
) -> str | None:
    """
    Find the catalogue's next-page URL.
    """

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    next_link = soup.select_one(
        "li.next a"
    )

    if not next_link:
        return None

    href = next_link.get("href")

    if not href:
        return None

    return urljoin(
        page_url,
        href,
    )


def parse_book(
    html: str,
    product_url: str,
    source_page: str,
) -> dict:
    """
    Extract the eight required raw fields.
    """

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    # --------------------------------------------------
    # Product information
    # --------------------------------------------------

    title_element = soup.select_one(
        "div.product_main h1"
    )

    price_element = soup.select_one(
        "div.product_main .price_color"
    )

    availability_element = soup.select_one(
        "div.product_main .availability"
    )

    rating_element = soup.select_one(
        "div.product_main p.star-rating"
    )

    description_element = soup.select_one(
        "#product_description + p"
    )

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    title = None

    if title_element:
        title = title_element.get_text(
            strip=True
        )

    # --------------------------------------------------
    # Price
    # --------------------------------------------------

    price_text = None

    if price_element:
        price_text = price_element.get_text(
            " ",
            strip=True,
        )

    # --------------------------------------------------
    # Availability
    # --------------------------------------------------

    availability_text = None

    if availability_element:
        availability_text = availability_element.get_text(
            " ",
            strip=True,
        )

    # --------------------------------------------------
    # Rating
    # --------------------------------------------------

    rating_text = None

    if rating_element:
        classes = rating_element.get(
            "class",
            [],
        )

        rating_classes = [
            item
            for item in classes
            if item != "star-rating"
        ]

        if rating_classes:
            rating_text = rating_classes[0]

    # --------------------------------------------------
    # Description
    # --------------------------------------------------

    description = None

    if description_element:
        description = description_element.get_text(
            " ",
            strip=True,
        )

        if not description:
            description = None

    # --------------------------------------------------
    # Timestamp
    # --------------------------------------------------

    fetched_at = datetime.now(
        timezone.utc
    ).isoformat()

    # --------------------------------------------------
    # Raw record
    # --------------------------------------------------

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }