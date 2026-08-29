"""
Motor de reglas determinista de Terraforming Mars.

Este modulo NO conoce LangGraph, FastAPI ni Supabase -- son funciones puras
de Python que reciben estado, devuelven estado nuevo, y son 100% testeables
sin mockear nada. Es exactamente lo que el nodo LLM (agent/graph.py) llama
via tools.py cuando necesita "hacer matematica": el LLM nunca calcula estos
numeros, solo decide que funcion llamar y con que argumentos.

Fuente de las reglas: reglamento oficial de Terraforming Mars (Fryxelius /
Stronghold Games). Los numeros de aqui abajo estan verificados contra el
rulebook -- si haces cambios, revalida contra tu copia fisica del juego o
una fuente oficial antes de tocar las constantes.

NOTA IMPORTANTE sobre el catalogo de cartas: este motor implementa la
mecanica NUCLEAR del juego (parametros globales, TR, proyectos estandar,
fase de produccion, conversion de recursos) con numeros verificados. Las
~200 cartas de proyecto individuales (costo, tags, requisitos, efecto) NO
estan precargadas aqui a proposito -- cada una tendria que verificarse
contra la fuente antes de confiar en ella para no romper el objetivo de
"100% de precision" del PRD. Ver seccion "Catalogo de cartas" en CLAUDE.md.
"""
from typing import TypedDict


# ---------------------------------------------------------------------------
# Constantes del reglamento (verificadas)
# ---------------------------------------------------------------------------

TR_START = 20

# Parametros globales: (minimo, maximo, tamano de paso)
TEMPERATURE_MIN = -30
TEMPERATURE_MAX = 8
TEMPERATURE_STEP = 2  # cada paso son 2 grados

OXYGEN_MIN = 0
OXYGEN_MAX = 14
OXYGEN_STEP = 1

OCEANS_MAX = 9  # cantidad maxima de tiles de oceano colocables

# Valor de conversion de recursos (solo para pagar cartas con el tag correspondiente)
STEEL_VALUE_MC = 2       # 1 acero = 2 MC, solo para cartas con tag "building"
TITANIUM_VALUE_MC = 3    # 1 titanio = 3 MC, solo para cartas con tag "space"

# Acciones de conversion disponibles en el tablero de cada jugador
PLANTS_PER_GREENERY = 8   # 8 plantas -> colocar 1 tile de greenery (sube oxigeno)
HEAT_PER_TEMPERATURE_STEP = 8  # 8 calor -> subir temperatura 1 paso

# Produccion de MC es la unica que puede ser negativa, con piso en -5
MC_PRODUCTION_FLOOR = -5

# Costos de los 6 proyectos estandar (siempre disponibles, en MC)
STANDARD_PROJECT_POWER_PLANT_COST = 11   # +1 produccion de energia
STANDARD_PROJECT_ASTEROID_COST = 14      # +1 paso de temperatura (+1 TR)
STANDARD_PROJECT_AQUIFER_COST = 18       # coloca tile de oceano (+1 TR)
STANDARD_PROJECT_GREENERY_COST = 23      # coloca tile de greenery, +1 paso de oxigeno (+1 TR)
STANDARD_PROJECT_CITY_COST = 25          # coloca tile de ciudad, +1 produccion de MC


# ---------------------------------------------------------------------------
# Tipos de estado
# ---------------------------------------------------------------------------

class PlayerState(TypedDict):
    """Stock y produccion de recursos de un jugador, mas su Terraform Rating."""
    tr: int
    mc: int
    steel: int
    titanium: int
    plants: int
    energy: int
    heat: int
    mc_production: int
    steel_production: int
    titanium_production: int
    plant_production: int
    energy_production: int
    heat_production: int


class GlobalParameters(TypedDict):
    """Estado compartido del tablero central -- no pertenece a un jugador."""
    temperature: int
    oxygen: int
    oceans_placed: int


def new_player_state() -> PlayerState:
    """Estado inicial de un jugador: TR 20, produccion 1 en cada recurso, stock 0."""
    return PlayerState(
        tr=TR_START,
        mc=0, steel=0, titanium=0, plants=0, energy=0, heat=0,
        mc_production=1, steel_production=1, titanium_production=1,
        plant_production=1, energy_production=1, heat_production=1,
    )


def new_global_parameters() -> GlobalParameters:
    return GlobalParameters(temperature=TEMPERATURE_MIN, oxygen=OXYGEN_MIN, oceans_placed=0)


# ---------------------------------------------------------------------------
# Errores de dominio
# ---------------------------------------------------------------------------

class InsufficientResourcesError(Exception):
    """El jugador no tiene suficiente MC/recurso para pagar la accion."""


class GlobalParameterMaxedError(Exception):
    """El parametro global ya esta en su tope; la accion no es legal."""


class CardEffectError(Exception):
    """El efecto de la carta no se pudo aplicar con los parametros dados."""


# ---------------------------------------------------------------------------
# Parametros globales y Terraform Rating
# ---------------------------------------------------------------------------

def raise_temperature(player: PlayerState, globals_: GlobalParameters, steps: int = 1) -> tuple[PlayerState, GlobalParameters]:
    """Sube la temperatura `steps` pasos (2 grados cada uno). +1 TR por paso aplicado."""
    if globals_["temperature"] >= TEMPERATURE_MAX:
        raise GlobalParameterMaxedError("La temperatura ya esta en su maximo (+8 C)")

    max_possible_steps = (TEMPERATURE_MAX - globals_["temperature"]) // TEMPERATURE_STEP
    applied_steps = min(steps, max_possible_steps)

    new_globals = {**globals_, "temperature": globals_["temperature"] + applied_steps * TEMPERATURE_STEP}
    new_player = {**player, "tr": player["tr"] + applied_steps}
    return new_player, new_globals


def raise_oxygen(player: PlayerState, globals_: GlobalParameters, steps: int = 1) -> tuple[PlayerState, GlobalParameters]:
    """Sube el oxigeno `steps` pasos (1% cada uno). +1 TR por paso aplicado."""
    if globals_["oxygen"] >= OXYGEN_MAX:
        raise GlobalParameterMaxedError("El oxigeno ya esta en su maximo (14%)")

    max_possible_steps = min(steps, OXYGEN_MAX - globals_["oxygen"])

    new_globals = {**globals_, "oxygen": globals_["oxygen"] + max_possible_steps}
    new_player = {**player, "tr": player["tr"] + max_possible_steps}
    return new_player, new_globals


def place_ocean(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Coloca 1 tile de oceano (de los 9 disponibles en total). +1 TR."""
    if globals_["oceans_placed"] >= OCEANS_MAX:
        raise GlobalParameterMaxedError("Ya se colocaron los 9 tiles de oceano")

    new_globals = {**globals_, "oceans_placed": globals_["oceans_placed"] + 1}
    new_player = {**player, "tr": player["tr"] + 1}
    return new_player, new_globals


# ---------------------------------------------------------------------------
# Los 6 proyectos estandar
# ---------------------------------------------------------------------------

def standard_project_sell_patents(player: PlayerState, num_cards: int) -> PlayerState:
    """Descarta `num_cards` cartas de la mano por 1 MC cada una. Sin costo."""
    if num_cards < 0:
        raise ValueError("num_cards no puede ser negativo")
    return {**player, "mc": player["mc"] + num_cards}


def standard_project_power_plant(player: PlayerState) -> PlayerState:
    """Paga 11 MC, +1 produccion de energia."""
    if player["mc"] < STANDARD_PROJECT_POWER_PLANT_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_POWER_PLANT_COST} MC, hay {player['mc']}"
        )
    return {
        **player,
        "mc": player["mc"] - STANDARD_PROJECT_POWER_PLANT_COST,
        "energy_production": player["energy_production"] + 1,
    }


def standard_project_asteroid(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Paga 14 MC, sube temperatura 1 paso (+1 TR)."""
    if player["mc"] < STANDARD_PROJECT_ASTEROID_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_ASTEROID_COST} MC, hay {player['mc']}"
        )
    paid_player = {**player, "mc": player["mc"] - STANDARD_PROJECT_ASTEROID_COST}
    return raise_temperature(paid_player, globals_, steps=1)


def standard_project_aquifer(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Paga 18 MC, coloca tile de oceano (+1 TR). Bonus de colocacion fuera de alcance."""
    if player["mc"] < STANDARD_PROJECT_AQUIFER_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_AQUIFER_COST} MC, hay {player['mc']}"
        )
    paid_player = {**player, "mc": player["mc"] - STANDARD_PROJECT_AQUIFER_COST}
    return place_ocean(paid_player, globals_)


def standard_project_greenery(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Paga 23 MC, coloca tile de greenery, sube oxigeno 1 paso (+1 TR)."""
    if player["mc"] < STANDARD_PROJECT_GREENERY_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_GREENERY_COST} MC, hay {player['mc']}"
        )
    paid_player = {**player, "mc": player["mc"] - STANDARD_PROJECT_GREENERY_COST}
    return raise_oxygen(paid_player, globals_, steps=1)


def standard_project_city(player: PlayerState) -> PlayerState:
    """Paga 25 MC, coloca tile de ciudad, +1 produccion de MC."""
    if player["mc"] < STANDARD_PROJECT_CITY_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_CITY_COST} MC, hay {player['mc']}"
        )
    return {
        **player,
        "mc": player["mc"] - STANDARD_PROJECT_CITY_COST,
        "mc_production": player["mc_production"] + 1,
    }


# ---------------------------------------------------------------------------
# Acciones de conversion del tablero de jugador (no son proyectos estandar)
# ---------------------------------------------------------------------------

def convert_plants_to_greenery(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Gasta 8 plantas, coloca tile de greenery, sube oxigeno 1 paso (+1 TR)."""
    if player["plants"] < PLANTS_PER_GREENERY:
        raise InsufficientResourcesError(
            f"Se necesitan {PLANTS_PER_GREENERY} plantas, hay {player['plants']}"
        )
    paid_player = {**player, "plants": player["plants"] - PLANTS_PER_GREENERY}
    return raise_oxygen(paid_player, globals_, steps=1)


def convert_heat_to_temperature(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Gasta 8 calor, sube temperatura 1 paso (+1 TR)."""
    if player["heat"] < HEAT_PER_TEMPERATURE_STEP:
        raise InsufficientResourcesError(
            f"Se necesitan {HEAT_PER_TEMPERATURE_STEP} calor, hay {player['heat']}"
        )
    paid_player = {**player, "heat": player["heat"] - HEAT_PER_TEMPERATURE_STEP}
    return raise_temperature(paid_player, globals_, steps=1)


# ---------------------------------------------------------------------------
# Fase de produccion
# ---------------------------------------------------------------------------

def run_production_phase(player: PlayerState) -> PlayerState:
    """
    Aplica la fase de produccion de una generacion:
      1. Toda la energia en stock se convierte en calor.
      2. Se gana MC = TR + produccion de MC (la produccion de MC nunca es
         menor a -5, pero el resultado de MC en stock si puede terminar
         en 0 como minimo -- no se puede deber dinero).
      3. El resto de recursos suman su produccion correspondiente.
    """
    heat_after_energy_conversion = player["heat"] + player["energy"]

    mc_income = player["tr"] + player["mc_production"]
    new_mc = max(0, player["mc"] + mc_income)

    return {
        **player,
        "mc": new_mc,
        "steel": player["steel"] + player["steel_production"],
        "titanium": player["titanium"] + player["titanium_production"],
        "plants": player["plants"] + player["plant_production"],
        "energy": player["energy_production"],  # arranca de 0 tras la conversion, mas la produccion nueva
        "heat": heat_after_energy_conversion + player["heat_production"],
    }


def adjust_mc_production(player: PlayerState, delta: int) -> PlayerState:
    """Cambia la produccion de MC por `delta`, respetando el piso de -5."""
    new_value = max(MC_PRODUCTION_FLOOR, player["mc_production"] + delta)
    return {**player, "mc_production": new_value}


# ---------------------------------------------------------------------------
# Pago generico de cartas (costo en MC, con posibilidad de pagar parte con
# acero/titanio segun los tags de la carta)
# ---------------------------------------------------------------------------

def calculate_card_payment(
    card_cost: int,
    mc_to_pay: int,
    steel_to_pay: int = 0,
    titanium_to_pay: int = 0,
    card_tags: tuple[str, ...] = (),
) -> int:
    """
    Verifica que una combinacion de MC + acero + titanio cubra el costo de
    una carta, respetando que acero solo vale para cartas con tag "building"
    y titanio solo para cartas con tag "space". No hay reembolso por pagar
    de mas (regla oficial).

    Devuelve el MC sobrante que el jugador de mas (0 si pago exacto o de mas).
    Lanza InsufficientResourcesError si no alcanza para cubrir el costo.
    """
    if steel_to_pay > 0 and "building" not in card_tags:
        raise ValueError("El acero solo puede pagar cartas con tag 'building'")
    if titanium_to_pay > 0 and "space" not in card_tags:
        raise ValueError("El titanio solo puede pagar cartas con tag 'space'")

    total_value = mc_to_pay + steel_to_pay * STEEL_VALUE_MC + titanium_to_pay * TITANIUM_VALUE_MC

    if total_value < card_cost:
        raise InsufficientResourcesError(
            f"El pago cubre {total_value} MC pero la carta cuesta {card_cost} MC"
        )

    return total_value - card_cost


# ---------------------------------------------------------------------------
# Efectos de cartas de proyecto (catalogo cargado a mano, ver
# backend/app/db/seed_cards.sql -- numeros verificados contra el scan oficial
# de cada carta, uno por uno)
# ---------------------------------------------------------------------------

def _apply_production_floor(key: str, value: int) -> int:
    """Todas las producciones tienen piso 0, salvo la de MC (piso -5)."""
    return max(MC_PRODUCTION_FLOOR if key == "mc_production" else 0, value)


def apply_card_effect(
    player: PlayerState,
    effects: dict,
    effect_amount: int | None = None,
    effect_choice: int | None = None,
) -> PlayerState:
    """
    Aplica el efecto inmediato de una carta ya pagada, segun el jsonb
    `effects` de la tabla `cards`. Vocabulario soportado por las cartas
    cargadas hasta ahora (ver seed_cards.sql):

      - "mc_production_delta": entero fijo que se suma a la produccion de MC
        (forma antigua, mantenida por compatibilidad -- ej. Sponsors: +2).
      - "mc_delta": entero fijo que se suma al stock de MC (forma antigua,
        mantenida por compatibilidad -- ej. Investment Loan: +10).
      - "production_deltas": {"<recurso>_production": delta, ...} -- forma
        generica para cambiar una o mas producciones a la vez (ej. Nuclear
        Power: -2 produccion MC, +3 produccion energia).
      - "resource_deltas": {"<recurso>": delta, ...} -- forma generica para
        cambiar stock de uno o mas recursos (ej. Solar Wind Power: +2 titanio).
      - "convert_production": {"from": "<recurso>_production", "to":
        "<recurso>_production"} convierte `effect_amount` (X, elegido por el
        jugador) pasos de produccion de un recurso a otro, limitado al stock
        de produccion disponible (ej. Insulation: -X calor, +X MC).
      - "choice": lista de sub-effects (cualquiera de los de arriba); el
        jugador elige uno via `effect_choice` (indice 0-based) (ej.
        Artificial Photosynthesis: +1 produccion de plantas O +2 de energia).

    effects == {} no hace nada (carta sin efecto modelado todavia).
    """
    if "choice" in effects:
        options = effects["choice"]
        if effect_choice is None or not (0 <= effect_choice < len(options)):
            raise CardEffectError(
                f"Esta carta requiere effect_choice entre 0 y {len(options) - 1}"
            )
        return apply_card_effect(player, options[effect_choice], effect_amount)

    new_player: dict = dict(player)

    if "mc_production_delta" in effects:
        new_player["mc_production"] = _apply_production_floor(
            "mc_production", new_player["mc_production"] + effects["mc_production_delta"]
        )

    if "mc_delta" in effects:
        new_player["mc"] = max(0, new_player["mc"] + effects["mc_delta"])

    if "production_deltas" in effects:
        for key, delta in effects["production_deltas"].items():
            new_player[key] = _apply_production_floor(key, new_player[key] + delta)

    if "resource_deltas" in effects:
        for key, delta in effects["resource_deltas"].items():
            new_player[key] = max(0, new_player[key] + delta)

    if "convert_production" in effects:
        from_key = effects["convert_production"]["from"]
        to_key = effects["convert_production"]["to"]

        if effect_amount is None or effect_amount < 0:
            raise CardEffectError("Esta carta requiere effect_amount (X) >= 0")
        if new_player[from_key] < effect_amount:
            raise InsufficientResourcesError(
                f"No hay suficiente {from_key} ({new_player[from_key]}) para convertir {effect_amount} pasos"
            )

        new_player[from_key] = _apply_production_floor(from_key, new_player[from_key] - effect_amount)
        new_player[to_key] = _apply_production_floor(to_key, new_player[to_key] + effect_amount)

    return PlayerState(**new_player)  # type: ignore[typeddict-item]
