'''
start in night time
Mafia told who else is mafia
then day, chance to lynch
then night, mafia kill
repeat until mafia all dead or mafia outnumber villagers
'''
from random import sample
from typing import List
from socket_games.mafia.mafia_player import MafiaPlayer
from socket_games.mafia.mafia_role import MafiaRole
from socket_games.mafia.mafia_stage import MafiaStage


class MafiaGame():
    def __init__(self):
        self.days = 0
        self.stage = MafiaStage.NIGHT
        self.players: List[MafiaPlayer] = []
        self.events = []

    def add_player(self, player_id):
        if player_id not in [player.id for player in self.players]:
            self.players.append(MafiaPlayer(player_id, None))

    def reset_game(self):
        self.days = 0
        self.stage = MafiaStage.NIGHT
        self.events = []
        for player in self.players:
            player.reset()

    def start_game(self):
        ## TODO make this variable?
        number_of_mafia = 2
        mafia_players = sample(self.players, number_of_mafia)
        for member in mafia_players:
            member.role = MafiaRole.MAFIA
        for player in self.players:
            if player not in mafia_players:
                player.role = MafiaRole.VILLAGER

    def nominate_lynching(self, nominater, nominee):
        pass

    def vote_for_lynch(self, voter, vote):
        pass

    def progress_game(self):
        pass

    def get_game_outcome(self):
        pass

    def vote_to_kill(self, nominater, nominee):
        pass

    def get_events_for_player(self, player_id):
        pass