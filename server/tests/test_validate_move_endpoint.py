from fastapi.testclient import TestClient
from util.game_state import GameState
from util.enums import PlayerEnum, HallEnum, RoomEnum, HttpEnum
import pytest

from main import app, games

client = TestClient(app)


def get_new_default_game_key(num: int):
    new_game = client.post("/new_game/", json={"num_players": num})
    key = new_game.json()
    return key


def test_bad_validate_move_key():
    response = client.post("/valid-move/", params={"gameKey": "", "player": "player1"})
    assert response.status_code == 404


def test_bad_validate_move_player():
    key = get_new_default_game_key(2)
    response = client.post("/valid-move/", params={"gameKey": key, "player": "player0"})
    assert response.status_code == 404


def test_good_no_moveable_players():
    player_name = "player1"
    key = get_new_default_game_key(3)
    games[key].moveable_players.remove(player_name)
    response = client.post(
        "/valid-move/", params={"gameKey": key, "player": player_name}
    )
    assert response.status_code == 200
    # Check the player has been incremented from 0
    assert games[key].current_turn.player == 1
    assert games[key].current_turn.phase == "move"


def test_good_regular_move():
    player_name = "player1"
    key = get_new_default_game_key(3)
    response = client.post(
        "/valid-move/", params={"gameKey": key, "player": player_name}
    )
    assert response.status_code == 200
    # Check the player has not changed
    assert games[key].current_turn.player == 0
    assert games[key].current_turn.phase == "move"


def test_good_no_possible_move():
    player_name = "player1"
    key = get_new_default_game_key(3)
    games[key].map = {}
    games[key].map[RoomEnum.hall] = [PlayerEnum.miss_scarlet]
    games[key].map[HallEnum.study_to_hall] = [PlayerEnum.col_mustard]
    games[key].map[HallEnum.hall_to_billiard] = [PlayerEnum.mrs_white]
    games[key].map[HallEnum.hall_to_lounge] = [PlayerEnum.mr_green]
    response = client.post(
        "/valid-move/", params={"gameKey": key, "player": player_name}
    )
    assert response.status_code == 200
    # Check the player has not changed
    assert games[key].current_turn.player == 0
    # Check that the phase of the game has changed
    assert games[key].current_turn.phase == "accuse"
