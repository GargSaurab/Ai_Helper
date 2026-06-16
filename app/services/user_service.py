from fastapi import HTTPException, status

from app.db.schema.user_schema import User
from app.models.request.user_registration_request import UserRegistrationRequest
from app.db.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, userRepo: UserRepository):
        self.userRepo = userRepo

    def register(self, request: UserRegistrationRequest):

        if self.userRepo.get_user_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        if self.userRepo.get_user_by_phone_number(
            request.phone_number
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this phone already exists",
            )
        user = User(
            username=request.username,
            email=request.email,
            hashed_password=self.password_encoder.hash_password(request.password),
            phone_number=request.phone_number,
        )

        saved_user = self.user_repo.save(user)

        if saved_user :
            return {
                    "id": saved_user.id,
                    "username": saved_user.username,
                    "email": saved_user.email,
                    "phone_number": saved_user.phone_number
            }
        else :
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User Registeratin failed please try again"
            )
