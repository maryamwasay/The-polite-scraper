from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator


class BookRecord(BaseModel):
    """
    Validated book record.
    """

    title: str

    product_url: HttpUrl

    price_text: str

    price_gbp: float

    availability_text: str

    rating_text: str

    description: Optional[str] = None

    source_page: HttpUrl

    fetched_at: datetime

    @field_validator(
        "title",
        "price_text",
        "availability_text",
        "rating_text",
    )
    @classmethod
    def required_text_must_not_be_empty(
        cls,
        value: str,
    ) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Value must not be empty"
            )

        return value

    @field_validator("price_gbp")
    @classmethod
    def price_must_be_non_negative(
        cls,
        value: float,
    ) -> float:

        if value < 0:
            raise ValueError(
                "price_gbp must be non-negative"
            )

        return value

    @field_validator("description")
    @classmethod
    def clean_description(
        cls,
        value: Optional[str],
    ) -> Optional[str]:

        if value is None:
            return None

        value = value.strip()

        return value or None