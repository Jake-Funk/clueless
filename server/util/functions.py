from util.enums import GameSolution, PlayerEnum, WeaponEnum, RoomEnum, HallEnum
from util.game_state import GameState


def deal_remaining_cards(solution: GameSolution, num_players: int) -> list[list[str]]:
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
    remaining_people.remove(solution.person)

    remaining_weapons = list(WeaponEnum)
    remaining_weapons.remove(solution.weapon)

    remaining_rooms = list(RoomEnum)
    remaining_rooms.remove(solution.room)

    # deal all reamaing items to players in order
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


def get_player_location(player: PlayerEnum, gs: GameState) -> RoomEnum | HallEnum:
    """
    Function to return the location of a given player

    Args:
        player {PlayerEnum}: The enum value of a given player
        gs {GameState}: The current state of the game

    Returns:
        location {RoomEnum | HallEnum}: The location of the player
        None: If the player does not exist, should NOT happen
    """
    for location in gs.map:
        if player in gs.map[location]:
            return location
    return None
