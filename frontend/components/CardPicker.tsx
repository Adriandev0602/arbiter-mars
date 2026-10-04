"use client";

import { Check } from "lucide-react";
import type { CardInfo } from "@/lib/api";
import { Tags } from "@/components/CardList";

/** Lista de cartas seleccionables (comprar en la investigacion, quedarse preludes). */
export default function CardPicker({
  ids,
  cards,
  selected,
  onToggle,
  maxSelected,
}: {
  ids: string[];
  cards: Record<string, CardInfo>;
  selected: string[];
  onToggle: (id: string) => void;
  maxSelected?: number;
}) {
  const full = maxSelected !== undefined && selected.length >= maxSelected;
  return (
    <ul className="grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-2 sm:[&>li:last-child:nth-child(odd)]:col-span-2">
      {ids.map((id) => {
        const card = cards[id];
        const on = selected.includes(id);
        const disabled = !on && full;
        return (
          <li key={id} className="bg-surface">
            <button
              type="button"
              aria-pressed={on}
              disabled={disabled}
              onClick={() => onToggle(id)}
              className={`flex h-full w-full items-start justify-between gap-3 px-4 py-3.5 text-left transition-colors duration-200 ${
                on ? "bg-coral/[0.09]" : "hover:bg-white/[0.03] disabled:opacity-40 disabled:hover:bg-transparent"
              }`}
            >
              <span className="min-w-0 space-y-1.5">
                <span className="block truncate text-[15px] font-medium tracking-tightish">{card?.name ?? id}</span>
                <Tags tags={card?.tags ?? []} />
              </span>
              <span className="flex shrink-0 items-center gap-2">
                {card?.cost !== undefined && <span className="num text-sm font-semibold text-res-mc">{card.cost} M€</span>}
                <span
                  className={`grid h-5 w-5 place-items-center rounded-full border transition-colors duration-200 ${
                    on ? "border-coral bg-coral text-coral-ink" : "border-line-strong"
                  }`}
                >
                  {on && <Check size={13} strokeWidth={3} />}
                </span>
              </span>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
