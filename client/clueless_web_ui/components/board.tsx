import { useContext } from "react";
import { Separator } from "./ui/separator";
import { GameStateContext } from "@/app/play/page";

export function Board() {
  const { gameState } = useContext(GameStateContext);

  return (
    <div className="px-4 flex flex-col w-full items-center">
      <div className="grid grid-cols-5 gap-0 max-w-4xl w-full">
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Study</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.study.map((person: string) => {
              if (person == gameState.map.study.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted">
          <div>{gameState.map["0"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Hall</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.hall.map((person: string) => {
              if (person == gameState.map.hall.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["1"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Lounge</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.lounge.map((person: string) => {
              if (person == gameState.map.lounge.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>

        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["2"][0]}</div>
        </div>
        <div className="border h-32 bg-muted-foreground"></div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["3"][0]}</div>
        </div>
        <div className="border h-32 bg-muted-foreground"></div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["4"][0]}</div>
        </div>

        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Library</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.library.map((person: string) => {
              if (person == gameState.map.library.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["5"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Billiard Room</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.billiard.map((person: string) => {
              if (person == gameState.map.billiard.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["6"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Dining Room</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.dining.map((person: string) => {
              if (person == gameState.map.dining.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>

        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["7"][0]}</div>
        </div>
        <div className="border h-32 bg-muted-foreground"></div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["8"][0]}</div>
        </div>
        <div className="border h-32 bg-muted-foreground"></div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["9"][0]}</div>
        </div>

        <div className="border h-32 flex flex-col items-center overflow-hidden">
          <div className="py-1 font-bold">Conservatory</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.conservatory.map((person: string) => {
              if (
                person == gameState.map.conservatory.findLast((elem) => elem)
              ) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["10"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Ballroom</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.ballroom.map((person: string) => {
              if (person == gameState.map.ballroom.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
        <div className="border h-32 bg-muted flex items-center justify-center">
          <div>{gameState.map["11"][0]}</div>
        </div>
        <div className="border h-32 flex flex-col items-center">
          <div className="py-1 font-bold">Kitchen</div>
          <Separator />
          <div className="flex w-full flex-wrap gap-1 items-center justify-center p-1">
            {gameState.map.kitchen.map((person: string) => {
              if (person == gameState.map.kitchen.findLast((elem) => elem)) {
                return <span key={person}>{person}</span>;
              } else {
                return <span key={person}>{person},</span>;
              }
            })}
          </div>
        </div>
      </div>
    </div>
  );
}