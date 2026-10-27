from fastapi import APIRouter, Depends, Request

from app.core.exception.app_exception import AppException
from app.core.logging.logger import get_logger
from app.core.response.response_code import ResponseCode
from app.core.response.response_documentation import error_responses
from app.core.security.security_dependency import authenticate_user
from app.db.repo_dependencies import UserRepositoryDep
from app.models.response.base_response import BaseResponse
from app.models.response.user_response import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

LOG = get_logger(__name__)


@router.get(
    "/me",
    response_model=BaseResponse[UserResponse],
    dependencies=[Depends(authenticate_user)],
    responses=error_responses(401, 404, 422, 500),
)
async def get_user(
    request: Request, user_repo: UserRepositoryDep
) -> BaseResponse[UserResponse]:
    user = user_repo.get_user_by_id(int(request.state.user_id))
    if user is None:
        raise AppException(ResponseCode.NOT_FOUND)

    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=UserResponse.model_validate(user),
    )
