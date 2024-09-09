from util.enums import PlayerEnum, RoomEnum, HallEnum, GameSolution
from typing import Dict
from dataclasses import dataclass
from util.functions import deal_remaining_cards
from datetime import datetime


@dataclass
class GameEvent:
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


class GameState:
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

    def __init__(self, num_players: int, solution: GameSolution | None = None):
        if solution:
            self.solution = solution
        else:
            self.solution = GameSolution()

        self.player_cards: list[list[str]] = deal_remaining_cards(
            self.solution, num_players
        )
        self.player_clues: list[list[str]] = [[] for _ in range(num_players)]

        self.map: Dict[RoomEnum | HallEnum, list[PlayerEnum]] = {}
        for item in list(RoomEnum) + list(HallEnum):
            self.map[item] = []

        self.map[HallEnum.hall_to_lounge] = [PlayerEnum.miss_scarlet]
        self.map[HallEnum.lounge_to_dining] = [PlayerEnum.col_mustard]
        self.map[HallEnum.ballroom_to_kitchen] = [PlayerEnum.mrs_white]
        self.map[HallEnum.conservatory_to_ballroom] = [PlayerEnum.mr_green]
        self.map[HallEnum.lib_to_conservatory] = [PlayerEnum.mrs_peacock]
        self.map[HallEnum.study_to_lib] = [PlayerEnum.prof_plum]

        self.log: list[GameEvent] = []
