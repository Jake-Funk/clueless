import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { useContext, useEffect, useState } from "react";
import { GameStateContext } from "@/app/play/page";

const boardMap = {
  0: ["study", "hall"],
  1: ["lounge", "hall"],
  2: ["study", "library"],
  3: ["billiard", "hall"],
  4: ["lounge", "dining"],
  5: ["billiard", "library"],
  6: ["billiard", "dining"],
  7: ["conservatory", "library"],
  8: ["ballroom", "billiard"],
  9: ["dining", "kitchen"],
  10: ["ballroom", "conservatory"],
  11: ["ballroom", "kitchen"],
  study: [0, 2, "kitchen"],
  hall: [0, 1, 3],
  lounge: [1, 4, "conservatory"],
  library: [2, 5, 7],
  billiard: [8, 3, 5, 6],
  dining: [9, 4, 6],
  conservatory: [10, "lounge", 7],
  ballroom: [8, 10, 11],
  kitchen: [9, 11, "study"],
};

export default function MoveBtn() {
  const { gameState, player, gameID } = useContext(GameStateContext);
  const [selection, setSelection] = useState("");

  function getAvailRooms() {
    for (const room in gameState.map) {
      if (
        gameState.map[room].includes(gameState.player_character_mapping[player])
      ) {
        return boardMap[room];
      }
    }
  }

  const availRooms = getAvailRooms();

  async function handleSubmit() {
    console.log(selection);
    const rawResp = await fetch(process.env.NEXT_PUBLIC_SERVER_URL + `/move`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ player: player, location: selection, id: gameID }),
    });
    const content = await rawResp.json();
    console.log(content);
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Move</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Move your Character</DialogTitle>
          <DialogDescription>
            Select where you want to move here. Click submit when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Location
            </Label>
            <Select
              onValueChange={(e) => {
                setSelection(e);
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Room" />
              </SelectTrigger>
              <SelectContent>
                {availRooms.map((item: string) => {
                  return (
                    <SelectItem value={item} key={item}>
                      {item}
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>
          </div>
        </div>
        <DialogFooter>
          <Button type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
