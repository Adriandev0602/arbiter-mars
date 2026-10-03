"""
Endpoints de la API. Delgados a proposito: la logica vive en agent/graph.py,
agent/tools.py y db/, esto solo traduce HTTP <-> el grafo y las lecturas de
estado que necesita el dashboard. Nada de calculos aca.
"""
import anthropic
from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from app.agent import tools
from app.agent.graph import compiled_graph
from app.db.supabase_client import supabase
from app.models.schemas import (
    ChatRequest, ChatResponse, CreatePlayerRequest, GameState, PlayerStateResponse, PlayerSummary,
)

router = APIRouter()


def _player_or_404(player_id: str) -> dict:
    res = supabase.table("players").select("id").eq("id", player_id).maybe_single().execute()
    if res is None or res.data is None:
        raise HTTPException(status_code=404, detail=f"Jugador '{player_id}' no existe")
    return dict(tools._load_player(player_id))


def _card_catalog(card_ids: set[str]) -> dict[str, dict]:
    """Nombre/costo/tags de las cartas que el dashboard tiene que mostrar,
    buscadas en los cuatro catalogos (proyecto, corporacion, prelude)."""
    if not card_ids:
        return {}
    ids = sorted(card_ids)
    catalog: dict[str, dict] = {}
    for table, columns in (
        ("cards", "id,name,cost,tags,is_event"),
        ("corporation_cards", "id,name,tags"),
        ("prelude_cards", "id,name,tags"),
    ):
        res = supabase.table(table).select(columns).in_("id", ids).execute()
        for row in res.data or []:
            catalog[row["id"]] = {**row, "kind": table}
    return catalog


@router.get("/players", response_model=list[PlayerSummary])
def list_players():
    """Jugadores existentes, para elegir con cual jugar."""
    res = supabase.table("players").select("id,display_name,tr,created_at").order("created_at").execute()
    return res.data or []


@router.post("/players", response_model=PlayerSummary)
def create_player(request: CreatePlayerRequest):
    """Crea un jugador nuevo con los valores iniciales del schema (TR 20, etc.)."""
    name = request.display_name.strip()
    if not name:
        raise HTTPException(status_code=422, detail="El nombre no puede estar vacio")
    res = supabase.table("players").insert({"display_name": name}).execute()
    row = res.data[0]
    return {k: row[k] for k in ("id", "display_name", "tr", "created_at")}


@router.get("/state/{player_id}", response_model=PlayerStateResponse)
def get_state(player_id: str):
    """Estado completo del jugador + nombres de las cartas que tiene en mano/juego."""
    player = _player_or_404(player_id)
    ids = set(player["hand"]) | set(player["active_cards"]) | set(player["played_cards"])
    return {"player": player, "cards": _card_catalog(ids)}


@router.get("/game", response_model=GameState)
def get_game():
    """Parametros globales compartidos + resumen de Turmoil y colonias en juego."""
    globals_ = dict(tools._load_global_parameters())
    turmoil = tools._load_turmoil()
    colonies = tools._load_colonies()
    return {
        "global_parameters": globals_,
        "turmoil": {
            "ruling_party": turmoil["ruling_party"],
            "dominant_party": turmoil["dominant_party"],
            "chairman": turmoil["chairman"],
            "current_event": turmoil["current_event"],
            "coming_event": turmoil["coming_event"],
            "distant_event": turmoil["distant_event"],
        },
        "colonies": sorted(colonies),
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Recibe una consulta en lenguaje natural, la corre a traves del grafo
    (LLM -> tools -> LLM) y devuelve el veredicto + el estado del jugador
    releido de la base, para que el dashboard se refresque sin otro pedido.
    """
    _player_or_404(request.player_id)
    try:
        result = compiled_graph.invoke(
            {
                "messages": [HumanMessage(content=request.message)],
                "player_id": request.player_id,
                "extracted_args": None,
                "tool_result": None,
            }
        )
    except anthropic.AuthenticationError:
        raise HTTPException(
            status_code=503,
            detail="El backend no tiene una ANTHROPIC_API_KEY valida (revisar backend/.env)",
        )
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Limite de uso de la API de Claude alcanzado, proba en un rato")
    except anthropic.APIConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar con la API de Claude")
    last_message = result["messages"][-1]
    reply = last_message.content if isinstance(last_message.content, str) else "".join(
        block.get("text", "") for block in last_message.content if isinstance(block, dict)
    )
    return ChatResponse(reply=reply, updated_state=dict(tools._load_player(request.player_id)))
