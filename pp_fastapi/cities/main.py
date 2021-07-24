import aiohttp
import asyncio
from fastapi import FastAPI
# from pydantic import BaseModel
# Register tortoise models to FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import Optional

from .models import City, CityInSerializer, CitySerializer


app = FastAPI()
DB_URL = 'sqlite://db.sqlite3'

# NOTE: Deprecated
# class City(BaseModel):
#     name: str
#     timezone: str

session: Optional[aiohttp.ClientSession] = None

@app.on_event('startup')
async def startup_event() -> None:
    """
    Use session singleton for async client pool
    :return: None
    """
    global session
    session = aiohttp.ClientSession()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    """
    Cleanup session
    :return: None
    """
    global session
    await session.close()


@app.get('/')
def index():
    return {'key': 'value'}


@app.get('/cities')
async def get_cities():
    cities_all = await CitySerializer.from_queryset(queryset=City.all())

    global session
    # Asyncio gather tasks method
    tasks = [asyncio.create_task(City.set_current_time(city, session)) for city in cities_all]
    print(tasks)
    await asyncio.gather(*tasks)
    return cities_all

    # Asyncio wait method
    # await asyncio.wait([City.set_current_time(city, session) for city in cities_all])
    # return cities_all


@app.get('/cities/{city_id}')
async def get_cities_id(city_id: int):
    # Both formats are awaitable
    # queryset_single = City.get(id=city_id)
    # return await CitySerializer.from_queryset_single(queryset=queryset_single)
    return await CitySerializer.from_queryset_single(queryset=City.get(id=city_id))


# Input: CityInSerializer
# Output: CitySerializer
# Tortoise model: City
@app.post('/cities')
async def create_cities(city: CityInSerializer):
    # exclude_unset to auto-increment ids
    city_object = await City.create(**city.dict(exclude_unset=True))
    return await CitySerializer.from_tortoise_orm(city_object)


@app.delete('/cities/{city_id}')
async def delete_cities(city_id: int):
    await City.filter(id=city_id).delete()
    return {}


register_tortoise(
    app=app,
    db_url=DB_URL,
    modules={
        'models': ['cities.models']
    },
    generate_schemas=True,
    add_exception_handlers=True
)