import pytest

from socket_games.mafia.mafia_game import MafiaGame

@pytest.fixture
def game_with_5_players() -> MafiaGame:
    game = MafiaGame()
    for i in range(0, 5):
        game.add_player(i)
    return game

def test_mafia_players_have_undefined_role_until_started(game_with_5_players: MafiaGame):
    for player in game_with_5_players.players:
        assert player.role == None

def test_mafia_players_get_assigned_role_on_start(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    for player in game_with_5_players.players:
        assert player.role != None

def test_game_starts_by_telling_mafia_of_others():
    raise NotImplementedError

def test_game_doesnt_tell_villager_of_mafia():
    raise NotImplementedError

def test_villagers_can_nominate_for_lynch():
    raise NotImplementedError

def test_majority_voting_for_lynch_kills_nominee():
    raise NotImplementedError

def test_exactly_half_voting_for_lynch_leaves_nominee_alive():
    raise NotImplementedError

def test_villager_cant_vote_to_kill():
    raise NotImplementedError

def test_mafia_can_vote_to_kill():
    raise NotImplementedError

def test_disagreeing_mafia_dont_kill():
    raise NotImplementedError

def test_all_mafia_voting_kill():
    raise NotImplementedError

def test_mafia_cant_vote_to_kill_during_day():
    raise NotImplementedError

def test_cant_nominate_for_lynch_at_night():
    raise NotImplementedError

def test_cant_vote_for_lynch_at_night():
    raise NotImplementedError