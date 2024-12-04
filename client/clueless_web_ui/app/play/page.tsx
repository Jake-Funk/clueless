"use client";
import { Button } from "@/components/ui/button";
import AccuseBtn from "@/components/accuse-btn";
import { AppSidebar } from "@/components/app-sidebar";
import { Board } from "@/components/board";
import EndGame from "@/components/end-game";
import MoveBtn from "@/components/move-btn";
import SuggestBtn from "@/components/suggest-btn";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { defaultGameState, GameStateContext, gsObj } from "@/lib/types";
import { useEffect, useState } from "react";

export const sendMessage = async (gameID, phase, player) => {
  const response = await fetch(process.env.NEXT_PUBLIC_SERVER_URL + `/phase`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      key: gameID,
      phase: phase,
      player: player
    }),
  });

  if (!response.ok) {
    throw new Error('Request failed');
  }

  const data = await response.json();
  return data;  // Return the response data for further processing
};

export default function Home() {
  const [gameID, setGameId] = useState("");
  const [player, setPlayer] = useState("");
  const [trigger, setTrigger] = useState(0);
  const [gameState, setGameState] = useState(defaultGameState);
  const currPlayer: string = gameState.game_phase.player;
  const currPhase: string = gameState.game_phase.phase;
  const [error, setError] = useState(null);

  useEffect(() => {
    const value = localStorage.getItem("gameID") || "";
    setGameId(value);

    const playerNo = localStorage.getItem("player") || "";
    setPlayer(playerNo);
  }, []);

  useEffect(() => {
    async function getGameState() {
      const rawResp = await fetch(
        process.env.NEXT_PUBLIC_SERVER_URL + `/State?gameKey=${gameID}`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        },
      );
      const content = await rawResp.json();
      console.log(content); // this is for development use only and should be removed for the target inc (probably)
      setGameState(content);
    }
    if (gameID) {
      getGameState();
    }
  }, [gameID, trigger]);

  // Handle the player choosing to stay in
  // the room they were moved to by an other
  // player's suggestion
  const handleClick = async (phase: string) => { 
    try {
      const response = await sendMessage(gameID, phase, player);
      setTrigger(trigger + 1);

    } catch (err) {
      setError('Error sending phase request');
      console.error(err);
    }
  };

  return (
    <GameStateContext.Provider
      value={{ gameState, player, gameID, trigger, setTrigger }}
    >
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <header className="flex h-16 shrink-0 items-center gap-2">
            <div className="flex items-center gap-2 px-4">
              <SidebarTrigger className="-ml-1" />
            </div>
          </header>
          {gameState.victory_state == 0 ? (
            <>
              <div className="flex items-center space-x-4 p-4 justify-center">
                {currPlayer != player ? (
                  <div>
                    It is{" "}
                    {(gameState as gsObj).player_character_mapping[currPlayer]}
                    &apos;s turn.
                  </div>
                ) : (
                  <>
                    {gameState.moved_by_suggest[(gameState as gsObj).player_character_mapping[currPlayer]] === false ? (
                      <>
                      <div>It is your turn.</div>
                      {currPhase == "move" && <MoveBtn />}
                      {currPhase == "suggest" && <SuggestBtn />}
                      {currPhase == "accuse" && (
                        <>
                          <div>Do you want to make an accusation?</div>
                          <AccuseBtn />
                        </>
                      )}
                    </>
                  ) : (
                    <div>
                      <div>Make Suggestion in current room OR move as normal?</div>
                      <Button 
                        onClick={() => handleClick("suggest")} 
                        variant="outline"
                        className="mt-2 ml-32 mr-2"
                      >
                        Stay
                      </Button>
                      <Button 
                        onClick={() => handleClick("move")} 
                        variant="outline"
                      >
                        Move
                      </Button>
                    </div> 
                  )}
                  </>
                )}
              </div>
              <Board />
              {process.env.NODE_ENV === "development" && (
                <pre>{JSON.stringify(gameState, null, 2)}</pre>
              )}
            </>
          ) : (
            <EndGame />
          )}
        </SidebarInset>
      </SidebarProvider>
    </GameStateContext.Provider>
  );
}
