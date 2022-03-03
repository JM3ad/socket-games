from functools import wraps
import pytest
import json
import os
from async_timeout import timeout

from socket_games.app import create_app


def with_timeout(corofunc):
    @wraps(corofunc)
    async def wrapper(*args, **kwargs):
        with timeout(1):
            return await corofunc(*args, **kwargs)

    return wrapper


@pytest.fixture
def test_app():
    os.environ["SECRET_KEY"] = "secret"
    return create_app()


@pytest.mark.asyncio
@with_timeout
async def test_websocket(test_app):
    test_client = test_app.test_client()
    game_id = "abcdef"
    data = json.dumps(
        {"message_type": "move", "game_id": game_id, "move": "top-right", "player": "X"}
    )
    await test_client.get(f"/game/{game_id}")

    async with test_client.websocket(f"/ws/{game_id}") as test_websocket:
        await test_websocket.send(data)
        result = await test_websocket.receive()

    json_result = json.loads(result)
    state = json_result["game_board"]
    assert len(state) == 9
