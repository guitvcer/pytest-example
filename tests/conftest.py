import os
from typing import AsyncIterator

import asyncpg
from pytest_asyncio import fixture
from pytest_mock import MockerFixture
from sanic import Sanic
from sanic_testing.testing import SanicASGITestClient

from tests.helpers import create_database, drop_database, get_db_name, get_db_url


@fixture
def app(db_url: str) -> SanicASGITestClient:
    Sanic.test_mode = True

    from src.app import app as app_

    app_.config.DATABASE_URL = db_url

    yield app_


@fixture
async def db_conn(
    mocker: MockerFixture, db_url: str
) -> AsyncIterator[asyncpg.Connection]:
    db_name = get_db_name(db_url)
    await create_database(db_name)

    os.system(f'dbmate -d "./migrations" -u {db_url} --no-dump-schema migrate')

    conn = await asyncpg.connect(db_url)
    yield conn
    await conn.close()

    await drop_database(db_name)


@fixture
def db_url() -> str:
    return get_db_url()
