from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseCode:
    code: int
    message: str
