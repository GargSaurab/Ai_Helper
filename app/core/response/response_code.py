from enum import Enum


class ResponseCode(Enum):
    def __init__(self, code: int, message: str, http_status: int):
        self.code = code
        self.message = message
        self.http_status = http_status

    SUCCESS = (0, "Success", 200)
    VALIDATION_FAILED = (1000, "Validation failed", 422)
    INVALID_CREDENTIALS = (1001, "Invalid email or password", 401)
    TOKEN_EXPIRED = (1002, "Token has expired", 401)
    INVALID_TOKEN = (1003, "Invalid token", 401)
    NOT_FOUND = (1004, "Resource not found", 404)
    ALREADY_EXISTS = (1005, "Resource already exists", 409)
    RATE_LIMITED = (1006, "Too many requests", 429)
    FORBIDDEN = (1007, "Access denied", 403)
    INTERNAL_ERROR = (9999, "Internal server error", 500)
    DATABASE_ERROR = (9001, "Database operation failed", 500)
    EXTERNAL_SERVICE_ERROR = (9002, "External service failed", 502)
