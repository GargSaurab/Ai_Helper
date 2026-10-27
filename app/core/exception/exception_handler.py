from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ExceptionHandler
from fastapi.encoders import jsonable_encoder

from app.core.exception.app_exception import AppException
from app.core.logging.logger import get_logger
from app.core.response.response_code import ResponseCode

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning("[%s] %s", exc.error.code, exc.message)
    return JSONResponse(
        status_code=exc.error.http_status,
        content={"code": exc.error.code, "message": exc.message, "data": None},
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=ResponseCode.VALIDATION_FAILED.http_status,
        content={
            "code": ResponseCode.VALIDATION_FAILED.code,
            "message": ResponseCode.VALIDATION_FAILED.message,
            "data": jsonable_encoder(exc.errors()),
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code * 10, "message": message, "data": None},
    )


async def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error")
    return JSONResponse(
        status_code=ResponseCode.INTERNAL_ERROR.http_status,
        content={
            "code": ResponseCode.INTERNAL_ERROR.code,
            "message": ResponseCode.INTERNAL_ERROR.message,
            "data": None,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        AppException, cast(ExceptionHandler, app_exception_handler)
    )
    app.add_exception_handler(
        RequestValidationError,
        cast(ExceptionHandler, request_validation_exception_handler),
    )
    app.add_exception_handler(
        StarletteHTTPException, cast(ExceptionHandler, http_exception_handler)
    )
    app.add_exception_handler(
        Exception, cast(ExceptionHandler, unexpected_exception_handler)
    )
