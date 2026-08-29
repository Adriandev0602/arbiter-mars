"use client";

import { useState } from "react";
import { sendChatMessage } from "@/lib/api";

type Message = { role: "user" | "assistant"; content: string };

/**
 * Chat persistente donde el usuario consulta jugadas en lenguaje natural.
 * Cada mensaje del usuario se manda al backend, que corre el grafo de
 * LangGraph y devuelve un veredicto basado en calculos deterministas.
 */
export default function SidebarChat({ playerId }: { playerId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChatMessage(playerId, userMessage.content);
      setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);
      // TODO: si res.updated_state viene, propagarlo al Dashboard (context / state global)
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error al consultar el arbitro. Revisa el backend." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-full p-4">
      <h2 className="text-lg font-medium mb-4">Consultar jugada</h2>

      <div className="flex-1 overflow-y-auto space-y-3 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span className="inline-block bg-gray-100 rounded px-3 py-2 text-sm">{m.content}</span>
          </div>
        ))}
        {loading && <p className="text-sm text-gray-400">Pensando...</p>}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2 text-sm"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Quiero jugar la carta X, tengo 5 de titanio..."
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-black text-white rounded px-4 py-2 text-sm disabled:opacity-50"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
