from fastapi import APIRouter, status

from app.core.logging.logger import get_logger
from app.core.response.response_code import ResponseCode
from app.core.response.response_documentation import error_responses
from app.models.request.refresh_token_request import RefreshTokenRequest
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.response.base_response import BaseResponse
from app.services.service_dependencies import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["Authentication"])

LOG = get_logger(__name__)


@router.post(
    "/register",
    response_model=BaseResponse[dict[str, str]],
    status_code=status.HTTP_201_CREATED,
    responses=error_responses(409, 422, 500),
)
def register_user(
    request: UserRegistrationRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse[dict[str, str]]:
    LOG.info("User registration started")
    tokens = auth_service.register(request)
    LOG.info("User registration completed")
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=tokens,
    )


@router.post(
    "/login",
    response_model=BaseResponse[dict[str, str]],
    responses=error_responses(401, 422, 429, 500),
)
def login(
    request: UserLoginRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse[dict[str, str]]:
    LOG.info("User login started")
    tokens = auth_service.login(request)
    LOG.info("User login completed")
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=tokens,
    )


@router.post(
    "/refresh",
    response_model=BaseResponse[dict[str, str]],
    responses=error_responses(401, 404, 422, 500, 502),
)
def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse[dict[str, str]]:
    tokens = auth_service.rotate_refresh_token(request.refresh_token)
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=tokens,
    )


@router.post(
    "/logout",
    response_model=BaseResponse[None],
    responses=error_responses(401, 422, 500),
)
def logout(
    request: RefreshTokenRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse[None]:
    auth_service.logout_current_session(request.refresh_token)
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=None,
    )
