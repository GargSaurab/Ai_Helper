from app.core.exception.error_code import ErrorCode


class ErrorCodes:
    SUCCESS = ErrorCode(0, "Success")

    NOT_FOUND = ErrorCode(1000, "Resource not found")

    ALREADY_EXISTS = ErrorCode(1001, "Resource already exists")

    INVALID_REQUEST = ErrorCode(1002, "Invalid request")

    UNAUTHORIZED = ErrorCode(1003, "Unauthorized")

    FORBIDDEN = ErrorCode(1004, "Access denied")

    VALIDATION_FAILED = ErrorCode(1005, "Validation failed")

    DATABASE_ERROR = ErrorCode(9001, "Database operation failed")

    EXTERNAL_SERVICE_ERROR = ErrorCode(9002, "External service failed")

    INTERNAL_SERVER_ERROR = ErrorCode(9999, "Internal server error")
