"use client";

import type { PlayerState } from "@/lib/api";
import { useChanged } from "@/lib/useChanged";

// `production` es el nombre real del campo en PlayerState (ojo: plants -> plant_production).
const RESOURCES = [
  { key: "mc", production: "mc_production", label: "M€", dot: "bg-res-mc" },
  { key: "steel", production: "steel_production", label: "Acero", dot: "bg-res-steel" },
  { key: "titanium", production: "titanium_production", label: "Titanio", dot: "bg-res-titanium" },
  { key: "plants", production: "plant_production", label: "Plantas", dot: "bg-res-plants" },
  { key: "energy", production: "energy_production", label: "Energía", dot: "bg-res-energy" },
  { key: "heat", production: "heat_production", label: "Calor", dot: "bg-res-heat" },
] as const;

/**
 * "antes X" superpuesto en la esquina superior derecha de su celda (el padre es
 * `relative`): aparecer o irse no ocupa lugar ni mueve el layout.
 */
export function Before({ value, className = "right-3 top-3" }: { value: number | undefined; className?: string }) {
  if (value === undefined) return null;
  return (
    <span
      className={`num pointer-events-none absolute animate-delta-in whitespace-nowrap rounded-full bg-coral/15 px-2 py-0.5 text-[11px] font-medium leading-4 text-coral-bright ${className}`}
    >
      antes {value}
    </span>
  );
}

/** Un numero del motor. Se re-monta cuando cambia su valor, asi el pulso arranca con cada cambio. */
export function EngineNumber({
  value,
  changed,
  className,
  testId,
}: {
  value: number;
  changed: boolean;
  className: string;
  testId?: string;
}) {
  return (
    <span key={value} data-testid={testId} className={`num ${className} ${changed ? "animate-value-pulse" : ""}`}>
      {value}
    </span>
  );
}

function Production({ value, previous }: { value: number; previous?: number }) {
  const signed = (n: number) => `${n >= 0 ? "+" : ""}${n}`;
  return (
    <span data-testid="production" className="num inline-flex flex-wrap items-center gap-x-1.5 text-[13px] text-ink-muted">
      <span key={value} className={previous !== undefined ? "animate-value-pulse" : undefined}>
        producción {signed(value)}
      </span>
      {previous !== undefined && <span className="animate-delta-in text-[11px] text-coral-bright">(antes {signed(previous)})</span>}
    </span>
  );
}

/**
 * El libro de cuentas del jugador: TR y M€ al frente, los otros cinco recursos al lado.
 * Todo numero sale tal cual de la API; lo que acaba de cambiar se marca en coral.
 */
export default function ResourcePanel({ player, playerId }: { player: PlayerState; playerId: string }) {
  const values: Record<string, number> = { tr: player.tr };
  for (const r of RESOURCES) {
    values[r.key] = player[r.key];
    values[r.production] = player[r.production];
  }
  const before = useChanged(values, playerId);
  const [mc, ...rest] = RESOURCES;

  return (
    <section data-testid="resources" aria-label="Recursos" className="panel overflow-hidden">
      <div className="grid gap-px bg-line lg:grid-cols-[minmax(0,1.15fr)_minmax(0,2fr)]">
        <div className="grid grid-cols-2 gap-px bg-line">
          <div className="relative flex flex-col justify-between gap-6 bg-surface p-5 sm:p-6">
            <span className="label">Terraform Rating</span>
            {/* Debajo del numero, en la misma linea que "producción" de M€: la fila ya mide eso. */}
            <div className="space-y-2">
              <EngineNumber
                testId="tr"
                value={player.tr}
                changed={before.tr !== undefined}
                className="block text-6xl font-semibold leading-none tracking-display sm:text-7xl"
              />
              <div className="relative h-5">
                <Before value={before.tr} className="left-0 top-0" />
              </div>
            </div>
          </div>

          <div data-testid={`resource-${mc.key}`} className="relative flex flex-col justify-between gap-6 bg-surface p-5 sm:p-6">
            <span className="label flex items-center gap-2">
              <span className={`h-2.5 w-2.5 rounded-full ${mc.dot}`} />
              {mc.label}
            </span>
            <div className="space-y-2">
              <EngineNumber
                testId="stock"
                value={player.mc}
                changed={before.mc !== undefined}
                className="block text-6xl font-semibold leading-none tracking-display text-res-mc sm:text-7xl"
              />
              <Before value={before.mc} className="right-4 top-4" />
              <Production value={player.mc_production} previous={before.mc_production} />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-px bg-line sm:grid-cols-5">
          {rest.map(({ key, production, label, dot }, i) => (
            <div
              key={key}
              data-testid={`resource-${key}`}
              className={`relative flex flex-col justify-between gap-5 bg-surface p-4 sm:p-5 ${i === rest.length - 1 ? "col-span-2 sm:col-span-1" : ""}`}
            >
              <span className="label flex items-center gap-2">
                <span className={`h-2 w-2 rounded-full ${dot}`} />
                {label}
              </span>
              <div className="space-y-1.5">
                <EngineNumber
                  testId="stock"
                  value={player[key]}
                  changed={before[key] !== undefined}
                  className="block text-4xl font-semibold leading-none tracking-display"
                />
                <Before value={before[key]} />
                <Production value={player[production]} previous={before[production]} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
