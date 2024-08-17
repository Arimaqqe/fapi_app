from contextlib import asynccontextmanager

from fastapi import FastAPI
import redis.asyncio as redis

import src.redis_client
from src.redis_client import create_redis
from src.phonebook.router import phonebook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    src.redis_client.pool = create_redis()

    yield

    if src.redis_client.pool:
        await redis.Redis(connection_pool=src.redis_client.pool).close()


app = FastAPI(lifespan=lifespan)
app.include_router(phonebook_router)
