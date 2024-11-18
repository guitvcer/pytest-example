import json
import uuid
from typing import Any

import asyncpg

from src import settings


def load_data(path: str) -> Any:
    try:
        with open(f"tests/data/{path}", "r") as file:
            content = file.read()
            try:
                data = json.loads(content)
            except Exception:
                data = content
    except Exception:
        return

    return data


def get_db_url() -> str:
    sslmode = "?sslmode=disable"
    database_url = settings.DATABASE_URL.replace(sslmode, "")
    return f"{database_url}_{uuid.uuid4().hex}_test{sslmode}"


def get_db_name(db_url: str) -> str:
    return db_url.rsplit("/", 1)[-1].split("?")[0]


async def create_database(db_name: str) -> None:
    conn = await asyncpg.connect(settings.DATABASE_URL)
    await conn.execute(f"CREATE DATABASE {db_name}")
    await conn.close()


async def drop_database(db_name: str) -> None:
    conn = await asyncpg.connect(settings.DATABASE_URL)
    await conn.execute(f"DROP DATABASE {db_name}")
    await conn.close()
