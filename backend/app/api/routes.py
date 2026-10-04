"""
Endpoints de la API. Delgados a proposito: la logica vive en agent/graph.py,
agent/tools.py y db/, esto solo traduce HTTP <-> el grafo y las lecturas de
estado que necesita el dashboard. Nada de calculos aca.
"""
import anthropic
from fastapi import APIRouter, HTTPException
from postgrest.exceptions import APIError
from langchain_core.messages import HumanMessage

from app.agent import board as boardlib
from app.agent import rules_engine as engine
from app.agent import tools
from app.agent.graph import compiled_graph
from app.db.supabase_client import supabase
from app.models.schemas import (
    BoardResponse, ChatRequest, ChatResponse, ChooseCorporationRequest, CorporationSummary, CreatePlayerRequest,
    DealHandRequest, GameState, KeepPreludesRequest, PlaceTileRequest, PlayerStateResponse, PlayerSummary, ResearchRequest,
)

router = APIRouter()


def _player_or_404(player_id: str) -> dict:
    # Un id que no es UUID hace fallar la consulta en Postgres: para el cliente
    # es lo mismo que un jugador inexistente (404, no 500).
    try:
        res = supabase.table("players").select("id").eq("id", player_id).maybe_single().execute()
    except APIError:
        res = None
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
    """
    Estado completo del jugador + nombres de las cartas que tiene en mano, en
    juego o pendientes de elegir. `research_cost_per_card` es el precio que el
    MOTOR le cobra a este jugador por carta (3, o 5 con Polyphemos, 1 con
    TerraLabs): la UI lo muestra, nunca lo calcula.
    """
    player = _player_or_404(player_id)
    ids = (
        set(player["hand"]) | set(player["active_cards"]) | set(player["played_cards"])
        | set(player["pending_research"]) | set(player.get("pending_prelude_choice") or [])
        | set(player.get("prelude_hand") or [])
    )
    cards = _card_catalog(ids)
    corporation = next(
        (cards[c] for c in player["played_cards"] if cards.get(c, {}).get("kind") == "corporation_cards"), None,
    )
    return {
        "player": player,
        "cards": cards,
        "corporation": corporation,
        "research_cost_per_card": engine.compute_research_cost_per_card(engine.PlayerState(**player)),  # type: ignore[typeddict-item]
    }


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


# ---------------------------------------------------------------------------
# Inicio de partida (setup oficial): corporacion -> mano inicial -> preludes.
# Cada endpoint es una llamada directa a la tool correspondiente: el motor
# valida y calcula; aca solo se traduce el error a HTTP.
# ---------------------------------------------------------------------------

_GAME_ERRORS = (
    ValueError, engine.CardEffectError, engine.InsufficientResourcesError,
    engine.CardNotInHandError, engine.CardRequirementNotMetError, engine.GlobalParameterMaxedError,
    boardlib.InvalidPlacementError, boardlib.HexOccupiedError, boardlib.UnknownHexError,
)


def _run_tool(tool, **kwargs) -> dict:
    try:
        return tool.func(**kwargs)
    except _GAME_ERRORS as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/corporations", response_model=list[CorporationSummary])
def list_corporations():
    """Catalogo de corporaciones para elegir al empezar la partida."""
    res = supabase.table("corporation_cards").select("id,name,expansion,starting_mc,tags").order("name").execute()
    return res.data or []


@router.post("/players/{player_id}/corporation")
def choose_corporation(player_id: str, request: ChooseCorporationRequest):
    _player_or_404(player_id)
    _run_tool(tools.choose_corporation, player_id=player_id, corporation_id=request.corporation_id)
    return get_state(player_id)


@router.post("/players/{player_id}/starting-hand")
def deal_starting_hand(player_id: str, request: DealHandRequest):
    """10 cartas: gratis a la mano (Beginner Corporation) o a elegir y comprar."""
    _player_or_404(player_id)
    _run_tool(tools.deal_starting_hand, player_id=player_id, buy_with_research=request.buy)
    return get_state(player_id)


@router.post("/players/{player_id}/research")
def resolve_research(player_id: str, request: ResearchRequest):
    """Compra las cartas elegidas de `pending_research`; el resto se descarta."""
    _player_or_404(player_id)
    _run_tool(tools.resolve_research_phase, player_id=player_id, card_ids_to_buy=request.card_ids)
    return get_state(player_id)


@router.post("/players/{player_id}/preludes/deal")
def deal_preludes(player_id: str):
    _player_or_404(player_id)
    _run_tool(tools.deal_prelude_hand, player_id=player_id)
    return get_state(player_id)


@router.post("/players/{player_id}/preludes/keep")
def keep_preludes(player_id: str, request: KeepPreludesRequest):
    _player_or_404(player_id)
    _run_tool(tools.keep_preludes, player_id=player_id, prelude_ids=request.prelude_ids)
    return get_state(player_id)


@router.post("/players/{player_id}/preludes/{prelude_id}/play")
def play_prelude(player_id: str, prelude_id: str):
    """Juega una prelude sin parametros extra. Las que piden elegir algo
    (un hexagono, un partido, una opcion) devuelven 400 con el motivo: esas
    se juegan por chat, donde el arbitro pregunta lo que falta."""
    _player_or_404(player_id)
    _run_tool(tools.play_prelude, player_id=player_id, prelude_id=prelude_id)
    return get_state(player_id)


# ---------------------------------------------------------------------------
# Tablero (mapa Tharsis). La legalidad de cada hexagono la decide board.py;
# la UI solo resalta los que el motor marca como validos.
# ---------------------------------------------------------------------------

@router.get("/board", response_model=BoardResponse)
def get_board(player_id: str | None = None):
    """Los 61 hexagonos con su tile actual. Con `player_id`, cada hexagono
    trae ademas si ese jugador puede colocar ahi oceano, ciudad o greenery."""
    if player_id is not None:
        _player_or_404(player_id)
    board = tools._load_board()
    oceans_left = tools._load_global_parameters()["oceans_placed"] < engine.OCEANS_MAX
    hexes = []
    for hex_id, hex_def in boardlib.HEX_DEFS.items():
        tile = board.get(hex_id)
        hexes.append({
            "id": hex_id,
            "row": hex_def["row"],
            "x": hex_def["x"],
            "hex_type": hex_def["hex_type"],
            "volcanic": hex_def["volcanic"],
            "volcano_name": hex_def["volcano_name"],
            "reserved_city": hex_def["reserved_city"],
            "bonus": [{"resource": r, "amount": n} for r, n in hex_def["bonus"]],
            "bonus_available": [{"resource": r, "amount": n} for r, n in boardlib.resolve_hex_bonus(board, hex_id)],
            "tile": tile,
            "can_place_ocean": oceans_left and boardlib.can_place_ocean(board, hex_id),
            "can_place_city": boardlib.can_place_city(board, hex_id),
            "can_place_greenery": player_id is not None and boardlib.can_place_greenery(board, hex_id, player_id),
        })
    owner_ids = sorted({t["owner"] for t in board.values() if t.get("owner")})
    owners: dict[str, str] = {}
    if owner_ids:
        try:
            res = supabase.table("players").select("id,display_name").in_("id", owner_ids).execute()
            owners = {row["id"]: row["display_name"] for row in res.data or []}
        except APIError:
            owners = {}
    return {"hexes": hexes, "owners": owners}


@router.post("/players/{player_id}/place")
def place_tile(player_id: str, request: PlaceTileRequest):
    """Coloca un tile desde el mapa: proyecto estandar (ciudad, greenery,
    acuifero) o 8 plantas -> greenery. Cobra, valida y calcula el motor."""
    _player_or_404(player_id)
    if request.action == "plants_to_greenery":
        _run_tool(tools.convert_resources, player_id=player_id, conversion="plants_to_greenery", hex_id=request.hex_id)
    else:
        _run_tool(tools.use_standard_project, player_id=player_id, project_name=request.action, hex_id=request.hex_id)
    return get_state(player_id)


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
