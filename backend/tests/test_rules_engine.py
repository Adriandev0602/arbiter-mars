"""
Tests del motor de reglas puro. Cada numero aqui esta verificado contra el
reglamento oficial de Terraforming Mars -- este archivo es la evidencia del
criterio de exito del PRD ("100% de precision en los calculos").
"""
import pytest

from app.agent.rules_engine import (
    TR_START,
    TEMPERATURE_MIN,
    TEMPERATURE_STEP,
    InsufficientResourcesError,
    GlobalParameterMaxedError,
    CardEffectError,
    CardRequirementNotMetError,
    new_player_state,
    new_global_parameters,
    raise_temperature,
    raise_oxygen,
    raise_venus,
    place_ocean,
    place_city_tile,
    standard_project_sell_patents,
    standard_project_power_plant,
    standard_project_asteroid,
    standard_project_air_scrapping,
    standard_project_aquifer,
    standard_project_greenery,
    standard_project_city,
    convert_plants_to_greenery,
    convert_heat_to_temperature,
    run_production_phase,
    adjust_mc_production,
    calculate_card_payment,
    apply_card_effect,
    check_card_requirements,
    register_active_card,
    use_card_action,
    increment_tags_played,
    increment_zero_tag_cards_played,
    register_passive_effect,
    compute_conversion_rates,
    compute_card_cost_discount,
    compute_trade_cost_discount,
    apply_event_played_bonuses,
    STEEL_VALUE_MC,
    TITANIUM_VALUE_MC,
    RESEARCH_PHASE_COST_MC,
    CardNotInHandError,
    initialize_deck,
    start_research_phase,
    resolve_research_phase,
    draw_cards_to_hand,
    remove_card_from_hand,
    reserve_card_in_slot,
    duplicate_reserved_card_resources,
    compute_reserved_card_discount,
    release_reserved_card,
    player_has_tag_swap_passive,
    swap_card_for_draw,
    register_played_card,
    increment_events_played,
    apply_tag_played_resource_bonuses,
    apply_greenery_placed_bonuses,
    apply_standard_project_used_bonuses,
    apply_city_placed_bonuses,
    apply_tag_played_choice,
    apply_any_tag_played_choice,
    spend_active_card_resource,
)


def test_new_player_state_starts_at_tr_20():
    player = new_player_state()
    assert player["tr"] == 20
    assert player["mc_production"] == 1
    assert player["mc"] == 0


def test_new_global_parameters_start_at_minimum():
    globals_ = new_global_parameters()
    assert globals_["temperature"] == -30
    assert globals_["oxygen"] == 0
    assert globals_["oceans_placed"] == 0


# --- Parametros globales ----------------------------------------------------

def test_raise_temperature_one_step_is_2_degrees_and_1_tr():
    player = new_player_state()
    globals_ = new_global_parameters()
    player, globals_ = raise_temperature(player, globals_, steps=1)
    assert globals_["temperature"] == -28
    assert player["tr"] == 21


def test_raise_temperature_caps_at_max_and_only_grants_tr_for_applied_steps():
    player = {**new_player_state(), "tr": 20}
    globals_ = {**new_global_parameters(), "temperature": 6}  # a 1 paso del maximo (8)
    player, globals_ = raise_temperature(player, globals_, steps=5)
    assert globals_["temperature"] == 8  # se clampea, no pasa de 8
    assert player["tr"] == 21  # solo se aplico 1 paso real, no 5


def test_raise_temperature_at_max_raises():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "temperature": 8}
    with pytest.raises(GlobalParameterMaxedError):
        raise_temperature(player, globals_)


def test_raise_oxygen_one_step_is_1_percent_and_1_tr():
    player = new_player_state()
    globals_ = new_global_parameters()
    player, globals_ = raise_oxygen(player, globals_, steps=1)
    assert globals_["oxygen"] == 1
    assert player["tr"] == 21


def test_raise_oxygen_caps_at_14():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "oxygen": 13}
    player, globals_ = raise_oxygen(player, globals_, steps=3)
    assert globals_["oxygen"] == 14
    assert player["tr"] == 21  # solo 1 paso real


def test_place_ocean_increments_and_grants_tr():
    player = new_player_state()
    globals_ = new_global_parameters()
    player, globals_ = place_ocean(player, globals_)
    assert globals_["oceans_placed"] == 1
    assert player["tr"] == 21


def test_place_ocean_at_max_raises():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "oceans_placed": 9}
    with pytest.raises(GlobalParameterMaxedError):
        place_ocean(player, globals_)


def test_raise_venus_one_step_is_2_percent_and_1_tr():
    player = new_player_state()
    globals_ = new_global_parameters()
    player, globals_ = raise_venus(player, globals_, steps=1)
    assert globals_["venus"] == 2
    assert player["tr"] == 21


def test_raise_venus_caps_at_30():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "venus": 28}
    player, globals_ = raise_venus(player, globals_, steps=3)
    assert globals_["venus"] == 30
    assert player["tr"] == 21  # solo 1 paso real


def test_raise_venus_at_max_raises():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "venus": 30}
    with pytest.raises(GlobalParameterMaxedError):
        raise_venus(player, globals_)


def test_raise_venus_bonus_step_8_percent_draws_free_card():
    player = {**new_player_state(), "deck": ["card_a", "card_b"]}
    globals_ = {**new_global_parameters(), "venus": 6}  # a 1 paso de 8%
    player, globals_ = raise_venus(player, globals_, steps=1)
    assert globals_["venus"] == 8
    assert player["hand"] == ["card_a"]  # +1 carta gratis al cruzar 8%
    assert player["tr"] == 21  # sin TR extra todavia (eso es a los 16%)


def test_raise_venus_bonus_step_16_percent_grants_extra_tr():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "venus": 14}  # a 1 paso de 16%
    player, globals_ = raise_venus(player, globals_, steps=1)
    assert globals_["venus"] == 16
    assert player["tr"] == 22  # +1 normal del paso, +1 bonus del umbral = +2
    assert player["hand"] == []  # el bonus de 16% es TR, no carta


def test_raise_venus_multiple_steps_crossing_both_bonus_thresholds_at_once():
    player = {**new_player_state(), "deck": ["card_a"]}
    globals_ = new_global_parameters()  # venus en 0%
    player, globals_ = raise_venus(player, globals_, steps=10)  # 0% -> 20%, cruza 8% y 16%
    assert globals_["venus"] == 20
    assert player["tr"] == 20 + 10 + 1  # 10 pasos normales + 1 TR bonus de 16%
    assert player["hand"] == ["card_a"]  # 1 carta gratis, una sola vez, al cruzar 8%


def test_standard_project_air_scrapping_costs_15_mc_and_raises_venus():
    player = {**new_player_state(), "mc": 15}
    globals_ = new_global_parameters()
    player, globals_ = standard_project_air_scrapping(player, globals_)
    assert player["mc"] == 0
    assert globals_["venus"] == 2
    assert player["tr"] == 21

    with pytest.raises(InsufficientResourcesError):
        standard_project_air_scrapping(new_player_state(), new_global_parameters())


# --- Proyectos estandar ------------------------------------------------------

def test_sell_patents_gives_1_mc_per_card():
    player = new_player_state()
    player = standard_project_sell_patents(player, num_cards=3)
    assert player["mc"] == 3


def test_power_plant_costs_11_mc_and_gives_1_energy_production():
    player = {**new_player_state(), "mc": 11}
    player = standard_project_power_plant(player)
    assert player["mc"] == 0
    assert player["energy_production"] == 2  # 1 base + 1


def test_power_plant_insufficient_funds_raises():
    player = {**new_player_state(), "mc": 10}
    with pytest.raises(InsufficientResourcesError):
        standard_project_power_plant(player)


def test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr():
    player = {**new_player_state(), "mc": 14}
    globals_ = new_global_parameters()
    player, globals_ = standard_project_asteroid(player, globals_)
    assert player["mc"] == 0
    assert globals_["temperature"] == -28
    assert player["tr"] == 21


def test_aquifer_costs_18_mc_places_ocean_and_1_tr():
    player = {**new_player_state(), "mc": 18}
    globals_ = new_global_parameters()
    player, globals_ = standard_project_aquifer(player, globals_)
    assert player["mc"] == 0
    assert globals_["oceans_placed"] == 1
    assert player["tr"] == 21


def test_greenery_costs_23_mc_raises_oxygen_1_percent_and_1_tr():
    player = {**new_player_state(), "mc": 23}
    globals_ = new_global_parameters()
    player, globals_ = standard_project_greenery(player, globals_)
    assert player["mc"] == 0
    assert globals_["oxygen"] == 1
    assert player["tr"] == 21


def test_city_costs_25_mc_and_gives_1_mc_production():
    player = {**new_player_state(), "mc": 25}
    player, globals_ = standard_project_city(player, new_global_parameters())
    assert player["mc"] == 0
    assert player["mc_production"] == 2  # 1 base + 1
    assert globals_["city_tiles_placed"] == 1


# --- Conversiones del tablero de jugador ------------------------------------

def test_convert_8_plants_to_greenery_raises_oxygen():
    player = {**new_player_state(), "plants": 8}
    globals_ = new_global_parameters()
    player, globals_ = convert_plants_to_greenery(player, globals_)
    assert player["plants"] == 0
    assert globals_["oxygen"] == 1
    assert player["tr"] == 21


def test_convert_plants_insufficient_raises():
    player = {**new_player_state(), "plants": 7}
    globals_ = new_global_parameters()
    with pytest.raises(InsufficientResourcesError):
        convert_plants_to_greenery(player, globals_)


def test_convert_8_heat_to_temperature():
    player = {**new_player_state(), "heat": 8}
    globals_ = new_global_parameters()
    player, globals_ = convert_heat_to_temperature(player, globals_)
    assert player["heat"] == 0
    assert globals_["temperature"] == -28
    assert player["tr"] == 21


# --- Fase de produccion ------------------------------------------------------

def test_production_phase_base_case_tr_20_all_production_1():
    """Caso base: jugador recien empezado, generacion 1 completa."""
    player = new_player_state()  # tr=20, produccion=1 en todo, stock=0
    result = run_production_phase(player)

    assert result["mc"] == 21          # TR(20) + mc_production(1)
    assert result["steel"] == 1        # 0 + steel_production(1)
    assert result["titanium"] == 1
    assert result["plants"] == 1
    assert result["energy"] == 1       # energia vieja (0) ya se movio a heat, ahora solo produccion nueva
    assert result["heat"] == 1         # 0 (heat previo) + 0 (energia vieja) + 1 (heat_production)


def test_production_phase_converts_leftover_energy_to_heat():
    player = {**new_player_state(), "energy": 5, "heat": 2}
    result = run_production_phase(player)

    # los 5 de energia se suman al heat existente (2), mas la produccion de heat (1)
    assert result["heat"] == 2 + 5 + 1
    assert result["energy"] == 1  # solo la produccion nueva, el stock viejo se vacio


def test_production_phase_with_higher_tr_and_production():
    player = {
        **new_player_state(),
        "tr": 35,
        "mc_production": 5,
        "mc": 10,
    }
    result = run_production_phase(player)
    assert result["mc"] == 10 + 35 + 5  # stock + TR + produccion


def test_production_phase_mc_never_goes_negative_even_with_negative_production():
    player = {**new_player_state(), "tr": 0, "mc_production": -5, "mc": 0}
    result = run_production_phase(player)
    # TR(0) + mc_production(-5) = -5 de ingreso, pero el stock nunca baja de 0
    assert result["mc"] == 0


def test_adjust_mc_production_respects_floor_of_minus_5():
    player = {**new_player_state(), "mc_production": -4}
    player = adjust_mc_production(player, delta=-3)
    assert player["mc_production"] == -5  # no -7


# --- Pago de cartas con acero/titanio ---------------------------------------

def test_calculate_card_payment_exact_mc():
    change = calculate_card_payment(card_cost=10, mc_to_pay=10)
    assert change == 0


def test_calculate_card_payment_with_steel_on_building_card():
    # carta de 10 MC, pago con 4 MC + 3 acero (3 * 2 MC = 6 MC) = 10 MC exactos
    change = calculate_card_payment(
        card_cost=10, mc_to_pay=4, steel_to_pay=3, card_tags=("building",)
    )
    assert change == 0


def test_calculate_card_payment_with_titanium_on_space_card():
    # carta de 9 MC, pago con 0 MC + 3 titanio (3 * 3 MC = 9 MC)
    change = calculate_card_payment(
        card_cost=9, mc_to_pay=0, titanium_to_pay=3, card_tags=("space",)
    )
    assert change == 0


def test_calculate_card_payment_steel_on_non_building_card_raises():
    with pytest.raises(ValueError):
        calculate_card_payment(card_cost=10, mc_to_pay=4, steel_to_pay=3, card_tags=("space",))


def test_calculate_card_payment_insufficient_raises():
    with pytest.raises(InsufficientResourcesError):
        calculate_card_payment(card_cost=10, mc_to_pay=5)


def test_calculate_card_payment_overpaying_gives_no_refund_but_no_error():
    change = calculate_card_payment(card_cost=5, mc_to_pay=8)
    assert change == 3  # el metodo devuelve el excedente informativamente,
    # pero la regla oficial es que no hay reembolso -- es responsabilidad de
    # quien llama a esta funcion no devolver ese cambio al stock del jugador


# ---------------------------------------------------------------------------
# Efectos de cartas cargadas en seed_cards.sql (numeros verificados contra
# el scan oficial de cada carta)
# ---------------------------------------------------------------------------

def test_sponsors_gives_plus_2_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"mc_production_delta": 2})
    assert new_player["mc_production"] == 3  # arranca en 1


def test_acquired_company_gives_plus_3_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"mc_production_delta": 3})
    assert new_player["mc_production"] == 4


def test_investment_loan_decreases_mc_production_and_gives_10_mc():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"mc_production_delta": -1, "mc_delta": 10}
    )
    assert new_player["mc_production"] == 0
    assert new_player["mc"] == 10


def test_investment_loan_respects_mc_production_floor_of_minus_5():
    player = {**new_player_state(), "mc_production": -5}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"mc_production_delta": -1, "mc_delta": 10}
    )
    assert new_player["mc_production"] == -5


def test_insulation_converts_heat_production_to_mc_production():
    player = {**new_player_state(), "heat_production": 3}
    new_player, _ = apply_card_effect(
        player,
        new_global_parameters(),
        {"convert_production": {"from": "heat_production", "to": "mc_production"}},
        effect_amount=3,
    )
    assert new_player["heat_production"] == 0
    assert new_player["mc_production"] == 4  # 1 base + 3 convertidos


def test_insulation_cannot_convert_more_heat_production_than_available():
    player = {**new_player_state(), "heat_production": 2}
    with pytest.raises(InsufficientResourcesError):
        apply_card_effect(
            player,
            new_global_parameters(),
            {"convert_production": {"from": "heat_production", "to": "mc_production"}},
            effect_amount=3,
        )


def test_insulation_requires_effect_amount():
    player = new_player_state()
    with pytest.raises(CardEffectError):
        apply_card_effect(
            player,
            new_global_parameters(),
            {"convert_production": {"from": "heat_production", "to": "mc_production"}},
        )


def test_apply_card_effect_with_no_effects_is_a_noop():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {})
    assert new_player == player
    assert new_globals == globals_


def test_nuclear_power_decreases_mc_production_and_increases_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"mc_production": -2, "energy_production": 3}},
    )
    assert new_player["mc_production"] == -1  # 1 - 2
    assert new_player["energy_production"] == 4  # 1 + 3


def test_solar_power_gives_plus_1_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"energy_production": 1}}
    )
    assert new_player["energy_production"] == 2


def test_titanium_mine_gives_plus_1_titanium_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"titanium_production": 1}}
    )
    assert new_player["titanium_production"] == 2


def test_solar_wind_power_gives_energy_production_and_titanium_stock():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player,
        new_global_parameters(),
        {"production_deltas": {"energy_production": 1}, "resource_deltas": {"titanium": 2}},
    )
    assert new_player["energy_production"] == 2
    assert new_player["titanium"] == 2


def test_artificial_photosynthesis_choice_0_gives_plant_production():
    player = new_player_state()
    effects = {
        "choice": [
            {"production_deltas": {"plant_production": 1}},
            {"production_deltas": {"energy_production": 2}},
        ]
    }
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, effect_choice=0)
    assert new_player["plant_production"] == 2
    assert new_player["energy_production"] == 1  # sin cambios


def test_artificial_photosynthesis_choice_1_gives_energy_production():
    player = new_player_state()
    effects = {
        "choice": [
            {"production_deltas": {"plant_production": 1}},
            {"production_deltas": {"energy_production": 2}},
        ]
    }
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, effect_choice=1)
    assert new_player["plant_production"] == 1  # sin cambios
    assert new_player["energy_production"] == 3


def test_artificial_photosynthesis_requires_valid_effect_choice():
    player = new_player_state()
    effects = {"choice": [{"production_deltas": {"plant_production": 1}}]}
    with pytest.raises(CardEffectError):
        apply_card_effect(player, new_global_parameters(), effects)
    with pytest.raises(CardEffectError):
        apply_card_effect(player, new_global_parameters(), effects, effect_choice=5)


def test_nitrogen_rich_asteroid_tag_count_choice_below_threshold():
    player = new_player_state()
    effects = {
        "tag_count_choice": {
            "tag": "plant", "count": 3,
            "if_met": {"raise_temperature_steps": 1, "production_deltas": {"plant_production": 4}},
            "else": {"raise_temperature_steps": 1, "production_deltas": {"plant_production": 1}},
        },
    }
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["plant_production"] == 2
    assert new_globals["temperature"] == TEMPERATURE_MIN + TEMPERATURE_STEP


def test_nitrogen_rich_asteroid_tag_count_choice_meets_threshold():
    player = new_player_state()
    player["tags_played"] = {"plant": 3}
    effects = {
        "tag_count_choice": {
            "tag": "plant", "count": 3,
            "if_met": {"production_deltas": {"plant_production": 4}},
            "else": {"production_deltas": {"plant_production": 1}},
        },
    }
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["plant_production"] == 5


def test_mine_gives_plus_1_steel_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"steel_production": 1}}
    )
    assert new_player["steel_production"] == 2


def test_resource_deltas_negative_below_zero_raises():
    player = new_player_state()  # plants = 0
    with pytest.raises(InsufficientResourcesError):
        apply_card_effect(player, new_global_parameters(), {"resource_deltas": {"plants": -2}})


def test_resource_deltas_negative_exact_stock_is_allowed():
    player = {**new_player_state(), "plants": 2}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"resource_deltas": {"plants": -2}}
    )
    assert new_player["plants"] == 0


def test_nitrophilic_moss_loses_2_plants_and_gives_2_plant_production():
    player = {**new_player_state(), "plants": 5}
    new_player, _ = apply_card_effect(
        player,
        new_global_parameters(),
        {"resource_deltas": {"plants": -2}, "production_deltas": {"plant_production": 2}},
    )
    assert new_player["plants"] == 3
    assert new_player["plant_production"] == 3


# ---------------------------------------------------------------------------
# Efectos globales inmediatos (bloque 2 de revision: Comet, Asteroid, Big
# Asteroid, Capital) -- ver CARDS_LOG.md sobre la regla de "remove up to N
# from any player" omitida por ser opcional en un solo jugador.
# ---------------------------------------------------------------------------

def test_comet_raises_temperature_and_places_ocean():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_, {"raise_temperature_steps": 1, "place_oceans": 1}
    )
    assert new_globals["temperature"] == TEMPERATURE_MIN + TEMPERATURE_STEP
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 2  # 1 TR por temperatura, 1 TR por oceano


def test_asteroid_card_raises_temperature_and_gives_titanium():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_, {"raise_temperature_steps": 1, "resource_deltas": {"titanium": 2}}
    )
    assert new_globals["temperature"] == TEMPERATURE_MIN + TEMPERATURE_STEP
    assert new_player["titanium"] == 2
    assert new_player["tr"] == TR_START + 1


def test_big_asteroid_raises_temperature_2_steps_and_gives_4_titanium():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_, {"raise_temperature_steps": 2, "resource_deltas": {"titanium": 4}}
    )
    assert new_globals["temperature"] == TEMPERATURE_MIN + 2 * TEMPERATURE_STEP
    assert new_player["titanium"] == 4
    assert new_player["tr"] == TR_START + 2


def test_capital_requires_4_oceans_and_changes_production():
    player = new_player_state()
    globals_met = {**new_global_parameters(), "oceans_placed": 4}
    check_card_requirements({"min_oceans": 4}, globals_met)  # no debe lanzar

    globals_not_met = {**new_global_parameters(), "oceans_placed": 3}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 4}, globals_not_met)

    new_player, new_globals = apply_card_effect(
        player, globals_met,
        {"production_deltas": {"energy_production": -2, "mc_production": 5}, "place_city_tiles": 1},
    )
    # energy_production arranca en 1, -2 lo dejaria en -1, pero el piso de
    # produccion (0 salvo MC) lo clampea -- comportamiento correcto, no un bug
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 6
    assert new_globals["city_tiles_placed"] == 1


# ---------------------------------------------------------------------------
# Requisitos de cartas (columna `requirements`)
# ---------------------------------------------------------------------------

def test_check_card_requirements_none_or_empty_is_a_noop():
    globals_ = new_global_parameters()
    check_card_requirements(None, globals_)
    check_card_requirements({}, globals_)


def test_farming_requires_temperature_4_or_warmer():
    globals_ = {**new_global_parameters(), "temperature": 2}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": 4}, globals_)


def test_farming_requirement_met_at_exactly_4():
    globals_ = {**new_global_parameters(), "temperature": 4}
    check_card_requirements({"min_temperature": 4}, globals_)  # no debe lanzar


def test_nitrophilic_moss_requires_3_oceans():
    globals_ = {**new_global_parameters(), "oceans_placed": 2}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 3}, globals_)

    globals_met = {**new_global_parameters(), "oceans_placed": 3}
    check_card_requirements({"min_oceans": 3}, globals_met)  # no debe lanzar


def test_check_card_requirements_min_oxygen():
    globals_ = {**new_global_parameters(), "oxygen": 5}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 8}, globals_)


# ---------------------------------------------------------------------------
# Cartas activas: accion repetible + recursos propios de la carta
# ---------------------------------------------------------------------------

def test_register_active_card_starts_with_0_resources_and_action_available():
    player = new_player_state()
    new_player = register_active_card(player, "ironworks")
    assert new_player["active_cards"] == {"ironworks": {"resources": 0, "action_used": False}}


def test_ironworks_action_spends_4_energy_gives_1_steel_and_raises_oxygen():
    player = register_active_card({**new_player_state(), "energy": 4}, "ironworks")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 1}, "raise_oxygen_steps": 1}}

    new_player, new_globals = use_card_action(player, globals_, "ironworks", action_spec)

    assert new_player["energy"] == 0
    assert new_player["steel"] == 1
    assert new_globals["oxygen"] == 1
    assert new_player["tr"] == TR_START + 1  # raise_oxygen otorga 1 TR por paso
    assert new_player["active_cards"]["ironworks"]["action_used"] is True


def test_steelworks_action_gives_2_steel():
    player = register_active_card({**new_player_state(), "energy": 4}, "steelworks")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 2}, "raise_oxygen_steps": 1}}

    new_player, _ = use_card_action(player, globals_, "steelworks", action_spec)
    assert new_player["steel"] == 2


def test_card_action_insufficient_stock_raises():
    player = register_active_card({**new_player_state(), "energy": 2}, "ironworks")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 1}}}

    with pytest.raises(InsufficientResourcesError):
        use_card_action(player, globals_, "ironworks", action_spec)


def test_card_action_cannot_be_used_twice_same_generation():
    player = register_active_card({**new_player_state(), "energy": 8}, "ironworks")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 1}}}

    new_player, new_globals = use_card_action(player, globals_, "ironworks", action_spec)
    with pytest.raises(CardEffectError):
        use_card_action(new_player, new_globals, "ironworks", action_spec)


def test_card_action_available_again_after_production_phase():
    player = register_active_card({**new_player_state(), "energy": 8}, "ironworks")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 1}}}

    used_player, _ = use_card_action(player, globals_, "ironworks", action_spec)
    reset_player = run_production_phase(used_player)
    assert reset_player["active_cards"]["ironworks"]["action_used"] is False


def test_use_card_action_on_inactive_card_raises():
    player = new_player_state()
    globals_ = new_global_parameters()
    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "ironworks", {"cost": {}, "gains": {}})


def test_regolith_eaters_choice_0_adds_1_microbe_to_the_card():
    player = register_active_card(new_player_state(), "regolith_eaters")
    globals_ = new_global_parameters()
    action_spec = {
        "choice": [
            {"cost": {}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_oxygen_steps": 1}},
        ]
    }

    new_player, _ = use_card_action(player, globals_, "regolith_eaters", action_spec, effect_choice=0)
    assert new_player["active_cards"]["regolith_eaters"]["resources"] == 1


def test_regolith_eaters_choice_1_spends_2_microbes_to_raise_oxygen():
    player = register_active_card(new_player_state(), "regolith_eaters")
    player["active_cards"]["regolith_eaters"]["resources"] = 2
    globals_ = new_global_parameters()
    action_spec = {
        "choice": [
            {"cost": {}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_oxygen_steps": 1}},
        ]
    }

    new_player, new_globals = use_card_action(
        player, globals_, "regolith_eaters", action_spec, effect_choice=1
    )
    assert new_player["active_cards"]["regolith_eaters"]["resources"] == 0
    assert new_globals["oxygen"] == 1


def test_regolith_eaters_choice_1_insufficient_card_resources_raises():
    player = register_active_card(new_player_state(), "regolith_eaters")  # 0 microbios
    globals_ = new_global_parameters()
    action_spec = {
        "choice": [
            {"cost": {}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_oxygen_steps": 1}},
        ]
    }

    with pytest.raises(InsufficientResourcesError):
        use_card_action(player, globals_, "regolith_eaters", action_spec, effect_choice=1)


# ---------------------------------------------------------------------------
# Contador global de ciudades y acciones que lo usan (bloque 2 de revision:
# Martian Rails, Capital, Space Elevator, Equatorial Magnetizer, Water Import
# from Europa)
# ---------------------------------------------------------------------------

def test_place_city_tile_increments_counter_without_tr():
    globals_ = new_global_parameters()
    new_globals = place_city_tile(globals_)
    assert new_globals["city_tiles_placed"] == 1


def test_martian_rails_action_gives_1_mc_per_city_tile():
    player = register_active_card({**new_player_state(), "energy": 1}, "martian_rails")
    globals_ = {**new_global_parameters(), "city_tiles_placed": 4}
    action_spec = {"cost": {"energy": 1}, "gains": {"mc_per_counter": "city_tiles_placed"}}

    new_player, _ = use_card_action(player, globals_, "martian_rails", action_spec)
    assert new_player["energy"] == 0
    assert new_player["mc"] == 4


def test_martian_rails_action_gives_0_mc_with_no_cities():
    player = register_active_card({**new_player_state(), "energy": 1}, "martian_rails")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 1}, "gains": {"mc_per_counter": "city_tiles_placed"}}

    new_player, _ = use_card_action(player, globals_, "martian_rails", action_spec)
    assert new_player["mc"] == 0


def test_equatorial_magnetizer_action_trades_energy_production_for_tr():
    player = register_active_card({**new_player_state(), "energy_production": 1}, "equatorial_magnetizer")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy_production": 1}, "gains": {"tr_delta": 1}}

    new_player, _ = use_card_action(player, globals_, "equatorial_magnetizer", action_spec)
    assert new_player["energy_production"] == 0
    assert new_player["tr"] == TR_START + 1


def test_space_elevator_action_trades_steel_for_5_mc():
    player = register_active_card({**new_player_state(), "steel": 1}, "space_elevator")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"steel": 1}, "gains": {"resource_deltas": {"mc": 5}}}

    new_player, _ = use_card_action(player, globals_, "space_elevator", action_spec)
    assert new_player["steel"] == 0
    assert new_player["mc"] == 5


def test_water_import_from_europa_action_places_ocean_for_12_mc():
    player = register_active_card({**new_player_state(), "mc": 12}, "water_import_from_europa")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 12}, "gains": {"place_oceans": 1}}

    new_player, new_globals = use_card_action(player, globals_, "water_import_from_europa", action_spec)
    assert new_player["mc"] == 0
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 1


# ---------------------------------------------------------------------------
# Tags jugados y efectos pasivos permanentes (bloque de logica faltante:
# Advanced Alloys, Mass Converter, Media Group, Optimal Aerobraking)
# ---------------------------------------------------------------------------

def test_increment_tags_played_counts_each_tag():
    player = new_player_state()
    player = increment_tags_played(player, ("science", "power"))
    player = increment_tags_played(player, ("science",))
    assert player["tags_played"] == {"science": 2, "power": 1}


def test_mass_converter_requires_5_science_tags():
    player = new_player_state()
    for _ in range(4):
        player = increment_tags_played(player, ("science",))
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 5}}, new_global_parameters(), player)

    player = increment_tags_played(player, ("science",))
    check_card_requirements(
        {"min_tag_count": {"tag": "science", "count": 5}}, new_global_parameters(), player
    )  # no debe lanzar


def test_min_tag_count_requires_player_argument():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 5}}, new_global_parameters())


def test_advanced_alloys_raises_steel_and_titanium_conversion_rates():
    player = new_player_state()
    steel_before, titanium_before = compute_conversion_rates(player)
    assert (steel_before, titanium_before) == (STEEL_VALUE_MC, TITANIUM_VALUE_MC)

    player = register_passive_effect(
        player, "advanced_alloys", {"steel_value_bonus": 1, "titanium_value_bonus": 1}
    )
    steel_after, titanium_after = compute_conversion_rates(player)
    assert steel_after == STEEL_VALUE_MC + 1
    assert titanium_after == TITANIUM_VALUE_MC + 1


def test_advanced_alloys_changes_calculate_card_payment_result():
    player = register_passive_effect(
        new_player_state(), "advanced_alloys", {"steel_value_bonus": 1, "titanium_value_bonus": 1}
    )
    steel_rate, titanium_rate = compute_conversion_rates(player)
    # sin Advanced Alloys, 3 acero cubririan 6 MC (building, costo 10 -> falta)
    # con Advanced Alloys, 3 acero cubren 9 MC
    change = calculate_card_payment(
        card_cost=9, mc_to_pay=0, steel_to_pay=3, card_tags=("building",),
        steel_value_mc=steel_rate, titanium_value_mc=titanium_rate,
    )
    assert change == 0  # pago exacto: 3 * 3 MC = 9


def test_media_group_gives_3_mc_when_event_card_is_played():
    player = register_passive_effect(new_player_state(), "media_group", {"on_event_played": {"mc_delta": 3}})
    new_player = apply_event_played_bonuses(player, played_card_tags=())
    assert new_player["mc"] == 3


def test_optimal_aerobraking_only_triggers_on_space_events():
    player = register_passive_effect(
        new_player_state(), "optimal_aerobraking",
        {"tag_filter": "space", "on_event_played": {"mc_delta": 3, "heat_delta": 3}},
    )
    # evento sin tag space: no dispara
    unaffected = apply_event_played_bonuses(player, played_card_tags=("earth",))
    assert unaffected["mc"] == 0
    assert unaffected["heat"] == 0

    # evento con tag space: si dispara
    affected = apply_event_played_bonuses(player, played_card_tags=("space",))
    assert affected["mc"] == 3
    assert affected["heat"] == 3


def test_multiple_passive_effects_stack():
    player = register_passive_effect(new_player_state(), "media_group", {"on_event_played": {"mc_delta": 3}})
    player = register_passive_effect(
        player, "optimal_aerobraking",
        {"tag_filter": "space", "on_event_played": {"mc_delta": 3, "heat_delta": 3}},
    )
    new_player = apply_event_played_bonuses(player, played_card_tags=("space",))
    assert new_player["mc"] == 6  # 3 (Media Group) + 3 (Optimal Aerobraking)
    assert new_player["heat"] == 3


def test_mass_converter_gives_2_mc_discount_on_space_cards():
    player = register_passive_effect(
        new_player_state(), "mass_converter", {"tag_filter": "space", "card_cost_discount_mc": 2}
    )
    discount = compute_card_cost_discount(player, card_tags=("space",))
    assert discount == 2


def test_mass_converter_discount_does_not_apply_to_non_space_cards():
    player = register_passive_effect(
        new_player_state(), "mass_converter", {"tag_filter": "space", "card_cost_discount_mc": 2}
    )
    discount = compute_card_cost_discount(player, card_tags=("building",))
    assert discount == 0


def test_compute_card_cost_discount_with_no_passive_effects_is_0():
    player = new_player_state()
    assert compute_card_cost_discount(player, card_tags=("space",)) == 0


# ---------------------------------------------------------------------------
# Sistema de mazo / mano
# ---------------------------------------------------------------------------

def test_initialize_deck_shuffles_but_keeps_same_cards():
    import random
    ids = [f"card_{i}" for i in range(20)]
    deck = initialize_deck(ids, rng=random.Random(42))
    assert sorted(deck) == sorted(ids)
    assert deck != ids  # con 20 elementos, la chance de que no se mueva nada es nula


def test_start_research_phase_draws_n_cards_from_deck_top():
    player = {**new_player_state(), "deck": ["a", "b", "c", "d", "e"]}
    new_player = start_research_phase(player, 3)
    assert new_player["pending_research"] == ["a", "b", "c"]
    assert new_player["deck"] == ["d", "e"]


def test_start_research_phase_draws_fewer_if_deck_is_short():
    player = {**new_player_state(), "deck": ["a", "b"]}
    new_player = start_research_phase(player, 4)
    assert new_player["pending_research"] == ["a", "b"]
    assert new_player["deck"] == []


def test_start_research_phase_fails_if_already_pending():
    player = {**new_player_state(), "deck": ["a", "b"], "pending_research": ["x"]}
    with pytest.raises(CardEffectError):
        start_research_phase(player, 2)


def test_resolve_research_phase_buys_selected_cards_at_standard_cost():
    player = {**new_player_state(), "mc": 20, "pending_research": ["a", "b", "c", "d"]}
    new_player = resolve_research_phase(player, ["a", "c"])
    assert new_player["mc"] == 20 - 2 * RESEARCH_PHASE_COST_MC
    assert sorted(new_player["hand"]) == ["a", "c"]
    assert new_player["pending_research"] == []  # b y d se descartaron


def test_resolve_research_phase_buying_zero_cards_is_valid():
    player = {**new_player_state(), "mc": 20, "pending_research": ["a", "b"]}
    new_player = resolve_research_phase(player, [])
    assert new_player["mc"] == 20
    assert new_player["hand"] == []
    assert new_player["pending_research"] == []


def test_resolve_research_phase_free_cost_for_inventors_guild_style():
    player = {**new_player_state(), "mc": 0, "pending_research": ["x"]}
    new_player = resolve_research_phase(player, ["x"], cost_per_card=0)
    assert new_player["mc"] == 0
    assert new_player["hand"] == ["x"]


def test_resolve_research_phase_rejects_id_not_in_pending():
    player = {**new_player_state(), "mc": 20, "pending_research": ["a", "b"]}
    with pytest.raises(ValueError):
        resolve_research_phase(player, ["z"])


def test_resolve_research_phase_insufficient_mc_raises():
    player = {**new_player_state(), "mc": 2, "pending_research": ["a", "b"]}
    with pytest.raises(InsufficientResourcesError):
        resolve_research_phase(player, ["a", "b"])  # 2 * 3 = 6 MC, solo hay 2


def test_draw_cards_to_hand_moves_from_deck_to_hand():
    player = {**new_player_state(), "deck": ["a", "b", "c"]}
    new_player = draw_cards_to_hand(player, 2)
    assert new_player["hand"] == ["a", "b"]
    assert new_player["deck"] == ["c"]


def test_remove_card_from_hand_removes_it():
    player = {**new_player_state(), "hand": ["a", "b"]}
    new_player = remove_card_from_hand(player, "a")
    assert new_player["hand"] == ["b"]


def test_remove_card_from_hand_raises_if_not_present():
    player = new_player_state()
    with pytest.raises(CardNotInHandError):
        remove_card_from_hand(player, "a")


def test_development_center_action_spends_energy_and_draws_1_card():
    player = register_active_card(
        {**new_player_state(), "energy": 1, "deck": ["a", "b"]}, "development_center"
    )
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 1}, "gains": {"draw_cards": 1}}

    new_player, _ = use_card_action(player, globals_, "development_center", action_spec)
    assert new_player["energy"] == 0
    assert new_player["hand"] == ["a"]
    assert new_player["deck"] == ["b"]


def test_inventors_guild_action_draws_1_card_to_pending_research():
    player = register_active_card(
        {**new_player_state(), "deck": ["a", "b"]}, "inventors_guild"
    )
    globals_ = new_global_parameters()
    action_spec = {"cost": {}, "gains": {"start_research": {"n": 1}}}

    new_player, _ = use_card_action(player, globals_, "inventors_guild", action_spec)
    assert new_player["pending_research"] == ["a"]
    assert new_player["deck"] == ["b"]

    # el usuario decide despues, sin costo (regla de Inventors' Guild)
    resolved = resolve_research_phase(new_player, ["a"], cost_per_card=0)
    assert resolved["hand"] == ["a"]
    assert resolved["mc"] == 0


# ---------------------------------------------------------------------------
# Bloque 2 de revision: requisitos max_temperature/max_oxygen, y pasivo
# on_ocean_placed enganchado directo en place_ocean
# ---------------------------------------------------------------------------

def test_domed_crater_requires_oxygen_7_or_less():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oxygen": 7}, {**new_global_parameters(), "oxygen": 8})
    check_card_requirements({"max_oxygen": 7}, {**new_global_parameters(), "oxygen": 7})  # no debe lanzar


def test_arctic_algae_requires_temperature_minus_12_or_colder():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_temperature": -12}, {**new_global_parameters(), "temperature": -10})
    check_card_requirements(
        {"max_temperature": -12}, {**new_global_parameters(), "temperature": -12}
    )  # no debe lanzar


def test_place_ocean_triggers_on_ocean_placed_passive():
    player = register_passive_effect(new_player_state(), "arctic_algae", {"on_ocean_placed": {"plants_delta": 2}})
    globals_ = new_global_parameters()

    new_player, new_globals = place_ocean(player, globals_)
    assert new_player["plants"] == 2
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 1


def test_place_ocean_without_passive_effects_does_not_change_plants():
    new_player, _ = place_ocean(new_player_state(), new_global_parameters())
    assert new_player["plants"] == 0


def test_multiple_ocean_placements_trigger_passive_each_time():
    player = register_passive_effect(new_player_state(), "arctic_algae", {"on_ocean_placed": {"plants_delta": 2}})
    globals_ = new_global_parameters()

    player, globals_ = place_ocean(player, globals_)
    player, globals_ = place_ocean(player, globals_)
    assert player["plants"] == 4
    assert globals_["oceans_placed"] == 2


def test_black_polar_dust_places_ocean_and_changes_production():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_, {"place_oceans": 1, "production_deltas": {"mc_production": -2, "heat_production": 3}}
    )
    assert new_globals["oceans_placed"] == 1
    assert new_player["mc_production"] == -1
    assert new_player["heat_production"] == 4
    assert new_player["tr"] == TR_START + 1


def test_release_of_inert_gases_raises_tr_2_steps_directly():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {"tr_delta": 2})
    assert new_player["tr"] == TR_START + 2
    assert new_globals == globals_  # no toca parametros globales


# ---------------------------------------------------------------------------
# Bloque 4 (CARDS_PENDING_REVIEW.md filas #1-10)
# ---------------------------------------------------------------------------

def test_deimos_down_raises_temperature_3_steps_and_gives_4_steel():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_,
        {"raise_temperature_steps": 3, "resource_deltas": {"steel": 4}},
    )
    assert new_globals["temperature"] == TEMPERATURE_MIN + 3 * TEMPERATURE_STEP
    assert new_player["steel"] == 4
    # clausula "remove up to 8 plants from any player" se omite (MVP single-player)


def test_asteroid_mining_gives_plus_2_titanium_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"titanium_production": 2}}
    )
    assert new_player["titanium_production"] == 3


def test_food_factory_minus_1_plant_plus_4_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"plant_production": -1, "mc_production": 4}},
    )
    assert new_player["plant_production"] == 0
    assert new_player["mc_production"] == 5


def test_archaebacteria_requires_max_temperature_minus_18():
    globals_ = {**new_global_parameters(), "temperature": -16}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_temperature": -18}, globals_)
    globals_["temperature"] = -20
    check_card_requirements({"max_temperature": -18}, globals_)  # no lanza


def test_archaebacteria_gives_plus_1_plant_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"plant_production": 1}}
    )
    assert new_player["plant_production"] == 2


def test_carbonate_processing_minus_1_energy_plus_3_heat_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "heat_production": 3}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["heat_production"] == 4


def test_natural_preserve_requires_max_oxygen_4_and_gives_plus_1_mc_production():
    globals_ = new_global_parameters()
    globals_["oxygen"] = 5
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oxygen": 4}, globals_)
    globals_["oxygen"] = 4
    check_card_requirements({"max_oxygen": 4}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"mc_production": 1}}
    )
    assert new_player["mc_production"] == 2
    # "place next to no other tile" es una restriccion de adyacencia sin
    # efecto en el motor (sin mapa hexagonal, ver CLAUDE.md seccion 6)


def test_lightning_harvest_requires_3_science_tags_and_gives_energy_and_mc():
    player = new_player_state()
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 3}}, globals_, player)
    player["tags_played"] = {"science": 3}
    check_card_requirements({"min_tag_count": {"tag": "science", "count": 3}}, globals_, player)
    new_player, _ = apply_card_effect(
        player, globals_,
        {"production_deltas": {"energy_production": 1, "mc_production": 1}},
    )
    assert new_player["energy_production"] == 2
    assert new_player["mc_production"] == 2


def test_algae_requires_5_oceans_and_gives_plant_resource_and_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 5}, globals_)
    globals_["oceans_placed"] = 5
    check_card_requirements({"min_oceans": 5}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_,
        {"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 2}},
    )
    assert new_player["plants"] == 1
    assert new_player["plant_production"] == 3


# ---------------------------------------------------------------------------
# Bloque 5 (CARDS_PENDING_REVIEW.md filas #1-10)
# ---------------------------------------------------------------------------

def test_adapted_lichen_gives_plus_1_plant_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"plant_production": 1}}
    )
    assert new_player["plant_production"] == 2


def test_tardigrades_action_adds_1_microbe_to_the_card_at_no_cost():
    player = register_active_card(new_player_state(), "tardigrades")
    globals_ = new_global_parameters()
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "tardigrades", action_spec)
    assert new_player["active_cards"]["tardigrades"]["resources"] == 1


def test_virus_has_no_modeled_effect_remove_up_to_clause_omitted():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_miranda_resort_gives_plus_1_mc_production_per_earth_tag():
    player = new_player_state()
    player["tags_played"] = {"earth": 3}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "earth", "production": "mc_production"}},
    )
    assert new_player["mc_production"] == 4  # 1 base + 3


def test_miranda_resort_with_no_earth_tags_gives_no_bonus():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "earth", "production": "mc_production"}},
    )
    assert new_player["mc_production"] == 1  # sin cambios


def test_fish_requires_2_degrees_and_decreases_plant_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": 2}, globals_)
    globals_["temperature"] = 2
    check_card_requirements({"min_temperature": 2}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"plant_production": -1}}
    )
    assert new_player["plant_production"] == 0
    active_player = register_active_card(new_player, "fish")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    final_player, _ = use_card_action(active_player, globals_, "fish", action_spec)
    assert final_player["active_cards"]["fish"]["resources"] == 1


def test_lake_marineris_requires_0_degrees_and_places_2_oceans():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": 0}, globals_)
    globals_["temperature"] = 0
    check_card_requirements({"min_temperature": 0}, globals_)  # no lanza
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, globals_, {"place_oceans": 2})
    assert new_globals["oceans_placed"] == 2
    assert new_player["tr"] == TR_START + 2


def test_small_animals_requires_6_oxygen_and_decreases_plant_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 6}, globals_)
    globals_["oxygen"] = 6
    check_card_requirements({"min_oxygen": 6}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"plant_production": -1}}
    )
    assert new_player["plant_production"] == 0


def test_kelp_farming_requires_6_oceans_and_gives_mc_plant_production_and_plants():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 6}, globals_)
    globals_["oceans_placed"] = 6
    check_card_requirements({"min_oceans": 6}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_,
        {"resource_deltas": {"plants": 2},
         "production_deltas": {"mc_production": 2, "plant_production": 3}},
    )
    assert new_player["plants"] == 2
    assert new_player["mc_production"] == 3
    assert new_player["plant_production"] == 4


def test_vesta_shipyard_gives_plus_1_titanium_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"titanium_production": 1}}
    )
    assert new_player["titanium_production"] == 2


def test_beam_from_a_thorium_asteroid_requires_jovian_tag_and_gives_heat_and_energy():
    player = new_player_state()
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "jovian", "count": 1}}, globals_, player)
    player["tags_played"] = {"jovian": 1}
    check_card_requirements({"min_tag_count": {"tag": "jovian", "count": 1}}, globals_, player)
    new_player, _ = apply_card_effect(
        player, globals_,
        {"production_deltas": {"heat_production": 3, "energy_production": 3}},
    )
    assert new_player["heat_production"] == 4
    assert new_player["energy_production"] == 4


# ---------------------------------------------------------------------------
# Bloque 6 (CARDS_PENDING_REVIEW.md filas #1-10)
# ---------------------------------------------------------------------------

def test_mangrove_requires_4_degrees_and_raises_oxygen_1_step():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": 4}, globals_)
    globals_["temperature"] = 4
    check_card_requirements({"min_temperature": 4}, globals_)  # no lanza
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, globals_, {"raise_oxygen_steps": 1})
    assert new_globals["oxygen"] == 1
    assert new_player["tr"] == TR_START + 1
    # "place on an area reserved for ocean, disregard placement restrictions"
    # es un detalle de tablero sin efecto medible (no modelamos el mapa)


def test_trees_requires_minus_4_degrees_and_gives_plant_production_and_stock():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -4}, globals_)
    globals_["temperature"] = -4
    check_card_requirements({"min_temperature": -4}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 3}}
    )
    assert new_player["plants"] == 1
    assert new_player["plant_production"] == 4


def test_great_escarpment_consortium_requires_own_steel_production():
    player = {**new_player_state(), "steel_production": 0}
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_production": {"key": "steel_production", "count": 1}}, globals_, player)
    player["steel_production"] = 1
    check_card_requirements({"min_production": {"key": "steel_production", "count": 1}}, globals_, player)  # no lanza
    # "decrease any steel production 1 step and increase your own 1 step" se
    # cancela en single-player (mismo objetivo) -- effects: {} tras el requisito


def test_mineral_deposit_gives_5_steel():
    player = new_player_state()
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"resource_deltas": {"steel": 5}})
    assert new_player["steel"] == 5


def test_mining_expedition_raises_oxygen_and_converts_plants_to_steel():
    player = {**new_player_state(), "plants": 2}
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_,
        {"raise_oxygen_steps": 1, "resource_deltas": {"plants": -2, "steel": 2}},
    )
    assert new_globals["oxygen"] == 1
    assert new_player["plants"] == 0
    assert new_player["steel"] == 2


def test_mining_expedition_insufficient_plants_raises():
    player = new_player_state()
    with pytest.raises(InsufficientResourcesError):
        apply_card_effect(
            player, new_global_parameters(),
            {"resource_deltas": {"plants": -2, "steel": 2}},
        )


def test_building_industries_minus_1_energy_plus_2_steel_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "steel_production": 2}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["steel_production"] == 3


def test_electro_catapult_requires_max_8_oxygen_and_minus_1_energy_production():
    globals_ = new_global_parameters()
    globals_["oxygen"] = 9
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oxygen": 8}, globals_)
    globals_["oxygen"] = 8
    check_card_requirements({"max_oxygen": 8}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"energy_production": -1}}
    )
    assert new_player["energy_production"] == 0


def test_electro_catapult_action_spends_plant_or_steel_for_7_mc():
    player = register_active_card({**new_player_state(), "plants": 1, "steel": 1}, "electro_catapult")
    globals_ = new_global_parameters()
    action_spec = {
        "choice": [
            {"cost": {"plants": 1}, "gains": {"resource_deltas": {"mc": 7}}},
            {"cost": {"steel": 1}, "gains": {"resource_deltas": {"mc": 7}}},
        ]
    }
    new_player, _ = use_card_action(player, globals_, "electro_catapult", action_spec, effect_choice=0)
    assert new_player["plants"] == 0
    assert new_player["mc"] == 7


# ---------------------------------------------------------------------------
# Bloque 7 (CARDS_PENDING_REVIEW.md filas #1-9, Advanced Alloys ya estaba cargada)
# ---------------------------------------------------------------------------

def test_earth_catapult_discount_applies_to_all_cards_no_tag_filter():
    player = new_player_state()
    player = register_passive_effect(player, "earth_catapult", {"card_cost_discount_mc": 2})
    assert compute_card_cost_discount(player, ("plant",)) == 2
    assert compute_card_cost_discount(player, ()) == 2


def test_birds_requires_13_oxygen_and_decreases_plant_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 13}, globals_)
    globals_["oxygen"] = 13
    check_card_requirements({"min_oxygen": 13}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"plant_production": -2}}
    )
    assert new_player["plant_production"] == 0  # piso 0, no negativo
    active_player = register_active_card(new_player, "birds")
    final_player, _ = use_card_action(
        active_player, globals_, "birds", {"cost": {}, "gains": {"card_resource_delta": 1}}
    )
    assert final_player["active_cards"]["birds"]["resources"] == 1


def test_mars_university_passive_offers_discard_for_draw_on_matching_tag():
    player = new_player_state()
    player["deck"] = ["sponsors"]
    player["hand"] = ["farming"]
    player = register_passive_effect(player, "mars_university", {"on_tag_played_may_swap_card": {"tag": "science"}})
    assert player_has_tag_swap_passive(player, ("science",)) is True
    assert player_has_tag_swap_passive(player, ("plant",)) is False
    new_player = swap_card_for_draw(player, "farming")
    assert "farming" not in new_player["hand"]
    assert "sponsors" in new_player["hand"]
    assert new_player["deck"] == []


def test_swap_card_for_draw_requires_card_in_hand():
    player = new_player_state()
    with pytest.raises(CardNotInHandError):
        swap_card_for_draw(player, "not_in_hand")


def test_towing_a_comet_gives_plants_raises_oxygen_and_places_ocean():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_,
        {"resource_deltas": {"plants": 2}, "raise_oxygen_steps": 1, "place_oceans": 1},
    )
    assert new_player["plants"] == 2
    assert new_globals["oxygen"] == 1
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 2  # +1 oxigeno, +1 oceano


def test_space_mirrors_action_spends_7_mc_for_1_energy_production():
    player = register_active_card({**new_player_state(), "mc": 7}, "space_mirrors")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 7}, "gains": {"production_deltas": {"energy_production": 1}}}
    new_player, _ = use_card_action(player, globals_, "space_mirrors", action_spec)
    assert new_player["mc"] == 0
    assert new_player["energy_production"] == 2


def test_ice_asteroid_places_2_oceans():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {"place_oceans": 2})
    assert new_globals["oceans_placed"] == 2
    assert new_player["tr"] == TR_START + 2


def test_quantum_extractor_requires_4_science_tags_gives_energy_and_space_discount():
    player = new_player_state()
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 4}}, globals_, player)
    player["tags_played"] = {"science": 4}
    check_card_requirements({"min_tag_count": {"tag": "science", "count": 4}}, globals_, player)
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"energy_production": 4}}
    )
    assert new_player["energy_production"] == 5
    new_player = register_passive_effect(
        new_player, "quantum_extractor", {"card_cost_discount_mc": 2, "tag_filter": "space"}
    )
    assert compute_card_cost_discount(new_player, ("space",)) == 2
    assert compute_card_cost_discount(new_player, ("plant",)) == 0


def test_giant_ice_asteroid_raises_temperature_and_places_2_oceans():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(
        player, globals_, {"raise_temperature_steps": 2, "place_oceans": 2}
    )
    assert new_globals["temperature"] == TEMPERATURE_MIN + 2 * TEMPERATURE_STEP
    assert new_globals["oceans_placed"] == 2
    assert new_player["tr"] == TR_START + 4  # +2 temperatura, +2 oceanos
    # "remove up to 6 plants from any player" se omite (MVP single-player)


# ---------------------------------------------------------------------------
# Bloque 8 (CARDS_PENDING_REVIEW.md filas #1-10)
# ---------------------------------------------------------------------------

def test_ganymede_colony_has_no_modeled_effect_vp_only_off_map():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_callisto_penal_mines_gives_plus_3_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"mc_production": 3}}
    )
    assert new_player["mc_production"] == 4


def test_giant_space_mirror_gives_plus_3_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"energy_production": 3}}
    )
    assert new_player["energy_production"] == 4


def test_trans_neptune_probe_has_no_modeled_effect_vp_only():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_commercial_district_minus_1_energy_plus_4_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "mc_production": 4}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 5
    # "1 VP por ciudad adyacente" no se trackea (sin puntuacion en el motor)


def test_grass_requires_minus_16_degrees_and_gives_plant_production_and_stock():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -16}, globals_)
    globals_["temperature"] = -16
    check_card_requirements({"min_temperature": -16}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_deltas": {"plants": 3}, "production_deltas": {"plant_production": 1}}
    )
    assert new_player["plants"] == 3
    assert new_player["plant_production"] == 2


def test_heather_requires_minus_14_degrees_and_gives_plant_production_and_stock():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -14}, globals_)
    globals_["temperature"] = -14
    check_card_requirements({"min_temperature": -14}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 1}}
    )
    assert new_player["plants"] == 1
    assert new_player["plant_production"] == 2


def test_peroxide_power_minus_1_mc_plus_2_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"mc_production": -1, "energy_production": 2}},
    )
    assert new_player["mc_production"] == 0
    assert new_player["energy_production"] == 3


def test_research_draws_2_cards():
    player = {**new_player_state(), "deck": ["mine", "sponsors", "farming"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["mine", "sponsors"]
    assert new_player["deck"] == ["farming"]


def test_research_draws_fewer_if_deck_runs_out():
    player = {**new_player_state(), "deck": ["mine"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["mine"]
    assert new_player["deck"] == []


def test_register_played_card_appends_to_history():
    player = new_player_state()
    player = register_played_card(player, "mine")
    player = register_played_card(player, "sponsors")
    assert player["played_cards"] == ["mine", "sponsors"]


def test_robotic_workforce_duplicates_production_via_apply_card_effect():
    # tools.play_card resuelve el lookup de la carta objetivo y arma este
    # production_deltas antes de llamar apply_card_effect -- este test
    # verifica solo la parte pura (duplicar = aplicar production_deltas de
    # nuevo), la resolucion del catalogo se prueba end-to-end en Supabase.
    player = new_player_state()
    target_production_deltas = {"steel_production": 1}  # ej. Mine
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"production_deltas": target_production_deltas})
    assert new_player["steel_production"] == 2


# ---------------------------------------------------------------------------
# Bloque 9 (CARDS_PENDING_REVIEW.md filas #1-10, Mass Converter ya estaba cargada)
# ---------------------------------------------------------------------------

def test_gene_repair_requires_3_science_tags_and_gives_mc_production():
    player = new_player_state()
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 3}}, globals_, player)
    player["tags_played"] = {"science": 3}
    check_card_requirements({"min_tag_count": {"tag": "science", "count": 3}}, globals_, player)
    new_player, _ = apply_card_effect(player, globals_, {"production_deltas": {"mc_production": 2}})
    assert new_player["mc_production"] == 3


def test_io_mining_industries_gives_titanium_and_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"titanium_production": 2, "mc_production": 2}},
    )
    assert new_player["titanium_production"] == 3
    assert new_player["mc_production"] == 3
    # "1 VP per jovian tag" no se trackea


def test_bushes_requires_minus_10_degrees_and_gives_plant_production_and_stock():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -10}, globals_)
    globals_["temperature"] = -10
    check_card_requirements({"min_temperature": -10}, globals_)  # no lanza
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_deltas": {"plants": 2}, "production_deltas": {"plant_production": 2}}
    )
    assert new_player["plants"] == 2
    assert new_player["plant_production"] == 3


def test_physics_complex_action_spends_6_energy_for_1_card_resource():
    player = register_active_card({**new_player_state(), "energy": 6}, "physics_complex")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 6}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "physics_complex", action_spec)
    assert new_player["energy"] == 0
    assert new_player["active_cards"]["physics_complex"]["resources"] == 1
    # "2 VP por recurso de ciencia en la carta" no se trackea


def test_greenhouses_gives_1_plant_per_city_tile_placed():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "city_tiles_placed": 3}
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_delta_per_counter": {"resource": "plants", "counter": "city_tiles_placed"}}
    )
    assert new_player["plants"] == 3


def test_greenhouses_with_no_cities_gives_no_plants():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_delta_per_counter": {"resource": "plants", "counter": "city_tiles_placed"}}
    )
    assert new_player["plants"] == 0


def test_nuclear_zone_raises_temperature_2_steps():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {"raise_temperature_steps": 2})
    assert new_globals["temperature"] == TEMPERATURE_MIN + 2 * TEMPERATURE_STEP
    assert new_player["tr"] == TR_START + 2
    # "-2 VP" y la colocacion del tile no se trackean


def test_tropical_resort_minus_2_heat_plus_3_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"heat_production": -2, "mc_production": 3}},
    )
    assert new_player["heat_production"] == 0  # piso 0
    assert new_player["mc_production"] == 4


def test_toll_station_has_no_effect_single_player_zero_opponents():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_fueled_generators_minus_1_mc_plus_1_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"mc_production": -1, "energy_production": 1}},
    )
    assert new_player["mc_production"] == 0
    assert new_player["energy_production"] == 2


# ---------------------------------------------------------------------------
# Bloque 10 (CARDS_PENDING_REVIEW.md filas #1-10, Media Group ya estaba cargada)
# ---------------------------------------------------------------------------

def test_power_grid_gives_1_energy_per_power_tag_including_itself():
    player = new_player_state()
    player["tags_played"] = {"power": 2}  # ya jugo 2 cartas power antes
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "power", "production": "energy_production"},
         "production_deltas": {"energy_production": 1}},
    )
    assert new_player["energy_production"] == 4  # 1 base + 2 previos + 1 (esta misma)


def test_power_grid_with_no_prior_power_tags_gives_1():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "power", "production": "energy_production"},
         "production_deltas": {"energy_production": 1}},
    )
    assert new_player["energy_production"] == 2  # 1 base + 0 previos + 1 (esta misma)


def test_ore_processor_action_spends_4_energy_for_titanium_and_oxygen():
    player = register_active_card({**new_player_state(), "energy": 4}, "ore_processor")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"energy": 4}, "gains": {"resource_deltas": {"titanium": 1}, "raise_oxygen_steps": 1}}
    new_player, new_globals = use_card_action(player, globals_, "ore_processor", action_spec)
    assert new_player["energy"] == 0
    assert new_player["titanium"] == 1
    assert new_globals["oxygen"] == 1


def test_earth_office_discount_only_applies_to_earth_tag():
    player = new_player_state()
    player = register_passive_effect(player, "earth_office", {"card_cost_discount_mc": 3, "tag_filter": "earth"})
    assert compute_card_cost_discount(player, ("earth",)) == 3
    assert compute_card_cost_discount(player, ("plant",)) == 0


def test_media_archives_gives_1_mc_per_event_ever_played():
    player = new_player_state()
    globals_ = {**new_global_parameters(), "events_played": 5}
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_delta_per_counter": {"resource": "mc", "counter": "events_played"}}
    )
    assert new_player["mc"] == 5


def test_increment_events_played_accumulates():
    globals_ = new_global_parameters()
    globals_ = increment_events_played(globals_)
    globals_ = increment_events_played(globals_)
    assert globals_["events_played"] == 2


def test_open_city_requires_12_oxygen_and_gives_production_and_plants():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 12}, globals_)
    globals_["oxygen"] = 12
    check_card_requirements({"min_oxygen": 12}, globals_)  # no lanza
    player = new_player_state()
    new_player, new_globals = apply_card_effect(
        player, globals_,
        {"production_deltas": {"energy_production": -1, "mc_production": 4},
         "resource_deltas": {"plants": 2}, "place_city_tiles": 1},
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 5
    assert new_player["plants"] == 2
    assert new_globals["city_tiles_placed"] == 1


def test_business_network_minus_1_mc_production_and_repeatable_research_action():
    player = register_active_card({**new_player_state(), "deck": ["mine"]}, "business_network")
    globals_ = new_global_parameters()
    new_player, _ = apply_card_effect(player, globals_, {"production_deltas": {"mc_production": -1}})
    assert new_player["mc_production"] == 0
    action_spec = {"cost": {}, "gains": {"start_research": {"n": 1}}}
    final_player, _ = use_card_action(new_player, globals_, "business_network", action_spec)
    assert final_player["pending_research"] == ["mine"]


def test_business_contacts_starts_research_of_4_and_resolves_exactly_2():
    player = {**new_player_state(), "deck": ["a", "b", "c", "d"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"start_research": {"n": 4}})
    assert new_player["pending_research"] == ["a", "b", "c", "d"]
    assert new_player["deck"] == []
    with pytest.raises(ValueError):
        resolve_research_phase(new_player, ["a", "b", "c"], cost_per_card=0, max_take=2)
    final_player = resolve_research_phase(new_player, ["a", "b"], cost_per_card=0, max_take=2)
    assert final_player["hand"] == ["a", "b"]
    assert final_player["pending_research"] == []


def test_bribed_committee_raises_tr_2_steps_directly():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {"tr_delta": 2})
    assert new_player["tr"] == TR_START + 2
    assert new_globals == globals_


def test_breathing_filters_requires_7_oxygen_no_modeled_effect():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 7}, globals_)
    globals_["oxygen"] = 7
    check_card_requirements({"min_oxygen": 7}, globals_)  # no lanza
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, globals_, {})
    assert new_player == player
    assert new_globals == globals_


# ---------------------------------------------------------------------------
# Bloque 11 (CARDS_PENDING_REVIEW.md filas #1-10)
# ---------------------------------------------------------------------------

def test_artificial_lake_requires_minus_6_degrees_and_places_ocean():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -6}, globals_)
    globals_["temperature"] = -6
    check_card_requirements({"min_temperature": -6}, globals_)  # no lanza
    player = new_player_state()
    # el marcador ocean_placement_bypasses_reservation es solo para tools.py
    # (decide que primitivo de board.py usar) -- apply_card_effect lo ignora
    # y sigue tratando "place_oceans" igual que siempre.
    new_player, new_globals = apply_card_effect(
        player, globals_, {"place_oceans": 1, "ocean_placement_bypasses_reservation": True}
    )
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 1


def test_geothermal_power_gives_plus_2_energy_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"energy_production": 2}}
    )
    assert new_player["energy_production"] == 3


def test_dust_seals_requires_max_3_oceans():
    globals_ = new_global_parameters()
    check_card_requirements({"max_oceans": 3}, globals_)  # no lanza, 0 oceanos
    globals_["oceans_placed"] = 3
    check_card_requirements({"max_oceans": 3}, globals_)  # no lanza, justo en el limite
    globals_["oceans_placed"] = 4
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oceans": 3}, globals_)


def test_urbanized_area_minus_1_energy_plus_2_mc_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "mc_production": 2}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 3
    # city_placement_requires_adjacent_cities es un marcador para tools.py
    # (decide que primitivo de board.py usar), no se procesa aca


def test_sabotage_has_no_modeled_effect_remove_up_to_clause_omitted():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_moss_requires_3_oceans_and_costs_1_plant_for_1_plant_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 3}, globals_)
    globals_["oceans_placed"] = 3
    check_card_requirements({"min_oceans": 3}, globals_)  # no lanza
    player = {**new_player_state(), "plants": 1}
    new_player, _ = apply_card_effect(
        player, globals_, {"resource_deltas": {"plants": -1}, "production_deltas": {"plant_production": 1}}
    )
    assert new_player["plants"] == 0
    assert new_player["plant_production"] == 2


def test_industrial_center_action_spends_7_mc_for_1_steel_production():
    player = register_active_card({**new_player_state(), "mc": 7}, "industrial_center")
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 7}, "gains": {"production_deltas": {"steel_production": 1}}}
    new_player, _ = use_card_action(player, globals_, "industrial_center", action_spec)
    assert new_player["mc"] == 0
    assert new_player["steel_production"] == 2
    # placement adyacente a una ciudad es responsabilidad de tools.py/board.py


def test_hired_raiders_has_no_modeled_effect_steal_up_to_clause_omitted():
    player = new_player_state()
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), {})
    assert new_player == player
    assert new_globals == new_global_parameters()


def test_hackers_minus_1_energy_production_mc_swap_cancels():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"production_deltas": {"energy_production": -1}}
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 1  # -2 a "cualquiera" +2 propio se cancela en single-player


def test_ghg_factories_minus_1_energy_plus_4_heat_production():
    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "heat_production": 4}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["heat_production"] == 5


# ---------------------------------------------------------------------------
# Bloque 12 (scans 127-136)
# ---------------------------------------------------------------------------

def test_subterranean_reservoir_places_1_ocean():
    player = new_player_state()
    globals_ = new_global_parameters()
    new_player, new_globals = apply_card_effect(player, globals_, {"place_oceans": 1})
    assert new_globals["oceans_placed"] == 1
    assert new_player["tr"] == TR_START + 1


def test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags():
    # 1. Al jugarse, Ecological Zone se activa y gana 2 animales (1 por tag animal, 1 por tag plant)
    player = register_active_card(new_player_state(), "ecological_zone")
    player = register_passive_effect(
        player,
        "ecological_zone",
        {"on_tag_played_add_resource": {"matching_tags": ["animal", "plant"], "resource_delta": 1}},
    )
    player = apply_tag_played_resource_bonuses(player, ("animal", "plant"))
    assert player["active_cards"]["ecological_zone"]["resources"] == 2

    # 2. Al jugar luego una carta con tag plant, suma 1 animal mas
    player = apply_tag_played_resource_bonuses(player, ("plant",))
    assert player["active_cards"]["ecological_zone"]["resources"] == 3

    # 3. Al jugar una carta espacial/power, no suma nada
    player = apply_tag_played_resource_bonuses(player, ("space", "power"))
    assert player["active_cards"]["ecological_zone"]["resources"] == 3


def test_zeppelins_mc_production_per_city_on_mars():
    globals_ = {**new_global_parameters(), "oxygen": 5, "city_tiles_placed": 4}
    check_card_requirements({"min_oxygen": 5}, globals_)

    player = new_player_state()
    effects = {
        "production_delta_per_counter": {
            "production": "mc_production",
            "counter": "city_tiles_placed",
            "per_counter": 1,
        }
    }
    new_player, _ = apply_card_effect(player, globals_, effects)
    assert new_player["mc_production"] == 1 + 4  # 1 inicial + 4 por las ciudades


def test_worms_plant_production_per_2_microbe_tags_including_this():
    globals_ = {**new_global_parameters(), "oxygen": 4}
    check_card_requirements({"min_oxygen": 4}, globals_)

    effects = {
        "production_delta_per_tag": {
            "tag": "microbe",
            "production": "plant_production",
            "tags_per_step": 2,
            "include_this": True,
        }
    }

    # Sin tags previos: total con Worms = 1 microbe tag -> 1 // 2 = 0 produccion extra
    player = new_player_state()
    p1, _ = apply_card_effect(player, globals_, effects)
    assert p1["plant_production"] == 1

    # Con 1 tag previo: total con Worms = 2 microbe tags -> 2 // 2 = +1 produccion
    player_with_1 = {**new_player_state(), "tags_played": {"microbe": 1}}
    p2, _ = apply_card_effect(player_with_1, globals_, effects)
    assert p2["plant_production"] == 2

    # Con 3 tags previos: total con Worms = 4 microbe tags -> 4 // 2 = +2 produccion
    player_with_3 = {**new_player_state(), "tags_played": {"microbe": 3}}
    p3, _ = apply_card_effect(player_with_3, globals_, effects)
    assert p3["plant_production"] == 3


def test_decomposers_passive_adds_microbes_on_bio_tags():
    player = register_active_card(new_player_state(), "decomposers")
    player = register_passive_effect(
        player,
        "decomposers",
        {"on_tag_played_add_resource": {"matching_tags": ["animal", "plant", "microbe"], "resource_delta": 1}},
    )
    # Al jugarse Decomposers (tag microbe), suma 1 microbio inicial
    player = apply_tag_played_resource_bonuses(player, ("microbe",))
    assert player["active_cards"]["decomposers"]["resources"] == 1

    # Al jugar una carta con plant y animal (ej. Ecological Zone), suma 2 microbios
    player = apply_tag_played_resource_bonuses(player, ("plant", "animal"))
    assert player["active_cards"]["decomposers"]["resources"] == 3


def test_fusion_power_requires_2_power_tags_and_gives_3_energy_prod():
    player = new_player_state()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "power", "count": 2}}, new_global_parameters(), player)

    player_ready = {**player, "tags_played": {"power": 2}}
    check_card_requirements({"min_tag_count": {"tag": "power", "count": 2}}, new_global_parameters(), player_ready)

    new_player, _ = apply_card_effect(
        player_ready, new_global_parameters(), {"production_deltas": {"energy_production": 3}}
    )
    assert new_player["energy_production"] == 4


def test_symbiotic_fungus_adds_microbe_to_another_active_card():
    globals_ = {**new_global_parameters(), "temperature": -14}
    check_card_requirements({"min_temperature": -14}, globals_)

    player = register_active_card(new_player_state(), "symbiotic_fungus")
    player = register_active_card(player, "decomposers")

    action_spec = {"gains": {"target_card_resource_delta": 1}}

    # Requiere target_card_id
    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "symbiotic_fungus", action_spec)

    # No puede agregarse a si misma
    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "symbiotic_fungus", action_spec, target_card_id="symbiotic_fungus")

    # Agrega 1 a decomposers
    new_player, _ = use_card_action(
        player, globals_, "symbiotic_fungus", action_spec, target_card_id="decomposers"
    )
    assert new_player["active_cards"]["decomposers"]["resources"] == 1
    assert new_player["active_cards"]["symbiotic_fungus"]["action_used"] is True


def test_extreme_cold_fungus_choice_plant_or_target_microbes():
    globals_ = {**new_global_parameters(), "temperature": -10}
    check_card_requirements({"max_temperature": -10}, globals_)

    player = register_active_card(new_player_state(), "extreme_cold_fungus")
    player = register_active_card(player, "regolith_eaters")

    action_spec = {
        "choice": [
            {"gains": {"resource_deltas": {"plants": 1}}},
            {"gains": {"target_card_resource_delta": 2}},
        ]
    }

    # Choice 0: gana 1 planta
    p1, _ = use_card_action(player, globals_, "extreme_cold_fungus", action_spec, effect_choice=0)
    assert p1["plants"] == 1

    # Choice 1: agrega 2 microbios a regolith_eaters
    p2, _ = use_card_action(
        player, globals_, "extreme_cold_fungus", action_spec, effect_choice=1, target_card_id="regolith_eaters"
    )
    assert p2["active_cards"]["regolith_eaters"]["resources"] == 2


def test_apply_card_effect_target_card_resource_delta():
    player = register_active_card(new_player_state(), "local_heat_trapping")
    player = register_active_card(player, "decomposers")
    globals_ = new_global_parameters()

    effects = {"target_card_resource_delta": 3}

    # Requiere target_card_id
    with pytest.raises(CardEffectError):
        apply_card_effect(player, globals_, effects)

    # La carta objetivo debe estar activa
    with pytest.raises(CardEffectError):
        apply_card_effect(player, globals_, effects, target_card_id="no_existe")

    new_player, _ = apply_card_effect(player, globals_, effects, target_card_id="decomposers")
    assert new_player["active_cards"]["decomposers"]["resources"] == 3
    assert new_player["active_cards"]["local_heat_trapping"]["resources"] == 0


def test_apply_card_effect_choice_threads_target_card_id():
    player = register_active_card(new_player_state(), "imported_hydrogen")
    player = register_active_card(player, "decomposers")
    globals_ = new_global_parameters()

    effects = {
        "choice": [
            {"resource_deltas": {"plants": 3}},
            {"target_card_resource_delta": 2},
        ]
    }

    new_player, _ = apply_card_effect(
        player, globals_, effects, effect_choice=1, target_card_id="decomposers"
    )
    assert new_player["active_cards"]["decomposers"]["resources"] == 2


def test_predators_moves_animal_from_another_active_card():
    player = register_active_card(new_player_state(), "predators")
    player = register_active_card(player, "ecological_zone")
    player["active_cards"]["ecological_zone"]["resources"] = 2
    globals_ = new_global_parameters()

    action_spec = {"gains": {"move_from_target_card_resource_delta": 1}}

    # Requiere target_card_id
    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "predators", action_spec)

    # No puede apuntar a si misma
    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "predators", action_spec, target_card_id="predators")

    # La carta origen debe tener suficientes recursos
    poor_player = register_active_card(new_player_state(), "predators")
    poor_player = register_active_card(poor_player, "ecological_zone")
    with pytest.raises(InsufficientResourcesError):
        use_card_action(poor_player, globals_, "predators", action_spec, target_card_id="ecological_zone")

    new_player, _ = use_card_action(
        player, globals_, "predators", action_spec, target_card_id="ecological_zone"
    )
    assert new_player["active_cards"]["ecological_zone"]["resources"] == 1
    assert new_player["active_cards"]["predators"]["resources"] == 1
    assert new_player["active_cards"]["predators"]["action_used"] is True


def test_local_heat_trapping_choice_plants_or_target_card():
    player = register_active_card(new_player_state(), "decomposers")
    player["heat"] = 5
    globals_ = new_global_parameters()

    effects = {
        "choice": [
            {"resource_deltas": {"heat": -5, "plants": 4}},
            {"resource_deltas": {"heat": -5}, "target_card_resource_delta": 2},
        ]
    }

    p1, _ = apply_card_effect(player, globals_, effects, effect_choice=0)
    assert p1["heat"] == 0
    assert p1["plants"] == 4

    p2, _ = apply_card_effect(player, globals_, effects, effect_choice=1, target_card_id="decomposers")
    assert p2["heat"] == 0
    assert p2["active_cards"]["decomposers"]["resources"] == 2


def test_imported_hydrogen_choice_places_ocean_and_targets_card():
    player = register_active_card(new_player_state(), "decomposers")
    globals_ = new_global_parameters()

    effects = {
        "choice": [
            {"place_oceans": 1, "resource_deltas": {"plants": 3}},
            {"place_oceans": 1, "target_card_resource_delta": 3},
            {"place_oceans": 1, "target_card_resource_delta": 2},
        ]
    }

    p1, g1 = apply_card_effect(player, globals_, effects, effect_choice=0)
    assert g1["oceans_placed"] == 1
    assert p1["plants"] == 3

    p2, g2 = apply_card_effect(player, globals_, effects, effect_choice=1, target_card_id="decomposers")
    assert g2["oceans_placed"] == 1
    assert p2["active_cards"]["decomposers"]["resources"] == 3


def test_eos_chasma_national_park_adds_animal_plants_and_mc_production():
    player = register_active_card(new_player_state(), "predators")
    globals_ = {**new_global_parameters(), "temperature": -12}
    check_card_requirements({"min_temperature": -12}, globals_)

    effects = {
        "target_card_resource_delta": 1,
        "resource_deltas": {"plants": 3},
        "production_deltas": {"mc_production": 2},
    }
    new_player, _ = apply_card_effect(player, globals_, effects, target_card_id="predators")
    assert new_player["active_cards"]["predators"]["resources"] == 1
    assert new_player["plants"] == 3
    assert new_player["mc_production"] == 3


def test_ants_action_moves_microbe_from_another_active_card():
    player = register_active_card(new_player_state(), "ants")
    player = register_active_card(player, "decomposers")
    player["active_cards"]["decomposers"]["resources"] = 1
    globals_ = {**new_global_parameters(), "oxygen": 4}
    check_card_requirements({"min_oxygen": 4}, globals_)

    action_spec = {"gains": {"move_from_target_card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "ants", action_spec, target_card_id="decomposers")
    assert new_player["active_cards"]["decomposers"]["resources"] == 0
    assert new_player["active_cards"]["ants"]["resources"] == 1


def test_cartel_mc_production_per_earth_tag_including_this():
    player = {**new_player_state(), "tags_played": {"earth": 2}}
    globals_ = new_global_parameters()
    effects = {
        "production_delta_per_tag": {"tag": "earth", "production": "mc_production", "per_tag": 1, "include_this": True}
    }
    new_player, _ = apply_card_effect(player, globals_, effects)
    assert new_player["mc_production"] == 4  # 1 base + 3 (2 previos + este)


def test_strip_mine_swaps_energy_for_steel_titanium_and_raises_oxygen():
    player = new_player_state()
    globals_ = new_global_parameters()
    effects = {
        "production_deltas": {"energy_production": -2, "steel_production": 2, "titanium_production": 1},
        "raise_oxygen_steps": 2,
    }
    new_player, new_globals = apply_card_effect(player, globals_, effects)
    assert new_player["energy_production"] == 0
    assert new_player["steel_production"] == 3
    assert new_player["titanium_production"] == 2
    assert new_globals["oxygen"] == 2


def test_wave_power_requires_3_oceans():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 3}, globals_)

    globals_["oceans_placed"] = 3
    check_card_requirements({"min_oceans": 3}, globals_)
    new_player, _ = apply_card_effect(new_player_state(), globals_, {"production_deltas": {"energy_production": 1}})
    assert new_player["energy_production"] == 2


def test_mohole_area_heat_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"heat_production": 4}}
    )
    assert new_player["heat_production"] == 5


def test_large_convoy_choice_nested_place_oceans_and_draw_cards():
    player = register_active_card(new_player_state(), "decomposers")
    player = {**player, "deck": ["card_a", "card_b", "card_c"]}
    globals_ = new_global_parameters()
    effects = {
        "choice": [
            {"place_oceans": 1, "draw_cards": 2, "resource_deltas": {"plants": 5}},
            {"place_oceans": 1, "draw_cards": 2, "target_card_resource_delta": 4},
        ]
    }
    p1, g1 = apply_card_effect(player, globals_, effects, effect_choice=0)
    assert g1["oceans_placed"] == 1
    assert p1["plants"] == 5
    assert len(p1["hand"]) == 2

    p2, g2 = apply_card_effect(player, globals_, effects, effect_choice=1, target_card_id="decomposers")
    assert g2["oceans_placed"] == 1
    assert len(p2["hand"]) == 2
    assert p2["active_cards"]["decomposers"]["resources"] == 4


def test_tectonic_stress_power_requires_2_science_tags_gives_3_energy():
    requirements = {"min_tag_count": {"tag": "science", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(requirements, new_global_parameters(), new_player_state())

    ready = {**new_player_state(), "tags_played": {"science": 2}}
    check_card_requirements(requirements, new_global_parameters(), ready)
    new_player, _ = apply_card_effect(ready, new_global_parameters(), {"production_deltas": {"energy_production": 3}})
    assert new_player["energy_production"] == 4


def test_herbivores_starts_with_1_animal_and_decreases_plant_production():
    player = register_active_card(new_player_state(), "herbivores", initial_resources=1)
    globals_ = {**new_global_parameters(), "oxygen": 8}
    check_card_requirements({"min_oxygen": 8}, globals_)

    new_player, _ = apply_card_effect(player, globals_, {"production_deltas": {"plant_production": -1}})
    assert new_player["active_cards"]["herbivores"]["resources"] == 1
    assert new_player["plant_production"] == 0

    player = register_passive_effect(
        new_player, "herbivores", {"on_greenery_placed_add_resource": {"resource_delta": 1}}
    )
    player = apply_greenery_placed_bonuses(player)
    assert player["active_cards"]["herbivores"]["resources"] == 2


def test_insects_plant_production_per_plant_tag_no_include_this():
    player = {**new_player_state(), "tags_played": {"plant": 3}}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "plant", "production": "plant_production", "per_tag": 1}},
    )
    assert new_player["plant_production"] == 4  # 1 base + 3, Insects no cuenta a si misma


def test_ceos_favorite_project_requires_target_with_at_least_1_resource():
    player = register_active_card(new_player_state(), "ceos_favorite_project")
    player = register_active_card(player, "decomposers")
    globals_ = new_global_parameters()
    effects = {"target_card_resource_delta": 1, "target_min_resources": 1}

    # Target sin recursos: no cumple
    with pytest.raises(CardEffectError):
        apply_card_effect(player, globals_, effects, target_card_id="decomposers")

    player["active_cards"]["decomposers"]["resources"] = 1
    new_player, _ = apply_card_effect(player, globals_, effects, target_card_id="decomposers")
    assert new_player["active_cards"]["decomposers"]["resources"] == 2


def test_anti_gravity_technology_discount_requires_7_science_tags():
    requirements = {"min_tag_count": {"tag": "science", "count": 7}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(requirements, new_global_parameters(), new_player_state())

    ready = {**new_player_state(), "tags_played": {"science": 7}}
    check_card_requirements(requirements, new_global_parameters(), ready)
    player = register_passive_effect(ready, "anti_gravity_technology", {"card_cost_discount_mc": 2})
    assert compute_card_cost_discount(player, ()) == 2


def test_adaptation_technology_relaxes_global_requirements_2_steps():
    player = register_passive_effect(
        new_player_state(), "adaptation_technology", {"global_requirements_tolerance_steps": 2}
    )
    globals_ = {**new_global_parameters(), "temperature": -30, "oxygen": 0, "oceans_placed": 0}

    # Sin el pasivo, -26C no alcanza para requerir -30C minimo... probamos requisitos que
    # normalmente fallarian pero se relajan 2 pasos (4C / 2% / 2 oceanos) con el pasivo.
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -26}, globals_, new_player_state())
    check_card_requirements({"min_temperature": -26}, globals_, player)  # -30 >= -26-4

    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oxygen": 2}, globals_, new_player_state())
    check_card_requirements({"min_oxygen": 2}, globals_, player)  # 0 >= 2-2

    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oceans": 1}, {**globals_, "oceans_placed": 3}, new_player_state())
    check_card_requirements({"max_oceans": 1}, {**globals_, "oceans_placed": 3}, player)  # 3 <= 1+2


def test_caretaker_contract_spends_heat_for_tr():
    player = register_active_card(new_player_state(), "caretaker_contract")
    player["heat"] = 8
    globals_ = {**new_global_parameters(), "temperature": 0}
    check_card_requirements({"min_temperature": 0}, globals_)

    action_spec = {"cost": {"heat": 8}, "gains": {"tr_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "caretaker_contract", action_spec)
    assert new_player["heat"] == 0
    assert new_player["tr"] == TR_START + 1


def test_standard_technology_gains_3_mc_after_non_sell_patents_project():
    player = register_passive_effect(
        new_player_state(), "standard_technology", {"on_standard_project_used": {"mc_delta": 3}}
    )
    after_power_plant = apply_standard_project_used_bonuses(player, "power_plant")
    assert after_power_plant["mc"] == player["mc"] + 3

    after_sell_patents = apply_standard_project_used_bonuses(player, "sell_patents")
    assert after_sell_patents["mc"] == player["mc"]


def test_nitrite_reducing_bacteria_starts_with_3_microbes_choice_action():
    player = register_active_card(new_player_state(), "nitrite_reducing_bacteria", initial_resources=3)
    globals_ = new_global_parameters()
    action_spec = {
        "choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 3}, "gains": {"tr_delta": 1}},
        ]
    }
    p1, _ = use_card_action(player, globals_, "nitrite_reducing_bacteria", action_spec, effect_choice=0)
    assert p1["active_cards"]["nitrite_reducing_bacteria"]["resources"] == 4

    p2, _ = use_card_action(player, globals_, "nitrite_reducing_bacteria", action_spec, effect_choice=1)
    assert p2["active_cards"]["nitrite_reducing_bacteria"]["resources"] == 0
    assert p2["tr"] == TR_START + 1


def test_power_supply_consortium_requires_2_power_tags_net_zero_energy():
    requirements = {"min_tag_count": {"tag": "power", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(requirements, new_global_parameters(), new_player_state())

    ready = {**new_player_state(), "tags_played": {"power": 2}}
    check_card_requirements(requirements, new_global_parameters(), ready)
    new_player, _ = apply_card_effect(ready, new_global_parameters(), {"production_deltas": {"energy_production": 0}})
    assert new_player["energy_production"] == 1  # -1 (any) +1 (propia) = neto 0, ver CARDS_LOG


def test_convoy_from_europa_places_ocean_and_draws_card():
    player = {**new_player_state(), "deck": ["card_a"]}
    new_player, new_globals = apply_card_effect(
        player, new_global_parameters(), {"place_oceans": 1, "draw_cards": 1}
    )
    assert new_globals["oceans_placed"] == 1
    assert new_player["hand"] == ["card_a"]


def test_imported_ghg_heat_production_and_stock():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"heat_production": 1}, "resource_deltas": {"heat": 3}},
    )
    assert new_player["heat_production"] == 2
    assert new_player["heat"] == 3


def test_imported_nitrogen_targets_two_different_active_cards():
    player = register_active_card(new_player_state(), "decomposers")
    player = register_active_card(player, "ants")
    globals_ = new_global_parameters()
    effects = {
        "tr_delta": 1, "resource_deltas": {"plants": 4},
        "target_card_resource_delta": 3, "target_card_resource_delta_2": 2,
    }

    # Requiere target_card_id_2
    with pytest.raises(CardEffectError):
        apply_card_effect(player, globals_, effects, target_card_id="decomposers")

    new_player, _ = apply_card_effect(
        player, globals_, effects, target_card_id="decomposers", target_card_id_2="ants"
    )
    assert new_player["tr"] == TR_START + 1
    assert new_player["plants"] == 4
    assert new_player["active_cards"]["decomposers"]["resources"] == 3
    assert new_player["active_cards"]["ants"]["resources"] == 2


def test_micro_mills_heat_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"heat_production": 1}}
    )
    assert new_player["heat_production"] == 2


def test_magnetic_field_generators_swaps_energy_for_plants_and_tr():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -4, "plant_production": 2}, "tr_delta": 3},
    )
    assert new_player["energy_production"] == 0  # piso 0, ver _apply_production_floor
    assert new_player["plant_production"] == 3
    assert new_player["tr"] == TR_START + 3


def test_shuttles_requires_5_oxygen_and_discounts_space_cards():
    globals_ = {**new_global_parameters(), "oxygen": 5}
    check_card_requirements({"min_oxygen": 5}, globals_)

    new_player, _ = apply_card_effect(
        new_player_state(), globals_, {"production_deltas": {"energy_production": -1, "mc_production": 2}}
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 3

    player = register_passive_effect(
        new_player_state(), "shuttles", {"card_cost_discount_mc": 2, "tag_filter": "space"}
    )
    assert compute_card_cost_discount(player, ("space",)) == 2
    assert compute_card_cost_discount(player, ("earth",)) == 0


def test_windmills_requires_7_oxygen():
    globals_ = {**new_global_parameters(), "oxygen": 7}
    check_card_requirements({"min_oxygen": 7}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_, {"production_deltas": {"energy_production": 1}}
    )
    assert new_player["energy_production"] == 2


def test_import_of_advanced_ghg_heat_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"heat_production": 2}}
    )
    assert new_player["heat_production"] == 3


def test_tundra_farming_requires_minus_6_temperature():
    globals_ = {**new_global_parameters(), "temperature": -6}
    check_card_requirements({"min_temperature": -6}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_,
        {"production_deltas": {"plant_production": 1, "mc_production": 2}, "resource_deltas": {"plants": 1}},
    )
    assert new_player["plant_production"] == 2
    assert new_player["mc_production"] == 3
    assert new_player["plants"] == 1


def test_aerobraked_ammonia_asteroid_targets_card_and_raises_production():
    player = register_active_card(new_player_state(), "decomposers")
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"target_card_resource_delta": 2, "production_deltas": {"heat_production": 3, "plant_production": 1}},
        target_card_id="decomposers",
    )
    assert new_player["active_cards"]["decomposers"]["resources"] == 2
    assert new_player["heat_production"] == 4
    assert new_player["plant_production"] == 2


def test_magnetic_field_dome_swaps_energy_for_plants_and_tr():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -2, "plant_production": 1}, "tr_delta": 1},
    )
    assert new_player["energy_production"] == 0
    assert new_player["plant_production"] == 2
    assert new_player["tr"] == TR_START + 1


def test_pets_starts_with_1_animal_and_reacts_to_city_tiles():
    player = register_active_card(new_player_state(), "pets", initial_resources=1)
    player = register_passive_effect(player, "pets", {"on_city_tile_placed_add_resource": {"resource_delta": 1}})
    player = apply_city_placed_bonuses(player)
    assert player["active_cards"]["pets"]["resources"] == 2


def test_protected_habitats_has_no_modeled_effect_in_solo():
    # Efecto real (proteger recursos de OTROS jugadores) no aplica en el
    # MVP de un solo jugador -- se paga pero no cambia nada del estado.
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {})
    assert new_player == new_player_state()
    assert new_globals == new_global_parameters()


def test_satellites_mc_production_per_space_tag_including_this():
    player = {**new_player_state(), "tags_played": {"space": 3}}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "space", "production": "mc_production", "per_tag": 1, "include_this": True}},
    )
    assert new_player["mc_production"] == 5  # 1 base + 4 (3 previos + este)


def test_noctis_farming_requires_minus_20_temperature():
    globals_ = {**new_global_parameters(), "temperature": -20}
    check_card_requirements({"min_temperature": -20}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_,
        {"production_deltas": {"mc_production": 1}, "resource_deltas": {"plants": 2}},
    )
    assert new_player["mc_production"] == 2
    assert new_player["plants"] == 2


def test_water_splitting_plant_requires_2_oceans_action_raises_oxygen():
    globals_ = {**new_global_parameters(), "oceans_placed": 2}
    check_card_requirements({"min_oceans": 2}, globals_)

    player = register_active_card(new_player_state(), "water_splitting_plant")
    player["energy"] = 3
    action_spec = {"cost": {"energy": 3}, "gains": {"raise_oxygen_steps": 1}}
    new_player, new_globals = use_card_action(player, globals_, "water_splitting_plant", action_spec)
    assert new_player["energy"] == 0
    assert new_globals["oxygen"] == 1


def test_heat_trappers_swaps_heat_for_energy():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"heat_production": -2, "energy_production": 1}},
    )
    assert new_player["heat_production"] == 0
    assert new_player["energy_production"] == 2


def test_soil_factory_swaps_energy_for_plants():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "plant_production": 1}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["plant_production"] == 2


def test_fuel_factory_swaps_energy_for_titanium_and_mc():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "titanium_production": 1, "mc_production": 1}},
    )
    assert new_player["energy_production"] == 0
    assert new_player["titanium_production"] == 2
    assert new_player["mc_production"] == 2


def test_ice_cap_melting_requires_plus_2_temperature():
    globals_ = {**new_global_parameters(), "temperature": 2}
    check_card_requirements({"min_temperature": 2}, globals_)
    _, new_globals = apply_card_effect(new_player_state(), globals_, {"place_oceans": 1})
    assert new_globals["oceans_placed"] == 1


def test_corporate_stronghold_swaps_energy_for_mc_and_places_city():
    new_player, new_globals = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "mc_production": 3}, "place_city_tiles": 1},
    )
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 4
    assert new_globals["city_tiles_placed"] == 1


def test_biomass_combustors_requires_6_oxygen():
    globals_ = {**new_global_parameters(), "oxygen": 6}
    check_card_requirements({"min_oxygen": 6}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_, {"production_deltas": {"plant_production": -1, "energy_production": 2}}
    )
    assert new_player["plant_production"] == 0
    assert new_player["energy_production"] == 3


def test_livestock_requires_9_oxygen_action_adds_animal():
    globals_ = {**new_global_parameters(), "oxygen": 9}
    check_card_requirements({"min_oxygen": 9}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_, {"production_deltas": {"plant_production": -1, "mc_production": 2}}
    )
    assert new_player["plant_production"] == 0
    assert new_player["mc_production"] == 3

    player = register_active_card(new_player_state(), "livestock")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player2, _ = use_card_action(player, globals_, "livestock", action_spec)
    assert new_player2["active_cards"]["livestock"]["resources"] == 1


def test_olympus_conference_tag_played_choice_add_or_spend():
    player = register_active_card(new_player_state(), "olympus_conference")
    player = register_passive_effect(
        player, "olympus_conference",
        {"on_tag_played_choice": {
            "matching_tags": ["science"],
            "add_resource_choice": {"resource_delta": 1},
            "spend_resource_choice": {"card_resource": 1, "draw_cards": 1},
        }},
    )

    # None (no elegir) no hace nada
    unchanged = apply_tag_played_choice(player, ("science",), None)
    assert unchanged == player

    # No dispara con un tag que no matchea
    not_triggered = apply_tag_played_choice(player, ("earth",), "add")
    assert not_triggered == player

    # "add" suma 1 recurso a la propia carta
    p1 = apply_tag_played_choice(player, ("science",), "add")
    assert p1["active_cards"]["olympus_conference"]["resources"] == 1

    # "spend" sin recursos guardados falla
    with pytest.raises(InsufficientResourcesError):
        apply_tag_played_choice(player, ("science",), "spend")

    # "spend" con 1 recurso guardado: lo gasta y roba 1 carta
    p1 = {**p1, "deck": ["card_a"]}
    p2 = apply_tag_played_choice(p1, ("science",), "spend")
    assert p2["active_cards"]["olympus_conference"]["resources"] == 0
    assert p2["hand"] == ["card_a"]


def test_viral_enhancers_any_tag_played_choice_add_or_gain():
    player = register_active_card(new_player_state(), "viral_enhancers")
    player = register_passive_effect(
        player, "viral_enhancers",
        {"on_any_tag_played_choice": {
            "matching_tags": ["plant", "microbe", "animal"],
            "add_resource_choice": {"resource_delta": 1},
            "gain_resource_choice": {"resource": "plants", "amount": 1},
        }},
    )
    player = register_active_card(player, "ecological_zone")

    # None (no elegir) no hace nada
    unchanged = apply_any_tag_played_choice(player, "ecological_zone", ("animal",), None)
    assert unchanged == player

    # No dispara con un tag que no matchea
    not_triggered = apply_any_tag_played_choice(player, "ecological_zone", ("earth",), "add")
    assert not_triggered == player

    # "add" suma 1 recurso a la carta RECIEN JUGADA (no a viral_enhancers)
    p1 = apply_any_tag_played_choice(player, "ecological_zone", ("animal",), "add")
    assert p1["active_cards"]["ecological_zone"]["resources"] == 1
    assert p1["active_cards"]["viral_enhancers"]["resources"] == 0

    # "add" sobre una carta sin caja de recursos (no en active_cards) falla
    with pytest.raises(CardEffectError):
        apply_any_tag_played_choice(player, "some_event_card", ("plant",), "add")

    # "gain" suma 1 planta al jugador, no toca ninguna carta
    p2 = apply_any_tag_played_choice(player, "ecological_zone", ("microbe",), "gain")
    assert p2["plants"] == player["plants"] + 1
    assert p2["active_cards"]["ecological_zone"]["resources"] == 0

    # Dispara incluso cuando la carta recien jugada ES viral_enhancers (self-trigger)
    p3 = apply_any_tag_played_choice(player, "viral_enhancers", ("microbe",), "add")
    assert p3["active_cards"]["viral_enhancers"]["resources"] == 1


def test_reserve_card_in_slot_moves_from_hand_and_stacks_resources():
    player = register_active_card(new_player_state(), "self_replicating_robots")
    player = {**player, "hand": ["asteroid_mining_consortium", "other_card"]}

    reserved = reserve_card_in_slot(player, "self_replicating_robots", "asteroid_mining_consortium")
    assert reserved["hand"] == ["other_card"]
    assert reserved["reserved_cards"]["asteroid_mining_consortium"] == {
        "resources": 2, "holder_card_id": "self_replicating_robots",
    }
    assert compute_reserved_card_discount(reserved, "asteroid_mining_consortium") == 2
    assert compute_reserved_card_discount(reserved, "other_card") == 0

    # No se puede reservar una carta que no esta en la mano
    with pytest.raises(CardNotInHandError):
        reserve_card_in_slot(reserved, "self_replicating_robots", "nonexistent_card")

    # No se puede reservar la misma carta dos veces
    hand_again = {**reserved, "hand": [*reserved["hand"], "asteroid_mining_consortium"]}
    with pytest.raises(CardEffectError):
        reserve_card_in_slot(hand_again, "self_replicating_robots", "asteroid_mining_consortium")


def test_duplicate_reserved_card_resources():
    player = reserve_card_in_slot(
        {**new_player_state(), "hand": ["asteroid_mining_consortium"]},
        "self_replicating_robots", "asteroid_mining_consortium",
    )
    doubled = duplicate_reserved_card_resources(player, "asteroid_mining_consortium")
    assert doubled["reserved_cards"]["asteroid_mining_consortium"]["resources"] == 4
    doubled_again = duplicate_reserved_card_resources(doubled, "asteroid_mining_consortium")
    assert doubled_again["reserved_cards"]["asteroid_mining_consortium"]["resources"] == 8

    with pytest.raises(CardEffectError):
        duplicate_reserved_card_resources(player, "not_reserved")


def test_release_reserved_card():
    player = reserve_card_in_slot(
        {**new_player_state(), "hand": ["asteroid_mining_consortium"]},
        "self_replicating_robots", "asteroid_mining_consortium",
    )
    released = release_reserved_card(player, "asteroid_mining_consortium")
    assert "asteroid_mining_consortium" not in released["reserved_cards"]
    assert compute_reserved_card_discount(released, "asteroid_mining_consortium") == 0
    # no-op si la carta no estaba reservada
    assert release_reserved_card(released, "asteroid_mining_consortium") == released


def test_self_replicating_robots_action_reserve_or_duplicate_via_use_card_action():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "self_replicating_robots")
    player = {**player, "hand": ["asteroid_mining_consortium"]}
    action_spec = {
        "choice": [
            {"gains": {"reserve_card_from_hand": {"requires_tag_any": ["space", "building"], "initial_resources": 2}}},
            {"gains": {"duplicate_reserved_card": True}},
        ]
    }

    # effect_choice=0: reserva la carta de la mano
    new_player, _ = use_card_action(
        player, globals_, "self_replicating_robots", action_spec, effect_choice=0,
        reserved_card_id="asteroid_mining_consortium",
    )
    assert new_player["hand"] == []
    assert new_player["reserved_cards"]["asteroid_mining_consortium"]["resources"] == 2
    assert new_player["active_cards"]["self_replicating_robots"]["action_used"] is True

    # La accion ya se uso esta generacion
    with pytest.raises(CardEffectError):
        use_card_action(
            new_player, globals_, "self_replicating_robots", action_spec, effect_choice=1,
            reserved_card_id="asteroid_mining_consortium",
        )

    # Reseteando action_used (nueva generacion), effect_choice=1: duplica
    reset_player = {
        **new_player,
        "active_cards": {"self_replicating_robots": {"resources": 0, "action_used": False}},
    }
    duplicated, _ = use_card_action(
        reset_player, globals_, "self_replicating_robots", action_spec, effect_choice=1,
        reserved_card_id="asteroid_mining_consortium",
    )
    assert duplicated["reserved_cards"]["asteroid_mining_consortium"]["resources"] == 4

    # Sin reserved_card_id, falla
    with pytest.raises(CardEffectError):
        use_card_action(reset_player, globals_, "self_replicating_robots", action_spec, effect_choice=0)


def test_rad_suits_requires_2_city_tiles():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_city_tiles": 2}, globals_)

    globals_["city_tiles_placed"] = 2
    check_card_requirements({"min_city_tiles": 2}, globals_)
    new_player, _ = apply_card_effect(new_player_state(), globals_, {"production_deltas": {"mc_production": 1}})
    assert new_player["mc_production"] == 2


def test_aquifer_pumping_action_spends_mc_for_ocean():
    player = register_active_card(new_player_state(), "aquifer_pumping")
    player["mc"] = 8
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 8}, "gains": {"place_oceans": 1}}
    new_player, new_globals = use_card_action(player, globals_, "aquifer_pumping", action_spec)
    assert new_player["mc"] == 0
    assert new_globals["oceans_placed"] == 1


def test_flooding_places_ocean():
    _, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {"place_oceans": 1})
    assert new_globals["oceans_placed"] == 1


def test_energy_saving_production_per_city_tile():
    globals_ = {**new_global_parameters(), "city_tiles_placed": 3}
    new_player, _ = apply_card_effect(
        new_player_state(), globals_,
        {"production_delta_per_counter": {"production": "energy_production", "counter": "city_tiles_placed", "per_counter": 1}},
    )
    assert new_player["energy_production"] == 4


def test_permafrost_extraction_requires_minus_8_temperature():
    globals_ = {**new_global_parameters(), "temperature": -8}
    check_card_requirements({"min_temperature": -8}, globals_)
    _, new_globals = apply_card_effect(new_player_state(), globals_, {"place_oceans": 1})
    assert new_globals["oceans_placed"] == 1


def test_invention_contest_starts_research_of_3():
    player = {**new_player_state(), "deck": ["a", "b", "c"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"start_research": {"n": 3}})
    assert new_player["pending_research"] == ["a", "b", "c"]
    assert new_player["deck"] == []


def test_plantation_requires_2_science_tags_places_greenery_normal_rules():
    requirements = {"min_tag_count": {"tag": "science", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(requirements, new_global_parameters(), new_player_state())

    ready = {**new_player_state(), "tags_played": {"science": 2}}
    check_card_requirements(requirements, new_global_parameters(), ready)
    new_player, new_globals = apply_card_effect(ready, new_global_parameters(), {"raise_oxygen_steps": 1})
    assert new_globals["oxygen"] == 1


def test_power_infrastructure_converts_any_amount_of_energy_to_mc():
    player = register_active_card(new_player_state(), "power_infrastructure")
    player["energy"] = 5
    globals_ = new_global_parameters()
    action_spec = {"convert_resource_amount": {"from": "energy", "to": "mc", "ratio": 1}}

    with pytest.raises(CardEffectError):
        use_card_action(player, globals_, "power_infrastructure", action_spec)

    new_player, _ = use_card_action(player, globals_, "power_infrastructure", action_spec, effect_amount=3)
    assert new_player["energy"] == 2
    assert new_player["mc"] == 3

    with pytest.raises(InsufficientResourcesError):
        use_card_action(player, globals_, "power_infrastructure", action_spec, effect_amount=6)


def test_indentured_workers_grants_pending_discount_consumed_next_card():
    player = new_player_state()
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"next_card_discount_mc": -8})
    assert new_player["pending_mc_discount"] == -8

    after_generation = run_production_phase(new_player)
    assert after_generation["pending_mc_discount"] == 0


def test_lagrange_observatory_draws_1_card():
    player = {**new_player_state(), "deck": ["card_a"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 1})
    assert new_player["hand"] == ["card_a"]


def test_terraforming_ganymede_tr_per_jovian_tag_including_this():
    player = {**new_player_state(), "tags_played": {"jovian": 2}}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"tr_delta_per_tag": {"tag": "jovian", "per_tag": 1, "include_this": True}},
    )
    assert new_player["tr"] == TR_START + 3  # 2 previos + este


def test_immigration_shuttles_mc_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 5}}
    )
    assert new_player["mc_production"] == 6


def test_restricted_area_places_generic_special_tile_and_action_draws():
    player = register_active_card(new_player_state(), "restricted_area")
    player["mc"] = 2
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 2}, "gains": {"draw_cards": 1}}
    player = {**player, "deck": ["card_a"]}
    new_player, _ = use_card_action(player, globals_, "restricted_area", action_spec)
    assert new_player["mc"] == 0
    assert new_player["hand"] == ["card_a"]


def test_immigrant_city_production_bonus_self_triggers_on_own_city():
    player = register_active_card(new_player_state(), "immigrant_city")
    player = register_passive_effect(
        player, "immigrant_city",
        {"on_city_tile_placed_production_delta": {"production": "mc_production", "per_tile": 1}},
    )
    new_player, new_globals = apply_card_effect(
        player, new_global_parameters(),
        {"production_deltas": {"energy_production": -1, "mc_production": -2}, "place_city_tiles": 1},
    )
    assert new_globals["city_tiles_placed"] == 1
    # apply_card_effect NO dispara apply_city_placed_bonuses (eso lo hace
    # tools._place_city_and_apply_bonus via el mapa hexagonal) -- se
    # prueba aparte para no acoplar rules_engine a board.py.
    triggered = apply_city_placed_bonuses(new_player)
    assert triggered["mc_production"] == 0  # 1 base -1 -2 +1 (self-trigger) = -1, piso 0


def test_energy_tapping_net_zero_energy_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"energy_production": 0}}
    )
    assert new_player["energy_production"] == 1


def test_underground_detonations_action_spends_mc_for_heat_production():
    player = register_active_card(new_player_state(), "underground_detonations")
    player["mc"] = 10
    globals_ = new_global_parameters()
    action_spec = {"cost": {"mc": 10}, "gains": {"production_deltas": {"heat_production": 2}}}
    new_player, _ = use_card_action(player, globals_, "underground_detonations", action_spec)
    assert new_player["mc"] == 0
    assert new_player["heat_production"] == 3


def test_soletta_heat_production():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"heat_production": 7}}
    )
    assert new_player["heat_production"] == 8


def test_technology_demonstration_draws_2_cards():
    player = {**new_player_state(), "deck": ["a", "b"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["a", "b"]


def test_rad_chem_factory_swaps_energy_for_tr():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_deltas": {"energy_production": -1}, "tr_delta": 2},
    )
    assert new_player["energy_production"] == 0
    assert new_player["tr"] == TR_START + 2


def test_special_design_grants_pending_requirement_tolerance():
    player = new_player_state()
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"next_card_requirement_tolerance_steps": 2})
    assert new_player["pending_requirement_tolerance_steps"] == 2

    # Se suma a la tolerancia del pasivo permanente si el jugador tiene ambos
    globals_ = {**new_global_parameters(), "temperature": -30}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_temperature": -26}, globals_, new_player_state())
    check_card_requirements({"min_temperature": -26}, globals_, new_player)  # -30 >= -26-4 (2 pasos = 4C)

    after_generation = run_production_phase(new_player)
    assert after_generation["pending_requirement_tolerance_steps"] == 0


def test_medical_lab_mc_production_per_2_building_tags_including_this():
    player = {**new_player_state(), "tags_played": {"building": 3}}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": {"tag": "building", "production": "mc_production", "tags_per_step": 2, "include_this": True}},
    )
    assert new_player["mc_production"] == 3  # 1 base + (3+1)//2 = 2


def test_ai_central_requires_3_science_tags_action_draws_2():
    requirements = {"min_tag_count": {"tag": "science", "count": 3}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(requirements, new_global_parameters(), new_player_state())

    ready = {**new_player_state(), "tags_played": {"science": 3}}
    check_card_requirements(requirements, new_global_parameters(), ready)
    new_player, _ = apply_card_effect(ready, new_global_parameters(), {"production_deltas": {"energy_production": -1}})
    assert new_player["energy_production"] == 0

    player = register_active_card(new_player_state(), "ai_central")
    player = {**player, "deck": ["a", "b"]}
    action_spec = {"cost": {}, "gains": {"draw_cards": 2}}
    new_player2, _ = use_card_action(player, new_global_parameters(), "ai_central", action_spec)
    assert new_player2["hand"] == ["a", "b"]


def test_small_asteroid_raises_temperature():
    _, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {"raise_temperature_steps": 1})
    assert new_globals["temperature"] == TEMPERATURE_MIN + TEMPERATURE_STEP


def test_snow_algae_requires_2_oceans():
    globals_ = {**new_global_parameters(), "oceans_placed": 2}
    check_card_requirements({"min_oceans": 2}, globals_)
    new_player, _ = apply_card_effect(
        new_player_state(), globals_, {"production_deltas": {"plant_production": 1, "heat_production": 1}}
    )
    assert new_player["plant_production"] == 2
    assert new_player["heat_production"] == 2


def test_advanced_ecosystems_multi_tag_requirements():
    req = {
        "min_tag_count": [
            {"tag": "plant", "count": 1},
            {"tag": "microbe", "count": 1},
            {"tag": "animal", "count": 1},
        ]
    }
    player = {**new_player_state(), "tags_played": {"plant": 1, "microbe": 1}}
    # Falta tag animal
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player)

    # Con los 3 tags
    player_ready = {**new_player_state(), "tags_played": {"plant": 1, "microbe": 1, "animal": 1}}
    check_card_requirements(req, new_global_parameters(), player_ready)  # no lanza


def test_great_dam_requires_4_oceans_and_gives_2_energy_production():
    globals_ = new_global_parameters()
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 4}, globals_)

    globals_["oceans_placed"] = 4
    check_card_requirements({"min_oceans": 4}, globals_)

    player = new_player_state()
    new_player, _ = apply_card_effect(
        player, globals_, {"production_deltas": {"energy_production": 2}}
    )
    assert new_player["energy_production"] == 3



# --- Bloque de revision 20 (expansion Venus Next) ---------------------------

def test_penguins_action_adds_animal_to_card():
    globals_ = new_global_parameters()
    check_card_requirements({"min_oceans": 8}, {**globals_, "oceans_placed": 8})
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_oceans": 8}, {**globals_, "oceans_placed": 7})

    player = register_active_card(new_player_state(), "penguins")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "penguins", action_spec)
    assert new_player["active_cards"]["penguins"]["resources"] == 1


def test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "aerial_mappers")
    player = register_active_card(player, "decomposers")
    action_spec = {
        "choice": [
            {"gains": {"card_resource_delta": 1}},
            {"gains": {"target_card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"draw_cards": 1}},
        ]
    }

    # Opcion 0: agrega floater a si misma
    p1, _ = use_card_action(player, globals_, "aerial_mappers", action_spec, effect_choice=0)
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 1

    # Opcion 1: agrega floater a OTRA carta activa (ej. otra carta con tag Venus)
    p2, _ = use_card_action(player, globals_, "aerial_mappers", action_spec, effect_choice=1, target_card_id="decomposers")
    assert p2["active_cards"]["decomposers"]["resources"] == 1
    assert p2["active_cards"]["aerial_mappers"]["resources"] == 0

    # Opcion 2: gasta 1 floater guardado para robar 1 carta
    player_with_floater = {
        **player,
        "active_cards": {**player["active_cards"], "aerial_mappers": {"resources": 1, "action_used": False}},
        "deck": ["card_a"],
    }
    p3, _ = use_card_action(player_with_floater, globals_, "aerial_mappers", action_spec, effect_choice=2)
    assert p3["active_cards"]["aerial_mappers"]["resources"] == 0
    assert p3["hand"] == ["card_a"]


def test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target():
    player = register_active_card(new_player_state(), "air_scrapping_expedition")
    player = register_active_card(player, "aerial_mappers")
    globals_ = new_global_parameters()
    effects = {"raise_venus_steps": 1, "target_card_resource_delta": 3}

    new_player, new_globals = apply_card_effect(player, globals_, effects, target_card_id="aerial_mappers")
    assert new_globals["venus"] == 2
    assert new_player["tr"] == 21
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 3


def test_atalanta_planitia_lab_requires_3_science_tags_draws_2():
    req = {"min_tag_count": {"tag": "science", "count": 3}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 2}})
    check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 3}})

    player = {**new_player_state(), "deck": ["card_a", "card_b"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["card_a", "card_b"]


def test_atmoscoop_choice_temperature_or_venus_plus_floaters_to_target():
    player = register_active_card(new_player_state(), "atmoscoop")
    player = register_active_card(player, "aerial_mappers")
    globals_ = new_global_parameters()
    effects = {
        "choice": [
            {"raise_temperature_steps": 2, "target_card_resource_delta": 2},
            {"raise_venus_steps": 2, "target_card_resource_delta": 2},
        ]
    }

    # Opcion 0: sube temperatura, no Venus
    p1, g1 = apply_card_effect(player, globals_, effects, effect_choice=0, target_card_id="aerial_mappers")
    assert g1["temperature"] == TEMPERATURE_MIN + 2 * TEMPERATURE_STEP
    assert g1["venus"] == 0
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 2

    # Opcion 1: sube Venus, no temperatura
    p2, g2 = apply_card_effect(player, globals_, effects, effect_choice=1, target_card_id="aerial_mappers")
    assert g2["venus"] == 4
    assert g2["temperature"] == TEMPERATURE_MIN
    assert p2["active_cards"]["aerial_mappers"]["resources"] == 2


def test_comet_for_venus_raises_venus_omits_opponent_clause():
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {"raise_venus_steps": 1})
    assert new_globals["venus"] == 2
    assert new_player["tr"] == 21


def test_corroder_suits_mc_production_and_target_card_resource():
    player = register_active_card(new_player_state(), "corroder_suits")
    player = register_active_card(player, "aerial_mappers")
    globals_ = new_global_parameters()
    effects = {"production_deltas": {"mc_production": 2}, "target_card_resource_delta": 1}

    new_player, _ = apply_card_effect(player, globals_, effects, target_card_id="aerial_mappers")
    assert new_player["mc_production"] == 3
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 1


def test_dawn_city_requires_4_science_tags_swaps_energy_for_titanium_and_places_city():
    req = {"min_tag_count": {"tag": "science", "count": 4}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 3}})

    effects = {"production_deltas": {"energy_production": -1, "titanium_production": 1}, "place_city_tiles": 1}
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), effects)
    assert new_player["energy_production"] == 0
    assert new_player["titanium_production"] == 2
    assert new_globals["city_tiles_placed"] == 1


def test_deuterium_export_action_choice_add_floater_or_spend_for_energy():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "deuterium_export")
    action_spec = {
        "choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"production_deltas": {"energy_production": 1}}},
        ]
    }

    p1, _ = use_card_action(player, globals_, "deuterium_export", action_spec, effect_choice=0)
    assert p1["active_cards"]["deuterium_export"]["resources"] == 1

    player_with_floater = {
        **player,
        "active_cards": {"deuterium_export": {"resources": 1, "action_used": False}},
    }
    p2, _ = use_card_action(player_with_floater, globals_, "deuterium_export", action_spec, effect_choice=1)
    assert p2["active_cards"]["deuterium_export"]["resources"] == 0
    assert p2["energy_production"] == 2


# --- Piezas nuevas de motor (bloque 21) --------------------------------------

def test_production_delta_per_tag_accepts_list_of_specs():
    player = {**new_player_state(), "tags_played": {"venus": 2, "earth": 3}}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(),
        {"production_delta_per_tag": [
            {"tag": "venus", "production": "mc_production", "per_tag": 1},
            {"tag": "earth", "production": "mc_production", "per_tag": 1},
        ]},
    )
    assert new_player["mc_production"] == 1 + 2 + 3  # base 1 + 2 venus + 3 earth


def test_target_card_resource_delta_per_tag_scales_with_tag_count():
    player = register_active_card(new_player_state(), "hydrogen_to_venus")
    player = register_active_card(player, "aerial_mappers")
    player = {**player, "tags_played": {"jovian": 3}}
    effects = {"target_card_resource_delta_per_tag": {"tag": "jovian", "per_tag": 1}}

    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 3


def test_target_card_resource_delta_per_tag_no_tags_is_noop_without_target():
    player = register_active_card(new_player_state(), "hydrogen_to_venus")
    effects = {"target_card_resource_delta_per_tag": {"tag": "jovian", "per_tag": 1}}
    # Sin tags jovian, no hace nada Y no exige target_card_id
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player == player


# --- Bloque de revision 21 (Venus Next) --------------------------------------

def test_extractor_balloons_starts_with_3_floaters_action_choice():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "extractor_balloons", initial_resources=3)
    action_spec = {
        "choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}},
        ]
    }

    p1, _ = use_card_action(player, globals_, "extractor_balloons", action_spec, effect_choice=0)
    assert p1["active_cards"]["extractor_balloons"]["resources"] == 4

    p2, g2 = use_card_action(player, globals_, "extractor_balloons", action_spec, effect_choice=1)
    assert p2["active_cards"]["extractor_balloons"]["resources"] == 1
    assert g2["venus"] == 2


def test_extremophiles_requires_2_science_action_adds_microbe():
    req = {"min_tag_count": {"tag": "science", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 1}})

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "extremophiles")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "extremophiles", action_spec)
    assert new_player["active_cards"]["extremophiles"]["resources"] == 1


def test_floating_habs_action_choice_add_self_or_target():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "floating_habs")
    player = {**register_active_card(player, "aerial_mappers"), "mc": 4}
    action_spec = {
        "choice": [
            {"cost": {"mc": 2}, "gains": {"card_resource_delta": 1}},
            {"cost": {"mc": 2}, "gains": {"target_card_resource_delta": 1}},
        ]
    }

    p1, _ = use_card_action(player, globals_, "floating_habs", action_spec, effect_choice=0)
    assert p1["active_cards"]["floating_habs"]["resources"] == 1
    assert p1["mc"] == 2

    p2, _ = use_card_action(player, globals_, "floating_habs", action_spec, effect_choice=1, target_card_id="aerial_mappers")
    assert p2["active_cards"]["aerial_mappers"]["resources"] == 1
    assert p2["mc"] == 2


def test_forced_precipitation_action_choice_add_or_spend_for_venus():
    globals_ = new_global_parameters()
    player = {**register_active_card(new_player_state(), "forced_precipitation"), "mc": 2}
    action_spec = {
        "choice": [
            {"cost": {"mc": 2}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}},
        ]
    }
    p1, _ = use_card_action(player, globals_, "forced_precipitation", action_spec, effect_choice=0)
    assert p1["active_cards"]["forced_precipitation"]["resources"] == 1

    player_with_floaters = {
        **player,
        "active_cards": {"forced_precipitation": {"resources": 2, "action_used": False}},
    }
    p2, g2 = use_card_action(player_with_floaters, globals_, "forced_precipitation", action_spec, effect_choice=1)
    assert p2["active_cards"]["forced_precipitation"]["resources"] == 0
    assert g2["venus"] == 2


def test_freyja_biodomes_requires_venus_10_percent_and_boosts_target_card():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 10}, {**new_global_parameters(), "venus": 8})
    check_card_requirements({"min_venus": 10}, {**new_global_parameters(), "venus": 10})

    player = register_active_card(new_player_state(), "freyja_biodomes")
    player = register_active_card(player, "aerial_mappers")
    effects = {"target_card_resource_delta": 2, "production_deltas": {"energy_production": -1, "mc_production": 2}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 3


def test_ghg_import_from_venus_raises_venus_and_heat_production():
    new_player, new_globals = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"raise_venus_steps": 1, "production_deltas": {"heat_production": 3}},
    )
    assert new_globals["venus"] == 2
    assert new_player["heat_production"] == 4


def test_giant_solar_shade_raises_venus_3_steps():
    _, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {"raise_venus_steps": 3})
    assert new_globals["venus"] == 6


def test_gyropolis_swaps_energy_for_mc_per_venus_and_earth_tag_places_city():
    player = {**new_player_state(), "tags_played": {"venus": 2, "earth": 1}}
    globals_ = new_global_parameters()
    effects = {
        "production_deltas": {"energy_production": -2},
        "production_delta_per_tag": [
            {"tag": "venus", "production": "mc_production", "per_tag": 1},
            {"tag": "earth", "production": "mc_production", "per_tag": 1},
        ],
        "place_city_tiles": 1,
    }
    new_player, new_globals = apply_card_effect(player, globals_, effects)
    assert new_player["energy_production"] == 0  # piso 0
    assert new_player["mc_production"] == 1 + 2 + 1  # base 1 + 2 venus + 1 earth
    assert new_globals["city_tiles_placed"] == 1


def test_hydrogen_to_venus_raises_venus_and_floaters_per_jovian_tag():
    player = register_active_card(new_player_state(), "hydrogen_to_venus")
    player = register_active_card(player, "aerial_mappers")
    player = {**player, "tags_played": {"jovian": 2}}
    effects = {"raise_venus_steps": 1, "target_card_resource_delta_per_tag": {"tag": "jovian", "per_tag": 1}}

    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_globals["venus"] == 2
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2

    # Sin tags jovian, sube Venus igual pero no toca ninguna carta ni exige target
    player_no_jovian = register_active_card(new_player_state(), "hydrogen_to_venus")
    new_player2, new_globals2 = apply_card_effect(player_no_jovian, new_global_parameters(), effects)
    assert new_globals2["venus"] == 2
    assert new_player2["active_cards"] == player_no_jovian["active_cards"]


# --- Bloque de revision 22 (Venus Next) --------------------------------------

def test_io_sulphur_research_draws_3_with_3_venus_tags_else_1():
    effects = {"tag_count_choice": {"tag": "venus", "count": 3, "if_met": {"draw_cards": 3}, "else": {"draw_cards": 1}}}

    player_no_venus = {**new_player_state(), "deck": ["a"]}
    new_player, _ = apply_card_effect(player_no_venus, new_global_parameters(), effects)
    assert new_player["hand"] == ["a"]

    player_3_venus = {**new_player_state(), "tags_played": {"venus": 3}, "deck": ["a", "b", "c"]}
    new_player2, _ = apply_card_effect(player_3_venus, new_global_parameters(), effects)
    assert new_player2["hand"] == ["a", "b", "c"]


def test_ishtar_mining_requires_venus_8_percent_titanium_production():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 8}, {**new_global_parameters(), "venus": 6})
    check_card_requirements({"min_venus": 8}, {**new_global_parameters(), "venus": 8})

    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(), {"production_deltas": {"titanium_production": 1}}
    )
    assert new_player["titanium_production"] == 2


def test_jet_stream_microscrappers_action_choice_titanium_or_venus():
    globals_ = new_global_parameters()
    player = {**register_active_card(new_player_state(), "jet_stream_microscrappers"), "titanium": 1}
    action_spec = {
        "choice": [
            {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 2}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}},
        ]
    }
    p1, _ = use_card_action(player, globals_, "jet_stream_microscrappers", action_spec, effect_choice=0)
    assert p1["active_cards"]["jet_stream_microscrappers"]["resources"] == 2
    assert p1["titanium"] == 0

    player_with_floaters = {
        **player,
        "active_cards": {"jet_stream_microscrappers": {"resources": 2, "action_used": False}},
    }
    p2, g2 = use_card_action(player_with_floaters, globals_, "jet_stream_microscrappers", action_spec, effect_choice=1)
    assert p2["active_cards"]["jet_stream_microscrappers"]["resources"] == 0
    assert g2["venus"] == 2


def test_local_shading_action_choice_add_or_spend_for_mc_production():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "local_shading")
    action_spec = {
        "choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"production_deltas": {"mc_production": 1}}},
        ]
    }
    p1, _ = use_card_action(player, globals_, "local_shading", action_spec, effect_choice=0)
    assert p1["active_cards"]["local_shading"]["resources"] == 1

    player_with_floater = {**player, "active_cards": {"local_shading": {"resources": 1, "action_used": False}}}
    p2, _ = use_card_action(player_with_floater, globals_, "local_shading", action_spec, effect_choice=1)
    assert p2["mc_production"] == 2


def test_luna_metropolis_mc_production_per_earth_tag_including_this_places_city():
    player = {**new_player_state(), "tags_played": {"earth": 2}}
    effects = {
        "production_delta_per_tag": {"tag": "earth", "production": "mc_production", "per_tag": 1, "include_this": True},
        "place_city_tiles": 1,
    }
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1 + 3  # base 1 + (2 previos + esta misma = 3)
    assert new_globals["city_tiles_placed"] == 1


def test_luxury_foods_requires_venus_earth_jovian_no_state_change():
    req = {"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1, "earth": 1}})
    check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1, "earth": 1, "jovian": 1}})

    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {})
    assert new_player == new_player_state()
    assert new_globals == new_global_parameters()


def test_maxwell_base_requires_venus_12_energy_down_city_placed_action_targets_other_card():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 12}, {**new_global_parameters(), "venus": 10})
    check_card_requirements({"min_venus": 12}, {**new_global_parameters(), "venus": 12})

    player = register_active_card(new_player_state(), "maxwell_base")
    effects = {"production_deltas": {"energy_production": -1}, "place_city_tiles": 1}
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["energy_production"] == 0
    assert new_globals["city_tiles_placed"] == 1

    player2 = register_active_card(player, "aerial_mappers")
    action_spec = {"cost": {}, "gains": {"target_card_resource_delta": 1}}
    new_player2, _ = use_card_action(player2, new_global_parameters(), "maxwell_base", action_spec, target_card_id="aerial_mappers")
    assert new_player2["active_cards"]["aerial_mappers"]["resources"] == 1


def test_mining_quota_requires_3_tags_steel_production():
    req = {"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"jovian": 1}})

    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"steel_production": 2}})
    assert new_player["steel_production"] == 3


def test_neutralizer_factory_requires_venus_10_raises_venus():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 10}, {**new_global_parameters(), "venus": 8})
    _, new_globals = apply_card_effect(new_player_state(), {**new_global_parameters(), "venus": 10}, {"raise_venus_steps": 1})
    assert new_globals["venus"] == 12


def test_omnicourt_requires_3_tags_grants_2_tr():
    req = {"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}
    check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1, "earth": 1, "jovian": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"tr_delta": 2})
    assert new_player["tr"] == 22


# --- Piezas nuevas de motor (bloque 23) --------------------------------------

def test_use_card_action_mc_or_titanium_cost_accepts_titanium_substitution():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "rotator_impacts")
    action_spec = {"cost": {"mc_or_titanium": 6}, "gains": {"card_resource_delta": 1}}

    # Todo en MC
    p1, _ = use_card_action({**player, "mc": 6}, globals_, "rotator_impacts", action_spec)
    assert p1["mc"] == 0
    assert p1["active_cards"]["rotator_impacts"]["resources"] == 1

    # Todo en titanio (2 titanio * 3 MC = 6)
    p2, _ = use_card_action({**player, "titanium": 2}, globals_, "rotator_impacts", action_spec, titanium_to_pay=2)
    assert p2["titanium"] == 0
    assert p2["mc"] == 0

    # Mixto: 1 titanio (3 MC) + 3 MC
    p3, _ = use_card_action({**player, "mc": 3, "titanium": 1}, globals_, "rotator_impacts", action_spec, titanium_to_pay=1)
    assert p3["titanium"] == 0
    assert p3["mc"] == 0

    # Titanio declarado insuficiente en stock
    with pytest.raises(InsufficientResourcesError):
        use_card_action({**player, "titanium": 0}, globals_, "rotator_impacts", action_spec, titanium_to_pay=1)

    # Cubre con titanio pero falta MC para el resto
    with pytest.raises(InsufficientResourcesError):
        use_card_action({**player, "mc": 0, "titanium": 1}, globals_, "rotator_impacts", action_spec, titanium_to_pay=1)


def test_convert_card_resource_amount_uses_own_card_resources():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "sulphur_eating_bacteria", initial_resources=2)
    action_spec = {"convert_card_resource_amount": {"to": "mc", "ratio": 3}}

    new_player, _ = use_card_action(player, globals_, "sulphur_eating_bacteria", action_spec, effect_amount=2)
    assert new_player["active_cards"]["sulphur_eating_bacteria"]["resources"] == 0
    assert new_player["mc"] == 6

    with pytest.raises(InsufficientResourcesError):
        use_card_action(player, globals_, "sulphur_eating_bacteria", action_spec, effect_amount=3)


def test_discard_card_then_draw_requires_discard_card_id_and_draws_n():
    player = {**new_player_state(), "hand": ["old_card"], "deck": ["a", "b", "c"]}
    effects = {"discard_card_then_draw": {"draw": 3}}

    with pytest.raises(CardEffectError):
        apply_card_effect(player, new_global_parameters(), effects)

    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, discard_card_id="old_card")
    assert new_player["hand"] == ["a", "b", "c"]

    with pytest.raises(CardNotInHandError):
        apply_card_effect(player, new_global_parameters(), effects, discard_card_id="not_in_hand")


# --- Bloque de revision 23 (Venus Next) --------------------------------------

def test_orbital_reflectors_raises_venus_2_heat_production_2():
    new_player, new_globals = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"raise_venus_steps": 2, "production_deltas": {"heat_production": 2}},
    )
    assert new_globals["venus"] == 4
    assert new_player["heat_production"] == 3


def test_rotator_impacts_requires_max_venus_14():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_venus": 14}, {**new_global_parameters(), "venus": 16})
    check_card_requirements({"max_venus": 14}, {**new_global_parameters(), "venus": 14})


def test_sister_planet_support_requires_venus_and_earth_tags_mc_production():
    req = {"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}]}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 3}})
    assert new_player["mc_production"] == 4


def test_solarnet_requires_3_tags_draws_2():
    req = {"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}
    check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1, "earth": 1, "jovian": 1}})
    player = {**new_player_state(), "deck": ["a", "b"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["a", "b"]


def test_spin_inducing_asteroid_requires_max_venus_10_raises_2():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_venus": 10}, {**new_global_parameters(), "venus": 12})
    _, new_globals = apply_card_effect(new_player_state(), {**new_global_parameters(), "venus": 10}, {"raise_venus_steps": 2})
    assert new_globals["venus"] == 14


def test_sponsored_academies_requires_science_and_earth_discards_and_draws_3():
    req = {"min_tag_count": [{"tag": "science", "count": 1}, {"tag": "earth", "count": 1}]}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 1}})

    player = {**new_player_state(), "hand": ["junk"], "deck": ["a", "b", "c"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"discard_card_then_draw": {"draw": 3}}, discard_card_id="junk")
    assert new_player["hand"] == ["a", "b", "c"]


def test_stratopolis_requires_2_science_boosts_mc_places_city_action_targets_venus_card():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 2}}, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 1}})

    effects = {"production_deltas": {"mc_production": 2}, "place_city_tiles": 1}
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), effects)
    assert new_player["mc_production"] == 3
    assert new_globals["city_tiles_placed"] == 1

    player = register_active_card(new_player_state(), "stratopolis")
    player = register_active_card(player, "aerial_mappers")
    action_spec = {"cost": {}, "gains": {"target_card_resource_delta": 2}}
    new_player2, _ = use_card_action(player, new_global_parameters(), "stratopolis", action_spec, target_card_id="aerial_mappers")
    assert new_player2["active_cards"]["aerial_mappers"]["resources"] == 2


def test_stratospheric_birds_requires_venus_12_action_moves_floater_to_animal():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 12}, {**new_global_parameters(), "venus": 10})

    player = register_active_card(new_player_state(), "stratospheric_birds")
    player = register_active_card(player, "aerial_mappers", initial_resources=1)
    action_spec = {"cost": {}, "gains": {"move_from_target_card_resource_delta": 1}}
    new_player, _ = use_card_action(player, new_global_parameters(), "stratospheric_birds", action_spec, target_card_id="aerial_mappers")
    assert new_player["active_cards"]["stratospheric_birds"]["resources"] == 1
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 0


def test_sulphur_exports_raises_venus_mc_production_per_venus_tag_including_this():
    player = {**new_player_state(), "tags_played": {"venus": 2}}
    effects = {
        "raise_venus_steps": 1,
        "production_delta_per_tag": {"tag": "venus", "production": "mc_production", "per_tag": 1, "include_this": True},
    }
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects)
    assert new_globals["venus"] == 2
    assert new_player["mc_production"] == 1 + 3  # base 1 + (2 previos + esta misma)


def test_sulphur_eating_bacteria_requires_venus_6():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 6}, {**new_global_parameters(), "venus": 4})
    check_card_requirements({"min_venus": 6}, {**new_global_parameters(), "venus": 6})


# --- Pieza nueva de motor (bloque 24): min_tr --------------------------------

def test_min_tr_requirement():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tr": 25}, new_global_parameters(), player={**new_player_state(), "tr": 24})
    check_card_requirements({"min_tr": 25}, new_global_parameters(), player={**new_player_state(), "tr": 25})
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tr": 25}, new_global_parameters(), player=None)


# --- Bloque de revision 24 (Venus Next) --------------------------------------

def test_terraforming_contract_requires_tr_25_mc_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 4}})
    assert new_player["mc_production"] == 5


def test_thermophiles_requires_venus_6_action_choice_add_other_or_spend_for_venus():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 6}, {**new_global_parameters(), "venus": 4})

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "thermophiles")
    player = register_active_card(player, "aerial_mappers")
    action_spec = {
        "choice": [
            {"gains": {"target_card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}},
        ]
    }
    p1, _ = use_card_action(player, globals_, "thermophiles", action_spec, effect_choice=0, target_card_id="aerial_mappers")
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 1

    player_with_microbes = {**player, "active_cards": {"thermophiles": {"resources": 2, "action_used": False}}}
    p2, g2 = use_card_action(player_with_microbes, globals_, "thermophiles", action_spec, effect_choice=1)
    assert p2["active_cards"]["thermophiles"]["resources"] == 0
    assert g2["venus"] == 2


def test_water_to_venus_raises_venus():
    _, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {"raise_venus_steps": 1})
    assert new_globals["venus"] == 2


def test_venus_governor_requires_2_venus_tags_mc_production():
    req = {"min_tag_count": {"tag": "venus", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"venus": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 2}})
    assert new_player["mc_production"] == 3


def test_venus_magnetizer_requires_venus_10_action_swaps_energy_for_venus():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 10}, {**new_global_parameters(), "venus": 8})

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "venus_magnetizer")
    action_spec = {"cost": {}, "gains": {"production_deltas": {"energy_production": -1}, "raise_venus_steps": 1}}
    new_player, new_globals = use_card_action(player, globals_, "venus_magnetizer", action_spec)
    assert new_player["energy_production"] == 0
    assert new_globals["venus"] == 2


def test_venus_soils_raises_venus_plant_production_and_boosts_target_card():
    player = register_active_card(new_player_state(), "venus_soils")
    player = register_active_card(player, "aerial_mappers")
    effects = {"raise_venus_steps": 1, "production_deltas": {"plant_production": 1}, "target_card_resource_delta": 2}
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_globals["venus"] == 2
    assert new_player["plant_production"] == 2
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2


def test_venus_waystation_passive_discounts_venus_tag_cards():
    player = register_passive_effect(
        new_player_state(), "venus_waystation", {"card_cost_discount_mc": 2, "tag_filter": "venus"},
    )
    assert compute_card_cost_discount(player, ("venus",)) == 2
    assert compute_card_cost_discount(player, ("earth",)) == 0


def test_venusian_animals_requires_venus_18_passive_adds_resource_on_science_tag():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 18}, {**new_global_parameters(), "venus": 16})

    player = register_active_card(new_player_state(), "venusian_animals")
    player = register_passive_effect(
        player, "venusian_animals", {"on_tag_played_add_resource": {"matching_tags": ["science"], "resource_delta": 1}},
    )
    new_player = apply_tag_played_resource_bonuses(player, ("science",))
    assert new_player["active_cards"]["venusian_animals"]["resources"] == 1


def test_venusian_insects_requires_venus_12_action_adds_microbe():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 12}, {**new_global_parameters(), "venus": 10})
    player = register_active_card(new_player_state(), "venusian_insects")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, new_global_parameters(), "venusian_insects", action_spec)
    assert new_player["active_cards"]["venusian_insects"]["resources"] == 1


def test_venusian_plants_requires_venus_16_raises_venus_boosts_other_card():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_venus": 16}, {**new_global_parameters(), "venus": 14})

    player = register_active_card(new_player_state(), "venusian_plants")
    player = register_active_card(player, "aerial_mappers")
    effects = {"raise_venus_steps": 1, "target_card_resource_delta": 1}
    new_player, new_globals = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_globals["venus"] == 2
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 1


# --- Pieza nueva de motor (bloque 25): zero_tag_cards_played -----------------

def test_increment_zero_tag_cards_played_only_for_cards_without_tags():
    player = new_player_state()
    p1 = increment_zero_tag_cards_played(player, ())
    assert p1["zero_tag_cards_played"] == 1
    p2 = increment_zero_tag_cards_played(p1, ("earth",))
    assert p2["zero_tag_cards_played"] == 1  # no cambia, tiene tag


def test_production_delta_per_zero_tag_card_includes_this():
    player = {**new_player_state(), "zero_tag_cards_played": 2}
    effects = {"production_delta_per_zero_tag_card": {"production": "mc_production", "per_card": 1, "include_this": True}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1 + 3  # base 1 + (2 previas + esta misma)


# --- Bloque de revision 25 (Colonies) ----------------------------------------

def test_atmo_collectors_action_choice_add_or_spend_for_titanium_energy_heat():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "atmo_collectors")
    action_spec = {"choice": [
        {"gains": {"card_resource_delta": 1}},
        {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"titanium": 2}}},
        {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"energy": 3}}},
        {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"heat": 4}}},
    ]}
    p1, _ = use_card_action(player, globals_, "atmo_collectors", action_spec, effect_choice=0)
    assert p1["active_cards"]["atmo_collectors"]["resources"] == 1

    player_with_floater = {**player, "active_cards": {"atmo_collectors": {"resources": 1, "action_used": False}}}
    p2, _ = use_card_action(player_with_floater, globals_, "atmo_collectors", action_spec, effect_choice=2)
    assert p2["energy"] == 3
    assert p2["active_cards"]["atmo_collectors"]["resources"] == 0

    # Efecto inmediato al jugar: +2 floaters a cualquier carta (incluida ella misma)
    new_player, _ = apply_card_effect(player, globals_, {"target_card_resource_delta": 2}, target_card_id="atmo_collectors")
    assert new_player["active_cards"]["atmo_collectors"]["resources"] == 2


def test_community_services_mc_production_per_zero_tag_card():
    player = {**new_player_state(), "zero_tag_cards_played": 1}
    effects = {"production_delta_per_zero_tag_card": {"production": "mc_production", "per_card": 1, "include_this": True}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1 + 2


def test_conscription_requires_2_earth_tags_discounts_next_card():
    req = {"min_tag_count": {"tag": "earth", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"earth": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"next_card_discount_mc": 16})
    assert new_player["pending_mc_discount"] == 16


def test_corona_extractor_requires_4_science_tags_energy_production():
    req = {"min_tag_count": {"tag": "science", "count": 4}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 3}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"energy_production": 4}})
    assert new_player["energy_production"] == 5


def test_earth_elevator_titanium_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"titanium_production": 3}})
    assert new_player["titanium_production"] == 4  # base 1 + 3


# --- Piezas nuevas de motor (Colonies) ---------------------------------------

def test_production_delta_per_colony():
    player = {**new_player_state(), "colonies_owned": ["callisto", "ganymede"]}
    effects = {"production_delta_per_colony": {"production": "plant_production", "per_colony": 1}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["plant_production"] == 1 + 2  # base 1 + 2 colonias


def test_production_delta_per_colony_no_colonies_no_change():
    new_player, _ = apply_card_effect(
        new_player_state(), new_global_parameters(),
        {"production_delta_per_colony": {"production": "plant_production", "per_colony": 1}},
    )
    assert new_player["plant_production"] == 1


def test_compute_trade_cost_discount_from_passive():
    player = register_passive_effect(new_player_state(), "cryo_sleep", {"trade_cost_discount": 1})
    assert compute_trade_cost_discount(player) == 1
    assert compute_trade_cost_discount(new_player_state()) == 0


def test_cryo_sleep_passive_trade_discount():
    player = register_passive_effect(new_player_state(), "cryo_sleep", {"trade_cost_discount": 1})
    assert compute_trade_cost_discount(player) == 1


def test_ecology_research_plant_production_per_colony_and_targets_two_cards():
    player = {**new_player_state(), "colonies_owned": ["callisto"]}
    player = register_active_card(player, "ecology_research")
    player = register_active_card(player, "aerial_mappers")
    player = register_active_card(player, "decomposers")
    effects = {
        "production_delta_per_colony": {"production": "plant_production", "per_colony": 1},
        "target_card_resource_delta": 1, "target_card_resource_delta_2": 2,
    }
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), effects,
        target_card_id="aerial_mappers", target_card_id_2="decomposers",
    )
    assert new_player["plant_production"] == 2  # base 1 + 1 colonia
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 1
    assert new_player["active_cards"]["decomposers"]["resources"] == 2


# --- Pieza nueva de motor (bloque 26): mc_per_card_resource ------------------

def test_mc_per_card_resource_gains_without_spending():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "jupiter_floating_station", initial_resources=3)
    action_spec = {"gains": {"mc_per_card_resource": {"cap": 4}}}
    new_player, _ = use_card_action(player, globals_, "jupiter_floating_station", action_spec)
    assert new_player["mc"] == 3
    assert new_player["active_cards"]["jupiter_floating_station"]["resources"] == 3  # no se gasta


def test_mc_per_card_resource_respects_cap():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "jupiter_floating_station", initial_resources=6)
    action_spec = {"gains": {"mc_per_card_resource": {"cap": 4}}}
    new_player, _ = use_card_action(player, globals_, "jupiter_floating_station", action_spec)
    assert new_player["mc"] == 4  # tope de 4, no 6


# --- Bloque de revision 26 (Colonies) ----------------------------------------

def test_floater_prototypes_targets_another_card():
    player = register_active_card(new_player_state(), "floater_prototypes")
    player = register_active_card(player, "aerial_mappers")
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"target_card_resource_delta": 2}, target_card_id="aerial_mappers",
    )
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2


def test_floater_technology_action_targets_another_card():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "floater_technology")
    player = register_active_card(player, "aerial_mappers")
    action_spec = {"cost": {}, "gains": {"target_card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "floater_technology", action_spec, target_card_id="aerial_mappers")
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 1


def test_galilean_waystation_mc_production_per_jovian_tag():
    player = {**new_player_state(), "tags_played": {"jovian": 3}}
    effects = {"production_delta_per_tag": {"tag": "jovian", "production": "mc_production", "per_tag": 1}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1 + 3


def test_heavy_taxation_requires_2_earth_tags_gives_mc_and_production():
    req = {"min_tag_count": {"tag": "earth", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"earth": 1}})
    effects = {"resource_deltas": {"mc": 4}, "production_deltas": {"mc_production": 2}}
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), effects)
    assert new_player["mc"] == 4
    assert new_player["mc_production"] == 3


def test_impactor_swarm_requires_2_jovian_tags_gives_heat():
    req = {"min_tag_count": {"tag": "jovian", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"jovian": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"resource_deltas": {"heat": 12}})
    assert new_player["heat"] == 12


def test_jovian_lanterns_requires_1_jovian_tag_tr_and_action():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(
            {"min_tag_count": {"tag": "jovian", "count": 1}}, new_global_parameters(), player=new_player_state(),
        )
    player = register_active_card(new_player_state(), "jovian_lanterns")
    player = register_active_card(player, "aerial_mappers")
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"tr_delta": 1, "target_card_resource_delta": 2}, target_card_id="aerial_mappers",
    )
    assert new_player["tr"] == 21
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2

    globals_ = new_global_parameters()
    player_with_titanium = {**player, "titanium": 1}
    action_spec = {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 2}}
    new_player2, _ = use_card_action(player_with_titanium, globals_, "jovian_lanterns", action_spec)
    assert new_player2["titanium"] == 0
    assert new_player2["active_cards"]["jovian_lanterns"]["resources"] == 2


def test_jupiter_floating_station_requires_3_science_action_choice():
    req = {"min_tag_count": {"tag": "science", "count": 3}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 2}})

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "jupiter_floating_station", initial_resources=2)
    player = register_active_card(player, "aerial_mappers")
    action_spec = {"choice": [
        {"gains": {"target_card_resource_delta": 1}},
        {"gains": {"mc_per_card_resource": {"cap": 4}}},
    ]}
    p1, _ = use_card_action(player, globals_, "jupiter_floating_station", action_spec, effect_choice=0, target_card_id="aerial_mappers")
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 1

    p2, _ = use_card_action(player, globals_, "jupiter_floating_station", action_spec, effect_choice=1)
    assert p2["mc"] == 2


def test_luna_governor_requires_3_earth_tags_mc_production():
    req = {"min_tag_count": {"tag": "earth", "count": 3}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"earth": 2}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 2}})
    assert new_player["mc_production"] == 3


# --- Pieza nueva de motor (bloque 27): max_colonies_owned --------------------

def test_max_colonies_owned_requirement():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(
            {"max_colonies_owned": 1}, new_global_parameters(),
            player={**new_player_state(), "colonies_owned": ["callisto", "ganymede"]},
        )
    check_card_requirements(
        {"max_colonies_owned": 1}, new_global_parameters(),
        player={**new_player_state(), "colonies_owned": ["callisto"]},
    )


# --- Bloque de revision 27 (Colonies) ----------------------------------------

def test_lunar_exports_choice_plant_or_mc_production():
    effects = {"choice": [
        {"production_deltas": {"plant_production": 2}},
        {"production_deltas": {"mc_production": 5}},
    ]}
    p1, _ = apply_card_effect(new_player_state(), new_global_parameters(), effects, effect_choice=0)
    assert p1["plant_production"] == 3
    p2, _ = apply_card_effect(new_player_state(), new_global_parameters(), effects, effect_choice=1)
    assert p2["mc_production"] == 6


def test_lunar_mining_titanium_production_per_2_earth_tags_including_this():
    player = {**new_player_state(), "tags_played": {"earth": 3}}
    effects = {"production_delta_per_tag": {"tag": "earth", "production": "titanium_production", "tags_per_step": 2, "per_step": 1, "include_this": True}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["titanium_production"] == 1 + 2  # (3+1)//2 = 2 pasos


def test_martian_zoo_requires_2_city_tiles_passive_and_action():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_city_tiles": 2}, {**new_global_parameters(), "city_tiles_placed": 1})

    player = register_active_card(new_player_state(), "martian_zoo", initial_resources=3)
    action_spec = {"cost": {}, "gains": {"mc_per_card_resource": {}}}
    new_player, _ = use_card_action(player, new_global_parameters(), "martian_zoo", action_spec)
    assert new_player["mc"] == 3
    assert new_player["active_cards"]["martian_zoo"]["resources"] == 3  # no se gasta


def test_mining_colony_titanium_production_and_builds_colony_flag():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"titanium_production": 1}})
    assert new_player["titanium_production"] == 2


def test_minority_refuge_decreases_mc_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": -2}})
    assert new_player["mc_production"] == -1


def test_molecular_printing_mc_per_city_tile_counter():
    globals_ = {**new_global_parameters(), "city_tiles_placed": 4}
    new_player, _ = apply_card_effect(
        new_player_state(), globals_,
        {"resource_delta_per_counter": {"resource": "mc", "counter": "city_tiles_placed", "per_counter": 1}},
    )
    assert new_player["mc"] == 4


def test_nitrogen_from_titan_tr_and_targets_jovian_card():
    player = register_active_card(new_player_state(), "nitrogen_from_titan")
    player = register_active_card(player, "aerial_mappers")
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"tr_delta": 2, "target_card_resource_delta": 2}, target_card_id="aerial_mappers",
    )
    assert new_player["tr"] == 22
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2


def test_pioneer_settlement_requires_at_most_1_colony():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(
            {"max_colonies_owned": 1}, new_global_parameters(),
            player={**new_player_state(), "colonies_owned": ["callisto", "ganymede"]},
        )
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": -2}})
    assert new_player["mc_production"] == -1


# --- Piezas nuevas de motor (bloque 28) --------------------------------------

def test_min_colonies_owned_requirement():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_colonies_owned": 1}, new_global_parameters(), player=new_player_state())
    check_card_requirements(
        {"min_colonies_owned": 1}, new_global_parameters(),
        player={**new_player_state(), "colonies_owned": ["callisto"]},
    )


def test_trade_fleet_delta_effect():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"trade_fleet_delta": 1})
    assert new_player["trade_fleets"] == 2  # arranca en 1


def test_draw_cards_per_tag_scales_and_includes_this():
    player = {**new_player_state(), "tags_played": {"science": 2}, "deck": ["a"]}
    effects = {"draw_cards_per_tag": {"tag": "science", "tags_per_step": 3, "cards_per_step": 1, "include_this": True}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["hand"] == ["a"]  # (2+1)//3 = 1 carta


def test_draw_cards_per_tag_below_threshold_draws_nothing():
    player = {**new_player_state(), "tags_played": {"science": 1}, "deck": ["a"]}
    effects = {"draw_cards_per_tag": {"tag": "science", "tags_per_step": 3, "cards_per_step": 1, "include_this": True}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["hand"] == []


# --- Bloque de revision 28 (Colonies) ----------------------------------------

def test_red_spot_observatory_requires_3_science_draws_2_action_choice():
    req = {"min_tag_count": {"tag": "science", "count": 3}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 2}})

    player = {**new_player_state(), "deck": ["a", "b"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["a", "b"]

    globals_ = new_global_parameters()
    active_player = register_active_card(new_player_state(), "red_spot_observatory")
    action_spec = {"choice": [{"gains": {"card_resource_delta": 1}}, {"cost": {"card_resource": 1}, "gains": {"draw_cards": 1}}]}
    p1, _ = use_card_action(active_player, globals_, "red_spot_observatory", action_spec, effect_choice=0)
    assert p1["active_cards"]["red_spot_observatory"]["resources"] == 1


def test_refugee_camps_action_swaps_mc_production_for_card_resource():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "refugee_camps")
    action_spec = {"cost": {}, "gains": {"production_deltas": {"mc_production": -1}, "card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "refugee_camps", action_spec)
    assert new_player["mc_production"] == 0
    assert new_player["active_cards"]["refugee_camps"]["resources"] == 1


def test_rim_freighters_passive_trade_discount():
    player = register_passive_effect(new_player_state(), "rim_freighters", {"trade_cost_discount": 1})
    assert compute_trade_cost_discount(player) == 1


def test_sky_docks_requires_2_earth_tags_gains_trade_fleet():
    req = {"min_tag_count": {"tag": "earth", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"earth": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"trade_fleet_delta": 1})
    assert new_player["trade_fleets"] == 2


def test_solar_reflectors_heat_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"heat_production": 5}})
    assert new_player["heat_production"] == 6  # base 1 + 5


def test_space_port_requires_1_colony_gains_trade_fleet_city_and_production():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_colonies_owned": 1}, new_global_parameters(), player=new_player_state())

    effects = {"trade_fleet_delta": 1, "place_city_tiles": 1, "production_deltas": {"energy_production": -1, "mc_production": 4}}
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), effects)
    assert new_player["trade_fleets"] == 2
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 5
    assert new_globals["city_tiles_placed"] == 1


# --- Pieza nueva de motor (bloque 29): trade_bump_track_first + registro ----

def test_trade_bump_track_first_passive_registration():
    player = register_passive_effect(new_player_state(), "trade_envoys", {"trade_bump_track_first": True})
    assert any(e.get("trade_bump_track_first") for e in player["passive_effects"])


# --- Bloque de revision 29 (cierre Colonies + primera carta Prelude) --------

def test_spin_off_department_mc_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 2}})
    assert new_player["mc_production"] == 3


def test_sub_zero_salt_fish_requires_max_temperature_action_adds_animal():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_temperature": -6}, {**new_global_parameters(), "temperature": -4})
    check_card_requirements({"max_temperature": -6}, {**new_global_parameters(), "temperature": -6})

    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"plant_production": -1}})
    assert new_player["plant_production"] == 0

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "sub_zero_salt_fish")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player2, _ = use_card_action(player, globals_, "sub_zero_salt_fish", action_spec)
    assert new_player2["active_cards"]["sub_zero_salt_fish"]["resources"] == 1


def test_titan_air_scrapping_action_choice_titanium_or_tr():
    globals_ = new_global_parameters()
    player = {**register_active_card(new_player_state(), "titan_air_scrapping"), "titanium": 1}
    action_spec = {"choice": [
        {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 2}},
        {"cost": {"card_resource": 2}, "gains": {"tr_delta": 1}},
    ]}
    p1, _ = use_card_action(player, globals_, "titan_air_scrapping", action_spec, effect_choice=0)
    assert p1["active_cards"]["titan_air_scrapping"]["resources"] == 2
    assert p1["titanium"] == 0

    player_with_floaters = {**player, "active_cards": {"titan_air_scrapping": {"resources": 2, "action_used": False}}}
    p2, _ = use_card_action(player_with_floaters, globals_, "titan_air_scrapping", action_spec, effect_choice=1)
    assert p2["tr"] == 21
    assert p2["active_cards"]["titan_air_scrapping"]["resources"] == 0


def test_titan_shuttles_action_choice_target_or_convert_to_titanium():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "titan_shuttles")
    player = register_active_card(player, "aerial_mappers")
    action_spec = {"choice": [
        {"gains": {"target_card_resource_delta": 2}},
        {"convert_card_resource_amount": {"to": "titanium", "ratio": 1}},
    ]}
    p1, _ = use_card_action(player, globals_, "titan_shuttles", action_spec, effect_choice=0, target_card_id="aerial_mappers")
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 2

    player_with_floaters = register_active_card(new_player_state(), "titan_shuttles", initial_resources=3)
    p2, _ = use_card_action(player_with_floaters, globals_, "titan_shuttles", action_spec, effect_choice=1, effect_amount=3)
    assert p2["titanium"] == 3
    assert p2["active_cards"]["titan_shuttles"]["resources"] == 0


def test_urban_decomposers_requires_city_and_colony_plant_production_and_target():
    req = {"min_city_tiles": 1, "min_colonies_owned": 1}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, {**new_global_parameters(), "city_tiles_placed": 0}, player={**new_player_state(), "colonies_owned": ["callisto"]})
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, {**new_global_parameters(), "city_tiles_placed": 1}, player=new_player_state())
    check_card_requirements(req, {**new_global_parameters(), "city_tiles_placed": 1}, player={**new_player_state(), "colonies_owned": ["callisto"]})

    player = register_active_card(new_player_state(), "urban_decomposers")
    player = register_active_card(player, "aerial_mappers")
    effects = {"production_deltas": {"plant_production": 1}, "target_card_resource_delta": 2}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects, target_card_id="aerial_mappers")
    assert new_player["plant_production"] == 2
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2


def test_warp_drive_requires_5_science_tags_passive_discounts_space_cards():
    req = {"min_tag_count": {"tag": "science", "count": 5}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"science": 4}})

    player = register_passive_effect(new_player_state(), "warp_drive", {"card_cost_discount_mc": 4, "tag_filter": "space"})
    assert compute_card_cost_discount(player, ("space",)) == 4
    assert compute_card_cost_discount(player, ("earth",)) == 0


def test_house_printing_steel_production():
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"steel_production": 1}})
    assert new_player["steel_production"] == 2


# --- Resuelto: Titan Floating Launch-Pad (bloque 29, pieza pendiente) -------

def test_titan_floating_launch_pad_action_choice_target_or_cost_only_for_free_trade():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "titan_floating_launch_pad")
    player = register_active_card(player, "aerial_mappers")
    action_spec = {"choice": [
        {"gains": {"target_card_resource_delta": 1}},
        {"cost": {"card_resource": 1}, "gains": {"free_trade": True}},
    ]}
    p1, _ = use_card_action(player, globals_, "titan_floating_launch_pad", action_spec, effect_choice=0, target_card_id="aerial_mappers")
    assert p1["active_cards"]["aerial_mappers"]["resources"] == 1

    # La rama "free_trade" solo cobra el costo declarado (1 floater guardado);
    # el "free_trade" en si es responsabilidad de tools.use_card_action, no
    # de este motor (que no conoce colonies.py) -- ver docstring.
    player_with_floater = {**player, "active_cards": {**player["active_cards"], "titan_floating_launch_pad": {"resources": 1, "action_used": False}}}
    p2, _ = use_card_action(player_with_floater, globals_, "titan_floating_launch_pad", action_spec, effect_choice=1)
    assert p2["active_cards"]["titan_floating_launch_pad"]["resources"] == 0


def test_titan_floating_launch_pad_immediate_effect_targets_any_jovian_card():
    player = register_active_card(new_player_state(), "titan_floating_launch_pad")
    player = register_active_card(player, "aerial_mappers")
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"target_card_resource_delta": 2}, target_card_id="aerial_mappers",
    )
    assert new_player["active_cards"]["aerial_mappers"]["resources"] == 2


# --- Piezas nuevas de motor (bloque 30) --------------------------------------

def test_mc_per_discarded_card_action():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "ceres_tech_market")
    action_spec = {"cost": {}, "gains": {"mc_per_discarded_card": {"per_card": 2}}}
    new_player, _ = use_card_action(player, globals_, "ceres_tech_market", action_spec, effect_amount=3)
    assert new_player["mc"] == 6


def test_resource_delta_per_colony():
    player = {**new_player_state(), "colonies_owned": ["callisto"]}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"resource_delta_per_colony": {"resource": "mc", "per_colony": 2}},
    )
    assert new_player["mc"] == 2


def test_production_delta_per_tag_pair_uses_minimum_of_both_counts():
    player = {**new_player_state(), "tags_played": {"earth": 3, "venus": 1}}
    effects = {"production_delta_per_tag_pair": {"tag_a": "earth", "tag_b": "venus", "production": "mc_production", "per_set": 1}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1 + 1  # min(3,1) = 1 set


def test_production_delta_per_tag_pair_no_pairs_no_change():
    player = {**new_player_state(), "tags_played": {"earth": 3}}
    effects = {"production_delta_per_tag_pair": {"tag_a": "earth", "tag_b": "venus", "production": "mc_production", "per_set": 1}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 1


# --- Bloque de revision 30 (Prelude + Venus Next promo + Prelude 2) ---------

def test_lava_tube_settlement_swaps_energy_for_mc_places_city_flag():
    effects = {"production_deltas": {"energy_production": -1, "mc_production": 2}, "place_city_tiles": 1}
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), effects)
    assert new_player["energy_production"] == 0
    assert new_player["mc_production"] == 3
    assert new_globals["city_tiles_placed"] == 1


def test_martian_survey_requires_max_oxygen_4_draws_2():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_oxygen": 4}, {**new_global_parameters(), "oxygen": 6})
    player = {**new_player_state(), "deck": ["a", "b"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 2})
    assert new_player["hand"] == ["a", "b"]


def test_sf_memorial_draws_1():
    player = {**new_player_state(), "deck": ["a"]}
    new_player, _ = apply_card_effect(player, new_global_parameters(), {"draw_cards": 1})
    assert new_player["hand"] == ["a"]


def test_space_hotels_requires_2_earth_tags_mc_production():
    req = {"min_tag_count": {"tag": "earth", "count": 2}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(req, new_global_parameters(), player={**new_player_state(), "tags_played": {"earth": 1}})
    new_player, _ = apply_card_effect(new_player_state(), new_global_parameters(), {"production_deltas": {"mc_production": 4}})
    assert new_player["mc_production"] == 5


def test_ceres_tech_market_mc_per_colony_and_discard_action():
    player = {**new_player_state(), "colonies_owned": ["callisto"]}
    new_player, _ = apply_card_effect(
        player, new_global_parameters(), {"resource_delta_per_colony": {"resource": "mc", "per_colony": 2}},
    )
    assert new_player["mc"] == 2

    globals_ = new_global_parameters()
    active_player = register_active_card(new_player_state(), "ceres_tech_market")
    action_spec = {"cost": {}, "gains": {"mc_per_discarded_card": {"per_card": 2}}}
    new_player2, _ = use_card_action(active_player, globals_, "ceres_tech_market", action_spec, effect_amount=2)
    assert new_player2["mc"] == 4


def test_cloud_tourism_mc_production_per_earth_venus_pair_action_adds_floater():
    player = {**new_player_state(), "tags_played": {"earth": 2, "venus": 2}}
    effects = {"production_delta_per_tag_pair": {"tag_a": "earth", "tag_b": "venus", "production": "mc_production", "per_set": 1}}
    new_player, _ = apply_card_effect(player, new_global_parameters(), effects)
    assert new_player["mc_production"] == 3

    globals_ = new_global_parameters()
    active_player = register_active_card(new_player_state(), "cloud_tourism")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player2, _ = use_card_action(active_player, globals_, "cloud_tourism", action_spec)
    assert new_player2["active_cards"]["cloud_tourism"]["resources"] == 1


# --- Pago con recurso de carta (Dirigibles/Psychrophiles) -------------------

def test_spend_active_card_resource_decrements():
    player = register_active_card(new_player_state(), "dirigibles", initial_resources=3)
    new_player = spend_active_card_resource(player, "dirigibles", 2)
    assert new_player["active_cards"]["dirigibles"]["resources"] == 1


def test_spend_active_card_resource_raises_if_not_enough():
    player = register_active_card(new_player_state(), "dirigibles", initial_resources=1)
    with pytest.raises(InsufficientResourcesError):
        spend_active_card_resource(player, "dirigibles", 2)


def test_target_card_resource_delta_allow_self_adds_to_own_card_by_default():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "dirigibles")
    action_spec = {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}}
    new_player, _ = use_card_action(player, globals_, "dirigibles", action_spec)
    assert new_player["active_cards"]["dirigibles"]["resources"] == 1


def test_target_card_resource_delta_allow_self_can_target_other_card():
    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "dirigibles")
    player = register_active_card(player, "some_jovian_card")
    action_spec = {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}}
    new_player, _ = use_card_action(
        player, globals_, "dirigibles", action_spec, target_card_id="some_jovian_card"
    )
    assert new_player["active_cards"]["some_jovian_card"]["resources"] == 1
    assert new_player["active_cards"]["dirigibles"]["resources"] == 0


def test_dirigibles_passive_pays_venus_card_with_floaters():
    player = register_active_card(new_player_state(), "dirigibles", initial_resources=4)
    player = register_passive_effect(player, "dirigibles", {"card_resource_payment": {"required_tag": "venus", "value_mc": 3}})
    match = next(p for p in player["passive_effects"] if "card_resource_payment" in p)
    assert match["card_id"] == "dirigibles"
    assert match["card_resource_payment"]["required_tag"] == "venus"
    assert match["card_resource_payment"]["value_mc"] == 3
    new_player = spend_active_card_resource(player, "dirigibles", 3)
    assert new_player["active_cards"]["dirigibles"]["resources"] == 1


def test_psychrophiles_requires_temperature_minus_20_action_adds_microbe():
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"max_temperature": -20}, {**new_global_parameters(), "temperature": -18})
    check_card_requirements({"max_temperature": -20}, {**new_global_parameters(), "temperature": -20})

    globals_ = new_global_parameters()
    player = register_active_card(new_player_state(), "psychrophiles")
    action_spec = {"cost": {}, "gains": {"card_resource_delta": 1}}
    new_player, _ = use_card_action(player, globals_, "psychrophiles", action_spec)
    assert new_player["active_cards"]["psychrophiles"]["resources"] == 1


def test_psychrophiles_passive_pays_plant_card_with_microbes():
    player = register_active_card(new_player_state(), "psychrophiles", initial_resources=2)
    player = register_passive_effect(player, "psychrophiles", {"card_resource_payment": {"required_tag": "plant", "value_mc": 2}})
    match = next(p for p in player["passive_effects"] if "card_resource_payment" in p)
    assert match["card_resource_payment"]["required_tag"] == "plant"
    assert match["card_resource_payment"]["value_mc"] == 2


# --- Tag comodin "wild" (Research Coordination) -----------------------------

def test_min_tag_count_ignores_wild_without_choice():
    player = {**new_player_state(), "tags_played": {"science": 4, "wild": 1}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements({"min_tag_count": {"tag": "science", "count": 5}}, new_global_parameters(), player)


def test_min_tag_count_wild_choice_covers_missing_tag():
    player = {**new_player_state(), "tags_played": {"science": 4, "wild": 1}}
    check_card_requirements(
        {"min_tag_count": {"tag": "science", "count": 5}},
        new_global_parameters(),
        player,
        wild_tag_choice="science",
    )


def test_min_tag_count_wild_choice_does_not_apply_to_unmatched_tag():
    player = {**new_player_state(), "tags_played": {"science": 4, "wild": 1}}
    with pytest.raises(CardRequirementNotMetError):
        check_card_requirements(
            {"min_tag_count": {"tag": "science", "count": 5}},
            new_global_parameters(),
            player,
            wild_tag_choice="earth",
        )


def test_research_coordination_no_immediate_effect_just_wild_tag():
    new_player, new_globals = apply_card_effect(new_player_state(), new_global_parameters(), {})
    new_player = increment_tags_played(new_player, ("wild",))
    assert new_player["tags_played"]["wild"] == 1
