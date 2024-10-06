from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from util.game_state import GameState, GameEvent
from util.enums import MoveAction, HallEnum, RoomEnum, HttpEnum
from util.functions import get_player_location
from util.movement import Map, move_player, validate_move
from pydantic import BaseModel
import random

import uuid

app = FastAPI()

origins = [
    "http://localhost:3000",  # this origin should be removed from PROD but for our purposes its no big deal
    "https://clueless-eight.vercel.app",
]

games = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewGameRequest(BaseModel):
    num_players: int


class Statement(BaseModel):
    """
    Class that will act as an input format for suggestions and accusations
    TODO: conform this to the Enums defined in enums.py (would require pydantic for those classes)
    """

    person: str
    weapon: str
    room: str


@app.post("/new_game")
async def initialize_game(req: NewGameRequest) -> str:
    try:
        temp = GameState(req.num_players)
    except:
        raise HTTPException(status_code=403, detail="Invalid number of players.")

    key = str(uuid.uuid4())
    games[key] = temp
    return key


@app.post("/move")
async def move(movement: MoveAction):
    # Check if player can be found on current map
    if movement.id == None or movement.id not in games.keys():
        raise HTTPException(status_code=404, detail="Game not found.")
    key = movement.id

    try:
        current_location = get_player_location(movement.player, games[key])
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found on Map.")

    http_code = validate_move(movement, current_location, games[key])

    if http_code[0] == HttpEnum.good:
        move_player(movement, current_location, games[key])
        # Check if player entered a room
        if isinstance(movement.location, RoomEnum):
            games[key].current_turn.phase = "suggest"
        # TODO: If not a room, need to keep turn as move but change
        # game player to be the next one. Would like utility function for this
        return {
            "Response": f"Successfully moved {movement.player.value} to {movement.location.value}"
        }
    else:
        raise HTTPException(status_code=http_code[0].value, detail=http_code[1])


@app.post("/State")
async def gameState(gameKey: str) -> dict:
    """
    Function to get the game state. For now this is assuming that the game state endpoint will work for everybody
    """
    # Check if the requester has the required access to get the game state
    # TODO

    # check to see if there are active games to query
    if not games:
        raise HTTPException(status_code=503, detail="No games available")

    # get the current game state from the requested game key
    if gameKey not in games.keys():
        # if there are keys and if the requested key doesn't match, throw an exception
        raise HTTPException(status_code=404, detail="unknown game key")
    else:
        # if there are no games throw an exception
        currentGame = games[gameKey]

    # convert the GameState into a dict of strings and return it
    return currentGame.dump_to_dict()


@app.post("/suggestion",status_code=200)
async def makeSuggestion(gameKey: str, suggestor: str, suggestion: Statement) -> str:
    """
    Function that accepts suggestions from a player, verifies they can be made,
    and returns the first card from the players following the player who suggested
    which disproves the suggestion

    Args:
        gameKey: string representing the game key for the game which the suggestion is made
        suggestor: the player making the suggestion
        suggestion: the suggestion they are making (player, weapon, and room)
    """
    # get the game state information
    if gameKey not in games.keys():
        # if there are keys and if the requested key doesn't match, throw an exception
        raise HTTPException(status_code=404, detail="unknown game key")
    else:
        currentGame = games[gameKey]

    # dump to dictionary format
    currentGameDict = currentGame.dump_to_dict()

    # first ensure the suggestor is in the same room as the suggestion they are making
    # Satisfies game requirement
    try:
        # get the character represented by the current player
        playersCharacter = currentGameDict["player_character_mapping"][suggestor]
    except:
        raise HTTPException(status_code=204, detail="Suggestor is unknown to the game")

    # search in the map for the location of that player
    for loc in currentGameDict["map"].keys():
        if playersCharacter in currentGameDict["map"][loc]:
            characterLocation = loc

    # get the location of the current player
    if characterLocation != suggestion.room:
        # TODO: This exception is necessary once the players can actually make suggestions - to test it will be commented out
        print("Exception will be raised here, but is commented out for now")

        # raise HTTPException(status_code=403, detail="Suggestor is unable to make this suggestion -- suggestor is not in the room where the suggestion is being made")

    # will need a way to relate the suggestor to the players in the game (i.e., their place in the order of the game)
    # this allows us to pick the next player to look at for cards
    playersList = list(currentGameDict["player_character_mapping"].keys())
    loopIdx = playersList.index(suggestor)

    # create a list of players that can be used to find the next player whose cards should be checked
    top = playersList[:loopIdx]
    bottom = playersList[loopIdx:]
    playersList = bottom[1:] + top

    # loop through the players in order and check their cards against the suggestion
    for p in playersList:
        # TODO: Future iterations should send a request out to the identified player to show a card if one of the suggestions is in their hand
        playerCards = currentGameDict[p]

        # select the cards that
        overlapCards = [
            c
            for c in playerCards
            if c in suggestion.person or c in suggestion.weapon or c in suggestion.room
        ]

        if overlapCards:
            # if there are any overlapping cards, return one of them randomly
            return f"{p} shows {random.choice(overlapCards)}"

    # if you get out of the loop that means there are no cards to show
    # this should happen when the exact solution is found or when every card in 
    # the suggesstion is in the players hand
    raise HTTPException(status_code=404, detail="None of the other players have these suggested cards - Are they in your hand?")