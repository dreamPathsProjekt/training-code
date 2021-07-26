import docker
import pprint
from fastapi.logger import logger


def list_containers() -> list:
    client = docker.from_env()
    containers = client.containers.list()
    return [{container.name: container.id} for container in containers]


def container_logs(container_id: str):
    client = docker.from_env()
    container = client.containers.get(container_id)
    logs = container.logs()
    logger(pprint.pprint(logs))
