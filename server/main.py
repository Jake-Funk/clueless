from fastapi import FastAPI, HTTPException

from util.game_state import GameState
from util.enums import MoveAction, HallEnum, HttpEnum
from util.functions import get_player_location
from util.movement import Map, move_player, validate_move

from pydantic import BaseModel
import uuid

app = FastAPI()
games = {}


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


@app.post("/")
async def move(movement: MoveAction):
    # Check if player can be found on current map
    try:
        current_location = get_player_location(movement.player)
    except Exception:
        raise HTTPException(status_code=404, detail="Player not found on Map.")

    http_code = validate_move(movement, current_location, games)

    if http_code == HttpEnum.not_found:
        raise HTTPException(status_code=404, detail="Game not found.")
    elif http_code == HttpEnum.bad_request:
        raise HTTPException(status_code=400, detail="Invalid move")
    elif http_code == HttpEnum.good:
        gs[movement.id].current_turn.phase = "suggest"
        move_player(movement, current_location, gs)
        return {"Response": f"Successfully moved {movement.player.value} to {movement.location}"}
    else:
       raise HTTPException(status_code=500, detail="Internal server error occurred.")

