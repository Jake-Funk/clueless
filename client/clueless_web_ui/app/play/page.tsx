"use client"
import { Github } from "lucide-react"
import Image from "next/image"
import { useEffect, useState } from "react"

export default function Home() {
  const [gameID, setGameId] = useState("")
  const [gameState, setGameState] = useState({})

  useEffect(() => {
    const value = localStorage.getItem("gameID") || ""
    setGameId(value)
  }, [])

  useEffect(() => {
    async function getGameState() {
      const rawResp = await fetch(
        `https://clueless-server-915069415929.us-east1.run.app/State?gameKey=${gameID}`,
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
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] overflow-hidden">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="flex items-center gap-4">
          <h1 className="scroll-m-20 text-2xl font-bold tracking-tight lg:text-5xl">
            Your Game ID:
          </h1>
        </div>
        <div>{gameID}</div>
        <div className="flex items-center gap-4">
          <h1 className="scroll-m-20 text-2xl font-bold tracking-tight lg:text-5xl">
            Game State:
          </h1>
        </div>
        <pre>{JSON.stringify(gameState, null, 2)}</pre>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="#"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Rules
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="#"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Github width={16} height={16} />
          GitHub
        </a>
      </footer>
    </div>
  )
}
