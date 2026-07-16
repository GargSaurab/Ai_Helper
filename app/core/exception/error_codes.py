from app.core.response.response_code import ResponseCode


class ErrorCodes:
    SUCCESS = ResponseCode(0, "Success")

    NOT_FOUND = ResponseCode(1000, "Resource not found")

    ALREADY_EXISTS = ResponseCode(1001, "Resource already exists")

    INVALID_REQUEST = ResponseCode(1002, "Invalid request")

    UNAUTHORIZED = ResponseCode(1003, "Unauthorized")

    FORBIDDEN = ResponseCode(1004, "Access denied")

    VALIDATION_FAILED = ResponseCode(1005, "Validation failed")

    DATABASE_ERROR = ResponseCode(9001, "Database operation failed")

    EXTERNAL_SERVICE_ERROR = ResponseCode(9002, "External service failed")

    INTERNAL_SERVER_ERROR = ResponseCode(9999, "Internal server error")
