"use client";

import { Before, EngineNumber } from "@/components/ResourcePanel";
import type { GameState } from "@/lib/api";
import { useChanged } from "@/lib/useChanged";

// Rangos oficiales (rules_engine.py), solo para dibujar el avance de cada pista.
// El valor mostrado es el que devuelve la API, nunca uno derivado.
// Cada pista con el color de su pista en el tablero (apagado para fondo oscuro);
// el coral queda reservado para accion y cambio.
const TRACKS = [
  { key: "temperature", label: "Temperatura", unit: "°C", min: -30, max: 8, step: 2, fill: "bg-[#e0634f]" },
  { key: "oxygen", label: "Oxígeno", unit: "%", min: 0, max: 14, step: 1, fill: "bg-[#8fc46b]" },
  { key: "oceans_placed", label: "Océanos", unit: "", min: 0, max: 9, step: 1, fill: "bg-[#4f9fe0]" },
  { key: "venus", label: "Venus", unit: "%", min: 0, max: 30, step: 2, fill: "bg-[#d6a35c]" },
] as const;

export const PARTY_LABELS: Record<string, string> = {
  mars_first: "Mars First",
  kelvinists: "Kelvinists",
  reds: "Reds",
  greens: "Greens",
  unity: "Unity",
  scientists: "Scientists",
};

export const humanize = (id: string | null) =>
  id ? id.split("_").map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w)).join(" ") : "—";

/** Una pista como la del tablero: una muesca por paso, las alcanzadas encendidas. */
function Track({ value, min, max, step, fill }: { value: number; min: number; max: number; step: number; fill: string }) {
  const steps = Math.round((max - min) / step);
  const reached = Math.round((value - min) / step);
  return (
    <div className="flex h-2 gap-[3px]" aria-hidden>
      {Array.from({ length: steps }, (_, i) => (
        <span
          key={i}
          className={`flex-1 rounded-[2px] transition-colors duration-200 ${i < reached ? fill : "bg-white/[0.07]"}`}
        />
      ))}
    </div>
  );
}

export default function GlobalParameters({ game }: { game: GameState }) {
  const g = game.global_parameters;
  const t = game.turmoil;
  const before = useChanged(
    { temperature: g.temperature, oxygen: g.oxygen, oceans_placed: g.oceans_placed, venus: g.venus },
    "game",
  );

  return (
    <section aria-label="Partida" className="panel p-5 sm:p-6">
      <div className="grid grid-cols-2 gap-x-6 gap-y-6 md:grid-cols-4">
        {TRACKS.map(({ key, label, unit, min, max, step, fill }) => (
          <div key={key} className="relative space-y-2.5">
            <div className="flex flex-wrap items-baseline justify-between gap-x-2 gap-y-1">
              <span className="label">{label}</span>
              <span className="num whitespace-nowrap text-xl font-semibold tracking-tightish">
                <EngineNumber value={g[key]} changed={before[key] !== undefined} className="" />
                {unit}
                <span className="ml-1 hidden text-xs font-normal text-ink-faint xl:inline">
                  / {max}
                  {unit}
                </span>
              </span>
            </div>
            <Track value={g[key]} min={min} max={max} step={step} fill={fill} />
            {/* Encima de la celda, en el espacio entre filas: no ocupa lugar. */}
            <Before value={before[key]} className="-top-6 right-0" />
          </div>
        ))}
      </div>

      <dl className="mt-6 grid grid-cols-2 gap-x-6 gap-y-3 border-t border-line pt-5 text-sm md:grid-cols-4">
        <div>
          <dt className="text-xs text-ink-faint">Gobierna</dt>
          <dd className="mt-0.5 font-medium">{PARTY_LABELS[t.ruling_party] ?? humanize(t.ruling_party)}</dd>
        </div>
        <div>
          <dt className="text-xs text-ink-faint">Partido dominante</dt>
          <dd className="mt-0.5 font-medium">{t.dominant_party ? PARTY_LABELS[t.dominant_party] ?? humanize(t.dominant_party) : "—"}</dd>
        </div>
        <div>
          <dt className="text-xs text-ink-faint">Global Event actual</dt>
          <dd className="mt-0.5 font-medium">{humanize(t.current_event)}</dd>
        </div>
        <div>
          <dt className="text-xs text-ink-faint">Colonias en juego</dt>
          <dd className="mt-0.5 font-medium">{game.colonies.length ? game.colonies.map(humanize).join(", ") : "—"}</dd>
        </div>
      </dl>
    </section>
  );
}
