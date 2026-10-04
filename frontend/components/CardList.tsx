"use client";

import { useState } from "react";
import type { ActiveCard, CardInfo } from "@/lib/api";

const TAG_DOT: Record<string, string> = {
  building: "bg-res-steel",
  space: "bg-[#2d2b40] ring-1 ring-[#f2c14e]",
  science: "bg-ink",
  power: "bg-res-energy",
  earth: "bg-[#3f8fd6]",
  jovian: "bg-[#e0a466]",
  venus: "bg-[#5aa9e6]",
  plant: "bg-res-plants",
  microbe: "bg-[#9bc93f]",
  animal: "bg-[#5d8f3a]",
  city: "bg-ink-faint",
  wild: "bg-coral",
};

const KIND_LABEL: Record<CardInfo["kind"], string> = {
  cards: "Proyecto",
  corporation_cards: "Corporación",
  prelude_cards: "Prelude",
};

export function Tags({ tags }: { tags: string[] }) {
  if (!tags.length) return <span className="text-xs text-ink-faint">sin tags</span>;
  return (
    <span className="flex flex-wrap gap-x-3 gap-y-1">
      {tags.map((tag, i) => (
        <span key={`${tag}-${i}`} className="inline-flex items-center gap-1.5 text-xs text-ink-muted">
          <span className={`h-2 w-2 rounded-full ${TAG_DOT[tag] ?? "bg-ink-faint"}`} />
          {tag}
        </span>
      ))}
    </span>
  );
}

function CardRow({ id, card, state }: { id: string; card?: CardInfo; state?: ActiveCard }) {
  return (
    <li className="flex items-start justify-between gap-4 py-3">
      <div className="min-w-0 space-y-1.5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="truncate text-[15px] font-medium tracking-tightish">{card?.name ?? id}</span>
          {card && card.kind !== "cards" && (
            <span className="rounded-full border border-line-strong px-2 py-px text-[11px] text-ink-muted">{KIND_LABEL[card.kind]}</span>
          )}
          {card?.is_event && <span className="rounded-full bg-bad/15 px-2 py-px text-[11px] text-bad">Evento</span>}
        </div>
        <Tags tags={card?.tags ?? []} />
      </div>
      <div className="shrink-0 space-y-1 text-right">
        {card?.cost !== undefined && (
          <div className="num rounded-full bg-res-mc/10 px-2.5 py-0.5 text-sm font-semibold text-res-mc">{card.cost} M€</div>
        )}
        {state && (
          <>
            {(state.resources > 0 || state.resource_type) && (
              <div className="num text-xs text-ink-muted">
                {state.resources} {state.resource_type ?? "recursos"}
              </div>
            )}
            <div className={`text-xs ${state.action_used ? "text-ink-faint" : "text-good"}`}>
              {state.action_used ? "acción usada" : "acción disponible"}
            </div>
          </>
        )}
      </div>
    </li>
  );
}

type Tab = { title: string; ids: string[]; empty: string; active?: Record<string, ActiveCard> };

/** Mano, cartas activas y jugadas en pestañas: una lista larga a la vez, no tres paneles. */
export default function CardTabs({ tabs, cards }: { tabs: Tab[]; cards: Record<string, CardInfo> }) {
  const [current, setCurrent] = useState(0);
  const tab = tabs[current];

  return (
    <section className="panel" aria-label="Cartas">
      <div role="tablist" className="flex gap-1 border-b border-line px-3 pt-3">
        {tabs.map((t, i) => (
          <button
            key={t.title}
            role="tab"
            aria-selected={i === current}
            data-testid={`cards-${t.title}`}
            onClick={() => setCurrent(i)}
            className={`relative rounded-t-lg px-3.5 pb-3 pt-1.5 text-sm font-medium transition-colors duration-200 ${
              i === current ? "text-ink" : "text-ink-faint hover:text-ink-muted"
            }`}
          >
            {t.title}{" "}
            <span data-testid="count" className="num font-normal text-ink-faint">
              ({t.ids.length})
            </span>
            {i === current && <span className="absolute inset-x-3 -bottom-px h-0.5 rounded-full bg-coral" />}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="px-5 sm:px-6">
        {tab.ids.length === 0 ? (
          <p className="py-8 text-sm text-ink-faint">{tab.empty}</p>
        ) : (
          <ul className="divide-y divide-line">
            {tab.ids.map((id, i) => (
              <CardRow key={`${id}-${i}`} id={id} card={cards[id]} state={tab.active?.[id]} />
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
