# Pretty Printed FastAPI tutorials

## Install

> NOTE: Do not try to run this from WSL, aiohttp is blocking.

Requires: Python 3.6+
Repo: Python 3.9.1

```Shell
pip install --upgrade pip
pip install -r requirements.txt

# Run the fastapi app - auto creates sqlite database if not exists.
hypercorn --bind 0.0.0.0:8000 --reload cities.main:app
# App is served on: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
# Redoc docs: http://localhost:8000/redoc

# Review schema
sqlite3 db.sqlite3
sqlite> .schema

CREATE TABLE IF NOT EXISTS "city" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "timezone" VARCHAR(50) NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
```

## Proposed order of Tutorials

FastAPI with async functionality, things that play well integrated:

- `AIOHTTP`
- `Tortoise ORM` - will also require you to have the async version of the database driver (sqlite, MySQL, Postgresql etc.). We have chosen `aiosqlite` installed with `tortoise-orm`
- [https://tortoise-orm.readthedocs.io/en/latest/reference.html](https://tortoise-orm.readthedocs.io/en/latest/reference.html)
- Install tortoise with accelerators (Linux) - `pip install tortoise-orm[accel]`

1. [FastAPI Intro](https://www.youtube.com/watch?v=kCggyi_7pHg)
2. [Tortoise ORM](https://www.youtube.com/watch?v=vVjWeLVv97c)
3. [FastAPI AIOHTTP](https://www.youtube.com/watch?v=BalvzyKg_4k)
4. [FastAPI Background Tasks - Avoid Celery for simple tasks](https://www.youtube.com/watch?v=_yXOJvr5vOM)
5. [FastAPI Return Files Async](https://www.youtube.com/watch?v=vpTAqnAbowo&list=RDCMUC-QDfvrRIDB6F0bIO4I4HkQ&index=5)
6. [FastAPI OAuth2, JWT](https://www.youtube.com/watch?v=6hTRw_HK3Ts)
7. [FastAPI Docs](https://fastapi.tiangolo.com/)
8. [FastAPI Performance Deployment](https://fastapi.tiangolo.com/deployment/docker/)
9. [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
10. [Full-stack FastAPI-Vue-Postgresql repo](https://github.com/tiangolo/full-stack-fastapi-postgresql)
11. [Mix Django with FastAPI](https://www.reddit.com/r/django/comments/jbsjbv/i_mix_django_with_fastapi_for_fun_and_discover/)
