from fastapi.testclient import TestClient
from util.game_state import GameState
from util.enums import PlayerEnum, WeaponEnum, RoomEnum

from main import app

client = TestClient(app)


def get_new_default_game_key(num: int) -> str:
    """
    Utility function to return the key of a newly created game
    state through the endpoint
    """
    new_game = client.post("/new_game/", json={"num_players": num})
    key = new_game.json()
    return key


def check_no_suggestion_return(
    player: str,
    character: PlayerEnum,
    weapon: WeaponEnum,
    room: RoomEnum,
    game_state: GameState,
) -> bool:
    """
    Utility function to check if all elements in a suggestion are
    either in the suggestor's hand or in the game solution
    """
    count = 0
    if (
        character in game_state.player_cards[player]
        or character == game_state.solution.person
    ):
        count += 1
    if (
        weapon in game_state.player_cards[player]
        or weapon == game_state.solution.weapon
    ):
        count += 1
    if room in game_state.player_cards[player] or room == game_state.solution.room:
        count += 1

    # If all cards are either in the solution or player's hand; return true
    if count == 3:
        return True
    return False
