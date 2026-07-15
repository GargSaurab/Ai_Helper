from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorCode:
    code: int
    message: str
