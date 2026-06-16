from fastapi import APIRouter
from app.models.request.user_registration_request import UserRegistrationRequest
from app.dependencies.service_dependencies import UserServiceDep
from app.models.response.base_response import BaseResponse

app = APIRouter(prefix="/users")

@app.post("/register")
def registerUser(
    request: UserRegistrationRequest, user_Service: UserServiceDep
) -> BaseResponse :
    user = user_Service.register(request)

    return BaseResponse(
        success=True,
        message="User registered successfully",
        data=user,
    )
        
        
