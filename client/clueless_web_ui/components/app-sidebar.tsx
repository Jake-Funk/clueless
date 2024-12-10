"use client";

import * as React from "react";
import { BookMarked, Copy, GithubIcon, Search } from "lucide-react";

import { NavMain } from "@/components/nav-main";
import { NavSecondary } from "@/components/nav-secondary";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

import { GameStateContext } from "@/lib/types";

import { Button } from "./ui/button";
import { Separator } from "./ui/separator";
import { useToast } from "@/hooks/use-toast";

const navSecondary = [
  {
    title: "Rules",
    url: "#",
    icon: BookMarked,
  },
  {
    title: "Github",
    url: "https://github.com/Jake-Funk/clueless",
    icon: GithubIcon,
  },
];

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { gameID, gameState, player } = React.useContext<any>(GameStateContext); // eslint-disable-line
  const { toast } = useToast();

  return (
    <Sidebar variant="inset" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Search className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Clueless</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
        <div>
          <h3 className="font-bold ">Game ID:</h3>
          <div className="flex items-center gap-2">
            {gameID}
            <Button
              variant="outline"
              size="icon"
              onClick={() => {
                navigator.clipboard.writeText(gameID);
                toast({ description: "Game ID copied to clipboard" });
              }}
            >
              <Copy className="p-1" />
            </Button>
          </div>
        </div>
        <div>
          <div className="font-bold">
            You are:{" "}
            <span className="font-normal">
              {gameState.player_username_mapping[player]}
            </span>
          </div>
          {player && (
            <div>
              playing as{" "}
              <span>{gameState.player_character_mapping[player]}</span>
            </div>
          )}
        </div>
      </SidebarHeader>
      <Separator />
      <SidebarContent>
        <NavMain />
        <NavSecondary items={navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter></SidebarFooter>
    </Sidebar>
  );
}
