import docker
from fastapi.logger import logger


def get_containers() -> None:
    client = docker.from_env()
    containers = client.containers.list()
    result = [container.attrs for container in containers]
    logger.info(result)