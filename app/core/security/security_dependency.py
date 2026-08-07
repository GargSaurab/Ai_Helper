from typing import Annotated
from fastapi import Depends

from app.core.security.jwt_service import JWTService
from app.core.security.authentication import AuthenticationService
from app.db.schema.user_schema import User
from app.dependencies.repo_dependencies import UserRepositoryDep
from app.core.security.oauth2 import oauth2_scheme
from app.models.response.user_response import UserResponse


# 1. JWT Service Provider
def get_jwt_service() -> JWTService:
    return JWTService()

JWTServiceDep = Annotated[JWTService, Depends(get_jwt_service)]


# 2. Authentication Service Provider
def get_authentication_service(
    jwt_service: JWTServiceDep, 
    user_repo: UserRepositoryDep
) -> AuthenticationService:
    return AuthenticationService(jwt_service, user_repo)

AuthServiceDep = Annotated[AuthenticationService, Depends(get_authentication_service)]


# 3. Current User Extraction Dependency
async def get_current_user(auth_service: AuthServiceDep, token : Annotated[str, Depends(oauth2_scheme)]) -> UserResponse:
    return await auth_service.get_current_user(token)


# 4. Exported Type Alias for Endpoints
CurrentUser = Annotated[User, Depends(get_current_user)]