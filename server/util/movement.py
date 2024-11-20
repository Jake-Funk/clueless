from util.game_state import GameState
from util.enums import PlayerEnum, RoomEnum, HallEnum, HttpEnum
from util.actions import MoveAction


Map = {
    RoomEnum.study: frozenset(
        [HallEnum.study_to_hall, HallEnum.study_to_lib, RoomEnum.kitchen]
    ),
    RoomEnum.hall: frozenset(
        [HallEnum.study_to_hall, HallEnum.hall_to_billiard, HallEnum.hall_to_lounge]
    ),
    RoomEnum.lounge: frozenset(
        [HallEnum.hall_to_lounge, HallEnum.lounge_to_dining, RoomEnum.conservatory]
    ),
    RoomEnum.library: frozenset(
        [HallEnum.study_to_lib, HallEnum.lib_to_billiard, HallEnum.lib_to_conservatory]
    ),
    RoomEnum.billiard: frozenset(
        [
            HallEnum.lib_to_billiard,
            HallEnum.hall_to_billiard,
            HallEnum.billiard_to_dining,
            HallEnum.billiard_to_ballroom,
        ]
    ),
    RoomEnum.dining: frozenset(
        [
            HallEnum.lounge_to_dining,
            HallEnum.billiard_to_dining,
            HallEnum.dining_to_kitchen,
        ]
    ),
    RoomEnum.conservatory: frozenset(
        [
            HallEnum.lib_to_conservatory,
            HallEnum.conservatory_to_ballroom,
            RoomEnum.lounge,
        ]
    ),
    RoomEnum.ballroom: frozenset(
        [
            HallEnum.conservatory_to_ballroom,
            HallEnum.billiard_to_ballroom,
            HallEnum.ballroom_to_kitchen,
        ]
    ),
    RoomEnum.kitchen: frozenset(
        [HallEnum.ballroom_to_kitchen, HallEnum.dining_to_kitchen, RoomEnum.study]
    ),
    HallEnum.study_to_hall: frozenset([RoomEnum.study, RoomEnum.hall]),
    HallEnum.hall_to_lounge: frozenset([RoomEnum.hall, RoomEnum.lounge]),
    HallEnum.study_to_lib: frozenset([RoomEnum.study, RoomEnum.library]),
    HallEnum.hall_to_billiard: frozenset([RoomEnum.hall, RoomEnum.billiard]),
    HallEnum.lounge_to_dining: frozenset([RoomEnum.lounge, RoomEnum.dining]),
    HallEnum.lib_to_billiard: frozenset([RoomEnum.library, RoomEnum.billiard]),
    HallEnum.billiard_to_dining: frozenset([RoomEnum.billiard, RoomEnum.dining]),
    HallEnum.lib_to_conservatory: frozenset([RoomEnum.library, RoomEnum.conservatory]),
    HallEnum.billiard_to_ballroom: frozenset([RoomEnum.billiard, RoomEnum.ballroom]),
    HallEnum.dining_to_kitchen: frozenset([RoomEnum.dining, RoomEnum.kitchen]),
    HallEnum.conservatory_to_ballroom: frozenset(
        [RoomEnum.conservatory, RoomEnum.ballroom]
    ),
    HallEnum.ballroom_to_kitchen: frozenset([RoomEnum.ballroom, RoomEnum.kitchen]),
    # Staging room holds characters not assigned to players
    RoomEnum.staging: frozenset(
        [
            HallEnum.hall_to_lounge,
            HallEnum.lounge_to_dining,
            HallEnum.ballroom_to_kitchen,
            HallEnum.conservatory_to_ballroom,
            HallEnum.lib_to_conservatory,
            HallEnum.study_to_lib,
        ]
    ),
}


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
