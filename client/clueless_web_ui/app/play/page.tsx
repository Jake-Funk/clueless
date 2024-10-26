"use client"
import AccuseBtn from "@/components/accuse-btn"
import { AppSidebar } from "@/components/app-sidebar"
import { Board } from "@/components/board"
import MoveBtn from "@/components/move-btn"
import SuggestBtn from "@/components/suggest-btn"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { createContext, useEffect, useState } from "react"

const defaultGameState = {
  game_phase: {
    player: "",
    phase: "",
  },
  player_character_mapping: {},
  map: {
    study: [],
    hall: [],
    lounge: [],
    library: [],
    billiard: [],
    dining: [],
    conservatory: [],
    ballroom: [],
    kitchen: [],
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
  },
}

export const GameStateContext = createContext({
  gameState: defaultGameState,
  player: "",
  gameID: "",
})
export default function Home() {
  const [gameID, setGameId] = useState("")
  const [player, setPlayer] = useState("")
  const [gameState, setGameState] = useState(defaultGameState)
  const currPlayer: string = gameState.game_phase.player
  const currPhase: string = gameState.game_phase.phase

  useEffect(() => {
    const value = localStorage.getItem("gameID") || ""
    setGameId(value)

    const playerNo = localStorage.getItem("player") || ""
    setPlayer(playerNo)
  }, [])

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
        }
      )
      const content = await rawResp.json()
      setGameState(content)
    }
    if (gameID) {
      getGameState()
    }
  }, [gameID])

  return (
    <GameStateContext.Provider value={{ gameState, player, gameID }}>
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <header className="flex h-16 shrink-0 items-center gap-2">
            <div className="flex items-center gap-2 px-4">
              <SidebarTrigger className="-ml-1" />
            </div>
          </header>
          <div className="flex items-center space-x-4 p-4 justify-center">
            {currPlayer != player ? (
              <div>
                It is {gameState.player_character_mapping[currPlayer]}'s turn.
              </div>
            ) : (
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
            )}
          </div>
          <Board />
          <pre>{JSON.stringify(gameState, null, 2)}</pre>
        </SidebarInset>
      </SidebarProvider>
    </GameStateContext.Provider>
  )
}
