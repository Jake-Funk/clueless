"use client";

import {useState } from 'react';

import {
  ChevronRight,
  FileStack,
  Logs,
  MessageCircle,
  SendToBack,
  Settings,
} from "lucide-react";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
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

export const sendMessage = async (gameID, player, message) => {
  const response = await fetch(process.env.NEXT_PUBLIC_SERVER_URL + `/chat`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      key: gameID,
      player: player,
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error('Request failed');
  }

  const data = await response.json();
  return data;  // Return the response data for further processing
};

export function NavMain() {
  const gameContext = useContext<any>(GameStateContext); // eslint-disable-line
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendClick = async () => {
    if (!inputValue) return;  // Prevent sending if input is empty

    setError(null);  // Reset previous errors

    try {
      const response = await sendMessage(gameContext.gameID, gameContext.player, inputValue);  // Use the external send function
      gameContext.setTrigger(gameContext.trigger + 1);
      console.log('Response:', response);
      // Optionally update the UI with the response or handle success.

    } catch (err) {
      setError('Error sending request');
      console.error(err);
    }
  };

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
                          <div className="w-full h-full mb-1">{subItem}</div>
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
            <SidebarMenuButton asChild tooltip={"Game Chat"}>
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
                <SidebarMenuSub className="max-h-72 overflow-y-auto mb-4">
                  {gameContext.gameState.chat?.map((subItem: string) => (
                    <SidebarMenuSubItem key={subItem}>
                      <SidebarMenuSubButton asChild>
                        <div className="w-full h-full mb-1">{subItem}</div>
                      </SidebarMenuSubButton>
                    </SidebarMenuSubItem>
                  ))}
                  {!gameContext.gameState.chat && (
                    <span className="p-4">There are no messages.</span>
                  )}
                </SidebarMenuSub>
                <div className="flex items-center gap-2 px-6 mb-4">
                  <Input 
                    type="text"
                    className="input-class"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        handleSendClick();
                      }
                    }}
                    placeholder="Enter message"
                  />
                  {error && <div className="text-red-500">{error}</div>}
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
