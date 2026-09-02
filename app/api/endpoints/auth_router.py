from fastapi import APIRouter, Depends, Request

from app.core.logging.logger import get_logger
from app.core.security.security_dependency import authenticate_user
from app.models.request.refresh_token_request import RefreshTokenRequest
from app.services.service_dependencies import AuthServiceDep
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.response.base_response import BaseResponse
from app.core.response.response_codes import SUCCESS

router = APIRouter(prefix="/auth", tags=["Authentication"])

LOG = get_logger(__name__)

@router.post("/register", response_model=BaseResponse)
def register_user(
    request: UserRegistrationRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse:

    LOG.info(
        "User registration started for email: %s",
        request.email,
    )

    user = auth_service.register(request)

    LOG.info(
        "User registration completed for email: %s",
        request.email,
    )

    return BaseResponse(
        code=SUCCESS.code,
        message="User registered successfully",
        data=user,
    )


@router.post("/login", response_model=BaseResponse)
def login(
    request: UserLoginRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse:

    LOG.info(
        "User login started for email: %s",
        request.email,
    )

    response: str = auth_service.login(request)

    LOG.info(
        "User login completed for email: %s",
        request.email,
    )

    return BaseResponse(
        code=SUCCESS.code,
        message="Login successful",
        data=response,
    )

@router.post("/refresh", response_model=BaseResponse)
def refresh_token(
    request: RefreshTokenRequest,  # 👈 Passed in the JSON request body
    auth_service: AuthServiceDep,
) -> BaseResponse:
    new_tokens = auth_service.rotate_refresh_token(request.refresh_token)
    
    return BaseResponse(
        code=SUCCESS.code,
        message="Token refreshed successfully",
        data=new_tokens,
    )

@router.post("/logout", response_model=BaseResponse)
def logout(
    request: RefreshTokenRequest,
    auth_service: AuthServiceDep,
) -> BaseResponse:
    """
    Logs out the current device by deleting its specific refresh token from Redis.
    """
    LOG.info("Received request to POST /auth/logout")
    auth_service.logout_current_session(request.refresh_token)

    return BaseResponse(
        code=SUCCESS.code,
        message="Logged out successfully",
        data=None,
    )
    
