from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from util.game_state import GameState, GameEvent
from util.enums import MoveAction, AccuseAction, HallEnum, RoomEnum, HttpEnum
from util.functions import get_player_location
from util.movement import Map, move_player, validate_move
from pydantic import BaseModel

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


class NewGameRequest(BaseModel):
    num_players: int


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


@app.post("/accusation", status_code=200)
async def makeAccusation(accusation: AccuseAction):
    """ """
    if accusation.id == None or accusation.id not in games.keys():
        raise HTTPException(status_code=404, detail="Game not found.")
    game = games[accusation.id]

    # If the accusation Statement is all None, no accusation is desired
    # and move to the next player. Not logging as it will be the average action
    accval = accusation.statement
    if not (accval.person or accval.weapon or accval.room):
        # TODO: Modify next_player to conform with Michael's changes

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
            # TODO: Define how we wish to signal the end of the game
            logger.info(
                f"{accusation.suggestor} correctly put together the Clues and won the game!"
            )
            logger.info(f"*****Game Over*****")
            return False
        # Otherwise, the player can continue playing only as an observor to disprove
        # suggestions; i.e. they cannot move and make suggestions or accusations
        else:
            logger.info(f"{accusation.suggestor}'s accusation was not correct.")
            logger.info("They will remain to provide input on suggestions.")
            # Remove player and transition to the next one
            game.moveable_players.remove(accusation.suggestor)
            if len(game.moveable_players) == 0:
                logger.info("No Players left to make correct accusations.")
                logger.info("*****Game Over*****")
                return False
            game.next_player()
            game.current_turn.phase = "move"
