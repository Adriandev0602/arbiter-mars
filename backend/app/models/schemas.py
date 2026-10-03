"""
Contratos de la API (Pydantic). Lo que entra y sale de /api vive aqui,
separado de los modelos internos del grafo.
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


class CreatePlayerRequest(BaseModel):
    display_name: str


class PlayerSummary(BaseModel):
    id: str
    display_name: str
    tr: int
    created_at: str


class PlayerStateResponse(BaseModel):
    # Misma forma que agent.rules_engine.PlayerState (stock, produccion, TR,
    # mano, cartas activas, etc.); se deja como dict para no duplicar las
    # ~40 claves del TypedDict.
    player: dict
    # card_id -> {id, name, tags, kind, cost?, is_event?} de las cartas que
    # aparecen en mano / cartas activas / jugadas.
    cards: dict[str, dict]


class GameState(BaseModel):
    global_parameters: dict
    turmoil: dict
    colonies: list[str]
