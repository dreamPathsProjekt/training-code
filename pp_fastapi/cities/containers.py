import docker
import pprint
import os
import inspect
from fastapi.logger import logger

BASE_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


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
        logs = str(container.logs())
    logger.info(pprint.pprint(logs))

    filepath = os.path.join(BASE_DIR, f'{container_id}.log')
    with open(filepath, mode='w') as logfile:
        logfile.write(logs)
