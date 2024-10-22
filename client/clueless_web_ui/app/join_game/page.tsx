"use client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { BookMarked, Github } from "lucide-react"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useState } from "react"

const formSchema = z.object({
  id: z.coerce.string().uuid("Not a valid game ID"),
})

export default function Home() {
  const router = useRouter()
  const [err, setErr] = useState(false)
  const [playerSelect, setPlayerSelect] = useState(false)
  const [playerOptions, setPlayerOptions] = useState<string[]>([])

  function chosePlayer(player: string) {
    try {
      localStorage.setItem("player", player)
    } catch {
      console.error("Problem adding data to local storage")
    }
    router.push("/play")
  }

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      id: "",
    },
  })

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
      }
    )
    if (rawResp.status == 200) {
      const content = await rawResp.json()

      console.log(content)
      try {
        localStorage.setItem("gameID", values.id)
        setPlayerSelect(true)
        setPlayerOptions(Object.keys(content.player_character_mapping))
      } catch {
        console.error("Err adding the game ID to local storage")
      }
    } else {
      setErr(true)
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
                          setErr(false)
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
      ) : (
        <main className="flex flex-col gap-8 row-start-2 items-center justify-center sm:items-start ">
          <div className="self-center font-bold text-xl">
            Who are you playing as?
          </div>
          <div className="flex flex-wrap gap-4 justify-center">
            {playerOptions.map((item) => {
              return (
                <Button
                  key={item}
                  className="basis-1/3"
                  onClick={() => {chosePlayer(item)}}
                >
                  {item}
                </Button>
              )
            })}
          </div>
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
