# app/services/redis_service.py
from typing import Any
import redis


class RedisService:
    def __init__(self, client: redis.Redis):
        self.client = client

    # ----------------------------------------------------------------------
    # Key-Value Operations
    # ----------------------------------------------------------------------
    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int | None = None,
    ) -> bool:
        """Sets a key with an optional Time-To-Live (TTL) in integer seconds."""
        return bool(self.client.set(name=key, value=value, ex=ttl_seconds))

    def get(self, key: str) -> str | None:
        """Retrieves a string value by key. Returns None if expired or missing."""
        return self.client.get(key)

    def delete(self, *keys: str) -> int:
        """Deletes one or more keys. Returns the number of keys removed."""
        if not keys:
            return 0
        return self.client.delete(*keys)

    def exists(self, key: str) -> bool:
        """Checks if a key exists in Redis."""
        return self.client.exists(key) == 1

    def expire(self, key: str, ttl_seconds: int) -> bool:
        """Sets or updates the expiration TTL on an existing key."""
        return bool(self.client.expire(name=key, time=ttl_seconds))

    def get_ttl(self, key: str) -> int:
        """
        Returns the remaining TTL in seconds.
        Returns -2 if key doesn't exist, -1 if key exists without TTL.
        """
        return self.client.ttl(key)

    # ----------------------------------------------------------------------
    # Pattern & Bulk Operations (Safe Scan-based Deletion)
    # ----------------------------------------------------------------------
    def delete_pattern(self, pattern: str) -> int:
        """
        Deletes all keys matching a pattern using SCAN (production safe, non-blocking).
        """
        deleted_count = 0
        cursor = 0
        while True:
            cursor, keys = self.client.scan(cursor=cursor, match=pattern, count=100)
            if keys:
                deleted_count += self.client.delete(*keys)
            if cursor == 0:
                break
        return deleted_count

    # ----------------------------------------------------------------------
    # Counters & Rate Limiting
    # ----------------------------------------------------------------------
    def increment(self, key: str, amount: int = 1) -> int:
        """Increments integer value of a key by amount."""
        return self.client.incrby(key, amount)
