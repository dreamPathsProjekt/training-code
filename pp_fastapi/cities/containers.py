import docker
import pprint
from fastapi.logger import logger


def list_containers() -> None:
    client = docker.from_env()
    containers = client.containers.list()
    result = [container.attrs for container in containers]
    logger.info(pprint.pprint(result))