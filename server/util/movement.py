from util.enums import PlayerEnum, RoomEnum, HallEnum, MoveAction, HttpEnum

# from util.game_state import GameState


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
}


def move_player(
    movement: MoveAction, current_location: RoomEnum | HallEnum, gs
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
    gs.map[current_location].remove(movement.player)
    gs.map[movement.location].append(movement.player)


def validate_move(
    movement: MoveAction, current_location: RoomEnum | HallEnum, gs
) -> HttpEnum:
    """
    Function to validate the desired move of a Player
    using the modified clue rule set

    Args:
        movement {MoveAction}: The Move desired by the player
        current_location {RoomEnum | HallEnum}: Current location of player
        gs {GameState}: Current game state

    Returns:
        A HttpEnum value indicating validity of desired movement
    """
    # Check if the turn is for movement
    if gs.current_turn.phase != "move":
        return HttpEnum.bad_request

    # Check if desired location is adjacent to the current location
    if movement.location not in Map[current_location]:
        return HttpEnum.bad_request

    # Check if desired location is a Hallway and if that hallway is occupied
    if isinstance(movement.location, HallEnum) and len(gs.map[movement.location]) >= 1:
        return HttpEnum.bad_request

    # Great Success!
    return HttpEnum.good
