import aiohttp
import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks
from fastapi.logger import logger
# from pydantic import BaseModel
# Register tortoise models to FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import Optional

from .models import City, CityInSerializer, CitySerializer
from .containers import get_containers


app = FastAPI()
DB_URL = 'sqlite://db.sqlite3'

# NOTE: Deprecated
# class City(BaseModel):
#     name: str
#     timezone: str

session: Optional[aiohttp.ClientSession] = None
logger.setLevel(logging.INFO)


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
    # tasks = [asyncio.create_task(City.set_current_time(city, session)) for city in cities_all]
    # await asyncio.gather(*tasks)
    # return cities_all

    # Asyncio wait method
    await asyncio.wait([City.set_current_time(city, session) for city in cities_all])
    return cities_all


@app.get('/cities/{city_id}')
async def get_cities_id(city_id: int):
    city = await CitySerializer.from_queryset_single(queryset=City.get(id=city_id))

    global session
    await asyncio.wait([City.set_current_time(city, session)])
    return city


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


@app.get('/containers')
async def get_containers(background_tasks: BackgroundTasks):
    background_tasks.add_task(get_containers)
    return {
        'result': 'Task sent, check your app logs.',
        'tasks': background_tasks.tasks
    }


register_tortoise(
    app=app,
    db_url=DB_URL,
    modules={
        'models': ['cities.models']
    },
    generate_schemas=True,
    add_exception_handlers=True
)