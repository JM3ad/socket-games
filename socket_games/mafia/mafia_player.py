class MafiaPlayer():
    def __init__(self, id, role):
        self.id = id
        self.role = role
        self.is_alive = True

    def kill(self):
        self.is_alive = False

    def reset(self):
        self.is_alive = True
        self.role = None