from fastapi import APIRouter, Depends, Request

from app.core.logging.logger import get_logger
from app.core.security.security_dependency import authenticate_user
from app.services.service_dependencies import UserServiceDep
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.response.base_response import BaseResponse
from app.core.response.response_codes import SUCCESS

router = APIRouter(prefix="/users", tags=["Users"])

LOG = get_logger(__name__)

@router.post("/me", response_model=BaseResponse, dependencies=[Depends(authenticate_user)])
async def get_user(
    request: Request
) -> BaseResponse:

    LOG.info(
        "Fetching current user information"
    )

    return BaseResponse(
        code=SUCCESS.code,
        message=SUCCESS.message,
        data=(request.state.user_id, request.state.user_email),
    )
