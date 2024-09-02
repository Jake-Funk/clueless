from enum import Enum, IntEnum


class PlayerEnum(str, Enum):
    miss_scarlet = "Miss Scarlet"
    prof_plum = "Professor Plum"
    mr_green = "Mr. Green"
    mrs_white = "Mrs. White"
    mrs_peacock = "Mrs. Peacock"
    col_mustard = "Colonel Mustard"


class WeaponEnum(str, Enum):
    rope = "rope"
    lead_pipe = "lead pipe"
    knife = "knife"
    wrench = "wrench"
    candlestick = "candlestick"
    revolver = "revolver"


class RoomEnum(IntEnum):
    study = 0
    hall = 1
    lounge = 2
    library = 3
    billiard = 4
    dining = 5
    conservatory = 6
    ballroom = 7
    kitchen = 8


class HallEnum(IntEnum):
    study_to_hall = 0
    hall_to_lounge = 1
    study_to_lib = 2
    hall_to_billiard = 3
    lounge_to_dining = 4
    lib_to_billiard = 5
    billiard_to_dining = 6
    lib_to_conservatory = 7
    billiard_to_ballroom = 8
    dining_to_kitchen = 9
    conservatory_to_ballroom = 10
    ballroom_to_kitchen = 11
