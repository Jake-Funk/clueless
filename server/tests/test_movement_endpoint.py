from fastapi.testclient import TestClient
from util.functions import get_character_location
from util.game_state import GameState
from util.enums import PlayerEnum, HallEnum, RoomEnum, HttpEnum
from util.movement import move_player, validate_move, does_possible_move_exist
from tests.data.move_actions import MOVES
from tests.util_functions import get_new_default_game_key
import pytest

from main import app, games

client = TestClient(app)

# Default player ids in a 6 player game
default_players = [f"player{i+1}" for i in range(6)]


@pytest.mark.parametrize("player", default_players)
def test_get_player_default_locations(player: str):
    """
    Test to gaurantee that the get_player_location
    function works using the default game state
    """
    default_gs = GameState(6)

    location = get_character_location(
        default_gs.player_character_mapping[player], default_gs
    )
    character = PlayerEnum(default_gs.player_character_mapping[player])

    if character == PlayerEnum.miss_scarlet:
        assert location == HallEnum.hall_to_lounge
    elif character == PlayerEnum.col_mustard:
        assert location == HallEnum.lounge_to_dining
    elif character == PlayerEnum.mrs_white:
        assert location == HallEnum.ballroom_to_kitchen
    elif character == PlayerEnum.mr_green:
        assert location == HallEnum.conservatory_to_ballroom
    elif character == PlayerEnum.mrs_peacock:
        assert location == HallEnum.lib_to_conservatory
    elif character == PlayerEnum.prof_plum:
        assert location == HallEnum.study_to_lib
    else:
        assert False, "Not a valid player"


def test_bad_key_move():
    response = client.post(
        "move/", json={"player": "player1", "location": RoomEnum.lounge, "id": "bad"}
    )
    assert response.status_code == 404


def test_bad_player_move():
    key = get_new_default_game_key(2)
    response = client.post(
        "/move", json={"player": "player0", "location": RoomEnum.lounge, "id": key}
    )
    assert response.status_code == 404


def test_movement():
    """
    Test to check that the move_player function removes
    the player from the old location and adds them to
    the new location and validates movement
    """
    key = get_new_default_game_key(2)

    # Check valid move of Miss Scarlet to Lounge
    response = client.post(
        "/move", json={"player": "player1", "location": RoomEnum.lounge, "id": key}
    )
    assert response.status_code == 200
    assert len(games[key].map[HallEnum.hall_to_lounge]) == 0
    assert len(games[key].map[RoomEnum.lounge]) == 1
    assert games[key].current_turn.phase == "suggest"

    # Reset Movement
    games[key].current_turn.phase = "move"

    # Check Invalid move to Occupied Hallway
    response = client.post(
        "/move",
        json={"player": "player1", "location": HallEnum.lounge_to_dining, "id": key},
    )
    assert response.status_code == 400
    assert len(games[key].map[HallEnum.lounge_to_dining]) == 1
    assert len(games[key].map[RoomEnum.lounge]) == 1
    assert games[key].current_turn.phase == "move"

    # Check Valid move to Hallway
    response = client.post(
        "/move",
        json={"player": "player1", "location": HallEnum.hall_to_lounge, "id": key},
    )
    assert response.status_code == 200
    assert len(games[key].map[HallEnum.hall_to_lounge]) == 1
    assert len(games[key].map[RoomEnum.lounge]) == 0
    assert games[key].current_turn.phase == "accuse"

    games[key].current_turn.phase = "move"

    # Check Invalid Move to non-adjacent hallway
    response = client.post(
        "/move",
        json={"player": "player1", "location": HallEnum.study_to_hall, "id": key},
    )
    assert response.status_code == 400
    assert len(games[key].map[HallEnum.hall_to_lounge]) == 1
    assert len(games[key].map[HallEnum.study_to_hall]) == 0
    assert games[key].current_turn.phase == "move"

    # Check Invalid Move to non-adjacent room
    response = client.post(
        "/move", json={"player": "player1", "location": RoomEnum.study, "id": key}
    )
    assert response.status_code == 400
    assert len(games[key].map[HallEnum.hall_to_lounge]) == 1
    assert len(games[key].map[RoomEnum.study]) == 0
    assert games[key].current_turn.phase == "move"


def test_validate_move_on_different_turn_phase():
    """
    Test to make sure a bad request is returned when
    trying to move in the wrong phase of the turn
    """
    default_gs = GameState(6)
    default_gs.current_turn.phase = "suggest"

    # Check valid move when not in correct phase
    assert (
        validate_move(MOVES[2], HallEnum.study_to_lib, default_gs)[0]
        == HttpEnum.bad_request
    )


def test_possible_move_exist():
    """
    Simple check to validate the does_possible_move_exist function
    """
    default_gs = GameState(6)

    # Assert a valid move exists
    assert does_possible_move_exist(HallEnum.conservatory_to_ballroom, default_gs)

    default_gs.map[RoomEnum.conservatory] = PlayerEnum.mrs_white
    # Assert a valid move exists
    assert does_possible_move_exist(RoomEnum.conservatory, default_gs)

    default_gs.map[HallEnum.billiard_to_ballroom] = PlayerEnum.prof_plum
    # Assert no possible move exists
    assert not does_possible_move_exist(RoomEnum.ballroom, default_gs)
