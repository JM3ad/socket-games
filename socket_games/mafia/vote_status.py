from abc import ABC
from typing import List


class VoteStatus(ABC):
    def __init__(self, expected_voters: List[str]):
        self.expected_voters = expected_voters
        self.current_votes = {}

    def add_vote(self, player_id, vote):
        self.current_votes[player_id] = vote

    def get_result(self):
        raise NotImplementedError()
