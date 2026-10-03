"use client";

import type { GameState } from "@/lib/api";

// Rangos oficiales (rules_engine.py): solo se usan para dibujar la barra de
// progreso, no para decidir nada del juego.
const PARAMETERS = [
  { key: "temperature", label: "Temperatura", unit: "°C", min: -30, max: 8 },
  { key: "oxygen", label: "Oxígeno", unit: "%", min: 0, max: 14 },
  { key: "oceans_placed", label: "Océanos", unit: "", min: 0, max: 9 },
  { key: "venus", label: "Venus", unit: "%", min: 0, max: 30 },
] as const;

const PARTY_LABELS: Record<string, string> = {
  mars_first: "Mars First",
  kelvinists: "Kelvinists",
  reds: "Reds",
  greens: "Greens",
  unity: "Unity",
  scientists: "Scientists",
};

const humanize = (id: string | null) =>
  id ? id.split("_").map((w) => w[0].toUpperCase() + w.slice(1)).join(" ") : "—";

export default function GlobalParameters({ game }: { game: GameState }) {
  const g = game.global_parameters;
  const t = game.turmoil;

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">Partida</h2>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {PARAMETERS.map(({ key, label, unit, min, max }) => {
          const value = g[key];
          const pct = Math.round(((value - min) / (max - min)) * 100);
          return (
            <div key={key}>
              <div className="flex items-baseline justify-between">
                <span className="text-sm text-slate-600">{label}</span>
                <span className="text-lg font-semibold tabular-nums">
                  {value}
                  {unit}
                </span>
              </div>
              <div className="mt-1 h-1.5 rounded bg-slate-100">
                <div className="h-1.5 rounded bg-orange-500" style={{ width: `${pct}%` }} />
              </div>
              <div className="mt-0.5 text-xs text-slate-400">
                máx. {max}
                {unit}
              </div>
            </div>
          );
        })}
      </div>
      <dl className="mt-4 grid grid-cols-2 gap-x-4 gap-y-1 border-t border-slate-100 pt-3 text-sm md:grid-cols-4">
        <div>
          <dt className="text-xs text-slate-400">Partido gobernante</dt>
          <dd>{PARTY_LABELS[t.ruling_party] ?? t.ruling_party}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-400">Partido dominante</dt>
          <dd>{t.dominant_party ? PARTY_LABELS[t.dominant_party] ?? t.dominant_party : "—"}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-400">Global Event actual</dt>
          <dd>{humanize(t.current_event)}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-400">Colonias en juego</dt>
          <dd>{game.colonies.length ? game.colonies.map(humanize).join(", ") : "—"}</dd>
        </div>
      </dl>
    </section>
  );
}
