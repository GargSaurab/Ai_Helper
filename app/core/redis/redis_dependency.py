# app/dependencies/service_dependencies.py
from typing import Annotated
from fastapi import Depends
import redis

from app.core.redis.redis_client import get_redis_client
from app.core.redis.redis_service import RedisService

def get_redis_service(
    client: Annotated[redis.Redis, Depends(get_redis_client)]
) -> RedisService:
    return RedisService(client)


RedisServiceDep = Annotated[RedisService, Depends(get_redis_service)]