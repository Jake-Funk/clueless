from enum import Enum
from util.enums import PlayerEnum, RoomEnum, HallEnum, GameSolution
from typing import Dict
from dataclasses import dataclass
from util.functions import deal_remaining_cards
from datetime import datetime


class TurnPhase(str, Enum):
    move = "move"
    suggest = "suggest"
    accuse = "accuse"


@dataclass
class GameTurn:
    """
    This class holds the information for whose turn it is and
    what phase of their turn it is (move, suggest, accuse)
    the defaults are set to be how the game starts
    """

    player: PlayerEnum = PlayerEnum.miss_scarlet
    phase: TurnPhase = TurnPhase.move

    def print(self, std_out: bool = True) -> str:
        msg = f"It is {self.player.value}'s turn to {self.phase.value}."
        if std_out:
            print(msg)
        return msg


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
    This is the core structure to represent the state of a game of clueless
    the class keeps track of the solution to the game, where everyone is on
    the board, who has what cards, and a log of the game progress.

    The number of players for a game is required when you initialize the
    game state object. Optionally you can pass in a GameSolution object
    if you want to have a specific solution for debug/testing purposes.
    If you leave out the solution argument then a random solution will
    be generated for this game.
    """

    def __init__(self, num_players: int, solution: GameSolution | None = None):
        self.solution: GameSolution = solution if solution else GameSolution()

        self.player_cards: list[list[str]] = deal_remaining_cards(
            self.solution, num_players
        )
        self.player_clues: list[list[str]] = [[] for _ in range(num_players)]
        self.current_turn: GameTurn = GameTurn()

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
