"""
Tests del motor de reglas puro. Cada numero aqui esta verificado contra el
reglamento oficial de Terraforming Mars -- este archivo es la evidencia del
criterio de exito del PRD ("100% de precision en los calculos").
"""
import pytest

from app.agent.rules_engine import (
    InsufficientResourcesError,
    GlobalParameterMaxedError,
    new_player_state,
    new_global_parameters,
    raise_temperature,
    raise_oxygen,
    place_ocean,
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
    player = standard_project_city(player)
    assert player["mc"] == 0
    assert player["mc_production"] == 2  # 1 base + 1


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
