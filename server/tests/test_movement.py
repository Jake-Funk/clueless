from util.functions import get_player_location
from util.game_state import GameState
from util.enums import PlayerEnum, HallEnum
import pytest

default_gs = GameState(6)


@pytest.mark.parametrize("player", list(PlayerEnum))
def test_get_player_default_locations(player: int):
    """ """
    location = get_player_location(player, default_gs)
    assert location is not None, "Location invalid"

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
