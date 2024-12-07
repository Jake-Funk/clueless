from fastapi.testclient import TestClient
from util.enums import PlayerEnum, HallEnum
import pytest

from main import app, games

client = TestClient(app)


@pytest.mark.parametrize("bad_num", [1, 10])
def test_bad_validate_move(bad_num: int):
    """
    Test that creating a game with an invalid
    number of players leads to a 403 message
    """
    response = client.post("/new_game/", json={"num_players": bad_num})
    assert response.status_code == 403


@pytest.mark.parametrize("num", [2, 3, 4, 5, 6])
def test_good_validate_move(num: int):
    """
    Test that creating a game with a valid number of players will
    return a 200 message and create the key for a populated GameState
    object
    """
    response = client.post("/new_game/", json={"num_players": num})
    assert response.status_code == 200

    game_key = response.json()
    assert len(games[game_key].moveable_players) == num
    assert len(games[game_key].player_order) == num
    assert games[game_key].current_turn.phase == "move"
    assert games[game_key].map[HallEnum.hall_to_lounge] == [PlayerEnum.miss_scarlet]
    assert games[game_key].victory_state == 0
