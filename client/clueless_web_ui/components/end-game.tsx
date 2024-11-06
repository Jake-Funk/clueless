"use client";
import { GameStateContext } from "@/lib/types";
import { BadgePlus, BookMarked, Github, Search } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useContext } from "react";

export default function EndGame() {
  const iconClasses = "fill-background";
  const router = useRouter();
  const { gameState, player } = useContext(GameStateContext);

  function handleClick(e: React.MouseEvent<HTMLElement>, route: string) {
    e.preventDefault();
    router.push(route);
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] overflow-hidden">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="flex items-center gap-4">
          <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
            {player == gameState.game_phase.player
              ? "You Won!"
              : `${gameState.game_phase.player} is the Winner!`}
          </h1>
          <Search className={iconClasses} size={40} />
        </div>
        <div className="text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          {player == gameState.game_phase.player
            ? "Great work gathering clues!"
            : "Better luck next time!"}
        </div>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <Link href="/new_game" onClick={(e) => handleClick(e, "new_game")}>
            <div
              className="rounded-full border border-solid border-transparent focus:bg-[#383838] dark:focus:bg-[#ccc] transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
              role="button"
              tabIndex={0}
            >
              <BadgePlus width={20} height={20} />
              Play Again
            </div>
          </Link>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="#"
          target="_blank"
          rel="noopener noreferrer"
        >
          <BookMarked width={16} height={16} />
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
  );
}
