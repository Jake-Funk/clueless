from util.enums import PlayerEnum, WeaponEnum, RoomEnum, HallEnum
from util.game_state import GameState


def get_player_location(player: str, gs: GameState) -> RoomEnum | HallEnum:
    """
    Function to return the location of a given player

    Args:
        player {PlayerEnum}: The enum value of a given player
        gs {GameState}: The current state of the game

    Returns:
        location {RoomEnum | HallEnum}: The location of the player
        None: If the player does not exist, should NOT happen
    """
    for location in gs.map:
        if gs.player_character_mapping[player] in gs.map[location]:
            return location
    raise Exception("Player not found.", player.value)
