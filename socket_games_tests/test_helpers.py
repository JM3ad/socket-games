
from functools import wraps
import json

from async_timeout import timeout
import pytest


def with_timeout(corofunc):
    @wraps(corofunc)
    async def wrapper(*args, **kwargs):
        with timeout(1):
            return await corofunc(*args, **kwargs)

    return wrapper

    
@pytest.mark.asyncio
@with_timeout
async def tic_tac_toe_socket_returns_game_board(test_app):
    test_client = test_app.test_client()
    game_id = "abcdef"
    tic_tac_toe_move = json.dumps(
        {"message_type": "move", "game_id": game_id, "move": "top-right", "player": "X"}
    )
    await test_client.get(f"/tic-tac-toe/{game_id}")

    async with test_client.websocket(f"/ws/tic-tac-toe/{game_id}") as test_websocket:
        await test_websocket.send(tic_tac_toe_move)
        result = await test_websocket.receive()

    json_result = json.loads(result)
    state = json_result["game_board"]
    assert len(state) == 9