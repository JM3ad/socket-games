import json

from socket_games_tests.tic_tac_toe.ttt_state_helper import completed_game

from socket_games.tic_tac_toe.ttt_encoder import TicTacToeEncoder


def test_game_state_encoder(completed_game):
    result = json.dumps(
        {
            "board": completed_game.board,
            "result": completed_game.get_result(),
            "players": completed_game.player_roles,
        },
        cls=TicTacToeEncoder,
    )
    loaded = json.loads(result)

    assert "X" in loaded["board"]
    assert "O" in loaded["board"]
    assert loaded["board"] == [square.value for square in completed_game.board]
    assert loaded["result"] == "Player X Win"
    assert loaded["players"] == {"a": "O", "b": "X"} or loaded["players"] == {
        "b": "O",
        "a": "X",
    }
