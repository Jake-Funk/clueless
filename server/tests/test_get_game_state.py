import pytest
from util.game_state import GameState


@pytest.mark.parametrize("num_players", range(2, 7))
def test_num_players(num_players: int):
    dummy_game = GameState(num_players)

    # make sure that the dump_to_dict function works in the valid range
    dummyDict = dummy_game.dump_to_dict()

    # check that the correct number of players got created
    playerList = ["player" + str(x) for x in range(1, num_players)]
    assert [player in dummyDict.keys() for player in playerList]

    # check that the solution and map exist as fields in the dictionary
    assert "map" in dummyDict.keys()
    assert "solution" in dummyDict.keys()
