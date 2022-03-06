"""
start in night time
Mafia told who else is mafia
then day, chance to lynch
then night, mafia kill
repeat until mafia all dead or mafia outnumber villagers
"""
from random import sample
from typing import List
from socket_games.mafia.kill_vote_status import KillVoteStatus
from socket_games.mafia.lynch_vote_status import LynchVoteStatus, Vote
from socket_games.mafia.mafia_event import MafiaEvent
from socket_games.mafia.mafia_player import MafiaPlayer
from socket_games.mafia.mafia_role import MafiaRole
from socket_games.mafia.mafia_stage import MafiaStage


class MafiaGame:
    def __init__(self):
        self.day_count = 0
        self.stage = MafiaStage.NIGHT
        self.players: List[MafiaPlayer] = []
        self.events: List[MafiaEvent] = []
        self.vote_status = None

    def add_player(self, player_id):
        if player_id not in [player.id for player in self.players]:
            self.players.append(MafiaPlayer(player_id, None))

    def reset_game(self):
        self.day_count = 0
        self.stage = MafiaStage.NIGHT
        self.events = []
        for player in self.players:
            player.reset()

    def start_game(self):
        ## TODO make this variable?
        self.reset_game()
        number_of_mafia = 2
        mafia_players = sample(self.players, number_of_mafia)
        for member in mafia_players:
            member.role = MafiaRole.MAFIA
        for player in self.players:
            if player not in mafia_players:
                player.role = MafiaRole.VILLAGER
        villager_event = "The Mafia identify each other"
        mafia_event = f"You recognise your fellow criminals: {', '.join([mafia.id for mafia in mafia_players])}"
        self._add_event(
            MafiaEvent(
                {
                    MafiaRole.MAFIA: mafia_event,
                    MafiaRole.VILLAGER: villager_event,
                }
            )
        )
        self._progress_stage()

    def nominate_lynching(self, nominater: str, nominee: str):
        if self.vote_status != None or self.stage != MafiaStage.DAY:
            print("Nomination already in play")
            return
        nomination_description = f"{nominater} nominated {nominee} to be lynched"
        self._add_event(
            MafiaEvent(
                {
                    MafiaRole.VILLAGER: nomination_description,
                }
            )
        )
        living_player_ids = [player.id for player in self.players if player.is_alive]
        self.vote_status = LynchVoteStatus(living_player_ids, nominee)

    def vote_for_lynch(self, voter: str, vote: str):
        if not self.vote_status:
            return
        self.vote_status.add_vote(voter, vote)
        if self.vote_status.get_result() != None:
            lynch_result = (
                "lynched"
                if self.vote_status.get_result() == Vote.LYNCH
                else "not lynched"
            )
            result_description = f"Player {self.vote_status.target} was {lynch_result}"
            print("registering result")
            self._add_event(
                MafiaEvent(
                    {
                        MafiaRole.VILLAGER: result_description,
                    }
                )
            )
            if self.vote_status.get_result() == Vote.LYNCH:
                target_player = [
                    player
                    for player in self.players
                    if player.id == self.vote_status.target
                ][0]
                target_player.kill()
                self.complete_day()

    def get_game_outcome(self):
        pass

    def vote_to_kill(self, nominater, nominee):
        if self.vote_status == None or self.stage != MafiaStage.NIGHT:
            return
        self.vote_status.add_vote(nominater, nominee)
        if self.vote_status.get_result() != None:
            killed_player = self.vote_status.get_result()
            result_description = f"Mafia killed {killed_player} in the night"
            self._add_event(
                MafiaEvent(
                    {
                        MafiaRole.VILLAGER: result_description,
                    }
                )
            )
            target_player = [
                player for player in self.players if player.id == killed_player
            ][0]
            target_player.kill()
            self._progress_stage()

    def get_events_for_player(self, player_id: str):
        player = [player for player in self.players if player.id == player_id][0]
        player_role = player.role
        return [event.describe_for_role(player_role) for event in self.events]

    def complete_day(self):
        if self.stage == MafiaStage.DAY:
            self._progress_stage()

    def _add_event(self, event):
        self.events.append(event)

    def _progress_stage(self):
        if self.get_game_outcome() != None:
            return
        if self.stage == MafiaStage.NIGHT:
            self.stage = MafiaStage.DAY
            self.day_count = 1
            self.vote_status = None
        else:
            self.stage = MafiaStage.NIGHT
            living_mafia = [
                player.id
                for player in self.players
                if player.is_alive and player.is_evil()
            ]
            self.vote_status = KillVoteStatus(living_mafia)
