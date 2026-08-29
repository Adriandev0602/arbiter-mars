"""
Tools que el LLM puede invocar. Son wrappers delgados sobre agent/rules_engine.py
(la matematica real) mas el acceso a Supabase (el estado real del jugador).
El LLM llama estas funciones con argumentos extraidos de la consulta en
lenguaje natural -- nunca calcula los numeros el mismo.
"""
from langchain_core.tools import tool

from app.agent import rules_engine as engine
from app.db.supabase_client import supabase


def _load_player(player_id: str) -> engine.PlayerState:
    """Trae el estado real del jugador desde Supabase."""
    res = supabase.table("players").select("*").eq("id", player_id).single().execute()
    row = res.data
    return engine.PlayerState(
        tr=row["tr"], mc=row["mc"], steel=row["steel"], titanium=row["titanium"],
        plants=row["plants"], energy=row["energy"], heat=row["heat"],
        mc_production=row["mc_production"], steel_production=row["steel_production"],
        titanium_production=row["titanium_production"], plant_production=row["plant_production"],
        energy_production=row["energy_production"], heat_production=row["heat_production"],
    )


def _save_player(player_id: str, player: engine.PlayerState) -> None:
    supabase.table("players").update(dict(player)).eq("id", player_id).execute()


def _load_global_parameters(game_id: str = "default") -> engine.GlobalParameters:
    res = supabase.table("global_parameters").select("*").eq("game_id", game_id).single().execute()
    row = res.data
    return engine.GlobalParameters(
        temperature=row["temperature"], oxygen=row["oxygen"], oceans_placed=row["oceans_placed"]
    )


def _save_global_parameters(globals_: engine.GlobalParameters, game_id: str = "default") -> None:
    supabase.table("global_parameters").update(dict(globals_)).eq("game_id", game_id).execute()


def _log_transaction(player_id: str, action_type: str, detail: dict) -> None:
    supabase.table("transactions").insert(
        {"player_id": player_id, "action_type": action_type, "detail": detail}
    ).execute()


@tool
def use_standard_project(player_id: str, project_name: str, num_cards_to_sell: int = 0) -> dict:
    """
    Ejecuta uno de los 6 proyectos estandar de Terraforming Mars, siempre
    disponibles para cualquier jugador.

    Args:
        player_id: id del jugador.
        project_name: uno de 'sell_patents', 'power_plant', 'asteroid',
            'aquifer', 'greenery', 'city'.
        num_cards_to_sell: solo se usa si project_name == 'sell_patents';
            cantidad de cartas que el jugador descarta (1 MC cada una).

    Returns:
        dict con el estado actualizado del jugador y, si aplica, de los
        parametros globales, mas el detalle de lo que se pago/gano.

    Lanza InsufficientResourcesError si no alcanza el MC, o
    GlobalParameterMaxedError si el parametro correspondiente ya esta al tope.
    """
    player = _load_player(player_id)
    globals_ = _load_global_parameters()

    if project_name == "sell_patents":
        new_player = engine.standard_project_sell_patents(player, num_cards_to_sell)
        new_globals = globals_
    elif project_name == "power_plant":
        new_player = engine.standard_project_power_plant(player)
        new_globals = globals_
    elif project_name == "asteroid":
        new_player, new_globals = engine.standard_project_asteroid(player, globals_)
    elif project_name == "aquifer":
        new_player, new_globals = engine.standard_project_aquifer(player, globals_)
    elif project_name == "greenery":
        new_player, new_globals = engine.standard_project_greenery(player, globals_)
    elif project_name == "city":
        new_player = engine.standard_project_city(player)
        new_globals = globals_
    else:
        raise ValueError(
            f"project_name debe ser uno de: sell_patents, power_plant, asteroid, "
            f"aquifer, greenery, city. Recibido: {project_name}"
        )

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    _log_transaction(player_id, "standard_project", {"project_name": project_name})

    return {"player": dict(new_player), "global_parameters": dict(new_globals)}


@tool
def convert_resources(player_id: str, conversion: str) -> dict:
    """
    Ejecuta una conversion de recursos del tablero de jugador (no es un
    proyecto estandar, pero sigue reglas fijas iguales para todos).

    Args:
        player_id: id del jugador.
        conversion: 'plants_to_greenery' (gasta 8 plantas, sube oxigeno 1
            paso) o 'heat_to_temperature' (gasta 8 calor, sube temperatura
            1 paso).

    Returns:
        dict con el estado actualizado del jugador y los parametros globales.
    """
    player = _load_player(player_id)
    globals_ = _load_global_parameters()

    if conversion == "plants_to_greenery":
        new_player, new_globals = engine.convert_plants_to_greenery(player, globals_)
    elif conversion == "heat_to_temperature":
        new_player, new_globals = engine.convert_heat_to_temperature(player, globals_)
    else:
        raise ValueError(
            f"conversion debe ser 'plants_to_greenery' o 'heat_to_temperature'. Recibido: {conversion}"
        )

    _save_player(player_id, new_player)
    _save_global_parameters(new_globals)
    _log_transaction(player_id, "convert_resources", {"conversion": conversion})

    return {"player": dict(new_player), "global_parameters": dict(new_globals)}


@tool
def run_production_phase(player_id: str) -> dict:
    """
    Corre la fase de produccion de fin de generacion para un jugador:
    convierte energia sobrante en calor y aplica toda su produccion
    (MC = TR + produccion de MC, y el resto de recursos suman su
    produccion correspondiente).

    Args:
        player_id: id del jugador.

    Returns:
        dict con el estado actualizado del jugador.
    """
    player = _load_player(player_id)
    new_player = engine.run_production_phase(player)

    _save_player(player_id, new_player)
    _log_transaction(player_id, "production_phase", {})

    return {"player": dict(new_player)}


@tool
def play_card(
    player_id: str,
    card_id: str,
    mc_to_pay: int,
    steel_to_pay: int = 0,
    titanium_to_pay: int = 0,
    effect_amount: int | None = None,
    effect_choice: int | None = None,
) -> dict:
    """
    Valida y paga una carta de proyecto contra su costo real en la tabla
    `cards`, respetando que acero solo cubre cartas con tag 'building' y
    titanio solo cartas con tag 'space'. Despues del pago, aplica el efecto
    inmediato de la carta segun su columna `effects` (ver
    rules_engine.apply_card_effect) -- solo esta implementado para las
    cartas cargadas en seed_cards.sql; una carta con effects={} se paga
    pero no cambia nada mas del estado.

    Args:
        player_id: id del jugador.
        card_id: id de la carta en la tabla `cards`.
        mc_to_pay: MC que el jugador declara pagar.
        steel_to_pay: acero que el jugador declara pagar (0 si no aplica).
        titanium_to_pay: titanio que el jugador declara pagar (0 si no aplica).
        effect_amount: parametro X que algunas cartas piden (ej. Insulation:
            cuantos pasos de produccion de calor convertir a MC). None si la
            carta no lo necesita.
        effect_choice: indice (0-based) de la opcion elegida, para cartas con
            efecto "OR" (ej. Artificial Photosynthesis: 0 = +1 produccion de
            plantas, 1 = +2 produccion de energia). None si la carta no lo pide.

    Returns:
        dict con is_legal, el cambio (MC que sobraron, sin reembolso segun
        regla oficial) y el estado actualizado del jugador si la jugada es legal.

    TODO: el catalogo de cartas (`cards`) no viene precargado completo -- ver
    nota en rules_engine.py y en CLAUDE.md sobre por que no se generan datos
    de ~200 cartas automaticamente.
    """
    card_res = supabase.table("cards").select("*").eq("id", card_id).single().execute()
    card = card_res.data
    if card is None:
        raise ValueError(f"Carta '{card_id}' no encontrada en el catalogo")

    player = _load_player(player_id)

    if player["mc"] < mc_to_pay or player["steel"] < steel_to_pay or player["titanium"] < titanium_to_pay:
        raise engine.InsufficientResourcesError("El jugador no tiene el stock declarado")

    change = engine.calculate_card_payment(
        card_cost=card["cost"],
        mc_to_pay=mc_to_pay,
        steel_to_pay=steel_to_pay,
        titanium_to_pay=titanium_to_pay,
        card_tags=tuple(card.get("tags", [])),
    )

    paid_player = {
        **player,
        "mc": player["mc"] - mc_to_pay,
        "steel": player["steel"] - steel_to_pay,
        "titanium": player["titanium"] - titanium_to_pay,
    }
    new_player = engine.apply_card_effect(
        paid_player, card.get("effects") or {}, effect_amount, effect_choice
    )

    _save_player(player_id, new_player)
    _log_transaction(
        player_id, "play_card",
        {"card_id": card_id, "mc_to_pay": mc_to_pay, "steel_to_pay": steel_to_pay,
         "titanium_to_pay": titanium_to_pay, "change_not_refunded": change,
         "effect_amount": effect_amount, "effect_choice": effect_choice},
    )

    return {"is_legal": True, "change_not_refunded": change, "player": dict(new_player)}


@tool
def get_player_state(player_id: str) -> dict:
    """
    Devuelve el estado actual del jugador: recursos, produccion y TR.
    Usado tanto por el agente como por el dashboard del frontend.
    """
    player = _load_player(player_id)
    return dict(player)


# Lista de tools que se bindean al LLM en graph.py
ALL_TOOLS = [use_standard_project, convert_resources, run_production_phase, play_card, get_player_state]
