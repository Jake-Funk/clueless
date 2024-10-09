from util.functions import get_player_location
from util.game_state import GameState
from util.enums import PlayerEnum, HallEnum, RoomEnum, HttpEnum, MoveAction
from util.movement import move_player, validate_move, does_possible_move_exist
from tests.data.move_actions import MOVES, DUMMY_MOVE_ID
import pytest


@pytest.mark.parametrize("player", list(PlayerEnum))
def test_get_player_default_locations(player: int):
    """
    Test to gaurantee that the get_player_location
    function works using the default game state
    """
    default_gs = GameState(6)

    location = get_player_location(player, default_gs)

    if player == PlayerEnum.miss_scarlet:
        assert location == HallEnum.hall_to_lounge
    elif player == PlayerEnum.col_mustard:
        assert location == HallEnum.lounge_to_dining
    elif player == PlayerEnum.mrs_white:
        assert location == HallEnum.ballroom_to_kitchen
    elif player == PlayerEnum.mr_green:
        assert location == HallEnum.conservatory_to_ballroom
    elif player == PlayerEnum.mrs_peacock:
        assert location == HallEnum.lib_to_conservatory
    elif player == PlayerEnum.prof_plum:
        assert location == HallEnum.study_to_lib
    else:
        assert False, "Not a valid player"


def test_move_player():
    """
    Test to check that the move_player function removes
    the player from the old location and adds them to
    the new location
    """
    default_gs = GameState(6)
    player = PlayerEnum.prof_plum

    assert player in default_gs.map[HallEnum.study_to_lib], "Control check"

    # Move plum to study
    move_player(MOVES[2], HallEnum.study_to_lib, default_gs)
    assert (
        player not in default_gs.map[HallEnum.study_to_lib]
    ), "Player in original location"
    assert player in default_gs.map[RoomEnum.study], "Player not in study after move"

    # Move plum to kitchen
    move_player(MOVES[3], RoomEnum.study, default_gs)
    assert player not in default_gs.map[RoomEnum.study], "Player in original location"
    assert (
        player in default_gs.map[RoomEnum.kitchen]
    ), "Player not in kitchen after move"

    # Move plum to dining to kitchen hallway
    move_player(MOVES[4], RoomEnum.kitchen, default_gs)
    assert player not in default_gs.map[RoomEnum.kitchen], "Player in original location"
    assert (
        player in default_gs.map[HallEnum.dining_to_kitchen]
    ), "Player not in hallway after move"


def test_validate_move_with_plum_moves():
    """
    Test which moves player professor plum around in various
    states to check the conditions of validate_player are
    correct.
    """
    default_gs = GameState(6)

    # Check valid move to study
    assert (
        validate_move(MOVES[2], HallEnum.study_to_lib, default_gs)[0] == HttpEnum.good
    )
    move_player(MOVES[2], HallEnum.study_to_lib, default_gs)

    # Check bad non-adjacent moves
    assert (
        validate_move(MOVES[0], RoomEnum.study, default_gs)[0] == HttpEnum.bad_request
    )
    assert (
        validate_move(MOVES[1], RoomEnum.study, default_gs)[0] == HttpEnum.bad_request
    )

    # Check valid move to kitchen
    assert validate_move(MOVES[3], RoomEnum.study, default_gs)[0] == HttpEnum.good
    move_player(MOVES[3], RoomEnum.study, default_gs)

    # Check valid move to unoccupied hallway
    assert validate_move(MOVES[4], RoomEnum.kitchen, default_gs)[0] == HttpEnum.good


def test_validate_move_with_green_moves():
    """
    Test which moves player mr green around to check
    that moving in an occupied hallway leads to a
    bad request being returned
    """
    default_gs = GameState(6)

    # Check valid move to ballroom
    assert (
        validate_move(MOVES[5], HallEnum.conservatory_to_ballroom, default_gs)[0]
        == HttpEnum.good
    )
    move_player(MOVES[5], HallEnum.conservatory_to_ballroom, default_gs)

    # Check bad move to occupied hallway
    assert (
        validate_move(MOVES[6], RoomEnum.ballroom, default_gs)[0]
        == HttpEnum.bad_request
    )


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
