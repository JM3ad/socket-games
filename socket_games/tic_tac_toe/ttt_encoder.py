import json
from socket_games.tic_tac_toe.ttt_game_result import GameResult

from socket_games.tic_tac_toe.ttt_player import TicTacToePlayer
from socket_games.tic_tac_toe.ttt_square import TicTacToeSquare


class TicTacToeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TicTacToePlayer):
            return obj.value
        if isinstance(obj, TicTacToeSquare):
            return obj.value
        if isinstance(obj, GameResult):
            return obj.value
        return json.JSONEncoder.default(self, obj)
