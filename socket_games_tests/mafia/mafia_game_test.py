import pytest
from socket_games.mafia.lynch_vote_status import Vote

from socket_games.mafia.mafia_game import MafiaGame
from socket_games.mafia.mafia_role import MafiaRole
from socket_games.mafia.mafia_stage import MafiaStage


@pytest.fixture
def game_with_5_players() -> MafiaGame:
    game = MafiaGame()
    for i in range(0, 5):
        game.add_player(str(i))
    return game


def test_mafia_players_have_undefined_role_until_started(
    game_with_5_players: MafiaGame,
):
    for player in game_with_5_players.players:
        assert player.role == None


def test_mafia_players_get_assigned_role_on_start(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    for player in game_with_5_players.players:
        assert player.role != None


def test_game_starts_by_telling_mafia_of_others(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    mafia_player = get_player_with_role(game_with_5_players, MafiaRole.MAFIA)
    events = game_with_5_players.get_events_for_player(mafia_player.id)
    assert len(events) >= 1
    assert any([mafia_player.id in event for event in events])


def test_game_doesnt_tell_villager_of_mafia(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    mafia_player = get_player_with_role(game_with_5_players, MafiaRole.MAFIA)
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    events = game_with_5_players.get_events_for_player(villager_player.id)
    assert len(events) >= 1
    assert not any([mafia_player.id in event for event in events])


def test_after_game_start_it_is_daylight(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    assert game_with_5_players.day_count == 1
    assert game_with_5_players.stage == MafiaStage.DAY


def test_players_can_nominate_for_lynch_during_day(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    player_one = game_with_5_players.players[0].id
    player_two = game_with_5_players.players[1].id
    game_with_5_players.nominate_lynching(player_one, player_two)
    events = game_with_5_players.get_events_for_player(player_one)
    assert any([f"{player_one} nominated {player_two} " in event for event in events])
    assert game_with_5_players.vote_status != None
    assert game_with_5_players.vote_status.target == player_two


def test_players_cant_nominate_after_existing_nomination(
    game_with_5_players: MafiaGame,
):
    game_with_5_players.start_game()
    player_one = game_with_5_players.players[0].id
    player_two = game_with_5_players.players[1].id
    game_with_5_players.nominate_lynching(player_one, player_two)
    game_with_5_players.nominate_lynching(player_two, player_one)
    events = game_with_5_players.get_events_for_player(player_one)
    assert not any(
        [f"{player_two} nominated {player_one} " in event for event in events]
    )
    assert game_with_5_players.vote_status != None
    assert game_with_5_players.vote_status.target == player_two


def test_majority_voting_for_lynch_kills_nominee(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    players = game_with_5_players.players
    game_with_5_players.nominate_lynching(players[0].id, players[1].id)
    for i in range(0, 3):
        game_with_5_players.vote_for_lynch(players[i].id, Vote.LYNCH)
    for i in range(3, 5):
        game_with_5_players.vote_for_lynch(players[i].id, Vote.DONT_LYNCH)

    assert any(
        f"Player {players[1].id} was lynched" in event
        for event in game_with_5_players.get_events_for_player(players[0].id)
    )
    assert not players[1].is_alive


def test_exactly_half_voting_for_lynch_leaves_nominee_alive(
    game_with_5_players: MafiaGame,
):
    game_with_5_players.add_player("6")
    game = game_with_5_players
    game.start_game()
    players = game.players
    game.nominate_lynching(players[0].id, players[1].id)
    for i in range(0, 3):
        game.vote_for_lynch(players[i].id, Vote.LYNCH)
    for i in range(3, 6):
        game.vote_for_lynch(players[i].id, Vote.DONT_LYNCH)

    assert any(
        f"Player {players[1].id} was not lynched" in event
        for event in game.get_events_for_player(players[0].id)
    )
    assert players[1].is_alive


def test_successful_lynch_ends_day(game_with_5_players: MafiaGame):
    game = game_with_5_players
    game.start_game()
    players = game.players
    game.nominate_lynching(players[0].id, players[1].id)
    for player in players:
        game.vote_for_lynch(player.id, Vote.LYNCH)

    assert not players[1].is_alive
    assert game.stage == MafiaStage.NIGHT


def test_failed_lynch_doesnt_end_day(game_with_5_players: MafiaGame):
    game = game_with_5_players
    game.start_game()
    players = game.players
    game.nominate_lynching(players[0].id, players[1].id)
    for player in players:
        game.vote_for_lynch(player.id, Vote.DONT_LYNCH)

    assert players[1].is_alive
    assert game.stage == MafiaStage.DAY


def test_cant_nominate_for_lynch_at_night(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    game_with_5_players.complete_day()
    players = game_with_5_players.players
    game_with_5_players.nominate_lynching(players[0].id, players[1].id)
    events = game_with_5_players.get_events_for_player(players[0].id)
    assert not any(
        [f"{players[0].id} nominated {players[1].id} " in event for event in events]
    )


def test_villager_cant_vote_to_kill(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    game_with_5_players.complete_day()
    mafia_player = get_player_with_role(game_with_5_players, MafiaRole.MAFIA)
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    game_with_5_players.vote_to_kill(villager_player, mafia_player)


def test_mafia_can_vote_to_kill(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    game_with_5_players.complete_day()
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    mafia_player = get_player_with_role(game_with_5_players, MafiaRole.MAFIA)
    game_with_5_players.vote_to_kill(mafia_player.id, villager_player.id)
    assert len(game_with_5_players.vote_status.current_votes) == 1


def test_disagreeing_mafia_dont_kill(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    game_with_5_players.complete_day()
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    mafia_players = [
        player for player in game_with_5_players.players if player.is_evil()
    ]
    mafia_one = mafia_players[0]
    game_with_5_players.vote_to_kill(mafia_one.id, mafia_one.id)
    for i in range(1, len(mafia_players)):
        game_with_5_players.vote_to_kill(mafia_players[i].id, villager_player.id)
    assert len(game_with_5_players.vote_status.current_votes) == len(mafia_players)

    assert game_with_5_players.stage == MafiaStage.NIGHT
    assert all([player.is_alive for player in game_with_5_players.players])


def test_all_mafia_voting_kill(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    game_with_5_players.complete_day()
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    mafia_players = [
        player for player in game_with_5_players.players if player.is_evil()
    ]
    for i in range(0, len(mafia_players)):
        game_with_5_players.vote_to_kill(mafia_players[i].id, villager_player.id)

    assert game_with_5_players.stage == MafiaStage.DAY
    assert not villager_player.is_alive


def test_mafia_cant_vote_to_kill_during_day(game_with_5_players: MafiaGame):
    game_with_5_players.start_game()
    assert game_with_5_players.stage == MafiaStage.DAY

    mafia_player = get_player_with_role(game_with_5_players, MafiaRole.MAFIA)
    villager_player = get_player_with_role(game_with_5_players, MafiaRole.VILLAGER)
    game_with_5_players.vote_to_kill(mafia_player.id, villager_player.id)

    assert game_with_5_players.vote_status == None


def get_player_with_role(game: MafiaGame, role: MafiaRole):
    for player in game.players:
        if player.role == role:
            return player
    raise Exception(f"No player has role {role}")
