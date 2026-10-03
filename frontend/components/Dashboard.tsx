"use client";

import { useState } from "react";
import { ArrowRight, LoaderCircle } from "lucide-react";
import CardTabs from "@/components/CardList";
import GlobalParameters from "@/components/GlobalParameters";
import PendingActions from "@/components/PendingActions";
import ResourcePanel from "@/components/ResourcePanel";
import SetupFlow, { type SetupStep } from "@/components/SetupFlow";
import { createPlayer, type GameState, type StateResponse } from "@/lib/api";

/** Estado vacio con su accion: crear el jugador ahi mismo. */
function CreatePlayer({ onCreated }: { onCreated: (id: string) => void }) {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  return (
    <form
      className="flex max-w-md flex-col gap-2 sm:flex-row"
      onSubmit={async (e) => {
        e.preventDefault();
        if (!name.trim()) return;
        setBusy(true);
        setError(null);
        try {
          onCreated((await createPlayer(name)).id);
        } catch (err) {
          setError(err instanceof Error ? err.message : "No se pudo crear el jugador");
        } finally {
          setBusy(false);
        }
      }}
    >
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Tu nombre"
        aria-label="Nombre del jugador nuevo"
        className="field min-w-0 flex-1"
      />
      <button type="submit" className="btn-primary" disabled={busy || !name.trim()}>
        {busy ? <LoaderCircle size={16} className="animate-spin" /> : null}
        Crear jugador
        {!busy && <ArrowRight size={16} />}
      </button>
      {error && <p className="w-full text-sm text-bad sm:order-last">{error}</p>}
    </form>
  );
}

/**
 * Panel principal. Mientras el setup no termino, muestra el inicio de partida;
 * despues, el libro de recursos primero (lo que se mira en la mesa), lo
 * pendiente, la partida y las cartas. Solo pinta lo que devuelve la API.
 */
export default function Dashboard({
  game,
  state,
  playerId,
  step,
  onState,
  onCreated,
  onSkipPreludes,
}: {
  game: GameState | null;
  state: StateResponse | null;
  playerId: string | null;
  step: SetupStep | null;
  onState: (s: StateResponse) => void;
  onCreated: (id: string) => void;
  onSkipPreludes: () => void;
}) {
  if (!playerId) {
    return (
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <section className="panel space-y-4 p-6 sm:p-10">
          <h2 className="max-w-xl text-3xl font-semibold leading-tight tracking-display sm:text-4xl">
            Jugá tu turno. El árbitro hace las cuentas.
          </h2>
          <p className="max-w-prose text-[15px] text-ink-muted">
            Creá tu jugador y elegí tu corporación. Después contale tus jugadas al árbitro: un motor de reglas calcula cada costo,
            producción y TR, y acá ves qué cambió.
          </p>
          <CreatePlayer onCreated={onCreated} />
        </section>
        {game && <GlobalParameters game={game} />}
      </div>
    );
  }

  if (!state) {
    return (
      <div className="mx-auto flex max-w-6xl flex-col gap-6" aria-busy>
        <div className="h-48 animate-pulse rounded-2xl bg-white/[0.04]" />
        <div className="h-36 animate-pulse rounded-2xl bg-white/[0.04]" />
      </div>
    );
  }

  if (step && step !== "done") {
    return (
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <SetupFlow playerId={playerId} state={state} step={step} onState={onState} onSkipPreludes={onSkipPreludes} />
        {game && <GlobalParameters game={game} />}
      </div>
    );
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6">
      {state.corporation && (
        <p className="text-sm text-ink-muted">
          Jugando con <span className="font-medium text-ink">{state.corporation.name}</span>
        </p>
      )}
      <ResourcePanel player={state.player} playerId={playerId} />
      <PendingActions playerId={playerId} state={state} onState={onState} />
      {game && <GlobalParameters game={game} />}
      <CardTabs
        cards={state.cards}
        tabs={[
          { title: "Mano", ids: state.player.hand, empty: "No tenés cartas en la mano. Las conseguís en la fase de investigación." },
          {
            title: "Activas",
            ids: Object.keys(state.player.active_cards),
            empty: "Ninguna carta con acción o recursos en juego todavía.",
            active: state.player.active_cards,
          },
          { title: "Jugadas", ids: state.player.played_cards, empty: "Todavía no jugaste ninguna carta." },
        ]}
      />
    </div>
  );
}
