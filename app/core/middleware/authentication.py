from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.exception.app_exception import AppException
from app.core.response.response_code import ResponseCode
from app.core.security.jwt_service import JWTService
from app.core.security.token_data import TokenData


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Require a valid access token except on explicitly public routes."""

    PUBLIC_PATHS = {
        "/",
        "/docs",
        "/openapi.json",
        "/redoc",
    }
    PUBLIC_PREFIXES = ("/api/v1/auth/",)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        is_public = path in self.PUBLIC_PATHS or any(
            path.startswith(prefix) for prefix in self.PUBLIC_PREFIXES
        )
        if request.method == "OPTIONS" or is_public:
            return await call_next(request)

        authorization = request.headers.get("Authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return self._unauthorized(ResponseCode.INVALID_TOKEN)

        try:
            claims: TokenData = JWTService().decode(token, expected_type="access")
        except AppException as exc:
            return self._unauthorized(exc.error, exc.message)

        request.state.token_claims = claims
        return await call_next(request)

    @staticmethod
    def _unauthorized(error: ResponseCode, message: str | None = None) -> JSONResponse:
        return JSONResponse(
            status_code=error.http_status,
            content={
                "code": error.code,
                "message": message or error.message,
                "data": None,
            },
        )
