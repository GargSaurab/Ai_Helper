from app.core.response.response_code import ResponseCode


class AppException(Exception):
    def __init__(self, error: ResponseCode, message: str | None = None):
        self.error = error
        self.message = message or error.message

        super().__init__(self.message)
