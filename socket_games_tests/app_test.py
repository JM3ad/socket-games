import pytest
import json
import os

from quart import Quart

from socket_games.app import create_app
from socket_games_tests.test_helpers import with_timeout


@pytest.fixture
def test_app():
    os.environ["SECRET_KEY"] = "secret"
    return create_app()


@pytest.mark.asyncio
@with_timeout
async def test_joining_game_redirects_correctly(test_app: Quart):
    test_client = test_app.test_client()
    game_id = "abcdef"
    await test_client.get(f"/tic-tac-toe/{game_id}")
    form_data = {"game_id": game_id}

    response = await test_client.post(f"/join-game", form=form_data)

    assert response.status_code == 302
    assert response.location == f"tic-tac-toe/{game_id}"
