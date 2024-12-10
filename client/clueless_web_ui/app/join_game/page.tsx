"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookMarked, Github } from "lucide-react";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";

const formSchema = z.object({
  id: z.coerce.string().uuid("Not a valid game ID"),
});

const usernameFormSchema = z.object({
  username: z.coerce
    .string()
    .min(1, { message: "Must have at least 1 character in your username" })
    .max(20, { message: "Must be 20 or fewer characters long" }),
});

const defaultUsernameMap = {
  player1: "",
  player2: "",
  player3: "",
  player4: "",
  player5: "",
  player6: "",
};

interface usernameMap {
  [key: string]: string;
}

export default function Home() {
  const router = useRouter();
  const [err, setErr] = useState(false);
  const [playerSelect, setPlayerSelect] = useState(false);
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [gameId, setGameId] = useState("");
  const [usernameSet, setUsernameSet] = useState(false);
  const [playerOptions, setPlayerOptions] = useState<string[]>([]);
  const [playerUsernameOptions, setPlayerUsernameOptions] =
    useState<usernameMap>(defaultUsernameMap);

  function chosePlayer(player: string) {
    try {
      localStorage.setItem("player", player);
    } catch {
      console.error("Problem adding data to local storage");
    }
    router.push("/play");
  }

  function chosePlayerUnset(player: string) {
    try {
      localStorage.setItem("player", player);
    } catch {
      console.error("Problem adding data to local storage");
    }
    setSelectedPlayer(player);
    setUsernameSet(true);
  }

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      id: "",
    },
  });

  const usernameForm = useForm<z.infer<typeof usernameFormSchema>>({
    resolver: zodResolver(usernameFormSchema),
    defaultValues: {
      username: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    // ✅ This will be type-safe and validated.
    const rawResp = await fetch(
      process.env.NEXT_PUBLIC_SERVER_URL + `/State?gameKey=${values.id}`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      },
    );
    if (rawResp.status == 200) {
      const content = await rawResp.json();

      console.log(content);
      try {
        localStorage.setItem("gameID", values.id);
      } catch {
        console.error("Err adding the game ID to local storage");
      }
      setPlayerSelect(true);
      setPlayerOptions(Object.keys(content.player_character_mapping));
      setPlayerUsernameOptions(content.player_username_mapping);
      setGameId(values.id);
    } else {
      setErr(true);
    }
  }

  async function onSubmitUsername(values: z.infer<typeof usernameFormSchema>) {
    // ✅ This will be type-safe and validated.
    const rawResp = await fetch(
      process.env.NEXT_PUBLIC_SERVER_URL + `/username`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: gameId,
          player: selectedPlayer,
          username: values.username,
        }),
      },
    );
    if (rawResp.status == 200) {
      router.push("/play");
    } else {
      setErr(true);
    }
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] animate-in ease-in-out zoom-in-0 duration-1000">
      {!playerSelect ? (
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start ">
          <div className="flex items-center gap-4">
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-center">
              Enter the game code to join:
            </h1>
          </div>
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="flex flex-col m-auto"
            >
              <FormField
                control={form.control}
                name="id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="m-auto">Game ID</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        onFocus={() => {
                          setErr(false);
                        }}
                      />
                    </FormControl>
                    {err ? (
                      <FormMessage>
                        This server did not find this game ID.
                      </FormMessage>
                    ) : (
                      <FormMessage />
                    )}
                  </FormItem>
                )}
              />
              <Button type="submit" className="m-3">
                Join Game
              </Button>
            </form>
          </Form>
        </main>
      ) : !usernameSet ? (
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start ">
          <div className="self-center font-bold text-xl">
            Who are you playing as?
          </div>
          <div className="flex flex-wrap gap-4 justify-center">
            {playerOptions.map((item) => {
              if (playerUsernameOptions[item] == "") {
                return (
                  <Button
                    key={item}
                    className="basis-1/3"
                    onClick={() => {
                      chosePlayerUnset(item);
                    }}
                  >
                    {item}
                  </Button>
                );
              } else {
                return (
                  <Button
                    key={item}
                    className="basis-1/3"
                    onClick={() => {
                      chosePlayer(item);
                    }}
                  >
                    {playerUsernameOptions[item]}
                  </Button>
                );
              }
            })}
          </div>
        </main>
      ) : (
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start">
          <div className="flex items-center gap-4">
            <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-center">
              What would you like your username to be?
            </h1>
          </div>
          <Form {...usernameForm}>
            <form
              onSubmit={usernameForm.handleSubmit(onSubmitUsername)}
              className="flex flex-col m-auto"
            >
              <FormField
                control={usernameForm.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="m-auto">Username</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        onFocus={() => {
                          setErr(false);
                        }}
                      />
                    </FormControl>
                    {err ? (
                      <FormMessage>
                        This server encountered an error.
                      </FormMessage>
                    ) : (
                      <FormMessage />
                    )}
                  </FormItem>
                )}
              />
              <Button type="submit" className="m-3">
                Join Game
              </Button>
            </form>
          </Form>
        </main>
      )}
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
