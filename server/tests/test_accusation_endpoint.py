from fastapi.testclient import TestClient
from util.game_state import GameState
from util.enums import PlayerEnum, WeaponEnum, HallEnum, RoomEnum, HttpEnum
from tests.util_functions import get_new_default_game_key
import pytest

from main import app, games

client = TestClient(app)


def test_bad_key_accuse():
    """
    Check that a bad game key will return a 404
    """
    response = client.post(
        "/accusation/",
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
    assert response.status_code == 404


def test_good_no_accusation():
    """
    Test that not inputting an accusation will move the game to the
    next player
    """
    key = get_new_default_game_key(2)
    response = client.post(
        "/accusation/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {"person": None, "weapon": None, "room": None},
        },
    )
    assert response.status_code == 200
    # Check the game has moved to the next player (1 from 0) and movement phase
    assert games[key].current_turn.player == 1
    assert games[key].current_turn.phase == "move"
    assert games[key].victory_state == 0


def test_good_correct_accusation():
    """
    Test that a correct accusation will change the victory_state to 2
    and perform the correct actions
    """
    key = get_new_default_game_key(2)
    response = client.post(
        "/accusation/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": games[key].solution.person,
                "weapon": games[key].solution.weapon,
                "room": games[key].solution.room,
            },
        },
    )
    assert response.status_code == 200
    # Check the game has not switched players or phase
    assert games[key].current_turn.player == 0

    # Check the victory state changed to 2
    assert games[key].victory_state == 2
    assert len(games[key].moveable_players) == 2


def test_good_bad_accusation():
    """
    Test that performing bad accusations performs the correct
    sequence of actions and ends up changing victory_state to 1
    """
    key = get_new_default_game_key(2)
    # Guarantee that the requested character is wrong
    player = PlayerEnum.prof_plum
    if games[key].solution.person == PlayerEnum.prof_plum:
        player = PlayerEnum.miss_scarlet

    response = client.post(
        "/accusation/",
        json={
            "gameKey": key,
            "player": "player1",
            "statementDetails": {
                "person": player,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 200
    # Check the game has switched players and phase
    assert games[key].current_turn.player == 1
    assert games[key].current_turn.phase == "move"

    # Check the victory state has not changed
    assert games[key].victory_state == 0
    assert len(games[key].moveable_players) < 2

    # Repeat for second player to trigger no winners end state
    response = client.post(
        "/accusation/",
        json={
            "gameKey": key,
            "player": "player2",
            "statementDetails": {
                "person": player,
                "weapon": WeaponEnum.knife,
                "room": RoomEnum.study,
            },
        },
    )
    assert response.status_code == 200
    # Check the game has switched players and moved to the move phase
    assert games[key].current_turn.player == 1
    assert games[key].current_turn.phase == "move"

    # Check the victory state changed to 1
    assert games[key].victory_state == 1
    assert len(games[key].moveable_players) < 2
