from socket_games.mafia.mafia_role import MafiaRole


class MafiaPlayer:
    def __init__(self, id: str, role: MafiaRole):
        self.id = id
        self.role = role
        self.is_alive: bool = True

    def kill(self):
        self.is_alive = False

    def reset(self):
        self.is_alive = True
        self.role = None

    def is_evil(self):
        return self.role == MafiaRole.MAFIA
