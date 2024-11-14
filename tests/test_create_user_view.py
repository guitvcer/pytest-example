from asyncpg import Connection, Record
from pytest import mark
from sanic_testing.testing import SanicASGITestClient

from .helpers import load_data


@mark.freeze_time('2025-01-01T00:00:00+00:00')
@mark.parametrize('case', (
    'basic',
))
async def test_create_user_view__success(
        app: SanicASGITestClient,
        db_conn: Connection,
        case: str,
) -> None:
    # Arrange
    base = f'views/create_user_view/success/{case}'
    payload = load_data(f'{base}/payload.json')
    expected_response = load_data(f'{base}/expected_response.json')
    expected_users = load_data(f'{base}/expected_users.json')

    # Act
    _, response = await app.asgi_client.post('/users', json=payload)

    # Assert
    assert response.json == expected_response
    assert response.status == 201

    users = await db_conn.fetch('SELECT * FROM users')
    assert [_serialize_user_record(u) for u in users] == expected_users


def _serialize_user_record(record: Record) -> dict:
    return {
        'id': record['id'],
        'username': record['username'],
        'created_at': record['created_at'].isoformat(),
    }


@mark.parametrize('case', (
    'body_is_not_json',
    'no_username',
    'username_is_not_string',
    'username_is_too_short',
    'username_is_too_long',
    'user_already_exists',
))
async def test_create_user_view__failure(
        app: SanicASGITestClient,
        db_conn: Connection,
        case: str,
) -> None:
    # Arrange
    base = f'views/create_user_view/failure/{case}'
    payload = load_data(f'{base}/payload.json') or {}
    insert_query = load_data(f'{base}/insert_query.sql')
    expected_response = load_data(f'{base}/expected_response.json')
    expected_users_count = 1 if insert_query else 0

    if insert_query:
        await db_conn.execute(insert_query)

    # Act
    _, response = await app.asgi_client.post('/users', json=payload)

    # Assert
    assert response.json == expected_response
    assert response.status == 400

    users_count = await db_conn.fetchval('SELECT COUNT(*) FROM users')
    assert users_count == expected_users_count
