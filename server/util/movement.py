from util.enums import RoomEnum, HallEnum


# Example Player Message concept
message = {
    "id": 0,
    "loc": RoomEnum.hall,
    "next_loc": HallEnum.hall_to_lounge,
    "suggestion": ("Player", "Location", "Weapon"),
    "accusation": ("Player", "Location", "Weapon"),
}

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
