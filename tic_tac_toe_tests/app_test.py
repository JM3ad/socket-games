import pytest

from tic_tac_toe.app import app

@pytest.fixture
def test_app():
    return app

@pytest.mark.asyncio
async def test_websocket(test_app):
    test_client = test_app.test_client()
    data = b'bob'
    async with test_client.websocket('/ws') as test_websocket:
        await test_websocket.send(data)
        result = await test_websocket.receive()
    assert result == f"echo {data}"