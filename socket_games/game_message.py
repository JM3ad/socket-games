from abc import ABC, abstractmethod


class GameMessage(ABC):
    @abstractmethod
    def get_game_info_for_user(self, player_id):
        raise NotImplementedError()
