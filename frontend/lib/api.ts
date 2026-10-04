/**
 * Cliente delgado hacia el backend. Centraliza la URL base y el manejo de
 * errores para no repetir fetch() sueltos por los componentes. Ningun numero
 * se calcula aca: todo sale tal cual de la API.
 */
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type PlayerSummary = {
  id: string;
  display_name: string;
  tr: number;
  created_at: string;
};

export type ActiveCard = {
  resources: number;
  action_used: boolean;
  resource_type?: string | null;
};

/** Forma de rules_engine.PlayerState (solo las claves que pinta el dashboard). */
export type PlayerState = {
  tr: number;
  mc: number;
  steel: number;
  titanium: number;
  plants: number;
  energy: number;
  heat: number;
  mc_production: number;
  steel_production: number;
  titanium_production: number;
  plant_production: number;
  energy_production: number;
  heat_production: number;
  hand: string[];
  deck: string[];
  played_cards: string[];
  active_cards: Record<string, ActiveCard>;
  tags_played: Record<string, number>;
  pending_research: string[];
  pending_prelude_choice: string[];
  prelude_hand: string[];
  pending_corporation_first_action: { corporation_id: string; type: string } | null;
  [key: string]: unknown;
};

export type CardInfo = {
  id: string;
  name: string;
  tags: string[];
  kind: "cards" | "corporation_cards" | "prelude_cards";
  cost?: number;
  is_event?: boolean;
};

export type StateResponse = {
  player: PlayerState;
  cards: Record<string, CardInfo>;
  /** Corporacion elegida, o null si el jugador todavia no la eligio. */
  corporation: CardInfo | null;
  /** Precio por carta que el MOTOR le cobra a este jugador (3, 5 con Polyphemos, 1 con TerraLabs). */
  research_cost_per_card: number;
};

export type Corporation = {
  id: string;
  name: string;
  expansion: string;
  starting_mc: number;
  tags: string[];
};

export type GameState = {
  global_parameters: {
    temperature: number;
    oxygen: number;
    oceans_placed: number;
    venus: number;
    city_tiles_placed: number;
  };
  turmoil: {
    ruling_party: string;
    dominant_party: string | null;
    chairman: string | null;
    current_event: string | null;
    coming_event: string | null;
    distant_event: string | null;
  };
  colonies: string[];
};

export type HexBonus = { resource: "steel" | "titanium" | "plant" | "card"; amount: number };

export type HexTile = {
  tile_type: "city" | "greenery" | "ocean" | "special" | "nomad" | "community";
  owner: string | null;
  bonus_consumed: boolean;
  card: string | null;
  cathedral?: boolean;
};

/** Un hexagono del mapa Tharsis: definicion fija + tile actual + legalidad segun el motor. */
export type Hex = {
  id: string;
  row: number;
  x: number;
  hex_type: "land" | "ocean";
  volcanic: boolean;
  volcano_name: string | null;
  reserved_city: string | null;
  bonus: HexBonus[];
  bonus_available: HexBonus[];
  tile: HexTile | null;
  can_place_ocean: boolean;
  can_place_city: boolean;
  can_place_greenery: boolean;
};

export type BoardState = { hexes: Hex[]; owners: Record<string, string> };

export type PlaceAction = "city" | "greenery" | "aquifer" | "plants_to_greenery";

export type ChatResponse = {
  reply: string;
  updated_state: PlayerState | null;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    let detail = `${res.status}`;
    try {
      const body = await res.json();
      if (body?.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      // cuerpo no-JSON: nos quedamos con el status
    }
    throw new Error(detail);
  }
  return res.json();
}

export const listPlayers = () => request<PlayerSummary[]>("/players");

export const createPlayer = (displayName: string) =>
  request<PlayerSummary>("/players", { method: "POST", body: JSON.stringify({ display_name: displayName }) });

export const getPlayerState = (playerId: string) => request<StateResponse>(`/state/${playerId}`);

export const getGame = () => request<GameState>("/game");

export const listCorporations = () => request<Corporation[]>("/corporations");

const post = <T,>(path: string, body?: unknown) =>
  request<T>(path, { method: "POST", body: body === undefined ? undefined : JSON.stringify(body) });

export const chooseCorporation = (playerId: string, corporationId: string) =>
  post<StateResponse>(`/players/${playerId}/corporation`, { corporation_id: corporationId });

export const dealStartingHand = (playerId: string, buy: boolean) =>
  post<StateResponse>(`/players/${playerId}/starting-hand`, { buy });

export const buyResearch = (playerId: string, cardIds: string[]) =>
  post<StateResponse>(`/players/${playerId}/research`, { card_ids: cardIds });

export const dealPreludes = (playerId: string) => post<StateResponse>(`/players/${playerId}/preludes/deal`);

export const keepPreludes = (playerId: string, preludeIds: string[]) =>
  post<StateResponse>(`/players/${playerId}/preludes/keep`, { prelude_ids: preludeIds });

export const playPrelude = (playerId: string, preludeId: string) =>
  post<StateResponse>(`/players/${playerId}/preludes/${preludeId}/play`);

export const getBoard = (playerId: string | null) =>
  request<BoardState>(`/board${playerId ? `?player_id=${encodeURIComponent(playerId)}` : ""}`);

export const placeTile = (playerId: string, action: PlaceAction, hexId: string) =>
  post<StateResponse>(`/players/${playerId}/place`, { action, hex_id: hexId });

export const sendChatMessage = (playerId: string, message: string) =>
  request<ChatResponse>("/chat", { method: "POST", body: JSON.stringify({ player_id: playerId, message }) });
