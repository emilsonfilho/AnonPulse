from http import HTTPStatus

from api.schemas.error_schema import ErrorResponse
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from .custom_exceptions import DomainValidationException, ResourceNotFoundException


def _json_error_response(error: ErrorResponse) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code, content=error.model_dump(exclude_none=True)
    )


async def resource_not_found_handler(
    _: Request, exc: ResourceNotFoundException
) -> JSONResponse:
    return _json_error_response(
        ErrorResponse.from_http_status(
            status_code=HTTPStatus.NOT_FOUND, message=exc.message
        )
    )


async def domain_validation_handler(
    _: Request, exc: DomainValidationException
) -> JSONResponse:
    return _json_error_response(
        ErrorResponse.from_http_status(
            status_code=HTTPStatus.BAD_REQUEST, message=exc.message
        )
    )


async def request_validation_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return _json_error_response(
        ErrorResponse.from_http_status(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            message="Erro de validação nos dados enviados",
            details=[exc.errors()],
        )
    )


async def http_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return _json_error_response(
        ErrorResponse.from_http_status(
            HTTPStatus(exc.status_code),
            message=exc.detail,
        )
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    #  logger.error(f"Erro inesperado em {request.url}: {repr(exc)}")

    return _json_error_response(
        ErrorResponse.from_http_status(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde.",
        )
    )
