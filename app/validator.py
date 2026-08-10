from typing import Any

from pydantic import ValidationError

from .models import BookRecord


def validate_record(
    record: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """
    Validate one normalized record.

    Returns:

        valid_record, None

    OR:

        None, error_record
    """

    try:

        validated = BookRecord.model_validate(
            record
        )

        return (
            validated.model_dump(
                mode="json"
            ),
            None,
        )

    except ValidationError as exc:

        error_record = {
            "record": record,
            "reason": exc.errors(),
        }

        return None, error_record

    except Exception as exc:

        error_record = {
            "record": record,
            "reason": str(exc),
        }

        return None, error_record