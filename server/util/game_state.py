from util.enums import PlayerEnum, RoomEnum, HallEnum, WeaponEnum
from typing import Dict
from dataclasses import dataclass
from util.functions import deal_remaining_cards
from datetime import datetime
from pydantic import BaseModel
import random


@dataclass
class GameEvent(BaseModel):
    """
    This class is for logging the game as it progresses
    the level of each game event represents who has access to view
    the log as follows:
        0: only the server gets to see this log
        1-6: only the server and player with the same number can view
        7: anyone can view
    """

    level: int = 0
    message: str = ""
    time: datetime = datetime.now()


class GameSolution(BaseModel):
    """
    The game solution class is just a structure for keeping tabs on a
    game's correct answer. If you want the solution to have specific values
    for test/debug purposes, then you can pass in a person, weapon, and/or
    room to the initializer. These arguments are optional, and If you don't
    pass them in, they will be set as a random value.
    """

    person: PlayerEnum | None
    weapon: WeaponEnum | None
    room: RoomEnum | None

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


class GameState(BaseModel):
    """
    This is the core stucture to represent the state of a game of clueless
    the class keeps track of the solution to the game, where everyone is on
    the board, who has what cards, and a log of the game progress.

    The number of players for a game is required when you initialize the
    game state object. Optionally you can pass in a GameSolution object
    if you want to have a specific solution for debug/testing purposes.
    If you leave out the solution argument then a random solution will
    be generated for this game.
    """

    # defining attributes at the class level for pydantic base model compatibility
    solution: GameSolution
    map: Dict[RoomEnum | HallEnum, list[PlayerEnum]]
    log: list[GameEvent]
    player_cards: list[list[str]]
    player_clues: list[list[str]]
    num_players: int

    def __init__(self, num_players: int, solution: GameSolution | None = None):
        if solution:
            self.solution = solution
        else:
            self.solution = GameSolution()

        self.player_cards = deal_remaining_cards(
            personSolution=self.solution.person,
            weaponSolution=self.solution.weapon,
            roomSolution=self.solution.room,
            num_players=num_players,
        )
        self.player_clues = [[] for _ in range(num_players)]

        self.map = {}
        for item in list(RoomEnum) + list(HallEnum):
            self.map[item] = []

        self.map[HallEnum.hall_to_lounge] = [PlayerEnum.miss_scarlet]
        self.map[HallEnum.lounge_to_dining] = [PlayerEnum.col_mustard]
        self.map[HallEnum.ballroom_to_kitchen] = [PlayerEnum.mrs_white]
        self.map[HallEnum.conservatory_to_ballroom] = [PlayerEnum.mr_green]
        self.map[HallEnum.lib_to_conservatory] = [PlayerEnum.mrs_peacock]
        self.map[HallEnum.study_to_lib] = [PlayerEnum.prof_plum]

        self.log = []
