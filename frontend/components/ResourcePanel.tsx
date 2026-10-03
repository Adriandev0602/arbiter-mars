"use client";

import type { PlayerState } from "@/lib/api";

// `production` es el nombre real del campo en PlayerState (ojo: plants -> plant_production).
const RESOURCES = [
  { key: "mc", production: "mc_production", label: "M€", color: "bg-yellow-400" },
  { key: "steel", production: "steel_production", label: "Acero", color: "bg-amber-700" },
  { key: "titanium", production: "titanium_production", label: "Titanio", color: "bg-slate-400" },
  { key: "plants", production: "plant_production", label: "Plantas", color: "bg-green-600" },
  { key: "energy", production: "energy_production", label: "Energía", color: "bg-purple-600" },
  { key: "heat", production: "heat_production", label: "Calor", color: "bg-red-500" },
] as const;

/** Stock y producción de cada recurso, más el Terraform Rating. */
export default function ResourcePanel({ player }: { player: PlayerState }) {
  return (
    <section data-testid="resources" className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="mb-3 flex items-baseline justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Recursos</h2>
        <span className="text-sm text-slate-600">
          Terraform Rating <span data-testid="tr" className="ml-1 text-2xl font-semibold tabular-nums text-slate-900">{player.tr}</span>
        </span>
      </div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {RESOURCES.map(({ key, production: productionKey, label, color }) => {
          const production = player[productionKey];
          return (
            <div key={key} data-testid={`resource-${key}`} className="rounded border border-slate-200 p-3">
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <span className={`inline-block h-2.5 w-2.5 rounded-sm ${color}`} />
                {label}
              </div>
              <div data-testid="stock" className="mt-1 text-2xl font-semibold tabular-nums">{player[key]}</div>
              <div data-testid="production" className="text-xs text-slate-500 tabular-nums">
                producción {production >= 0 ? "+" : ""}
                {production}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
