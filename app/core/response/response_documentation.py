from http import HTTPStatus
from typing import Any

from app.models.response.base_response import BaseResponse


def error_responses(*status_codes: int) -> dict[int | str, dict[str, Any]]:
    """Return OpenAPI metadata for the shared API error envelope."""
    return {
        status_code: {
            "model": BaseResponse[Any],
            "description": HTTPStatus(status_code).phrase,
        }
        for status_code in status_codes
    }
