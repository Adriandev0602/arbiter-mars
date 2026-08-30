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
        active_cards=row.get("active_cards") or {},
        tags_played=row.get("tags_played") or {},
        passive_effects=row.get("passive_effects") or [],
        deck=row.get("deck") or [],
        hand=row.get("hand") or [],
        pending_research=row.get("pending_research") or [],
    )


def _save_player(player_id: str, player: engine.PlayerState) -> None:
    supabase.table("players").update(dict(player)).eq("id", player_id).execute()


def _load_global_parameters(game_id: str = "default") -> engine.GlobalParameters:
    res = supabase.table("global_parameters").select("*").eq("game_id", game_id).single().execute()
    row = res.data
    return engine.GlobalParameters(
        temperature=row["temperature"], oxygen=row["oxygen"], oceans_placed=row["oceans_placed"],
        city_tiles_placed=row.get("city_tiles_placed") or 0,
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
        new_player, new_globals = engine.standard_project_city(player, globals_)
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
    titanio solo cartas con tag 'space'. Exige que la carta este en la mano
    del jugador (`player.hand`, ver rules_engine seccion "Sistema de mazo /
    mano") -- lanza CardNotInHandError si no la tiene; para tenerla, primero
    hay que robarla via start_research_phase/resolve_research_phase, una
    accion con `draw_cards`, o deal_starting_hand al arrancar la partida.
    Despues del pago, aplica el efecto inmediato de la carta segun su
    columna `effects` (ver rules_engine.apply_card_effect) -- solo esta
    implementado para las cartas cargadas en seed_cards.sql; una carta con
    effects={} se paga pero no cambia nada mas del estado. Al final, saca
    la carta de la mano (ya se jugo).

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

    Ademas de aplicar el efecto: incrementa `tags_played` del jugador con los
    tags de esta carta (alimenta requisitos como "5 tags de ciencia"), y si
    `cards.effects.passive` esta definido, registra un efecto pasivo
    permanente (ej. Advanced Alloys: steel/titanio valen mas MC en pagos
    futuros; Media Group: +MC cada vez que se juega un evento). Si
    `cards.is_event` es true, dispara los bonus "on_event_played" de
    cualquier efecto pasivo que el jugador ya tenga activo.

    TODO: el catalogo de cartas (`cards`) no viene precargado completo -- ver
    nota en rules_engine.py y en CLAUDE.md sobre por que no se generan datos
    de ~200 cartas automaticamente.
    """
    card_res = supabase.table("cards").select("*").eq("id", card_id).single().execute()
    card = card_res.data
    if card is None:
        raise ValueError(f"Carta '{card_id}' no encontrada en el catalogo")

    globals_ = _load_global_parameters()
    player = _load_player(player_id)
    if card_id not in player["hand"]:
        raise engine.CardNotInHandError(f"El jugador no tiene '{card_id}' en la mano")
    engine.check_card_requirements(card.get("requirements"), globals_, player)

    if player["mc"] < mc_to_pay or player["steel"] < steel_to_pay or player["titanium"] < titanium_to_pay:
        raise engine.InsufficientResourcesError("El jugador no tiene el stock declarado")

    card_tags = tuple(card.get("tags", []))
    steel_value_mc, titanium_value_mc = engine.compute_conversion_rates(player)
    discount = engine.compute_card_cost_discount(player, card_tags)
    effective_cost = max(0, card["cost"] - discount)
    change = engine.calculate_card_payment(
        card_cost=effective_cost,
        mc_to_pay=mc_to_pay,
        steel_to_pay=steel_to_pay,
        titanium_to_pay=titanium_to_pay,
        card_tags=card_tags,
        steel_value_mc=steel_value_mc,
        titanium_value_mc=titanium_value_mc,
    )

    paid_player = {
        **player,
        "mc": player["mc"] - mc_to_pay,
        "steel": player["steel"] - steel_to_pay,
        "titanium": player["titanium"] - titanium_to_pay,
    }
    effects = card.get("effects") or {}
    new_player, new_globals = engine.apply_card_effect(
        paid_player, globals_, effects, effect_amount, effect_choice
    )
    if effects.get("becomes_active"):
        new_player = engine.register_active_card(new_player, card_id)
    if effects.get("passive"):
        new_player = engine.register_passive_effect(new_player, card_id, effects["passive"])

    new_player = engine.increment_tags_played(new_player, card_tags)
    if card.get("is_event"):
        new_player = engine.apply_event_played_bonuses(new_player, card_tags)
    new_player = engine.remove_card_from_hand(new_player, card_id)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    _log_transaction(
        player_id, "play_card",
        {"card_id": card_id, "mc_to_pay": mc_to_pay, "steel_to_pay": steel_to_pay,
         "titanium_to_pay": titanium_to_pay, "change_not_refunded": change,
         "cost_discount_applied": discount,
         "effect_amount": effect_amount, "effect_choice": effect_choice},
    )

    return {
        "is_legal": True, "change_not_refunded": change,
        "player": dict(new_player), "global_parameters": dict(new_globals),
    }


@tool
def use_card_action(player_id: str, card_id: str, effect_choice: int | None = None) -> dict:
    """
    Ejecuta la accion repetible de una carta que el jugador ya tiene activa
    (jugada previamente, con `effects.action` en su fila de `cards` -- ej.
    Ironworks: gastar 4 energia para ganar 1 acero y subir oxigeno 1 paso).
    Cada carta activa permite usar su accion una sola vez por generacion;
    run_production_phase la vuelve a habilitar.

    Args:
        player_id: id del jugador.
        card_id: id de la carta activa cuya accion se ejecuta.
        effect_choice: indice (0-based) de la opcion elegida, para acciones
            con eleccion (ej. Regolith Eaters: agregar 1 microbio O gastar 2
            para subir oxigeno). None si la accion no lo pide.

    Returns:
        dict con el estado actualizado del jugador y, si la accion afecto
        parametros globales (ej. subir oxigeno), tambien esos.

    Lanza CardEffectError si la carta no esta activa o su accion ya se uso
    esta generacion, InsufficientResourcesError si falta stock para pagarla.
    """
    card_res = supabase.table("cards").select("*").eq("id", card_id).single().execute()
    card = card_res.data
    if card is None:
        raise ValueError(f"Carta '{card_id}' no encontrada en el catalogo")

    action_spec = (card.get("effects") or {}).get("action")
    if action_spec is None:
        raise ValueError(f"La carta '{card_id}' no tiene una accion definida")

    player = _load_player(player_id)
    globals_ = _load_global_parameters()

    new_player, new_globals = engine.use_card_action(player, globals_, card_id, action_spec, effect_choice)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    _log_transaction(player_id, "use_card_action", {"card_id": card_id, "effect_choice": effect_choice})

    return {"player": dict(new_player), "global_parameters": dict(new_globals)}


@tool
def get_player_state(player_id: str) -> dict:
    """
    Devuelve el estado actual del jugador: recursos, produccion y TR.
    Usado tanto por el agente como por el dashboard del frontend.
    """
    player = _load_player(player_id)
    return dict(player)


@tool
def deal_starting_hand(player_id: str, hand_size: int = 10) -> dict:
    """
    Arma el mazo personal del jugador con TODO el catalogo disponible en
    `cards` (barajado), reparte `hand_size` cartas gratis a la mano inicial
    (regla oficial: 10 cartas al arrancar la partida, el jugador decide
    despues cuales quedarse via play_card -- las que no juegue quedan en la
    mano para siempre, no hay descarte de mano en este motor) y deja el
    resto en el mazo para futuras fases de investigacion. Se llama UNA vez
    por jugador, al arrancar la partida.

    Solo tiene sentido llamarla si el jugador todavia no tiene mazo (mazo y
    mano vacios) -- lanza CardEffectError si ya se repartio antes, para no
    volver a barajar y perder la mano/mazo actuales por accidente.

    Args:
        player_id: id del jugador.
        hand_size: cuantas cartas van directo a la mano (10 por regla oficial).

    Returns:
        dict con el estado actualizado del jugador.
    """
    player = _load_player(player_id)
    if player["deck"] or player["hand"]:
        raise engine.CardEffectError(
            "El jugador ya tiene mazo/mano armados -- no se puede repartir de nuevo"
        )

    all_card_ids = [row["id"] for row in supabase.table("cards").select("id").execute().data]
    deck = engine.initialize_deck(all_card_ids)
    new_player = {**player, "deck": deck}
    new_player = engine.draw_cards_to_hand(new_player, hand_size)

    _save_player(player_id, new_player)
    _log_transaction(player_id, "deal_starting_hand", {"hand_size": hand_size, "deck_size": len(all_card_ids)})

    return {"player": dict(new_player)}


@tool
def start_research_phase(player_id: str, n: int = 4) -> dict:
    """
    Roba `n` cartas del tope del mazo del jugador a una zona "pendiente"
    (`pending_research`), SIN cobrar nada todavia -- son las cartas que el
    usuario va a ver y decidir cuales comprar. Regla oficial: 4 cartas al
    inicio de cada generacion. Algunas cartas activas dan una version con
    otro N (ej. Inventors' Guild: n=1).

    Hay que llamar a resolve_research_phase despues para cerrar la fase
    (comprar algunas a 3 MC cada una, descartar el resto) -- no se puede
    iniciar una fase nueva mientras haya una pendiente sin resolver.

    Args:
        player_id: id del jugador.
        n: cuantas cartas robar (4 por regla oficial en investigacion normal).

    Returns:
        dict con el estado del jugador y la lista `pending_research` (los
        ids de las cartas robadas) para que el LLM se las muestre al usuario
        y le pregunte cuales quiere comprar.
    """
    player = _load_player(player_id)
    new_player = engine.start_research_phase(player, n)

    _save_player(player_id, new_player)
    _log_transaction(player_id, "start_research_phase", {"n": n, "drawn": new_player["pending_research"]})

    return {"player": dict(new_player), "pending_research": new_player["pending_research"]}


@tool
def resolve_research_phase(player_id: str, card_ids_to_buy: list[str], cost_per_card: int = 3) -> dict:
    """
    Cierra una fase de investigacion iniciada con start_research_phase.
    Compra las cartas en `card_ids_to_buy` (deben estar en
    `pending_research`) a `cost_per_card` MC cada una -- pasan a la mano del
    jugador. Las que no se compran se descartan (no vuelven al mazo). Elegir
    comprar 0 cartas es valido (lista vacia).

    Args:
        player_id: id del jugador.
        card_ids_to_buy: ids (subconjunto de pending_research) que el
            usuario decidio comprar.
        cost_per_card: MC por carta (3 en la investigacion normal; 0 para
            acciones gratuitas como Inventors' Guild -- pasar el valor que
            corresponda segun que disparo la fase).

    Returns:
        dict con el estado actualizado del jugador.

    Lanza ValueError si algun id no estaba en pending_research,
    InsufficientResourcesError si no alcanza el MC.
    """
    player = _load_player(player_id)
    new_player = engine.resolve_research_phase(player, card_ids_to_buy, cost_per_card)

    _save_player(player_id, new_player)
    _log_transaction(
        player_id, "resolve_research_phase",
        {"card_ids_to_buy": card_ids_to_buy, "cost_per_card": cost_per_card},
    )

    return {"player": dict(new_player)}


# Lista de tools que se bindean al LLM en graph.py
ALL_TOOLS = [
    use_standard_project, convert_resources, run_production_phase,
    play_card, use_card_action, get_player_state,
    deal_starting_hand, start_research_phase, resolve_research_phase,
]
