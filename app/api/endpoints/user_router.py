from fastapi import APIRouter
from sqlalchemy import true
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.request.user_login_request import UserLoginRequest
from app.dependencies.service_dependencies import UserServiceDep
from app.models.response.base_response import BaseResponse
from app.core.logging.logger import get_logger

app = APIRouter(prefix="/users")

logger = get_logger(__name__)


@app.post("/register")
def registerUser(
    request: UserRegistrationRequest, user_Service: UserServiceDep
) -> BaseResponse:
    logger.info("User registeration started")

    user = user_Service.register(request)

    logger.info("User registeration finished")

    return BaseResponse(
        success=True,
        code=200,
        message="User registered successfully",
        data=user,
    )


@app.post("/login")
def login(request: UserLoginRequest, user_Service: UserServiceDep):
    logger.info("User login started")
    response: BaseResponse = user_Service.login(request)
    logger.info("User login finished")
    return response
