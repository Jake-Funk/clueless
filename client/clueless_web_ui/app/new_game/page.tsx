"use client";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { BookMarked, Github, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

const formSchema = z.object({
  numPlayers: z.coerce
    .number()
    .min(2, { message: "You need at least 2 people to play" })
    .max(6, { message: "You can only play with up to 6 players." }),
  username: z.coerce
    .string()
    .min(1, { message: "Must have at least 1 character for your username" })
    .max(20, { message: "Must be 20 or fewer characters long" }),
});

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      numPlayers: 2,
      username: "Player1",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    // ✅ This will be type-safe and validated.
    const rawResp = await fetch(
      process.env.NEXT_PUBLIC_SERVER_URL + "/new_game",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ num_players: values.numPlayers }),
      },
    );
    const content = await rawResp.json();

    if (rawResp.status == 200) {
      console.log(content);
      try {
        localStorage.setItem("gameID", content);
        localStorage.setItem("player", "player1");
      } catch {
        console.error("Err adding the game ID to local storage");
      } finally {
        const rawUsernameResp = await fetch(
          process.env.NEXT_PUBLIC_SERVER_URL + `/username`,
          {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              game_id: content,
              player: "player1",
              username: values.username,
            }),
          },
        );
        if (rawUsernameResp.status == 200) {
          router.push("/play");
        } else {
          console.error("A problem has occurred");
        }
        router.push("/play");
      }
    }

    setIsLoading(false);
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] animate-in ease-in-out zoom-in-0 duration-1000">
      <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start ">
        <div className="flex items-center gap-4">
          <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-4xl text-center">
            Tell us how many people are playing, and what you want your username
            to be.
          </h1>
        </div>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex flex-col m-auto"
          >
            <FormField
              control={form.control}
              name="numPlayers"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="m-auto">Number of Players</FormLabel>
                  <FormControl>
                    <Input {...field} type="number" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="m-auto">Username</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            {isLoading ? (
              <Loader2 className="animate-spin self-center m-4" />
            ) : (
              <Button type="submit" className="m-3">
                Start Game
              </Button>
            )}
          </form>
        </Form>
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
