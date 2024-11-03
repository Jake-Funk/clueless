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
import { useContext, useState } from "react";
import { GameStateContext, gsObj } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";

const availPeople = [
  "Miss Scarlet",
  "Professor Plum",
  "Mr. Green",
  "Mrs. Peacock",
  "Colonel Mustard",
  "Mrs. White",
];

const availWeapons = [
  "rope",
  "knife",
  "revolver",
  "candlestick",
  "lead pipe",
  "wrench",
];

export default function SuggestBtn() {
  const { player, gameID, gameState, trigger, setTrigger } =
    useContext(GameStateContext);
  const [person, setPerson] = useState("");
  const [weapon, setWeapon] = useState("");
  const [open, setOpen] = useState(false);
  const { toast } = useToast();
  let room: string;

  for (const tmpRoom in gameState.map) {
    if (
      (gameState as gsObj).map[tmpRoom].includes(
        gameState.player_character_mapping[player],
      )
    ) {
      room = tmpRoom;
    }
  }

  async function handleSubmit() {
    console.log(
      `You chose:\nperson: ${person}\nweapon: ${weapon}\nroom: ${room}`,
    );
    const rawResp = await fetch(
      process.env.NEXT_PUBLIC_SERVER_URL + `/suggestion`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          player: player,
          gameKey: gameID,
          statementDetails: { person: person, weapon: weapon, room: room },
        }),
      },
    );
    const content = await rawResp.json();
    if (rawResp.status == 200) {
      setOpen(false);
      setTrigger(trigger + (1 % 10));
      if (content.response) {
        toast({ description: `${content.player} had ${content.response}` });
      } else {
        toast({
          description:
            "Nobody could disprove your suggestion... Is this a clue?",
        });
      }
    } else {
      console.log(content);
    }
    console.log(content); // this log should be removed once we have a permanent store of gathered clues.
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">Make Suggestion</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Suggestion</DialogTitle>
          <DialogDescription>
            Put together your suggestion. Click submit when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Person:
            </Label>
            <Select
              onValueChange={(e) => {
                setPerson(e);
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Person" />
              </SelectTrigger>
              <SelectContent>
                {availPeople.map((item: string) => {
                  return (
                    <SelectItem value={item} key={item}>
                      {item}
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Weapon:
            </Label>
            <Select
              onValueChange={(e) => {
                setWeapon(e);
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="weapon" />
              </SelectTrigger>
              <SelectContent>
                {availWeapons.map((item: string) => {
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
