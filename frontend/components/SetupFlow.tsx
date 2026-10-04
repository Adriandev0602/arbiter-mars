"use client";

import { useEffect, useMemo, useState } from "react";
import { ArrowRight, Check, LoaderCircle, Search } from "lucide-react";
import CardPicker from "@/components/CardPicker";
import { Tags } from "@/components/CardList";
import {
  buyResearch,
  chooseCorporation,
  dealPreludes,
  dealStartingHand,
  keepPreludes,
  listCorporations,
  type Corporation,
  type StateResponse,
} from "@/lib/api";

const BEGINNER = "beginner_corporation";

export type SetupStep = "corporation" | "hand" | "preludes" | "done";

/** Paso del setup en el que esta el jugador, deducido de su estado (no de un flag de la UI). */
export function setupStep(state: StateResponse, preludesSkipped: boolean): SetupStep {
  const p = state.player;
  if (!state.corporation) return "corporation";
  const dealt = p.deck.length > 0 || p.hand.length > 0;
  if (!dealt || (p.pending_research.length > 0 && p.played_cards.length === 1 && p.hand.length === 0)) return "hand";
  const preludesTouched =
    p.pending_prelude_choice.length > 0 ||
    p.prelude_hand.length > 0 ||
    p.played_cards.some((id) => state.cards[id]?.kind === "prelude_cards");
  if (!preludesTouched && !preludesSkipped) return "preludes";
  if (p.pending_prelude_choice.length > 0) return "preludes";
  return "done";
}

const STEPS: { id: Exclude<SetupStep, "done">; label: string }[] = [
  { id: "corporation", label: "Corporación" },
  { id: "hand", label: "Mano inicial" },
  { id: "preludes", label: "Preludes" },
];

function Stepper({ current }: { current: SetupStep }) {
  const index = STEPS.findIndex((s) => s.id === current);
  return (
    <ol className="flex flex-wrap items-center gap-2 text-sm">
      {STEPS.map((s, i) => (
        <li key={s.id} className="flex items-center gap-2">
          <span
            className={`num grid h-6 w-6 place-items-center rounded-full text-xs font-semibold ${
              i < index ? "bg-coral/20 text-coral-bright" : i === index ? "bg-coral text-coral-ink" : "bg-white/[0.06] text-ink-faint"
            }`}
          >
            {i + 1}
          </span>
          <span className={i === index ? "font-medium text-ink" : "hidden text-ink-faint sm:inline"}>{s.label}</span>
          {i < STEPS.length - 1 && <span className="mx-1 h-px w-6 bg-line-strong" />}
        </li>
      ))}
    </ol>
  );
}

function ErrorLine({ message }: { message: string | null }) {
  if (!message) return null;
  return (
    <p role="alert" className="rounded-xl border border-bad/30 bg-bad/10 px-4 py-3 text-sm text-bad">
      {message}
    </p>
  );
}

function useAction(onState: (s: StateResponse) => void) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const run = async (fn: () => Promise<StateResponse>) => {
    setBusy(true);
    setError(null);
    try {
      onState(await fn());
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo completar el paso");
    } finally {
      setBusy(false);
    }
  };
  return { busy, error, run };
}

function CorporationStep({ playerId, onState }: { playerId: string; onState: (s: StateResponse) => void }) {
  const [corps, setCorps] = useState<Corporation[]>([]);
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const { busy, error, run } = useAction(onState);

  useEffect(() => {
    listCorporations().then(setCorps).catch(() => setCorps([]));
  }, []);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return q ? corps.filter((c) => `${c.name} ${c.expansion}`.toLowerCase().includes(q)) : corps;
  }, [corps, query]);
  const chosen = corps.find((c) => c.id === selected);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tightish">Elegí tu corporación</h2>
          <p className="max-w-prose text-sm text-ink-muted">
            Define tus M€ iniciales y tu producción. Beginner Corporation reparte las 10 cartas gratis; con cualquier otra las
            comprás.
          </p>
        </div>
        <label className="relative w-full sm:w-64">
          <span className="sr-only">Buscar corporación</span>
          <Search size={16} className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-faint" />
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Buscar por nombre o expansión" className="field w-full pl-10" />
        </label>
      </div>

      {corps.length === 0 ? (
        <div className="grid gap-px overflow-hidden rounded-xl border border-line bg-line sm:grid-cols-2" aria-hidden>
          {Array.from({ length: 6 }, (_, i) => (
            <div key={i} className="h-[84px] animate-pulse bg-surface" />
          ))}
        </div>
      ) : (
        <ul className="grid max-h-[52vh] gap-px overflow-y-auto rounded-xl border border-line bg-line sm:grid-cols-2 sm:[&>li:last-child:nth-child(odd)]:col-span-2">
          {visible.map((c) => {
            const on = c.id === selected;
            return (
              <li key={c.id} className="bg-surface">
                <button
                  type="button"
                  aria-pressed={on}
                  onClick={() => setSelected(c.id)}
                  className={`flex h-full w-full items-start justify-between gap-3 px-4 py-3.5 text-left transition-colors duration-200 ${
                    on ? "bg-coral/[0.09]" : "hover:bg-white/[0.03]"
                  }`}
                >
                  <span className="min-w-0 space-y-1.5">
                    <span className="block truncate text-[15px] font-medium tracking-tightish">{c.name}</span>
                    <span className="block text-xs text-ink-faint">{c.expansion}</span>
                    <Tags tags={c.tags} />
                  </span>
                  <span className="flex shrink-0 items-center gap-2.5">
                    <span className="num text-lg font-semibold text-res-mc">{c.starting_mc} M€</span>
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
          {visible.length === 0 && (
            <li className="bg-surface px-4 py-6 text-sm text-ink-faint sm:col-span-2">Ninguna corporación coincide con “{query}”.</li>
          )}
        </ul>
      )}

      <ErrorLine message={error} />
      <div className="flex justify-end">
        <button
          className="btn-primary"
          disabled={!chosen || busy}
          onClick={() => chosen && run(() => chooseCorporation(playerId, chosen.id))}
        >
          {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
          {chosen ? `Empezar con ${chosen.name}` : "Elegí una corporación"}
          {!busy && <ArrowRight size={16} />}
        </button>
      </div>
    </div>
  );
}

function HandStep({ playerId, state, onState }: { playerId: string; state: StateResponse; onState: (s: StateResponse) => void }) {
  const p = state.player;
  const isBeginner = state.corporation?.id === BEGINNER;
  const [selected, setSelected] = useState<string[]>([]);
  const { busy, error, run } = useAction(onState);
  const toggle = (id: string) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  if (p.pending_research.length === 0) {
    return (
      <div className="space-y-5">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tightish">Repartí tu mano inicial</h2>
          <p className="max-w-prose text-sm text-ink-muted">
            {isBeginner
              ? "Con Beginner Corporation las 10 cartas van gratis a tu mano."
              : `Se reparten 10 cartas y elegís cuáles comprar, a ${state.research_cost_per_card} M€ cada una según el motor. Las que no compres se descartan.`}
          </p>
        </div>
        <ErrorLine message={error} />
        <div className="flex justify-end">
          <button className="btn-primary" disabled={busy} onClick={() => run(() => dealStartingHand(playerId, !isBeginner))}>
            {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
            Repartir 10 cartas
            {!busy && <ArrowRight size={16} />}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tightish">Elegí qué cartas comprar</h2>
          <p className="max-w-prose text-sm text-ink-muted">
            Cada carta cuesta <span className="num font-semibold text-res-mc">{state.research_cost_per_card} M€</span>. Tenés{" "}
            <span className="num font-semibold text-res-mc">{p.mc} M€</span>; el motor valida el pago al confirmar.
          </p>
        </div>
        <span className="num text-sm text-ink-muted">{selected.length} de 10 elegidas</span>
      </div>
      <CardPicker ids={p.pending_research} cards={state.cards} selected={selected} onToggle={toggle} />
      <ErrorLine message={error} />
      <div className="flex justify-end">
        <button className="btn-primary" disabled={busy} onClick={() => run(() => buyResearch(playerId, selected))}>
          {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
          {selected.length === 0 ? "No comprar ninguna" : `Comprar ${selected.length} ${selected.length === 1 ? "carta" : "cartas"}`}
        </button>
      </div>
    </div>
  );
}

function PreludeStep({
  playerId,
  state,
  onState,
  onSkip,
}: {
  playerId: string;
  state: StateResponse;
  onState: (s: StateResponse) => void;
  onSkip: () => void;
}) {
  const p = state.player;
  const [selected, setSelected] = useState<string[]>([]);
  const { busy, error, run } = useAction(onState);
  const toggle = (id: string) => setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]));

  if (p.pending_prelude_choice.length === 0) {
    return (
      <div className="space-y-5">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tightish">¿Jugás con Preludes?</h2>
          <p className="max-w-prose text-sm text-ink-muted">
            Se reparten 4 al azar y te quedás con 2, gratis. Las jugás antes de tu primera generación.
          </p>
        </div>
        <ErrorLine message={error} />
        <div className="flex flex-wrap justify-end gap-3">
          <button className="btn-quiet" onClick={onSkip}>
            Jugar sin Preludes
          </button>
          <button className="btn-primary" disabled={busy} onClick={() => run(() => dealPreludes(playerId))}>
            {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
            Repartir 4 Preludes
            {!busy && <ArrowRight size={16} />}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tightish">Quedate con 2 Preludes</h2>
          <p className="max-w-prose text-sm text-ink-muted">Las otras dos se descartan.</p>
        </div>
        <span className="num text-sm text-ink-muted">{selected.length} de 2 elegidas</span>
      </div>
      <CardPicker ids={p.pending_prelude_choice} cards={state.cards} selected={selected} onToggle={toggle} maxSelected={2} />
      <ErrorLine message={error} />
      <div className="flex justify-end">
        <button className="btn-primary" disabled={busy || selected.length !== 2} onClick={() => run(() => keepPreludes(playerId, selected))}>
          {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
          Quedarme con estas 2
        </button>
      </div>
    </div>
  );
}

/** Inicio de partida guiado: corporacion, mano inicial y preludes, cada paso una tool del motor. */
export default function SetupFlow({
  playerId,
  state,
  step,
  onState,
  onSkipPreludes,
}: {
  playerId: string;
  state: StateResponse;
  step: SetupStep;
  onState: (s: StateResponse) => void;
  onSkipPreludes: () => void;
}) {
  return (
    <section className="panel space-y-7 p-5 sm:p-8" aria-label="Inicio de partida">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Stepper current={step} />
        {state.corporation && (
          <span className="text-sm text-ink-muted">
            Corporación: <span className="font-medium text-ink">{state.corporation.name}</span> ·{" "}
            <span className="num font-medium text-res-mc">{state.player.mc} M€</span>
          </span>
        )}
      </div>
      {step === "corporation" && <CorporationStep playerId={playerId} onState={onState} />}
      {step === "hand" && <HandStep playerId={playerId} state={state} onState={onState} />}
      {step === "preludes" && <PreludeStep playerId={playerId} state={state} onState={onState} onSkip={onSkipPreludes} />}
    </section>
  );
}
