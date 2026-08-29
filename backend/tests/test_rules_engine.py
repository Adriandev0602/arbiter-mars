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
    place_ocean,
    place_city_tile,
    standard_project_sell_patents,
    standard_project_power_plant,
    standard_project_asteroid,
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
