import requests
import aiohttp
from fastapi.logger import logger
from tortoise.models import Model
from tortoise import fields
# Replace pydantic serializer with tortoise helper
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt_sha256


WORLD_TIME_API_BASE_URL = 'http://worldtimeapi.org/api/timezone'


class User(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)

    def verify_password(self, password: str):
        return bcrypt_sha256.verify(password, self.password)


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    timezone = fields.CharField(max_length=50, null=False)

    # Read-only computed field
    # NOTE: Cannot use async methods to be computed
    def current_time(self) -> str:
        # Synchronous request queries will be slowww.
        # resp = requests.get(f'{WORLD_TIME_API_BASE_URL}/{self.timezone}')
        # current = resp.json().get('datetime')
        # return current

        # Patch for use of computed with async
        return ''

    @classmethod
    async def set_current_time(cls, instance: 'City', session: aiohttp.ClientSession):
        async with session.get(f'{WORLD_TIME_API_BASE_URL}/{instance.timezone}') as response:
            result = await response.json()
            logger.info(result)
            current_time = result.get('datetime')
            instance.current_time = current_time

    # Similar to Django meta
    class PydanticMeta:
        computed = ('current_time', )


CitySerializer = pydantic_model_creator(City, name='City')
# Incoming data helper, post serializer to exclude readonly fields, e.g. id
CityInSerializer = pydantic_model_creator(City, name='CityIn', exclude_readonly=True)
UserSerializer = pydantic_model_creator(User, name='User')
UserInSerializer = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)