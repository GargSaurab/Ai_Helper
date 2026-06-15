from fastapi import APIRouter
from app.models.request.user_registration_request import UserRegistrationRequest
from app.dependencies.dependencies import userServiceDep

app = APIRouter(prefix = "/users")

@app.post("/register")
def registerUser(user_registeration_request : UserRegistrationRequest, user_Service : userServiceDep):
    user_Service.register(user_registeration_request)


