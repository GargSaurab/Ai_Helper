import redis
from app.core.config import settings

# Create a connection pool for efficient reuse across requests
pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,  # Automatically decodes Redis bytes to strings
)


def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=pool)
