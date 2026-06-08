from fastapi import FASTAPI, APIRouter, Depends
from app.models.request.user_registeration_request import UserRegistrationRequest

app = APIRouter(prefix = "/users")

@app.post("/register")
def registerUser(user_registeration_request : UserRegistrationRequest):
    pass


