import pytest
import json
import os

from socket_games.app import create_app
from socket_games.mafia.mafia_role import MafiaRole
from socket_games_tests.test_helpers import with_timeout


@pytest.fixture
def test_app():
    os.environ["SECRET_KEY"] = "secret"
    return create_app()


@pytest.mark.asyncio
@with_timeout
async def test_each_player_sees_their_role_and_nobody_elses(test_app):
    test_clients = [
        test_app.test_client(),
        test_app.test_client(),
        test_app.test_client(),
        test_app.test_client(),
        test_app.test_client(),
    ]

    game_id = "abcdef"
    for client in test_clients:
        await client.get(f"/mafia/{game_id}")

    # connect all 5 to websocket
    start_game_message = json.dumps({"message_type": "start"})
    async with test_clients[0].websocket(f"/ws/mafia/{game_id}") as ws_1:
        async with test_clients[1].websocket(f"/ws/mafia/{game_id}") as ws_2:
            async with test_clients[2].websocket(f"/ws/mafia/{game_id}") as ws_3:
                async with test_clients[3].websocket(f"/ws/mafia/{game_id}") as ws_4:
                    async with test_clients[4].websocket(
                        f"/ws/mafia/{game_id}"
                    ) as ws_5:
                        await ws_5.send(start_game_message)
                        ws_1_state = await ws_1.receive()
                        ws_2_state = await ws_2.receive()
                        ws_3_state = await ws_3.receive()
                        ws_4_state = await ws_4.receive()
                        ws_5_state = await ws_5.receive()

    states = [ws_1_state, ws_2_state, ws_3_state, ws_4_state, ws_5_state]

    for string in states:
        state = json.loads(string)
        if player_is_mafia(state):
            assert gamestate_includes_other_mafia(state)
        else:
            assert gamestate_contains_only_own_role(state)


def player_is_mafia(state):
    return state["role"] == MafiaRole.MAFIA.value


def gamestate_contains_only_own_role(state):
    defined_roles = [player for player in state["players"] if player["role"] != None]
    return len(defined_roles) == 1


def gamestate_includes_other_mafia(state):
    defined_roles = [player for player in state["players"] if player["role"] != None]
    return len(defined_roles) == 2 and all(
        [player["role"] == MafiaRole.MAFIA.value for player in defined_roles]
    )
