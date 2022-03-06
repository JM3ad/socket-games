from socket_games.mafia.vote_status import VoteStatus


class KillVoteStatus(VoteStatus):
    def __init__(self, expected_voters):
        super().__init__(expected_voters)

    def get_result(self):
        if len(self.current_votes) < len(self.expected_voters):
            return None
        first_voter = list(self.current_votes)[0]
        first_vote = self.current_votes[first_voter]
        if all(
            [self.current_votes[voter] == first_vote for voter in self.current_votes]
        ):
            return first_vote
        return None
