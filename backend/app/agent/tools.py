"""
Tools que el LLM puede invocar. Son wrappers delgados sobre agent/rules_engine.py
(la matematica real) mas el acceso a Supabase (el estado real del jugador).
El LLM llama estas funciones con argumentos extraidos de la consulta en
lenguaje natural -- nunca calcula los numeros el mismo.
"""
from langchain_core.tools import tool

from app.agent import board as boardlib
from app.agent import colonies as colonieslib
from app.agent import turmoil as turmoillib
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
        played_cards=row.get("played_cards") or [],
        pending_mc_discount=row.get("pending_mc_discount") or 0,
        pending_ocean_offers=row.get("pending_ocean_offers") or 0,
        pending_requirement_tolerance_steps=row.get("pending_requirement_tolerance_steps") or 0,
        reserved_cards=row.get("reserved_cards") or {},
        zero_tag_cards_played=row.get("zero_tag_cards_played") or 0,
        colonies_owned=row.get("colonies_owned") or [],
        trade_fleets=row.get("trade_fleets") if row.get("trade_fleets") is not None else 1,
        trade_fleets_used=row.get("trade_fleets_used") or 0,
        lobby_delegates=row.get("lobby_delegates") if row.get("lobby_delegates") is not None else 1,
        reserve_delegates=row.get("reserve_delegates") if row.get("reserve_delegates") is not None else 6,
    )


def _save_player(player_id: str, player: engine.PlayerState) -> None:
    supabase.table("players").update(dict(player)).eq("id", player_id).execute()


def _load_global_parameters(game_id: str = "default") -> engine.GlobalParameters:
    res = supabase.table("global_parameters").select("*").eq("game_id", game_id).single().execute()
    row = res.data
    return engine.GlobalParameters(
        temperature=row["temperature"], oxygen=row["oxygen"], oceans_placed=row["oceans_placed"],
        city_tiles_placed=row.get("city_tiles_placed") or 0,
        events_played=row.get("events_played") or 0,
        venus=row.get("venus") or 0,
    )


def _save_global_parameters(globals_: engine.GlobalParameters, game_id: str = "default") -> None:
    supabase.table("global_parameters").update(dict(globals_)).eq("game_id", game_id).execute()


def _log_transaction(player_id: str, action_type: str, detail: dict) -> None:
    supabase.table("transactions").insert(
        {"player_id": player_id, "action_type": action_type, "detail": detail}
    ).execute()


def _load_board(game_id: str = "default") -> boardlib.Board:
    """Trae el estado mutable del tablero (que hexagonos ya tienen tile)."""
    res = supabase.table("global_parameters").select("board").eq("game_id", game_id).single().execute()
    return res.data.get("board") or {}


def _save_board(board: boardlib.Board, game_id: str = "default") -> None:
    supabase.table("global_parameters").update({"board": board}).eq("game_id", game_id).execute()


def _load_colonies(game_id: str = "default") -> colonieslib.Colonies:
    """Trae el estado mutable de las Colony Tiles en juego (expansion Colonies)."""
    res = supabase.table("global_parameters").select("colonies").eq("game_id", game_id).single().execute()
    return res.data.get("colonies") or {}


def _save_colonies(colonies: colonieslib.Colonies, game_id: str = "default") -> None:
    supabase.table("global_parameters").update({"colonies": colonies}).eq("game_id", game_id).execute()


def _load_turmoil(game_id: str = "default") -> turmoillib.TurmoilState:
    """Trae el estado mutable de Turmoil (partidos/delegados/dominante/chairman)."""
    res = supabase.table("global_parameters").select("turmoil").eq("game_id", game_id).single().execute()
    stored = res.data.get("turmoil")
    return stored if stored else turmoillib.new_turmoil()


def _save_turmoil(turmoil: turmoillib.TurmoilState, game_id: str = "default") -> None:
    supabase.table("global_parameters").update({"turmoil": dict(turmoil)}).eq("game_id", game_id).execute()


def _apply_hex_bonus(player: engine.PlayerState, hex_bonus: list[tuple[str, int]]) -> engine.PlayerState:
    """
    Aplica el bonus impreso de un hexagono (steel/titanium/plant/card) al
    jugador que acaba de colocar un tile ahi. "card" roba esa cantidad de
    cartas del mazo directo a la mano (ver rules_engine.draw_cards_to_hand);
    el resto son deltas de stock directos.
    """
    new_player: dict = dict(player)
    for resource, amount in hex_bonus:
        if resource == "card":
            new_player = dict(engine.draw_cards_to_hand(new_player, amount))  # type: ignore[arg-type]
        elif resource == "plant":
            new_player["plants"] = new_player["plants"] + amount
        else:
            new_player[resource] = new_player[resource] + amount
    return new_player  # type: ignore[return-value]


def _place_ocean_and_apply_bonus(
    board: boardlib.Board, player: engine.PlayerState, hex_id: str, on_land: bool = False
) -> tuple[boardlib.Board, engine.PlayerState]:
    """
    on_land=True: para cartas como Artificial Lake, que colocan el oceano
    "en un area NO reservada para oceano" -- exactamente lo inverso de la
    colocacion normal (ver boardlib.place_ocean_tile_on_land).
    """
    place_fn = boardlib.place_ocean_tile_on_land if on_land else boardlib.place_ocean_tile
    new_board, hex_bonus, ocean_bonus_mc = place_fn(board, hex_id)
    new_player = _apply_hex_bonus(player, hex_bonus)
    new_player = {**new_player, "mc": new_player["mc"] + ocean_bonus_mc}
    return new_board, new_player  # type: ignore[return-value]


def _place_city_and_apply_bonus(
    board: boardlib.Board, player: engine.PlayerState, hex_id: str, owner_id: str,
    require_adjacent_cities: int | None = None, placement_bonus_multiplier: int = 1,
) -> tuple[boardlib.Board, engine.PlayerState]:
    """
    require_adjacent_cities: para cartas como Urbanized Area, que EXIGEN
    adyacencia a N ciudades ya existentes (lo inverso de la regla normal,
    ver boardlib.place_city_tile_adjacent_to_cities).
    """
    if require_adjacent_cities is not None:
        new_board, hex_bonus, ocean_bonus_mc = boardlib.place_city_tile_adjacent_to_cities(
            board, hex_id, owner_id, require_adjacent_cities
        )
    else:
        new_board, hex_bonus, ocean_bonus_mc = boardlib.place_city_tile(board, hex_id, owner_id)
    if placement_bonus_multiplier != 1:
        # Frontier Town: "gain the printed placement bonus 2 additional
        # times". Multiplica el bonus impreso del hex Y el de 2 MC por
        # oceano adyacente: el FAQ oficial (p.22) agrupa a los dos bajo la
        # misma categoria "D. Placement bonuses", sin distinguirlos.
        hex_bonus = [(resource, amount * placement_bonus_multiplier) for resource, amount in hex_bonus]
        ocean_bonus_mc *= placement_bonus_multiplier
    new_player = _apply_hex_bonus(player, hex_bonus)
    new_player = {**new_player, "mc": new_player["mc"] + ocean_bonus_mc}
    new_player = engine.apply_city_placed_bonuses(new_player)
    return new_board, new_player  # type: ignore[return-value]


def _apply_colony_gain(player: dict, key: str, amount: int, target_card_id: str | None) -> dict:
    """
    Aplica una ganancia de colonia (income, colony bonus o placement bonus).

    Las cinco colonias "simples" dan recursos de stock y les alcanza con sumar
    la clave al jugador, pero otras dan cosas que no viven en el stock:
      - "cards": ROBA N cartas del mazo (ej. Pluto: su trade income son
        cartas, no un recurso).
      - "card_resource:<tipo>": suma N recursos a UNA carta activa elegida
        (`target_card_id`), porque microbios/floaters/animales viven en cartas
        (ej. Enceladus microbios, Titan floaters, Miranda animales). Valida
        que la carta destino guarde ese tipo de recurso.
      - cualquier otra clave: recurso o produccion del jugador, suma directa.
    """
    if key == "cards":
        return dict(engine.draw_cards_to_hand(engine.PlayerState(**player), amount))
    if key.startswith("card_resource:"):
        resource_type = key.split(":", 1)[1]
        if target_card_id is None:
            raise ValueError(
                f"Esta colonia entrega {amount} {resource_type}(s) a una carta: falta target_card_id"
            )
        active = player["active_cards"]
        if target_card_id not in active:
            raise ValueError(f"La carta '{target_card_id}' no esta activa para este jugador")
        if active[target_card_id].get("resource_type") != resource_type:
            raise ValueError(f"'{target_card_id}' no guarda recursos de tipo '{resource_type}'")
        return {
            **player,
            "active_cards": {
                **active,
                target_card_id: {**active[target_card_id], "resources": active[target_card_id]["resources"] + amount},
            },
        }
    return {**player, key: player[key] + amount}


def _matches_required_tag(required_tag, card_tags: tuple[str, ...]) -> bool:
    """
    `required_tag` de un pasivo acepta un tag suelto o una LISTA de tags, en
    cuyo caso alcanza con que la carta tenga alguno (ej. Carbon Nanosystems:
    los graphenes pagan cartas con tag space O city). Mismo criterio que
    `tag_filter` en compute_card_cost_discount.
    """
    if isinstance(required_tag, list):
        return any(t in card_tags for t in required_tag)
    return required_tag in card_tags


def _place_greenery_and_apply_bonus(
    board: boardlib.Board, player: engine.PlayerState, hex_id: str, owner_id: str,
    ignore_restrictions: bool = False,
) -> tuple[boardlib.Board, engine.PlayerState]:
    new_board, hex_bonus, ocean_bonus_mc = boardlib.place_greenery_tile(
        board, hex_id, owner_id, ignore_restrictions=ignore_restrictions
    )
    new_player = _apply_hex_bonus(player, hex_bonus)
    new_player = {**new_player, "mc": new_player["mc"] + ocean_bonus_mc}
    new_player = engine.apply_greenery_placed_bonuses(new_player)
    return new_board, new_player  # type: ignore[return-value]


@tool
def use_standard_project(
    player_id: str, project_name: str, num_cards_to_sell: int = 0, hex_id: str | None = None
) -> dict:
    """
    Ejecuta uno de los 6 proyectos estandar de Terraforming Mars, siempre
    disponibles para cualquier jugador.

    Args:
        player_id: id del jugador.
        project_name: uno de 'sell_patents', 'power_plant', 'asteroid',
            'aquifer', 'greenery', 'city', 'air_scrapping' (expansion Venus
            Next: 15 MC, +1 paso de Venus).
        num_cards_to_sell: solo se usa si project_name == 'sell_patents';
            cantidad de cartas que el jugador descarta (1 MC cada una).
        hex_id: OBLIGATORIO para 'aquifer' (coloca oceano), 'greenery' (coloca
            greenery) y 'city' (coloca ciudad) -- el id del hexagono del mapa
            Tharsis (ver app.agent.board.HEX_DEFS, ids "03".."63") donde se
            coloca el tile. Ignorado para el resto de los proyectos.

    Returns:
        dict con el estado actualizado del jugador, los parametros globales
        y, si el proyecto coloco un tile, el bonus de hexagono/adyacencia
        oceanica que se aplico.

    Lanza InsufficientResourcesError si no alcanza el MC,
    GlobalParameterMaxedError si el parametro correspondiente ya esta al
    tope, ValueError si falta hex_id para un proyecto que lo requiere, y
    board.InvalidPlacementError / board.HexOccupiedError si el hexagono
    elegido no es legal para ese tile.
    """
    player = _load_player(player_id)
    globals_ = _load_global_parameters()
    board = None

    if project_name == "sell_patents":
        new_player = engine.standard_project_sell_patents(player, num_cards_to_sell)
        new_globals = globals_
    elif project_name == "power_plant":
        new_player = engine.standard_project_power_plant(player)
        new_globals = globals_
    elif project_name == "asteroid":
        new_player, new_globals = engine.standard_project_asteroid(player, globals_)
    elif project_name == "aquifer":
        if hex_id is None:
            raise ValueError("project_name 'aquifer' requiere hex_id (donde colocar el oceano)")
        board = _load_board()
        if not boardlib.can_place_ocean(board, hex_id):
            raise boardlib.InvalidPlacementError(f"No se puede colocar oceano en '{hex_id}'")
        new_player, new_globals = engine.standard_project_aquifer(player, globals_)
        board, new_player = _place_ocean_and_apply_bonus(board, new_player, hex_id)
    elif project_name == "greenery":
        if hex_id is None:
            raise ValueError("project_name 'greenery' requiere hex_id (donde colocar el greenery)")
        board = _load_board()
        if not boardlib.can_place_greenery(board, hex_id, player_id):
            raise boardlib.InvalidPlacementError(f"No se puede colocar greenery en '{hex_id}' para este jugador")
        new_player, new_globals = engine.standard_project_greenery(player, globals_)
        board, new_player = _place_greenery_and_apply_bonus(board, new_player, hex_id, player_id)
    elif project_name == "city":
        if hex_id is None:
            raise ValueError("project_name 'city' requiere hex_id (donde colocar la ciudad)")
        board = _load_board()
        if not boardlib.can_place_city(board, hex_id):
            raise boardlib.InvalidPlacementError(f"No se puede colocar ciudad en '{hex_id}'")
        new_player, new_globals = engine.standard_project_city(player, globals_)
        board, new_player = _place_city_and_apply_bonus(board, new_player, hex_id, player_id)
    elif project_name == "air_scrapping":
        new_player, new_globals = engine.standard_project_air_scrapping(player, globals_)
    else:
        raise ValueError(
            f"project_name debe ser uno de: sell_patents, power_plant, asteroid, "
            f"aquifer, greenery, city, air_scrapping. Recibido: {project_name}"
        )

    new_player = engine.apply_standard_project_used_bonuses(new_player, project_name)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    if board is not None:
        _save_board(board)
    _log_transaction(player_id, "standard_project", {"project_name": project_name, "hex_id": hex_id})

    return {"player": dict(new_player), "global_parameters": dict(new_globals)}


@tool
def convert_resources(player_id: str, conversion: str, hex_id: str | None = None) -> dict:
    """
    Ejecuta una conversion de recursos del tablero de jugador (no es un
    proyecto estandar, pero sigue reglas fijas iguales para todos).

    Args:
        player_id: id del jugador.
        conversion: 'plants_to_greenery' (gasta 8 plantas, sube oxigeno 1
            paso) o 'heat_to_temperature' (gasta 8 calor, sube temperatura
            1 paso).
        hex_id: OBLIGATORIO para 'plants_to_greenery' -- el hexagono del mapa
            Tharsis donde se coloca el tile de greenery. Ignorado para
            'heat_to_temperature' (no coloca tile).

    Returns:
        dict con el estado actualizado del jugador y los parametros globales.
    """
    player = _load_player(player_id)
    globals_ = _load_global_parameters()
    board = None

    if conversion == "plants_to_greenery":
        if hex_id is None:
            raise ValueError("conversion 'plants_to_greenery' requiere hex_id (donde colocar el greenery)")
        board = _load_board()
        if not boardlib.can_place_greenery(board, hex_id, player_id):
            raise boardlib.InvalidPlacementError(f"No se puede colocar greenery en '{hex_id}' para este jugador")
        new_player, new_globals = engine.convert_plants_to_greenery(player, globals_)
        board, new_player = _place_greenery_and_apply_bonus(board, new_player, hex_id, player_id)
    elif conversion == "heat_to_temperature":
        new_player, new_globals = engine.convert_heat_to_temperature(player, globals_)
    else:
        raise ValueError(
            f"conversion debe ser 'plants_to_greenery' o 'heat_to_temperature'. Recibido: {conversion}"
        )

    _save_player(player_id, new_player)
    _save_global_parameters(new_globals)
    if board is not None:
        _save_board(board)
    _log_transaction(player_id, "convert_resources", {"conversion": conversion, "hex_id": hex_id})

    return {"player": dict(new_player), "global_parameters": dict(new_globals)}


@tool
def run_production_phase(player_id: str, energy_to_convert: int | None = None) -> dict:
    """
    Corre la fase de produccion de fin de generacion para un jugador:
    convierte energia sobrante en calor y aplica toda su produccion
    (MC = TR + produccion de MC, y el resto de recursos suman su
    produccion correspondiente).

    Args:
        player_id: id del jugador.
        energy_to_convert: OPCIONAL, solo valido si el jugador tiene un
            pasivo que haga opcional la conversion de energia a calor (ej.
            Supercapacitors). Cuanta energia convertir; la que no se
            convierte queda en stock para la generacion siguiente. None
            (default) convierte toda la energia, que es la regla base.

    Returns:
        dict con el estado actualizado del jugador.
    """
    player = _load_player(player_id)
    new_player = engine.run_production_phase(player, energy_to_convert=energy_to_convert)
    new_player = {**new_player, "trade_fleets_used": 0}

    colonies = _load_colonies()
    if colonies:
        new_colonies = colonieslib.run_colony_production(colonies)
        _save_colonies(new_colonies)

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
    ocean_hex_ids: list[str] | None = None,
    city_hex_ids: list[str] | None = None,
    greenery_hex_id: str | None = None,
    special_tile_hex_id: str | None = None,
    discard_for_draw_card_id: str | None = None,
    duplicate_production_target_card_id: str | None = None,
    duplicate_production_target_card_ids: list[str] | None = None,
    retrieve_event_card_ids: list[str] | None = None,
    target_card_id: str | None = None,
    target_card_id_2: str | None = None,
    tag_played_choice: str | None = None,
    any_tag_played_choice: str | None = None,
    discard_card_id: str | None = None,
    build_colony_id: str | None = None,
    colony_id_increase: str | None = None,
    colony_id_decrease: str | None = None,
    card_resource_to_pay: int = 0,
    stock_resource_to_pay: int = 0,
    nomad_hex_id: str | None = None,
    wild_tag_choice: str | None = None,
    delegate_party_choices: list[str] | None = None,
    removal_party: str | None = None,
    target_card_id_3: str | None = None,
) -> dict:
    """
    Valida y paga una carta de proyecto contra su costo real en la tabla
    `cards`, respetando que acero solo cubre cartas con tag 'building' y
    titanio solo cartas con tag 'space'. Exige que la carta este en la mano
    del jugador (`player.hand`, ver rules_engine seccion "Sistema de mazo /
    mano") -- lanza CardNotInHandError si no la tiene; para tenerla, primero
    hay que robarla via start_research_phase/resolve_research_phase, una
    accion con `draw_cards`, o deal_starting_hand al arrancar la partida.
    Tambien acepta jugar una carta que este RESERVADA (ver
    `player.reserved_cards`, rules_engine.reserve_card_in_slot -- ej. Self-
    Replicating Robots) en vez de en la mano: en ese caso el costo se
    descuenta ademas en la cantidad de recursos acumulados sobre ella (ver
    rules_engine.compute_reserved_card_discount), y la reserva se libera al
    jugarla en vez de sacarla de la mano.
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
        ocean_hex_ids: OBLIGATORIO (con esa cantidad exacta de hex_ids) si la
            carta coloca oceano(s) (ej. Comet: 1; Lake Marineris: 2). None si
            la carta no coloca oceanos.
        city_hex_ids: igual que ocean_hex_ids pero para cartas que colocan
            ciudad(es) (ej. Capital: 1).
        greenery_hex_id: OBLIGATORIO si `effects.place_greenery` esta definido
            (ej. Protected Valley: coloca un greenery ignorando restricciones
            normales, incluso sobre un hex reservado a oceano). Distinto de
            standard_project_greenery/convert_plants_to_greenery (esos son
            acciones aparte, no un efecto de carta).
        special_tile_hex_id: OBLIGATORIO si `effects.place_special_tile` esta
            definido en la carta (ej. Mining Rights, Mining Area) -- el hex
            debe tener el bonus de recurso que pide la carta (steel/titanium)
            y, si la carta lo exige (Mining Area), ser adyacente a un tile
            propio. None si la carta no tiene esta mecanica.
        discard_for_draw_card_id: OPCIONAL -- si el jugador tiene un pasivo
            "on_tag_played_may_swap_card" activo que matchea alguno de los
            tags de la carta que se esta jugando (ej. Mars University: tag
            science), puede pasar el id de una carta de su mano para
            descartarla y robar 1 del mazo. None si no quiere ejercer la
            opcion (es siempre opcional, nunca obligatoria).
        tag_played_choice: OPCIONAL -- "add" o "spend", si el jugador tiene
            un pasivo "on_tag_played_choice" activo que matchea alguno de
            los tags de la carta que se esta jugando (ej. Olympus
            Conference: tag science). "add" suma un recurso a esa carta
            activa; "spend" gasta un recurso guardado ahi para robar 1
            carta. None si no quiere ejercer la opcion.
        duplicate_production_target_card_id: OBLIGATORIO si
            `effects.duplicate_production` esta definido en la carta (ej.
            Robotic Workforce) -- el id de una carta que el jugador ya jugo
            antes (debe estar en su historial `played_cards`) y que cumpla
            el tag requerido (ej. "building"). Se duplica su
            `production_deltas` una vez. None si la carta no tiene esta
            mecanica.
        target_card_id: OBLIGATORIO si `effects` (o la rama de `choice`
            elegida via effect_choice) tiene `target_card_resource_delta` --
            el id de OTRA carta ya activa del jugador (en `active_cards`) a
            la que se le agregan recursos (ej. Local Heat Trapping, Imported
            Hydrogen, Eos Chasma National Park). Tambien obligatorio si tiene
            `target_card_resource_delta_per_tag` Y el conteo de tags da mas
            de 0 (ej. Hydrogen to Venus: floaters por cada tag jovian -- si
            el jugador no tiene tags jovian, no hace falta pasar nada). None
            si la carta no tiene esta mecanica.
        target_card_id_2: OBLIGATORIO si `effects` tiene `target_card_resource_delta_2`
            -- una SEGUNDA carta activa distinta a la de target_card_id (ej.
            Imported Nitrogen: 3 microbios a una carta, 2 animales a otra).
            None si la carta no tiene esta mecanica.
        any_tag_played_choice: OPCIONAL -- "add" o "gain", si el jugador
            tiene un pasivo "on_any_tag_played_choice" activo que matchea
            alguno de los tags de la carta que se esta jugando (ej. Viral
            Enhancers: tags plant/microbe/animal, dispara incluso si la
            carta que dispara es esta misma). "add" suma un recurso a la
            carta RECIEN JUGADA (`card_id`, debe tener caja de recursos);
            "gain" suma el recurso propio que indique el pasivo (ej. +1
            planta). None si no quiere ejercer la opcion.
        discard_card_id: OBLIGATORIO si `effects.discard_card_then_draw` esta
            definido (ej. Sponsored Academies: descartar 1 carta de la mano
            y robar 3) -- el id de la carta a descartar (debe estar en la
            mano). None si la carta no tiene esta mecanica. Distinto de
            `discard_for_draw_card_id` (ese es para el pasivo opcional
            "on_tag_played_may_swap_card").
        build_colony_id: OBLIGATORIO si `effects.build_colony` esta definido
            (expansion Colonies, ej. Interplanetary Colony Ship, Ice Moon
            Colony -- "place a colony" como parte del efecto de la carta,
            SIN cobrar los 17 MC del proyecto estandar, ya incluidos en el
            costo de la carta) -- el id de `colonies.COLONY_DEFS`, debe
            estar en juego (ver tools.setup_colonies). Si `effects.build_colony`
            es `{"allow_duplicate": true}` en vez de `true` (ej. Research
            Colony, Space Port Colony: "may be placed where you already
            have a colony"), se ignora la restriccion normal de 1 colonia
            por jugador por tile. None si la carta no tiene esta mecanica.
        colony_id_increase: OBLIGATORIO junto con `colony_id_decrease` si
            `effects.adjust_colony_tracks` esta definido (ej. Market
            Manipulation: subir el track de una colonia 1 paso, bajar el
            de otra 1 paso) -- la colonia cuyo track sube. None si la
            carta no tiene esta mecanica.
        colony_id_decrease: la colonia cuyo track baja (ver
            `colony_id_increase`). Debe ser distinta de esa.
        card_resource_to_pay: cantidad de recurso guardado en una carta
            activa propia a usar como pago de esta carta (ej. Dirigibles:
            floaters a 3 M€ cada uno para cartas tag "venus"; Psychrophiles:
            microbios a 2 M€ cada uno para cartas tag "plant" -- ver pasivo
            "card_resource_payment" en rules_engine.register_passive_effect).
            El motor busca automaticamente, entre los pasivos activos del
            jugador, cual carta habilita pagar la carta que se esta jugando
            (segun sus tags) -- lanza ValueError si ninguna matchea o
            InsufficientResourcesError si esa carta no tiene suficiente
            recurso guardado. 0 si no se usa esta forma de pago.
        wild_tag_choice: OPCIONAL -- si la carta que se esta jugando tiene
            `requirements.min_tag_count` y el jugador tiene tags "wild" en
            juego (ej. Research Coordination), el tag que el jugador elige
            que esos tags "wild" representen para este chequeo puntual (ej.
            "science" para cubrir un requisito de Mass Converter). None si
            no aplica.
        delegate_party_choices: OBLIGATORIO (con esa cantidad exacta) si
            `effects.place_delegates_per_colony` esta definido (expansion
            Turmoil, ej. Colonial Envoys: "Place 1 delegate for each
            colony you have. You may place them in separate parties.") --
            lista de `turmoil.PARTY_NAMES`, uno por delegado a colocar (1
            por colonia propia), pueden repetirse. Sale de la Reserva del
            jugador (`player.reserve_delegates`), no del Lobby. None si la
            carta no tiene esta mecanica.

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
    played_from_reserve = card_id in player["reserved_cards"]
    if not played_from_reserve and card_id not in player["hand"]:
        raise engine.CardNotInHandError(f"El jugador no tiene '{card_id}' en la mano ni reservada")
    requirements = card.get("requirements") or {}
    turmoil = (
        _load_turmoil()
        if "ruling_or_delegates" in requirements
        or "party_leader_and_neutral_chairman" in requirements
        or "min_party_leader_count" in requirements
        else None
    )
    engine.check_card_requirements(
        requirements, globals_, player, wild_tag_choice=wild_tag_choice, turmoil=turmoil, player_id=player_id,
    )

    # Requisito de greeneries PROPIOS en el mapa: se resuelve aca y no en
    # el motor puro porque necesita el tablero (mismo criterio que
    # free_trade/duplicate_production) (ej. Harvest, bloque 34: 3 greeneries).
    min_greeneries = requirements.get("min_greenery_tiles_owned")
    if min_greeneries is not None:
        own_greeneries = boardlib.count_tiles_of_type(_load_board(), "greenery", owner=player_id)
        if own_greeneries < min_greeneries:
            raise engine.CardRequirementNotMetError(
                f"Requiere {min_greeneries} greenery(s) propios en el mapa, hay {own_greeneries}"
            )

    # Ciudades PROPIAS en el mapa. Distinto de `min_city_tiles`, que cuenta
    # el contador global de ciudades de CUALQUIER jugador (e incluye las de
    # fuera del mapa): estas cartas dicen "requires that YOU have N city
    # tiles" (ej. City Parks: 3; Casinos: 1), asi que se cuentan del tablero
    # filtrando por dueno, igual que min_greenery_tiles_owned.
    min_own_cities = requirements.get("min_own_city_tiles")
    if min_own_cities is not None:
        own_cities = boardlib.count_tiles_of_type(_load_board(), "city", owner=player_id)
        if own_cities < min_own_cities:
            raise engine.CardRequirementNotMetError(
                f"Requiere {min_own_cities} ciudad(es) propias en el mapa, hay {own_cities}"
            )

    # Ciudad adyacente a oceano: de cualquier jugador (Outdoor Sports) o
    # propia (Aqueduct Systems). Tambien necesita el tablero, igual que el
    # requisito de greeneries de arriba.
    if requirements.get("any_city_adjacent_to_ocean"):
        if not boardlib.has_city_adjacent_to_ocean(_load_board()):
            raise engine.CardRequirementNotMetError(
                "Requiere alguna ciudad en el mapa adyacente a un oceano"
            )
    if requirements.get("own_city_adjacent_to_ocean"):
        if not boardlib.has_city_adjacent_to_ocean(_load_board(), owner=player_id):
            raise engine.CardRequirementNotMetError(
                "Requiere una ciudad PROPIA adyacente a un oceano"
            )

    if player["mc"] < mc_to_pay or player["steel"] < steel_to_pay or player["titanium"] < titanium_to_pay:
        raise engine.InsufficientResourcesError("El jugador no tiene el stock declarado")

    # Snapshot para el pasivo "on_card_resource_gained" (ej. Meat Industry:
    # +2 MC por cada animal ganado en cualquier carta) -- se compara contra
    # el estado final de la jugada, ver engine.apply_card_resource_gained_bonuses.
    card_resource_totals_before = engine.snapshot_card_resource_totals(player)
    active_cards_before = dict(player["active_cards"])

    card_tags = tuple(card.get("tags", []))
    steel_value_mc, titanium_value_mc = engine.compute_conversion_rates(player)

    card_resource_source_id = None
    card_resource_discount = 0
    if card_resource_to_pay > 0:
        match = next(
            (
                p for p in player["passive_effects"]
                if "card_resource_payment" in p
                and _matches_required_tag(p["card_resource_payment"]["required_tag"], card_tags)
            ),
            None,
        )
        if match is None:
            raise ValueError(
                f"Ninguna carta activa del jugador permite pagar '{card_id}' con recurso guardado"
            )
        card_resource_source_id = match["card_id"]
        card_resource_value_mc = match["card_resource_payment"].get("value_mc", 3)
        card_resource_discount = card_resource_to_pay * card_resource_value_mc

    # Pago con un recurso de STOCK distinto de acero/titanio (Martian Lumber
    # Corp, X60 bloque 36: las plantas valen 3 M€ al jugar cartas building).
    # Es la cuarta forma de pago: acero/titanio estan cableados en el motor,
    # `card_resource_to_pay` gasta recursos guardados en una carta, y esto
    # gasta stock normal del jugador habilitado por un pasivo.
    stock_resource_discount = 0
    stock_resource_key = None
    if stock_resource_to_pay > 0:
        match = next(
            (
                p for p in player["passive_effects"]
                if "stock_resource_payment" in p
                and _matches_required_tag(p["stock_resource_payment"]["required_tag"], card_tags)
            ),
            None,
        )
        if match is None:
            raise ValueError(
                f"Ningun pasivo del jugador permite pagar '{card_id}' con un recurso de stock"
            )
        stock_resource_key = match["stock_resource_payment"]["resource"]
        if player[stock_resource_key] < stock_resource_to_pay:
            raise engine.InsufficientResourcesError(
                f"El jugador tiene {player[stock_resource_key]} de {stock_resource_key}, "
                f"declaro pagar {stock_resource_to_pay}"
            )
        stock_resource_discount = stock_resource_to_pay * match["stock_resource_payment"].get("value_mc", 1)

    discount = (
        engine.compute_card_cost_discount(player, card_tags, has_requirement=bool(requirements))
        + player["pending_mc_discount"]
        + engine.compute_reserved_card_discount(player, card_id)
        + card_resource_discount
        + stock_resource_discount
    )
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
        # Se consume el descuento/tolerancia pendiente al jugar esta carta
        # (los haya cubierto entera o no) -- antes de aplicar el efecto de
        # ESTA carta, para no borrar un next_card_discount_mc/
        # next_card_requirement_tolerance_steps que ella misma otorgue.
        "pending_mc_discount": 0,
        "pending_requirement_tolerance_steps": 0,
    }
    if card_resource_source_id is not None:
        paid_player = engine.spend_active_card_resource(paid_player, card_resource_source_id, card_resource_to_pay)
    if stock_resource_key is not None:
        paid_player = {**paid_player, stock_resource_key: paid_player[stock_resource_key] - stock_resource_to_pay}
    effects = card.get("effects") or {}

    # Se registra como activa/pasiva ANTES de aplicar el efecto (que puede
    # colocar oceano/ciudad/greenery mas abajo) para que los pasivos "se
    # dispara al colocar X, incluida esta" (ej. Immigrant City:
    # on_city_tile_placed_production_delta) se autodisparen con su propia
    # colocacion, igual que on_tag_played_add_resource ya se autodispara
    # con el propio tag (ver apply_tag_played_resource_bonuses mas abajo).
    if effects.get("becomes_active"):
        paid_player = engine.register_active_card(
            paid_player, card_id,
            initial_resources=engine.resolve_active_card_starting_resources(paid_player, effects),
            resource_type=effects.get("active_card_resource_type"),
        )
    if effects.get("passive"):
        paid_player = engine.register_passive_effect(paid_player, card_id, effects["passive"])

    new_player, new_globals = engine.apply_card_effect(
        paid_player, globals_, effects, effect_amount, effect_choice,
        target_card_id=target_card_id, target_card_id_2=target_card_id_2,
        target_card_id_3=target_card_id_3, discard_card_id=discard_card_id,
    )

    # El efecto resuelto (incluso detras de choice/tag_count_choice) puede
    # haber colocado oceano(s)/ciudad(es) -- se detecta comparando el
    # contador global antes/despues, sin tener que re-inspeccionar `effects`
    # (salvo "place_city_tiles": ese es un contador SIN mapa -- ver seccion
    # 3 de AGENTS.md, "areas de ciudad fuera de tablero" -- y no debe pedir
    # hex_id; se resta su cantidad para no confundirlo con una ciudad real
    # en el tablero, bug encontrado en la prueba de humo del bloque 32 al
    # cargar Stanford Torus).
    oceans_delta = new_globals["oceans_placed"] - globals_["oceans_placed"]
    cities_delta = (
        new_globals["city_tiles_placed"] - globals_["city_tiles_placed"] - effects.get("place_city_tiles", 0)
    )
    board = None
    if oceans_delta > 0 or cities_delta > 0:
        board = _load_board()
    if oceans_delta > 0:
        chosen = ocean_hex_ids or []
        if len(chosen) != oceans_delta:
            raise ValueError(
                f"Esta carta coloca {oceans_delta} oceano(s); se recibieron {len(chosen)} hex_id(s)"
            )
        on_land = bool(effects.get("ocean_placement_bypasses_reservation"))
        can_place_fn = boardlib.can_place_ocean_on_land if on_land else boardlib.can_place_ocean
        for hid in chosen:
            if not can_place_fn(board, hid):
                raise boardlib.InvalidPlacementError(f"No se puede colocar oceano en '{hid}'")
            board, new_player = _place_ocean_and_apply_bonus(board, new_player, hid, on_land=on_land)
    if cities_delta > 0:
        chosen = city_hex_ids or []
        if len(chosen) != cities_delta:
            raise ValueError(
                f"Esta carta coloca {cities_delta} ciudad(es); se recibieron {len(chosen)} hex_id(s)"
            )
        require_adjacent_cities = effects.get("city_placement_requires_adjacent_cities")
        on_volcanic = effects.get("city_placement_on_volcanic")
        for hid in chosen:
            if require_adjacent_cities is not None:
                if not boardlib.can_place_city_adjacent_to_cities(board, hid, require_adjacent_cities):
                    raise boardlib.InvalidPlacementError(
                        f"'{hid}' no es adyacente a al menos {require_adjacent_cities} ciudad(es)"
                    )
            elif on_volcanic:
                if not boardlib.can_place_city_on_volcanic(board, hid):
                    raise boardlib.InvalidPlacementError(f"'{hid}' no es un hexagono volcanico vacio")
            elif not boardlib.can_place_city(board, hid):
                raise boardlib.InvalidPlacementError(f"No se puede colocar ciudad en '{hid}'")
            board, new_player = _place_city_and_apply_bonus(
                board, new_player, hid, player_id, require_adjacent_cities=require_adjacent_cities,
                placement_bonus_multiplier=effects.get("city_placement_bonus_multiplier", 1),
            )

    special_tile_spec = effects.get("place_special_tile")
    if special_tile_spec is not None:
        if special_tile_hex_id is None:
            raise ValueError(f"La carta '{card_id}' requiere special_tile_hex_id")
        if board is None:
            board = _load_board()
        board, hex_bonus, ocean_bonus_mc = boardlib.place_special_tile(
            board, special_tile_hex_id, special_tile_spec, player_id, card_id
        )
        # Si la carta pide un hex con bonus de recurso especifico (ej. Mining
        # Rights), ese bonus se convierte en produccion permanente del
        # recurso que matchea (no se aplica como stock de una sola vez).
        # Cartas como Industrial Center no tienen hex_bonus_resource -- solo
        # exigen la posicion (adyacente a una ciudad) y ganan su efecto por
        # otro lado (ej. su propia accion repetible), sin bump automatico aca.
        if "hex_bonus_resource" in special_tile_spec:
            resource_bumped = next(r for r, _ in hex_bonus if r in special_tile_spec["hex_bonus_resource"])
            production_key = f"{resource_bumped}_production"
            new_player, new_globals = engine.apply_card_effect(
                new_player, new_globals, {"production_deltas": {production_key: 1}}
            )
        new_player = {**new_player, "mc": new_player["mc"] + ocean_bonus_mc}

    if effects.get("mc_per_empty_hex_adjacent_to_own_tiles"):
        # Red Tourism Wave (T12, Turmoil, bloque 31): "Gain 1 M€ for each
        # EMPTY AREA ADJACENT TO YOUR TILES." Ver
        # board.count_empty_hexes_adjacent_to_owner.
        if board is None:
            board = _load_board()
        empty_adjacent = boardlib.count_empty_hexes_adjacent_to_owner(board, player_id)
        new_player = {**new_player, "mc": new_player["mc"] + empty_adjacent}

    build_colony_spec = effects.get("build_colony")
    if build_colony_spec:
        if build_colony_id is None:
            raise ValueError(f"La carta '{card_id}' requiere build_colony_id")
        allow_duplicate = isinstance(build_colony_spec, dict) and bool(build_colony_spec.get("allow_duplicate"))
        colonies = _load_colonies()
        new_colonies, placement_bonus = colonieslib.build_colony(
            colonies, build_colony_id, player_id, allow_duplicate=allow_duplicate,
        )
        new_player = {**new_player, "colonies_owned": [*new_player["colonies_owned"], build_colony_id]}
        for key, delta in placement_bonus.items():
            new_player[key] = new_player[key] + delta
        _save_colonies(new_colonies)

    if effects.get("convert_own_greenery_to_city"):
        # Kaguya Tech (X58): saca un greenery PROPIO y pone una ciudad en ese
        # mismo hexagono, ignorando la restriccion de adyacencia entre
        # ciudades y SIN tocar el oxigeno (lo aclara el texto de la carta).
        # Los bonus de colocacion se cobran normal.
        if greenery_hex_id is None:
            raise ValueError(f"La carta '{card_id}' requiere greenery_hex_id (el greenery a convertir)")
        if board is None:
            board = _load_board()
        board = boardlib.remove_greenery_tile(board, greenery_hex_id, player_id)
        board, new_player = _place_city_and_apply_bonus(board, new_player, greenery_hex_id, player_id)
        new_globals = dict(engine.place_city_tile(engine.GlobalParameters(**new_globals)))

    if effects.get("place_nomads"):
        # Mars Nomads (X59): coloca el marcador en un hexagono vacio. No
        # otorga bonus al colocarse, solo al moverlo (ver use_card_action).
        if nomad_hex_id is None:
            raise ValueError(f"La carta '{card_id}' requiere nomad_hex_id")
        if board is None:
            board = _load_board()
        board = boardlib.place_nomads(board, nomad_hex_id)

    if effects.get("adjust_colony_tracks"):
        if colony_id_increase is None or colony_id_decrease is None:
            raise ValueError(f"La carta '{card_id}' requiere colony_id_increase y colony_id_decrease")
        if colony_id_increase == colony_id_decrease:
            raise ValueError("colony_id_increase y colony_id_decrease deben ser distintas")
        colonies = _load_colonies()
        colonies = colonieslib.adjust_colony_track(colonies, colony_id_increase, 1)
        colonies = colonieslib.adjust_colony_track(colonies, colony_id_decrease, -1)
        _save_colonies(colonies)

    if effects.get("gain_all_colony_bonuses"):
        for colony_id in new_player["colonies_owned"]:
            for key, delta in colonieslib.COLONY_DEFS[colony_id]["colony_bonus"].items():
                new_player[key] = new_player[key] + delta

    if effects.get("mc_per_colony_in_play"):
        colonies_in_play = _load_colonies()
        new_player = {**new_player, "mc": new_player["mc"] + len(colonies_in_play)}

    production_per_colony_spec = effects.get("production_delta_per_colony_in_play")
    if production_per_colony_spec:
        colonies_in_play = _load_colonies()
        key = production_per_colony_spec["production"]
        delta = len(colonies_in_play) * production_per_colony_spec.get("per_colony", 1)
        new_player = {**new_player, key: engine._apply_production_floor(key, new_player[key] + delta)}

    # Dos formas de colocar delegados desde una carta: 1 por colonia propia
    # (place_delegates_per_colony) o una cantidad FIJA (place_delegates). Las
    # dos gastan de la Reserva y exigen `delegate_party_choices` con el largo
    # exacto -- las parties pueden repetirse (ej. Cultural Metropolis: "place
    # 2 delegates in 1 party").
    num_delegates = 0
    if effects.get("place_delegates_per_colony"):
        num_delegates = len(new_player["colonies_owned"])
    elif effects.get("place_delegates"):
        num_delegates = effects["place_delegates"]
    if num_delegates:
        chosen_parties = delegate_party_choices or []
        if len(chosen_parties) != num_delegates:
            raise ValueError(
                f"Esta carta coloca {num_delegates} delegado(s); "
                f"se recibieron {len(chosen_parties)} party(s)"
            )
        if new_player["reserve_delegates"] < num_delegates:
            raise engine.InsufficientResourcesError(
                f"El jugador tiene {new_player['reserve_delegates']} delegados en la Reserva, se necesitan {num_delegates}"
            )
        turmoil = turmoil if turmoil is not None else _load_turmoil()
        for party in chosen_parties:
            turmoil = turmoillib.place_delegate(turmoil, party, player_id)
        new_player = {**new_player, "reserve_delegates": new_player["reserve_delegates"] - num_delegates}
        _save_turmoil(turmoil)

    if effects.get("remove_own_delegate"):
        if removal_party is None:
            raise ValueError(f"La carta '{card_id}' requiere removal_party")
        turmoil = turmoil if turmoil is not None else _load_turmoil()
        turmoil = turmoillib.remove_delegate(turmoil, removal_party, player_id)
        new_player = {**new_player, "reserve_delegates": new_player["reserve_delegates"] + 1}
        _save_turmoil(turmoil)

    if effects.get("become_chairman_from_neutral"):
        # Vote of No Confidence (T16, bloque 31): requisito
        # "party_leader_and_neutral_chairman" ya garantizo chairman neutral.
        # Mueve 1 delegado propio de la Reserva a la silla de Chairman y
        # gana 1 TR (regla real de la carta) -- turmoil.py no modela
        # delegados neutrales en partidos, pero el Chairman SI tiene un
        # estado neutral explicito (`chairman is None`), asi que esta carta
        # no necesita esa pieza mas grande (ver "Pendientes" para
        # Recruitment, que si la necesita).
        if new_player["reserve_delegates"] < 1:
            raise engine.InsufficientResourcesError(
                f"El jugador tiene {new_player['reserve_delegates']} delegados en la Reserva, se necesita 1"
            )
        turmoil = turmoil if turmoil is not None else _load_turmoil()
        turmoil = dict(turmoil)
        turmoil["chairman"] = player_id
        new_player = {
            **new_player,
            "reserve_delegates": new_player["reserve_delegates"] - 1,
            "tr": new_player["tr"] + 1,
        }
        _save_turmoil(turmoil)  # type: ignore[arg-type]

    if effects.get("reset_card_action_used"):
        # Project Inspection (X02, bloque 31): "use a card action that has
        # already been used this generation". En vez de re-ejecutar la
        # accion adentro de play_card (duplicaria toda la logica de
        # use_card_action), esta carta solo REHABILITA la accion elegida
        # (`target_card_id`, obligatorio) -- el jugador la usa despues con
        # una llamada normal a use_card_action.
        if target_card_id is None:
            raise ValueError(f"La carta '{card_id}' requiere target_card_id")
        if target_card_id not in new_player["active_cards"]:
            raise ValueError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        new_active_cards = dict(new_player["active_cards"])
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id], "action_used": False,
        }
        new_player = {**new_player, "active_cards": new_active_cards}

    draw_tag_spec = effects.get("draw_cards_matching_tag")
    if draw_tag_spec is not None:
        specs = draw_tag_spec if isinstance(draw_tag_spec, list) else [draw_tag_spec]
        for spec in specs:
            new_player = _draw_cards_matching_tag(new_player, spec["tag"], spec["n"])

    greenery_spec = effects.get("place_greenery")
    if greenery_spec is not None:
        if greenery_hex_id is None:
            raise ValueError(f"La carta '{card_id}' requiere greenery_hex_id")
        if board is None:
            board = _load_board()
        board, new_player = _place_greenery_and_apply_bonus(
            board, new_player, greenery_hex_id, player_id,
            ignore_restrictions=greenery_spec.get("ignore_restrictions", False),
        )

    # Dispara bonus pasivos por tags jugados (ej. Ecological Zone, Decomposers)
    new_player = engine.apply_tag_played_resource_bonuses(new_player, card_tags)

    duplicate_spec = effects.get("duplicate_production")
    if duplicate_spec is not None:
        # `count` (default 1) permite duplicar la caja de produccion de MAS de
        # una carta jugada (ej. Cyberia Systems, bloque 35: 2 cartas building).
        # Con count > 1 hay que pasar `duplicate_production_target_card_ids`,
        # que ademas deben ser cartas DISTINTAS entre si.
        count = duplicate_spec.get("count", 1)
        if count > 1:
            chosen = duplicate_production_target_card_ids or []
            if len(chosen) != count:
                raise ValueError(
                    f"La carta '{card_id}' duplica la produccion de {count} cartas; "
                    f"se recibieron {len(chosen)}"
                )
            if len(set(chosen)) != len(chosen):
                raise ValueError("Las cartas a duplicar deben ser distintas entre si")
        else:
            if duplicate_production_target_card_id is None:
                raise ValueError(f"La carta '{card_id}' requiere duplicate_production_target_card_id")
            chosen = [duplicate_production_target_card_id]

        required_tag = duplicate_spec.get("requires_tag")
        for target_id in chosen:
            if target_id not in new_player["played_cards"]:
                raise ValueError(f"'{target_id}' no esta entre las cartas jugadas por el jugador")
            target_res = supabase.table("cards").select("*").eq("id", target_id).single().execute()
            target_card = target_res.data
            if target_card is None:
                raise ValueError(f"Carta '{target_id}' no encontrada en el catalogo")
            if required_tag is not None and required_tag not in (target_card.get("tags") or []):
                raise ValueError(f"'{target_id}' no tiene el tag requerido '{required_tag}'")
            target_production = (target_card.get("effects") or {}).get("production_deltas")
            if not target_production:
                raise ValueError(f"'{target_id}' no tiene una caja de produccion para duplicar")
            new_player, new_globals = engine.apply_card_effect(
                new_player, new_globals, {"production_deltas": target_production}
            )

    retrieve_spec = effects.get("retrieve_played_events_to_hand")
    if retrieve_spec is not None:
        # Astra Mechanica (X51, bloque 35): "choose 2 project cards from your
        # EVENT PILE and take them to hand. It may not be cards that place
        # special tiles". La "pila de eventos" no es un campo aparte: es
        # `played_cards` filtrado por `cards.is_event` del catalogo -- por eso
        # se resuelve aca y no en el motor puro (mismo criterio que
        # duplicate_production).
        count = retrieve_spec.get("count", 1)
        chosen = retrieve_event_card_ids or []
        if len(chosen) != count:
            raise ValueError(
                f"La carta '{card_id}' recupera {count} evento(s) jugados; se recibieron {len(chosen)}"
            )
        if len(set(chosen)) != len(chosen):
            raise ValueError("Los eventos a recuperar deben ser distintos entre si")
        for event_id in chosen:
            if event_id not in new_player["played_cards"]:
                raise ValueError(f"'{event_id}' no esta entre las cartas jugadas por el jugador")
            event_res = supabase.table("cards").select("*").eq("id", event_id).single().execute()
            event_card = event_res.data
            if event_card is None:
                raise ValueError(f"Carta '{event_id}' no encontrada en el catalogo")
            if not event_card.get("is_event"):
                raise ValueError(f"'{event_id}' no es un evento: no esta en la pila de eventos")
            if retrieve_spec.get("exclude_special_tile_cards") and (
                (event_card.get("effects") or {}).get("place_special_tile") is not None
            ):
                raise ValueError(f"'{event_id}' coloca un special tile: esta carta no permite recuperarla")
            new_player = {**new_player, "hand": [*new_player["hand"], event_id]}

    new_player = engine.increment_tags_played(new_player, card_tags)
    new_player = engine.increment_zero_tag_cards_played(new_player, card_tags)
    for effect in new_player["passive_effects"]:
        threshold_spec = effect.get("on_card_played_cost_threshold_draw")
        if threshold_spec is not None and card["cost"] >= threshold_spec["min_cost"]:
            new_player = engine.draw_cards_to_hand(new_player, threshold_spec.get("draw", 1))
        production_threshold_spec = effect.get("on_card_played_cost_threshold_production_delta")
        if production_threshold_spec is not None and card["cost"] >= production_threshold_spec["min_cost"]:
            # Advertising (X13, bloque 32): "when you play a card with a
            # basic cost of 20+, +1 MC production" -- mismo patron que
            # on_card_played_cost_threshold_draw (bloque 29), pero suma
            # produccion en vez de robar cartas. `card["cost"]` es el costo
            # IMPRESO del catalogo, no el efectivo pagado con descuentos.
            key = production_threshold_spec["production"]
            new_player = {
                **new_player,
                key: engine._apply_production_floor(key, new_player[key] + production_threshold_spec.get("delta", 1)),
            }
    if card.get("is_event"):
        new_player = engine.apply_event_played_bonuses(new_player, card_tags)
        new_globals = engine.increment_events_played(new_globals)
    if played_from_reserve:
        new_player = engine.release_reserved_card(new_player, card_id)
    else:
        new_player = engine.remove_card_from_hand(new_player, card_id)
    new_player = engine.register_played_card(new_player, card_id)

    if discard_for_draw_card_id is not None:
        if not engine.player_has_tag_swap_passive(new_player, card_tags):
            raise ValueError(
                f"El jugador no tiene un pasivo activo que ofrezca descartar/robar para tags {card_tags}"
            )
        new_player = engine.swap_card_for_draw(new_player, discard_for_draw_card_id)

    new_player = engine.apply_tag_played_choice(new_player, card_tags, tag_played_choice)
    new_player = engine.apply_any_tag_played_choice(new_player, card_id, card_tags, any_tag_played_choice)
    new_player = engine.apply_card_resource_gained_bonuses(new_player, card_resource_totals_before, active_cards_before)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    if board is not None:
        _save_board(board)
    _log_transaction(
        player_id, "play_card",
        {"card_id": card_id, "mc_to_pay": mc_to_pay, "steel_to_pay": steel_to_pay,
         "titanium_to_pay": titanium_to_pay, "change_not_refunded": change,
         "cost_discount_applied": discount,
         "effect_amount": effect_amount, "effect_choice": effect_choice,
         "ocean_hex_ids": ocean_hex_ids, "city_hex_ids": city_hex_ids, "greenery_hex_id": greenery_hex_id,
         "special_tile_hex_id": special_tile_hex_id, "discard_for_draw_card_id": discard_for_draw_card_id,
         "duplicate_production_target_card_id": duplicate_production_target_card_id,
         "target_card_id": target_card_id, "target_card_id_2": target_card_id_2,
         "tag_played_choice": tag_played_choice, "any_tag_played_choice": any_tag_played_choice,
         "discard_card_id": discard_card_id, "build_colony_id": build_colony_id,
         "colony_id_increase": colony_id_increase, "colony_id_decrease": colony_id_decrease},
    )

    return {
        "is_legal": True, "change_not_refunded": change,
        "player": dict(new_player), "global_parameters": dict(new_globals),
    }


@tool
def use_card_action(
    player_id: str,
    card_id: str,
    effect_choice: int | None = None,
    ocean_hex_ids: list[str] | None = None,
    target_card_id: str | None = None,
    effect_amount: int | None = None,
    reserved_card_id: str | None = None,
    titanium_to_pay: int = 0,
    trade_colony_id: str | None = None,
    removal_parties: list[str] | None = None,
    delegate_party_choices: list[str] | None = None,
    steel_to_pay: int = 0,
    nomad_hex_id: str | None = None,
    city_hex_id: str | None = None,
) -> dict:
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
        ocean_hex_ids: OBLIGATORIO (con esa cantidad exacta) si la accion
            coloca oceano(s) (ej. Water Import from Europa: 1). None si la
            accion no coloca oceanos.
        target_card_id: OBLIGATORIO si la accion agrega recursos a otra carta
            activa (ej. Symbiotic Fungus: 1 microbio; Extreme-Cold Fungus: 2)
            o MUEVE recursos desde otra carta activa hacia esta (ej.
            Predators: 1 animal; Ants: 1 microbio). None si la accion no
            afecta otra carta.
        effect_amount: OBLIGATORIO si `effects.action.convert_resource_amount`
            esta definido (ej. Power Infrastructure: cuanta energia
            convertir a MC, 1 a 1). None si la accion no lo pide.
        reserved_card_id: OBLIGATORIO si `effects.action.reserve_card_from_hand`
            o `effects.action.duplicate_reserved_card` esta definido (ej.
            Self-Replicating Robots) -- para "reserve_card_from_hand", el id
            de una carta en la MANO del jugador con el tag que exija la
            accion (`requires_tag_any`, ej. space o building); para
            "duplicate_reserved_card", el id de una carta ya reservada por
            esta misma carta. None si la accion no tiene esta mecanica.
        titanium_to_pay: OPCIONAL, solo si `effects.action.cost.mc_or_titanium`
            esta definido -- cuanto titanio declara pagar el jugador hacia
            ese costo (el resto se cubre con MC del stock). 0 (default) paga
            todo en MC.
        trade_colony_id: OBLIGATORIO si `effects.action.gains.free_trade`
            esta definido (expansion Colonies, ej. Titan Floating
            Launch-Pad: "spend 1 floater here to trade for free") -- el id
            de `colonies.COLONY_DEFS` con el que comerciar, debe estar en
            juego y libre de flota. Comercia SIN cobrar el costo normal de
            9 MC/3 energia/3 titanio ni gastar una flota de comercio propia
            -- el costo real de esta accion es el que declare
            `effects.action.cost` de la carta (ej. 1 floater guardado).
            None si la accion no tiene esta mecanica.

    Returns:
        dict con el estado actualizado del jugador y, si la accion afecto
        parametros globales (ej. subir oxigeno), tambien esos.

    Lanza CardEffectError si la carta no esta activa o su accion ya se uso
    esta generacion, InsufficientResourcesError si falta stock para pagarla.
    """
    card_res = supabase.table("cards").select("*").eq("id", card_id).maybe_single().execute()
    card = card_res.data if card_res else None
    if card is None:
        # Las preludes tambien pueden quedarse en juego con accion repetible
        # (ej. Applied Science, Floating Trade Hub), y viven en su propia
        # tabla porque no tienen costo ni requisitos -- ver play_prelude.
        prelude_res = supabase.table("prelude_cards").select("*").eq("id", card_id).maybe_single().execute()
        card = prelude_res.data if prelude_res else None
    if card is None:
        raise ValueError(f"Carta '{card_id}' no encontrada en el catalogo (ni en `cards` ni en `prelude_cards`)")

    action_spec = (card.get("effects") or {}).get("action")
    if action_spec is None:
        raise ValueError(f"La carta '{card_id}' no tiene una accion definida")

    player = _load_player(player_id)
    globals_ = _load_global_parameters()
    # Ver el mismo snapshot en play_card: pasivo "on_card_resource_gained".
    card_resource_totals_before = engine.snapshot_card_resource_totals(player)
    active_cards_before = dict(player["active_cards"])

    resolved_spec = action_spec
    if effect_choice is not None and "choice" in (action_spec or {}):
        options = action_spec["choice"]
        if 0 <= effect_choice < len(options):
            resolved_spec = options[effect_choice]

    reserve_spec = resolved_spec.get("gains", {}).get("reserve_card_from_hand")
    if reserve_spec is not None:
        if reserved_card_id is None:
            raise ValueError(f"La accion de '{card_id}' requiere reserved_card_id")
        required_tags = reserve_spec.get("requires_tag_any")
        if required_tags:
            reserved_res = supabase.table("cards").select("*").eq("id", reserved_card_id).single().execute()
            reserved_card = reserved_res.data
            if reserved_card is None:
                raise ValueError(f"Carta '{reserved_card_id}' no encontrada en el catalogo")
            if not set(reserved_card.get("tags") or []).intersection(required_tags):
                raise ValueError(
                    f"'{reserved_card_id}' no tiene ninguno de los tags requeridos {required_tags}"
                )

    free_trade = bool(resolved_spec.get("gains", {}).get("free_trade"))
    if free_trade and trade_colony_id is None:
        raise ValueError(f"La accion de '{card_id}' requiere trade_colony_id")

    # MC por cada ciudad/special tile del mapa adyacente a un oceano, de
    # cualquier dueno (Red Ships, X62 bloque 36). Se resuelve aca porque
    # necesita el tablero, igual que los requisitos de adyacencia: se
    # convierte a un resource_deltas concreto antes de llamar al motor.
    board_mc_spec = resolved_spec.get("gains", {}).get("mc_per_city_or_special_tile_adjacent_to_ocean")
    city_on_mars_spec = resolved_spec.get("gains", {}).get("mc_per_city_on_mars")
    spec_for_engine = action_spec
    if city_on_mars_spec:
        # Weather Balloons (X76, bloque 38): "gain 1 M€ per city ON MARS".
        # Se cuenta del TABLERO, no del contador global `city_tiles_placed`,
        # que tambien suma las ciudades fuera del mapa (Stanford Torus,
        # Maxwell Base, ...) -- esas no estan "on Mars".
        earned = boardlib.count_tiles_of_type(_load_board(), "city")
        new_gains = {k: v for k, v in resolved_spec.get("gains", {}).items() if k != "mc_per_city_on_mars"}
        resource_deltas = {**new_gains.get("resource_deltas", {})}
        resource_deltas["mc"] = resource_deltas.get("mc", 0) + earned
        new_gains["resource_deltas"] = resource_deltas
        spec_for_engine = {**resolved_spec, "gains": new_gains}
    if board_mc_spec:
        earned = boardlib.count_cities_and_special_tiles_adjacent_to_ocean(_load_board())
        new_gains = {k: v for k, v in resolved_spec.get("gains", {}).items()
                     if k != "mc_per_city_or_special_tile_adjacent_to_ocean"}
        resource_deltas = {**new_gains.get("resource_deltas", {})}
        resource_deltas["mc"] = resource_deltas.get("mc", 0) + earned
        new_gains["resource_deltas"] = resource_deltas
        spec_for_engine = {**resolved_spec, "gains": new_gains}

    # Acciones que mueven/colocan marcadores en el tablero (bloque 37). Se
    # resuelven aca porque necesitan el `board`, igual que free_trade; el
    # bonus del hexagono se traduce a un resource_deltas concreto y el resto
    # de la accion (incluido su costo) lo cobra el motor como siempre.
    marker_board = None
    nomad_bonus: list[tuple[str, int]] = []
    if resolved_spec.get("gains", {}).get("move_nomads"):
        if nomad_hex_id is None:
            raise ValueError(f"La accion de '{card_id}' requiere nomad_hex_id (destino)")
        marker_board, nomad_bonus = boardlib.move_nomads(_load_board(), nomad_hex_id)
        new_gains = {k: v for k, v in resolved_spec.get("gains", {}).items() if k != "move_nomads"}
        resource_deltas = {**new_gains.get("resource_deltas", {})}
        for resource, amount in nomad_bonus:
            resource_deltas[resource] = resource_deltas.get(resource, 0) + amount
        new_gains["resource_deltas"] = resource_deltas
        spec_for_engine = {**resolved_spec, "gains": new_gains}

    if resolved_spec.get("gains", {}).get("place_cathedral"):
        if city_hex_id is None:
            raise ValueError(f"La accion de '{card_id}' requiere city_hex_id")
        marker_board = boardlib.place_cathedral(_load_board(), city_hex_id)
        new_gains = {k: v for k, v in resolved_spec.get("gains", {}).items() if k != "place_cathedral"}
        spec_for_engine = {**resolved_spec, "gains": new_gains}

    # Algunas acciones tienen su PROPIO requisito, distinto del de jugar la
    # carta (ej. Red Appeasement: la accion exige que Reds gobierne o tener 2
    # delegados ahi). Se valida con la misma funcion del motor.
    turmoil = None
    action_requirements = resolved_spec.get("requirements")
    if action_requirements:
        turmoil = _load_turmoil()
        engine.check_card_requirements(
            action_requirements, globals_, player, turmoil=turmoil, player_id=player_id,
        )

    # Costo de accion pagado con delegados propios: se cobra ACA (tools.py),
    # no en el motor puro, que no conoce Turmoil -- mismo criterio que
    # free_trade y que remove_own_delegate en play_card.
    remove_delegates_count = resolved_spec.get("cost", {}).get("remove_own_delegates", 0)
    if remove_delegates_count:
        chosen_parties = removal_parties or []
        if len(chosen_parties) != remove_delegates_count:
            raise ValueError(
                f"Esta accion cuesta {remove_delegates_count} delegado(s) propio(s); "
                f"se recibieron {len(chosen_parties)} party(s)"
            )
        turmoil = turmoil if turmoil is not None else _load_turmoil()
        for party in chosen_parties:
            turmoil = turmoillib.remove_delegate(turmoil, party, player_id, allow_leader=True)
        spec_for_engine = {
            **resolved_spec,
            "cost": {k: v for k, v in resolved_spec.get("cost", {}).items() if k != "remove_own_delegates"},
        }

    # Revela y descarta la carta de arriba del mazo, y si tiene el tag
    # pedido agrega 1 recurso a la propia carta -- se resuelve ACA porque
    # necesita el catalogo (tags de la carta revelada), igual criterio que
    # free_trade / duplicate_production (bloque 32: Asteroid Deflection
    # System, "reveal and discard the top card of the deck, if it has a
    # space tag add an asteroid here").
    reveal_spec = resolved_spec.get("gains", {}).get("reveal_top_deck_card_add_resource_if_tag")
    if reveal_spec is not None:
        deck = list(player["deck"])
        matched = False
        if deck:
            top_card_id, deck = deck[0], deck[1:]
            top_res = supabase.table("cards").select("tags").eq("id", top_card_id).single().execute()
            top_tags = (top_res.data or {}).get("tags") or []
            matched = reveal_spec["tag"] in top_tags
            player = {**player, "deck": deck}
        new_gains = {k: v for k, v in spec_for_engine.get("gains", {}).items()
                     if k != "reveal_top_deck_card_add_resource_if_tag"}
        if matched:
            new_gains["card_resource_delta"] = new_gains.get("card_resource_delta", 0) + 1
        spec_for_engine = {**spec_for_engine, "gains": new_gains}

    new_player, new_globals = engine.use_card_action(
        player, globals_, card_id, spec_for_engine,
        None if remove_delegates_count else effect_choice, target_card_id=target_card_id,
        effect_amount=effect_amount, reserved_card_id=reserved_card_id, titanium_to_pay=titanium_to_pay,
        steel_to_pay=steel_to_pay,
    )
    if remove_delegates_count:
        new_player = {
            **new_player,
            "reserve_delegates": new_player["reserve_delegates"] + remove_delegates_count,
        }
        _save_turmoil(turmoil)

    # Accion que COLOCA delegados (el costo en MC lo cobra el motor puro por
    # la via normal, ej. Martian Media Center: "pay 3 M€ to add a delegate to
    # any party"). Simetrico a remove_own_delegates: se resuelve aca porque
    # rules_engine.py no conoce Turmoil.
    place_delegates_count = resolved_spec.get("gains", {}).get("place_delegates", 0)
    if place_delegates_count:
        chosen_parties = delegate_party_choices or []
        if len(chosen_parties) != place_delegates_count:
            raise ValueError(
                f"Esta accion coloca {place_delegates_count} delegado(s); "
                f"se recibieron {len(chosen_parties)} party(s)"
            )
        if new_player["reserve_delegates"] < place_delegates_count:
            raise engine.InsufficientResourcesError(
                f"El jugador tiene {new_player['reserve_delegates']} delegados en la Reserva, "
                f"se necesitan {place_delegates_count}"
            )
        turmoil = turmoil if turmoil is not None else _load_turmoil()
        for party in chosen_parties:
            turmoil = turmoillib.place_delegate(turmoil, party, player_id)
        new_player = {
            **new_player,
            "reserve_delegates": new_player["reserve_delegates"] - place_delegates_count,
        }
        _save_turmoil(turmoil)

    oceans_delta = new_globals["oceans_placed"] - globals_["oceans_placed"]
    board = None
    if oceans_delta > 0:
        board = _load_board()
        chosen = ocean_hex_ids or []
        if len(chosen) != oceans_delta:
            raise ValueError(
                f"Esta accion coloca {oceans_delta} oceano(s); se recibieron {len(chosen)} hex_id(s)"
            )
        # World Government Advisor (P67) sube el parametro "sin TR NI OTROS
        # BONUSES": si el oceano vino de ahi, el tile se coloca igual (ocupa
        # el hexagono) pero no se cobra el bonus de colocacion.
        skip_bonus = bool(resolved_spec.get("gains", {}).get("raise_global_parameter_without_bonuses"))
        for hid in chosen:
            if not boardlib.can_place_ocean(board, hid):
                raise boardlib.InvalidPlacementError(f"No se puede colocar oceano en '{hid}'")
            if skip_bonus:
                board, _hex_bonus, _ocean_mc = boardlib.place_ocean_tile(board, hid)
            else:
                board, new_player = _place_ocean_and_apply_bonus(board, new_player, hid)

    trade_result = None
    if free_trade:
        colonies = _load_colonies()
        new_colonies, income_type, income_amount, colony_bonus = colonieslib.trade_with_colony(colonies, trade_colony_id)
        new_player = dict(new_player)
        new_player = _apply_colony_gain(new_player, income_type, income_amount, target_card_id)
        if player_id in new_colonies[trade_colony_id]["owners"]:
            for key, delta in colony_bonus.items():
                new_player = _apply_colony_gain(new_player, key, delta, target_card_id)
        _save_colonies(new_colonies)
        trade_result = {"income_type": income_type, "income_amount": income_amount, "colony_bonus": colony_bonus}

    new_player = engine.apply_card_resource_gained_bonuses(new_player, card_resource_totals_before, active_cards_before)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    if board is not None:
        _save_board(board)
    elif marker_board is not None:
        # Movimiento de Nomads / colocacion de catedral: tocaron el tablero
        # antes de que el motor resolviera la accion (ver arriba).
        _save_board(marker_board)
    _log_transaction(
        player_id, "use_card_action",
        {"card_id": card_id, "effect_choice": effect_choice, "ocean_hex_ids": ocean_hex_ids,
         "target_card_id": target_card_id, "effect_amount": effect_amount, "trade_colony_id": trade_colony_id},
    )

    result = {"player": dict(new_player), "global_parameters": dict(new_globals)}
    if trade_result is not None:
        result.update(trade_result)
    return result


@tool
def get_board_state(player_id: str) -> dict:
    """
    Devuelve el mapa Tharsis completo: la geometria estatica de cada uno de
    los 61 hexagonos (id, fila, tipo de terreno, bonus impreso, si es
    volcanico o esta reservado para Noctis City) mas el estado actual de
    ocupacion (que hexagonos ya tienen tile y de quien). Se usa para que el
    LLM pueda mostrarle al usuario las opciones legales de hex_id antes de
    llamar use_standard_project/convert_resources/play_card/use_card_action
    con un tile que coloca oceano/ciudad/greenery.

    Args:
        player_id: id del jugador (para poder calcular can_place_greenery,
            que depende de si el jugador ya tiene tiles propios en el mapa).

    Returns:
        dict con "hexes": lista de hexagonos, cada uno con su definicion
        estatica, si esta ocupado (y por quien/con que tile), y si HOY es
        legal colocar ahi oceano/ciudad/greenery para este jugador.
    """
    board = _load_board()
    hexes = []
    for hex_id, hex_def in boardlib.HEX_DEFS.items():
        occupancy = board.get(hex_id)
        hexes.append({
            **hex_def,
            "occupied": occupancy is not None,
            "tile": occupancy,
            "can_place_ocean": boardlib.can_place_ocean(board, hex_id),
            "can_place_city": boardlib.can_place_city(board, hex_id),
            "can_place_greenery": boardlib.can_place_greenery(board, hex_id, player_id),
        })
    return {"hexes": hexes}


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
def resolve_research_phase(
    player_id: str, card_ids_to_buy: list[str], cost_per_card: int = 3, max_take: int | None = None
) -> dict:
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
        max_take: OBLIGATORIO pasar 2 si la fase la disparo Business
            Contacts (mira 4, exige tomar EXACTAMENTE 2 -- este tope hace
            que tomar de mas lance error en vez de permitirse). None para
            el resto de las fases (sin tope explicito, solo el MC limita).

    Returns:
        dict con el estado actualizado del jugador.

    Lanza ValueError si algun id no estaba en pending_research o si supera
    max_take, InsufficientResourcesError si no alcanza el MC.
    """
    player = _load_player(player_id)
    new_player = engine.resolve_research_phase(player, card_ids_to_buy, cost_per_card, max_take)

    _save_player(player_id, new_player)
    _log_transaction(
        player_id, "resolve_research_phase",
        {"card_ids_to_buy": card_ids_to_buy, "cost_per_card": cost_per_card, "max_take": max_take},
    )

    return {"player": dict(new_player)}


@tool
def setup_colonies(colony_ids: list[str]) -> dict:
    """
    Elige que Colony Tiles estan en juego esta partida (expansion Colonies,
    solo tiene sentido llamarla una vez, al arrancar). Regla oficial del
    modo solo ("Solo with Colonies"): sortear 4 y elegir 3 -- el sorteo/
    eleccion de cuales queda fuera de esta tool (el LLM se las ofrece al
    usuario a partir de `colonies.COLONY_DEFS`, que hoy solo tiene
    'callisto' cargada y verificada -- ver CARDS_LOG.md, seccion
    "Colonies: mecanica de colonias/comercio", para el resto de las 11
    colonias reales del juego, todavia sin cargar).

    Args:
        colony_ids: ids de `colonies.COLONY_DEFS` a poner en juego (ej.
            ["callisto"]).

    Returns:
        dict con el estado inicial de las colonias en juego.

    Lanza colonies.UnknownColonyError si algun id no esta en COLONY_DEFS.
    """
    new_colonies = colonieslib.new_colonies(colony_ids)
    _save_colonies(new_colonies)
    return {"colonies": dict(new_colonies)}


@tool
def build_colony(player_id: str, colony_id: str, target_card_id: str | None = None) -> dict:
    """
    Proyecto estandar de la expansion Colonies: paga 17 MC, coloca el
    marcador del jugador en el slot mas bajo libre de `colony_id` (maximo 3
    duenos por colonia, 1 por jugador) y otorga el placement_bonus impreso
    (ej. Callisto: +1 produccion de energia). No es lo mismo que comerciar
    -- ver use_trade_fleet.

    Args:
        player_id: id del jugador.
        colony_id: id de `colonies.COLONY_DEFS`, debe estar en juego (ver
            setup_colonies).

    Returns:
        dict con el estado actualizado del jugador y de las colonias.

    Lanza InsufficientResourcesError si falta MC, colonies.ColonyFullError
    si la colonia ya esta completa o el jugador ya tiene una ahi,
    colonies.UnknownColonyError si `colony_id` no esta en juego.
    """
    player = _load_player(player_id)
    if player["mc"] < colonieslib.BUILD_COLONY_COST_MC:
        raise engine.InsufficientResourcesError(
            f"Se necesitan {colonieslib.BUILD_COLONY_COST_MC} MC, hay {player['mc']}"
        )
    colonies = _load_colonies()
    new_colonies, placement_bonus = colonieslib.build_colony(colonies, colony_id, player_id)

    new_player: dict = {
        **player, "mc": player["mc"] - colonieslib.BUILD_COLONY_COST_MC,
        "colonies_owned": [*player["colonies_owned"], colony_id],
    }
    for key, delta in placement_bonus.items():
        new_player = _apply_colony_gain(new_player, key, delta, target_card_id)

    _save_player(player_id, engine.PlayerState(**new_player))  # type: ignore[typeddict-item]
    _save_colonies(new_colonies)
    _log_transaction(player_id, "build_colony", {"colony_id": colony_id})

    return {"player": new_player, "colonies": dict(new_colonies)}


@tool
def use_trade_fleet(
    player_id: str, colony_id: str, payment: str, bump_track_first: bool = False,
    target_card_id: str | None = None,
) -> dict:
    """
    Accion de comerciar de la expansion Colonies (no es un proyecto
    estandar -- una accion mas del turno). Paga el costo elegido (9 MC, 3
    energia o 3 titanio, reducido por el pasivo "trade_cost_discount" si el
    jugador lo tiene, ej. Cryo-Sleep), gasta 1 flota de comercio disponible
    (`trade_fleets - trade_fleets_used`), y mueve la flota a `colony_id`
    (debe estar libre de flota). Da el trade income (segun el track actual
    de esa colonia) al jugador, y el colony_bonus a TODOS sus duenos
    (incluido este jugador si tiene una ahi). Las flotas usadas vuelven a
    estar disponibles en la fase de produccion (ver run_production_phase).

    Args:
        player_id: id del jugador.
        colony_id: id de `colonies.COLONY_DEFS`, debe estar en juego.
        payment: "mc", "energy" o "titanium" -- que recurso usa para pagar
            el costo de comerciar.
        bump_track_first: OPCIONAL, True solo si el jugador tiene el pasivo
            "trade_bump_track_first" activo (ej. Trade Envoys, Trading
            Colony: "when you trade, you may first increase that Colony
            Tile track 1 step") y quiere ejercer esa opcion -- sube el
            track de `colony_id` 1 paso ANTES de calcular el trade income
            (asi cobra el valor mas alto). False (default) no la ejerce.

    Returns:
        dict con el estado actualizado del jugador y de las colonias, mas
        `income_type`/`income_amount`/`colony_bonus` para que el LLM le
        explique al usuario que gano.

    Lanza ValueError si `payment` no es valido o si `bump_track_first` es
    True sin tener el pasivo, InsufficientResourcesError si falta el
    recurso o no hay flotas disponibles, colonies.ColonyOccupiedError si la
    colonia ya tiene flota visitandola.
    """
    if payment not in ("mc", "energy", "titanium"):
        raise ValueError("payment debe ser 'mc', 'energy' o 'titanium'")

    player = _load_player(player_id)
    if player["trade_fleets"] - player["trade_fleets_used"] <= 0:
        raise engine.InsufficientResourcesError("El jugador no tiene flotas de comercio disponibles")

    discount = engine.compute_trade_cost_discount(player)
    base_cost = {
        "mc": colonieslib.TRADE_COST_MC,
        "energy": colonieslib.TRADE_COST_ENERGY,
        "titanium": colonieslib.TRADE_COST_TITANIUM,
    }[payment]
    cost = max(0, base_cost - discount)
    if player[payment] < cost:
        raise engine.InsufficientResourcesError(f"Se necesita {cost} de {payment}, hay {player[payment]}")

    colonies = _load_colonies()
    if bump_track_first:
        bump_steps = next(
            (e["trade_bump_track_first"] for e in player["passive_effects"] if e.get("trade_bump_track_first")),
            None,
        )
        if not bump_steps:
            raise ValueError("El jugador no tiene el pasivo 'trade_bump_track_first' activo")
        # El pasivo guarda la CANTIDAD de pasos (Trade Envoys/Trading Colony: 1;
        # L1 Trade Terminal: 2). `true` de las filas viejas equivale a 1 paso.
        colonies = colonieslib.adjust_colony_track(colonies, colony_id, int(bump_steps))
    new_colonies, income_type, income_amount, colony_bonus = colonieslib.trade_with_colony(colonies, colony_id)

    new_player: dict = {**player, payment: player[payment] - cost, "trade_fleets_used": player["trade_fleets_used"] + 1}
    new_player = _apply_colony_gain(new_player, income_type, income_amount, target_card_id)
    # Pasivos que premian el acto de comerciar (ej. Venus Trade Hub: +3 MC)
    for effect in player["passive_effects"]:
        new_player["mc"] = new_player["mc"] + effect.get("mc_delta_on_trade", 0)
    if player_id in new_colonies[colony_id]["owners"]:
        for key, delta in colony_bonus.items():
            new_player = _apply_colony_gain(new_player, key, delta, target_card_id)

    _save_player(player_id, engine.PlayerState(**new_player))  # type: ignore[typeddict-item]
    _save_colonies(new_colonies)
    _log_transaction(
        player_id, "use_trade_fleet",
        {"colony_id": colony_id, "payment": payment, "cost": cost,
         "income_type": income_type, "income_amount": income_amount},
    )

    return {
        "player": new_player, "colonies": dict(new_colonies),
        "income_type": income_type, "income_amount": income_amount, "colony_bonus": colony_bonus,
    }


@tool
def lobby(player_id: str, party: str, from_reserve: bool = False) -> dict:
    """
    Accion "Lobbying" de la expansion Turmoil (ver turmoil.py para el
    mecanismo completo) -- NO es un proyecto estandar, se puede usar
    cualquier cantidad de veces por generacion. Mueve 1 delegado del
    jugador al area de `party`: gratis desde el Lobby (`from_reserve=False`,
    consume `player.lobby_delegates`, que arranca en 1 y se rellena en
    tools.resolve_new_government) o pagando 5 MC desde la Reserva
    (`from_reserve=True`, consume `player.reserve_delegates`).

    Args:
        player_id: id del jugador.
        party: uno de turmoil.PARTY_NAMES (ej. "unity").
        from_reserve: False (default) usa el delegado gratis del Lobby;
            True paga 5 MC y usa uno de la Reserva.

    Returns:
        dict con el estado actualizado del jugador y de Turmoil.

    Lanza turmoil.UnknownPartyError si `party` no existe,
    InsufficientResourcesError si no hay delegado disponible en el origen
    elegido (Lobby vacio, o Reserva vacia/MC insuficiente).
    """
    player = _load_player(player_id)
    if from_reserve:
        if player["reserve_delegates"] < 1:
            raise engine.InsufficientResourcesError("El jugador no tiene delegados en la Reserva")
        if player["mc"] < turmoillib.LOBBY_FROM_RESERVE_COST_MC:
            raise engine.InsufficientResourcesError(
                f"Se necesitan {turmoillib.LOBBY_FROM_RESERVE_COST_MC} MC para colocar desde la Reserva"
            )
        new_player: dict = {
            **player,
            "reserve_delegates": player["reserve_delegates"] - 1,
            "mc": player["mc"] - turmoillib.LOBBY_FROM_RESERVE_COST_MC,
        }
    else:
        if player["lobby_delegates"] < 1:
            raise engine.InsufficientResourcesError("El jugador no tiene delegados en el Lobby")
        new_player = {**player, "lobby_delegates": player["lobby_delegates"] - 1}

    turmoil = _load_turmoil()
    new_turmoil = turmoillib.place_delegate(turmoil, party, player_id)

    _save_player(player_id, engine.PlayerState(**new_player))  # type: ignore[typeddict-item]
    _save_turmoil(new_turmoil)
    _log_transaction(player_id, "lobby", {"party": party, "from_reserve": from_reserve})

    return {"player": new_player, "turmoil": dict(new_turmoil)}


@tool
def resolve_new_government(player_id: str) -> dict:
    """
    Paso "New Government" de la expansion Turmoil, ACOTADO a un solo
    jugador (modo un jugador de este proyecto -- ver turmoil.py, seccion
    "Alcance de esta primera pasada"). El partido Dominante pasa a ser el
    Ruling; si `player_id` era su Party Leader, se vuelve el nuevo
    Chairman; el resto de sus delegados propios ahi (mas su delegado de
    Chairman anterior si lo tenia) vuelven a su Reserva. Tambien rellena
    el Lobby del jugador (1 delegado, tomado de la Reserva si hay).

    NO aplica Ruling Bonus/Ruling Policy ni la revision de TR (-1 a todos
    los jugadores) -- fuera de alcance de esta primera pasada, ver
    turmoil.py.

    Args:
        player_id: id del jugador.

    Returns:
        dict con el estado actualizado del jugador y de Turmoil. No hace
        nada si todavia no hay partido Dominante (delegados_devueltos=0).
    """
    player = _load_player(player_id)
    turmoil = _load_turmoil()
    new_turmoil, returned = turmoillib.resolve_new_government(turmoil, player_id)

    new_reserve = player["reserve_delegates"] + returned
    new_lobby = player["lobby_delegates"]
    if new_lobby < turmoillib.STARTING_LOBBY_DELEGATES and new_reserve > 0:
        new_lobby += 1
        new_reserve -= 1
    new_player = {**player, "reserve_delegates": new_reserve, "lobby_delegates": new_lobby}

    _save_player(player_id, engine.PlayerState(**new_player))  # type: ignore[typeddict-item]
    _save_turmoil(new_turmoil)
    _log_transaction(player_id, "resolve_new_government", {"delegates_returned": returned})

    return {"player": new_player, "turmoil": dict(new_turmoil), "delegates_returned": returned}


@tool
def get_turmoil_state(player_id: str) -> dict:
    """
    Devuelve el estado actual de Turmoil (partidos, delegados, partido
    Dominante/Ruling, Chairman) mas la Influencia calculada de
    `player_id` (formula oficial + bonus de cartas como Colonial
    Representation, ver turmoil.compute_influence).
    """
    player = _load_player(player_id)
    turmoil = _load_turmoil()
    influence = _compute_player_influence(player, turmoil, player_id)
    return {"turmoil": dict(turmoil), "influence": influence}


@tool
def resolve_ocean_offer(player_id: str, card_id: str, steel_to_pay: int = 0) -> dict:
    """
    Resuelve una de las ofertas opcionales que dispara colocar un oceano
    (`player.pending_ocean_offers`), pagando su costo (ej. Neptunian Power
    Consultants: "when any ocean is placed, you MAY spend 5 M€ -- steel may
    be used -- to raise your energy production 1 step and add 1 hydroelectric
    resource here").

    Existe como tool aparte porque la oferta es una DECISION del jugador: el
    motor no puede resolverla dentro de place_ocean, que corre sin
    interaccion y desde muchisimos caminos distintos. Cada oceano colocado
    suma una oferta; las que no se usen se pierden al cerrar la generacion
    (run_production_phase las limpia).

    Args:
        player_id: id del jugador.
        card_id: la carta activa que ofrece el trato (debe tener el pasivo
            `on_ocean_placed_offer` registrado y estar activa).
        steel_to_pay: cuanto acero declara pagar hacia el costo, si la oferta
            lo permite (`allow_steel`). 0 paga todo en MC.

    Lanza ValueError si no hay ofertas pendientes o la carta no ofrece nada,
    InsufficientResourcesError si no alcanza el pago.
    """
    player = _load_player(player_id)
    if player["pending_ocean_offers"] < 1:
        raise ValueError("No hay ofertas pendientes por colocacion de oceano")

    offer = next(
        (
            e["on_ocean_placed_offer"] for e in player["passive_effects"]
            if "on_ocean_placed_offer" in e and e["card_id"] == card_id
        ),
        None,
    )
    if offer is None:
        raise ValueError(f"La carta '{card_id}' no tiene una oferta por colocacion de oceano")

    cost_mc = offer.get("cost_mc", 0)
    if steel_to_pay and not offer.get("allow_steel"):
        raise ValueError(f"La oferta de '{card_id}' no permite pagar con acero")
    if player["steel"] < steel_to_pay:
        raise engine.InsufficientResourcesError(
            f"El jugador tiene {player['steel']} de acero, declaro pagar {steel_to_pay}"
        )
    steel_value_mc, _ = engine.compute_conversion_rates(player)
    mc_needed = max(0, cost_mc - steel_to_pay * steel_value_mc)
    if player["mc"] < mc_needed:
        raise engine.InsufficientResourcesError(f"Se necesitan {mc_needed} MC, hay {player['mc']}")

    new_player: dict = {
        **player,
        "mc": player["mc"] - mc_needed,
        "steel": player["steel"] - steel_to_pay,
        "pending_ocean_offers": player["pending_ocean_offers"] - 1,
    }
    for key, delta in offer.get("production_deltas", {}).items():
        new_player[key] = engine._apply_production_floor(key, new_player[key] + delta)
    if offer.get("card_resource_delta"):
        active = new_player["active_cards"]
        if card_id not in active:
            raise ValueError(f"La carta '{card_id}' no esta activa para este jugador")
        new_player["active_cards"] = {
            **active,
            card_id: {**active[card_id], "resources": active[card_id]["resources"] + offer["card_resource_delta"]},
        }

    _save_player(player_id, new_player)  # type: ignore[arg-type]
    _log_transaction(player_id, "resolve_ocean_offer", {"card_id": card_id, "steel_to_pay": steel_to_pay})
    return {"player": new_player}


@tool
def get_active_cards_state(player_id: str) -> dict:
    """
    Devuelve `player.active_cards` tal cual (card_id -> {resources,
    action_used, resource_type}) para que el LLM le muestre al usuario
    cuales ya usaron su accion esta generacion (`action_used: true`) --
    necesario para elegir `target_card_id` con sentido al jugar Project
    Inspection (X02, bloque 31: "use a card action that has already been
    used this generation", effect `reset_card_action_used`).
    """
    player = _load_player(player_id)
    return {"active_cards": dict(player["active_cards"])}


def _draw_cards_matching_tag(player: dict, tag, n: int) -> dict:
    """
    Roba las primeras `n` cartas del mazo que tengan `tag` (un tag suelto o
    una LISTA de tags, en cuyo caso vale cualquiera de ellos), salteando (sin
    descartar ni reordenar) las que no matcheen -- las no elegidas quedan en
    el mazo, en su orden original. Necesita el catalogo `cards` para conocer
    los tags, por eso vive en tools.py y no en el motor puro (mismo criterio
    que duplicate_production / on_card_played_cost_threshold_draw). Si el
    mazo no tiene `n` cartas con ese tag, roba las que haya (igual que
    draw_cards_to_hand con mazo corto). Ej. Ishtar Expedition: "draw 2 Venus
    cards".
    """
    deck = list(player["deck"])
    if not deck:
        return player
    res = supabase.table("cards").select("id,tags").in_("id", deck).execute()
    wanted = tag if isinstance(tag, list) else [tag]
    tagged = {
        row["id"] for row in (res.data or [])
        if any(t in (row["tags"] or []) for t in wanted)
    }

    # Se revela DE A UNA desde el tope hasta juntar N con el tag. Las
    # reveladas que no matchean se DESCARTAN (no vuelven al mazo): FAQ
    # oficial, "Once the card(s) have been obtained, all other revealed
    # cards are added to the discard pile". El motor no modela pila de
    # descarte, asi que simplemente salen del mazo. Las cartas por debajo
    # del punto donde se corto quedan intactas y en su orden.
    drawn: list[str] = []
    revealed_count = 0
    for cid in deck:
        revealed_count += 1
        if cid in tagged:
            drawn.append(cid)
            if len(drawn) == n:
                break
    if not drawn:
        return player
    remaining = deck[revealed_count:]
    return {**player, "deck": remaining, "hand": [*player["hand"], *drawn]}


def _count_blue_cards_played(played_card_ids: list[str]) -> int:
    """
    Cuenta cuantas de las cartas ya jugadas por el jugador son AZULES,
    cruzando su historial (`player["played_cards"]`) contra el catalogo.
    La clasificacion de color vive en engine.is_blue_card (funcion pura);
    aca solo se hace el acceso a base, respetando que rules_engine.py no
    consulta Supabase. Usado por el Global Event Solarnet Shutdown.
    """
    if not played_card_ids:
        return 0
    res = supabase.table("cards").select("id,is_event,effects").in_("id", played_card_ids).execute()
    return sum(
        1 for row in (res.data or [])
        if engine.is_blue_card(row["is_event"], row.get("effects"))
    )


def _compute_player_influence(
    player: engine.PlayerState, turmoil: turmoillib.TurmoilState, player_id: str
) -> int:
    bonus = sum(effect.get("influence_bonus", 0) for effect in player["passive_effects"])
    return turmoillib.compute_influence(turmoil, player_id, bonus=bonus)


@tool
def resolve_global_event(
    player_id: str, event_id: str, target_card_id: str | None = None, effect_choice: int | None = None,
    discard_card_ids: list[str] | None = None, remove_ocean_hex_id: str | None = None,
) -> dict:
    """
    Resuelve el efecto de la carta "Current Global Event" (expansion
    Turmoil, mazo separado de las cartas de proyecto -- ver
    `global_events`, tabla nueva, y CARDS_LOG.md seccion "Turmoil: Global
    Events"). Calcula la Influencia de `player_id` (ver
    turmoil.compute_influence) y aplica `event.effects` con
    rules_engine.apply_card_effect (mismo motor que las cartas de
    proyecto -- reusa su vocabulario, mas las piezas nuevas especificas de
    Global Events, ej. "resource_delta_per_capped_counter").

    ALCANCE (ver turmoil.py): NO simula el reparto de delegados neutrales
    al revelar la carta, ni el avance Distant -> Coming -> Current del
    mazo (single-player, no hay ciclo de generaciones automatizado). El
    LLM/usuario elige que Global Event resolver segun el contexto de la
    partida que este llevando afuera del motor.

    Args:
        player_id: id del jugador.
        event_id: id de `global_events` (ej. "generous_funding", "riots").
        target_card_id: OBLIGATORIO si `effects` tiene
            "target_card_resource_delta_typed" (ej. Corrosive Rain: "Lose
            2 floaters from a card" -- la carta activa propia elegida
            para perder los floaters). None si el evento no lo necesita.
        effect_choice: OBLIGATORIO si `effects` tiene "choice" (ej.
            Corrosive Rain: elegir entre perder floaters o 10 M€). None si
            el evento no tiene eleccion.
        discard_card_ids: OBLIGATORIO (con ese largo exacto) si `effects`
            tiene "discard_cards" (ej. Paradigm Breakdown: "Discard 2
            cards from hand") -- los card_ids de la mano a descartar.
            None si el evento no descarta cartas.
        remove_ocean_hex_id: OBLIGATORIO si `effects` tiene
            "remove_ocean_tile" (ej. Dry Deserts) -- el hex_id del oceano
            a sacar del mapa. Se ignora si los 9 oceanos ya estan
            colocados: con el parametro global maximizado el efecto NO se
            aplica (FAQ oficial). None si el evento no remueve oceanos.

    Returns:
        dict con el estado actualizado del jugador/parametros globales y
        la Influencia usada para el calculo.

    Lanza ValueError si `event_id` no existe en el catalogo.
    """
    event_res = supabase.table("global_events").select("*").eq("id", event_id).single().execute()
    event = event_res.data
    if event is None:
        raise ValueError(f"Global Event '{event_id}' no encontrado en el catalogo")

    effects = event.get("effects") or {}
    player = _load_player(player_id)
    globals_ = _load_global_parameters()
    turmoil = _load_turmoil()
    influence = _compute_player_influence(player, turmoil, player_id)

    # El tablero se carga una sola vez y sirve para los dos casos que lo
    # necesitan: leerlo (Mud Slides) y mutarlo (Dry Deserts).
    board = _load_board()
    new_board = None
    resolved_globals = globals_
    if effects.get("remove_ocean_tile"):
        if globals_["oceans_placed"] >= engine.OCEANS_MAX:
            # Parametro global maximizado: esta parte del evento no se aplica
            # (FAQ oficial, entrada de Dry Deserts).
            pass
        elif remove_ocean_hex_id is None:
            raise ValueError(f"El evento '{event_id}' requiere remove_ocean_hex_id")
        else:
            new_board = boardlib.remove_ocean_tile(board, remove_ocean_hex_id)
            # El tile vuelve a la reserva y puede colocarse de nuevo; nadie
            # pierde TR por la remocion (FAQ oficial).
            resolved_globals = {**globals_, "oceans_placed": globals_["oceans_placed"] - 1}

    new_player, new_globals = engine.apply_card_effect(
        player, resolved_globals, effects, effect_choice=effect_choice,
        target_card_id=target_card_id, influence=influence, discard_card_ids=discard_card_ids,
        board_tiles_adjacent_to_ocean=boardlib.count_tiles_adjacent_to_ocean(board),
        blue_cards_played=_count_blue_cards_played(player["played_cards"]),
    )

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    if new_board is not None:
        _save_board(new_board)
    _log_transaction(
        player_id, "resolve_global_event",
        {"event_id": event_id, "influence": influence, "remove_ocean_hex_id": remove_ocean_hex_id},
    )

    return {"player": dict(new_player), "globals": dict(new_globals), "influence": influence}


@tool
def play_prelude(
    player_id: str, prelude_id: str,
    ocean_hex_ids: list[str] | None = None, city_hex_ids: list[str] | None = None,
    greenery_hex_id: str | None = None, delegate_party_choices: list[str] | None = None,
    build_colony_id: str | None = None, discard_card_ids: list[str] | None = None,
) -> dict:
    """
    Juega una carta PRELUDE (expansion Prelude). A diferencia de play_card:
    las preludes se reparten gratis en el setup (2 por jugador), NO se pagan
    y no tienen requisitos -- por eso viven en su propia tabla
    `prelude_cards` (id, name, tags, effects) y no en `cards`.

    Aplica `effects` con el mismo motor que las cartas de proyecto
    (rules_engine.apply_card_effect), suma sus tags a `tags_played` y
    resuelve la colocacion de tiles en el mapa igual que play_card (por
    diferencia de contadores globales).

    Args:
        player_id: id del jugador.
        prelude_id: id en `prelude_cards` (ej. "allied_bank").
        ocean_hex_ids: OBLIGATORIO (con esa cantidad exacta) si la prelude
            coloca oceano(s) (ej. Great Aquifer: 2).
        city_hex_ids: idem para ciudades (ej. Early Settlement: 1).
        greenery_hex_id: OBLIGATORIO si la prelude coloca un greenery (ej.
            Experimental Forest).

    Returns:
        dict con el estado actualizado del jugador y de los parametros
        globales.

    Lanza ValueError si `prelude_id` no existe en el catalogo.
    """
    res = supabase.table("prelude_cards").select("*").eq("id", prelude_id).single().execute()
    prelude = res.data
    if prelude is None:
        raise ValueError(f"Prelude '{prelude_id}' no encontrada en el catalogo")

    effects = prelude.get("effects") or {}
    tags = tuple(prelude.get("tags") or [])
    player = _load_player(player_id)
    globals_ = _load_global_parameters()

    # Una prelude puede quedarse en juego con accion repetible y/o recursos
    # propios, igual que una carta de proyecto azul (ej. Applied Science:
    # arranca con 6 "science" y los gasta de a uno). Se registra ANTES de
    # aplicar el efecto, mismo orden que play_card, para que los pasivos que
    # se autodisparan encuentren la carta ya activa.
    if effects.get("becomes_active"):
        player = engine.register_active_card(
            player, prelude_id,
            initial_resources=engine.resolve_active_card_starting_resources(player, effects),
            resource_type=effects.get("active_card_resource_type"),
        )
    if effects.get("passive"):
        player = engine.register_passive_effect(player, prelude_id, effects["passive"])

    new_player, new_globals = engine.apply_card_effect(
        player, globals_, effects, discard_card_ids=discard_card_ids,
    )

    # Colocacion de tiles: mismo patron de diff de contadores que play_card
    # (misma resta de "place_city_tiles" -- contador sin mapa, ver ahi).
    board = None
    oceans_delta = new_globals["oceans_placed"] - globals_["oceans_placed"]
    cities_delta = (
        new_globals["city_tiles_placed"] - globals_["city_tiles_placed"] - effects.get("place_city_tiles", 0)
    )
    if oceans_delta > 0 or cities_delta > 0 or effects.get("place_greenery") is not None:
        board = _load_board()
    if oceans_delta > 0:
        chosen = ocean_hex_ids or []
        if len(chosen) != oceans_delta:
            raise ValueError(
                f"Esta prelude coloca {oceans_delta} oceano(s); se recibieron {len(chosen)} hex_id(s)"
            )
        for hid in chosen:
            if not boardlib.can_place_ocean(board, hid):
                raise boardlib.InvalidPlacementError(f"No se puede colocar oceano en '{hid}'")
            board, new_player = _place_ocean_and_apply_bonus(board, new_player, hid)
    if cities_delta > 0:
        chosen = city_hex_ids or []
        if len(chosen) != cities_delta:
            raise ValueError(
                f"Esta prelude coloca {cities_delta} ciudad(es); se recibieron {len(chosen)} hex_id(s)"
            )
        for hid in chosen:
            if not boardlib.can_place_city(board, hid):
                raise boardlib.InvalidPlacementError(f"No se puede colocar ciudad en '{hid}'")
            board, new_player = _place_city_and_apply_bonus(board, new_player, hid, player_id)
    greenery_spec = effects.get("place_greenery")
    if greenery_spec is not None:
        if greenery_hex_id is None:
            raise ValueError(f"La prelude '{prelude_id}' requiere greenery_hex_id")
        board, new_player = _place_greenery_and_apply_bonus(
            board, new_player, greenery_hex_id, player_id,
            ignore_restrictions=greenery_spec.get("ignore_restrictions", False),
        )

    draw_tag_spec = effects.get("draw_cards_matching_tag")
    if draw_tag_spec is not None:
        # Acepta un spec suelto o una LISTA de specs, para cartas que piden
        # N de un tag Y M de otro (ej. Planetary Alliance: 1 jovian + 1 venus).
        specs = draw_tag_spec if isinstance(draw_tag_spec, list) else [draw_tag_spec]
        for spec in specs:
            new_player = _draw_cards_matching_tag(new_player, spec["tag"], spec["n"])

    if effects.get("place_delegates"):
        num = effects["place_delegates"]
        chosen = delegate_party_choices or []
        if len(chosen) != num:
            raise ValueError(f"Esta prelude coloca {num} delegado(s); se recibieron {len(chosen)}")
        if new_player["reserve_delegates"] < num:
            raise engine.InsufficientResourcesError(
                f"El jugador tiene {new_player['reserve_delegates']} delegados en la Reserva, se necesitan {num}"
            )
        turmoil = _load_turmoil()
        for party in chosen:
            turmoil = turmoillib.place_delegate(turmoil, party, player_id)
        new_player = {**new_player, "reserve_delegates": new_player["reserve_delegates"] - num}
        _save_turmoil(turmoil)

    build_colony_spec = effects.get("build_colony")
    if build_colony_spec:
        if build_colony_id is None:
            raise ValueError(f"La prelude '{prelude_id}' requiere build_colony_id")
        allow_dup = isinstance(build_colony_spec, dict) and bool(build_colony_spec.get("allow_duplicate"))
        colonies = _load_colonies()
        new_colonies, placement_bonus = colonieslib.build_colony(
            colonies, build_colony_id, player_id, allow_duplicate=allow_dup,
        )
        new_player = {**new_player, "colonies_owned": [*new_player["colonies_owned"], build_colony_id]}
        for key, delta in placement_bonus.items():
            new_player[key] = new_player[key] + delta
        _save_colonies(new_colonies)

    # El pasivo ya quedo registrado mas arriba, ANTES de aplicar el efecto y
    # de disparar los bonus por tag, para que los que se auto-disparan con su
    # propio tag (ej. Albedo Plants: "+3 calor por cada tag plant, incluida
    # esta") funcionen -- mismo orden que tools.play_card. Registrarlo tambien
    # aca lo duplicaba, y un pasivo duplicado paga dos veces (lo agarro la
    # prueba de humo con Main Belt Asteroids: +2 titanio por 1 asteroide).
    new_player = engine.apply_tag_played_resource_bonuses(new_player, tags)
    new_player = engine.increment_tags_played(new_player, tags)

    _save_player(player_id, new_player)
    if new_globals != globals_:
        _save_global_parameters(new_globals)
    if board is not None:
        _save_board(board)
    _log_transaction(player_id, "play_prelude", {"prelude_id": prelude_id})

    return {"player": dict(new_player), "globals": dict(new_globals)}


# Lista de tools que se bindean al LLM en graph.py
ALL_TOOLS = [
    use_standard_project, convert_resources, run_production_phase,
    play_card, use_card_action, get_player_state, get_board_state,
    deal_starting_hand, start_research_phase, resolve_research_phase,
    setup_colonies, build_colony, use_trade_fleet,
    lobby, resolve_new_government, get_turmoil_state, resolve_global_event, play_prelude,
    get_active_cards_state, resolve_ocean_offer,
]
