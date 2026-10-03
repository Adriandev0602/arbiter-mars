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
    TOTAL_NEUTRAL_DELEGATES,
    NEUTRAL,
    UnknownPartyError,
    new_turmoil,
    place_delegate,
    can_play_party_gated_card,
    compute_influence,
    resolve_new_government,
    remove_delegate,
    exchange_neutral_delegate,
    place_neutral_delegate,
    neutral_non_leader_count,
    normalize_turmoil,
    setup_global_events,
    changing_times,
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
    # Setup oficial (rulebook p.2): 14 neutrales, 1 en la silla de Chairman
    # (chairman None) y 13 en la Neutral Reserve; ningun partido arranca con
    # neutrales -- entran solo via Global Events.
    assert TOTAL_NEUTRAL_DELEGATES == 14
    assert t["neutral_reserve"] == 13
    assert (t["distant_event"], t["coming_event"], t["current_event"]) == (None, None, None)


# --- Delegados neutrales (mecanismo oficial, rulebook p.2/5/6/7) ---

_EVENT_PARTIES = {
    "e1": ("mars_first", "reds"),
    "e2": ("greens", "unity"),
    "e3": ("mars_first", "scientists"),
    "e4": ("kelvinists", "greens"),
}


def test_neutral_delegate_sale_de_la_reserva_y_puede_ser_leader_y_dominante():
    t = place_neutral_delegate(new_turmoil(), "reds")
    assert t["neutral_reserve"] == 12
    assert t["parties"]["reds"] == {"delegates": {NEUTRAL: 1}, "leader": NEUTRAL}
    assert t["dominant_party"] == "reds"


def test_neutral_delegate_con_reserva_vacia_no_hace_nada():
    t = {**new_turmoil(), "neutral_reserve": 0}
    assert place_neutral_delegate(t, "reds") == t


def test_jugador_con_mas_delegados_reemplaza_al_leader_neutral():
    t = place_neutral_delegate(new_turmoil(), "reds")
    t = place_delegate(t, "reds", "p1")
    assert t["parties"]["reds"]["leader"] == NEUTRAL  # empate 1-1: no reemplaza
    t = place_delegate(t, "reds", "p1")
    assert t["parties"]["reds"]["leader"] == "p1"


def test_setup_global_events_coming_y_distant_ponen_neutrales_arriba_a_la_izquierda():
    t = setup_global_events(new_turmoil(), ["e1", "e2", "e3", "e4"], _EVENT_PARTIES)
    assert (t["coming_event"], t["distant_event"], t["current_event"]) == ("e1", "e2", None)
    assert t["global_event_deck"] == ["e3", "e4"]
    assert t["parties"]["mars_first"]["leader"] == NEUTRAL
    assert t["parties"]["greens"]["leader"] == NEUTRAL
    assert t["dominant_party"] == "mars_first"  # la Coming define el Dominante
    assert t["neutral_reserve"] == 11


def test_setup_global_events_mismo_partido_el_segundo_va_a_delegados():
    t = setup_global_events(new_turmoil(), ["e1", "e3", "e2"], _EVENT_PARTIES)
    assert t["parties"]["mars_first"] == {"delegates": {NEUTRAL: 2}, "leader": NEUTRAL}


def test_setup_global_events_rechaza_track_ya_armado_o_mazo_corto():
    t = setup_global_events(new_turmoil(), ["e1", "e2"], _EVENT_PARTIES)
    with pytest.raises(ValueError):
        setup_global_events(t, ["e3", "e4"], _EVENT_PARTIES)
    with pytest.raises(ValueError):
        setup_global_events(new_turmoil(), ["e1"], _EVENT_PARTIES)


def test_changing_times_avanza_el_track_y_reparte_neutrales():
    t = setup_global_events(new_turmoil(), ["e1", "e2", "e3", "e4"], _EVENT_PARTIES)
    t = changing_times(t, _EVENT_PARTIES)
    # e1 pasa a Current: neutral en su mitad derecha (reds); e3 es la nueva
    # Distant: neutral en su esquina superior izquierda (mars_first).
    assert (t["current_event"], t["coming_event"], t["distant_event"]) == ("e1", "e2", "e3")
    assert t["parties"]["reds"]["delegates"] == {NEUTRAL: 1}
    assert t["parties"]["mars_first"]["delegates"] == {NEUTRAL: 2}
    assert t["global_event_deck"] == ["e4"]
    assert t["neutral_reserve"] == 9


def test_changing_times_con_mazo_vacio_deja_distant_vacia():
    t = setup_global_events(new_turmoil(), ["e1", "e2"], _EVENT_PARTIES)
    t = changing_times(t, _EVENT_PARTIES)
    assert (t["current_event"], t["coming_event"], t["distant_event"]) == ("e1", "e2", None)
    with pytest.raises(ValueError):
        changing_times(new_turmoil(), _EVENT_PARTIES)


def test_exchange_neutral_delegate_cambia_un_neutral_no_lider_por_uno_propio():
    # Recruitment (T11): "exchange one NEUTRAL NON-LEADER delegate with one
    # of your own from the reserve" -- el neutral vuelve a la Neutral Reserve.
    t = place_neutral_delegate(place_neutral_delegate(new_turmoil(), "unity"), "unity")
    assert neutral_non_leader_count(t, "unity") == 1
    t = exchange_neutral_delegate(t, "unity", "p1")
    assert t["parties"]["unity"]["delegates"] == {NEUTRAL: 1, "p1": 1}
    assert t["parties"]["unity"]["leader"] == NEUTRAL  # empate: el neutral sigue liderando
    assert t["neutral_reserve"] == 12
    assert t["dominant_party"] == "unity"  # el total no cambio


def test_exchange_neutral_delegate_falla_si_solo_queda_el_neutral_leader():
    t = place_neutral_delegate(new_turmoil(), "unity")
    with pytest.raises(UnknownPartyError):
        exchange_neutral_delegate(t, "unity", "p1")
    with pytest.raises(UnknownPartyError):
        exchange_neutral_delegate(new_turmoil(), "bogus_party", "p1")


def test_exchange_neutral_delegate_puede_volver_leader_al_jugador():
    t = place_delegate(new_turmoil(), "unity", "p1")
    t = place_neutral_delegate(t, "unity")
    t = exchange_neutral_delegate(t, "unity", "p1")
    assert t["parties"]["unity"] == {"delegates": {"p1": 2}, "leader": "p1"}


def test_resolve_new_government_neutrales_vuelven_a_su_reserva_y_leader_neutral_es_chairman():
    t = setup_global_events(new_turmoil(), ["e1", "e3", "e2"], _EVENT_PARTIES)  # 2 neutrales en mars_first
    t = place_delegate(t, "mars_first", "p1")
    assert t["neutral_reserve"] == 11
    new_t, returned = resolve_new_government(t, "p1")
    assert new_t["ruling_party"] == "mars_first"
    assert new_t["chairman"] is None  # el leader neutral pasa a la silla
    # vuelven: 1 neutral no-lider + el Chairman neutral anterior
    assert new_t["neutral_reserve"] == 13
    assert returned == 1  # el delegado de p1 (no-lider)


def test_normalize_turmoil_descarta_el_neutral_fijo_viejo_y_completa_claves():
    legacy = {
        "parties": {name: {"delegates": {}, "leader": None, "neutral": 2} for name in PARTY_NAMES},
        "dominant_party": None, "ruling_party": "reds", "chairman": None,
    }
    t = normalize_turmoil(legacy)
    assert t["ruling_party"] == "reds"
    assert all(p == {"delegates": {}, "leader": None} for p in t["parties"].values())
    assert t["neutral_reserve"] == 13
    assert normalize_turmoil({}) == new_turmoil()


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
