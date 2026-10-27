from fastapi import FastAPI, Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.core.exception.app_exception import AppException
from app.core.exception.error_codes import ErrorCodes
from app.core.logging.logger import get_logger
from app.models.response.base_response import BaseResponse

logger = get_logger(__name__)

HTTP_STATUS_BY_ERROR_CODE = {
    ErrorCodes.NOT_FOUND.code: status.HTTP_404_NOT_FOUND,
    ErrorCodes.ALREADY_EXISTS.code: status.HTTP_409_CONFLICT,
    ErrorCodes.INVALID_REQUEST.code: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.UNAUTHORIZED.code: status.HTTP_401_UNAUTHORIZED,
    ErrorCodes.FORBIDDEN.code: status.HTTP_403_FORBIDDEN,
    ErrorCodes.VALIDATION_FAILED.code: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorCodes.DATABASE_ERROR.code: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorCodes.EXTERNAL_SERVICE_ERROR.code: status.HTTP_502_BAD_GATEWAY,
    ErrorCodes.INTERNAL_SERVER_ERROR.code: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


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
        status_code=HTTP_STATUS_BY_ERROR_CODE.get(
            exc.error.code, status.HTTP_400_BAD_REQUEST
        ),
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
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
