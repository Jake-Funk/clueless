from enum import Enum
from util.enums import PlayerEnum, RoomEnum, HallEnum, WeaponEnum, EndGameEnum
from util.game_map import MAP
from typing import Dict
from dataclasses import dataclass
from datetime import datetime
import random

STARTING_LOCATIONS = {
    PlayerEnum.miss_scarlet: HallEnum.hall_to_lounge,
    PlayerEnum.col_mustard: HallEnum.lounge_to_dining,
    PlayerEnum.mrs_white: HallEnum.ballroom_to_kitchen,
    PlayerEnum.mr_green: HallEnum.conservatory_to_ballroom,
    PlayerEnum.mrs_peacock: HallEnum.lib_to_conservatory,
    PlayerEnum.prof_plum: HallEnum.study_to_lib,
}


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
        msg = f"It is {self.player}'s turn to {self.phase.value}."
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

        self.moveable_players = []  # For tracking what players can still play
        self.player_order = []  # For tracking player order
        self.player_username_mapping = {}

        # Mapping player ids to game characters
        self.player_character_mapping: Dict[str, PlayerEnum] = (
            player_character_mapping if player_character_mapping else {}
        )
        allCharacters = list(PlayerEnum)
        for i in range(num_players):
            # First player is always Miss Scarlet
            if i == 0:
                # Miss Scarlet will be the first in the list
                randCharacter = allCharacters[0]
            else:
                randCharacter = random.choice(allCharacters)

            player_id = "player" + str(i + 1)
            self.player_character_mapping[player_id] = randCharacter
            allCharacters.remove(randCharacter)

            self.moveable_players.append(player_id)
            self.player_order.append(player_id)
            self.player_username_mapping[player_id] = ""

        self.map: Dict[RoomEnum | HallEnum, list[PlayerEnum]] = {}
        for item in list(RoomEnum) + list(HallEnum):
            self.map[item] = []

        # Starting Player locations
        self.set_player_positions()

        # A Map to store if a Player was moved forcibly by a suggestion
        self.moved_by_suggest: Dict[PlayerEnum, bool] = {}
        for character in list(PlayerEnum):
            self.moved_by_suggest[character] = False

        # sets for validating responses for the suggestion endpoint
        # uses the same keys (e.g., "player1") for cards each player has seen
        self.playerHasSeen: Dict[str, set] = {}
        for K in self.player_character_mapping.keys():
            self.playerHasSeen[K] = set()

        self.victory_state = EndGameEnum.keep_playing

        self.logs: list[GameEvent] = []

        self.chat: list[str] = []

    def set_player_positions(self) -> None:
        """
        Utility function to set starting character positions
        """
        characters_chosen = []
        for player in self.player_order:
            character = self.player_character_mapping[player]
            self.map[STARTING_LOCATIONS[character]] = [character]
            characters_chosen.append(character)

        if len(characters_chosen) != 6:
            for character in list(PlayerEnum):
                if character not in characters_chosen:
                    self.map[RoomEnum.staging].append(character)

    def set_player_moved_by_suggest(self, player: PlayerEnum) -> None:
        """
        A utility function to mark a player as being moved by a suggestion
        """
        self.moved_by_suggest[player] = True

    def reset_player_moved_by_suggest(self, player: PlayerEnum) -> None:
        """
        A utility function to reset a player having been moved by a suggestion
        """
        self.moved_by_suggest[player] = False

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
        if not self.moveable_players:
            return
        elif len(self.moveable_players) == 1:
            return

        while True:
            self.current_turn.player += 1
            if self.current_turn.player >= len(self.player_order):
                self.current_turn.player = 0
            if self.player_order[self.current_turn.player] not in self.moveable_players:
                continue
            else:
                break

    def next_phase(self, desired_phase: str):
        """
        Moves the game phase to the next VALID phase of the game.
        This function will skip the move phase if it is impossible at the current time.
        (when the moving player is in a room where all adjacent hallways are full)

        this function also assumes that the next_player function was called prior to this one
        being called with "move" as its argument.
        """

        if desired_phase != "move":
            self.current_turn.phase = desired_phase
        else:
            current_location = None
            for location in self.map:
                if (
                    self.player_character_mapping[
                        self.player_order[self.current_turn.player]
                    ]
                    in self.map[location]
                ):
                    current_location = location

            if not current_location:
                print(
                    "Wat!? We couldn't find the player in the map. The server will probably implode now."
                )

            hall_count = 0
            player_count = 0
            for location in MAP[current_location]:
                if type(location) is HallEnum:
                    hall_count += 1
                if self.map[location]:
                    player_count += 1

            # If the adjacent locations are not all Hallways there is a valid move
            # A secret Passageway counts as an adjacent room not hallway
            if hall_count != len(MAP[current_location]):
                self.current_turn.phase = "move"
            # Otherwise check if all adjacent hallways are occupied
            else:
                if player_count != len(MAP[current_location]):
                    self.current_turn.phase = "move"
                else:
                    self.current_turn.phase = "accuse"
                    self.logs.append(
                        f"{self.current_turn.player} cannot make a valid move, skipping to accusation phase."
                    )

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
        outputDict["moved_by_suggest"] = self.moved_by_suggest
        outputDict["player_username_mapping"] = self.player_username_mapping

        outputDict["victory_state"] = self.victory_state

        # player cards
        for i, card_list in enumerate(self.player_cards):
            currentPlayer = "player" + str(i + 1)
            outputDict[currentPlayer] = card_list

        outputDict["map"] = self.map

        # return phase of game in dictionary
        outputDict["game_phase"] = {
            "phase": self.current_turn.phase,
            "player": self.player_order[self.current_turn.player],
        }

        # return the dictionary of cards the players have been shown
        outputDict["playerHasSeen"] = self.playerHasSeen

        outputDict["logs"] = reversed(self.logs)
        outputDict["chat"] = reversed(self.chat)
        outputDict["moved_by_suggest"] = self.moved_by_suggest

        return outputDict
