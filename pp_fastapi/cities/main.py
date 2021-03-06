import aiohttp
import asyncio
import logging

import jwt

from fastapi import FastAPI, BackgroundTasks, HTTPException, status, Depends
from fastapi.logger import logger
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt_sha256

# from pydantic import BaseModel
# Register tortoise models to FastAPI
from tortoise.contrib.fastapi import register_tortoise
from typing import Optional

from .models import City, CityInSerializer, CitySerializer, User, UserSerializer, UserInSerializer
from .containers import list_containers, container_logs, BASE_DIR, os


app = FastAPI()
DB_URL = 'sqlite://db.sqlite3'
JWT_SECRET = 'pokUk2VSTrJ1cSImF6do'


# NOTE: Deprecated
# class City(BaseModel):
#     name: str
#     timezone: str

session: Optional[aiohttp.ClientSession] = None
logger.setLevel(logging.INFO)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


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
    return {'message': 'Hello!'}


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@app.post('/token')
# Dependency injection using Depends() on form_data - no params Depends() -> depends on annotated class.
# If OAuth2PasswordRequestForm fails, function won't run
# Authenticate only /container endpoints
# Needs package: pip install python-multipart
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User authentication failed')
    user_object = await UserSerializer.from_tortoise_orm(user)
    token = jwt.encode({'id': str(user_object.id), 'username': user_object.username}, JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


# OAuth2 scheme lock plumbing, using dependency injection.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User authentication failed')
    return await UserSerializer.from_tortoise_orm(user)


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserSerializer)
async def create_user(user: UserInSerializer):
    user_object = await User.create(username=user.username, password=bcrypt_sha256.hash(user.password))
    return await UserSerializer.from_tortoise_orm(user_object)


@app.get('/user/me', response_model=UserSerializer)
async def get_user(user: UserSerializer = Depends(get_current_user)):
    return user


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
def get_containers(token: str = Depends(oauth2_scheme)):
    logger.info(f'User login on /containers with token {token}')
    return list_containers()


@app.get('/containers/{container_id}/logs', status_code=status.HTTP_201_CREATED)
async def get_containers_logs(container_id: str, background_tasks: BackgroundTasks, token: str = Depends(oauth2_scheme)):
    logger.info(f'User login on /containers/{container_id}/logs with token {token}')
    background_tasks.add_task(container_logs, container_id)
    return {
        'result': f'Task logs sent to container {container_id}, check your app logs.',
        'tasks': background_tasks.tasks
    }


# Use responses to control swagger documentation, media_type
@app.get('/containers/{container_id}/file', responses={200: {"content": {"text/plain": {"example": "No example. Downloads file."}}}})
async def get_containers_logs_file(container_id: str, token: str = Depends(oauth2_scheme)):
    logger.info(f'User login on /containers/{container_id}/file with token {token}')
    filepath = os.path.join(BASE_DIR, f'{container_id}.log')
    if not os.path.exists(filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'File {container_id}.log not Found')
    # Include filename attribute to send as downloadable attachment and not in browser. We only include filename and not full path.
    return FileResponse(filepath, filename=f'{container_id}.log', media_type='text/plain')


register_tortoise(
    app=app,
    db_url=DB_URL,
    modules={
        'models': ['cities.models']
    },
    generate_schemas=True,
    add_exception_handlers=True
)