"use client";

import { useEffect, useState } from "react";
import { createPlayer, listPlayers, type PlayerSummary } from "@/lib/api";

/** Elegir un jugador existente o crear uno nuevo (TR 20, valores iniciales del schema). */
export default function PlayerPicker({
  playerId,
  onSelect,
}: {
  playerId: string | null;
  onSelect: (id: string | null) => void;
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
  }, []);

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
      <div className="flex items-center gap-2">
        <input
          autoFocus
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleCreate();
            if (e.key === "Escape") setCreating(false);
          }}
          placeholder="Nombre del jugador"
          className="w-44 rounded border border-slate-300 px-2 py-1.5 text-sm"
        />
        <button onClick={handleCreate} className="rounded bg-slate-900 px-3 py-1.5 text-sm text-white hover:bg-slate-700">
          Crear
        </button>
        <button onClick={() => setCreating(false)} className="px-2 py-1.5 text-sm text-slate-500 hover:text-slate-800">
          Cancelar
        </button>
        {error && <span className="text-xs text-red-600">{error}</span>}
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <label htmlFor="player" className="text-sm text-slate-500">
        Jugador
      </label>
      <select
        id="player"
        value={playerId ?? ""}
        onChange={(e) => onSelect(e.target.value || null)}
        className="w-40 rounded border border-slate-300 sm:w-48 bg-white px-2 py-1.5 text-sm"
      >
        <option value="">— Elegir —</option>
        {players.map((p) => (
          <option key={p.id} value={p.id}>
            {p.display_name} (TR {p.tr})
          </option>
        ))}
      </select>
      <button
        onClick={() => setCreating(true)}
        className="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm hover:bg-slate-100"
      >
        Nuevo
      </button>
    </div>
  );
}
