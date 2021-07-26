import docker
import pprint
from fastapi.logger import logger
from fastapi.exceptions import HTTPException


def list_containers() -> list:
    client = docker.from_env()
    containers = client.containers.list()
    return [{container.name: container.id} for container in containers]


def container_logs(container_id: str):
    client = docker.from_env()
    container = client.containers.get(container_id)
    if not container:
        logs = ''
    else:
        logs = container.logs()
    logger.info(pprint.pprint(logs))
