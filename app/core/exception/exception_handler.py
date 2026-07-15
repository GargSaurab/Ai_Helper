from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exception.app_exception import AppException
from app.core.exception.error_codes import ErrorCodes
from app.core.logging.logger import get_logger
from app.models.response.base_response import BaseResponse

logger = get_logger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    logger.warning(
        "[%s] %s",
        exc.error.code,
        exc.message,
    )

    return JSONResponse(
        status_code=200,
        content=BaseResponse(
            success=False, code=exc.error.code, message=exc.message
        ).model_dump(),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content=BaseResponse(
            success=False,
            code=ErrorCodes.INTERNAL_SERVER_ERROR.code,
            message=ErrorCodes.INTERNAL_SERVER_ERROR.message,
        ).model_dump(),
    )


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )
