import json
from socket_games.game_message import GameMessage
from socket_games.mafia.mafia_encoder import MafiaEncoder
from socket_games.mafia.mafia_game import MafiaGame


class MafiaSocketMessage(GameMessage):
    def __init__(self, game: MafiaGame):
        self.game = game

    def get_game_info_for_user(self, player_id):
        if self.game == None:
            return None
        return json.dumps(
            {
                "role": self.game.get_role_for_player(player_id),
                "day_count": self.game.day_count,
                "stage": self.game.stage,
                "players": self.game.get_all_players_as_seen_by(player_id),
                "events": self.game.get_events_for_player(player_id),
                "vote_status": self.game.get_vote_status_for_player(player_id),
            },
            cls=MafiaEncoder,
        )
