from util.game_state import GameState, Map
from util.enums import PlayerEnum, RoomEnum, HallEnum, HttpEnum
from util.actions import MoveAction


def move_player(
    character: PlayerEnum | None,
    target_location: RoomEnum | HallEnum | None,
    current_location: RoomEnum | HallEnum | None,
    gs: GameState,
) -> None:
    """
    Function to move a player in the map within the game state.
    Removes player from current location and adds them to the new location.
    Atomized function, no safe guards employed

    Args:
        movement {MoveAction}: The Move desired by the player
        current_location {RoomEnum | HallEnum}: Current location of player
        gs {GameState}: Current game state

    Returns:
        None
    """
    gs.map[current_location].remove(character)
    gs.map[target_location].append(character)


def validate_move(
    movement: MoveAction, current_location: RoomEnum | HallEnum, gs: GameState
) -> tuple:
    """
    Function to validate the desired move of a Player
    using the modified clue rule set

    Args:
        movement {MoveAction}: The Move desired by the player
        current_location {RoomEnum | HallEnum}: Current location of player
        gs {GameState}: Current game state

    Returns:
        A tuple of a HttpEnum value indicating validity of desired movement,
        and a string error message
    """
    # Check if the turn is for movement
    if gs.current_turn.phase != "move":
        return (HttpEnum.bad_request, "Wrong phase of the game to perform a move.")

    # Check if desired location is adjacent to the current location
    if movement.location not in Map[current_location]:
        return (HttpEnum.bad_request, "Invalid location to move to.")

    # Check if desired location is a Hallway and if that hallway is occupied
    if isinstance(movement.location, HallEnum) and len(gs.map[movement.location]) >= 1:
        return (HttpEnum.bad_request, "Cannot move to an occupied hallway.")

    # Great Success!
    return (HttpEnum.good, "")


def does_possible_move_exist(
    current_location: RoomEnum | HallEnum, gs: GameState
) -> bool:
    """
    Function to check if there is a valid move possible at the current location
    and given game state

    Returns:
        True if a possible move exists, False otherwise
    """
    hall_count = 0
    player_count = 0
    for location in Map[current_location]:
        if type(location) is HallEnum:
            hall_count += 1
        if gs.map[location]:
            player_count += 1

    # If the adjacent locations are not all Hallways return True
    # A secret Passageway counts as an adjacent room not hallway
    if hall_count != len(Map[current_location]):
        return True
    # Otherwise check if all adjacent hallways are occupied
    else:
        if player_count != len(Map[current_location]):
            return True
        else:
            return False
