"""
Contratos de la API (Pydantic). Lo que entra y sale de /api vive aqui,
separado de los modelos internos del grafo.
"""
from typing import Literal

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


class ChooseCorporationRequest(BaseModel):
    corporation_id: str


class DealHandRequest(BaseModel):
    # True: las 10 cartas van a pending_research y se compran (setup oficial
    # con corporaciones). False: van gratis a la mano (Beginner Corporation).
    buy: bool = True


class ResearchRequest(BaseModel):
    card_ids: list[str]


class KeepPreludesRequest(BaseModel):
    prelude_ids: list[str]


class CorporationSummary(BaseModel):
    id: str
    name: str
    expansion: str
    starting_mc: int
    tags: list[str]


class PlayerStateResponse(BaseModel):
    # Misma forma que agent.rules_engine.PlayerState (stock, produccion, TR,
    # mano, cartas activas, etc.); se deja como dict para no duplicar las
    # ~40 claves del TypedDict.
    player: dict
    # card_id -> {id, name, tags, kind, cost?, is_event?} de las cartas que
    # aparecen en mano / cartas activas / jugadas / pendientes de elegir.
    cards: dict[str, dict]
    # Corporacion elegida (entrada de `cards`), o None si todavia no eligio.
    corporation: dict | None = None
    # Precio por carta que el motor cobra a este jugador en la investigacion.
    research_cost_per_card: int


class PlaceTileRequest(BaseModel):
    # Las cuatro jugadas de reglas fijas que colocan un tile en el mapa:
    # proyectos estandar city/greenery/aquifer y la conversion 8 plantas ->
    # greenery. Las colocaciones de cartas siguen yendo por chat.
    action: Literal["city", "greenery", "aquifer", "plants_to_greenery"]
    hex_id: str


class BoardResponse(BaseModel):
    # Un item por hexagono: definicion estatica (board.HEX_DEFS), tile actual
    # y si el MOTOR permite hoy colocar oceano/ciudad/greenery ahi.
    hexes: list[dict]
    # owner_id -> display_name, para nombrar los tiles de cada jugador.
    owners: dict[str, str]


class GameState(BaseModel):
    global_parameters: dict
    turmoil: dict
    colonies: list[str]
