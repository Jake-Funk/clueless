from util.game_state import GameState, GameSolution
from util.enums import PlayerEnum
import pytest


def test_next_player():
    """
    Test that the next_player class function works as intended
    """
    gs = GameState(6)

    assert gs.current_turn.player == PlayerEnum.miss_scarlet

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.prof_plum

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.mr_green

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.mrs_white

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.mrs_peacock

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.col_mustard

    gs.next_player()
    assert gs.current_turn.player == PlayerEnum.miss_scarlet
