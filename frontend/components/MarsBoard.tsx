"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Building2, Check, LoaderCircle, Mountain, Sparkles, Sprout, Tent, Users, Waves, X } from "lucide-react";
import { humanize } from "@/components/GlobalParameters";
import { placeTile, type BoardState, type Hex, type HexBonus, type PlaceAction, type StateResponse } from "@/lib/api";

// Geometria: hexagonos con punta arriba. R es el radio en unidades del viewBox.
const R = 30;
const W = Math.sqrt(3) * R;
const ROW_STEP = 1.5 * R;
const ROW_SIZES = [5, 6, 7, 8, 9, 8, 7, 6, 5];
const PAD = 14;
const VIEW_W = 9 * W + PAD * 2;
const VIEW_H = 8 * ROW_STEP + 2 * R + PAD * 2;

const HEX_POINTS = Array.from({ length: 6 }, (_, i) => {
  const a = (Math.PI / 180) * (60 * i - 90);
  return `${(R * Math.cos(a)).toFixed(2)},${(R * Math.sin(a)).toFixed(2)}`;
}).join(" ");

/** Centro de un hexagono: la fila define la altura; la posicion dentro de la fila, el ancho. */
function center(hex: Hex) {
  const n = ROW_SIZES[hex.row];
  const index = hex.x - (9 - n);
  return { cx: VIEW_W / 2 + (index - (n - 1) / 2) * W, cy: PAD + R + hex.row * ROW_STEP };
}

const ACTIONS: { action: PlaceAction; label: string; group: string; legal: keyof Hex }[] = [
  { action: "city", label: "Ciudad", group: "Proyecto estándar", legal: "can_place_city" },
  { action: "greenery", label: "Greenery", group: "Proyecto estándar", legal: "can_place_greenery" },
  { action: "aquifer", label: "Océano", group: "Proyecto estándar", legal: "can_place_ocean" },
  { action: "plants_to_greenery", label: "Greenery con plantas", group: "Conversión", legal: "can_place_greenery" },
];

const TILE_STYLE: Record<string, { fill: string; label: string }> = {
  ocean: { fill: "#4f9fe0", label: "Océano" },
  greenery: { fill: "#7cb35f", label: "Greenery" },
  city: { fill: "#aaa39b", label: "Ciudad" },
  special: { fill: "#c08a57", label: "Tile especial" },
  nomad: { fill: "#d6a35c", label: "Nómades" },
  community: { fill: "#b083ee", label: "Comunidad" },
};

const TILE_ICON = { ocean: Waves, greenery: Sprout, city: Building2, special: Sparkles, nomad: Tent, community: Users };

const BONUS_STYLE: Record<HexBonus["resource"], { fill: string; one: string; many: string }> = {
  steel: { fill: "#c08a57", one: "acero", many: "acero" },
  titanium: { fill: "#bdb5ac", one: "titanio", many: "titanio" },
  plant: { fill: "#7cc463", one: "planta", many: "plantas" },
  card: { fill: "#f5efe8", one: "carta", many: "cartas" },
};

const bonusText = (b: HexBonus[]) =>
  b.length === 0 ? "sin bonus" : b.map((x) => `${x.amount} ${x.amount === 1 ? BONUS_STYLE[x.resource].one : BONUS_STYLE[x.resource].many}`).join(" + ");

function terrainText(hex: Hex) {
  if (hex.reserved_city) return `Reservado para ${humanize(hex.reserved_city)}`;
  if (hex.volcanic) return `Volcán · ${humanize(hex.volcano_name)}`;
  return hex.hex_type === "ocean" ? "Reservado para océano" : "Tierra";
}

/** Los iconos de bonus impresos en el hexagono, uno por unidad, como en el tablero fisico. */
function BonusMarks({ bonus, cx, cy }: { bonus: HexBonus[]; cx: number; cy: number }) {
  const marks = bonus.flatMap((b) => Array.from({ length: b.amount }, () => b.resource));
  if (marks.length === 0) return null;
  const size = 7;
  const gap = 3;
  const total = marks.length * size + (marks.length - 1) * gap;
  return (
    <g aria-hidden>
      {marks.map((res, i) => {
        const x = cx - total / 2 + i * (size + gap);
        const y = cy - 9;
        const fill = BONUS_STYLE[res].fill;
        if (res === "plant") return <circle key={i} cx={x + size / 2} cy={y + size / 2} r={size / 2} fill={fill} />;
        if (res === "card")
          return <rect key={i} x={x + 1} y={y - 1} width={size - 2} height={size + 2} rx={1} fill="none" stroke={fill} strokeWidth={1.2} />;
        return <rect key={i} x={x} y={y} width={size} height={size} rx={1.5} fill={fill} />;
      })}
    </g>
  );
}

/**
 * El mapa Tharsis. Pinta lo que devuelve /api/board: los tiles colocados y,
 * al elegir una jugada, los hexagonos donde el MOTOR dice que es legal
 * colocarla. Elegir un hexagono y confirmar llama al motor, que cobra y
 * valida; la UI no decide nada de reglas.
 */
export default function MarsBoard({
  board,
  playerId,
  onState,
}: {
  board: BoardState;
  playerId: string;
  onState: (s: StateResponse) => void;
}) {
  const [mode, setMode] = useState<PlaceAction | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Tiles que aparecieron desde la ultima lectura del tablero: entran con pulso.
  const seen = useRef<Set<string> | null>(null);
  const fresh = useMemo(() => {
    const placed = new Set(board.hexes.filter((h) => h.tile).map((h) => h.id));
    const prev = seen.current;
    return prev ? new Set([...placed].filter((id) => !prev.has(id))) : new Set<string>();
  }, [board]);
  useEffect(() => {
    seen.current = new Set(board.hexes.filter((h) => h.tile).map((h) => h.id));
  }, [board]);

  const active = ACTIONS.find((a) => a.action === mode) ?? null;
  const isLegal = (hex: Hex) => (active ? Boolean(hex[active.legal]) : false);
  const legalCount = active ? board.hexes.filter(isLegal).length : 0;
  const byId = useMemo(() => Object.fromEntries(board.hexes.map((h) => [h.id, h])), [board]);
  const focus = byId[selected ?? hovered ?? ""] ?? null;

  const chooseMode = (next: PlaceAction | null) => {
    setMode(next);
    setSelected(null);
    setError(null);
  };

  const pick = (id: string) => {
    setSelected(id);
    setError(null);
  };

  const confirm = async () => {
    if (!mode || !selected) return;
    setBusy(true);
    setError(null);
    try {
      onState(await placeTile(playerId, mode, selected));
      setMode(null);
      setSelected(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo colocar el tile");
    } finally {
      setBusy(false);
    }
  };

  const ownerName = (owner: string | null) =>
    owner === null ? null : owner === playerId ? "vos" : (board.owners[owner] ?? "otro jugador");

  return (
    <section data-testid="board" aria-label="Mapa de Marte" className="panel overflow-hidden">
      <div className="flex flex-wrap items-end justify-between gap-4 border-b border-line px-5 py-4 sm:px-6">
        <div>
          <h2 className="text-lg font-semibold tracking-tightish">Marte · Tharsis</h2>
          <p className="text-[13px] text-ink-muted">Elegí una jugada y el motor marca dónde es legal.</p>
        </div>
        <div role="group" aria-label="Jugada en el mapa" className="flex flex-wrap gap-1.5">
          {ACTIONS.map((a) => (
            <button
              key={a.action}
              aria-pressed={mode === a.action}
              onClick={() => chooseMode(mode === a.action ? null : a.action)}
              className={
                mode === a.action
                  ? "btn-primary px-3.5 py-1.5"
                  : "btn-quiet px-3.5 py-1.5"
              }
            >
              {a.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-px bg-line lg:grid-cols-[minmax(0,1fr)_260px]">
        <div className="relative bg-surface px-2 py-4 sm:px-4">
          <svg
            viewBox={`0 0 ${VIEW_W.toFixed(1)} ${VIEW_H.toFixed(1)}`}
            className="mx-auto block w-full max-w-[620px]"
            role="img"
            aria-label={active ? `${legalCount} hexágonos válidos para ${active.label}` : "Mapa de Marte"}
            onMouseLeave={() => setHovered(null)}
          >
            <defs>
              <radialGradient id="mars-disc" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#3a1d14" stopOpacity="0.9" />
                <stop offset="70%" stopColor="#24130e" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#171513" stopOpacity="0" />
              </radialGradient>
            </defs>
            <circle cx={VIEW_W / 2} cy={VIEW_H / 2} r={VIEW_H / 2} fill="url(#mars-disc)" />

            {board.hexes.map((hex) => {
              const { cx, cy } = center(hex);
              const legal = isLegal(hex);
              const dim = active !== null && !legal;
              const isSelected = selected === hex.id;
              const tile = hex.tile;
              const style = tile ? TILE_STYLE[tile.tile_type] : null;
              const Icon = tile ? TILE_ICON[tile.tile_type] : null;
              const filledTile = tile && tile.tile_type !== "nomad" && tile.tile_type !== "community";
              const baseFill = filledTile ? style!.fill : hex.hex_type === "ocean" ? "#132634" : "#2a1a14";
              const baseStroke = hex.hex_type === "ocean" && !tile ? "rgb(79 159 224 / 0.45)" : "rgb(255 240 225 / 0.10)";
              const owner = tile?.owner ?? null;

              return (
                <g
                  key={hex.id}
                  data-hex={hex.id}
                  data-legal={legal || undefined}
                  transform={`translate(${cx.toFixed(2)} ${cy.toFixed(2)})`}
                  className={`transition-opacity duration-200 ${dim ? "opacity-30" : ""} ${legal ? "cursor-pointer" : ""}`}
                  role={legal ? "button" : undefined}
                  tabIndex={legal ? 0 : undefined}
                  aria-label={legal ? `Hexágono ${hex.id}, ${terrainText(hex)}, ${bonusText(hex.bonus_available)}` : undefined}
                  aria-pressed={legal ? isSelected : undefined}
                  onMouseEnter={() => setHovered(hex.id)}
                  onFocus={() => setHovered(hex.id)}
                  onClick={() => legal && pick(hex.id)}
                  onKeyDown={(e) => {
                    if (legal && (e.key === "Enter" || e.key === " ")) {
                      e.preventDefault();
                      pick(hex.id);
                    }
                  }}
                >
                  <g className={fresh.has(hex.id) ? "animate-tile-in" : undefined} style={{ transformBox: "fill-box", transformOrigin: "center" }}>
                    <polygon
                      points={HEX_POINTS}
                      fill={baseFill}
                      fillOpacity={filledTile ? 0.92 : 1}
                      stroke={baseStroke}
                      strokeWidth={1}
                      strokeDasharray={hex.reserved_city && !tile ? "4 3" : undefined}
                    />
                    {legal && (
                      <polygon
                        points={HEX_POINTS}
                        fill="#ff6b4a"
                        fillOpacity={isSelected ? 0.55 : hovered === hex.id ? 0.3 : 0.07}
                        stroke={isSelected ? "#ff8467" : "#ff6b4a"}
                        strokeOpacity={isSelected || hovered === hex.id ? 1 : 0.5}
                        strokeWidth={isSelected ? 2.5 : 1.25}
                        className="transition-[fill-opacity] duration-150"
                      />
                    )}
                    {Icon && (
                      <Icon
                        x={-10}
                        y={-11}
                        width={20}
                        height={20}
                        strokeWidth={2}
                        color={filledTile ? "#141110" : style!.fill}
                        aria-hidden
                      />
                    )}
                    {!tile && <BonusMarks bonus={hex.bonus_available} cx={0} cy={0} />}
                    {!tile && hex.volcanic && (
                      <Mountain x={-5} y={-24} width={10} height={10} strokeWidth={2} color="#f0614f" aria-hidden />
                    )}
                    {owner && (
                      <circle
                        cx={0}
                        cy={15}
                        r={3.6}
                        fill={owner === playerId ? "#f5efe8" : "none"}
                        stroke={owner === playerId ? "#141110" : "#f5efe8"}
                        strokeWidth={1.4}
                      />
                    )}
                    {tile?.cathedral && <circle cx={11} cy={-12} r={3} fill="#f2c14e" stroke="#141110" strokeWidth={1} />}
                    {!tile && (
                      <text y={18} textAnchor="middle" className="num" fontSize={8.5} fill="rgb(245 239 232 / 0.38)">
                        {hex.id}
                      </text>
                    )}
                  </g>
                </g>
              );
            })}
          </svg>
        </div>

        <aside aria-live="polite" className="space-y-4 bg-surface px-5 py-5 text-sm">
          {active ? (
            <>
              <div>
                <p className="label">{active.group}</p>
                <p className="mt-0.5 text-base font-semibold tracking-tightish">{active.label}</p>
                <p className="mt-1 text-ink-muted">
                  {legalCount === 0 ? (
                    "El motor no encuentra ningún hexágono válido para esta jugada."
                  ) : (
                    <>
                      <span className="num font-medium text-ink">{legalCount}</span> hexágonos válidos. Tocá uno.
                    </>
                  )}
                </p>
              </div>
              {selected && byId[selected] && (
                <div className="space-y-3 border-t border-line pt-4">
                  <p>
                    Hexágono <span className="num font-semibold">{selected}</span>
                    <span className="block text-ink-muted">{terrainText(byId[selected])}</span>
                    <span className="block text-ink-muted">Bonus: {bonusText(byId[selected].bonus_available)}</span>
                  </p>
                  {error && (
                    <p role="alert" className="text-bad">
                      {error}
                    </p>
                  )}
                  <div className="flex gap-2">
                    <button className="btn-primary flex-1 px-4 py-2" disabled={busy} onClick={confirm}>
                      {busy ? <LoaderCircle size={15} className="animate-spin" /> : <Check size={15} />}
                      Colocar
                    </button>
                    <button className="btn-quiet h-9 w-9 px-0 py-0" aria-label="Cancelar" onClick={() => chooseMode(null)}>
                      <X size={15} />
                    </button>
                  </div>
                </div>
              )}
            </>
          ) : focus ? (
            <div className="space-y-1">
              <p className="label">Hexágono <span className="num">{focus.id}</span></p>
              <p className="text-base font-semibold tracking-tightish">
                {focus.tile ? TILE_STYLE[focus.tile.tile_type].label : terrainText(focus)}
              </p>
              {focus.tile ? (
                <p className="text-ink-muted">
                  {focus.tile.owner ? `De ${ownerName(focus.tile.owner)}` : "Neutral"}
                  {focus.tile.card ? ` · ${humanize(focus.tile.card)}` : ""}
                  {focus.tile.cathedral ? " · con catedral" : ""}
                </p>
              ) : (
                <p className="text-ink-muted">Bonus: {bonusText(focus.bonus_available)}</p>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-ink-muted">Pasá por un hexágono para ver su bonus. El número sirve para pedírselo al árbitro en el chat.</p>
              <ul className="grid grid-cols-2 gap-x-3 gap-y-2 text-[13px] text-ink-muted">
                {(["ocean", "greenery", "city", "special"] as const).map((t) => (
                  <li key={t} className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-[3px]" style={{ background: TILE_STYLE[t].fill }} />
                    {TILE_STYLE[t].label}
                  </li>
                ))}
                <li className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full border border-ground bg-ink" />
                  Tuyo
                </li>
                <li className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full border border-ink" />
                  De otro
                </li>
              </ul>
            </div>
          )}
        </aside>
      </div>
    </section>
  );
}
