from typing import Optional

import redis.asyncio as redis

from src.config import settings


pool: Optional[redis.ConnectionPool] = None


def create_redis() -> redis.ConnectionPool:
    return redis.ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True
    )


def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=pool)


def build_cache_key(namespace: str, *args) -> str:
    return f"{namespace}:{':'.join(args)}"
