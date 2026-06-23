from fastapi import APIRouter
from app.models.request.user_registration_request import UserRegistrationRequest
from app.models.request.user_login_request import UserLoginRequest
from app.dependencies.service_dependencies import UserServiceDep
from app.models.response.base_response import BaseResponse

app = APIRouter(prefix="/users")


@app.post("/register")
def registerUser(
    request: UserRegistrationRequest, user_Service: UserServiceDep
) -> BaseResponse:
    user = user_Service.register(request)

    return BaseResponse(
        success=200,
        message="User registered successfully",
        data=user,
    )


@app.post("/login")
def login(request: UserLoginRequest, user_Service: UserServiceDep):

    response : BaseResponse = user_Service.login(request)
    return  response

