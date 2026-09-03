"""
Tests del modulo de colonias/comercio (expansion Colonies). El mecanismo
(costos, orden de pasos) esta verificado contra el rulebook oficial
(TM_COLONIES_ENG_RULES); los numeros de Callisto (unica colonia cargada
hasta ahora) estan verificados con dos fuentes independientes -- ver
colonies.py y CARDS_LOG.md.
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
    with pytest.raises(UnknownColonyError):
        new_colonies(["ganymede"])


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
