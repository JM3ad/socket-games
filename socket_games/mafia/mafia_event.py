from typing import Dict
from socket_games.mafia.mafia_role import MafiaRole


class MafiaEvent:
    def __init__(self, role_descriptions):
        self.role_descriptions: Dict[MafiaRole, str] = role_descriptions

    def describe_for_role(self, role):
        if role in self.role_descriptions:
            return self.role_descriptions[role]
        return self.role_descriptions[MafiaRole.VILLAGER]
