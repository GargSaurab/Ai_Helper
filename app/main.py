from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.api_router import api_router
from app.core.config import settings
from app.core.exception.exception_handler import register_exception_handlers
from app.core.logging.logger import get_logger
from app.core.logging.logger_config import configure_logging

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

app.include_router(
    api_router,
    prefix="/api/v1",
)

register_exception_handlers(app)


@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT.lower() == "development",
    )
