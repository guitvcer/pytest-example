from datetime import datetime
from zoneinfo import ZoneInfo

from asyncpg import Connection


async def create_user(username: str, db_conn: Connection) -> int:
    query = """
        INSERT INTO users (username, created_at)
        VALUES ($1, $2)
        RETURNING id
    """
    now = datetime.now(tz=ZoneInfo("UTC"))
    return await db_conn.fetchval(query, username, now)
