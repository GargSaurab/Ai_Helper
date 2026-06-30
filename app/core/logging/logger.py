from app.core.logging.factory import LoggerFactory


def get_logger(name: str):
    """
    This is the only method the application should use.
    """
    return LoggerFactory.get_logger(name)
