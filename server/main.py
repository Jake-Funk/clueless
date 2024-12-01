from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from util.game_state import GameState
from util.enums import RoomEnum, HttpEnum, EndGameEnum
from util.actions import ChatRequest, NewGameRequest, MoveAction, Statement
from util.functions import get_character_location, get_time, location_str
from util.movement import move_player, validate_move
import random

import uuid

import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    logger.debug(f"Creating Game State of ID: {key}")
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
        current_location = get_character_location(
            games[key].player_character_mapping[movement.player], games[key]
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found on Map.")

    # If the player's character is marked as having been moved by a suggestion,
    # reset it here. The default is false, so setting it to false is technically
    # faster than also adding a conditional
    games[key].reset_player_moved_by_suggest(
        games[key].player_character_mapping[movement.player]
    )

    http_code = validate_move(movement, current_location, games[key])

    if http_code[0] == HttpEnum.good:
        move_player(
            character=games[key].player_character_mapping[movement.player],
            target_location=movement.location,
            current_location=current_location,
            gs=games[key],
        )
        # Check if player entered a room
        # If they have, move the game phase to suggestion
        # Otherwise keep the same phase but change players
        if isinstance(movement.location, RoomEnum):
            games[key].next_phase("suggest")
            logging.info(f"Moving {movement.player} to {movement.location}")
            logging.info(f"{movement.player} can now make a suggestion")
        else:
            # Players in Hallways can still make Accusations
            games[key].next_phase("accuse")
            logging.info(
                f"{movement.player} moved to a Hallway, going to Accusation phase"
            )

        games[key].logs.append(
            f"{get_time()} - {movement.player} moved to {location_str(movement.location)}."
        )
        return {
            "Response": f"Successfully moved {movement.player} to {movement.location.value}. Moving to next Player."
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
    if accusation.gameKey == None or accusation.gameKey not in games.keys():
        raise HTTPException(status_code=404, detail="Game not found.")
    game = games[accusation.gameKey]

    if game.current_turn.phase != "accuse":
        raise HTTPException(
            status_code=HttpEnum.bad_request,
            detail="Game phase not in the accusation phase",
        )

    # If the accusation Statement is all None, no accusation is desired
    # and move to the next player.
    accval = accusation.statementDetails
    if not (accval.person or accval.weapon or accval.room):
        log_str = f"{accusation.player} opted to not make an accusation."
        logger.info(log_str)
        game.logs.append(f"{get_time()} - " + log_str)
        # Move game to the next player and the move phase
        game.next_player()
        game.next_phase("move")
    else:
        game.logs.append(
            f"{get_time()} - {accusation.player} made an accusation of {accval.person.value} in {location_str(accval.room)} with the {accval.weapon.value}."
        )
        # If the accusation is correct, end the game
        if (
            accval.person == game.solution.person
            and accval.weapon == game.solution.weapon
            and accval.room == game.solution.room
        ):
            game.logs.append(
                f"{get_time()} - {accusation.player} uncovered all the Clues and won the game!"
            )
            logging.info(
                f"{accusation.player} correctly put together the Clues and won the game!"
            )
            logging.info(f"*****Game Over*****")
            game.victory_state = EndGameEnum.winner_found
        # Otherwise, the player can continue playing only as an observor to disprove
        # suggestions; i.e. they cannot move, make suggestions or accusations.
        # Their only purpose is to disprove other suggestions.
        else:
            game.logs.append(
                f"{get_time()} - {accusation.player}'s accusation was incorrect; they are now a spectator"
            )
            logging.info(f"{accusation.player}'s accusation was not correct.")
            logging.info("They will remain to provide input on suggestions.")
            game.next_player()
            # Remove player and transition to the next one
            game.moveable_players.remove(accusation.player)
            if len(game.moveable_players) == 0:
                logging.info("No Players left to make correct accusations.")
                logging.info("*****Game Over*****")
                game.victory_state = EndGameEnum.no_winners
            game.next_phase("move")

    return game.victory_state


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
    returnDict = {"response": "", "player": ""}

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

    if not (
        playerSuggestion.statementDetails.person
        or playerSuggestion.statementDetails.weapon
        or playerSuggestion.statementDetails.room
    ):
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

    if currentGame.current_turn.phase != "suggest":
        raise HTTPException(
            status_code=HttpEnum.bad_request,
            detail="Game phase not in the suggestion phase",
        )

    # If the player's character is marked as having been moved by a suggestion,
    # reset it here. The default is false, so setting it to false is technically
    # faster than also adding a conditional
    currentGame.reset_player_moved_by_suggest(playersCharacter)

    # Ensure the suggestor is in the same room as the suggestion they are making
    # Satisfies game requirement
    if get_character_location(playersCharacter, currentGame) != suggestion.room:
        # TODO: This exception is necessary once the players can actually make suggestions - to test it will be commented out
        raise HTTPException(
            status_code=HttpEnum.forbidden,
            detail="Suggestor is unable to make this suggestion -- suggestor is not in the room where the suggestion is being made",
        )

    # move the target player to the suggested room
    # get current room
    movingPlayerCurrentLocation = get_character_location(suggestion.person, currentGame)
    # create a move object of the suggestion movement

    # For the sake of being more professional, don't display log
    # if the suggested person and the player's character are the same
    if playerSuggestion.player is not suggestion.person:
        currentGame.logs.append(
            f"{get_time()} - Moving suggested character {suggestion.person.value} to {location_str(suggestion.room)}"
        )
        logger.info(f"Moving suggested player {suggestion.person} to {suggestion.room}")

    # execute move
    move_player(
        character=suggestion.person,
        target_location=suggestion.room,
        current_location=movingPlayerCurrentLocation,
        gs=currentGame,
    )

    # Mark the Targeted player as having been moved by a suggestion
    logger.info(
        f"{suggestion.person} is being marked as having been moved by suggestion"
    )
    currentGame.set_player_moved_by_suggest(suggestion.person)

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
    found_card = False
    for p in playersList:
        # TODO: Future iterations should send a request out to the identified player to show a card if one of the suggestions is in their hand
        playerCards = currentGameDict[p]

        # select the cards that are in the suggestion
        overlapCards = [
            c
            for c in playerCards
            if c in suggestion.person or c in suggestion.weapon or c in suggestion.room
        ]

        # check all overlapping cards for cards that the player has seen before and remove them from the pool of possible cards
        overlapCards = [
            c for c in overlapCards if c not in currentGame.playerHasSeen[suggestor]
        ]

        if overlapCards:
            # if there are any overlapping cards, return one of them randomly
            returnDict["response"] = random.choice(overlapCards)
            returnDict["player"] = p

            # add chosen card to the set of seen cards
            currentGame.playerHasSeen[suggestor].add(returnDict["response"])

            currentGame.logs.append(
                f"{get_time()} - {suggestor}'s suggestion was disproved."
            )
            logger.info(
                f"{suggestor}'s suggestion had a card in an other player's hand."
            )

            # break loop immediately once an overlapping card is found
            found_card = True
            break
    if not found_card:
        currentGame.logs.append(
            f"{get_time()} - {suggestor}'s suggestion was not disproved."
        )
        logger.info(
            f"{suggestor}'s suggestion did NOT have a card in an other player's hand."
        )

    # change game turn phase
    currentGame.next_phase("accuse")
    return returnDict


@app.post("/chat", status_code=200)
async def formChat(chatReq: ChatRequest):
    """
    Endpoint to form a chat message
    """
    # get the game state information
    if chatReq.key not in games.keys():
        # if there are keys and if the requested key doesn't match, throw an exception
        raise HTTPException(status_code=HttpEnum.not_found, detail="unknown game key")
    else:
        currentGame = games[chatReq.key]

    logger.debug("Forming a chat message")
    currentGame.chat.append(f'{get_time()} - {chatReq.player}: "{chatReq.message}"')
    return {"Response": f'{get_time()} - {chatReq.player}: "{chatReq.message}"'}
