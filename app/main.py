from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_router import api_router
from app.core.config import settings
from app.core.exception.exception_handler import register_exception_handlers
from app.core.logging.logger import get_logger
from app.core.logging.logger_config import configure_logging
from app.core.middleware.auth_rate_limit import AuthRateLimitMiddleware
from app.core.middleware.authentication import AuthenticationMiddleware
from app.core.redis.redis_client import get_redis_client
from app.core.redis.redis_service import RedisService
from app.core.response.response_code import ResponseCode
from app.core.response.response_documentation import error_responses
from app.models.response.base_response import BaseResponse
from app.models.response.health_response import HealthResponse

# Configure logging before anything else
configure_logging(settings.LOGGER_LEVEL)

LOG = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    LOG.info(
        "Starting %s v%s",
        settings.APP_NAME,
        settings.APP_VERSION,
    )

    LOG.info("Environment: %s", settings.ENVIRONMENT)
    LOG.info("Log Level: %s", settings.LOGGER_LEVEL)

    yield

    LOG.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    AuthRateLimitMiddleware,
    redis_service=RedisService(get_redis_client()),
)

app.add_middleware(AuthenticationMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
)

register_exception_handlers(app)


@app.get(
    "/",
    tags=["Health"],
    response_model=BaseResponse[HealthResponse],
    responses=error_responses(500),
)
async def health_check() -> BaseResponse[HealthResponse]:
    return BaseResponse(
        code=ResponseCode.SUCCESS.code,
        message=ResponseCode.SUCCESS.message,
        data=HealthResponse(
            status="healthy",
            application=settings.APP_NAME,
            version=settings.APP_VERSION,
        ),
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT.lower() == "development",
    )
