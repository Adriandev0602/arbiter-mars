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

# Venus (expansion Venus Next): 4to parametro global, opcional -- 0% a 30%
# (a diferencia de temperatura/oxigeno que llegan a 100% de progreso), en
# pasos de 2%. Fuente: rulebook oficial de Venus Next (fryxgames.se). No
# es condicion de fin de partida (solo temperatura/oxigeno/oceanos lo son).
VENUS_MIN = 0
VENUS_MAX = 30
VENUS_STEP = 2

# Bonus de paso del Venus scale (verificado contra el rulebook oficial): al
# CRUZAR 8% se roba 1 carta gratis (una sola vez); al cruzar 16% se otorga
# 1 TR extra (una sola vez). "Cruzar" = el valor anterior estaba por debajo
# del umbral y el nuevo lo alcanza o supera -- ver raise_venus.
VENUS_BONUS_STEP_DRAW_CARD = 8
VENUS_BONUS_STEP_EXTRA_TR = 16

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
STANDARD_PROJECT_AIR_SCRAPPING_COST = 15  # +1 paso de Venus (Venus Next, +1 TR como cualquier paso)


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

    # pending_mc_discount: MC de descuento pendiente para la PROXIMA carta
    # que el jugador juegue esta generacion (ej. Indentured Workers: -8).
    # Se consume (vuelve a 0) al jugar la siguiente carta -- la cubra
    # entera o no -- y tambien se pierde si termina la generacion sin
    # usarse (ver run_production_phase). Ver apply_card_effect
    # ("next_card_discount_mc") y tools.play_card.
    pending_mc_discount: int

    # Igual que pending_mc_discount pero para relajar/endurecer (puede ser
    # negativo) los requisitos de temperatura/oxigeno/oceanos de la
    # PROXIMA carta jugada esta generacion, en pasos (ej. Special Design:
    # +/-2, a eleccion del jugador). Se consume al chequear esa carta. Ver
    # check_card_requirements ("next_card_requirement_tolerance_steps") y
    # tools.play_card.
    pending_requirement_tolerance_steps: int

    # reserved_cards: {reserved_card_id: {"resources": int, "holder_card_id":
    # str}} -- cartas de la mano "reservadas" sobre otra carta activa (ej.
    # Self-Replicating Robots) sin jugarlas ni pagarlas todavia, con
    # recursos acumulables encima que despues descuentan su costo al
    # jugarlas. Distinto de active_cards (cartas YA jugadas con accion
    # repetible) y de hand (cartas sin tocar) -- una carta reservada salio
    # de hand pero no cuenta como jugada (no tags_played, no played_cards,
    # no dispara pasivos) hasta que tools.play_card la juegue "como si
    # estuviera en mano". Ver reserve_card_in_slot,
    # duplicate_reserved_card_resources, compute_reserved_card_discount,
    # release_reserved_card.
    reserved_cards: dict

    # zero_tag_cards_played: cuenta de cartas jugadas SIN ningun tag (ej.
    # Community Services: +1 produccion MC por cada una, incluida ella
    # misma). Se incrementa en tools.play_card cuando card.tags esta vacio,
    # analogo a tags_played pero para el caso "sin tags" (que tags_played
    # no puede expresar, ya que no hay ningun tag que contar).
    zero_tag_cards_played: int

    # colonies_owned: colony_ids donde este jugador ya construyo una
    # colonia (maximo 1 por colonia, ver colonies.build_colony). Alimenta
    # "production_delta_per_colony" (ej. Ecology Research: +1 produccion
    # de plantas por cada colonia propia).
    colonies_owned: list

    # trade_fleets: cantidad de flotas de comercio que POSEE el jugador
    # (arranca en 1, algunas cartas dan mas). trade_fleets_used: cuantas ya
    # uso esta generacion (vuelve a 0 en la fase solar, junto con
    # run_production_phase -- ver tools.run_production_phase). Disponibles
    # para comerciar = trade_fleets - trade_fleets_used. Ver colonies.py.
    trade_fleets: int
    trade_fleets_used: int

    # lobby_delegates/reserve_delegates: expansion Turmoil (ver
    # backend/app/agent/turmoil.py para el mecanismo completo). Arrancan en
    # 1 y 6 respectivamente (7 delegados totales, setup oficial). Se gastan
    # al colocar delegados (tools.lobby, tools.play_card para Colonial
    # Envoys) y vuelven con tools.resolve_new_government.
    lobby_delegates: int
    reserve_delegates: int


class GlobalParameters(TypedDict):
    """Estado compartido del tablero central -- no pertenece a un jugador.

    city_tiles_placed: cuenta total de tiles de ciudad colocados por CUALQUIER
    jugador (no se trackea de quien es cada uno -- no hay mapa hexagonal, ver
    CLAUDE.md seccion 6). Suficiente para cartas que pagan "por cada ciudad en
    Marte" (ej. Martian Rails) sin necesitar el tablero completo.

    events_played: cuenta total de cartas con is_event=true jugadas por
    CUALQUIER jugador, historico, nunca se resetea (ej. Media Archives: gana
    1 MC por cada evento jugado alguna vez). Se incrementa en tools.play_card
    via increment_events_played, junto con apply_event_played_bonuses.

    venus: 4to parametro global, opcional (expansion Venus Next), 0% a 30%
    en pasos de 2%. NO es condicion de fin de partida -- ver raise_venus."""
    temperature: int
    oxygen: int
    oceans_placed: int
    city_tiles_placed: int
    events_played: int
    venus: int


def new_player_state() -> PlayerState:
    """Estado inicial de un jugador: TR 20, produccion 1 en cada recurso, stock 0."""
    return PlayerState(
        tr=TR_START,
        mc=0, steel=0, titanium=0, plants=0, energy=0, heat=0,
        mc_production=1, steel_production=1, titanium_production=1,
        plant_production=1, energy_production=1, heat_production=1,
        active_cards={}, tags_played={}, passive_effects=[],
        deck=[], hand=[], pending_research=[], played_cards=[],
        pending_mc_discount=0, pending_requirement_tolerance_steps=0,
        reserved_cards={}, zero_tag_cards_played=0,
        colonies_owned=[], trade_fleets=1, trade_fleets_used=0,
        lobby_delegates=1, reserve_delegates=6,
    )


def new_global_parameters() -> GlobalParameters:
    return GlobalParameters(
        temperature=TEMPERATURE_MIN, oxygen=OXYGEN_MIN, oceans_placed=0, city_tiles_placed=0,
        events_played=0, venus=VENUS_MIN,
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


def raise_venus(player: PlayerState, globals_: GlobalParameters, steps: int = 1) -> tuple[PlayerState, GlobalParameters]:
    """
    Sube el Venus scale (expansion Venus Next) `steps` pasos (2% cada uno).
    +1 TR por paso aplicado, igual que temperatura/oxigeno. Ademas aplica
    los bonus de paso oficiales, cada uno una sola vez al CRUZAR el umbral
    (el valor anterior estaba por debajo, el nuevo lo alcanza o supera):
    al llegar a 8% roba 1 carta gratis; al llegar a 16% otorga 1 TR extra.
    """
    if globals_["venus"] >= VENUS_MAX:
        raise GlobalParameterMaxedError("El Venus scale ya esta en su maximo (30%)")

    before = globals_["venus"]
    max_possible_steps = min(steps, (VENUS_MAX - before) // VENUS_STEP)
    after = before + max_possible_steps * VENUS_STEP

    new_globals = {**globals_, "venus": after}
    new_player: dict = {**player, "tr": player["tr"] + max_possible_steps}
    if before < VENUS_BONUS_STEP_DRAW_CARD <= after:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), 1))  # type: ignore[typeddict-item]
    if before < VENUS_BONUS_STEP_EXTRA_TR <= after:
        new_player["tr"] = new_player["tr"] + 1
    return PlayerState(**new_player), new_globals  # type: ignore[typeddict-item]


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


def increment_events_played(globals_: GlobalParameters) -> GlobalParameters:
    """
    Suma 1 al contador global historico de cartas "Event" jugadas (por
    cualquier jugador). Llamado desde tools.play_card junto con
    apply_event_played_bonuses, cada vez que se juega una carta con
    cards.is_event = true (ej. Media Archives: gana MC segun este contador).
    """
    return {**globals_, "events_played": globals_["events_played"] + 1}


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


def standard_project_air_scrapping(
    player: PlayerState, globals_: GlobalParameters
) -> tuple[PlayerState, GlobalParameters]:
    """
    Proyecto estandar de la expansion Venus Next: paga 15 MC, sube el Venus
    scale 1 paso (+1 TR, mas los bonus de umbral si corresponde -- ver
    raise_venus). Solo disponible si el proyecto usa el parametro Venus
    (ver tools.use_standard_project).
    """
    if player["mc"] < STANDARD_PROJECT_AIR_SCRAPPING_COST:
        raise InsufficientResourcesError(
            f"Se necesitan {STANDARD_PROJECT_AIR_SCRAPPING_COST} MC, hay {player['mc']}"
        )
    paid_player = {**player, "mc": player["mc"] - STANDARD_PROJECT_AIR_SCRAPPING_COST}
    return raise_venus(paid_player, globals_, steps=1)


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
      5. Un descuento pendiente sin usar (ej. Indentured Workers, si el
         jugador no jugo ninguna carta mas esa generacion) se pierde.
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
        "pending_mc_discount": 0,
        "pending_requirement_tolerance_steps": 0,
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
    wild_tag_choice: str | None = None,
    turmoil: dict | None = None,
    player_id: str | None = None,
) -> None:
    """
    Valida que el estado del tablero cumpla el requisito de la carta
    (columna `requirements` en la tabla `cards`). Vocabulario soportado:

      - "min_temperature": temperatura minima en grados C (ej. Farming: 4).
      - "max_temperature": temperatura maxima en grados C (ej. Arctic Algae:
        -12, solo se puede jugar mientras haga MAS frio que eso).
      - "min_oxygen": oxigeno minimo en % (ej. cartas que piden 8% o mas).
      - "max_oxygen": oxigeno maximo en % (ej. Domed Crater: 7).
      - "min_oceans" / "max_oceans": cantidad minima/maxima de tiles de
        oceano colocados (ej. Dust Seals: maximo 3).
      - "min_tr": Terraform Rating minimo del jugador (ej. Terraforming
        Contract: 25). Requiere pasar `player`.
      - "max_colonies_owned": N -- maximo de colonias que el jugador puede
        tener ya construidas (`player["colonies_owned"]`, expansion
        Colonies, ej. Pioneer Settlement: maximo 1). Requiere pasar `player`.
      - "min_colonies_owned": N -- minimo de colonias que el jugador ya
        tiene construidas (ej. Space Port: requiere 1). Requiere pasar
        `player`.
      - "min_venus" / "max_venus": Venus scale minimo/maximo en % (expansion
        Venus Next, ej. cartas que piden Venus >= 8%).
      - "min_city_tiles": cantidad minima de tiles de ciudad colocados en el
        mapa por CUALQUIER jugador (`globals_["city_tiles_placed"]`, ej.
        Rad-Suits: requiere 2 ciudades en juego).
      - "min_tag_count": {"tag": "<tag>", "count": N} -- requiere que el
        jugador haya jugado al menos N cartas con ese tag (ej. Mass
        Converter: 5 tags de ciencia). Requiere pasar `player`. Si el
        jugador tiene el tag comodin "wild" jugado (ej. Research
        Coordination) y pasa `wild_tag_choice="<tag>"` que matchee el tag
        de este requisito, los tags "wild" en juego cuentan como ese tag
        para este chequeo puntual (ver parametro `wild_tag_choice` abajo).
      - "ruling_or_delegates": {"party": "<partido>", "min_delegates": N
        (default 2)} -- expansion Turmoil (ver turmoil.py), requiere que
        `party` sea el partido Ruling actual, O que el jugador tenga al
        menos `min_delegates` delegados propios ahi (ej. Colonial Envoys:
        partido "unity"). Requiere pasar `turmoil` y `player_id`.
      - "min_production": {"key": "<recurso>_production", "count": N} -- requiere
        que el jugador ya tenga esa produccion en al menos N (ej. Great
        Escarpment Consortium: requiere tener produccion de steel >= 1).
        Requiere pasar `player`.

    requirements None o {} no exige nada. Lanza CardRequirementNotMetError
    si algun requisito no se cumple.

    wild_tag_choice: OPCIONAL -- el tag que el jugador elige que representen
    sus tags "wild" en juego (ej. Research Coordination: "the wild tag
    counts as any tag of your choice when performing an action") para ESTE
    chequeo puntual. Solo afecta "min_tag_count" -- si `spec["tag"]` matchea
    `wild_tag_choice`, se suma `player["tags_played"].get("wild", 0)` al
    conteo de ese tag. None si el jugador no tiene tags "wild" o no los
    necesita para este requisito.

    Si `player` tiene el pasivo "global_requirements_tolerance_steps": N
    (ej. Adaptation Technology: N=2 -- "your global requirements are +2 or
    -2 steps, your choice in each case") y/o `pending_requirement_tolerance_steps`
    > 0 (version de un solo uso, ej. Special Design: +/-2 solo para la
    PROXIMA carta jugada -- ver apply_card_effect
    "next_card_requirement_tolerance_steps" y tools.play_card, que la
    consume despues de este chequeo), los umbrales de temperatura/oxigeno/
    oceanos se relajan esos pasos EN LA DIRECCION QUE FAVOREZCA al jugador
    (el juego real deja elegir +N o -N por requisito; como siempre conviene
    elegir la direccion favorable, el motor la aplica directo sin pedir la
    eleccion): baja los pisos "min_*" y sube los techos "max_*". Ambas
    fuentes se suman si el jugador tiene las dos activas a la vez.
    """
    if not requirements:
        return

    tolerance_steps = 0
    if player is not None:
        for effect in player["passive_effects"]:
            tolerance_steps = max(tolerance_steps, effect.get("global_requirements_tolerance_steps", 0))
        tolerance_steps += abs(player.get("pending_requirement_tolerance_steps", 0))
    temperature_tolerance = tolerance_steps * TEMPERATURE_STEP
    oxygen_tolerance = tolerance_steps * OXYGEN_STEP
    oceans_tolerance = tolerance_steps
    venus_tolerance = tolerance_steps * VENUS_STEP

    if "min_tag_count" in requirements:
        specs = requirements["min_tag_count"]
        if isinstance(specs, dict):
            specs = [specs]
        if player is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado del jugador (tags_played)"
            )
        for spec in specs:
            have = player["tags_played"].get(spec["tag"], 0)
            if wild_tag_choice == spec["tag"]:
                have += player["tags_played"].get("wild", 0)
            if have < spec["count"]:
                raise CardRequirementNotMetError(
                    f"Requiere {spec['count']} tags de '{spec['tag']}' jugados, hay {have}"
                )

    if "ruling_or_delegates" in requirements:
        spec = requirements["ruling_or_delegates"]
        party = spec["party"]
        min_delegates = spec.get("min_delegates", 2)
        if turmoil is None or player_id is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado de Turmoil y el player_id"
            )
        is_ruling = turmoil["ruling_party"] == party
        own_delegates = turmoil["parties"][party]["delegates"].get(player_id, 0)
        if not is_ruling and own_delegates < min_delegates:
            raise CardRequirementNotMetError(
                f"Requiere que '{party}' este gobernando o tener {min_delegates} delegados ahi, hay {own_delegates}"
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

    if "min_temperature" in requirements:
        threshold = requirements["min_temperature"] - temperature_tolerance
        if globals_["temperature"] < threshold:
            raise CardRequirementNotMetError(
                f"Requiere temperatura >= {threshold}C, hay {globals_['temperature']}C"
            )
    if "min_oxygen" in requirements:
        threshold = requirements["min_oxygen"] - oxygen_tolerance
        if globals_["oxygen"] < threshold:
            raise CardRequirementNotMetError(f"Requiere oxigeno >= {threshold}%, hay {globals_['oxygen']}%")
    if "min_oceans" in requirements:
        threshold = requirements["min_oceans"] - oceans_tolerance
        if globals_["oceans_placed"] < threshold:
            raise CardRequirementNotMetError(
                f"Requiere {threshold} oceanos colocados, hay {globals_['oceans_placed']}"
            )
    if "min_tr" in requirements:
        if player is None:
            raise CardRequirementNotMetError("Este requisito necesita el estado del jugador (TR)")
        if player["tr"] < requirements["min_tr"]:
            raise CardRequirementNotMetError(f"Requiere TR >= {requirements['min_tr']}, hay {player['tr']}")
    if "max_colonies_owned" in requirements:
        if player is None:
            raise CardRequirementNotMetError("Este requisito necesita el estado del jugador (colonias)")
        have = len(player["colonies_owned"])
        if have > requirements["max_colonies_owned"]:
            raise CardRequirementNotMetError(
                f"Requiere maximo {requirements['max_colonies_owned']} colonias propias, hay {have}"
            )
    if "min_colonies_owned" in requirements:
        if player is None:
            raise CardRequirementNotMetError("Este requisito necesita el estado del jugador (colonias)")
        have = len(player["colonies_owned"])
        if have < requirements["min_colonies_owned"]:
            raise CardRequirementNotMetError(
                f"Requiere al menos {requirements['min_colonies_owned']} colonias propias, hay {have}"
            )
    if "min_venus" in requirements:
        threshold = requirements["min_venus"] - venus_tolerance
        if globals_["venus"] < threshold:
            raise CardRequirementNotMetError(f"Requiere Venus >= {threshold}%, hay {globals_['venus']}%")
    if "max_venus" in requirements:
        threshold = requirements["max_venus"] + venus_tolerance
        if globals_["venus"] > threshold:
            raise CardRequirementNotMetError(f"Requiere Venus <= {threshold}%, hay {globals_['venus']}%")
    if "min_city_tiles" in requirements and globals_["city_tiles_placed"] < requirements["min_city_tiles"]:
        raise CardRequirementNotMetError(
            f"Requiere {requirements['min_city_tiles']} ciudades en juego, "
            f"hay {globals_['city_tiles_placed']}"
        )
    if "max_oceans" in requirements:
        threshold = requirements["max_oceans"] + oceans_tolerance
        if globals_["oceans_placed"] > threshold:
            raise CardRequirementNotMetError(
                f"Requiere maximo {threshold} oceanos colocados, hay {globals_['oceans_placed']}"
            )
    if "max_temperature" in requirements:
        threshold = requirements["max_temperature"] + temperature_tolerance
        if globals_["temperature"] > threshold:
            raise CardRequirementNotMetError(
                f"Requiere temperatura <= {threshold}C, hay {globals_['temperature']}C"
            )
    if "max_oxygen" in requirements:
        threshold = requirements["max_oxygen"] + oxygen_tolerance
        if globals_["oxygen"] > threshold:
            raise CardRequirementNotMetError(f"Requiere oxigeno <= {threshold}%, hay {globals_['oxygen']}%")


def apply_card_effect(
    player: PlayerState,
    globals_: GlobalParameters,
    effects: dict,
    effect_amount: int | None = None,
    effect_choice: int | None = None,
    target_card_id: str | None = None,
    target_card_id_2: str | None = None,
    discard_card_id: str | None = None,
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
      - "raise_venus_steps": N -- sube el Venus scale N pasos (+N TR, mas los
        bonus de umbral, ver raise_venus). Expansion Venus Next.
      - "trade_fleet_delta": N -- suma N a `player["trade_fleets"]` (expansion
        Colonies, ej. Sky Docks, Space Port: +1 flota de comercio).
      - "draw_cards_per_tag": {"tag": "<tag>", "tags_per_step": N (default 1),
        "cards_per_step": N (default 1), "include_this": bool} -- roba tantas
        cartas como pasos de `tags_per_step` tags ya jugados (division
        entera, igual que production_delta_per_tag pero para robar cartas
        en vez de subir produccion) (ej. Solar Probe: 1 carta cada 3 tags
        de ciencia, incluida esta).
      - "discard_card_then_draw": {"draw": N} -- descarta `discard_card_id`
        (OBLIGATORIO, debe estar en la mano) y roba N cartas del mazo (ej.
        Sponsored Academies: descartar 1, robar 3). La clausula "each
        opponent draws 1" del texto real se omite -- no afecta el estado del
        propio jugador en single-player, no hace falta modelarla.
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
      - "start_research": {"n": N} -- roba N cartas a pending_research como
        efecto inmediato al jugar la carta (ej. Business Contacts: n=4,
        despues se resuelve con resolve_research_phase(cost_per_card=0,
        max_take=2) porque el texto exige tomar EXACTAMENTE 2 de las 4).
        Mismo mecanismo que use_card_action.gains.start_research, pero
        disparado al jugar la carta en vez de por una accion repetible.
      - "next_card_discount_mc": N -- suma N a `player.pending_mc_discount`,
        que tools.play_card resta del costo efectivo de la PROXIMA carta
        que el jugador juegue esta generacion (ej. Indentured Workers: -8
        MC). Se consume al jugar esa siguiente carta, la cubra entera o
        no, y tambien se pierde si termina la generacion sin usarse
        (run_production_phase lo resetea a 0).
      - "next_card_requirement_tolerance_steps": N -- analogo, pero suma N
        (en valor absoluto) a `player.pending_requirement_tolerance_steps`,
        que relaja los requisitos de temperatura/oxigeno/oceanos de la
        PROXIMA carta jugada esta generacion (ej. Special Design: N=2,
        "+2 or -2, your choice" -- el motor siempre aplica la direccion
        favorable, ver check_card_requirements). tools.play_card lo
        consume despues de chequear los requisitos de esa carta.
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
        de la carta actual. Acepta tambien una LISTA de specs (igual que
        min_tag_count en check_card_requirements) para sumar por mas de un
        tag a la vez (ej. Gyropolis: +1 produccion de MC por cada tag venus
        Y +1 por cada tag earth, en la misma carta).
      - "production_delta_per_colony": {"production": "<recurso>_production",
        "per_colony": N (default 1)} -- suma N por cada colonia que el
        jugador ya construyo (`player["colonies_owned"]`, expansion
        Colonies, ver colonies.py) (ej. Ecology Research: +1 produccion de
        plantas por cada colonia propia).
      - "resource_delta_per_colony": {"resource": "<recurso>", "per_colony":
        N (default 1)} -- igual que production_delta_per_colony pero suma
        al STOCK del recurso en vez de a su produccion (ej. Ceres Tech
        Market: +2 MC de stock por cada colonia propia).
      - "production_delta_per_tag_pair": {"tag_a": "<tag>", "tag_b": "<tag>",
        "production": "<recurso>_production", "per_set": N (default 1)} --
        suma N por cada PAR completo de tags "<tag_a>"+"<tag_b>" ya jugados
        (el minimo de los dos conteos, no la suma) (ej. Cloud Tourism: +1
        produccion de MC por cada set de tag earth Y tag venus que tenga).
      - "production_delta_per_zero_tag_card": {"production": "<recurso>_production",
        "per_card": N (default 1), "include_this": bool} -- suma N por cada
        carta jugada SIN NINGUN tag (`zero_tag_cards_played`, incluida esta
        si `include_this` es true) (ej. Community Services: +1 produccion
        de MC por cada carta sin tags, incluida ella misma). Distinto de
        production_delta_per_tag porque no hay un tag que contar -- lee
        `zero_tag_cards_played` en vez de `tags_played`.
      - "tr_delta_per_tag": {"tag": "<tag>", "per_tag": N (default 1),
        "include_this": bool} -- igual que production_delta_per_tag pero
        sube el TR directo en vez de una produccion (ej. Terraforming
        Ganymede: +1 TR por cada tag jovian jugado, incluido este).
      - "target_card_resource_delta": N -- agrega N recursos a OTRA carta
        activa del jugador, elegida via el parametro `target_card_id` (no un
        sub-efecto de choice; casi siempre aparece dentro de una rama de
        "choice", ej. Local Heat Trapping: agregar 3 recursos a una carta
        animal/microbio propia; Eos Chasma National Park: agregar 1 animal a
        cualquier carta animal propia). Mismo mecanismo que
        use_card_action.gains.target_card_resource_delta, pero como efecto
        inmediato al jugar la carta (a diferencia de la version de
        use_card_action, aca no se valida "no apuntar a si misma" porque
        esta funcion no recibe el card_id de la carta que dispara el
        efecto -- tools.play_card ya registro esa carta como activa/pasiva
        ANTES de llamar aca, precisamente para que pasivos "se dispara al
        colocar X, incluida esta" se autodisparen con su propia colocacion).
        Lanza CardEffectError si falta target_card_id o si la carta objetivo
        no esta activa para este jugador.
      - "target_min_resources": N -- opcional, junto a target_card_resource_delta;
        exige que la carta objetivo YA tenga al menos N recursos antes de
        aplicar el delta (ej. CEO's Favorite Project: "add 1 resource to a
        card with at least 1 resource on it" -- target_min_resources: 1).
        Lanza CardEffectError si no se cumple.
      - "target_card_resource_delta_2": N -- igual que target_card_resource_delta
        pero para una SEGUNDA carta objetivo distinta, via el parametro
        `target_card_id_2` (ej. Imported Nitrogen: agregar 3 microbios a una
        carta y 2 animales a OTRA carta distinta, en la misma jugada). Sin
        target_min_resources propio -- si algun dia una carta lo necesita,
        agregar target_min_resources_2 en vez de generalizar de mas.
      - "target_card_resource_delta_per_tag": {"tag": "<tag>", "per_tag": N
        (default 1), "include_this": bool} -- combina target_card_resource_delta
        con production_delta_per_tag: agrega a OTRA carta activa (via
        `target_card_id`) tantos recursos como N por cada tag "<tag>" ya
        jugado (ej. Hydrogen to Venus: +1 floater a una carta Venus por cada
        tag jovian). Si el conteo da 0, no hace nada y NO exige
        target_card_id (jugar la carta sigue siendo legal sin tags jovian).

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
        return apply_card_effect(
            player, globals_, options[effect_choice], effect_amount,
            target_card_id=target_card_id, target_card_id_2=target_card_id_2,
        )

    if "tag_count_choice" in effects:
        spec = effects["tag_count_choice"]
        have = player["tags_played"].get(spec["tag"], 0)
        branch = spec["if_met"] if have >= spec["count"] else spec["else"]
        return apply_card_effect(
            player, globals_, branch, effect_amount,
            target_card_id=target_card_id, target_card_id_2=target_card_id_2,
        )

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
        specs = effects["production_delta_per_tag"]
        if isinstance(specs, dict):
            specs = [specs]
        for spec in specs:
            key = spec["production"]
            count = player["tags_played"].get(spec["tag"], 0)
            if spec.get("include_this"):
                count += 1
            tags_per_step = spec.get("tags_per_step", 1)
            per_step = spec.get("per_step", spec.get("per_tag", 1))
            delta = (count // tags_per_step) * per_step
            new_player[key] = _apply_production_floor(key, new_player[key] + delta)

    if "tr_delta_per_tag" in effects:
        spec = effects["tr_delta_per_tag"]
        count = player["tags_played"].get(spec["tag"], 0)
        if spec.get("include_this"):
            count += 1
        new_player["tr"] = new_player["tr"] + count * spec.get("per_tag", 1)

    if "production_delta_per_colony" in effects:
        spec = effects["production_delta_per_colony"]
        key = spec["production"]
        count = len(player["colonies_owned"])
        new_player[key] = _apply_production_floor(key, new_player[key] + count * spec.get("per_colony", 1))

    if "resource_delta_per_colony" in effects:
        spec = effects["resource_delta_per_colony"]
        key = spec["resource"]
        count = len(player["colonies_owned"])
        new_player[key] = max(0, new_player[key] + count * spec.get("per_colony", 1))

    if "production_delta_per_tag_pair" in effects:
        spec = effects["production_delta_per_tag_pair"]
        key = spec["production"]
        count_a = player["tags_played"].get(spec["tag_a"], 0)
        count_b = player["tags_played"].get(spec["tag_b"], 0)
        sets = min(count_a, count_b)
        new_player[key] = _apply_production_floor(key, new_player[key] + sets * spec.get("per_set", 1))

    if "production_delta_per_zero_tag_card" in effects:
        spec = effects["production_delta_per_zero_tag_card"]
        key = spec["production"]
        count = player["zero_tag_cards_played"]
        if spec.get("include_this"):
            count += 1
        new_player[key] = _apply_production_floor(key, new_player[key] + count * spec.get("per_card", 1))

    if "production_delta_per_counter" in effects:
        spec = effects["production_delta_per_counter"]
        key = spec["production"]
        count = globals_[spec["counter"]]
        delta = count * spec.get("per_counter", 1)
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

    if "raise_venus_steps" in effects:
        p2, g2 = raise_venus(
            PlayerState(**new_player), GlobalParameters(**new_globals),  # type: ignore[typeddict-item]
            steps=effects["raise_venus_steps"],
        )
        new_player, new_globals = dict(p2), dict(g2)

    if "trade_fleet_delta" in effects:
        new_player["trade_fleets"] = new_player["trade_fleets"] + effects["trade_fleet_delta"]

    if "draw_cards_per_tag" in effects:
        spec = effects["draw_cards_per_tag"]
        count = player["tags_played"].get(spec["tag"], 0)
        if spec.get("include_this"):
            count += 1
        tags_per_step = spec.get("tags_per_step", 1)
        cards = (count // tags_per_step) * spec.get("cards_per_step", 1)
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), cards))  # type: ignore[typeddict-item]

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

    if "discard_card_then_draw" in effects:
        spec = effects["discard_card_then_draw"]
        if discard_card_id is None:
            raise CardEffectError("Esta carta requiere discard_card_id")
        new_player = dict(remove_card_from_hand(PlayerState(**new_player), discard_card_id))  # type: ignore[typeddict-item]
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), spec["draw"]))  # type: ignore[typeddict-item]

    if "start_research" in effects:
        new_player = dict(start_research_phase(PlayerState(**new_player), effects["start_research"]["n"]))  # type: ignore[typeddict-item]

    if "next_card_discount_mc" in effects:
        new_player["pending_mc_discount"] = new_player["pending_mc_discount"] + effects["next_card_discount_mc"]

    if "next_card_requirement_tolerance_steps" in effects:
        new_player["pending_requirement_tolerance_steps"] = (
            new_player["pending_requirement_tolerance_steps"]
            + abs(effects["next_card_requirement_tolerance_steps"])
        )

    if "target_card_resource_delta" in effects:
        amount = effects["target_card_resource_delta"]
        if target_card_id is None:
            raise CardEffectError("Esta carta requiere target_card_id")
        active_cards = new_player["active_cards"]
        if target_card_id not in active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        min_target_resources = effects.get("target_min_resources")
        if min_target_resources is not None and active_cards[target_card_id]["resources"] < min_target_resources:
            raise CardEffectError(
                f"'{target_card_id}' tiene {active_cards[target_card_id]['resources']} recursos, "
                f"se necesitan al menos {min_target_resources}"
            )
        new_active_cards = dict(active_cards)
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id],
            "resources": max(0, new_active_cards[target_card_id]["resources"] + amount),
        }
        new_player["active_cards"] = new_active_cards

    if "target_card_resource_delta_2" in effects:
        amount = effects["target_card_resource_delta_2"]
        if target_card_id_2 is None:
            raise CardEffectError("Esta carta requiere target_card_id_2")
        active_cards = new_player["active_cards"]
        if target_card_id_2 not in active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id_2}' no esta activa para este jugador")
        new_active_cards = dict(active_cards)
        new_active_cards[target_card_id_2] = {
            **new_active_cards[target_card_id_2],
            "resources": max(0, new_active_cards[target_card_id_2]["resources"] + amount),
        }
        new_player["active_cards"] = new_active_cards

    if "target_card_resource_delta_per_tag" in effects:
        spec = effects["target_card_resource_delta_per_tag"]
        count = player["tags_played"].get(spec["tag"], 0)
        if spec.get("include_this"):
            count += 1
        amount = count * spec.get("per_tag", 1)
        if amount > 0:
            if target_card_id is None:
                raise CardEffectError("Esta carta requiere target_card_id")
            active_cards = new_player["active_cards"]
            if target_card_id not in active_cards:
                raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
            new_active_cards = dict(active_cards)
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": max(0, new_active_cards[target_card_id]["resources"] + amount),
            }
            new_player["active_cards"] = new_active_cards

    return PlayerState(**new_player), GlobalParameters(**new_globals)  # type: ignore[typeddict-item]


# ---------------------------------------------------------------------------
# Cartas activas: accion repetible (una vez por generacion) y/o recursos
# propios de la carta (ej. Ironworks: accion; Regolith Eaters: accion +
# microbios guardados en la carta)
# ---------------------------------------------------------------------------

def register_active_card(player: PlayerState, card_id: str, initial_resources: int = 0) -> PlayerState:
    """
    Marca una carta recien jugada como "activa" -- queda en juego frente al
    jugador porque tiene una accion repetible y/o guarda recursos propios.
    Se llama despues de pagar la carta, solo si `effects.becomes_active` es
    true en su fila de `cards`. Si la carta ya estaba activa (no deberia
    pasar, cada carta se juega una vez), reinicia sus contadores.

    initial_resources: N > 0 si la carta arranca con recursos propios ya
    puestos, sin depender de un trigger (ej. Herbivores: "Add 1 animal to
    this card" al jugarse -- a diferencia de Ecological Zone/Decomposers,
    que arrancan con recursos via su propio pasivo "on_tag_played_add_resource"
    autodisparado por su propio tag). Viene de `effects.active_card_starting_resources`
    en la fila de `cards`, leido por tools.play_card.
    """
    new_active_cards = dict(player["active_cards"])
    new_active_cards[card_id] = {"resources": initial_resources, "action_used": False}
    return {**player, "active_cards": new_active_cards}


def spend_active_card_resource(player: PlayerState, card_id: str, amount: int) -> PlayerState:
    """
    Descuenta `amount` recursos guardados en una carta activa (`card_id`).
    Lanza InsufficientResourcesError si no alcanza. Usado por tools.play_card
    para pagar con el recurso guardado en una carta (ej. Dirigibles: floaters
    valen 3 M€ para cartas Venus; Psychrophiles: microbios valen 2 M€ para
    cartas plant -- ver pasivo "card_resource_payment" en
    register_passive_effect), distinto de move_from_target_card_resource_delta
    (ese mueve recursos de una carta a OTRA carta, no los gasta como pago).
    """
    current = player["active_cards"][card_id]["resources"]
    if current < amount:
        raise InsufficientResourcesError(
            f"'{card_id}' tiene {current} recurso(s) guardado(s), se necesitan {amount}"
        )
    new_active_cards = {
        **player["active_cards"],
        card_id: {**player["active_cards"][card_id], "resources": current - amount},
    }
    return {**player, "active_cards": new_active_cards}


def use_card_action(
    player: PlayerState,
    globals_: GlobalParameters,
    card_id: str,
    action_spec: dict,
    effect_choice: int | None = None,
    target_card_id: str | None = None,
    effect_amount: int | None = None,
    reserved_card_id: str | None = None,
    titanium_to_pay: int = 0,
) -> tuple[PlayerState, GlobalParameters]:
    """
    Ejecuta la accion repetible de una carta activa (columna `effects.action`
    en `cards`). Vocabulario de `action_spec`:

      - "convert_resource_amount": {"from": "<recurso>", "to": "<recurso>",
        "ratio": N (default 1)} -- convierte `effect_amount` (X, elegido por
        el jugador) unidades de stock de un recurso a X*ratio del otro,
        limitado al stock disponible (ej. Power Infrastructure: gastar
        cualquier cantidad de energia para ganar esa cantidad de MC). A
        diferencia de "convert_production" (apply_card_effect, convierte
        PRODUCCION), esta convierte STOCK. Lanza CardEffectError si falta
        effect_amount o es negativo, InsufficientResourcesError si no hay
        suficiente stock del recurso origen.
      - "convert_card_resource_amount": {"to": "<recurso>", "ratio": N
        (default 1)} -- igual que convert_resource_amount, pero el origen es
        SIEMPRE el recurso guardado en la propia carta (no stock del
        jugador): gasta `effect_amount` (X) recursos de la carta y gana X*ratio
        del recurso `to` (ej. Sulphur-Eating Bacteria: gastar X microbios
        guardados para ganar 3X MC). Mismos errores que convert_resource_amount.
      - "cost": {"<recurso>": N, ...} -- recursos de stock del jugador que se
        gastan (ej. Ironworks: {"energy": 4}). La clave especial
        "mc_or_titanium": N -- cuesta N MC, pero el jugador puede cubrir
        parte o todo con titanio (parametro `titanium_to_pay`, valorizado
        igual que al pagar cartas -- ver compute_conversion_rates, asi
        Advanced Alloys tambien lo beneficia) (ej. Rotator Impacts: 6 MC,
        "titanium may be used"). Otra clave especial
        "card_resource" gasta N recursos guardados en la propia carta (ej.
        Regolith Eaters: remover 2 microbios).
      - "gains": {"resource_deltas": {...}, "production_deltas": {...},
        "raise_oxygen_steps": N, "raise_temperature_steps": N, "raise_venus_steps": N,
        "card_resource_delta": N, "target_card_resource_delta": N,
        "move_from_target_card_resource_delta": N, "tr_delta": N,
        "mc_per_counter": "<nombre del contador en GlobalParameters>"} -- N > 0 en
        card_resource_delta agrega recursos a la propia carta (ej. Regolith
        Eaters: agregar 1 microbio); target_card_resource_delta agrega N recursos
        a OTRA carta activa (ej. Symbiotic Fungus: 1 microbio; Extreme-Cold Fungus: 2);
        move_from_target_card_resource_delta MUEVE N recursos desde OTRA carta
        activa (`target_card_id`, debe tener al menos N) hacia la propia carta
        (ej. Predators: mover 1 animal; Ants: mover 1 microbio) -- a diferencia
        de target_card_resource_delta, esta resta del origen ademas de sumar
        al destino; "target_card_resource_delta_allow_self": N -- igual que
        target_card_resource_delta pero el jugador puede elegir CUALQUIER
        carta activa como destino, incluida la propia (`target_card_id` es
        opcional -- si se omite, agrega a la propia carta) (ej. Dirigibles:
        "Add 1 floater to ANY card"); tr_delta sube el TR directo sin pasar por un parametro global (ej.
        Equatorial Magnetizer); mc_per_counter da tanto MC como valga ese
        contador global (ej. Martian Rails: MC por cada ciudad en Marte via
        "city_tiles_placed"); place_oceans: N coloca N tiles de oceano (+N TR
        cada uno) (ej. Water Import from Europa); draw_cards: N roba N cartas
        del mazo directo a la mano, sin fase de investigacion (ej. Development
        Center); start_research: {"n": N} roba N cartas a pending_research -- el
        jugador todavia tiene que resolver la compra por separado con
        resolve_research_phase (tipicamente a costo 0, ej. Inventors' Guild: n=1).
        "mc_per_card_resource": {"per_resource": N (default 1), "cap": M
        (opcional)} -- da tanto MC como recursos guardados en la propia
        carta, SIN gastarlos (a diferencia de convert_card_resource_amount,
        que si los gasta), limitado a `cap` si esta presente (ej. Jupiter
        Floating Station: 1 MC por floater guardado, maximo 4).
        "mc_per_discarded_card": {"per_card": N (default 1)} -- da N MC por
        cada carta que el jugador declara descartar (`effect_amount` = X,
        elegido por el jugador). Igual que standard_project_sell_patents,
        NO valida ni saca cartas puntuales de `hand` -- confia en el X
        declarado (ej. Ceres Tech Market: 2 MC por carta).
        "free_trade": true -- NO se procesa aca (este motor no conoce
        colonies.py a proposito, ver CLAUDE.md seccion 3): es un flag que
        `tools.use_card_action` detecta ANTES de llamar a esta funcion,
        para comerciar sin cobrar el costo normal de comerciar despues de
        que esta funcion resuelva el "cost" propio de la accion (ej. gastar
        1 floater guardado) (ej. Titan Floating Launch-Pad: "spend 1
        floater here to trade for free"). Ver tools.use_card_action,
        parametro `trade_colony_id`.
        "reserve_card_from_hand": {"initial_resources": N (default 2)} --
        reserva `reserved_card_id` (obligatorio, debe estar en la mano)
        sobre la propia carta, ver reserve_card_in_slot (ej. Self-
        Replicating Robots). "duplicate_reserved_card": true -- duplica los
        recursos de `reserved_card_id` (obligatorio, ya reservada), ver
        duplicate_reserved_card_resources (ej. Self-Replicating Robots,
        opcion alternativa de la misma accion).
      - "choice": lista de action_spec alternativos; se elige uno con
        `effect_choice` (ej. Regolith Eaters: agregar microbio O gastar 2
        para subir oxigeno; Extreme-Cold Fungus: ganar 1 planta O 2 microbios a otra carta).

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

    if "convert_card_resource_amount" in action_spec:
        spec = action_spec["convert_card_resource_amount"]
        to_key = spec["to"]
        if effect_amount is None or effect_amount < 0:
            raise CardEffectError("Esta accion requiere effect_amount (X) >= 0")
        if card_resources < effect_amount:
            raise InsufficientResourcesError(
                f"'{card_id}' tiene {card_resources} recursos guardados, se necesitan {effect_amount}"
            )
        card_resources -= effect_amount
        new_player[to_key] = new_player[to_key] + effect_amount * spec.get("ratio", 1)
        new_active_cards[card_id] = {"resources": card_resources, "action_used": True}
        new_player["active_cards"] = new_active_cards
        return PlayerState(**new_player), globals_  # type: ignore[typeddict-item]

    if "convert_resource_amount" in action_spec:
        spec = action_spec["convert_resource_amount"]
        from_key, to_key = spec["from"], spec["to"]
        if effect_amount is None or effect_amount < 0:
            raise CardEffectError("Esta accion requiere effect_amount (X) >= 0")
        if new_player[from_key] < effect_amount:
            raise InsufficientResourcesError(
                f"No hay suficiente {from_key} ({new_player[from_key]}) para convertir {effect_amount}"
            )
        new_player[from_key] -= effect_amount
        new_player[to_key] += effect_amount * spec.get("ratio", 1)
        new_active_cards[card_id] = {"resources": card_resources, "action_used": True}
        new_player["active_cards"] = new_active_cards
        return PlayerState(**new_player), globals_  # type: ignore[typeddict-item]

    for key, amount in action_spec.get("cost", {}).items():
        if key == "card_resource":
            if card_resources < amount:
                raise InsufficientResourcesError(
                    f"'{card_id}' tiene {card_resources} recursos guardados, se necesitan {amount}"
                )
            card_resources -= amount
        elif key == "mc_or_titanium":
            if titanium_to_pay < 0:
                raise CardEffectError("titanium_to_pay no puede ser negativo")
            if new_player["titanium"] < titanium_to_pay:
                raise InsufficientResourcesError(
                    f"Se necesita {titanium_to_pay} de titanio, hay {new_player['titanium']}"
                )
            _, titanium_value_mc = compute_conversion_rates(PlayerState(**new_player))  # type: ignore[typeddict-item]
            mc_needed = max(0, amount - titanium_to_pay * titanium_value_mc)
            if new_player["mc"] < mc_needed:
                raise InsufficientResourcesError(f"Se necesita {mc_needed} de MC, hay {new_player['mc']}")
            new_player["titanium"] -= titanium_to_pay
            new_player["mc"] -= mc_needed
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
    if "target_card_resource_delta" in gains:
        amount = gains["target_card_resource_delta"]
        if target_card_id is None:
            raise CardEffectError(f"La accion de '{card_id}' requiere target_card_id")
        if target_card_id == card_id:
            raise CardEffectError(f"La accion de '{card_id}' debe agregar recursos a OTRA carta, no a si misma")
        if target_card_id not in new_active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id],
            "resources": max(0, new_active_cards[target_card_id]["resources"] + amount),
        }
    if "target_card_resource_delta_allow_self" in gains:
        amount = gains["target_card_resource_delta_allow_self"]
        dest_id = target_card_id if target_card_id is not None else card_id
        if dest_id == card_id:
            card_resources = max(0, card_resources + amount)
        else:
            if dest_id not in new_active_cards:
                raise CardEffectError(f"La carta objetivo '{dest_id}' no esta activa para este jugador")
            new_active_cards[dest_id] = {
                **new_active_cards[dest_id],
                "resources": max(0, new_active_cards[dest_id]["resources"] + amount),
            }
    if "move_from_target_card_resource_delta" in gains:
        amount = gains["move_from_target_card_resource_delta"]
        if target_card_id is None:
            raise CardEffectError(f"La accion de '{card_id}' requiere target_card_id")
        if target_card_id == card_id:
            raise CardEffectError(f"La accion de '{card_id}' debe mover recursos desde OTRA carta, no desde si misma")
        if target_card_id not in new_active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        source_resources = new_active_cards[target_card_id]["resources"]
        if source_resources < amount:
            raise InsufficientResourcesError(
                f"'{target_card_id}' tiene {source_resources} recursos guardados, se necesitan {amount}"
            )
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id],
            "resources": source_resources - amount,
        }
        card_resources = card_resources + amount
    if "raise_oxygen_steps" in gains:
        p2, g2 = raise_oxygen(PlayerState(**new_player), GlobalParameters(**new_globals), steps=gains["raise_oxygen_steps"])  # type: ignore[typeddict-item]
        new_player, new_globals = dict(p2), dict(g2)
    if "raise_temperature_steps" in gains:
        p2, g2 = raise_temperature(PlayerState(**new_player), GlobalParameters(**new_globals), steps=gains["raise_temperature_steps"])  # type: ignore[typeddict-item]
        new_player, new_globals = dict(p2), dict(g2)
    if "raise_venus_steps" in gains:
        p2, g2 = raise_venus(PlayerState(**new_player), GlobalParameters(**new_globals), steps=gains["raise_venus_steps"])  # type: ignore[typeddict-item]
        new_player, new_globals = dict(p2), dict(g2)
    if "tr_delta" in gains:
        new_player["tr"] = new_player["tr"] + gains["tr_delta"]
    if "mc_per_counter" in gains:
        new_player["mc"] = new_player["mc"] + new_globals[gains["mc_per_counter"]]
    if "mc_per_card_resource" in gains:
        spec = gains["mc_per_card_resource"]
        counted = min(card_resources, spec["cap"]) if "cap" in spec else card_resources
        new_player["mc"] = new_player["mc"] + counted * spec.get("per_resource", 1)
    if "mc_per_discarded_card" in gains:
        if effect_amount is None or effect_amount < 0:
            raise CardEffectError("Esta accion requiere effect_amount (X) >= 0")
        # Igual que standard_project_sell_patents: no se valida ni se saca
        # de `hand` una carta puntual, solo se otorga el MC declarado (el
        # jugador es quien elige cuantas descarta, el motor confia en X).
        new_player["mc"] = new_player["mc"] + effect_amount * gains["mc_per_discarded_card"].get("per_card", 1)
    if "place_oceans" in gains:
        for _ in range(gains["place_oceans"]):
            p2, g2 = place_ocean(PlayerState(**new_player), GlobalParameters(**new_globals))  # type: ignore[typeddict-item]
            new_player, new_globals = dict(p2), dict(g2)
    if "draw_cards" in gains:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), gains["draw_cards"]))  # type: ignore[typeddict-item]
    if "start_research" in gains:
        new_player = dict(start_research_phase(PlayerState(**new_player), gains["start_research"]["n"]))  # type: ignore[typeddict-item]
    if "reserve_card_from_hand" in gains:
        if reserved_card_id is None:
            raise CardEffectError(f"La accion de '{card_id}' requiere reserved_card_id")
        initial = gains["reserve_card_from_hand"].get("initial_resources", 2)
        new_player["active_cards"] = new_active_cards
        new_player = dict(reserve_card_in_slot(PlayerState(**new_player), card_id, reserved_card_id, initial))  # type: ignore[typeddict-item]
        new_active_cards = dict(new_player["active_cards"])
    if "duplicate_reserved_card" in gains:
        if reserved_card_id is None:
            raise CardEffectError(f"La accion de '{card_id}' requiere reserved_card_id")
        new_player = dict(duplicate_reserved_card_resources(PlayerState(**new_player), reserved_card_id))  # type: ignore[typeddict-item]

    new_active_cards[card_id] = {"resources": card_resources, "action_used": True}
    new_player["active_cards"] = new_active_cards

    return PlayerState(**new_player), GlobalParameters(**new_globals)  # type: ignore[typeddict-item]


# ---------------------------------------------------------------------------
# Tags jugados y efectos pasivos permanentes
# ---------------------------------------------------------------------------

def reserve_card_in_slot(
    player: PlayerState, holder_card_id: str, reserved_card_id: str, initial_resources: int = 2
) -> PlayerState:
    """
    Reserva `reserved_card_id` (debe estar en la mano) sobre la carta activa
    `holder_card_id` (ej. Self-Replicating Robots): la saca de la mano SIN
    jugarla ni pagarla, y le pone `initial_resources` recursos encima. Se
    diferencia de active_cards en que la carta reservada todavia no esta
    jugada -- no cuenta tags_played, no entra a played_cards, no dispara
    sus propios pasivos ni accion hasta que tools.play_card la juegue "como
    si estuviera en mano", con el costo reducido en la cantidad de recursos
    acumulados (ver compute_reserved_card_discount). El chequeo de que
    `reserved_card_id` tenga el tag que exige la carta contenedora (ej.
    space o building) es responsabilidad del caller (tools.py), que es
    quien tiene acceso al catalogo de cartas -- este motor no lo conoce.

    Lanza CardNotInHandError si no esta en la mano, CardEffectError si esa
    carta ya esta reservada.
    """
    if reserved_card_id not in player["hand"]:
        raise CardNotInHandError(f"'{reserved_card_id}' no esta en la mano, no se puede reservar")
    if reserved_card_id in player["reserved_cards"]:
        raise CardEffectError(f"'{reserved_card_id}' ya esta reservada")
    new_hand = [c for c in player["hand"] if c != reserved_card_id]
    new_reserved = {
        **player["reserved_cards"],
        reserved_card_id: {"resources": initial_resources, "holder_card_id": holder_card_id},
    }
    return {**player, "hand": new_hand, "reserved_cards": new_reserved}


def duplicate_reserved_card_resources(player: PlayerState, reserved_card_id: str) -> PlayerState:
    """
    Duplica los recursos acumulados sobre una carta ya reservada (ej. Self-
    Replicating Robots: en vez de reservar una carta nueva con la accion,
    duplica los recursos de una que ya tiene reservada). Lanza
    CardEffectError si `reserved_card_id` no esta reservada.
    """
    if reserved_card_id not in player["reserved_cards"]:
        raise CardEffectError(f"'{reserved_card_id}' no esta reservada")
    current = player["reserved_cards"][reserved_card_id]
    new_reserved = {
        **player["reserved_cards"],
        reserved_card_id: {**current, "resources": current["resources"] * 2},
    }
    return {**player, "reserved_cards": new_reserved}


def compute_reserved_card_discount(player: PlayerState, card_id: str) -> int:
    """
    MC de descuento por jugar `card_id` desde reserved_cards en vez de desde
    la mano -- igual a los recursos acumulados sobre ella (0 si no esta
    reservada). Ver tools.play_card: se suma al resto de descuentos antes
    de calcular el costo efectivo.
    """
    reserved = player["reserved_cards"].get(card_id)
    return reserved["resources"] if reserved is not None else 0


def release_reserved_card(player: PlayerState, card_id: str) -> PlayerState:
    """
    Saca `card_id` de reserved_cards una vez que tools.play_card la jugo
    (ya gasto su descuento, no queda mas rastro de la reserva). No-op si la
    carta no estaba reservada.
    """
    if card_id not in player["reserved_cards"]:
        return player
    new_reserved = {k: v for k, v in player["reserved_cards"].items() if k != card_id}
    return {**player, "reserved_cards": new_reserved}


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


def increment_zero_tag_cards_played(player: PlayerState, card_tags: tuple[str, ...]) -> PlayerState:
    """
    Suma 1 a `zero_tag_cards_played` si `card_tags` esta vacio (la carta no
    tiene ningun tag). Se llama junto a increment_tags_played en
    tools.play_card. Alimenta "production_delta_per_zero_tag_card" (ej.
    Community Services).
    """
    if card_tags:
        return player
    return {**player, "zero_tag_cards_played": player["zero_tag_cards_played"] + 1}


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
      - "on_standard_project_used": {"mc_delta": N} -- se suma cada vez que
        el jugador paga un proyecto estandar que no sea 'sell_patents' (ej.
        Standard Technology: +3 MC). Ver apply_standard_project_used_bonuses,
        llamado desde tools.use_standard_project.
      - "global_requirements_tolerance_steps": N -- relaja N pasos los
        requisitos de temperatura/oxigeno/oceanos de OTRAS cartas que el
        jugador quiera jugar despues (ej. Adaptation Technology: N=2). Ver
        check_card_requirements.
      - "trade_cost_discount": N -- descuenta N del costo de comerciar
        (expansion Colonies, 9 MC / 3 energia / 3 titanio, cualquiera sea
        el elegido) cada vez que el jugador usa tools.use_trade_fleet (ej.
        Cryo-Sleep: N=1). Ver compute_trade_cost_discount.
      - "trade_bump_track_first": true -- habilita el parametro
        `bump_track_first` de tools.use_trade_fleet (ej. Trade Envoys,
        Trading Colony: "when you trade, you may first increase that
        Colony Tile track 1 step").
      - "on_card_played_cost_threshold_draw": {"min_cost": N, "draw": M
        (default 1)} -- roba M cartas cada vez que el jugador juega
        (cualquier) carta cuyo costo IMPRESO (antes de descuentos) sea >= N
        (ej. Spin-Off Department: N=20). Chequeado en tools.play_card, que
        es quien tiene el costo impreso de la carta -- no hay funcion en
        rules_engine.py para este pasivo especifico.
      - "influence_bonus": N -- expansion Turmoil, suma N fijo a la
        Influencia calculada del jugador (ej. Colonial Representation:
        N=1, "you have influence +1"). Ver turmoil.compute_influence
        (parametro `bonus`), sumado por tools.get_player_state -- no hay
        funcion en rules_engine.py para este pasivo especifico porque la
        formula base de Influencia vive en turmoil.py, no en el motor
        puro (mismo criterio de decoupling que free_trade, ver seccion 3
        de CLAUDE.md).
      - "on_tag_played_add_resource": {"matching_tags": ["<tag>", ...], "resource_delta": N (default 1)}
        -- suma N recurso(s) a la propia carta activa cada vez que el jugador juega
        una carta con alguno de esos tags (ej. Ecological Zone: tags animal/plant;
        Decomposers: tags animal/plant/microbe).
      - "on_greenery_placed_add_resource": {"resource_delta": N (default 1)}
        -- suma N recurso(s) a la propia carta activa cada vez que el jugador
        coloca un tile de greenery, sea por proyecto estandar o por
        conversion de 8 plantas (ej. Herbivores: +1 animal). Ver
        apply_greenery_placed_bonuses, llamado desde
        tools._place_greenery_and_apply_bonus.
      - "on_city_tile_placed_add_resource": {"resource_delta": N (default 1)}
        -- igual que el de arriba pero disparado por colocar un tile de
        CIUDAD, de cualquier jugador (ej. Pets: +1 animal). Ver
        apply_city_placed_bonuses, llamado desde
        tools._place_city_and_apply_bonus.
      - "on_tag_played_may_swap_card": {"tag": "<tag>"} -- cada vez que el
        jugador juega CUALQUIER carta con ese tag (incluida la que registra
        el pasivo), puede opcionalmente descartar 1 carta de la mano para
        robar 1 del mazo (ej. Mars University: tag "science"). A diferencia
        de on_event_played (automatico), esto es una ELECCION del jugador --
        ver tools.play_card (parametro discard_for_draw_card_id) y
        rules_engine.player_has_tag_swap_passive / swap_card_for_draw.
      - "on_tag_played_choice": {"matching_tags": ["<tag>", ...],
        "add_resource_choice": {"resource_delta": N}, "spend_resource_choice":
        {"card_resource": N, "draw_cards": N}} -- similar a
        on_tag_played_may_swap_card (eleccion opcional del jugador, dispara
        con cualquier carta que tenga alguno de esos tags), pero en vez de
        descartar/robar, elige entre agregar recursos a la PROPIA carta
        activa o gastarlos para robar cartas del mazo (ej. Olympus
        Conference: tag "science", +1 recurso O gastar 1 para robar 1
        carta). Ver tools.play_card (parametro tag_played_choice) y
        rules_engine.apply_tag_played_choice.
      - "on_any_tag_played_choice": {"matching_tags": ["<tag>", ...],
        "add_resource_choice": {"resource_delta": N (default 1)},
        "gain_resource_choice": {"resource": "<recurso>", "amount": N
        (default 1)}} -- distinto de on_tag_played_choice: el target del
        "add" no es la carta que tiene el pasivo, sino la CARTA RECIEN
        JUGADA que disparo el match (debe estar en active_cards, es decir
        tener caja de recursos). Dispara con cualquier carta jugada que
        tenga alguno de esos tags, incluida la que registra el pasivo (ej.
        Viral Enhancers: tags plant/microbe/animal, +1 recurso a la carta
        recien jugada O +1 planta para el jugador). Ver tools.play_card
        (parametro any_tag_played_choice) y
        rules_engine.apply_any_tag_played_choice.
      - "card_resource_payment": {"required_tag": "<tag>", "value_mc": N
        (default 3)} -- habilita pagar OTRAS cartas que tengan ese tag
        usando los recursos guardados en ESTA carta activa, a N M€ cada
        uno (ej. Dirigibles: floaters propios valen 3 M€ para cartas tag
        "venus"; Psychrophiles: microbios propios valen 2 M€ para cartas
        tag "plant"). Tercera moneda de pago cuyo stock vive en una carta,
        no en el jugador -- distinta de acero/titanio (que valen para
        cualquier carta con su tag, no dependen de una carta activa
        puntual). Ver tools.play_card (parametro card_resource_to_pay) y
        rules_engine.spend_active_card_resource.

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


def compute_trade_cost_discount(player: PlayerState) -> int:
    """
    Suma los descuentos "trade_cost_discount" de todos los efectos pasivos
    activos del jugador (ej. Cryo-Sleep: "when you trade, you pay 1 less
    resource for it" -- trade_cost_discount: 1). Se resta del costo de
    comerciar (9 MC / 3 energia / 3 titanio, cualquiera sea el elegido)
    antes de cobrarlo -- nunca deja el costo por debajo de 0. Ver
    tools.use_trade_fleet.
    """
    discount = 0
    for effect in player["passive_effects"]:
        discount += effect.get("trade_cost_discount", 0)
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


def apply_standard_project_used_bonuses(player: PlayerState, project_name: str) -> PlayerState:
    """
    Aplica el pasivo "on_standard_project_used": {"mc_delta": N} -- se suma
    cada vez que el jugador paga un proyecto estandar que NO sea
    'sell_patents' (ej. Standard Technology: +3 MC). Llamar desde
    tools.use_standard_project justo despues de resolver el proyecto.
    """
    if project_name == "sell_patents":
        return player
    new_player: dict = dict(player)
    for effect in player["passive_effects"]:
        bonus = effect.get("on_standard_project_used")
        if bonus is None:
            continue
        new_player["mc"] = new_player["mc"] + bonus.get("mc_delta", 0)
    return PlayerState(**new_player)  # type: ignore[typeddict-item]


def apply_tag_played_resource_bonuses(
    player: PlayerState, played_card_tags: tuple[str, ...] = ()
) -> PlayerState:
    """
    Aplica los bonus pasivos "on_tag_played_add_resource" (ej. Ecological Zone:
    +1 animal por cada tag animal/plant jugado; Decomposers: +1 microbio por
    cada tag animal/plant/microbe jugado).
    Suma resource_delta a la carta activa del jugador por cada tag coincidente.
    """
    new_active_cards = dict(player["active_cards"])
    changed = False
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_add_resource")
        if spec is None:
            continue
        target_card_id = effect["card_id"]
        if target_card_id not in new_active_cards:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        matches = sum(1 for t in played_card_tags if t in matching_tags)
        if matches > 0:
            current_res = new_active_cards[target_card_id]["resources"]
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": current_res + matches * spec.get("resource_delta", 1),
            }
            changed = True
    if not changed:
        return player
    return {**player, "active_cards": new_active_cards}


def apply_greenery_placed_bonuses(player: PlayerState) -> PlayerState:
    """
    Aplica el pasivo "on_greenery_placed_add_resource": {"resource_delta": N}
    -- suma N recursos a la propia carta activa cada vez que el jugador
    coloca un tile de greenery, sin importar la fuente (proyecto estandar o
    conversion de 8 plantas) (ej. Herbivores: +1 animal). Analogo a
    apply_tag_played_resource_bonuses pero disparado por "colocar greenery"
    en vez de "jugar un tag" -- llamado desde tools._place_greenery_and_apply_bonus,
    el unico punto donde confluyen ambos caminos que colocan greenery.
    """
    new_active_cards = dict(player["active_cards"])
    changed = False
    for effect in player["passive_effects"]:
        spec = effect.get("on_greenery_placed_add_resource")
        if spec is None:
            continue
        target_card_id = effect["card_id"]
        if target_card_id not in new_active_cards:
            continue
        current_res = new_active_cards[target_card_id]["resources"]
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id],
            "resources": current_res + spec.get("resource_delta", 1),
        }
        changed = True
    if not changed:
        return player
    return {**player, "active_cards": new_active_cards}


def apply_city_placed_bonuses(player: PlayerState) -> PlayerState:
    """
    Aplica los pasivos que disparan cada vez que se coloca un tile de
    CIUDAD en el mapa, sin importar de quien sea ni la fuente (proyecto
    estandar o una carta). Analogo a apply_greenery_placed_bonuses --
    llamado desde tools._place_city_and_apply_bonus, el unico punto donde
    confluyen todos los caminos que colocan una ciudad real en el tablero.
    Vocabulario:

      - "on_city_tile_placed_add_resource": {"resource_delta": N (default 1)}
        -- suma N recursos a la propia carta activa (ej. Pets: +1 animal).
      - "on_city_tile_placed_production_delta": {"production":
        "<recurso>_production", "per_tile": N (default 1)} -- sube esa
        produccion N pasos (ej. Immigrant City: +1 produccion MC, incluida
        su propia colocacion -- funciona porque tools.play_card registra
        la carta como activa/pasiva ANTES de colocar su ciudad).
    """
    new_active_cards = dict(player["active_cards"])
    new_player: dict = dict(player)
    changed = False
    for effect in player["passive_effects"]:
        resource_spec = effect.get("on_city_tile_placed_add_resource")
        if resource_spec is not None:
            target_card_id = effect["card_id"]
            if target_card_id in new_active_cards:
                current_res = new_active_cards[target_card_id]["resources"]
                new_active_cards[target_card_id] = {
                    **new_active_cards[target_card_id],
                    "resources": current_res + resource_spec.get("resource_delta", 1),
                }
                changed = True
        production_spec = effect.get("on_city_tile_placed_production_delta")
        if production_spec is not None:
            key = production_spec["production"]
            new_player[key] = _apply_production_floor(key, new_player[key] + production_spec.get("per_tile", 1))
            changed = True
    if not changed:
        return player
    new_player["active_cards"] = new_active_cards
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


def apply_tag_played_choice(
    player: PlayerState, played_card_tags: tuple[str, ...], choice: str | None
) -> PlayerState:
    """
    Aplica el pasivo "on_tag_played_choice": {"matching_tags": ["<tag>", ...],
    "add_resource_choice": {"resource_delta": N (default 1)},
    "spend_resource_choice": {"card_resource": N (default 1), "draw_cards": N
    (default 1)}} -- a diferencia de on_tag_played_add_resource (automatico,
    sin eleccion), esto dispara con cualquier carta que tenga alguno de esos
    tags (incluida la que registra el pasivo) y es una ELECCION OPCIONAL del
    jugador en el momento: "add" agrega recursos a la PROPIA carta activa
    (ej. Olympus Conference: +1 ciencia); "spend" gasta recursos guardados
    en la carta para robar cartas del mazo. None (no elegir) no hace nada --
    ver tools.play_card, parametro tag_played_choice.

    Si mas de un pasivo de este tipo matchea, se aplica el de la PRIMERA
    carta activa encontrada (en este motor solo hay una carta con este
    pasivo cargada hasta ahora, Olympus Conference).
    """
    if choice is None:
        return player
    new_active_cards = dict(player["active_cards"])
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_choice")
        if spec is None:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        if not matching_tags.intersection(played_card_tags):
            continue
        target_card_id = effect["card_id"]
        if target_card_id not in new_active_cards:
            continue
        if choice == "add":
            amount = spec.get("add_resource_choice", {}).get("resource_delta", 1)
            current_res = new_active_cards[target_card_id]["resources"]
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": current_res + amount,
            }
            return {**player, "active_cards": new_active_cards}
        if choice == "spend":
            spend_spec = spec.get("spend_resource_choice", {})
            amount = spend_spec.get("card_resource", 1)
            current_res = new_active_cards[target_card_id]["resources"]
            if current_res < amount:
                raise InsufficientResourcesError(
                    f"'{target_card_id}' tiene {current_res} recursos guardados, se necesitan {amount}"
                )
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": current_res - amount,
            }
            new_player = {**player, "active_cards": new_active_cards}
            return draw_cards_to_hand(new_player, spend_spec.get("draw_cards", 1))
        raise CardEffectError(f"choice invalido '{choice}', debe ser 'add' o 'spend'")
    return player


def apply_any_tag_played_choice(
    player: PlayerState, played_card_id: str, played_card_tags: tuple[str, ...], choice: str | None
) -> PlayerState:
    """
    Aplica el pasivo "on_any_tag_played_choice": {"matching_tags": ["<tag>",
    ...], "add_resource_choice": {"resource_delta": N (default 1)},
    "gain_resource_choice": {"resource": "<recurso>", "amount": N (default
    1)}} -- a diferencia de apply_tag_played_choice, el target de "add" es
    la CARTA RECIEN JUGADA (`played_card_id`), no la carta que registra el
    pasivo (ej. Viral Enhancers: +1 recurso a la carta que se acaba de
    jugar, O +1 planta para el jugador). None (no elegir) no hace nada --
    ver tools.play_card, parametro any_tag_played_choice.

    Si mas de un pasivo de este tipo matchea, se aplica el de la PRIMERA
    carta activa encontrada con este pasivo.
    """
    if choice is None:
        return player
    for effect in player["passive_effects"]:
        spec = effect.get("on_any_tag_played_choice")
        if spec is None:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        if not matching_tags.intersection(played_card_tags):
            continue
        if choice == "add":
            if played_card_id not in player["active_cards"]:
                raise CardEffectError(
                    f"'{played_card_id}' no tiene caja de recursos, no se le puede agregar recurso"
                )
            amount = spec.get("add_resource_choice", {}).get("resource_delta", 1)
            current_res = player["active_cards"][played_card_id]["resources"]
            new_active_cards = {
                **player["active_cards"],
                played_card_id: {
                    **player["active_cards"][played_card_id],
                    "resources": current_res + amount,
                },
            }
            return {**player, "active_cards": new_active_cards}
        if choice == "gain":
            gain_spec = spec.get("gain_resource_choice", {})
            resource = gain_spec["resource"]
            amount = gain_spec.get("amount", 1)
            return {**player, resource: player[resource] + amount}  # type: ignore[typeddict-item]
        raise CardEffectError(f"choice invalido '{choice}', debe ser 'add' o 'gain'")
    return player


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
    max_take: int | None = None,
) -> PlayerState:
    """
    Cierra una fase de investigacion iniciada con start_research_phase.
    `card_ids_to_buy` deben ser un subconjunto de `pending_research` -- esas
    se pagan a `cost_per_card` MC cada una (0 para acciones gratuitas como
    Inventors' Guild) y pasan a `hand`; el resto de `pending_research` se
    descarta (no vuelve al mazo). Siempre limpia `pending_research`, incluso
    si `card_ids_to_buy` esta vacio (comprar 0 cartas es una eleccion valida).

    `max_take`: tope explicito de cuantas se pueden tomar (ej. Business
    Contacts: "mira 4, toma EXACTAMENTE 2, descarta las otras 2" -- se pasa
    max_take=2 para que tomar de mas lance error en vez de permitirse en
    silencio). None (default) no impone tope, solo el MC disponible limita.

    Lanza ValueError si algun id en `card_ids_to_buy` no estaba en
    `pending_research`, o si supera `max_take`. Lanza
    InsufficientResourcesError si no alcanza el MC.
    """
    if max_take is not None and len(card_ids_to_buy) > max_take:
        raise ValueError(f"Como maximo se pueden tomar {max_take} cartas, se pidieron {len(card_ids_to_buy)}")

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
