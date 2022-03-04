import pytest

from socket_games.tic_tac_toe.ttt_game_state import TicTacToeState
from socket_games.tic_tac_toe.ttt_player import TicTacToePlayer


@pytest.fixture
def completed_game():
    state = TicTacToeState()
    state.add_player("a")
    state.add_player("b")
    state.assign_players()

    first_player = get_p1(state.player_roles)
    second_player = get_p2(state.player_roles)

    state.play_move("top-left", first_player)
    state.play_move("middle-left", second_player)
    state.play_move("top-centre", first_player)
    state.play_move("middle-centre", second_player)
    state.play_move("top-right", first_player)
    return state


def get_p1(roles):
    for role_key in roles:
        if roles[role_key] == TicTacToePlayer.X:
            return role_key


def get_p2(roles):
    for role_key in roles:
        if roles[role_key] == TicTacToePlayer.O:
            return role_key
