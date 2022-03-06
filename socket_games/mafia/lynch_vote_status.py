from enum import Enum

from socket_games.mafia.vote_status import VoteStatus


class Vote(Enum):
    LYNCH = True
    DONT_LYNCH = False


class LynchVoteStatus(VoteStatus):
    def __init__(self, expected_voters, target):
        self.target = target
        super().__init__(expected_voters)

    def get_result(self):
        if all([expected in self.current_votes for expected in self.expected_voters]):
            quorum = len(self.expected_voters) // 2
            votes_for = len(
                [
                    vote
                    for vote in self.current_votes
                    if self.current_votes[vote] == Vote.LYNCH
                ]
            )
            if votes_for > quorum:
                return Vote.LYNCH
            else:
                return Vote.DONT_LYNCH
        # TODO return number of players left to vote?
        return None
