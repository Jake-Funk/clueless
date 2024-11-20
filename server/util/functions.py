import datetime
from util.enums import PlayerEnum, RoomEnum, HallEnum
from util.game_state import GameState


def get_time() -> str:
    return str(datetime.datetime.now().time())


def location_str(location: RoomEnum | HallEnum) -> str:
    if type(location) is RoomEnum:
        return location.value
    else:
        return f"hallway{location.value}"


def get_character_location(
    character: PlayerEnum | None, gs: GameState
) -> RoomEnum | HallEnum:
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
        if character in gs.map[location]:
            return location
    raise Exception("Character not found.", character)
