import random
from socket_games.tic_tac_toe.ttt_game_result import GameResult

from socket_games.tic_tac_toe.ttt_player import TicTacToePlayer
from socket_games.tic_tac_toe.ttt_square import TicTacToeSquare


CELL_IDS = {
    "top-left": 0,
    "top-centre": 1,
    "top-right": 2,
    "middle-left": 3,
    "middle-centre": 4,
    "middle-right": 5,
    "bottom-left": 6,
    "bottom-centre": 7,
    "bottom-right": 8,
}


class TicTacToeState:
    def __init__(self):
        self.board = [TicTacToeSquare.EMPTY] * 9
        self.players = []
        self.player_roles = {}

    def reset(self):
        self.board = [TicTacToeSquare.EMPTY] * 9
        self.assign_players()

    def assign_players(self):
        if len(self.players) < 2:
            return

        x_player = random.choice([0, 1])
        o_player = 1 - x_player
        self.player_roles = {
            self.players[x_player]: TicTacToePlayer.X,
            self.players[o_player]: TicTacToePlayer.O,
        }

    def add_player(self, id):
        if id not in self.players:
            print(f"Adding {id}")
            self.players.append(id)

    def play_move(self, cell_name, player_id):
        if cell_name not in CELL_IDS:
            return
        cell = CELL_IDS[cell_name]
        if player_id not in self.player_roles:
            return
        player = self.player_roles[player_id]
        print("This far")
        print(self.board[cell])
        print(player)
        if (
            self.board[cell] == TicTacToeSquare.EMPTY
            and player == self.get_player_turn()
            and self.is_unfinished()
        ):
            print("Trying?")
            move = (
                TicTacToeSquare.X if player == TicTacToePlayer.X else TicTacToeSquare.O
            )
            self.board[cell] = move

    def is_unfinished(self):
        return self.get_result() == None

    def get_player_turn(self):
        turns_played = len(
            [square for square in self.board if square != TicTacToeSquare.EMPTY]
        )
        if turns_played % 2 == 0:
            return TicTacToePlayer.X
        else:
            return TicTacToePlayer.O

    def get_result(self):
        possible_winning_combos = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (6, 4, 2),
        ]
        for combo in possible_winning_combos:
            if self._do_squares_match(combo[0], combo[1], combo[2]):
                winning_square = self.board[combo[0]]
                return (
                    GameResult.X_WIN
                    if winning_square == TicTacToeSquare.X
                    else GameResult.O_WIN
                )

        if (
            len([square for square in self.board if square != TicTacToeSquare.EMPTY])
            == 9
        ):
            return GameResult.DRAW
        return None

    def _do_squares_match(self, idx_1, idx_2, idx_3):
        game = self.board
        return (
            game[idx_1] != TicTacToeSquare.EMPTY
            and game[idx_1] == game[idx_2]
            and game[idx_2] == game[idx_3]
        )
