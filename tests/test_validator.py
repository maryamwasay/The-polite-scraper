from app.validator import validate_record


def valid_record():
    return {
        "title": "Test Book",
        "product_url": (
            "https://books.toscrape.com/"
            "catalogue/test_1/index.html"
        ),
        "price_text": "£10.99",
        "price_gbp": 10.99,
        "availability_text": (
            "In stock (10 available)"
        ),
        "rating_text": "Three",
        "description": "A test description.",
        "source_page": (
            "https://books.toscrape.com/"
            "catalogue/page-1.html"
        ),
        "fetched_at": (
            "2026-08-10T10:00:00+00:00"
        ),
    }


def test_valid_record():

    valid, error = validate_record(
        valid_record()
    )

    assert valid is not None
    assert error is None


def test_invalid_price():

    record = valid_record()

    record["price_gbp"] = -5

    valid, error = validate_record(
        record
    )

    assert valid is None
    assert error is not None


def test_missing_title():

    record = valid_record()

    record["title"] = ""

    valid, error = validate_record(
        record
    )

    assert valid is None
    assert error is not None