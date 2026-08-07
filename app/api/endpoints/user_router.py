from fastapi import APIRouter

from app.core.logging.logger import get_logger
from app.core.security.security_dependency import CurrentUser
from app.dependencies.service_dependencies import UserServiceDep
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.response.base_response import BaseResponse
from app.core.response.response_codes import SUCCESS

router = APIRouter(prefix="/users", tags=["Users"])

LOG = get_logger(__name__)

@router.post("/register", response_model=BaseResponse)
def register_user(
    request: UserRegistrationRequest,
    user_service: UserServiceDep,
) -> BaseResponse:

    LOG.info(
        "User registration started for email: %s",
        request.email,
    )

    user = user_service.register(request)

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
    user_service: UserServiceDep,
) -> BaseResponse:

    LOG.info(
        "User login started for email: %s",
        request.email,
    )

    response: str = user_service.login(request)

    LOG.info(
        "User login completed for email: %s",
        request.email,
    )

    return BaseResponse(
        code=SUCCESS.code,
        message="Login successful",
        data=response,
    )
    

@router.post("/me", response_model=BaseResponse)
def getUser(
    current_user: CurrentUser
) -> BaseResponse:

    LOG.info(
        "Fetching current user information"
    )

    return BaseResponse(
        code=SUCCESS.code,
        message=SUCCESS.message,
        data=current_user,
    )
    
