import asyncio
import hashlib

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.config import settings
from app.core.redis.redis_service import RedisService
from app.core.response.response_code import ResponseCode


class AuthRateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limit selected auth routes; all other requests pass through."""

    def __init__(self, app, redis_service: RedisService):
        super().__init__(app)
        self.redis_service = redis_service
        self.limits = {
            ("POST", "/api/v1/auth/login"): ("auth:login", settings.LOGIN_RATE_LIMIT),
            ("POST", "/api/v1/auth/register"): (
                "auth:register",
                settings.REGISTER_RATE_LIMIT,
            ),
            ("POST", "/api/v1/auth/refresh"): (
                "auth:refresh",
                settings.REFRESH_RATE_LIMIT,
            ),
        }

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        rule = self.limits.get((request.method, request.url.path))
        if rule is None:
            return await call_next(request)

        endpoint, limit = rule
        client_ip = request.client.host if request.client else "unknown"
        allowed = await asyncio.to_thread(self._increment, endpoint, client_ip, limit)
        if not allowed:
            error = ResponseCode.RATE_LIMITED
            return JSONResponse(
                status_code=error.http_status,
                content={"code": error.code, "message": error.message, "data": None},
            )

        return await call_next(request)

    def _increment(self, endpoint: str, client_ip: str, limit: int) -> bool:
        ip_digest = hashlib.sha256(client_ip.encode("utf-8")).hexdigest()
        key = f"rate_limit:{endpoint}:{ip_digest}"
        count = self.redis_service.increment(key)
        if count == 1:
            self.redis_service.expire(key, settings.AUTH_RATE_LIMIT_WINDOW_SECONDS)
        return count <= limit
