from util.game_state import GameState, GameSolution
from util.enums import PlayerEnum
import pytest


def test_next_player():
    """
    Test that the next_player class function works as intended
    """
    gs = GameState(6)

    assert gs.get_current_player() == gs.player_order[0]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[1]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[2]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[3]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[4]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[5]

    gs.next_player()
    assert gs.get_current_player() == gs.player_order[0]
