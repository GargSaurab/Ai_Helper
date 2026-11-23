from typing import Annotated
from fastapi import Depends, Request

from app.core.exception.app_exception import AppException
from app.core.response.response_code import ResponseCode
from app.db.repo_dependencies import UserRepositoryDep
from app.db.schema.user_schema import User


def get_current_user(
    request: Request,
    user_repo: UserRepositoryDep,
) -> User:
    claims = request.state.token_claims
    if claims.user_id is None:
        raise AppException(ResponseCode.INVALID_TOKEN)
    user = user_repo.get_user_by_id(int(claims.user_id))
    if user is None:
        raise AppException(ResponseCode.NOT_FOUND)
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
