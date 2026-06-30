from app.core.logging.python_logger import PythonLogger


class LoggerFactory:
    @staticmethod
    def get_logger(name: str):
        """
        In future:
        - LoguruLogger
        - JsonLogger
        - CloudWatchLogger
        - OpenTelemetryLogger
        """
        return PythonLogger(name)
