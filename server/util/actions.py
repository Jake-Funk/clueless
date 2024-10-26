from enum import Enum, IntEnum
from dataclasses import dataclass
from fastapi import Header
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
        person: PlayerEnum | None
        weapon: WeaponEnum | None
        room: HallEnum | RoomEnum | None

    gameKey: str
    player: str
    statementDetails: Details


@dataclass
class MoveAction:
    """
    Class to describe a move action from a player
    """

    player: str
    location: HallEnum | RoomEnum | None
    id: str | None = None
