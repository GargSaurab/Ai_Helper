from app.services.user_service import UserService
from fastapi import Annotation

userServiceDep = Annotation[UserService, Depends(UserService)]