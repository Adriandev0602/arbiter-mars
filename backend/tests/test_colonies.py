"""
Tests del modulo de colonias/comercio (expansion Colonies). El mecanismo
(costos, orden de pasos) esta verificado contra el rulebook oficial
(TM_COLONIES_ENG_RULES); los numeros de cada Colony Tile se transcribieron
de su scan, con Callisto (verificada antes con dos fuentes independientes)
como control del metodo -- ver colonies.py y CARDS_LOG.md.
"""
import pytest

from app.agent.colonies import (
    BUILD_COLONY_COST_MC,
    TRADE_COST_MC,
    TRADE_COST_ENERGY,
    TRADE_COST_TITANIUM,
    MAX_COLONISTS_PER_TILE,
    COLONY_DEFS,
    UnknownColonyError,
    ColonyFullError,
    ColonyOccupiedError,
    new_colonies,
    build_colony,
    trade_with_colony,
    run_colony_production,
    adjust_colony_track,
    trade_income,
)


def test_constants_match_official_rulebook():
    assert BUILD_COLONY_COST_MC == 17
    assert TRADE_COST_MC == 9
    assert TRADE_COST_ENERGY == 3
    assert TRADE_COST_TITANIUM == 3
    assert MAX_COLONISTS_PER_TILE == 3


def test_callisto_def_matches_verified_sources():
    callisto = COLONY_DEFS["callisto"]
    assert callisto["income_type"] == "energy"
    assert callisto["track"] == [0, 2, 3, 5, 7, 10, 13]
    assert callisto["colony_bonus"] == {"energy": 3}
    assert callisto["placement_bonus"] == {"energy_production": 1}


def test_new_colonies_starts_at_index_1_no_owners():
    colonies = new_colonies(["callisto"])
    assert colonies["callisto"]["track_position"] == 1
    assert colonies["callisto"]["owners"] == []
    assert colonies["callisto"]["trade_fleet_present"] is False


def test_new_colonies_unknown_id_raises():
    # id inventado a proposito: usar una colonia real haria que el test se
    # rompa el dia que esa colonia se cargue en COLONY_DEFS (paso con
    # "ganymede" al cargar las 5 del bloque de colonias).
    with pytest.raises(UnknownColonyError):
        new_colonies(["colonia_inexistente"])


def test_build_colony_adds_owner_and_returns_placement_bonus():
    colonies = new_colonies(["callisto"])
    new_state, placement_bonus = build_colony(colonies, "callisto", "player-1")
    assert new_state["callisto"]["owners"] == ["player-1"]
    assert placement_bonus == {"energy_production": 1}
    # 1 dueno, marcador ya estaba en 1 -- no hace falta subirlo
    assert new_state["callisto"]["track_position"] == 1


def test_build_colony_moves_white_marker_up_when_needed():
    colonies = new_colonies(["callisto"])
    colonies = {**colonies, "callisto": {**colonies["callisto"], "track_position": 0}}
    new_state, _ = build_colony(colonies, "callisto", "player-1")
    # 1 dueno pero el marcador estaba en 0 -- sube a 1 para dejar lugar
    assert new_state["callisto"]["track_position"] == 1


def test_build_colony_same_player_twice_raises():
    colonies = new_colonies(["callisto"])
    colonies, _ = build_colony(colonies, "callisto", "player-1")
    with pytest.raises(ColonyFullError):
        build_colony(colonies, "callisto", "player-1")


def test_build_colony_max_3_owners():
    colonies = new_colonies(["callisto"])
    colonies, _ = build_colony(colonies, "callisto", "player-1")
    colonies, _ = build_colony(colonies, "callisto", "player-2")
    colonies, _ = build_colony(colonies, "callisto", "player-3")
    with pytest.raises(ColonyFullError):
        build_colony(colonies, "callisto", "player-4")


def test_build_colony_not_in_play_raises():
    colonies = new_colonies(["callisto"])
    with pytest.raises(UnknownColonyError):
        build_colony(colonies, "ganymede", "player-1")


def test_trade_with_colony_gives_income_at_current_position_then_resets():
    colonies = new_colonies(["callisto"])
    colonies = {**colonies, "callisto": {**colonies["callisto"], "track_position": 5}}  # valor 10
    new_state, income_type, income_amount, colony_bonus = trade_with_colony(colonies, "callisto")
    assert income_type == "energy"
    assert income_amount == 10  # track[5] == 10, coincide con el ejemplo del rulebook
    assert colony_bonus == {"energy": 3}
    assert new_state["callisto"]["trade_fleet_present"] is True
    # sin duenos -- el marcador vuelve al fondo (0)
    assert new_state["callisto"]["track_position"] == 0


def test_trade_with_colony_resets_next_to_owners_not_to_zero():
    colonies = new_colonies(["callisto"])
    colonies, _ = build_colony(colonies, "callisto", "player-1")  # 1 dueno, marcador en 1
    colonies = {**colonies, "callisto": {**colonies["callisto"], "track_position": 4}}
    new_state, _, income_amount, _ = trade_with_colony(colonies, "callisto")
    assert income_amount == 7  # track[4] == 7
    assert new_state["callisto"]["track_position"] == 1  # al lado del unico dueno


def test_trade_with_colony_occupied_raises():
    colonies = new_colonies(["callisto"])
    colonies, _, _, _ = trade_with_colony(colonies, "callisto")
    with pytest.raises(ColonyOccupiedError):
        trade_with_colony(colonies, "callisto")


def test_run_colony_production_advances_marker_and_frees_fleets():
    colonies = new_colonies(["callisto"])
    colonies, _, _, _ = trade_with_colony(colonies, "callisto")  # marcador a 0, flota presente
    new_state = run_colony_production(colonies)
    assert new_state["callisto"]["track_position"] == 1  # sube 1 paso
    assert new_state["callisto"]["trade_fleet_present"] is False


def test_run_colony_production_caps_at_top_of_track():
    colonies = new_colonies(["callisto"])
    colonies = {**colonies, "callisto": {**colonies["callisto"], "track_position": 6}}  # tope del track (len 7)
    new_state = run_colony_production(colonies)
    assert new_state["callisto"]["track_position"] == 6  # no se pasa del tope


def test_adjust_colony_track_clamps_between_0_and_top():
    colonies = new_colonies(["callisto"])  # arranca en 1
    colonies = adjust_colony_track(colonies, "callisto", 4)
    assert colonies["callisto"]["track_position"] == 5
    colonies = adjust_colony_track(colonies, "callisto", 5)  # se pasaria de 6 (tope)
    assert colonies["callisto"]["track_position"] == 6
    colonies = adjust_colony_track(colonies, "callisto", -100)
    assert colonies["callisto"]["track_position"] == 0


def test_adjust_colony_track_unknown_colony_raises():
    colonies = new_colonies(["callisto"])
    with pytest.raises(UnknownColonyError):
        adjust_colony_track(colonies, "ganymede", 1)


def test_build_colony_allow_duplicate_bypasses_owner_check():
    colonies = new_colonies(["callisto"])
    colonies, _ = build_colony(colonies, "callisto", "player-1")
    # Sin allow_duplicate, falla
    with pytest.raises(ColonyFullError):
        build_colony(colonies, "callisto", "player-1")
    # Con allow_duplicate, el mismo jugador puede quedarse con un 2do slot
    new_state, _ = build_colony(colonies, "callisto", "player-1", allow_duplicate=True)
    assert new_state["callisto"]["owners"] == ["player-1", "player-1"]


def test_build_colony_allow_duplicate_still_respects_max_3():
    colonies = new_colonies(["callisto"])
    colonies, _ = build_colony(colonies, "callisto", "player-1", allow_duplicate=True)
    colonies, _ = build_colony(colonies, "callisto", "player-1", allow_duplicate=True)
    colonies, _ = build_colony(colonies, "callisto", "player-1", allow_duplicate=True)
    with pytest.raises(ColonyFullError):
        build_colony(colonies, "callisto", "player-1", allow_duplicate=True)


# --- Catalogo de colonias (transcrito de los scans, bloque de colonias) -----

def test_las_once_colonias_cargadas_tienen_track_de_7_casillas():
    # El track impreso de una Colony Tile siempre tiene 7 casillas; si alguna
    # quedo con 6 u 8 es que se transcribio mal del scan.
    assert len(COLONY_DEFS) == 11
    for cid, cdef in COLONY_DEFS.items():
        assert len(cdef["track"]) == 7, f"{cid} tiene {len(cdef['track'])} casillas"
        assert cdef["id"] == cid


def test_track_de_cada_colonia_es_no_decreciente():
    # Ningun Colony Tile del juego baja de valor al avanzar el marcador.
    for cid, cdef in COLONY_DEFS.items():
        track = cdef["track"]
        assert track == sorted(track), f"{cid} tiene un track que baja: {track}"


def test_valores_puntuales_leidos_del_scan():
    # Un valor "ancla" por colonia, para que un error de transcripcion no pase
    # silencioso. Callisto es ademas el control del metodo de lectura.
    assert COLONY_DEFS["callisto"]["track"] == [0, 2, 3, 5, 7, 10, 13]
    assert COLONY_DEFS["luna"]["track"][-1] == 17          # la de mayor tope
    assert COLONY_DEFS["luna"]["placement_bonus"] == {"mc_production": 2}
    assert COLONY_DEFS["io"]["colony_bonus"] == {"heat": 2}
    assert COLONY_DEFS["ceres"]["income_type"] == "steel"
    assert COLONY_DEFS["ganymede"]["track"] == [0, 1, 2, 3, 4, 5, 6]
    # Triton reparte titanio de STOCK, no produccion (sus spots no tienen marco)
    assert COLONY_DEFS["triton"]["placement_bonus"] == {"titanium": 3}


def test_colonias_de_recurso_de_carta_usan_el_prefijo():
    # Enceladus/Titan/Miranda dan recursos que viven EN UNA CARTA
    for cid, tipo in [("enceladus", "microbe"), ("titan", "floater"), ("miranda", "animal")]:
        assert COLONY_DEFS[cid]["income_type"] == f"card_resource:{tipo}"
    # Miranda ademas da una carta del mazo como colony bonus
    assert COLONY_DEFS["miranda"]["colony_bonus"] == {"cards": 1}


# --- Pluto y Europa (2026-10-02) ---------------------------------------------

def test_pluto_def_leida_del_scan():
    pluto = COLONY_DEFS["pluto"]
    assert pluto["income_type"] == "cards"
    assert pluto["track"] == [0, 1, 2, 2, 3, 3, 4]
    # "+1 carta -1 carta": roba 1 y despues descarta 1
    assert pluto["colony_bonus"] == {"cards_draw_then_discard": 1}
    # colony spots: dos cartas sin marco = robar 2
    assert pluto["placement_bonus"] == {"cards": 2}


def test_europa_def_leida_del_scan():
    europa = COLONY_DEFS["europa"]
    assert europa["income_types"] == [
        "mc_production", "mc_production", "energy_production", "energy_production",
        "plant_production", "plant_production", "plant_production",
    ]
    assert europa["track"] == [1, 1, 1, 1, 1, 1, 1]
    assert europa["colony_bonus"] == {"mc": 1}
    assert europa["placement_bonus"] == {"ocean": 1}


def test_trade_income_por_casilla_de_europa():
    assert trade_income("europa", 0) == ("mc_production", 1)
    assert trade_income("europa", 1) == ("mc_production", 1)
    assert trade_income("europa", 2) == ("energy_production", 1)
    assert trade_income("europa", 3) == ("energy_production", 1)
    assert trade_income("europa", 4) == ("plant_production", 1)
    assert trade_income("europa", 6) == ("plant_production", 1)
    # Las colonias de income fijo no cambian de clave
    assert trade_income("callisto", 5) == ("energy", 10)
    assert trade_income("pluto", 6) == ("cards", 4)


def test_trade_with_europa_da_la_produccion_de_la_casilla_actual():
    colonies = new_colonies(["europa"])
    colonies = adjust_colony_track(colonies, "europa", 2)  # 1 -> 3 (energia)
    new_state, income_type, income_amount, colony_bonus = trade_with_colony(colonies, "europa")
    assert (income_type, income_amount) == ("energy_production", 1)
    assert colony_bonus == {"mc": 1}
    assert new_state["europa"]["track_position"] == 0


def test_trade_with_europa_al_tope_da_plantas():
    colonies = new_colonies(["europa"])
    for _ in range(10):
        colonies = run_colony_production(colonies)
    assert colonies["europa"]["track_position"] == 6
    _, income_type, income_amount, _ = trade_with_colony(colonies, "europa")
    assert (income_type, income_amount) == ("plant_production", 1)


def test_trade_with_pluto_en_posicion_inicial_roba_1():
    colonies = new_colonies(["pluto"])
    colonies, _ = build_colony(colonies, "pluto", "player-1")
    colonies = adjust_colony_track(colonies, "pluto", 3)  # 1 -> 4
    new_state, income_type, income_amount, colony_bonus = trade_with_colony(colonies, "pluto")
    assert (income_type, income_amount) == ("cards", 3)
    assert colony_bonus == {"cards_draw_then_discard": 1}
    assert new_state["pluto"]["track_position"] == 1


def test_build_europa_devuelve_el_oceano_como_placement_bonus():
    colonies = new_colonies(["europa"])
    _, placement_bonus = build_colony(colonies, "europa", "player-1")
    assert placement_bonus == {"ocean": 1}


def _player_with_hand(hand, deck):
    from app.agent.rules_engine import new_player_state
    return {**new_player_state(), "hand": list(hand), "deck": list(deck)}


def test_draw_cards_then_require_discard_roba_y_anota_el_descarte():
    from app.agent.rules_engine import draw_cards_then_require_discard
    player = _player_with_hand(["a"], ["b", "c"])
    new_player = draw_cards_then_require_discard(player, 1)
    assert new_player["hand"] == ["a", "b"]
    assert new_player["deck"] == ["c"]
    assert new_player["pending_card_discards"] == 1


def test_resolve_pending_discards_puede_descartar_la_carta_recien_robada():
    from app.agent.rules_engine import draw_cards_then_require_discard, resolve_pending_discards
    player = draw_cards_then_require_discard(_player_with_hand(["a"], ["b"]), 1)
    new_player = resolve_pending_discards(player, ["b"])
    assert new_player["hand"] == ["a"]
    assert new_player["pending_card_discards"] == 0


def test_resolve_pending_discards_puede_descartar_una_carta_vieja():
    from app.agent.rules_engine import draw_cards_then_require_discard, resolve_pending_discards
    player = draw_cards_then_require_discard(_player_with_hand(["a"], ["b"]), 1)
    new_player = resolve_pending_discards(player, ["a"])
    assert new_player["hand"] == ["b"]


def test_resolve_pending_discards_exige_la_cantidad_exacta():
    from app.agent.rules_engine import (
        CardEffectError, draw_cards_then_require_discard, resolve_pending_discards,
    )
    player = draw_cards_then_require_discard(_player_with_hand(["a"], ["b"]), 1)
    with pytest.raises(CardEffectError):
        resolve_pending_discards(player, [])
    with pytest.raises(CardEffectError):
        resolve_pending_discards(player, ["a", "b"])


def test_resolve_pending_discards_sin_pendientes_falla():
    from app.agent.rules_engine import CardEffectError, resolve_pending_discards
    with pytest.raises(CardEffectError):
        resolve_pending_discards(_player_with_hand(["a"], []), ["a"])


def test_resolve_pending_discards_carta_ajena_falla():
    from app.agent.rules_engine import (
        CardNotInHandError, draw_cards_then_require_discard, resolve_pending_discards,
    )
    player = draw_cards_then_require_discard(_player_with_hand(["a"], ["b"]), 1)
    with pytest.raises(CardNotInHandError):
        resolve_pending_discards(player, ["z"])


def test_resolve_pending_discards_con_mano_vacia_alcanza_con_nada():
    from app.agent.rules_engine import draw_cards_then_require_discard, resolve_pending_discards
    # Mazo vacio y mano vacia: no se robo nada y no hay que descartar nada
    player = draw_cards_then_require_discard(_player_with_hand([], []), 1)
    assert player["pending_card_discards"] == 1
    assert resolve_pending_discards(player, [])["pending_card_discards"] == 0
def test_add_colony_tile_agrega_sin_tocar_las_que_estan():
    # Aridor (scan): "As your first action, put an additional Colony Tile of
    # your choice into play." Agrega, no reemplaza: Callisto conserva su
    # track y su dueno.
    from app.agent.colonies import add_colony_tile
    other = next(cid for cid in COLONY_DEFS if cid != "callisto")
    colonies, _ = build_colony(new_colonies(["callisto"]), "callisto", "p1")
    new = add_colony_tile(colonies, other)
    assert new["callisto"] == colonies["callisto"]
    assert new[other] == {"track_position": 1, "owners": [], "trade_fleet_present": False}
    assert len(new) == 2


def test_add_colony_tile_rechaza_repetida_o_desconocida():
    from app.agent.colonies import add_colony_tile
    colonies = new_colonies(["callisto"])
    with pytest.raises(ValueError):
        add_colony_tile(colonies, "callisto")
    with pytest.raises(UnknownColonyError):
        add_colony_tile(colonies, "no_existe")
