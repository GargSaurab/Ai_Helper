from app.core.exception.error_code import ErrorCode


class AppException(Exception):
    def __init__(self, error: ErrorCode, message: str | None = None):
        self.error = error
        self.message = message or error.message

        super().__init__(self.message)
