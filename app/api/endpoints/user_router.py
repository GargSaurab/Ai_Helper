from fastapi import APIRouter

from app.core.logging.logger import get_logger
from app.core.response.response_code import ResponseCode
from app.core.response.response_documentation import error_responses
from app.core.security.auth_dependencies import CurrentUserDep
from app.models.response.base_response import BaseResponse
from app.models.response.user_response import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

LOG = get_logger(__name__)


@router.get(
    "/me",
    response_model=BaseResponse[UserResponse],
    responses=error_responses(401, 404, 422, 500),
)
async def get_user(user: CurrentUserDep) -> BaseResponse[UserResponse]:
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=UserResponse.model_validate(user),
    )
