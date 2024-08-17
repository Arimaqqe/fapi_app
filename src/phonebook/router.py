from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from redis.asyncio import Redis

from src.redis_client import get_redis
from src.phonebook.service import get_record, create_record, change_record
from src.phonebook.schemas import PhoneBookRecord

from src.config import settings


phonebook_router = APIRouter(prefix="/phonebook", tags=["phonebook"])


@phonebook_router.get("/check_data")
async def phonebook_get_record(
    redis: Annotated[Redis, Depends(get_redis)], 
    phone: str = Query(...)
):
    if not phone:
        raise HTTPException(
            status_code=400, 
            detail="The phone number cannot be None or an empty string"
        )

    record = await get_record(redis, phone)

    if record is None:
        return {"msg": "Record does no exist"}
    else:
        return {
            "phone": phone,
            "address": record
        }


@phonebook_router.post("/write_data")
async def phonebook_create_record(
    redis: Annotated[Redis, Depends(get_redis)],     
    record: PhoneBookRecord
):
    if not record.phone or not record.address:
        raise HTTPException(
            status_code=400,
            detail="Field cannot be None or an empty string"
        )
    result = await create_record(redis, record)
    return {"msg": result}


@phonebook_router.put("/write_data")
async def phonebook_change_record(
    redis: Annotated[Redis, Depends(get_redis)],     
    record: PhoneBookRecord
):
    if not record.phone or not record.address:
        raise HTTPException(
            status_code=400,
            detail="Field cannot be None or an empty string"
        )
    result = await change_record(redis, record)
    return {"msg": result}
