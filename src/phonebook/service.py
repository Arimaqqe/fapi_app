from typing import Optional
from redis.asyncio import Redis

from src.redis_client import build_cache_key
from src.phonebook.constants import NAMESPACE
from src.phonebook.schemas import PhoneBookRecord


async def get_record(redis: Redis, phone: str) -> Optional[str]:
    cache_key = build_cache_key(NAMESPACE, phone)
    return await redis.get(cache_key)


async def create_record(redis: Redis, record: PhoneBookRecord) -> str:
    cache_key = build_cache_key(NAMESPACE, record.phone)
    await redis.set(name=cache_key, value=record.address)
    return "Record has been created!"


async def change_record(redis: Redis, record: PhoneBookRecord) -> str:
    result = await get_record(redis, record.phone)
    if result is None:
        return "Record does not exist"
    else:
        await create_record(redis, record)
        return "Address has been changed!"
