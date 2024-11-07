from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_new_default_game_key(num: int):
    """ """
    new_game = client.post("/new_game/", json={"num_players": num})
    key = new_game.json()
    return key
