import pytest

from src.redis_client import build_cache_key
from src.phonebook.constants import NAMESPACE
from src.phonebook.schemas import PhoneBookRecord


async def test_startup(async_client):
    response = await async_client.get("/phonebook/check_data?phone=1111")
    assert response.status_code == 200


@pytest.mark.parametrize(
        "phone, status_code", 
        [
            ("", 400),
            (None, 400),
            ("1111", 200)
        ]
)
async def test_phonebook_get_record(async_client, phone, status_code):
    params = {"phone": phone}
    response = await async_client.get("/phonebook/check_data", params=params)

    assert response.status_code == status_code


@pytest.mark.parametrize(
        "phone, address, status_code", 
        [
            ("", "", 400), 
            ("1111", "", 400), 
            ("", "addr", 400),
            ("1111", "addr", 200)
        ]
)
async def test_phonebook_create_record(async_client, setup_redis, phone, address, status_code):
    record = PhoneBookRecord(phone=phone, address=address)
    response = await async_client.post("/phonebook/write_data", json=record.model_dump())
    assert response.status_code == status_code

    if status_code == 200:
        assert response.json() == {"msg": "Record has been created!"}

        cache_key = build_cache_key(NAMESPACE, phone)
        cache_data = await setup_redis.get(name=cache_key)

        assert cache_data == address


@pytest.mark.parametrize(
        "phone, address, status_code", 
        [
            ("", "", 400), 
            ("1111", "", 400), 
            ("", "addr", 400),
            ("1111", "addr", 200)
        ]
)
async def test_phonebook_change_record(async_client, setup_redis, phone, address, status_code,):
    record = PhoneBookRecord(phone=phone, address=address)
    response = await async_client.put("/phonebook/write_data", json=record.model_dump())
    assert response.status_code == status_code

    if response.status_code == 200 and response.json() == {"msg": "Record does not exist"}:
        cache_key = build_cache_key(NAMESPACE, record.phone)
        test_addres = "bbbbbb"
        await setup_redis.set(name=cache_key, value=test_addres)
        cache_data = await setup_redis.get(name=cache_key)
        assert cache_data == test_addres

        response = await async_client.put("/phonebook/write_data", json=record.model_dump())
        assert response.status_code == 200
        assert response.json() == {"msg": "Address has been changed!"}

        cache_data = await setup_redis.get(name=cache_key)
        assert cache_data == record.address


