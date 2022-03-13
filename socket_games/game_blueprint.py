from abc import abstractmethod
from quart import Blueprint


class GameBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def is_relevant_game(self, game):
        raise NotImplementedError()

    @abstractmethod
    def get_game_url(self, game_id: str):
        raise NotImplementedError()
