import asyncpg
from asyncpg import UniqueViolationError
from sanic import Sanic, Request, HTTPResponse, response
from sanic.exceptions import BadRequest

from . import settings
from .database import create_user

app = Sanic("pytest-example")
app.config.DATABASE_URL = settings.DATABASE_URL


@app.on_request
async def open_db_conn(request: Request) -> None:
    request.ctx.db_conn = await asyncpg.connect(request.app.config.DATABASE_URL)


@app.on_response
async def close_db_conn(request: Request, response: HTTPResponse) -> None:
    await request.ctx.db_conn.close()


@app.post("/users")
async def create_user_view(request: Request) -> HTTPResponse:
    try:
        username = request.json.get("username")
    except AttributeError as exc:
        raise BadRequest("Body is not JSON") from exc

    if username is None:
        raise BadRequest("Username is required")

    if not isinstance(username, str):
        raise BadRequest("Username must be a string")

    if len(username) < 4 or len(username) > 32:
        raise BadRequest("Username length must be between 4 and 32 symbols.")

    try:
        user_id = await create_user(username, request.ctx.db_conn)
    except UniqueViolationError as exc:
        raise BadRequest("User already exists") from exc

    return response.json({"id": user_id}, status=201)


if __name__ == "__main__":
    app.run(single_process=True)
