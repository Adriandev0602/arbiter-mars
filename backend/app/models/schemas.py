"""
Contratos de la API (Pydantic). Lo que entra y sale de /api/chat y /api/state
vive aqui, separado de los modelos internos del grafo.
"""
from pydantic import BaseModel


class ChatRequest(BaseModel):
    player_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    # Estado actualizado del jugador tras la jugada, para que el frontend
    # refresque el dashboard sin otro round-trip
    updated_state: dict | None = None


class PlayerState(BaseModel):
    player_id: str
    resources: dict[str, int]
    active_cards: list[str]
    transaction_history: list[dict]
