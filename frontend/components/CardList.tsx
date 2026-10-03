"use client";

import type { ActiveCard, CardInfo } from "@/lib/api";

const KIND_LABEL: Record<CardInfo["kind"], string> = {
  cards: "Proyecto",
  corporation_cards: "Corporación",
  prelude_cards: "Prelude",
};

/** Lista de cartas por id, con nombre/costo/tags del catálogo que devuelve la API. */
export default function CardList({
  title,
  emptyText,
  ids,
  cards,
  active,
  compact = false,
}: {
  title: string;
  emptyText: string;
  ids: string[];
  cards: Record<string, CardInfo>;
  active?: Record<string, ActiveCard>;
  compact?: boolean;
}) {
  return (
    <section data-testid={`cards-${title}`} className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
        {title} <span data-testid="count" className="font-normal text-slate-400">({ids.length})</span>
      </h2>
      {ids.length === 0 ? (
        <p className="text-sm text-slate-400">{emptyText}</p>
      ) : compact ? (
        <div className="flex flex-wrap gap-1.5">
          {ids.map((id) => (
            <span key={id} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-700">
              {cards[id]?.name ?? id}
            </span>
          ))}
        </div>
      ) : (
        <ul className="divide-y divide-slate-100">
          {ids.map((id) => {
            const card = cards[id];
            const state = active?.[id];
            return (
              <li key={id} className="flex items-start justify-between gap-3 py-2">
                <div className="min-w-0">
                  <div className="truncate text-sm font-medium">{card?.name ?? id}</div>
                  <div className="flex flex-wrap gap-1 pt-0.5">
                    {card && card.kind !== "cards" && (
                      <span className="rounded bg-indigo-50 px-1.5 text-xs text-indigo-700">{KIND_LABEL[card.kind]}</span>
                    )}
                    {card?.is_event && <span className="rounded bg-red-50 px-1.5 text-xs text-red-700">Evento</span>}
                    {(card?.tags ?? []).map((tag) => (
                      <span key={tag} className="rounded bg-slate-100 px-1.5 text-xs text-slate-600">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="shrink-0 text-right text-xs text-slate-500">
                  {card?.cost !== undefined && <div className="text-sm font-semibold text-slate-800">{card.cost} M€</div>}
                  {state && (
                    <>
                      {(state.resources > 0 || state.resource_type) && (
                        <div>
                          {state.resources} {state.resource_type ?? "recursos"}
                        </div>
                      )}
                      <div>{state.action_used ? "acción usada" : "acción disponible"}</div>
                    </>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
