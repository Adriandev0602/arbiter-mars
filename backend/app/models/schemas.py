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
    """Stock, produccion y TR de un jugador -- misma forma plana que
    agent.rules_engine.PlayerState / tools.get_player_state()."""
    tr: int
    mc: int
    steel: int
    titanium: int
    plants: int
    energy: int
    heat: int
    mc_production: int
    steel_production: int
    titanium_production: int
    plant_production: int
    energy_production: int
    heat_production: int
