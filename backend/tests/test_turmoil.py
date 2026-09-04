"""
Tests del modulo politico de la expansion Turmoil (nucleo: partidos,
delegados, Lobbying, Party Leader/Dominante/Chairman, Influencia). El
mecanismo esta verificado contra el rulebook oficial (TM_TURMOIL_ENG_RULES)
-- ver turmoil.py para el detalle de cada regla y la nota de alcance.
"""
import pytest

from app.agent.turmoil import (
    PARTY_NAMES,
    STARTING_LOBBY_DELEGATES,
    STARTING_RESERVE_DELEGATES,
    LOBBY_FROM_RESERVE_COST_MC,
    UnknownPartyError,
    new_turmoil,
    place_delegate,
    can_play_party_gated_card,
    compute_influence,
    resolve_new_government,
    remove_delegate,
)


def test_constants_match_official_rulebook():
    assert PARTY_NAMES == ["mars_first", "kelvinists", "reds", "greens", "unity", "scientists"]
    assert STARTING_LOBBY_DELEGATES == 1
    assert STARTING_RESERVE_DELEGATES == 6
    assert LOBBY_FROM_RESERVE_COST_MC == 5


def test_new_turmoil_starts_with_greens_ruling_no_dominant_no_chairman():
    t = new_turmoil()
    assert t["ruling_party"] == "greens"
    assert t["dominant_party"] is None
    assert t["chairman"] is None
    assert all(p["leader"] is None and p["delegates"] == {} for p in t["parties"].values())


def test_place_delegate_unknown_party_raises():
    t = new_turmoil()
    with pytest.raises(UnknownPartyError):
        place_delegate(t, "bogus_party", "p1")


def test_first_delegate_becomes_party_leader_and_dominant():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    assert t["parties"]["unity"]["leader"] == "p1"
    assert t["parties"]["unity"]["delegates"] == {"p1": 1}
    assert t["dominant_party"] == "unity"


def test_party_leader_replaced_only_by_strictly_more_delegates():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "unity", "p2")
    # empatados 1-1, el lider original se mantiene
    assert t["parties"]["unity"]["leader"] == "p1"
    t = place_delegate(t, "unity", "p2")
    # p2 ahora tiene 2 contra 1 de p1 -- reemplaza al lider
    assert t["parties"]["unity"]["leader"] == "p2"


def test_dominant_party_shifts_only_on_strictly_more_delegates():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "greens", "p1")
    # empatados 1-1, el dominante (el primero en fijarse) se mantiene
    assert t["dominant_party"] == "unity"
    t = place_delegate(t, "greens", "p1")
    assert t["dominant_party"] == "greens"


def test_can_play_party_gated_card_true_if_ruling():
    t = new_turmoil()
    assert can_play_party_gated_card(t, "greens", "p1") is True  # greens arranca ruling


def test_can_play_party_gated_card_true_with_min_delegates():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    assert can_play_party_gated_card(t, "unity", "p1") is False  # solo 1, hace falta 2
    t = place_delegate(t, "unity", "p1")
    assert can_play_party_gated_card(t, "unity", "p1") is True


def test_can_play_party_gated_card_false_otherwise():
    t = new_turmoil()
    assert can_play_party_gated_card(t, "unity", "p1") is False


def test_compute_influence_chairman_bonus():
    t = new_turmoil()
    t = {**t, "chairman": "p1"}
    assert compute_influence(t, "p1") == 1
    assert compute_influence(t, "p2") == 0


def test_compute_influence_dominant_party_leader_vs_non_leader_delegate():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "unity", "p2")
    t = place_delegate(t, "unity", "p2")
    # p2 es lider (2 delegados), p1 tiene 1 no-lider
    assert t["parties"]["unity"]["leader"] == "p2"
    assert compute_influence(t, "p2") == 1  # leader del dominante
    assert compute_influence(t, "p1") == 1  # no-lider con delegados ahi
    assert compute_influence(t, "p3") == 0  # sin nada


def test_compute_influence_adds_card_bonus_and_can_exceed_3():
    t = new_turmoil()
    t = {**t, "chairman": "p1"}
    t = place_delegate(t, "unity", "p1")
    assert compute_influence(t, "p1", bonus=1) == 1 + 1 + 1  # chairman + lider dominante + bonus


def test_resolve_new_government_no_dominant_does_nothing():
    t = new_turmoil()
    new_t, returned = resolve_new_government(t, "p1")
    assert new_t == t
    assert returned == 0


def test_resolve_new_government_leader_becomes_chairman_others_return_to_reserve():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "unity", "p1")  # p1 lider con 2 delegados en unity (dominante)
    new_t, returned = resolve_new_government(t, "p1")
    assert new_t["ruling_party"] == "unity"
    assert new_t["chairman"] == "p1"
    assert new_t["parties"]["unity"]["delegates"] == {}
    assert new_t["parties"]["unity"]["leader"] is None
    # 2 delegados propios, 1 se queda de chairman -> vuelve 1 a la reserva
    assert returned == 1


def test_resolve_new_government_non_leader_returns_all_own_delegates():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "unity", "p2")
    t = place_delegate(t, "unity", "p2")  # p2 lider (2), p1 no-lider (1)
    new_t, returned = resolve_new_government(t, "p1")
    assert new_t["chairman"] == "p2"
    assert returned == 1  # el unico delegado de p1 ahi, no era lider


def test_resolve_new_government_old_chairman_delegate_also_returns():
    t = new_turmoil()
    t = {**t, "chairman": "p1"}
    t = place_delegate(t, "greens", "p2")
    new_t, returned = resolve_new_government(t, "p1")
    # p1 no tenia delegados en el nuevo dominante (greens), pero era chairman viejo
    assert returned == 1
    assert new_t["chairman"] == "p2"


def test_resolve_new_government_recomputes_dominant_among_remaining_parties():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")
    t = place_delegate(t, "unity", "p1")  # unity dominante con 2
    t = place_delegate(t, "greens", "p2")  # greens con 1
    new_t, _ = resolve_new_government(t, "p1")
    assert new_t["ruling_party"] == "unity"
    assert new_t["dominant_party"] == "greens"  # el unico partido con delegados restante


def test_remove_delegate_returns_to_reserve_and_recomputes_dominant():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")   # p1 lider en unity
    t = place_delegate(t, "greens", "p2")
    t = place_delegate(t, "greens", "p1")  # p1 no-lider en greens (p2 llego primero)
    assert t["parties"]["greens"]["leader"] == "p2"
    new_t = remove_delegate(t, "greens", "p1")
    assert "p1" not in new_t["parties"]["greens"]["delegates"]
    assert new_t["parties"]["greens"]["delegates"] == {"p2": 1}


def test_remove_delegate_rejects_leader_and_missing_delegate():
    t = new_turmoil()
    t = place_delegate(t, "unity", "p1")  # p1 queda lider
    with pytest.raises(UnknownPartyError):
        remove_delegate(t, "unity", "p1")   # es el lider, no se puede
    with pytest.raises(UnknownPartyError):
        remove_delegate(t, "reds", "p1")    # no tiene delegados ahi
