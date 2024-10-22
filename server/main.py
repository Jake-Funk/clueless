from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from util.game_state import GameState, GameEvent
from util.enums import HallEnum, RoomEnum, PlayerEnum, WeaponEnum, HttpEnum, EndGameEnum
from util.actions import NewGameRequest, MoveAction, Statement
from util.functions import get_player_location
from util.movement import Map, move_player, validate_move, does_possible_move_exist
from pydantic import BaseModel
import random

import uuid

# TODO: Potentially use this for our logging system?
import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

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
    """
    Endpoint to validate and execute a move action desired by the player. The
    endpoint takes in a MoveAction as input, which contains the player making
    the action, the game id and the desired location to move to.
    """
    # Check if game exists
    if movement.id == None or movement.id not in games.keys():
        raise HTTPException(status_code=404, detail="Game not found.")
    key = movement.id

    # Check if player can be found in the current map
    try:
        current_location = get_player_location(movement.player, games[key])
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found on Map.")

    # Check if there exists a possible move
    if not does_possible_move_exist(current_location, games[key]):
        games[key].next_player()
        logger.info("No possible move available. Transitioning to next player.")
        return {"Response": f"No valid move available. Moving to next Player."}

    # Check if the player can make an action
    if movement.player not in games[key].moveable_players:
        logger.info(f"{movement.player} cannot take actions; moving to next player.")
        games[key].next_player()

    http_code = validate_move(movement, current_location, games[key])

    if http_code[0] == HttpEnum.good:
        move_player(movement, current_location, games[key])
        # Check if player entered a room
        # If they have, move the game phase to suggestion
        # Otherwise keep the same phase but change players
        if isinstance(movement.location, RoomEnum):
            games[key].current_turn.phase = "suggest"
            logging.info(f"Moving {movement.player.value} to {movement.location.value}")
            logging.info(f"{movement.player.value} can now make a suggestion")
        else:
            games[key].next_player()
            logging.info(
                f"{movement.player.value} moved to a Hallway, going to next player"
            )

        return {
            "Response": f"Successfully moved {movement.player.value} to {movement.location.value}. Moving to next Player."
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


@app.post("/accusation", status_code=200)
async def makeAccusation(accusation: Statement):
    """
    Endpoint to validate and execute an Accuse action from the player. The function
    takes in a Statement object. If all details are None, the accusation phase is
    skipped.
    """
    # Check if game exists
    if accusation.id == None or accusation.id not in games.keys():
        raise HTTPException(status_code=404, detail="Game not found.")
    game = games[accusation.id]

    # If the accusation Statement is all None, no accusation is desired
    # and move to the next player. Not logging as it will be the average action
    accval = accusation.statementDetails
    if not (accval.person or accval.weapon or accval.room):
        # Move game to the next player and the move phase
        game.next_player()
        game.current_turn.phase = "move"
    else:
        # If the accusation is correct, end the game
        if (
            accval.person == game.solution.person
            and accval.weapon == game.solution.weapon
            and accval.room == game.solution.room
        ):
            logger.info(
                f"{accusation.suggestor} correctly put together the Clues and won the game!"
            )
            logger.info(f"*****Game Over*****")
            game.victory_state = EndGameEnum.winner_found
        # Otherwise, the player can continue playing only as an observor to disprove
        # suggestions; i.e. they cannot move, make suggestions or accusations.
        # Their only purpose is to disprove other suggestions.
        else:
            logger.info(f"{accusation.suggestor}'s accusation was not correct.")
            logger.info("They will remain to provide input on suggestions.")
            # Remove player and transition to the next one
            game.moveable_players.remove(accusation.suggestor)
            if len(game.moveable_players) == 0:
                logger.info("No Players left to make correct accusations.")
                logger.info("*****Game Over*****")
                game.victory_state = EndGameEnum.no_winners
            game.next_player()
            game.current_turn.phase = "move"


@app.post("/suggestion", status_code=200)
async def makeSuggestion(playerSuggestion: Statement) -> dict:
    """
    Function that accepts suggestions from a player, verifies they can be made,
    and returns the first card from the players following the player who suggested
    which disproves the suggestion

    Args:
        gameKey: string representing the game key for the game which the suggestion is made
        suggestor: the player making the suggestion
        suggestion: the suggestion they are making (player, weapon, and room)
    """

    # specify internal variable details
    suggestor: str
    gameKey: str
    suggestion: Statement.Details
    returnDict = {
        "response": PlayerEnum | RoomEnum | WeaponEnum | None,
        "player": str | None,
    }

    # exceptions for unprovided data
    if not playerSuggestion.player:
        raise HTTPException(
            status_code=HttpEnum.bad_request,
            detail="player making suggestion is unspecified",
        )
    else:
        suggestor = playerSuggestion.player

    if not playerSuggestion.gameKey:
        raise HTTPException(
            status_code=HttpEnum.bad_request, detail="gameKey unspecified"
        )
    else:
        gameKey = playerSuggestion.gameKey

    if not playerSuggestion.statementDetails:
        raise HTTPException(
            status_code=HttpEnum.bad_request, detail="suggestion details unspecified"
        )
    else:
        suggestion = playerSuggestion.statementDetails

    # get the game state information
    if gameKey not in games.keys():
        # if there are keys and if the requested key doesn't match, throw an exception
        raise HTTPException(status_code=HttpEnum.not_found, detail="unknown game key")
    else:
        currentGame = games[gameKey]

    # dump to dictionary format
    currentGameDict = currentGame.dump_to_dict()

    try:
        # get the character represented by the current player
        playersCharacter = currentGameDict["player_character_mapping"][suggestor]
    except:
        raise HTTPException(
            status_code=HttpEnum.not_found, detail="Suggestor is unknown to the game"
        )

    # Ensure the suggestor is in the same room as the suggestion they are making
    # Satisfies game requirement
    if get_player_location(playersCharacter, currentGame) != suggestion.room:
        # TODO: This exception is necessary once the players can actually make suggestions - to test it will be commented out
        raise HTTPException(
            status_code=HttpEnum.forbidden,
            detail="Suggestor is unable to make this suggestion -- suggestor is not in the room where the suggestion is being made",
        )

    # move the target player to the suggested room
    # get current room
    movingPlayerCurrentLocation = get_player_location(suggestion.person, currentGame)
    # create a move object of the suggestion movement
    forcedMove = MoveAction(player=suggestion.person, location=suggestion.room)
    # execute move
    move_player(
        movement=forcedMove,
        current_location=movingPlayerCurrentLocation,
        gs=currentGame,
    )

    # after move update the game state dictionary
    currentGameDict = currentGame.dump_to_dict()

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
            returnDict["response"] = random.choice(overlapCards)
            returnDict["player"] = p
            # break loop immediately once an overlapping card is found
            break

    # change game turn phase
    currentGame.current_turn.phase = "accuse"
    return returnDict
