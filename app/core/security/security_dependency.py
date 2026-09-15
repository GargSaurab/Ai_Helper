from typing import Annotated
from fastapi import Depends, Request

from app.core.security.jwt_service import JWTService
from app.core.security.authentication import AuthenticationService
from app.db.schema.user_schema import User
from app.db.repo_dependencies import UserRepositoryDep
from app.core.security.oauth2 import oauth2_scheme
from app.models.response.user_response import UserResponse


# 1. JWT Service Provider
def get_jwt_service() -> JWTService:
    return JWTService()


JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


# 2. Authentication Service Provider
def get_authentication_service(jwt_service: JWTServiceDep) -> AuthenticationService:
    return AuthenticationService(jwt_service)


AuthServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]


TokenDep = Annotated[str, Depends(oauth2_scheme)]


def authenticate_user(
    request: Request,
    token: TokenDep,
    auth_service: AuthServiceDep,
) -> None:
    auth_service.authenticate_request(request=request, token=token)


AuthRequired = Annotated[None, Depends(authenticate_user)]
