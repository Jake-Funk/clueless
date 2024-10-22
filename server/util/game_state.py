from enum import Enum
from util.enums import PlayerEnum, RoomEnum, HallEnum, WeaponEnum, EndGameEnum
from typing import Dict
from dataclasses import dataclass
from datetime import datetime
import random


class TurnPhase(str, Enum):
    move = "move"
    suggest = "suggest"
    accuse = "accuse"


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


@dataclass
class GameTurn:
    """
    This class holds the information for whose turn it is and
    what phase of their turn it is (move, suggest, accuse)
    the defaults are set to be how the game starts
    """

    player: int = 0  # Index into the PLAYERS list, 0 is miss scarlet
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

    def __init__(
        self,
        num_players: int,
        solution: GameSolution | None = None,
        player_character_mapping: Dict[str, PlayerEnum] | None = None,
    ):
        self.solution: GameSolution = solution if solution else GameSolution()

        self.player_cards: list[list[str]] = self.deal_remaining_cards(num_players)
        self.player_clues: list[list[str]] = [[] for _ in range(num_players)]
        self.current_turn: GameTurn = GameTurn()

        # TODO: This will need an update to proper player IDs
        self.moveable_players = []  # For tracking what players can still play
        self.player_order = []  # For tracking player order

        # Mapping player ids to game characters
        self.player_character_mapping: Dict[str, PlayerEnum] = (
            player_character_mapping if player_character_mapping else {}
        )
        allCharacters = list(PlayerEnum)
        for i in range(num_players):
            randCharacter = random.choice(allCharacters)
            player_id = "player" + str(i + 1)
            self.player_character_mapping[player_id] = randCharacter
            allCharacters.remove(randCharacter)

            self.moveable_players.append(player_id)
            self.player_order.append(player_id)

        self.map: Dict[RoomEnum | HallEnum, list[PlayerEnum]] = {}
        for item in list(RoomEnum) + list(HallEnum):
            self.map[item] = []

        # Starting Player locations
        self.map[HallEnum.hall_to_lounge] = [PlayerEnum.miss_scarlet]
        self.map[HallEnum.lounge_to_dining] = [PlayerEnum.col_mustard]
        self.map[HallEnum.ballroom_to_kitchen] = [PlayerEnum.mrs_white]
        self.map[HallEnum.conservatory_to_ballroom] = [PlayerEnum.mr_green]
        self.map[HallEnum.lib_to_conservatory] = [PlayerEnum.mrs_peacock]
        self.map[HallEnum.study_to_lib] = [PlayerEnum.prof_plum]

        self.victory_state = EndGameEnum.keep_playing

        self.log: list[GameEvent] = []

    def deal_remaining_cards(self, num_players: int) -> list[list[str]]:
        """
        This function will take in a game solution and split all
        remaining cards into a list of n lists according to the number of players, each list
        represents the cards a player is dealt at the beginning of the game

        solution -- the correct solution (person, weapon, place) to a specific game of clue
        num_players -- how many players, ie how many lists do the remaining cards need to be
        split into
        """
        if num_players < 2 or 6 < num_players:
            raise ValueError("The number of player must be in the range 2-6")

        # creating the lists of remaining items
        remaining_people = list(PlayerEnum)
        remaining_people.remove(self.solution.person)

        remaining_weapons = list(WeaponEnum)
        remaining_weapons.remove(self.solution.weapon)

        remaining_rooms = list(RoomEnum)
        remaining_rooms.remove(self.solution.room)

        # deal all remaining items to players in order
        player_hands = [[] for _ in range(num_players)]

        # use a global counter for all of these loops to keep the
        # total number of cards per person consistent
        i = 0
        for person in remaining_people:
            player_hands[i % num_players].append(person.value)
            i += 1

        for weapon in remaining_weapons:
            player_hands[i % num_players].append(weapon.value)
            i += 1

        for room in remaining_rooms:
            player_hands[i % num_players].append(room.value)
            i += 1

        return player_hands

    def next_player(self) -> None:
        """
        Atomic function to change the current turn's player to the next one
        """
        self.current_turn.player += 1

        if self.current_turn.player >= len(self.player_order):
            self.current_turn.player = 0

    def get_current_player(self) -> PlayerEnum:
        """
        Utility function to get the current player of the game
        """
        return self.player_order[self.current_turn.player]

    def dump_to_dict(self) -> dict:
        """
        Member function that pushes all attributes to a dict for return
        """
        outputDict = {}

        # Solution information
        outputDict["solution"] = {}
        outputDict["solution"]["killer"] = self.solution.person
        outputDict["solution"]["weapon"] = self.solution.weapon
        outputDict["solution"]["room"] = self.solution.room

        outputDict["player_character_mapping"] = self.player_character_mapping

        # player cards
        for i, card_list in enumerate(self.player_cards):
            currentPlayer = "player" + str(i + 1)
            outputDict[currentPlayer] = card_list

        outputDict["map"] = self.map

        return outputDict
