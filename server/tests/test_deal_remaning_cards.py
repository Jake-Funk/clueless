from util.game_state import deal_remaining_cards
from util.enums import GameSolution
import pytest


@pytest.mark.parametrize("num_players", [-1, 0, 1, 7])
def test_num_players(num_players: int):
    sol = GameSolution()

    # if given invalid input the function should raise a ValueError
    with pytest.raises(ValueError):
        deal_remaining_cards(sol, num_players)


@pytest.mark.parametrize("num_players", range(2, 7))
def test_hands_dealt(num_players: int):
    sol = GameSolution()

    hands = deal_remaining_cards(sol, num_players)

    # check that the function generated the right number of hands
    assert len(hands) == num_players

    # check that the solution values are not in anyone's hand
    for hand in hands:
        for card in hand:
            assert (
                (card != sol.person.value)
                and (card != sol.weapon.value)
                and (card != sol.room.value)
            )
