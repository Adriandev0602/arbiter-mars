"use client";

import { useState } from "react";
import { LoaderCircle, MessageSquare, Play } from "lucide-react";
import CardPicker from "@/components/CardPicker";
import { Tags } from "@/components/CardList";
import { humanize } from "@/components/GlobalParameters";
import { buyResearch, playPrelude, type StateResponse } from "@/lib/api";

const FIRST_ACTION_TEXT: Record<string, string> = {
  place_greenery: "colocar un greenery y subir el oxígeno 1 paso",
  place_city: "colocar una ciudad",
  add_colony_tile: "agregar una colonia al juego",
  build_colony: "construir una colonia",
  place_community: "colocar una comunidad",
  reveal_preludes: "revelar 3 Preludes y jugar 1",
  reveal_until_matching: "revelar cartas hasta encontrar 2 con floaters",
};

/**
 * Lo que el jugador tiene pendiente de resolver: preludes por jugar, una
 * investigacion abierta y la primera accion de su corporacion. Las que piden
 * elegir un hexagono o una opcion se derivan al chat, donde el arbitro pregunta.
 */
export default function PendingActions({
  playerId,
  state,
  onState,
}: {
  playerId: string;
  state: StateResponse;
  onState: (s: StateResponse) => void;
}) {
  const p = state.player;
  const [busy, setBusy] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [selected, setSelected] = useState<string[]>([]);

  const act = async (key: string, fn: () => Promise<StateResponse>) => {
    setBusy(key);
    setErrors((e) => ({ ...e, [key]: "" }));
    try {
      onState(await fn());
      setSelected([]);
    } catch (err) {
      setErrors((e) => ({ ...e, [key]: err instanceof Error ? err.message : "No se pudo completar" }));
    } finally {
      setBusy(null);
    }
  };

  const firstAction = p.pending_corporation_first_action;
  const items = [p.prelude_hand.length > 0, p.pending_research.length > 0, Boolean(firstAction)].filter(Boolean).length;
  if (items === 0) return null;

  return (
    <section className="panel space-y-6 p-5 sm:p-6" aria-label="Pendiente">
      <h2 className="text-lg font-semibold tracking-tightish">Tenés cosas por resolver</h2>

      {firstAction && (
        <div className="flex flex-wrap items-center justify-between gap-3 border-y border-line py-3">
          <p className="text-sm">
            Primera acción de <span className="font-medium">{humanize(firstAction.corporation_id)}</span>:{" "}
            {FIRST_ACTION_TEXT[firstAction.type] ?? humanize(firstAction.type)}.
          </p>
          <span className="inline-flex items-center gap-1.5 text-sm text-ink-muted">
            <MessageSquare size={15} /> Pedísela al árbitro en el chat
          </span>
        </div>
      )}

      {p.prelude_hand.length > 0 && (
        <div className="space-y-3">
          <h3 className="label">Preludes para jugar</h3>
          <ul className="grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-2 sm:[&>li:last-child:nth-child(odd)]:col-span-2">
            {p.prelude_hand.map((id) => (
              <li key={id} className="space-y-2 bg-surface px-4 py-3.5">
                <div className="flex items-start justify-between gap-3">
                  <span className="min-w-0 space-y-1.5">
                    <span className="block truncate text-[15px] font-medium tracking-tightish">{state.cards[id]?.name ?? id}</span>
                    <Tags tags={state.cards[id]?.tags ?? []} />
                  </span>
                  <button className="btn-quiet shrink-0 px-3.5 py-1.5" disabled={busy !== null} onClick={() => act(id, () => playPrelude(playerId, id))}>
                    {busy === id ? <LoaderCircle size={14} className="animate-spin" /> : <Play size={14} />}
                    Jugar
                  </button>
                </div>
                {errors[id] && (
                  <p role="alert" className="text-xs text-bad">
                    {errors[id]}. Jugala por chat y el árbitro te va a preguntar lo que falta.
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {p.pending_research.length > 0 && (
        <div className="space-y-3">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 className="label">Investigación: elegí qué comprar</h3>
            <span className="text-sm text-ink-muted">
              <span className="num font-semibold text-res-mc">{state.research_cost_per_card} M€</span> cada una
            </span>
          </div>
          <CardPicker
            ids={p.pending_research}
            cards={state.cards}
            selected={selected}
            onToggle={(id) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]))}
          />
          {errors.research && (
            <p role="alert" className="text-sm text-bad">
              {errors.research}
            </p>
          )}
          <div className="flex justify-end">
            <button className="btn-primary" disabled={busy !== null} onClick={() => act("research", () => buyResearch(playerId, selected))}>
              {busy === "research" ? <LoaderCircle size={16} className="animate-spin" /> : null}
              {selected.length === 0 ? "No comprar ninguna" : `Comprar ${selected.length} ${selected.length === 1 ? "carta" : "cartas"}`}
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
