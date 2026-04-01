from pydantic import BaseModel
from http import HTTPStatus
from typing import Any


class ErrorResponse(BaseModel):
    status_code: HTTPStatus
    error: str
    message: str
    details: dict[str, Any] | list[Any] | None = None

    @classmethod
    def from_http_status(
        cls,
        status_code: HTTPStatus,
        message: str,
        details: dict[str, Any] | list[Any] | None = None,
        error: str | None = None,
    ) -> "ErrorResponse":
        return ErrorResponse(
            status_code=status_code,
            error=error or status_code.phrase,
            message=message,
            details=details,
        )
