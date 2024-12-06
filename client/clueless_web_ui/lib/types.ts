import { createContext, Dispatch, SetStateAction } from "react";

export const defaultGameState = {
  game_phase: {
    player: "",
    phase: "",
  },
  victory_state: 0,
  player_character_mapping: {},
  moved_by_suggest: {},
  map: {
    study: [],
    hall: [],
    lounge: [],
    library: [],
    billiard: [],
    dining: [],
    conservatory: [],
    ballroom: [],
    kitchen: [],
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
  },
};

export interface gsObj {
  game_phase: {
    player: string;
    phase: string;
  };
  victory_state: number;
  player_character_mapping: {
    [key: string]: string;
  };
  moved_by_suggest: {
    [key: string]: boolean;
  };
  map: {
    [key: string | number]: string[] | string;
  };
}

export interface gsContext {
  gameState: gsObj;
  player: string;
  gameID: string;
  trigger: number;
  setTrigger: Dispatch<SetStateAction<number>>;
}

export const GameStateContext = createContext<gsContext>({
  gameState: defaultGameState,
  player: "",
  gameID: "",
  trigger: 0,
  setTrigger: () => {},
});
