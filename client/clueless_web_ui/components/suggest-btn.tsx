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
import { GameStateContext } from "@/lib/types";

const availPeople = [
  "Miss Scarlet",
  "Professor Plum",
  "Mr. Green",
  "Mrs. Peacock",
  "Colonel Mustard",
  "Mrs. White",
];

const availRooms = [
  "study",
  "hall",
  "lounge",
  "library",
  "billiard",
  "dining",
  "kitchen",
  "conservatory",
  "ballroom",
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
  const { player, gameID } = useContext(GameStateContext);
  const [person, setPerson] = useState("");
  const [weapon, setWeapon] = useState("");
  const [room, setRoom] = useState("");

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
    console.log(content);
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Make Suggestion</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Suggestion</DialogTitle>
          <DialogDescription>
            Put together your suggestion. Click submit when you`&apos;`re done.
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
                <SelectValue placeholder="Person" />
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
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Room:
            </Label>
            <Select
              onValueChange={(e) => {
                setRoom(e);
              }}
            >
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Person" />
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