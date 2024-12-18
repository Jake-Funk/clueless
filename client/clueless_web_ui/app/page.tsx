"use client";
import {
  BadgePlus,
  BookMarked,
  Github,
  Search,
  UserRoundPlus,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const [iconClasses, setIconClasses] = useState("fill-background");
  const router = useRouter();

  function handleClick(e: React.MouseEvent<HTMLElement>, route: string) {
    e.preventDefault();
    setIconClasses(
      "fill-background animate-out ease-in zoom-out-[150] duration-1.5s fill-mode-forwards",
    );
    setTimeout(() => {
      router.push(route);
    }, 1500);
  }
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] overflow-hidden">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="flex items-center gap-4">
          <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
            Clueless
          </h1>
          <Search className={iconClasses} size={40} />
        </div>
        <div className="text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          Everyone has a secret...
          <br />
          Can you find the killer before they find you?
        </div>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <Link href="/new_game" onClick={(e) => handleClick(e, "new_game")}>
            <div
              className="rounded-full border border-solid border-transparent focus:bg-[#383838] dark:focus:bg-[#ccc] transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
              role="button"
              tabIndex={0}
            >
              <BadgePlus width={20} height={20} />
              Start Game
            </div>
          </Link>

          <Link href="/join_game">
            <div
              className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center gap-2 hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
              role="button"
              tabIndex={0}
              onClick={(e) => handleClick(e, "join_game")}
            >
              <UserRoundPlus width={20} height={20} />
              Join Game
            </div>
          </Link>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="/Clue-Less.pdf"
          target="_blank"
          rel="noopener noreferrer"
        >
          <BookMarked width={16} height={16} />
          Rules
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://github.com/Jake-Funk/clueless"
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
