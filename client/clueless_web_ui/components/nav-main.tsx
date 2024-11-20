"use client";

import {
  ChevronRight,
  FileStack,
  Logs,
  MessageCircle,
  Send,
  SendToBack,
  Settings,
} from "lucide-react";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";
import { useContext } from "react";
import { GameStateContext } from "@/lib/types";

import { Input } from "./ui/input";

export function NavMain() {
  const gameContext = useContext<any>(GameStateContext); // eslint-disable-line

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Game Info</SidebarGroupLabel>
      <SidebarMenu>
        {/* Player Cards section */}
        <Collapsible asChild>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip={"Your Cards"}>
              <div>
                <FileStack />
                <span className="cursor-default select-none">Your Cards</span>
              </div>
            </SidebarMenuButton>
            {gameContext.gameState[gameContext.player]?.length ? (
              <>
                <CollapsibleTrigger asChild>
                  <SidebarMenuAction className="data-[state=open]:rotate-90">
                    <ChevronRight />
                    <span className="sr-only">Toggle</span>
                  </SidebarMenuAction>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <SidebarMenuSub>
                    {gameContext.gameState[gameContext.player]?.map(
                      (subItem: string) => (
                        <SidebarMenuSubItem key={subItem}>
                          <SidebarMenuSubButton asChild>
                            <span>{subItem}</span>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      ),
                    )}
                  </SidebarMenuSub>
                </CollapsibleContent>
              </>
            ) : null}
          </SidebarMenuItem>
        </Collapsible>

        {/* Game log section */}
        <Collapsible asChild>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip={"Game Log"}>
              <div>
                <Logs />
                <span className="cursor-default select-none">Game Log</span>
              </div>
            </SidebarMenuButton>
            {gameContext.gameState.logs ? (
              <>
                <CollapsibleTrigger asChild>
                  <SidebarMenuAction className="data-[state=open]:rotate-90">
                    <ChevronRight />
                    <span className="sr-only">Toggle</span>
                  </SidebarMenuAction>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <SidebarMenuSub className="max-h-72 overflow-y-auto">
                    {gameContext.gameState.logs?.map((subItem: string) => (
                      <SidebarMenuSubItem key={subItem}>
                        <SidebarMenuSubButton asChild>
                          <span className="block whitespace-pre-wrap break-words w-full h-full">{subItem}</span>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                </CollapsibleContent>
              </>
            ) : null}
          </SidebarMenuItem>
        </Collapsible>

        {/* Game Chat section */}
        <Collapsible asChild>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip={"Your Cards"}>
              <div>
                <MessageCircle />
                <span className="cursor-default select-none">Chat</span>
              </div>
            </SidebarMenuButton>

            <>
              <CollapsibleTrigger asChild>
                <SidebarMenuAction className="data-[state=open]:rotate-90">
                  <ChevronRight />
                  <span className="sr-only">Toggle</span>
                </SidebarMenuAction>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <SidebarMenuSub>
                  {gameContext.gameState.logs?.map((subItem: string) => (
                    <SidebarMenuSubItem key={subItem}>
                      <SidebarMenuSubButton asChild>
                        <span>{subItem}</span>
                      </SidebarMenuSubButton>
                    </SidebarMenuSubItem>
                  ))}
                  {!gameContext.gameState.logs && (
                    <span className="p-4">There are no messages.</span>
                  )}
                </SidebarMenuSub>
                <div className="flex items-center gap-2 px-6">
                  <Input />
                  <Send className="cursor-pointer hover:text-sidebar-primary" />
                </div>
              </CollapsibleContent>
            </>
          </SidebarMenuItem>
        </Collapsible>

        {/* Settings section */}
        <Collapsible asChild>
          <SidebarMenuItem>
            <SidebarMenuButton asChild tooltip={"Your Cards"}>
              <div>
                <Settings />
                <span className="cursor-default select-none">Settings</span>
              </div>
            </SidebarMenuButton>

            <>
              <CollapsibleTrigger asChild>
                <SidebarMenuAction className="data-[state=open]:rotate-90">
                  <ChevronRight />
                  <span className="sr-only">Toggle</span>
                </SidebarMenuAction>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <SidebarMenuSub>
                  <SidebarMenuSubButton asChild>
                    <a href="/join_game">
                      <SendToBack />
                      <span>Change Game</span>
                    </a>
                  </SidebarMenuSubButton>
                </SidebarMenuSub>
              </CollapsibleContent>
            </>
          </SidebarMenuItem>
        </Collapsible>
      </SidebarMenu>
    </SidebarGroup>
  );
}
