"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowUp, LoaderCircle } from "lucide-react";
import { sendChatMessage } from "@/lib/api";

type Message = { role: "user" | "assistant" | "error"; content: string };

const EXAMPLES = [
  "¿Cuál es mi estado actual?",
  "Quiero usar el proyecto estándar Planta de energía",
  "Cerrá mi fase de producción",
];

/**
 * Chat con el árbitro. Cada mensaje va al backend, que corre el grafo de
 * LangGraph (el LLM solo interpreta; los números salen del motor de reglas).
 * Después de cada respuesta avisa a la página para que refresque el dashboard.
 */
export default function SidebarChat({ playerId, onReply }: { playerId: string | null; onReply: () => void }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages([]);
  }, [playerId]);

  // Scrollea solo el panel de mensajes (no la pagina: en celular la pagina
  // entera scrollea y scrollIntoView la arrastraba hasta el chat al cargar).
  useEffect(() => {
    const el = scrollRef.current;
    if (el && (messages.length > 0 || loading)) el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  async function send(text: string) {
    const content = text.trim();
    if (!content || loading || !playerId) return;
    setMessages((prev) => [...prev, { role: "user", content }]);
    setInput("");
    setLoading(true);
    try {
      const res = await sendChatMessage(playerId, content);
      setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);
      onReply();
      // En celular el chat esta al final de la pagina: llevar la vista a la respuesta.
      if (window.matchMedia("(max-width: 1023px)").matches) {
        requestAnimationFrame(() => scrollRef.current?.lastElementChild?.scrollIntoView({ behavior: "smooth", block: "end" }));
      }
    } catch (err) {
      const detail = err instanceof Error ? err.message : "error desconocido";
      setMessages((prev) => [...prev, { role: "error", content: `No se pudo consultar al árbitro (${detail}).` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-line px-5 py-4">
        <h2 className="text-base font-semibold tracking-tightish">Árbitro</h2>
        <p className="text-[13px] text-ink-muted">Contale tu jugada. Interpreta el modelo; calcula el motor.</p>
      </div>

      <div ref={scrollRef} className="space-y-3 px-5 py-5 lg:flex-1 lg:overflow-y-auto">
        {!playerId && <p className="text-sm text-ink-faint">Elegí un jugador para empezar.</p>}
        {playerId && messages.length === 0 && (
          <div className="space-y-2">
            <p className="text-xs text-ink-faint">Probá con</p>
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                onClick={() => send(ex)}
                className="block w-full rounded-xl border border-line-strong bg-surface-sunk px-4 py-2.5 text-left text-sm text-ink-muted transition-colors duration-200 hover:border-coral/50 hover:text-ink"
              >
                {ex}
              </button>
            ))}
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
            <div
              className={
                "max-w-[88%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm leading-relaxed " +
                (m.role === "user"
                  ? "rounded-br-md bg-coral/[0.14] text-ink"
                  : m.role === "error"
                    ? "rounded-bl-md border border-bad/30 bg-bad/10 text-bad"
                    : "rounded-bl-md bg-surface-raised text-ink")
              }
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && (
          <p className="inline-flex items-center gap-2 text-sm text-ink-muted">
            <LoaderCircle size={15} className="animate-spin text-coral" />
            El árbitro está calculando…
          </p>
        )}
      </div>

      {/* En celular la caja queda fija abajo, siempre a mano; en escritorio vive al pie del panel. */}
      <form
        className="fixed inset-x-0 bottom-0 z-30 flex items-center gap-2 border-t border-line bg-surface/95 p-3 backdrop-blur lg:static lg:z-auto lg:bg-transparent lg:backdrop-blur-none"
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
      >
        <input
          className="field min-w-0 flex-1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={playerId ? "Quiero jugar la carta X pagando…" : "Elegí un jugador primero"}
          aria-label="Mensaje para el árbitro"
          disabled={!playerId}
        />
        <button
          type="submit"
          aria-label="Enviar"
          disabled={loading || !playerId || !input.trim()}
          className="btn-primary h-10 w-10 shrink-0 px-0 py-0"
        >
          <ArrowUp size={18} strokeWidth={2.5} />
        </button>
      </form>
    </div>
  );
}
