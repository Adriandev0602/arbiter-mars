"use client";

import CardList from "@/components/CardList";
import GlobalParameters from "@/components/GlobalParameters";
import ResourcePanel from "@/components/ResourcePanel";
import type { GameState, StateResponse } from "@/lib/api";

/**
 * Panel principal: parametros globales de la partida, recursos del jugador y
 * sus cartas. Solo pinta lo que devuelve la API (GET /api/game y
 * /api/state/{id}); no calcula nada.
 */
export default function Dashboard({
  game,
  state,
  hasPlayer,
}: {
  game: GameState | null;
  state: StateResponse | null;
  hasPlayer: boolean;
}) {
  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      {game && <GlobalParameters game={game} />}

      {!hasPlayer && (
        <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">
          Elegí un jugador o creá uno nuevo arriba a la derecha para ver su estado.
        </div>
      )}

      {state && (
        <>
          <ResourcePanel player={state.player} />
          <div className="grid gap-6 lg:grid-cols-2">
            <CardList
              title="Mano"
              emptyText="Sin cartas en la mano."
              ids={state.player.hand}
              cards={state.cards}
            />
            <CardList
              title="Cartas activas"
              emptyText="Ninguna carta con acción o recursos en juego."
              ids={Object.keys(state.player.active_cards)}
              cards={state.cards}
              active={state.player.active_cards}
            />
          </div>
          <CardList
            title="Jugadas"
            emptyText="Todavía no se jugó ninguna carta."
            ids={state.player.played_cards}
            cards={state.cards}
            compact
          />
        </>
      )}
    </div>
  );
}
