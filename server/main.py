from fastapi import FastAPI, HTTPException

from util.game_state import GameState
from util.enums import MoveAction, HallEnum, RoomEnum, HttpEnum
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
