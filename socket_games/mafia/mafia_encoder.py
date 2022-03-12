import json
from socket_games.mafia.lynch_vote_status import Vote
from socket_games.mafia.mafia_player import MafiaPlayer

from socket_games.mafia.mafia_role import MafiaRole
from socket_games.mafia.mafia_stage import MafiaStage


class MafiaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Vote):
            return obj.value
        if isinstance(obj, MafiaRole):
            return obj.value
        if isinstance(obj, MafiaStage):
            return obj.value
        return json.JSONEncoder.default(self, obj)
