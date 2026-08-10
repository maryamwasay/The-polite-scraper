import pytest

from app.normalizer import (
    clean_text,
    normalize_price,
)


def test_price_normalization():
    assert normalize_price(
        "£51.77"
    ) == 51.77


def test_price_with_comma():
    assert normalize_price(
        "£1,234.50"
    ) == 1234.50


def test_clean_text():
    assert clean_text(
        "   Hello    world   "
    ) == "Hello world"


def test_none_text():
    assert clean_text(
        None
    ) is None


def test_invalid_price():
    with pytest.raises(ValueError):
        normalize_price(
            "not-a-price"
        )