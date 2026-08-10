import re
from typing import Any


def normalize_price(
    price_text: str | None,
) -> float:
    """
    Convert values such as:

        £51.77

    into:

        51.77
    """

    if not price_text:
        raise ValueError(
            "Missing price"
        )

    cleaned = price_text.replace(
        ",",
        "",
    )

    match = re.search(
        r"\d+(?:\.\d+)?",
        cleaned,
    )

    if not match:
        raise ValueError(
            f"Could not parse price: {price_text}"
        )

    return float(
        match.group(0)
    )


def clean_text(
    value: str | None,
) -> str | None:
    """
    Normalize whitespace.
    """

    if value is None:
        return None

    value = " ".join(
        value.split()
    )

    return value or None


def normalize_record(
    raw_record: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize one raw scraped record.
    """

    record = dict(raw_record)

    # --------------------------------------------------
    # Clean text fields
    # --------------------------------------------------

    record["title"] = clean_text(
        record.get("title")
    )

    record["price_text"] = clean_text(
        record.get("price_text")
    )

    record["availability_text"] = clean_text(
        record.get("availability_text")
    )

    record["rating_text"] = clean_text(
        record.get("rating_text")
    )

    record["description"] = clean_text(
        record.get("description")
    )

    # --------------------------------------------------
    # Convert price
    # --------------------------------------------------

    record["price_gbp"] = normalize_price(
        record.get("price_text")
    )

    return record