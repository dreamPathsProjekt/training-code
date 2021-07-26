import aiohttp
import asyncio
import logging
import os
import inspect

from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from fastapi.logger import logger
from fastapi.responses import FileResponse
# from pydantic import BaseModel
# Register tortoise models to FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import Optional

from .models import City, CityInSerializer, CitySerializer
from .containers import list_containers, container_logs


app = FastAPI()
DB_URL = 'sqlite://db.sqlite3'
BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

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
@app.post('/cities', status_code=status.HTTP_201_CREATED)
async def create_cities(city: CityInSerializer):
    # exclude_unset to auto-increment ids
    city_object = await City.create(**city.dict(exclude_unset=True))
    return await CitySerializer.from_tortoise_orm(city_object)


@app.delete('/cities/{city_id}')
async def delete_cities(city_id: int):
    await City.filter(id=city_id).delete()
    return {}


@app.get('/containers')
async def get_containers():
    return list_containers()


@app.get('/containers/{container_id}/logs', status_code=status.HTTP_201_CREATED)
async def get_containers_logs(container_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(container_logs, container_id)
    return {
        'result': f'Task logs sent to container {container_id}, check your app logs.',
        'tasks': background_tasks.tasks
    }


@app.get('/containers/{container_id}/file')
async def get_containers_logs_file(container_id: str):
    filepath = os.path.join(BASE_DIR, f'{container_id}.json')
    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'File {container_id}.json not Found')
    return FileResponse(filepath, media_type='application/json')


register_tortoise(
    app=app,
    db_url=DB_URL,
    modules={
        'models': ['cities.models']
    },
    generate_schemas=True,
    add_exception_handlers=True
)