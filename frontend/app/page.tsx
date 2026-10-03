"use client";

import { useCallback, useEffect, useState } from "react";
import Dashboard from "@/components/Dashboard";
import PlayerPicker from "@/components/PlayerPicker";
import SidebarChat from "@/components/SidebarChat";
import { getGame, getPlayerState, type GameState, type StateResponse } from "@/lib/api";

const PLAYER_KEY = "arbiter.playerId";

/**
 * Layout de dos columnas: dashboard con el estado del jugador a la izquierda
 * y chat con el arbitro a la derecha. El jugador elegido se recuerda en el
 * navegador (localStorage); el estado se vuelve a pedir a la API despues de
 * cada respuesta del chat.
 */
export default function Home() {
  const [playerId, setPlayerId] = useState<string | null>(null);
  const [state, setState] = useState<StateResponse | null>(null);
  const [game, setGame] = useState<GameState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // ?player=<id> en la URL tiene prioridad (sirve para abrir un jugador directo).
    const fromUrl = new URLSearchParams(window.location.search).get("player");
    if (fromUrl) {
      setPlayerId(fromUrl);
      return;
    }
    try {
      setPlayerId(localStorage.getItem(PLAYER_KEY));
    } catch {
      // storage bloqueado: se elige jugador en cada visita
    }
  }, []);

  const selectPlayer = (id: string | null) => {
    setPlayerId(id);
    setState(null);
    try {
      if (id) localStorage.setItem(PLAYER_KEY, id);
      else localStorage.removeItem(PLAYER_KEY);
    } catch {
      // idem
    }
  };

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [gameRes, stateRes] = await Promise.all([
        getGame(),
        playerId ? getPlayerState(playerId) : Promise.resolve(null),
      ]);
      setGame(gameRes);
      setState(stateRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }, [playerId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 text-slate-900 lg:h-screen">
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-white px-4 py-3 sm:px-6">
        <div>
          <h1 className="text-lg font-semibold">Árbitro de Terraforming Mars</h1>
          <p className="text-xs text-slate-500">Los cálculos los hace el motor de reglas, no el modelo.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2 sm:gap-3">
          <PlayerPicker playerId={playerId} onSelect={selectPlayer} />
          <button
            onClick={refresh}
            disabled={loading}
            className="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-100 disabled:opacity-50"
          >
            {loading ? "Actualizando…" : "Actualizar"}
          </button>
        </div>
      </header>

      <main className="flex flex-1 flex-col lg:min-h-0 lg:flex-row">
        <section className="min-w-0 flex-1 p-4 sm:p-6 lg:overflow-y-auto">
          {error && (
            <div className="mb-4 rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
              No se pudo cargar el estado: {error}. ¿Está corriendo el backend en {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}?
            </div>
          )}
          <Dashboard game={game} state={state} hasPlayer={Boolean(playerId)} />
        </section>
        <aside className="flex h-[80vh] w-full shrink-0 flex-col border-t border-slate-200 bg-white lg:h-auto lg:w-96 lg:border-l lg:border-t-0">
          <SidebarChat playerId={playerId} onReply={refresh} />
        </aside>
      </main>
    </div>
  );
}
