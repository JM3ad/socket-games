import pytest

from socket_games.tic_tac_toe.ttt_game_result import GameResult
from socket_games.tic_tac_toe.ttt_game_state import CELL_IDS, TicTacToeState
from socket_games.tic_tac_toe.ttt_square import TicTacToeSquare
from socket_games_tests.tic_tac_toe.ttt_state_helper import get_p1, get_p2

A_POSITION = next(iter(CELL_IDS))


@pytest.fixture
def game_with_players():
    state = TicTacToeState()
    state.add_player("a")
    state.add_player("b")
    state.assign_players()
    return state


def test_game_starts_with_fresh_board():
    state = TicTacToeState()

    assert len(state.board) == 9
    assert all([square == TicTacToeSquare.EMPTY for square in state.board])


def test_game_result_returns_unfinished_initially():
    state = TicTacToeState()

    assert state.is_unfinished()


def test_game_result_returns_unfinished_if_no_winner_yet():
    state = TicTacToeState()
    state.board = [
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.EMPTY,
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.O,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.X,
    ]

    assert state.is_unfinished()


def test_game_result_returns_draw_if_no_winner_after_9_moves():
    state = TicTacToeState()
    state.board = [
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.O,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.X,
    ]

    assert state.get_result() == GameResult.DRAW


def test_game_result_returns_winner_if_three_in_a_row():
    state = TicTacToeState()
    state.board = [
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.O,
        TicTacToeSquare.X,
        TicTacToeSquare.X,
    ]

    assert state.get_result() == GameResult.X_WIN


def test_game_handles_player_added_twice():
    state = TicTacToeState()
    p1_id = "abc"
    p2_id = "bcd"

    state.add_player(p1_id)
    state.add_player(p2_id)

    # assert no exception
    state.add_player(p1_id)


def test_game_doesnt_asign_roles_if_only_one_player():
    state = TicTacToeState()
    p1_id = "abc"
    state.add_player(p1_id)

    state.assign_players()

    assert state.player_roles == {}


def test_game_reset_restores_initial_board_state(game_with_players: TicTacToeState):
    first_player = get_p1(game_with_players.player_roles)
    game_with_players.play_move(A_POSITION, first_player)
    assert not is_board_fresh(game_with_players.board)

    game_with_players.reset()
    assert is_board_fresh(game_with_players.board)


def test_game_doesnt_play_move_out_of_turn(game_with_players: TicTacToeState):
    second_player = get_p2(game_with_players.player_roles)
    game_with_players.play_move(A_POSITION, second_player)
    assert is_board_fresh(game_with_players.board)


def test_game_doesnt_allow_move_to_already_played_square(
    game_with_players: TicTacToeState,
):
    first_player = get_p1(game_with_players.player_roles)
    second_player = get_p2(game_with_players.player_roles)
    game_with_players.play_move(A_POSITION, first_player)
    played_squares = [
        square for square in game_with_players.board if square != TicTacToeSquare.EMPTY
    ]
    assert len(played_squares) == 1

    game_with_players.play_move(A_POSITION, second_player)
    played_squares = [
        square for square in game_with_players.board if square != TicTacToeSquare.EMPTY
    ]
    assert len(played_squares) == 1


def test_game_doesnt_allow_move_to_finished_game(game_with_players: TicTacToeState):
    first_player = get_p1(game_with_players.player_roles)
    second_player = get_p2(game_with_players.player_roles)
    game_with_players.play_move("top-left", first_player)
    game_with_players.play_move("middle-left", second_player)
    game_with_players.play_move("top-centre", first_player)
    game_with_players.play_move("middle-centre", second_player)
    game_with_players.play_move("top-right", first_player)

    assert game_with_players.get_result() == GameResult.X_WIN
    game_with_players.play_move("middle-right", second_player)

    played_squares = [
        square for square in game_with_players.board if square != TicTacToeSquare.EMPTY
    ]
    assert len(played_squares) == 5


def is_board_fresh(board):
    return all([square == TicTacToeSquare.EMPTY for square in board])
