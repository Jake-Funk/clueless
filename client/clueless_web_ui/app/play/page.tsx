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

export default function Home() {
  const [gameID, setGameId] = useState("");
  const [player, setPlayer] = useState("");
  const [userAnswer, setUserAnswer] = useState("");
  const [trigger, setTrigger] = useState(0);
  const [gameState, setGameState] = useState(defaultGameState);
  const currPlayer: string = gameState.game_phase.player;
  const currPhase: string = gameState.game_phase.phase;

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
                {currPlayer != player ? ( // someone else's turn
                  <div>
                    It is{" "}
                    {(gameState as gsObj).player_username_mapping[currPlayer] ==
                    ""
                      ? "someone else"
                      : (gameState as gsObj).player_username_mapping[
                          currPlayer
                        ]}
                    &apos;s turn.
                  </div>
                ) : // your turn and not marked as moved
                !(gameState as gsObj).moved_by_suggest[
                    (gameState as gsObj).player_character_mapping[currPlayer]
                  ] ? (
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
                ) : // your turn and marked as moved
                !userAnswer ? (
                  <div>
                    <div className="text-center">
                      You were moved by another player&apos;s suggestion. <br />
                      Would you like to make a suggestion in current room OR
                      move as normal?
                    </div>
                    <div className="flex justify-center gap-4 m-3">
                      <Button
                        onClick={() => setUserAnswer("suggest")}
                        variant="outline"
                      >
                        Suggestion
                      </Button>
                      <Button
                        onClick={() => setUserAnswer("move")}
                        variant="outline"
                      >
                        Move
                      </Button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div>It is your turn.</div>
                    {userAnswer == "suggest" && <SuggestBtn />}
                    {userAnswer == "move" && (
                      <>
                        {currPhase == "move" && <MoveBtn />}
                        {currPhase == "accuse" && (
                          <>
                            <div className="text-center">
                              You have no valid moves.
                              <br />
                              Do you want to make an accusation?
                            </div>
                            <AccuseBtn />
                          </>
                        )}
                      </>
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
