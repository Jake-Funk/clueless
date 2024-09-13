from util.functions import get_player_location
from util.game_state import GameState
from util.enums import PlayerEnum, HallEnum, RoomEnum, MoveAction
from util.movement import move_player
from tests.data.move_actions import MOVES
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
    """
    default_gs = GameState(6)
    player  = PlayerEnum.prof_plum

    assert player in default_gs.map[HallEnum.study_to_lib], "Control check"

    # Move plum to study 
    move_player(MOVES[2], HallEnum.study_to_lib, default_gs)
    assert player not in default_gs.map[HallEnum.study_to_lib], "Player in original location"
    assert player in default_gs.map[RoomEnum.study], "Player not in study after move"

    # Move plum to kitchen 
    move_player(MOVES[3], RoomEnum.study, default_gs)
    assert player not in default_gs.map[RoomEnum.study], "Player in original location"
    assert player in default_gs.map[RoomEnum.kitchen], "Player not in kitchen after move"

    # Move plum to dining to kitchen hallway
    move_player(MOVES[4], RoomEnum.kitchen, default_gs)
    assert player not in default_gs.map[RoomEnum.kitchen], "Player in original location"
    assert player in default_gs.map[HallEnum.dining_to_kitchen], "Player not in hallway after move"



