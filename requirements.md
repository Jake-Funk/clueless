# Requirements
- This document covers the essential requirements for this project
---

## Skeletal
The bare bones architecture increment to prove that subsystems can communicate

#### Server

- Functional
    - [] The server shall store all the game data for the players, acting as the main source of truth and rules
    - [] The server shall be the only actor capable of altering the stored game data
    - [] The server needs to be able to create and initialize a game with a unique identifier
    - [] Upon creation of a new game, the server will create a random solution and deal the remaining cards to the players
- Non-Functional
    - [] The server will guarantee type safety using Pydantic
    - [] The server will define specific input enums to control data types
    - [] The server will utilize FastAPI to define endpoints to the client

#### Client

- Functional
    - [] The client will need to be able to allow the user to create a new game and join an existing game
    - [] Once the client creates or joins a game, they need to be able to see the respective game state information
- Non-Functional
    - [] The client will be implemented using NodeJS
    - [] The client will utilize Javascript

## Minimal
The essential increment which allows a full play through of the game but is not optimized or refined

#### Server

- Functional
    - [] The server will allow the player to make a Move, Suggestion and Accusation action on their turn
    - [] After each player's turn, the server will iterate to the next player, starting back at the first player when all players have gone
    - [] The server will end the game when a player makes a correct accusation or no players are able to make an accusation 
    - [] The server will restrict and enforce input conditions on the players 
- Non-Functional 
    - [] The server will map out all possible locations for a player to move their character at any location 
    - [] The server will respond to the players with error codes if they have made an input error
    - [] The server will validate all logic needed to execute the player actions with unit tests

#### Client

- Functional 
    - [] The client will display a basic board for the players to view the status of the game at any moment
    - [] The client will display where all characters are located with initials
    - [] The client will hide most of the internal game state from the players to prevent cheating
    - [] The client will communicate to the player the consequences of their action 
      - Proper or improper movement
      - What cards were disproved with a suggestion 
      - If an Accusation was correct or not 
- Non-Functional 
    - [] The client will constantly ping the server for any updates to keep the players in the loop
    - [] The client provide a basic menu for the player's to navigate
    - [] The client will need to display room names but not Hallways
    - [] the client will allow the user to click on board locations for their movement or suggestions

## Target
The desired final state of the project for the class

#### Server

- Functional 
    - [] The server will need to authenticate players when joining a game to prevent any risk and keep accuracy
    - [] The server will need to support multiple games at once 
    - [] The server should ask players what characters they wish to be and what their username is 
    - [] The server will need to hold onto what cards a player has disproved 

#### Client 

