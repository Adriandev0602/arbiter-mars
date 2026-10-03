"use client";

import { useEffect, useRef, useState } from "react";
import { sendChatMessage } from "@/lib/api";

type Message = { role: "user" | "assistant" | "error"; content: string };

const EXAMPLES = [
  "¿Cuál es mi estado actual?",
  "Cerrá mi fase de producción",
  "Quiero usar el proyecto estándar Planta de energía",
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
    } catch (err) {
      const detail = err instanceof Error ? err.message : "error desconocido";
      setMessages((prev) => [...prev, { role: "error", content: `No se pudo consultar al árbitro (${detail}).` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-sm font-semibold">Consultar al árbitro</h2>
        <p className="text-xs text-slate-500">Describí tu jugada en lenguaje natural.</p>
      </div>

      <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
        {!playerId && <p className="text-sm text-slate-400">Elegí un jugador para empezar.</p>}
        {playerId && messages.length === 0 && (
          <div className="space-y-2">
            <p className="text-xs text-slate-400">Probá con:</p>
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                onClick={() => send(ex)}
                className="block w-full rounded border border-slate-200 px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-50"
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
                "max-w-[85%] whitespace-pre-wrap rounded-lg px-3 py-2 text-sm " +
                (m.role === "user"
                  ? "bg-slate-900 text-white"
                  : m.role === "error"
                    ? "border border-red-200 bg-red-50 text-red-800"
                    : "bg-slate-100 text-slate-800")
              }
            >
              {m.content}
            </div>
          </div>
        ))}
        {loading && <p className="text-sm text-slate-400">El árbitro está calculando…</p>}
      </div>

      <form
        className="flex gap-2 border-t border-slate-200 p-3"
        onSubmit={(e) => {
          e.preventDefault();
          send(input);
        }}
      >
        <input
          className="min-w-0 flex-1 rounded border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-50"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={playerId ? "Quiero jugar la carta X pagando…" : "Elegí un jugador primero"}
          disabled={!playerId}
        />
        <button
          type="submit"
          disabled={loading || !playerId || !input.trim()}
          className="rounded bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-700 disabled:opacity-40"
        >
          Enviar
        </button>
      </form>
    </div>
  );
}
