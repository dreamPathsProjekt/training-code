import docker
import pprint
import json
from fastapi.logger import logger


def list_containers() -> list:
    client = docker.from_env()
    containers = client.containers.list()
    return [{container.name: container.id} for container in containers]


def container_logs(container_id: str):
    client = docker.from_env()
    container = client.containers.get(container_id)
    if not container:
        logs = {}
    else:
        logs = container.logs()
    logger.info(pprint.pprint(logs.encode()))

    with open(f'{container_id}.json', mode='w') as logfile:
        json.dump(json.loads(logs), logfile)
