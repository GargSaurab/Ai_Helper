from fastapi import HTTPException, status

from app.db.schema.user_schema import User
from app.models.request.user_login_request import UserLoginRequest
from app.models.request.user_registration_request import UserRegistrationRequest
from app.db.repositories.user_repository import UserRepository
from app.core.password_hasher import hash_password, verify_password
from app.models.response.base_response import BaseResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, request: UserRegistrationRequest):

        if self.user_repo.get_user_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        if self.user_repo.get_user_by_phone_number(request.phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone already exists",
            )
        user = User(
            name=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            phone_number=request.phone_number,
        )

        saved_user = self.user_repo.save(user)

        if saved_user:
            return {
                "id": saved_user.id,
                "name": saved_user.name,
                "email": saved_user.email,
                "phone_number": saved_user.phone_number,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User Registeratin failed please try again",
            )

    def login(self, request: UserLoginRequest) -> BaseResponse:

        user: User = self.user_repo.get_user_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email does not exists",
            )

        if verify_password(request.password, user.password_hash):
            return BaseResponse(code=200, message="Login SuccessFull")
        else:
            return BaseResponse(code=302, message="Login Failed")
