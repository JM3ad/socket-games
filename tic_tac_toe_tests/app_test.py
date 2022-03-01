import pytest
import json

from tic_tac_toe.app import app

@pytest.fixture
def test_app():
    return app

@pytest.mark.asyncio
async def test_websocket(test_app):
    test_client = test_app.test_client()
    game_id = "abcdef"
    data = json.dumps({
        "message_type": "move",
        "game_id": game_id,
        "move": "top-right"
    })
    await test_client.get(f'/game/{game_id}')

    async with test_client.websocket('/ws') as test_websocket:
        await test_websocket.send(data)
        result = await test_websocket.receive()
    
    json_result = json.loads(result)
    state = json_result['state']
    assert "X" in state
