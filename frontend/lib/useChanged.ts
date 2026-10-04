"use client";

import { useEffect, useRef, useState } from "react";

/**
 * Valores ANTERIORES de los numeros que cambiaron entre dos lecturas de la API
 * con la misma `scope` (un jugador, o la partida). No resta nada: guarda el
 * numero que el motor devolvio antes, para mostrar "antes X" al lado del nuevo.
 * Queda visible hasta el proximo cambio (o hasta cambiar de scope), asi el
 * jugador que vuelve la vista del tablero todavia ve que movio el motor.
 */
export function useChanged(values: Record<string, number>, scope: string): Record<string, number> {
  const last = useRef<{ scope: string; values: Record<string, number> } | null>(null);
  const [changed, setChanged] = useState<Record<string, number>>({});
  const signature = JSON.stringify(values);

  useEffect(() => {
    const prev = last.current;
    if (prev && prev.scope === scope) {
      const diff: Record<string, number> = {};
      for (const k of Object.keys(values)) if (values[k] !== prev.values[k]) diff[k] = prev.values[k];
      if (Object.keys(diff).length) setChanged(diff);
    } else {
      setChanged({});
    }
    last.current = { scope, values };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [signature, scope]);

  return changed;
}
