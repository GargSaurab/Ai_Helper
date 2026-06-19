from fastapi import APIRouter

from app.api.endpoints.user_router import app as user_router

api_router = APIRouter()

api_router.include_router(user_router)
