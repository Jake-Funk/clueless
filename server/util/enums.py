from enum import Enum, IntEnum
import random


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


class RoomEnum(str, Enum):
    study = "study"
    hall = "hall"
    lounge = "lounge"
    library = "library"
    billiard = "billiard"
    dining = "dining"
    conservatory = "conservatory"
    ballroom = "ballroom"
    kitchen = "kitchen"


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


class GameSolution:
    """
    The game solution class is just a structure for keeping tabs on a
    game's correct answer. If you want the solution to have specific values
    for test/debug purposes, then you can pass in a person, weapon, and/or
    room to the initializer. These arguments are optional, and If you don't
    pass them in, they will be set as a random value.
    """

    def __init__(
        self,
        person: PlayerEnum | None = None,
        weapon: WeaponEnum | None = None,
        room: RoomEnum | None = None,
    ) -> None:
        self.weapon = weapon if weapon else random.choice(list(WeaponEnum))
        self.person = person if person else random.choice(list(PlayerEnum))
        self.room = room if room else random.choice(list(RoomEnum))

    def print(self):
        print("Weapon:", self.weapon.value)
        print("Person:", self.person.value)
        print("Room:", self.room.value)
