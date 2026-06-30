import logging

from app.core.logging.app_logger import AppLogger


class PythonLogger(AppLogger):
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def debug(self, message, *args, **kwargs):
        self._logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self._logger.exception(message, *args, **kwargs)
