from fastapi import FastAPI, HTTPException

from util.game_state import GameState
from util.enums import MoveAction, HallEnum
from util.functions import get_player_location
from util.movement import Map, move_player

# TODO: Require proper initialization of game state(s) here for
# skeleton and minimal systems
dummy_game_state = GameState(3)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
def move(movement: MoveAction):
    gs = dummy_game_state
    # Check if the Game Id is valid and exists
    # TODO: Need to also validate against the list of available game states
    if movement.id is None:
        raise HTTPException(status_code=404, detail="Invalid Game")

    # Check if it is the correct part of the current turn
    if gs.current_turn.phase != "move":
        raise HTTPException(status_code=404, detail="Not in the movement phase")

    # Check if player can be found on current map
    current_location = get_player_location(movement.player)
    if current_location is None:
        raise HTTPException(status_code=403, detail="Player not found on Map")

    # Check if desired location is adjacent or in secret passageway (if applicable)
    if movement.location not in Map[current_location]:
        raise HTTPException(
            status_code=400, detail="Invalid move from current location"
        )

    # Check if movement is to a hallway and if that hallway is already occupied
    if isinstance(movement.location, HallEnum) and len(gs.map[movement.location]) >= 1:
        raise HTTPException(
            status_code=404, detail="Cannot move into an occupied hallway"
        )

    # Great Success!
    move_player(movement, current_location, gs)
    gs.current_turn.phase = "suggest"
    raise HTTPException(
        status_code=200,
        detail=f"Successfully moved {movement.player.value} to {movement.location}",
    )
