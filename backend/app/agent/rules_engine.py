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
import random
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

# Fase de investigacion: costo estandar por carta comprada del mazo (regla
# oficial). Algunas cartas activas (ej. Inventors' Guild) dan una version
# gratuita de este mismo mecanismo -- ver start_research_phase.
RESEARCH_PHASE_COST_MC = 3

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
    """Stock y produccion de recursos de un jugador, mas su Terraform Rating.

    active_cards: cartas jugadas que quedan "en juego" frente al jugador
    porque tienen una accion repetible y/o guardan recursos propios (ej.
    Ironworks: accion; Regolith Eaters: accion + microbios en la carta).
    Forma: {card_id: {"resources": int, "action_used": bool}}. action_used
    se resetea a False en cada fase de produccion (una accion por carta por
    generacion, regla oficial)."""
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
    active_cards: dict

    # tags_played: {"<tag>": int} -- cuenta acumulada de tags en cartas ya
    # jugadas por este jugador (ej. Mass Converter requiere 5 tags de
    # ciencia). Se incrementa en tools.play_card segun los tags de cada
    # carta pagada, nunca se resetea entre generaciones.
    tags_played: dict

    # passive_effects: [{"card_id": str, ...efecto...}, ...] -- cartas ya
    # jugadas que modifican reglas futuras mientras estan en juego, sin ser
    # una accion repetible (ej. Advanced Alloys: steel/titanio valen mas MC;
    # Media Group: +3 MC al jugar un evento). Ver apply_passive_effects_*
    # en este modulo.
    passive_effects: list

    # Sistema de mazo/mano (ver seccion correspondiente mas abajo):
    #   deck: card_ids restantes por robar, orden = orden de robo (el tope
    #     del mazo es deck[0]).
    #   hand: card_ids que el jugador posee y todavia no jugo. play_card
    #     ahora exige que la carta este aca antes de pagarla.
    #   pending_research: card_ids "sobre la mesa", robados pero sin decidir
    #     todavia si se compran (fase de investigacion en dos pasos: ver
    #     start_research_phase / resolve_research_phase).
    deck: list
    hand: list
    pending_research: list

    # played_cards: card_ids que el jugador ya jugo exitosamente, en orden,
    # SIN volver a sacarlas nunca (a diferencia de hand, esto es un historial
    # permanente). Necesario para cartas que targetean "una de tus cartas
    # jugadas" por catalogo/tag en vez de por recursos guardados en la carta
    # (ej. Robotic Workforce: duplicar la caja de produccion de una carta de
    # building ya jugada -- ver tools.play_card, effects.duplicate_production).
    played_cards: list


class GlobalParameters(TypedDict):
    """Estado compartido del tablero central -- no pertenece a un jugador.

    city_tiles_placed: cuenta total de tiles de ciudad colocados por CUALQUIER
    jugador (no se trackea de quien es cada uno -- no hay mapa hexagonal, ver
    CLAUDE.md seccion 6). Suficiente para cartas que pagan "por cada ciudad en
    Marte" (ej. Martian Rails) sin necesitar el tablero completo."""
    temperature: int
    oxygen: int
    oceans_placed: int
    city_tiles_placed: int


def new_player_state() -> PlayerState:
    """Estado inicial de un jugador: TR 20, produccion 1 en cada recurso, stock 0."""
    return PlayerState(
        tr=TR_START,
        mc=0, steel=0, titanium=0, plants=0, energy=0, heat=0,
        mc_production=1, steel_production=1, titanium_production=1,
        plant_production=1, energy_production=1, heat_production=1,
        active_cards={}, tags_played={}, passive_effects=[],
        deck=[], hand=[], pending_research=[], played_cards=[],
    )


def new_global_parameters() -> GlobalParameters:
    return GlobalParameters(
        temperature=TEMPERATURE_MIN, oxygen=OXYGEN_MIN, oceans_placed=0, city_tiles_placed=0
    )


# ---------------------------------------------------------------------------
# Errores de dominio
# ---------------------------------------------------------------------------

class InsufficientResourcesError(Exception):
    """El jugador no tiene suficiente MC/recurso para pagar la accion."""


class GlobalParameterMaxedError(Exception):
    """El parametro global ya esta en su tope; la accion no es legal."""


class CardEffectError(Exception):
    """El efecto de la carta no se pudo aplicar con los parametros dados."""


class CardRequirementNotMetError(Exception):
    """El estado actual del tablero no cumple el requisito de la carta."""


class CardNotInHandError(Exception):
    """El jugador intenta jugar una carta que no tiene en la mano."""


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
    """
    Coloca 1 tile de oceano (de los 9 disponibles en total). +1 TR.

    Tambien dispara los bonus pasivos "on_ocean_placed" que el jugador ya
    tenga activos (ej. Arctic Algae: +2 plantas cada vez que se coloca un
    oceano). En el juego real esto se dispara sin importar QUIEN coloque el
    oceano; como el MVP es de un solo jugador, "cualquiera" siempre es este
    mismo jugador -- por eso el hook vive aca (un solo lugar, todos los
    caminos que colocan oceano se benefician: proyecto estandar Aquifer,
    apply_card_effect, use_card_action) en vez de duplicarse por caller.
    """
    if globals_["oceans_placed"] >= OCEANS_MAX:
        raise GlobalParameterMaxedError("Ya se colocaron los 9 tiles de oceano")

    new_globals = {**globals_, "oceans_placed": globals_["oceans_placed"] + 1}
    new_player: dict = {**player, "tr": player["tr"] + 1}
    for effect in player["passive_effects"]:
        bonus = effect.get("on_ocean_placed")
        if bonus is None:
            continue
        new_player["plants"] = new_player["plants"] + bonus.get("plants_delta", 0)
    return PlayerState(**new_player), new_globals  # type: ignore[typeddict-item]


def place_city_tile(globals_: GlobalParameters) -> GlobalParameters:
    """
    Suma 1 al contador global de tiles de ciudad colocados (por cualquier
    jugador -- no se trackea de quien es cada uno, ver GlobalParameters).
    A diferencia de place_ocean, colocar una ciudad no otorga TR por si sola
    (la regla oficial da TR por produccion de MC ganada, no por el tile).
    """
    return {**globals_, "city_tiles_placed": globals_["city_tiles_placed"] + 1}


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


def standard_project_city(
    player: PlayerState, globals_: GlobalParameters
) -> tuple[PlayerState, GlobalParameters]:
    """Paga 25 MC, coloca tile de ciudad (+1 al contador global), +1 produccion de MC."""
    if player["mc"] < STANDARD_PROJECT_CITY_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_CITY_COST} MC, hay {player['mc']}"
        )
    new_player = {
        **player,
        "mc": player["mc"] - STANDARD_PROJECT_CITY_COST,
        "mc_production": player["mc_production"] + 1,
    }
    return new_player, place_city_tile(globals_)


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
      4. Las acciones de cartas activas (ej. Ironworks) vuelven a estar
         disponibles -- una accion por carta por generacion.
    """
    heat_after_energy_conversion = player["heat"] + player["energy"]

    mc_income = player["tr"] + player["mc_production"]
    new_mc = max(0, player["mc"] + mc_income)

    reset_active_cards = {
        card_id: {**data, "action_used": False} for card_id, data in player["active_cards"].items()
    }

    return {
        **player,
        "mc": new_mc,
        "steel": player["steel"] + player["steel_production"],
        "titanium": player["titanium"] + player["titanium_production"],
        "plants": player["plants"] + player["plant_production"],
        "energy": player["energy_production"],  # arranca de 0 tras la conversion, mas la produccion nueva
        "heat": heat_after_energy_conversion + player["heat_production"],
        "active_cards": reset_active_cards,
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
    steel_value_mc: int = STEEL_VALUE_MC,
    titanium_value_mc: int = TITANIUM_VALUE_MC,
) -> int:
    """
    Verifica que una combinacion de MC + acero + titanio cubra el costo de
    una carta, respetando que acero solo vale para cartas con tag "building"
    y titanio solo para cartas con tag "space". No hay reembolso por pagar
    de mas (regla oficial).

    steel_value_mc/titanium_value_mc son parametrizables (por defecto las
    constantes oficiales 2/3) porque algunas cartas activas los suben de
    forma permanente mientras estan en juego (ej. Advanced Alloys: +1 MC
    extra por cada uno). Ver compute_conversion_rates.

    Devuelve el MC sobrante que el jugador de mas (0 si pago exacto o de mas).
    Lanza InsufficientResourcesError si no alcanza para cubrir el costo.
    """
    if steel_to_pay > 0 and "building" not in card_tags:
        raise ValueError("El acero solo puede pagar cartas con tag 'building'")
    if titanium_to_pay > 0 and "space" not in card_tags:
        raise ValueError("El titanio solo puede pagar cartas con tag 'space'")

    total_value = mc_to_pay + steel_to_pay * steel_value_mc + titanium_to_pay * titanium_value_mc

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


def check_card_requirements(
    requirements: dict | None,
    globals_: GlobalParameters,
    player: PlayerState | None = None,
) -> None:
    """
    Valida que el estado del tablero cumpla el requisito de la carta
    (columna `requirements` en la tabla `cards`). Vocabulario soportado:

      - "min_temperature": temperatura minima en grados C (ej. Farming: 4).
      - "max_temperature": temperatura maxima en grados C (ej. Arctic Algae:
        -12, solo se puede jugar mientras haga MAS frio que eso).
      - "min_oxygen": oxigeno minimo en % (ej. cartas que piden 8% o mas).
      - "max_oxygen": oxigeno maximo en % (ej. Domed Crater: 7).
      - "min_oceans": cantidad minima de tiles de oceano colocados.
      - "min_tag_count": {"tag": "<tag>", "count": N} -- requiere que el
        jugador haya jugado al menos N cartas con ese tag (ej. Mass
        Converter: 5 tags de ciencia). Requiere pasar `player`.
      - "min_production": {"key": "<recurso>_production", "count": N} -- requiere
        que el jugador ya tenga esa produccion en al menos N (ej. Great
        Escarpment Consortium: requiere tener produccion de steel >= 1).
        Requiere pasar `player`.

    requirements None o {} no exige nada. Lanza CardRequirementNotMetError
    si algun requisito no se cumple.
    """
    if not requirements:
        return

    if "min_tag_count" in requirements:
        spec = requirements["min_tag_count"]
        if player is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado del jugador (tags_played)"
            )
        have = player["tags_played"].get(spec["tag"], 0)
        if have < spec["count"]:
            raise CardRequirementNotMetError(
                f"Requiere {spec['count']} tags de '{spec['tag']}' jugados, hay {have}"
            )

    if "min_production" in requirements:
        spec = requirements["min_production"]
        if player is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado del jugador (produccion propia)"
            )
        have = player[spec["key"]]
        if have < spec["count"]:
            raise CardRequirementNotMetError(
                f"Requiere {spec['key']} >= {spec['count']}, hay {have}"
            )

    if "min_temperature" in requirements and globals_["temperature"] < requirements["min_temperature"]:
        raise CardRequirementNotMetError(
            f"Requiere temperatura >= {requirements['min_temperature']}C, "
            f"hay {globals_['temperature']}C"
        )
    if "min_oxygen" in requirements and globals_["oxygen"] < requirements["min_oxygen"]:
        raise CardRequirementNotMetError(
            f"Requiere oxigeno >= {requirements['min_oxygen']}%, hay {globals_['oxygen']}%"
        )
    if "min_oceans" in requirements and globals_["oceans_placed"] < requirements["min_oceans"]:
        raise CardRequirementNotMetError(
            f"Requiere {requirements['min_oceans']} oceanos colocados, "
            f"hay {globals_['oceans_placed']}"
        )
    if "max_temperature" in requirements and globals_["temperature"] > requirements["max_temperature"]:
        raise CardRequirementNotMetError(
            f"Requiere temperatura <= {requirements['max_temperature']}C, "
            f"hay {globals_['temperature']}C"
        )
    if "max_oxygen" in requirements and globals_["oxygen"] > requirements["max_oxygen"]:
        raise CardRequirementNotMetError(
            f"Requiere oxigeno <= {requirements['max_oxygen']}%, hay {globals_['oxygen']}%"
        )


def apply_card_effect(
    player: PlayerState,
    globals_: GlobalParameters,
    effects: dict,
    effect_amount: int | None = None,
    effect_choice: int | None = None,
) -> tuple[PlayerState, GlobalParameters]:
    """
    Aplica el efecto inmediato de una carta ya pagada, segun el jsonb
    `effects` de la tabla `cards`. Siempre recibe y devuelve tambien los
    parametros globales porque algunas cartas suben temperatura/oceanos
    directamente (no solo cambian stock/produccion del jugador). Vocabulario
    soportado por las cartas cargadas hasta ahora (ver seed_cards.sql):

      - "mc_production_delta": entero fijo que se suma a la produccion de MC
        (forma antigua, mantenida por compatibilidad -- ej. Sponsors: +2).
      - "mc_delta": entero fijo que se suma al stock de MC (forma antigua,
        mantenida por compatibilidad -- ej. Investment Loan: +10).
      - "production_deltas": {"<recurso>_production": delta, ...} -- forma
        generica para cambiar una o mas producciones a la vez (ej. Nuclear
        Power: -2 produccion MC, +3 produccion energia).
      - "resource_deltas": {"<recurso>": delta, ...} -- forma generica para
        cambiar stock de uno o mas recursos (ej. Solar Wind Power: +2 titanio).
        Un delta negativo que dejaria el stock por debajo de 0 lanza
        InsufficientResourcesError (es un costo obligatorio de la carta, ej.
        Nitrophilic Moss: perder 2 plantas).
      - "convert_production": {"from": "<recurso>_production", "to":
        "<recurso>_production"} convierte `effect_amount` (X, elegido por el
        jugador) pasos de produccion de un recurso a otro, limitado al stock
        de produccion disponible (ej. Insulation: -X calor, +X MC).
      - "raise_temperature_steps": N -- sube la temperatura N pasos (+N TR),
        via raise_temperature (ej. Comet: 1 paso).
      - "raise_oxygen_steps": N -- sube el oxigeno N pasos (+N TR).
      - "place_oceans": N -- coloca N tiles de oceano (+N TR) (ej. Comet: 1).
      - "place_city_tiles": N -- suma N al contador global de ciudades, sin
        TR (ej. Capital: 1).
      - "tr_delta": N -- sube el TR directo, sin pasar por un parametro
        global (ej. Release of Inert Gases: +2).
      - "draw_cards": N -- roba N cartas del mazo directo a la mano, sin
        fase de investigacion (ej. Research: +2 cartas). Reusa
        draw_cards_to_hand (mismo mecanismo que use_card_action.gains.draw_cards,
        pero como efecto inmediato al jugar la carta, no como accion repetible).
      - "resource_delta_per_counter": {"resource": "<recurso>", "counter":
        "<contador de GlobalParameters>", "per_counter": N (default 1)} --
        suma al stock del recurso tanto como valga ese contador global (ej.
        Greenhouses: +1 planta por cada ciudad en city_tiles_placed). Analogo
        a "mc_per_counter" en use_card_action.gains, pero como efecto
        inmediato y para cualquier recurso, no solo MC.
      - "choice": lista de sub-effects (cualquiera de los de arriba); el
        jugador elige uno via `effect_choice` (indice 0-based) (ej.
        Artificial Photosynthesis: +1 produccion de plantas O +2 de energia).
      - "tag_count_choice": {"tag": "<tag>", "count": N, "if_met": <sub-effect>,
        "else": <sub-effect>} -- a diferencia de "choice", esta rama NO la
        elige el jugador: se resuelve sola comparando `tags_played` del
        jugador contra `count` (ej. Nitrogen-Rich Asteroid: +4 produccion de
        plantas si ya jugo 3 tags de planta, si no +1). `tags_played` se lee
        ANTES de sumar los tags de la carta que se esta jugando (tools.play_card
        llama apply_card_effect antes de increment_tags_played).
      - "production_delta_per_tag": {"tag": "<tag>", "production":
        "<recurso>_production", "per_tag": N (default 1)} -- suma N por cada
        tag "<tag>" ya jugado (no es un umbral binario como tag_count_choice,
        escala linealmente) (ej. Miranda Resort: +1 produccion de MC por cada
        tag earth jugado). Tambien lee `tags_played` antes de sumar los tags
        de la carta actual.

    NOTA sobre "remove up to N <recurso> from any player": varias cartas del
    catalogo (ej. Comet, Asteroid, Big Asteroid) tienen esta clausula opcional
    (0 a N) para hostigar a otro jugador. Como el MVP es de un solo jugador y
    elegir 0 siempre es legal, esta clausula se omite del todo -- el resto del
    efecto (garantizado) si se aplica. Ver CARDS_LOG.md.

    effects == {} no hace nada (carta sin efecto modelado todavia).
    """
    if "choice" in effects:
        options = effects["choice"]
        if effect_choice is None or not (0 <= effect_choice < len(options)):
            raise CardEffectError(
                f"Esta carta requiere effect_choice entre 0 y {len(options) - 1}"
            )
        return apply_card_effect(player, globals_, options[effect_choice], effect_amount)

    if "tag_count_choice" in effects:
        spec = effects["tag_count_choice"]
        have = player["tags_played"].get(spec["tag"], 0)
        branch = spec["if_met"] if have >= spec["count"] else spec["else"]
        return apply_card_effect(player, globals_, branch, effect_amount)

    new_player: dict = dict(player)
    new_globals: dict = dict(globals_)

    if "mc_production_delta" in effects:
        new_player["mc_production"] = _apply_production_floor(
            "mc_production", new_player["mc_production"] + effects["mc_production_delta"]
        )

    if "mc_delta" in effects:
        new_player["mc"] = max(0, new_player["mc"] + effects["mc_delta"])

    if "production_deltas" in effects:
        for key, delta in effects["production_deltas"].items():
            new_player[key] = _apply_production_floor(key, new_player[key] + delta)

    if "production_delta_per_tag" in effects:
        spec = effects["production_delta_per_tag"]
        key = spec["production"]
        count = player["tags_played"].get(spec["tag"], 0)
        delta = count * spec.get("per_tag", 1)
        new_player[key] = _apply_production_floor(key, new_player[key] + delta)

    if "resource_delta_per_counter" in effects:
        spec = effects["resource_delta_per_counter"]
        resource_key = spec["resource"]
        count = globals_[spec["counter"]]
        new_player[resource_key] = max(0, new_player[resource_key] + count * spec.get("per_counter", 1))

    if "resource_deltas" in effects:
        for key, delta in effects["resource_deltas"].items():
            if delta < 0 and new_player[key] + delta < 0:
                raise InsufficientResourcesError(
                    f"No hay suficiente {key} ({new_player[key]}) para pagar el costo de {-delta}"
                )
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

    if "raise_temperature_steps" in effects:
        p2, g2 = raise_temperature(
            PlayerState(**new_player), GlobalParameters(**new_globals),  # type: ignore[typeddict-item]
            steps=effects["raise_temperature_steps"],
        )
        new_player, new_globals = dict(p2), dict(g2)

    if "raise_oxygen_steps" in effects:
        p2, g2 = raise_oxygen(
            PlayerState(**new_player), GlobalParameters(**new_globals),  # type: ignore[typeddict-item]
            steps=effects["raise_oxygen_steps"],
        )
        new_player, new_globals = dict(p2), dict(g2)

    if "place_oceans" in effects:
        for _ in range(effects["place_oceans"]):
            p2, g2 = place_ocean(PlayerState(**new_player), GlobalParameters(**new_globals))  # type: ignore[typeddict-item]
            new_player, new_globals = dict(p2), dict(g2)

    if "place_city_tiles" in effects:
        for _ in range(effects["place_city_tiles"]):
            new_globals = dict(place_city_tile(GlobalParameters(**new_globals)))  # type: ignore[typeddict-item]

    if "tr_delta" in effects:
        new_player["tr"] = new_player["tr"] + effects["tr_delta"]

    if "draw_cards" in effects:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), effects["draw_cards"]))  # type: ignore[typeddict-item]

    return PlayerState(**new_player), GlobalParameters(**new_globals)  # type: ignore[typeddict-item]


# ---------------------------------------------------------------------------
# Cartas activas: accion repetible (una vez por generacion) y/o recursos
# propios de la carta (ej. Ironworks: accion; Regolith Eaters: accion +
# microbios guardados en la carta)
# ---------------------------------------------------------------------------

def register_active_card(player: PlayerState, card_id: str) -> PlayerState:
    """
    Marca una carta recien jugada como "activa" -- queda en juego frente al
    jugador porque tiene una accion repetible y/o guarda recursos propios.
    Se llama despues de pagar la carta, solo si `effects.becomes_active` es
    true en su fila de `cards`. Si la carta ya estaba activa (no deberia
    pasar, cada carta se juega una vez), reinicia sus contadores.
    """
    new_active_cards = dict(player["active_cards"])
    new_active_cards[card_id] = {"resources": 0, "action_used": False}
    return {**player, "active_cards": new_active_cards}


def use_card_action(
    player: PlayerState,
    globals_: GlobalParameters,
    card_id: str,
    action_spec: dict,
    effect_choice: int | None = None,
) -> tuple[PlayerState, GlobalParameters]:
    """
    Ejecuta la accion repetible de una carta activa (columna `effects.action`
    en `cards`). Vocabulario de `action_spec`:

      - "cost": {"<recurso>": N, ...} -- recursos de stock del jugador que se
        gastan (ej. Ironworks: {"energy": 4}). La clave especial
        "card_resource" gasta N recursos guardados en la propia carta (ej.
        Regolith Eaters: remover 2 microbios).
      - "gains": {"resource_deltas": {...}, "production_deltas": {...},
        "raise_oxygen_steps": N, "raise_temperature_steps": N,
        "card_resource_delta": N, "tr_delta": N, "mc_per_counter":
        "<nombre del contador en GlobalParameters>"} -- N > 0 en
        card_resource_delta agrega recursos a la propia carta (ej. Regolith
        Eaters: agregar 1 microbio); tr_delta sube el TR directo sin pasar
        por un parametro global (ej. Equatorial Magnetizer); mc_per_counter
        da tanto MC como valga ese contador global (ej. Martian Rails: MC
        por cada ciudad en Marte via "city_tiles_placed"); place_oceans: N
        coloca N tiles de oceano (+N TR cada uno) (ej. Water Import from
        Europa); draw_cards: N roba N cartas del mazo directo a la mano,
        sin fase de investigacion (ej. Development Center); start_research:
        {"n": N} roba N cartas a pending_research -- el jugador todavia
        tiene que resolver la compra por separado con resolve_research_phase
        (tipicamente a costo 0, ej. Inventors' Guild: n=1).
      - "choice": lista de action_spec alternativos; se elige uno con
        `effect_choice` (ej. Regolith Eaters: agregar microbio O gastar 2
        para subir oxigeno).

    Lanza CardEffectError si la carta no esta activa para este jugador o si
    su accion ya se uso esta generacion. Lanza InsufficientResourcesError si
    falta stock (del jugador o de la propia carta) para pagar el costo.
    """
    if card_id not in player["active_cards"]:
        raise CardEffectError(f"La carta '{card_id}' no esta activa para este jugador")
    if player["active_cards"][card_id]["action_used"]:
        raise CardEffectError(f"La accion de '{card_id}' ya se uso esta generacion")

    if "choice" in action_spec:
        options = action_spec["choice"]
        if effect_choice is None or not (0 <= effect_choice < len(options)):
            raise CardEffectError(
                f"Esta accion requiere effect_choice entre 0 y {len(options) - 1}"
            )
        action_spec = options[effect_choice]

    new_player: dict = dict(player)
    new_active_cards = dict(player["active_cards"])
    card_resources = new_active_cards[card_id]["resources"]

    for key, amount in action_spec.get("cost", {}).items():
        if key == "card_resource":
            if card_resources < amount:
                raise InsufficientResourcesError(
                    f"'{card_id}' tiene {card_resources} recursos guardados, se necesitan {amount}"
                )
            card_resources -= amount
        else:
            if new_player[key] < amount:
                raise InsufficientResourcesError(f"Se necesita {amount} de {key}, hay {new_player[key]}")
            new_player[key] -= amount

    gains = action_spec.get("gains", {})
    new_globals: dict = dict(globals_)

    for key, delta in gains.get("resource_deltas", {}).items():
        new_player[key] = max(0, new_player[key] + delta)
    for key, delta in gains.get("production_deltas", {}).items():
        new_player[key] = _apply_production_floor(key, new_player[key] + delta)
    if "card_resource_delta" in gains:
        card_resources = max(0, card_resources + gains["card_resource_delta"])
    if "raise_oxygen_steps" in gains:
        p2, g2 = raise_oxygen(PlayerState(**new_player), GlobalParameters(**new_globals), steps=gains["raise_oxygen_steps"])  # type: ignore[typeddict-item]
        new_player, new_globals = dict(p2), dict(g2)
    if "raise_temperature_steps" in gains:
        p2, g2 = raise_temperature(PlayerState(**new_player), GlobalParameters(**new_globals), steps=gains["raise_temperature_steps"])  # type: ignore[typeddict-item]
        new_player, new_globals = dict(p2), dict(g2)
    if "tr_delta" in gains:
        new_player["tr"] = new_player["tr"] + gains["tr_delta"]
    if "mc_per_counter" in gains:
        new_player["mc"] = new_player["mc"] + new_globals[gains["mc_per_counter"]]
    if "place_oceans" in gains:
        for _ in range(gains["place_oceans"]):
            p2, g2 = place_ocean(PlayerState(**new_player), GlobalParameters(**new_globals))  # type: ignore[typeddict-item]
            new_player, new_globals = dict(p2), dict(g2)
    if "draw_cards" in gains:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), gains["draw_cards"]))  # type: ignore[typeddict-item]
    if "start_research" in gains:
        new_player = dict(start_research_phase(PlayerState(**new_player), gains["start_research"]["n"]))  # type: ignore[typeddict-item]

    new_active_cards[card_id] = {"resources": card_resources, "action_used": True}
    new_player["active_cards"] = new_active_cards

    return PlayerState(**new_player), GlobalParameters(**new_globals)  # type: ignore[typeddict-item]


# ---------------------------------------------------------------------------
# Tags jugados y efectos pasivos permanentes
# ---------------------------------------------------------------------------

def increment_tags_played(player: PlayerState, card_tags: tuple[str, ...]) -> PlayerState:
    """
    Suma 1 a cada tag de `card_tags` en el contador `tags_played` del
    jugador. Se llama una vez por cada carta pagada exitosamente (via
    tools.play_card), nunca se resetea entre generaciones. Alimenta
    requisitos como "requiere 5 tags de ciencia" (Mass Converter).
    """
    new_tags_played = dict(player["tags_played"])
    for tag in card_tags:
        new_tags_played[tag] = new_tags_played.get(tag, 0) + 1
    return {**player, "tags_played": new_tags_played}


def register_passive_effect(player: PlayerState, card_id: str, passive: dict) -> PlayerState:
    """
    Registra un efecto pasivo permanente de una carta recien jugada. A
    diferencia de active_cards (accion repetible), un efecto pasivo no se
    "usa" -- esta siempre activo mientras la carta siga en juego (que en
    este motor es para siempre, no hay descarte). Vocabulario de `passive`:

      - "steel_value_bonus" / "titanium_value_bonus": MC extra por unidad al
        pagar OTRAS cartas con acero/titanio (ej. Advanced Alloys: +1 cada
        uno). Ver compute_conversion_rates.
      - "on_event_played": {"mc_delta": N, "heat_delta": N, ...} -- se suma
        al jugador cada vez que juega una carta con `cards.is_event = true`
        (ej. Media Group: +3 MC; Optimal Aerobraking: +3 MC y +3 calor, solo
        para eventos con tag space -- ver "tag_filter" opcional).
      - "on_ocean_placed": {"plants_delta": N} -- se suma cada vez que se
        coloca un oceano, sin importar la fuente (proyecto estandar Aquifer,
        una carta, una accion) (ej. Arctic Algae: +2 plantas). Aplicado
        directo dentro de place_ocean, no hace falta llamarlo aparte.
      - "card_cost_discount_mc": N -- ver compute_card_cost_discount.
      - "on_tag_played_may_swap_card": {"tag": "<tag>"} -- cada vez que el
        jugador juega CUALQUIER carta con ese tag (incluida la que registra
        el pasivo), puede opcionalmente descartar 1 carta de la mano para
        robar 1 del mazo (ej. Mars University: tag "science"). A diferencia
        de on_event_played (automatico), esto es una ELECCION del jugador --
        ver tools.play_card (parametro discard_for_draw_card_id) y
        rules_engine.player_has_tag_swap_passive / swap_card_for_draw.

    No revisa duplicados: cada carta se juega una sola vez en este motor.
    """
    return {**player, "passive_effects": [*player["passive_effects"], {"card_id": card_id, **passive}]}


def compute_conversion_rates(player: PlayerState) -> tuple[int, int]:
    """
    Devuelve (steel_value_mc, titanium_value_mc) sumando los bonus de todos
    los efectos pasivos activos del jugador a las constantes oficiales
    (ej. con Advanced Alloys en juego: 2+1=3 MC por acero, 3+1=4 por titanio).
    """
    steel_value = STEEL_VALUE_MC
    titanium_value = TITANIUM_VALUE_MC
    for effect in player["passive_effects"]:
        steel_value += effect.get("steel_value_bonus", 0)
        titanium_value += effect.get("titanium_value_bonus", 0)
    return steel_value, titanium_value


def compute_card_cost_discount(player: PlayerState, card_tags: tuple[str, ...]) -> int:
    """
    Suma los descuentos de costo ("card_cost_discount_mc") de todos los
    efectos pasivos activos del jugador que apliquen a esta carta (segun
    `tag_filter`, si el efecto lo tiene) (ej. Mass Converter: -2 MC en
    cartas con tag "space"). Se resta del costo antes de calcular el pago
    en tools.play_card -- nunca deja el costo por debajo de 0.
    """
    discount = 0
    for effect in player["passive_effects"]:
        bonus = effect.get("card_cost_discount_mc")
        if bonus is None:
            continue
        tag_filter = effect.get("tag_filter")
        if tag_filter is not None and tag_filter not in card_tags:
            continue
        discount += bonus
    return discount


def apply_event_played_bonuses(player: PlayerState, played_card_tags: tuple[str, ...] = ()) -> PlayerState:
    """
    Aplica los bonus "on_event_played" de todos los efectos pasivos activos
    del jugador. Llamar UNA VEZ, justo despues de pagar y aplicar el efecto
    de una carta cuyo `cards.is_event` sea true. `played_card_tags` filtra
    bonus que solo aplican a un tag especifico del evento jugado (ej. Optimal
    Aerobraking: "cuando juegues un EVENTO ESPACIAL" via
    passive["tag_filter"] = "space" -- si el evento jugado no tiene ese tag,
    ese bonus en particular no se aplica).
    """
    new_player: dict = dict(player)
    for effect in player["passive_effects"]:
        bonus = effect.get("on_event_played")
        if bonus is None:
            continue
        tag_filter = effect.get("tag_filter")
        if tag_filter is not None and tag_filter not in played_card_tags:
            continue
        new_player["mc"] = new_player["mc"] + bonus.get("mc_delta", 0)
        new_player["heat"] = new_player["heat"] + bonus.get("heat_delta", 0)
    return PlayerState(**new_player)  # type: ignore[typeddict-item]


def player_has_tag_swap_passive(player: PlayerState, played_card_tags: tuple[str, ...]) -> bool:
    """
    True si el jugador tiene un pasivo "on_tag_played_may_swap_card" cuyo tag
    coincide con alguno de los tags de la carta recien jugada (ej. Mars
    University: tag "science"). Usado por tools.play_card para saber si
    ofrecerle al usuario la opcion de descartar 1 carta y robar 1.
    """
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_may_swap_card")
        if spec is not None and spec["tag"] in played_card_tags:
            return True
    return False


def swap_card_for_draw(player: PlayerState, discard_card_id: str) -> PlayerState:
    """
    Descarta `discard_card_id` de la mano y roba 1 carta del mazo (ej. Mars
    University). Lanza CardNotInHandError si el jugador no tiene esa carta.
    """
    discarded_player = remove_card_from_hand(player, discard_card_id)
    return draw_cards_to_hand(discarded_player, 1)


# ---------------------------------------------------------------------------
# Sistema de mazo / mano
#
# Cada jugador tiene su propio mazo (barajado a partir del catalogo
# disponible en `cards`) y su propia mano (cartas que posee y no jugo
# todavia). No hay mazo/descarte compartido entre jugadores -- coherente con
# que el MVP es de un solo jugador (ver CLAUDE.md seccion 6). play_card
# ahora exige que la carta este en la mano antes de pagarla.
#
# La fase de investigacion (robar N, elegir cuales comprar a
# RESEARCH_PHASE_COST_MC cada una) se modela en dos pasos porque requiere
# que el usuario vea las cartas robadas antes de decidir:
#   1. start_research_phase: roba N cartas del mazo a `pending_research`.
#   2. resolve_research_phase: de esas, compra las elegidas (se van a
#      `hand`, se cobran); las no elegidas se descartan (no vuelven al mazo).
# Cartas como Inventors' Guild usan el mismo mecanismo con N=1 y costo 0
# (su accion es "gratis": ver seed_cards.sql).
# ---------------------------------------------------------------------------

def initialize_deck(card_ids: list[str], rng: random.Random | None = None) -> list[str]:
    """
    Baraja `card_ids` (tipicamente todo `cards.id` del catalogo disponible)
    y devuelve el mazo inicial de un jugador. `rng` es inyectable para tests
    deterministicos; por defecto usa aleatoriedad real.
    """
    shuffled = list(card_ids)
    (rng or random).shuffle(shuffled)
    return shuffled


def start_research_phase(player: PlayerState, n: int) -> PlayerState:
    """
    Roba `n` cartas del tope del mazo (deck[0], deck[1], ...) a
    `pending_research`, sin cobrar nada todavia -- el jugador (via el
    usuario, a traves del LLM) decide despues cuales comprar con
    resolve_research_phase. Si el mazo tiene menos de `n` cartas, roba las
    que queden (no es un error: el mazo se puede agotar).

    Lanza CardEffectError si ya hay una investigacion pendiente sin resolver
    (no se puede empezar una nueva fase mientras la anterior no se cierra).
    """
    if player["pending_research"]:
        raise CardEffectError(
            "Ya hay una fase de investigacion pendiente -- resolvela antes de iniciar otra"
        )
    drawn = player["deck"][:n]
    remaining_deck = player["deck"][n:]
    return {**player, "deck": remaining_deck, "pending_research": drawn}


def resolve_research_phase(
    player: PlayerState,
    card_ids_to_buy: list[str],
    cost_per_card: int = RESEARCH_PHASE_COST_MC,
) -> PlayerState:
    """
    Cierra una fase de investigacion iniciada con start_research_phase.
    `card_ids_to_buy` deben ser un subconjunto de `pending_research` -- esas
    se pagan a `cost_per_card` MC cada una (0 para acciones gratuitas como
    Inventors' Guild) y pasan a `hand`; el resto de `pending_research` se
    descarta (no vuelve al mazo). Siempre limpia `pending_research`, incluso
    si `card_ids_to_buy` esta vacio (comprar 0 cartas es una eleccion valida).

    Lanza ValueError si algun id en `card_ids_to_buy` no estaba en
    `pending_research`. Lanza InsufficientResourcesError si no alcanza el MC.
    """
    pending = set(player["pending_research"])
    for card_id in card_ids_to_buy:
        if card_id not in pending:
            raise ValueError(
                f"'{card_id}' no estaba en la investigacion pendiente ({sorted(pending)})"
            )

    total_cost = len(card_ids_to_buy) * cost_per_card
    if player["mc"] < total_cost:
        raise InsufficientResourcesError(
            f"Comprar {len(card_ids_to_buy)} cartas cuesta {total_cost} MC, hay {player['mc']}"
        )

    return {
        **player,
        "mc": player["mc"] - total_cost,
        "hand": [*player["hand"], *card_ids_to_buy],
        "pending_research": [],
    }


def draw_cards_to_hand(player: PlayerState, n: int) -> PlayerState:
    """
    Roba `n` cartas del mazo DIRECTO a la mano, sin costo de investigacion
    (ej. Development Center: pagar 1 energia y robar 1 carta gratis -- el
    costo de energia ya se cobro en use_card_action, esto solo mueve las
    cartas). Si el mazo tiene menos de `n`, roba las que queden.
    """
    drawn = player["deck"][:n]
    remaining_deck = player["deck"][n:]
    return {**player, "deck": remaining_deck, "hand": [*player["hand"], *drawn]}


def remove_card_from_hand(player: PlayerState, card_id: str) -> PlayerState:
    """
    Saca `card_id` de la mano del jugador (se llama al jugarla exitosamente
    via tools.play_card). Lanza CardNotInHandError si el jugador no la tiene
    -- no se puede jugar una carta que no se posee.
    """
    if card_id not in player["hand"]:
        raise CardNotInHandError(f"El jugador no tiene '{card_id}' en la mano")
    new_hand = list(player["hand"])
    new_hand.remove(card_id)
    return {**player, "hand": new_hand}


def register_played_card(player: PlayerState, card_id: str) -> PlayerState:
    """
    Agrega `card_id` al historial permanente de cartas jugadas (`played_cards`).
    Se llama UNA vez por cada carta jugada exitosamente via tools.play_card,
    sin importar si la carta tiene accion/pasivo/efecto de tablero o no --
    cualquier carta puede ser el objetivo de una futura carta que targetee
    "una de tus cartas jugadas" (ej. Robotic Workforce).
    """
    return {**player, "played_cards": [*player["played_cards"], card_id]}
