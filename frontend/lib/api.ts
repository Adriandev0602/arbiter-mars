/**
 * Cliente delgado hacia el backend. Centraliza la URL base y el manejo de
 * errores para no repetir fetch() sueltos por los componentes.
 */
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type ChatResponse = {
  reply: string;
  updated_state: Record<string, unknown> | null;
};

export async function sendChatMessage(playerId: string, message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_id: playerId, message }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }

  return res.json();
}

// TODO: agregar getPlayerState(playerId) una vez que GET /api/state este implementado
