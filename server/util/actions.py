from enum import Enum, IntEnum
from dataclasses import dataclass
from pydantic import BaseModel
import random

from util.enums import HallEnum, RoomEnum, PlayerEnum, WeaponEnum, HttpEnum


class NewGameRequest(BaseModel):
    num_players: int


class Statement(BaseModel):
    """
    Class that will act as an input format for suggestions and accusations
    TODO: conform this to the Enums defined in enums.py (would require pydantic for those classes)
    """

    class Details(BaseModel):
        person: PlayerEnum | None = None
        weapon: WeaponEnum | None = None
        room: RoomEnum | None = None

    gameKey: str | None
    player: str | None
    statementDetails: Details | None


@dataclass
class MoveAction:
    """
    Class to describe a move action from a player
    """

    player: str
    location: HallEnum | RoomEnum
    id: str | None = None
