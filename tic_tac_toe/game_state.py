class TicTacToeState:
    def __init__(self):
        self.board = ["."] * 9
        self.players = []
        self.player_roles = {}

    def reset(self):
        self.board = ["."] * 9

    def assign_players(self):
        self.player_roles = {self.players[0]: "X", self.players[1]: "O"}

    def add_player(self, id):
        if id not in self.players:
            print(f"Adding {id}")
            self.players.append(id)

    def play_move(self, cell, player_id):
        if player_id not in self.player_roles:
            return
        player = self.player_roles[player_id]
        if (
            self.board[cell] == "."
            and player == self.get_player_turn()
            and self.is_unfinished()
        ):
            self.board[cell] = player

    def is_unfinished(self):
        return self.get_result() == "Unfinished"

    def get_player_turn(self):
        turns_played = len([square for square in self.board if square != "."])
        if turns_played % 2 == 0:
            return "X"
        else:
            return "O"

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
                winner = self.board[combo[0]]
                return f"Player {winner} wins"

        if len([square for square in self.board if square != "."]) == 9:
            return "Draw"
        return "Unfinished"

    def _do_squares_match(self, idx_1, idx_2, idx_3):
        game = self.board
        return (
            game[idx_1] != "."
            and game[idx_1] == game[idx_2]
            and game[idx_2] == game[idx_3]
        )
