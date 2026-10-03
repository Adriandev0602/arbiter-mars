"use client";

import { useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import Dashboard from "@/components/Dashboard";
import PlayerPicker from "@/components/PlayerPicker";
import { setupStep } from "@/components/SetupFlow";
import SidebarChat from "@/components/SidebarChat";
import { getGame, getPlayerState, type GameState, type StateResponse } from "@/lib/api";

const PLAYER_KEY = "arbiter.playerId";
const skipKey = (id: string) => `arbiter.skipPreludes.${id}`;

function readStorage(key: string): string | null {
  try {
    return localStorage.getItem(key);
  } catch {
    return null; // storage bloqueado: se trabaja sin recordar
  }
}

function writeStorage(key: string, value: string | null) {
  try {
    if (value === null) localStorage.removeItem(key);
    else localStorage.setItem(key, value);
  } catch {
    // idem
  }
}

/**
 * Dashboard a la izquierda, chat con el árbitro a la derecha (debajo en
 * pantallas chicas). El jugador elegido se recuerda en el navegador o se
 * abre directo con ?player=<id>; el estado se vuelve a pedir a la API
 * después de cada respuesta del chat y de cada paso del setup.
 */
export default function Home() {
  const [playerId, setPlayerId] = useState<string | null>(null);
  const [state, setState] = useState<StateResponse | null>(null);
  const [game, setGame] = useState<GameState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [skipPreludes, setSkipPreludes] = useState(false);
  const [playersVersion, setPlayersVersion] = useState(0);

  useEffect(() => {
    const fromUrl = new URLSearchParams(window.location.search).get("player");
    setPlayerId(fromUrl ?? readStorage(PLAYER_KEY));
  }, []);

  useEffect(() => {
    setSkipPreludes(playerId ? readStorage(skipKey(playerId)) === "1" : false);
  }, [playerId]);

  const selectPlayer = (id: string | null) => {
    setPlayerId(id);
    setState(null);
    writeStorage(PLAYER_KEY, id);
  };

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [gameRes, stateRes] = await Promise.all([getGame(), playerId ? getPlayerState(playerId) : Promise.resolve(null)]);
      setGame(gameRes);
      setState(stateRes);
      setPlayersVersion((v) => v + 1); // el TR del selector tambien sale de la API
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  }, [playerId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const onState = (s: StateResponse) => {
    setState(s);
    getGame().then(setGame).catch(() => undefined);
  };

  const step = state ? setupStep(state, skipPreludes) : null;

  return (
    <div className="flex min-h-screen flex-col lg:h-screen">
      <header className="sticky top-0 z-30 flex items-center justify-between gap-3 border-b border-line bg-ground/90 px-4 py-2.5 backdrop-blur sm:px-6 sm:py-3">
        <h1 className="flex shrink-0 items-baseline gap-2">
          <span className="text-lg font-semibold tracking-display">Árbitro</span>
          <span className="sr-only text-sm text-ink-muted sm:not-sr-only">de Terraforming Mars</span>
        </h1>
        <div className="flex min-w-0 flex-1 items-center justify-end gap-2">
          <PlayerPicker playerId={playerId} onSelect={selectPlayer} version={playersVersion} />
          <button onClick={refresh} disabled={loading} aria-label="Actualizar" className="btn-quiet h-10 w-10 px-0 py-0">
            <RefreshCw size={16} className={loading ? "animate-spin" : undefined} />
          </button>
        </div>
      </header>

      <main className="flex flex-1 flex-col pb-[68px] lg:min-h-0 lg:flex-row lg:pb-0">
        <section className="min-w-0 flex-1 p-4 sm:p-6 lg:overflow-y-auto">
          {error && (
            <p role="alert" className="mx-auto mb-6 max-w-6xl rounded-xl border border-bad/30 bg-bad/10 px-4 py-3 text-sm text-bad">
              No se pudo cargar el estado: {error}. Revisá que el backend esté corriendo en{" "}
              {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}.
            </p>
          )}
          <Dashboard
            game={game}
            state={state}
            playerId={playerId}
            step={step}
            onState={onState}
            onCreated={(id) => {
              setPlayersVersion((v) => v + 1);
              selectPlayer(id);
            }}
            onSkipPreludes={() => {
              if (playerId) writeStorage(skipKey(playerId), "1");
              setSkipPreludes(true);
            }}
          />
        </section>
        <aside className="flex w-full shrink-0 flex-col border-t border-line bg-surface lg:w-[400px] lg:border-l lg:border-t-0">
          <SidebarChat playerId={playerId} onReply={refresh} />
        </aside>
      </main>
    </div>
  );
}
