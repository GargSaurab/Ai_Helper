from abc import ABC, abstractmethod


class AppLogger(ABC):
    @abstractmethod
    def debug(self, message: str, *args, **kwargs): ...

    @abstractmethod
    def info(self, message: str, *args, **kwargs): ...

    @abstractmethod
    def warning(self, message: str, *args, **kwargs): ...

    @abstractmethod
    def error(self, message: str, *args, **kwargs): ...

    @abstractmethod
    def critical(self, message: str, *args, **kwargs): ...

    @abstractmethod
    def exception(self, message: str, *args, **kwargs): ...
