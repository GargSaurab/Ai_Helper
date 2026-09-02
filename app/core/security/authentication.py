from fastapi import Request
from app.core.security.jwt_service import JWTService


class AuthenticationService:
    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    def authenticate_request(
        self,
        request: Request,
        token: str,
    ) -> None:
        claims = self.jwt_service.decode(token)

        request.state.user_id = claims.user_id
        request.state.user_email = claims.email
        request.state.token_claims = claims