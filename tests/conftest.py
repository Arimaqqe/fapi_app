import pytest
from httpx import AsyncClient, ASGITransport
import redis.asyncio as redis

from src.main import app
from src.redis_client import create_redis


@pytest.fixture(scope="function")
async def setup_redis():
    pool = create_redis()
    redis_connect = redis.Redis(connection_pool=pool)

    try:
        await redis_connect.ping()
    except ConnectionError:
        pytest.fail("Cloud not connect Redis.")

    yield redis_connect

    await redis_connect.flushall()
    await redis_connect.close()
    await pool.disconnect()


@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
