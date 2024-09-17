from enum import Enum, IntEnum
from dataclasses import dataclass
from pydantic import BaseModel
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


class HttpEnum(IntEnum):
    bad_request = 400
    unauthorized = 401
    forbidden = 403
    not_found = 404
    timeout = 408
    good = 200
    created = 201
    accepted = 202
    no_content = 204
    internal_error = 500


@dataclass
class MoveAction:
    """
    Class to describe a move action from a player
    """

    player: PlayerEnum
    location: HallEnum | RoomEnum
    id: str | None = None
