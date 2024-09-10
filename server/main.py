from fastapi import FastAPI
from util.game_state import GameEvent, GameState

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
Server endpoint that sends players suggestions in the form of a GameEvent message to the server

'''
@app.post('/Suggestions/')
async def playerSuggests(playerSuggestion: GameEvent):
    # NOTE: either the GameEvent class needs to be made into a pydantic object or I need to do that here
    
    # PlayerSuggestions are visible to all players, so make visibility 0
    playerSuggestion.level = 0

    # message string that will be passed as the suggestion
    playerSuggestion.message = "Test"

    return(playerSuggestion)

'''
Server endpoint that allows the client to view the game state
    For the skeletal implementation, this will be direcly viewable by any client
    barebones for now - will be built out 
    
    :author: Michael Baker
'''
@app.get('/game/')
async def gameState(currentGameState: GameState) -> GameState:
    return(currentGameState)