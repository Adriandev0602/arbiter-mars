"use client";

import { useEffect, useState } from "react";
import { ChevronDown, Plus } from "lucide-react";
import { createPlayer, listPlayers, type PlayerSummary } from "@/lib/api";

/** Elegir un jugador existente o crear uno nuevo (TR 20, valores iniciales del schema). */
export default function PlayerPicker({
  playerId,
  onSelect,
  version = 0,
}: {
  playerId: string | null;
  onSelect: (id: string | null) => void;
  /** Se incrementa cuando otro lugar de la UI crea un jugador, para recargar la lista. */
  version?: number;
}) {
  const [players, setPlayers] = useState<PlayerSummary[]>([]);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listPlayers()
      .then((list) => {
        setPlayers(list);
        // Si el jugador recordado ya no existe, se olvida.
        if (playerId && !list.some((p) => p.id === playerId)) onSelect(null);
      })
      .catch(() => setPlayers([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [version]);

  async function handleCreate() {
    if (!name.trim()) return;
    setError(null);
    try {
      const player = await createPlayer(name);
      setPlayers((prev) => [...prev, player]);
      setName("");
      setCreating(false);
      onSelect(player.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo crear");
    }
  }

  if (creating) {
    return (
      <form
        className="flex flex-wrap items-center gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          handleCreate();
        }}
      >
        <input
          autoFocus
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Escape" && setCreating(false)}
          placeholder="Nombre del jugador"
          aria-label="Nombre del jugador"
          className="field w-44 py-2"
        />
        <button type="submit" className="btn-primary px-4 py-2" disabled={!name.trim()}>
          Crear
        </button>
        <button type="button" onClick={() => setCreating(false)} className="px-2 py-2 text-sm text-ink-muted hover:text-ink">
          Cancelar
        </button>
        {error && <span className="w-full text-xs text-bad">{error}</span>}
      </form>
    );
  }

  return (
    <div className="flex min-w-0 flex-1 items-center gap-2 sm:flex-none">
      <label htmlFor="player" className="sr-only">
        Jugador
      </label>
      <div className="relative min-w-0 flex-1 sm:flex-none">
        <select
          id="player"
          value={playerId ?? ""}
          onChange={(e) => onSelect(e.target.value || null)}
          className="field w-full appearance-none py-2 pr-9 sm:w-56"
        >
          <option value="">Elegí un jugador</option>
          {players.map((p) => (
            <option key={p.id} value={p.id}>
              {p.display_name} · TR {p.tr}
            </option>
          ))}
        </select>
        <ChevronDown size={16} className="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-ink-faint" />
      </div>
      <button onClick={() => setCreating(true)} className="btn-quiet py-2" aria-label="Nuevo jugador">
        <Plus size={16} />
        <span className="hidden sm:inline">Nuevo</span>
      </button>
    </div>
  );
}
