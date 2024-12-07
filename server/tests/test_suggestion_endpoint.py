from fastapi.testclient import TestClient
from util.functions import get_character_location
from util.enums import PlayerEnum, WeaponEnum, RoomEnum
from tests.util_functions import get_new_default_game_key, check_no_suggestion_return

from main import app, games

client = TestClient(app)


def test_bad_no_player_suggest():
    """
    Test to check having no player returns a HTTP 400 message
    """
    key = get_new_default_game_key(2)
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 400


def test_bad_key_suggest():
    """
    Test to check having no valid key returns a HTTP 400 message
    """
    get_new_default_game_key(2)
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": "",
            "player": "player1",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 400


def test_bad_no_suggest():
    """
    Test to check having an empty suggestion returns a HTTP 400 message
    """
    key = get_new_default_game_key(2)
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": None,
                "weapon": None,
                "room": None,
            },
        },
    )
    assert response.status_code == 400


def test_bad_player_suggest():
    """
    Test to check having a bad player ID returns a HTTP 404 message
    """
    key = get_new_default_game_key(2)
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player0",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 404


def test_bad_player_not_in_same_room_suggest():
    """
    Test to check that when a suggestion is not in the same room
    as the suggestor, a HTTP 403 message is returned
    """
    key = get_new_default_game_key(2)
    games[key].current_turn.phase = "suggest"
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 403


def test_good_suggestion_moves_other_character():
    """
    Test to check a valid suggestion properly moves the
    suggested character
    """
    key = get_new_default_game_key(6)
    client.post(
        "/move", json={"player": "player1", "location": RoomEnum.lounge, "id": key}
    )
    # Check the lounge only has 1 player in it
    games[key].current_turn.phase = "suggest"
    assert len(games[key].map[RoomEnum.lounge]) == 1
    old_location = get_character_location(PlayerEnum.prof_plum, games[key])
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.lounge,
            },
        },
    )
    assert response.status_code == 200

    # Check the suggested character has been moved
    if old_location != RoomEnum.staging:
        assert len(games[key].map[old_location]) == 0
    assert len(games[key].map[RoomEnum.lounge]) == 2
    assert games[key].current_turn.phase == "accuse"


def test_good_suggestion_of_same_character_does_not_copy_them():
    """
    Test to check a valid suggestion which suggests the same character
    as the player does not copy the character in the same location
    """
    key = get_new_default_game_key(6)
    client.post(
        "/move", json={"player": "player1", "location": RoomEnum.lounge, "id": key}
    )
    # Check the lounge only has 1 player in it
    assert len(games[key].map[RoomEnum.lounge]) == 1
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": PlayerEnum.miss_scarlet,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.lounge,
            },
        },
    )
    assert response.status_code == 200

    # Check the suggested character has not been copied
    assert len(games[key].map[RoomEnum.lounge]) == 1
    assert games[key].current_turn.phase == "accuse"


def test_good_suggestion_returns_card_or_no_card_if_solution_or_hand():
    """
    Test that a valid suggestion will return a card, or if a card is not reutrned,
    that all elements in the suggestion are either in the player's hand or in the
    game solution
    """
    key = get_new_default_game_key(6)
    client.post(
        "/move", json={"player": "player1", "location": RoomEnum.lounge, "id": key}
    )
    # Check the lounge only has 1 player in it
    response = client.post(
        "/suggestion/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": PlayerEnum.prof_plum,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.lounge,
            },
        },
    )
    assert response.status_code == 200

    # Check the suggested character has been moved
    assert len(games[key].map[RoomEnum.lounge]) == 2
    assert games[key].current_turn.phase == "accuse"

    results = response.json()
    # Vaildate a card was found to disprove a suggestion or if
    # no card was returned, check if it is part of the suggestor's
    # hand or solution.
    assert results["response"] or check_no_suggestion_return(
        games[key].current_turn.player,
        PlayerEnum.prof_plum,
        WeaponEnum.knife,
        RoomEnum.lounge,
        games[key],
    ), "No card was returned, when one should have been!"
