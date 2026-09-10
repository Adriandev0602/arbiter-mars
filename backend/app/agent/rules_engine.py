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

    # Ofertas opcionales y PAGADAS que quedaron disparadas al colocar un
    # oceano y que el jugador todavia no resolvio (ej. Neptunian Power
    # Consultants). Se acumulan en place_ocean, se consumen con la tool
    # resolve_ocean_offer y se pierden al cerrar la generacion.
    pending_ocean_offers: int
    # True si el jugador subio su TR en lo que va de esta generacion.
    # Lo marca _raise_tr y lo limpia run_production_phase (ver ambas).
    tr_raised_this_generation: bool

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
        pending_mc_discount=0, pending_requirement_tolerance_steps=0, pending_ocean_offers=0,
        tr_raised_this_generation=False,
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
    """
    Sube la temperatura `steps` pasos (2 grados cada uno). +1 TR por paso aplicado.

    Tambien dispara el pasivo "on_temperature_raised" que el jugador tenga
    activo (ej. Homeostasis Bureau: +3 M€), UNA VEZ POR PASO APLICADO -- no
    por llamada: subir 2 pasos de una paga el bonus dos veces, y si la
    temperatura ya estaba al tope no paga nada, igual criterio que el TR.
    Mismo patron que on_ocean_placed en place_ocean.
    """
    if globals_["temperature"] >= TEMPERATURE_MAX:
        raise GlobalParameterMaxedError("La temperatura ya esta en su maximo (+8 C)")

    max_possible_steps = (TEMPERATURE_MAX - globals_["temperature"]) // TEMPERATURE_STEP
    applied_steps = min(steps, max_possible_steps)

    new_globals = {**globals_, "temperature": globals_["temperature"] + applied_steps * TEMPERATURE_STEP}
    new_player: dict = _raise_tr(dict(player), applied_steps)
    for effect in player["passive_effects"]:
        bonus = effect.get("on_temperature_raised")
        if bonus is None:
            continue
        new_player["mc"] = new_player["mc"] + bonus.get("mc_delta", 0) * applied_steps
        new_player["heat"] = new_player["heat"] + bonus.get("heat_delta", 0) * applied_steps
    return PlayerState(**new_player), new_globals  # type: ignore[typeddict-item]


def raise_oxygen(player: PlayerState, globals_: GlobalParameters, steps: int = 1) -> tuple[PlayerState, GlobalParameters]:
    """Sube el oxigeno `steps` pasos (1% cada uno). +1 TR por paso aplicado."""
    if globals_["oxygen"] >= OXYGEN_MAX:
        raise GlobalParameterMaxedError("El oxigeno ya esta en su maximo (14%)")

    max_possible_steps = min(steps, OXYGEN_MAX - globals_["oxygen"])

    new_globals = {**globals_, "oxygen": globals_["oxygen"] + max_possible_steps}
    new_player = _raise_tr(dict(player), max_possible_steps)
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
    new_player: dict = _raise_tr(dict(player), max_possible_steps)
    # Pasivo "on_venus_raised" (ej. Aphrodite: +2 M€ por PASO aplicado),
    # mismo patron que on_temperature_raised en raise_temperature: una vez
    # por paso realmente aplicado, cero si Venus ya estaba al tope.
    for effect in player["passive_effects"]:
        bonus = effect.get("on_venus_raised")
        if bonus is None:
            continue
        new_player["mc"] = new_player["mc"] + bonus.get("mc_delta", 0) * max_possible_steps
        new_player["heat"] = new_player["heat"] + bonus.get("heat_delta", 0) * max_possible_steps
    if before < VENUS_BONUS_STEP_DRAW_CARD <= after:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), 1))  # type: ignore[typeddict-item]
    if before < VENUS_BONUS_STEP_EXTRA_TR <= after:
        new_player = _raise_tr(new_player, 1)
    return PlayerState(**new_player), new_globals  # type: ignore[typeddict-item]


PARAMETERS_WITHOUT_BONUSES = ("temperature", "oxygen", "venus", "ocean")


def raise_global_parameter_without_bonuses(
    globals_: GlobalParameters, parameter: str,
) -> GlobalParameters:
    """
    Sube UN paso del parametro global `parameter` moviendo solo el contador:
    sin TR, sin los bonus de umbral de Venus y sin disparar ningun pasivo
    (on_temperature_raised, on_ocean_placed...).

    Es lo que pide World Government Advisor (P67, Prelude): "raise 1 global
    parameter WITHOUT GETTING ANY TR OR OTHER BONUSES". Por eso no toca al
    jugador y no reusa raise_temperature/raise_oxygen/raise_venus/place_ocean:
    todas esas SI otorgan TR y disparan pasivos, que es justo lo que la carta
    prohibe. Si el parametro ya esta al tope, levanta GlobalParameterMaxedError
    para que el jugador elija otro en vez de perder la accion.

    "ocean" aca solo mueve el contador `oceans_placed`; la eleccion del
    hexagono y el bonus de colocacion los resuelve tools.py, que es quien
    conoce el tablero -- y para esta carta ese bonus tampoco se cobra.
    """
    if parameter == "temperature":
        if globals_["temperature"] >= TEMPERATURE_MAX:
            raise GlobalParameterMaxedError("La temperatura ya esta en su maximo (+8 C)")
        return {**globals_, "temperature": globals_["temperature"] + TEMPERATURE_STEP}
    if parameter == "oxygen":
        if globals_["oxygen"] >= OXYGEN_MAX:
            raise GlobalParameterMaxedError("El oxigeno ya esta en su maximo (14%)")
        return {**globals_, "oxygen": globals_["oxygen"] + 1}
    if parameter == "venus":
        if globals_["venus"] >= VENUS_MAX:
            raise GlobalParameterMaxedError("El Venus scale ya esta en su maximo (30%)")
        return {**globals_, "venus": globals_["venus"] + VENUS_STEP}
    if parameter == "ocean":
        if globals_["oceans_placed"] >= OCEANS_MAX:
            raise GlobalParameterMaxedError("Ya se colocaron los 9 tiles de oceano")
        return {**globals_, "oceans_placed": globals_["oceans_placed"] + 1}
    raise CardEffectError(
        f"Parametro global desconocido: '{parameter}' (validos: {', '.join(PARAMETERS_WITHOUT_BONUSES)})"
    )


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
    new_player: dict = _raise_tr(dict(player), 1)
    for effect in player["passive_effects"]:
        bonus = effect.get("on_ocean_placed")
        if bonus is None:
            continue
        new_player["plants"] = new_player["plants"] + bonus.get("plants_delta", 0)
        # Lakefront Resorts: "when ANY ocean is placed, increase your M€
        # production 1 step" -- el mismo hook, pero sobre produccion.
        for key, delta in bonus.get("production_deltas", {}).items():
            new_player = _increase_production(new_player, key, delta)
        # Ofertas OPCIONALES y PAGADAS (ej. Neptunian Power Consultants: "you
        # MAY spend 5 M€ to raise energy production and add 1 hydroelectric
        # here"). No se pueden resolver aca -- necesitan que el jugador
        # decida y pague -- asi que se anotan como pendientes y se cobran
        # despues con la tool resolve_ocean_offer. Las que no se usen se
        # pierden al cerrar la generacion (run_production_phase las limpia).
    if any("on_ocean_placed_offer" in effect for effect in player["passive_effects"]):
        new_player["pending_ocean_offers"] = new_player["pending_ocean_offers"] + 1
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
    paid_player = {**player, "mc": player["mc"] - STANDARD_PROJECT_POWER_PLANT_COST}
    return _increase_production(paid_player, "energy_production", 1)


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

def plants_per_greenery(player: PlayerState) -> int:
    """
    Cuantas plantas le cuesta a ESTE jugador convertir a greenery. Por defecto
    PLANTS_PER_GREENERY (8), pero un pasivo "plants_per_greenery" puede
    bajarlo (ej. EcoLine: 7). Si hubiera varios, gana el mas barato.
    """
    cost = PLANTS_PER_GREENERY
    for effect in player["passive_effects"]:
        override = effect.get("plants_per_greenery")
        if override is not None:
            cost = min(cost, override)
    return cost


def convert_plants_to_greenery(player: PlayerState, globals_: GlobalParameters) -> tuple[PlayerState, GlobalParameters]:
    """Gasta 8 plantas (7 con EcoLine), coloca greenery, sube oxigeno 1 paso (+1 TR)."""
    cost = plants_per_greenery(player)
    if player["plants"] < cost:
        raise InsufficientResourcesError(
            f"Se necesitan {cost} plantas, hay {player['plants']}"
        )
    paid_player = {**player, "plants": player["plants"] - cost}
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

def player_has_optional_energy_to_heat(player: PlayerState) -> bool:
    """
    True si el jugador tiene el pasivo "optional_energy_to_heat" (ej.
    Supercapacitors, bloque 35: "converting energy to heat during production
    is optional for each energy resource"). Sin ese pasivo, la conversion es
    obligatoria y total, como manda la regla base.
    """
    return any(effect.get("optional_energy_to_heat") for effect in player["passive_effects"])


def run_production_phase(player: PlayerState, energy_to_convert: int | None = None) -> PlayerState:
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

    `energy_to_convert`: solo tiene sentido si el jugador tiene el pasivo
    "optional_energy_to_heat" (ver player_has_optional_energy_to_heat, ej.
    Supercapacitors) -- cuanta energia convertir a calor, unidad por unidad;
    la que no se convierte QUEDA en stock de energia para la generacion que
    viene. None (default) convierte todo, que es la regla base y lo unico
    legal sin ese pasivo. Lanza CardEffectError si se declara una cantidad
    sin tener el pasivo, o si no esta entre 0 y la energia disponible.
    """
    if energy_to_convert is None:
        energy_to_convert = player["energy"]
    else:
        if not player_has_optional_energy_to_heat(player):
            raise CardEffectError(
                "Convertir solo parte de la energia requiere un pasivo que lo habilite "
                "(ej. Supercapacitors); la regla base convierte toda la energia"
            )
        if not 0 <= energy_to_convert <= player["energy"]:
            raise CardEffectError(
                f"energy_to_convert debe estar entre 0 y {player['energy']}, se recibio {energy_to_convert}"
            )
    energy_kept = player["energy"] - energy_to_convert
    heat_after_energy_conversion = player["heat"] + energy_to_convert

    mc_income = player["tr"] + player["mc_production"]
    new_mc = max(0, player["mc"] + mc_income)

    reset_active_cards = {
        card_id: {**data, "action_used": False} for card_id, data in player["active_cards"].items()
    }

    # Pristar: "during production phase, if you did not get TR so far this
    # generation, add 1 preservation resource here and gain 6 M€". Se evalua
    # ACA, con el flag de ENTRADA (`player`, todavia sin resetear) -- si se
    # leyera despues del reset veria siempre False y el pasivo no pagaria
    # nunca, en silencio. Por eso el reset va al final, en el dict de retorno,
    # igual que pending_mc_discount y pending_ocean_offers.
    extra_mc = 0
    for effect in player["passive_effects"]:
        spec = effect.get("on_production_phase_if_tr_not_raised")
        if spec is None or player["tr_raised_this_generation"]:
            continue
        extra_mc += spec.get("mc_delta", 0)
        card_id = effect["card_id"]
        if spec.get("card_resource_delta") and card_id in reset_active_cards:
            reset_active_cards[card_id] = {
                **reset_active_cards[card_id],
                "resources": reset_active_cards[card_id]["resources"] + spec["card_resource_delta"],
            }

    return {
        **player,
        "mc": new_mc + extra_mc,
        "steel": player["steel"] + player["steel_production"],
        "titanium": player["titanium"] + player["titanium_production"],
        "plants": player["plants"] + player["plant_production"],
        # Sin pasivo: arranca de 0 tras la conversion, mas la produccion nueva.
        # Con Supercapacitors: la energia NO convertida tambien se conserva.
        "energy": energy_kept + player["energy_production"],
        "heat": heat_after_energy_conversion + player["heat_production"],
        "active_cards": reset_active_cards,
        "pending_mc_discount": 0,
        "pending_requirement_tolerance_steps": 0,
        "pending_ocean_offers": 0,
        # Arranca la generacion nueva sin TR subido (ver _raise_tr).
        "tr_raised_this_generation": False,
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


# Traduce cada campo "<recurso>_production" al campo de stock que corresponde
# (plants/plant es la unica irregularidad). Usado solo por _increase_production
# para saber que stock sumarle al pasivo "on_production_increased" (Manutech).
_PRODUCTION_STOCK_KEY = {
    "mc_production": "mc",
    "steel_production": "steel",
    "titanium_production": "titanium",
    "plant_production": "plants",
    "energy_production": "energy",
    "heat_production": "heat",
}


def _raise_tr(new_player: dict, delta: int) -> dict:
    """
    Punto UNICO por el que pasa todo cambio de Terraform Rating del motor.
    Ademas de aplicar el delta, marca `tr_raised_this_generation` cuando el
    cambio es un AUMENTO real -- el flag que necesitan las cartas que
    preguntan "¿subiste el TR en esta generacion?".

    Cinco cartas dependen de este flag: United Nations Mars Initiative
    ("if your TR was raised this generation, pay 3 M€ to raise it 1 more"),
    Pristar (al reves: paga solo si NO subiste TR) y las tres preludes
    Preservation Program / Suitable Infrastructure / Terraforming Deal.

    Un delta negativo (ej. tr_delta_reduced_by_influence, o la reversion de
    una oferta de oceano no aceptada) pasa igual por aca pero NO marca el
    flag: bajar el TR no es haberlo subido. Mismo criterio y misma forma que
    _increase_production, que centraliza los aumentos de produccion.

    El flag se limpia en run_production_phase, al cerrar la generacion.
    """
    new_player = {**new_player, "tr": new_player["tr"] + delta}
    if delta > 0:
        new_player["tr_raised_this_generation"] = True
    return new_player


def _increase_production(new_player: dict, key: str, delta: int) -> dict:
    """
    Punto UNICO por el que pasa todo cambio de produccion del motor (positivo
    o negativo): aplica el piso correspondiente (ver _apply_production_floor)
    y, si el cambio es un aumento real, dispara el pasivo
    "on_production_increased" (Manutech, corporaciones bloque 2: *"For each
    step you increase the production of a resource, including this, you also
    gain that resource"* -- texto literal de la carta, sin excepcion para M€
    -- gana tantas unidades de stock como pasos subio esa produccion).

    Reemplaza el patron repetido `new_player[key] = _apply_production_floor(
    key, new_player[key] + delta)` que antes vivia suelto en ~17 lugares del
    motor (production_deltas, production_delta_per_tag, proyectos estandar,
    etc.) -- centralizarlo evita tener que cablear Manutech en cada uno.
    """
    current = new_player[key]
    new_value = _apply_production_floor(key, current + delta)
    applied_delta = new_value - current
    new_player = {**new_player, key: new_value}
    if applied_delta > 0:
        stock_key = _PRODUCTION_STOCK_KEY.get(key)
        if stock_key is not None and any(
            effect.get("on_production_increased") for effect in new_player["passive_effects"]
        ):
            new_player[stock_key] = new_player[stock_key] + applied_delta
    return new_player


def is_blue_card(is_event: bool, effects: dict | None) -> bool:
    """
    True si la carta es AZUL segun la clasificacion de colores del juego.
    En Terraforming Mars las cartas de proyecto son verdes (efecto inmediato
    de una sola vez), azules (efecto ONGOING: accion repetible y/o efecto
    pasivo permanente, quedan en juego frente al jugador) o rojas (eventos).

    El color no esta guardado como columna: se deriva de lo que el catalogo
    ya sabe -- `cards.is_event` y las claves `becomes_active`/`passive` de
    `cards.effects`. Regla verificada contra 6 scans reales de cada
    categoria, incluido el caso dificil (una carta azul con `passive` pero
    SIN accion ni recursos propios, ej. Spin-Off Department) -- ver
    CARDS_LOG.md, entrada de Solarnet Shutdown. Funcion pura: recibe los dos
    campos del catalogo ya leidos, no accede a la base (eso lo hace
    tools._count_blue_cards_played).
    """
    if is_event:
        return False
    effects = effects or {}
    return "becomes_active" in effects or "passive" in effects


def _resolve_capped_counter(counter: str, player: dict, globals_: dict) -> int:
    """
    Fuente del contador SIN capar (el cap de 5 y el ajuste por Influencia se
    aplican en el caller, ver "resource_delta_per_capped_counter" en
    apply_card_effect -- expansion Turmoil, Global Events). Vocabulario:

      - "city_tiles_placed": ciudades colocadas por CUALQUIER jugador (ej.
        Riots: "Lose 4 M€ for each city tile").
      - "tr_sets_of_5_over_15": cuantos grupos completos de 5 TR el jugador
        tiene por encima de 15 (ej. Generous Funding: "Gain 2 M€ for each
        ... set of 5 TR over 15").
      - "events_played": cartas evento jugadas historicamente, cualquier
        jugador (`globals_["events_played"]`, ej. Celebrity Leaders: "Gain
        2 M€ for each event played").
      - "tr_sets_of_5_over:<N>": forma general del anterior con el umbral
        que imprima la carta (ej. Red Influence: "each set of 5 TR over
        10" -> counter="tr_sets_of_5_over:10").
      - "colonies_owned": colonias propias construidas
        (`player["colonies_owned"]`, expansion Colonies, ej. Microgravity
        Health Problems: "Lose 3 M€ for each colony").
      - "hand_size": cartas en la mano del jugador (ej. Scientific
        Community: "Gain 1 M€ for each card in hand").
      - "board_tiles_adjacent_to_ocean": CASO ESPECIAL -- no lo resuelve
        esta funcion sino que viene PRECALCULADO por el caller en el
        parametro `board_tiles_adjacent_to_ocean` de apply_card_effect
        (mismo desacople que `influence`: rules_engine.py no importa
        board.py). Ver board.count_tiles_adjacent_to_ocean (ej. Mud
        Slides).
      - "blue_cards_played": CASO ESPECIAL igual que el anterior -- viene
        precalculado en el parametro `blue_cards_played` de
        apply_card_effect, porque contar cartas azules exige cruzar
        `player["played_cards"]` contra el catalogo `cards` (acceso a
        base, prohibido en el motor puro). Ver is_blue_card y
        tools._count_blue_cards_played (ej. Solarnet Shutdown).
      - "<recurso>_production": la produccion propia de ese recurso (ej.
        Successful Organisms: "Gain 1 plant per plant production" ->
        counter="plant_production").
      - "tag:<tag>": cartas jugadas con ese tag (`player["tags_played"]`,
        ej. Asteroid Mining: "Gain 1 titanium for each Jovian tag" ->
        counter="tag:jovian").
    """
    if counter == "city_tiles_placed":
        return globals_["city_tiles_placed"]
    if counter == "tr_sets_of_5_over_15":  # forma vieja, equivale a "tr_sets_of_5_over:15"
        return max(0, (player["tr"] - 15) // 5)
    if counter.startswith("tr_sets_of_5_over:"):
        threshold = int(counter[len("tr_sets_of_5_over:"):])
        return max(0, (player["tr"] - threshold) // 5)
    if counter == "events_played":
        return globals_["events_played"]
    if counter == "colonies_owned":
        return len(player["colonies_owned"])
    if counter == "hand_size":
        return len(player["hand"])
    if counter.endswith("_production"):
        return player[counter]
    if counter.startswith("tag:"):
        return player["tags_played"].get(counter[len("tag:"):], 0)
    raise CardEffectError(f"Contador '{counter}' no soportado en resource_delta_per_capped_counter")


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
      - "requires_tr_raised_this_generation": bool -- True exige que el
        jugador YA haya subido su TR en esta generacion (ej. United Nations
        Mars Initiative: "if your TR was raised this generation, pay 3 M€ to
        raise it 1 step more"); False exige lo contrario. Lee el campo
        `tr_raised_this_generation`, que marca _raise_tr y limpia
        run_production_phase.
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
      - "is_chairman": true -- expansion Turmoil, requiere que el jugador
        sea el Chairman (`turmoil["chairman"] == player_id`, ver
        turmoil.py). Requiere pasar `turmoil` y `player_id` (ej. Banned
        Delegate).
      - "min_party_leader_count": N -- expansion Turmoil, requiere ser Party
        Leader de al menos N partidos distintos simultaneamente (cuenta
        `turmoil["parties"][p]["leader"] == player_id` para cada partido).
        Requiere pasar `turmoil` y `player_id` (ej. Political Alliance,
        bloque 32: N=2).
      - "party_leader_and_neutral_chairman": true -- expansion Turmoil,
        requiere que el jugador sea Party Leader de AL MENOS un partido y
        que la silla de Chairman este vacante/neutral (`turmoil["chairman"]
        is None`, el valor inicial de new_turmoil() antes de la primera
        "New Government" -- ver turmoil.py). Requiere pasar `turmoil` y
        `player_id` (ej. Vote of No Confidence, bloque 31: reemplaza al
        Chairman neutral, efecto `become_chairman_from_neutral`).
      - "min_own_city_tiles": N -- ciudades PROPIAS del jugador en el mapa
        (ej. City Parks: "requires that YOU have 3 city tiles"; Casinos: 1).
        Distinto de "min_city_tiles", que mira el contador global de
        ciudades de CUALQUIER jugador e incluye las de fuera del mapa. Se
        resuelve en tools.play_card, que es quien tiene el tablero (mismo
        criterio que min_greenery_tiles_owned).
      - "min_distinct_resource_types": N -- requiere tener al menos N TIPOS
        de recurso distintos ahora mismo, contando los 6 de stock (mc,
        steel, titanium, plants, energy, heat) con cantidad > 0 mas cada
        tipo guardado en cartas activas (microbe, animal, floater, ...) con
        total > 0 (ej. Diversity Support: 9). Ver
        count_distinct_resource_types; depende de que las cartas declaren
        `active_card_resource_type`.
      - "min_total_card_resources": {"resource_type": "<tipo>", "count": N}
        -- requiere al menos N recursos de ese TIPO sumados entre TODAS
        las cartas activas del jugador (ej. Aerosport Tournament: 5
        floaters, sin importar en que carta(s) esten guardados). Ver
        register_active_card (parametro `resource_type`) y
        sum_card_resources_by_type. Requiere pasar `player`.

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
    venus_only_steps = 0
    if player is not None:
        for effect in player["passive_effects"]:
            tolerance_steps = max(tolerance_steps, effect.get("global_requirements_tolerance_steps", 0))
            # Morning Star Inc solo relaja los requisitos de VENUS ("your Venus
            # requirements are +/- 2 steps"), no los de temperatura/oxigeno/
            # oceanos como Inventrix o Adaptation Technology.
            venus_only_steps = max(venus_only_steps, effect.get("venus_requirements_tolerance_steps", 0))
        tolerance_steps += abs(player.get("pending_requirement_tolerance_steps", 0))
    temperature_tolerance = tolerance_steps * TEMPERATURE_STEP
    oxygen_tolerance = tolerance_steps * OXYGEN_STEP
    oceans_tolerance = tolerance_steps
    venus_tolerance = max(tolerance_steps, venus_only_steps) * VENUS_STEP

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

    if requirements.get("is_chairman"):
        if turmoil is None or player_id is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado de Turmoil y el player_id"
            )
        if turmoil["chairman"] != player_id:
            raise CardRequirementNotMetError("Requiere ser el Chairman")

    if "min_party_leader_count" in requirements:
        if turmoil is None or player_id is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado de Turmoil y el player_id"
            )
        min_count = requirements["min_party_leader_count"]
        led = sum(1 for party in turmoil["parties"].values() if party["leader"] == player_id)
        if led < min_count:
            raise CardRequirementNotMetError(f"Requiere ser Party Leader de {min_count} partidos, es de {led}")

    if requirements.get("party_leader_and_neutral_chairman"):
        if turmoil is None or player_id is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado de Turmoil y el player_id"
            )
        if turmoil["chairman"] is not None:
            raise CardRequirementNotMetError("Requiere que el Chairman actual sea neutral")
        is_leader_somewhere = any(
            party["leader"] == player_id for party in turmoil["parties"].values()
        )
        if not is_leader_somewhere:
            raise CardRequirementNotMetError("Requiere ser Party Leader de algun partido")

    if "min_distinct_resource_types" in requirements:
        if player is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado del jugador"
            )
        distinct = count_distinct_resource_types(player)
        if distinct < requirements["min_distinct_resource_types"]:
            raise CardRequirementNotMetError(
                f"Requiere {requirements['min_distinct_resource_types']} tipos de recurso "
                f"distintos, hay {distinct}"
            )

    if "min_total_card_resources" in requirements:
        spec = requirements["min_total_card_resources"]
        if player is None:
            raise CardRequirementNotMetError(
                "Este requisito necesita el estado del jugador (recursos guardados en cartas)"
            )
        have = sum_card_resources_by_type(player, spec["resource_type"])
        if have < spec["count"]:
            raise CardRequirementNotMetError(
                f"Requiere {spec['count']} {spec['resource_type']}(s) guardados en cartas activas, hay {have}"
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
    if "requires_tr_raised_this_generation" in requirements:
        if player is None:
            raise CardRequirementNotMetError("Este requisito necesita el estado del jugador (TR)")
        expected = requirements["requires_tr_raised_this_generation"]
        if bool(player["tr_raised_this_generation"]) is not bool(expected):
            raise CardRequirementNotMetError(
                "Requiere haber subido el TR en esta generacion" if expected
                else "Requiere NO haber subido el TR en esta generacion"
            )
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
    target_card_id_3: str | None = None,
    discard_card_id: str | None = None,
    influence: int = 0,
    discard_card_ids: list[str] | None = None,
    board_tiles_adjacent_to_ocean: int = 0,
    blue_cards_played: int = 0,
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
      - "place_oceans_without_tr": N -- igual pero SIN otorgar TR, y sin
        error si ya se colocaron los 9 (simplemente no coloca mas). Los
        pasivos "on_ocean_placed" (ej. Arctic Algae) SI se disparan. Para
        Global Events que colocan oceano sin premiar al jugador (ej.
        Aquifer Released by Public Council: "the first player places an
        ocean tile, but no player gets any TR or placement bonuses" --
        FAQ oficial).
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
      - "production_delta_per_distinct_tag": {"production": "<recurso>_production",
        "per_tag": N (default 1), "extra_tags": [<tags de esta carta>]} --
        suma N por cada tag DISTINTO que el jugador tenga en juego (no
        repeticiones de un tag como production_delta_per_tag) (ej.
        Interplanetary Trade: +1 MC de produccion por cada tag distinto,
        incluido el propio -- `extra_tags` declara los tags de la carta
        misma, igual criterio que include_this en production_delta_per_tag).
      - "production_delta_per_colony": {"production": "<recurso>_production",
        "per_colony": N (default 1), "cap": N (opcional, sin tope por
        defecto -- ej. Jovian Tax Rights, cuya ERRATA oficial agrega
        "(max 5)" al texto impreso)} -- suma N por cada colonia que el
        jugador ya construyo (`player["colonies_owned"]`, expansion
        Colonies, ver colonies.py) (ej. Ecology Research: +1 produccion de
        plantas por cada colonia propia).
      - "resource_delta_per_colony": {"resource": "<recurso>", "per_colony":
        N (default 1)} -- igual que production_delta_per_colony pero suma
        al STOCK del recurso en vez de a su produccion (ej. Ceres Tech
        Market: +2 MC de stock por cada colonia propia).
      - "resource_delta_per_tag": {"tag": "<tag>", "resource": "<recurso>",
        "per_tag": N (default 1), "include_this": bool} o una LISTA de
        specs -- analogo de STOCK a production_delta_per_tag: suma al
        recurso segun cuantos tags de ese tipo jugo el jugador (ej. Soil
        Studies: 1 planta por cada tag venus y por cada tag plant
        incluyendo esta; Summit Logistics: 1 M€ por cada tag jovian/earth/
        venus).
      - "resource_delta_per_capped_counter": {"counter": "<ver
        _resolve_capped_counter>", "resource": "<recurso>", "per_unit": N,
        "cap": 5 (default, `null` = sin tope cuando la carta dice
        explicitamente "no limit", ej. Scientific Community),
        "influence_direction": "add"|"subtract"|"none" (default "add";
        "none" para cartas donde la Influencia NO ajusta este contador
        porque se usa en otra clausula aparte, ej. Red Influence)} --
        expansion Turmoil, vocabulario de los Global Event cards (ver turmoil.py y tools.resolve_global_event). El
        contador se calcula sin tope, se capa a `cap` (regla oficial:
        "any Global Event that counts something... can only count up to a
        maximum of 5"), y se ajusta sumando o restando la Influencia del
        jugador (parametro `influence`, calculada por el caller con
        turmoil.compute_influence -- rules_engine.py no conoce Turmoil,
        solo recibe el numero ya resuelto, mismo desacople que
        wild_tag_choice/card_resource_to_pay). El resultado nunca es
        negativo (se clampea a 0 antes de multiplicar). Ej. Generous
        Funding: counter="tr_sets_of_5_over_15", resource="mc",
        per_unit=2, influence_direction="add" (+influencia SUMA sets);
        Riots: counter="city_tiles_placed", resource="mc", per_unit=-4,
        influence_direction="subtract" (+influencia RESTA del conteo de
        ciudades, reduciendo cuanto se pierde).
      - "resource_delta_per_influence": {"<recurso>": per_unit, ...} --
        expansion Turmoil (Global Events), suma `influence * per_unit` a
        cada recurso listado, SIN tope de 5 (la Influencia se usa directo
        como multiplicador, no como ajuste de un contador separado -- ej.
        Aquifer Released by Public Council: "Gain 1 plant and 1 steel per
        influence" -> {"plants": 1, "steel": 1}).
      - "resource_delta_if_tag_diversity": {"threshold": N, "resource":
        "<recurso>", "amount": M} -- suma M al recurso SOLO si la cantidad
        de tags DISTINTOS que el jugador jugo (uno por tipo, sin importar
        cuantas veces) mas su Influencia llega a `threshold` (ej.
        Diversity: "Gain 10 M€ if you have 9 or more different tags.
        Influence counts as unique tags" -> threshold=9, resource="mc",
        amount=10). Sin tope de 5 -- es un umbral booleano, no un
        contador que se multiplica.
      - "resource_delta_per_influence_choice": {"options": ["<recurso>",
        ...], "per_unit": N (default 1)} -- el jugador ELIGE uno de los
        recursos de `options` (via `effect_choice`, indice 0-based) y gana
        `influencia * per_unit` de ese recurso (ej. Dry Deserts: "Gain 1
        standard resource per influence" -- los 6 recursos basicos, segun
        el FAQ oficial: MC, acero, titanio, plantas, energia o calor).
      - "production_delta_per_influence": {"<recurso>_production": per_unit,
        ...} -- analogo de produccion a resource_delta_per_influence, sin
        tope (ej. Volcanic Eruptions: "+1 heat production per influence";
        Red Influence: "+1 M€ production per influence").
      - "tr_delta_reduced_by_influence": {"base_reduction": N} -- BAJA el
        TR N pasos, y cada punto de Influencia evita 1 paso; nunca se
        convierte en ganancia (piso 0 pasos) (ej. War on Earth: "Reduce TR
        4 steps. Each influence prevents 1 step").
      - "lower_temperature_steps": N -- BAJA la temperatura N pasos
        (clampeada al piso TEMPERATURE_MIN). NO toca el TR: bajar un
        parametro global nunca quita TR en este motor (el TR ya ganado por
        haberlo subido no se devuelve) (ej. Snow Cover: "Decrease
        temperature 2 steps").
      - "add_resource_to_all_cards_with_resources": {"amount": N} -- suma
        N a TODA carta activa que YA tenga al menos 1 recurso, sin filtrar
        por tipo (a diferencia de add_resource_to_all_matching_type, que
        filtra por `resource_type` e incluye las que estan en 0) (ej.
        Sponsored Projects: "All cards with resources on them gain 1
        resource").
      - "discard_cards": {"n": N} -- descarta N cartas de la mano elegidas
        por el jugador (parametro `discard_card_ids`, lista de largo
        exacto N), sin robar nada a cambio -- distinto de
        discard_card_then_draw (esa descarta 1 y roba) (ej. Paradigm
        Breakdown: "Discard 2 cards from hand").
      - "resource_delta_clamp_to_capped_max": {"resource": "<recurso>",
        "base_max": N} -- expansion Turmoil (Global Events), BAJA el stock
        de ese recurso al minimo entre su valor actual y `base_max +
        influence` (nunca lo sube) -- distinto de un delta, es un techo
        (ej. Eco Sabotage: "Lose all plants except 3 + influence" ->
        resource="plants", base_max=3).
      - "resource_set_to_zero": ["<recurso>", ...] -- pone esos recursos
        en 0 (ej. Global Dust Storm: "Lose all heat" -> ["heat"]).
      - "tr_delta_by_threshold": {"score_tags": ["<tag>", ...] (opcional),
        "score_counters": ["<contador global>", ...] (opcional),
        "thresholds": [[min_score, tr], ...] (orden descendente)} --
        calcula un puntaje (Influencia + suma de tags + suma de
        contadores globales) y suma el TR del primer umbral que alcance
        (ej. Election: "Count your influence plus building tags and city
        tiles... The player with most (or 10 in solo) gains 2 TR, the 2nd
        (or counting 5 in solo) gains 1 TR" -> score_tags=["building"],
        score_counters=["city_tiles_placed"], thresholds=[[10,2],[5,1]] --
        la carta imprime explícitamente la regla de un jugador, sin
        ambigüedad).
      - "production_delta_per_tag_plus_influence": {"tag": "<tag>",
        "production": "<recurso>_production", "divisor": N (default 1),
        "per_unit": N (default 1)} -- como production_delta_per_card_resource_type
        pero el contador es tags jugados + Influencia, SIN tope (ej.
        Improved Energy Templates: "+1 energy production per 2 power tags
        (no limit). Influence counts as power tags" -> tag="power",
        production="energy_production", divisor=2).
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
      - "target_card_resource_delta_typed": {"resource_type": "<tipo>",
        "amount": N} -- igual que target_card_resource_delta, pero exige
        que la carta objetivo (`target_card_id`) tenga ESE `resource_type`
        (ver register_active_card) -- lanza CardEffectError si no matchea
        (ej. Airliners: "Add 2 floaters to ANOTHER card" -- solo vale
        apuntar a una carta que de verdad coleccione floaters, no
        cualquier carta activa). `amount` puede ser negativo (ej.
        Corrosive Rain, expansion Turmoil: "Lose 2 floaters from a card"
        -> amount=-2, dentro de una rama de "choice"). Alternativa
        "amount_per_influence": true en vez de "amount" -- usa la
        Influencia del jugador (parametro `influence`) como cantidad
        dinamica en vez de un numero fijo (ej. Cloud Societies, expansion
        Turmoil: "Add 1 floater for each influence to a card").
      - "add_resource_to_all_matching_type": {"resource_type": "<tipo>",
        "amount": N} -- suma N al recurso de TODAS las cartas activas del
        jugador que tengan ese `resource_type`, sin elegir una en
        particular (ej. Cloud Societies, expansion Turmoil Global Events:
        "Add a floater to each card that can collect floaters").
      - "resource_delta_per_card_resource_type": {"resource_type":
        "<tipo>", "resource": "<recurso>", "divisor": N (default 1),
        "per_unit": N (default 1)} -- analogo de STOCK a
        production_delta_per_card_resource_type: suma al recurso segun
        cuantos recursos de ese tipo tiene el jugador sumados entre TODAS
        sus cartas activas (ej. GHG Shipment: "gain 1 heat for each
        floater you have").
      - "production_delta_per_card_resource_type": {"resource_type":
        "<tipo>", "production": "<recurso>_production", "divisor": N
        (default 1), "per_unit": N (default 1)} -- suma produccion segun
        cuantos recursos de ese tipo tiene el jugador sumados entre TODAS
        sus cartas activas (ver sum_card_resources_by_type), dividido
        entero por `divisor` (ej. Floater Leasing: "+1 produccion MC por
        cada 3 floaters que tengas" -> resource_type="floater",
        production="mc_production", divisor=3, per_unit=1).
      - "draw_cards_per_influence": true -- expansion Turmoil, roba tantas
        cartas como Influencia tenga el jugador (parametro `influence`,
        ver turmoil.compute_influence) (ej. Corrosive Rain: "Draw 1 card
        for each influence").

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
            discard_card_id=discard_card_id, influence=influence,
            discard_card_ids=discard_card_ids,
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
        new_player = _increase_production(new_player, "mc_production", effects["mc_production_delta"])

    if "mc_delta" in effects:
        new_player["mc"] = max(0, new_player["mc"] + effects["mc_delta"])

    if "production_deltas" in effects:
        for key, delta in effects["production_deltas"].items():
            new_player = _increase_production(new_player, key, delta)

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
            new_player = _increase_production(new_player, key, delta)

    if "production_delta_per_distinct_tag" in effects:
        # Interplanetary Trade (X05, bloque 32): "+1 M€ production per
        # DIFFERENT tag you have in play, including this" -- a diferencia
        # de production_delta_per_tag (cuenta repeticiones de UN tag), esto
        # cuenta cuantos tags DISTINTOS tiene el jugador. `extra_tags`
        # declara los tags de la propia carta (increment_tags_played corre
        # DESPUES de apply_card_effect, asi que "including this" hay que
        # sumarlo a mano, igual que include_this en production_delta_per_tag).
        spec = effects["production_delta_per_distinct_tag"]
        key = spec["production"]
        distinct = {tag for tag, count in player["tags_played"].items() if count > 0}
        distinct |= set(spec.get("extra_tags", []))
        delta = len(distinct) * spec.get("per_tag", 1)
        new_player = _increase_production(new_player, key, delta)

    if "tr_delta_per_tag" in effects:
        spec = effects["tr_delta_per_tag"]
        count = player["tags_played"].get(spec["tag"], 0)
        if spec.get("include_this"):
            count += 1
        new_player = _raise_tr(new_player, count * spec.get("per_tag", 1))

    if "production_delta_per_colony" in effects:
        spec = effects["production_delta_per_colony"]
        key = spec["production"]
        count = len(player["colonies_owned"])
        if spec.get("cap") is not None:
            count = min(count, spec["cap"])
        new_player = _increase_production(new_player, key, count * spec.get("per_colony", 1))

    if "resource_delta_per_colony" in effects:
        spec = effects["resource_delta_per_colony"]
        key = spec["resource"]
        count = len(player["colonies_owned"])
        new_player[key] = max(0, new_player[key] + count * spec.get("per_colony", 1))

    if "resource_delta_per_tag" in effects:
        specs = effects["resource_delta_per_tag"]
        if isinstance(specs, dict):
            specs = [specs]
        for spec in specs:
            count = player["tags_played"].get(spec["tag"], 0)
            if spec.get("include_this"):
                count += 1
            key = spec["resource"]
            new_player[key] = max(0, new_player[key] + count * spec.get("per_tag", 1))

    if "resource_delta_per_capped_counter" in effects:
        spec = effects["resource_delta_per_capped_counter"]
        if spec["counter"] == "board_tiles_adjacent_to_ocean":
            raw_count = board_tiles_adjacent_to_ocean
        elif spec["counter"] == "blue_cards_played":
            raw_count = blue_cards_played
        else:
            raw_count = _resolve_capped_counter(spec["counter"], new_player, new_globals)
        cap = spec.get("cap", 5)
        capped = raw_count if cap is None else min(raw_count, cap)
        direction = spec.get("influence_direction", "add")
        signed_influence = {"add": influence, "subtract": -influence, "none": 0}[direction]
        count = max(0, capped + signed_influence)
        key = spec["resource"]
        new_player[key] = max(0, new_player[key] + count * spec.get("per_unit", 1))

    if "resource_delta_per_influence" in effects:
        for key, per_unit in effects["resource_delta_per_influence"].items():
            new_player[key] = max(0, new_player[key] + influence * per_unit)

    if "resource_delta_per_influence_choice" in effects:
        spec = effects["resource_delta_per_influence_choice"]
        options = spec["options"]
        if effect_choice is None or not (0 <= effect_choice < len(options)):
            raise CardEffectError(
                f"Este efecto requiere effect_choice entre 0 y {len(options) - 1} (recurso elegido)"
            )
        key = options[effect_choice]
        new_player[key] = max(0, new_player[key] + influence * spec.get("per_unit", 1))

    if "production_delta_per_influence" in effects:
        for key, per_unit in effects["production_delta_per_influence"].items():
            new_player = _increase_production(new_player, key, influence * per_unit)

    if "tr_delta_reduced_by_influence" in effects:
        spec = effects["tr_delta_reduced_by_influence"]
        steps = max(0, spec["base_reduction"] - influence)
        new_player = _raise_tr(new_player, -steps)

    if "lower_temperature_steps" in effects and new_globals["temperature"] < TEMPERATURE_MAX:
        # Si la temperatura ya esta en su maximo, este efecto NO se aplica: un
        # parametro global maximizado no vuelve a ser afectado en toda la
        # partida (FAQ oficial, entrada de Snow Cover).
        new_globals["temperature"] = max(
            TEMPERATURE_MIN,
            new_globals["temperature"] - effects["lower_temperature_steps"] * TEMPERATURE_STEP,
        )

    if "add_resource_to_all_cards_with_resources" in effects:
        amount = effects["add_resource_to_all_cards_with_resources"]["amount"]
        new_active_cards = dict(new_player["active_cards"])
        for cid, c in new_active_cards.items():
            if c["resources"] > 0:
                new_active_cards[cid] = {**c, "resources": max(0, c["resources"] + amount)}
        new_player["active_cards"] = new_active_cards

    if "discard_cards" in effects:
        n = effects["discard_cards"]["n"]
        chosen = discard_card_ids or []
        if len(chosen) != n:
            raise CardEffectError(f"Este efecto descarta {n} carta(s); se recibieron {len(chosen)}")
        for cid in chosen:
            new_player = dict(remove_card_from_hand(PlayerState(**new_player), cid))  # type: ignore[typeddict-item]

    if "resource_delta_if_tag_diversity" in effects:
        spec = effects["resource_delta_if_tag_diversity"]
        # El tag comodin "wild" NO cuenta en los Global Events: solo vale como
        # tag durante la fase de accion del jugador, no en la fase Turmoil
        # (FAQ oficial, entrada del wild tag / Research Network).
        unique_tags = sum(
            1 for tag, count in player["tags_played"].items() if count > 0 and tag != "wild"
        )
        if unique_tags + influence >= spec["threshold"]:
            key = spec["resource"]
            new_player[key] = max(0, new_player[key] + spec["amount"])

    if "resource_delta_clamp_to_capped_max" in effects:
        spec = effects["resource_delta_clamp_to_capped_max"]
        key = spec["resource"]
        cap = max(0, spec["base_max"] + influence)
        new_player[key] = min(new_player[key], cap)

    if "resource_set_to_zero" in effects:
        for key in effects["resource_set_to_zero"]:
            new_player[key] = 0

    if "tr_delta_by_threshold" in effects:
        spec = effects["tr_delta_by_threshold"]
        score = influence
        for tag in spec.get("score_tags", []):
            score += player["tags_played"].get(tag, 0)
        for counter in spec.get("score_counters", []):
            score += new_globals[counter]
        tr_gain = 0
        for min_score, tr in spec["thresholds"]:
            if score >= min_score:
                tr_gain = tr
                break
        new_player = _raise_tr(new_player, tr_gain)

    if "production_delta_per_tag_plus_influence" in effects:
        spec = effects["production_delta_per_tag_plus_influence"]
        key = spec["production"]
        count = player["tags_played"].get(spec["tag"], 0) + influence
        units = count // spec.get("divisor", 1)
        new_player = _increase_production(new_player, key, units * spec.get("per_unit", 1))

    if "production_delta_per_tag_pair" in effects:
        spec = effects["production_delta_per_tag_pair"]
        key = spec["production"]
        count_a = player["tags_played"].get(spec["tag_a"], 0)
        count_b = player["tags_played"].get(spec["tag_b"], 0)
        sets = min(count_a, count_b)
        new_player = _increase_production(new_player, key, sets * spec.get("per_set", 1))

    if "production_delta_per_zero_tag_card" in effects:
        spec = effects["production_delta_per_zero_tag_card"]
        key = spec["production"]
        count = player["zero_tag_cards_played"]
        if spec.get("include_this"):
            count += 1
        new_player = _increase_production(new_player, key, count * spec.get("per_card", 1))

    if "production_delta_per_counter" in effects:
        spec = effects["production_delta_per_counter"]
        key = spec["production"]
        count = globals_[spec["counter"]]
        delta = count * spec.get("per_counter", 1)
        new_player = _increase_production(new_player, key, delta)

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
        new_player = _increase_production(new_player, to_key, effect_amount)

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

    if "place_oceans_without_tr" in effects:
        for _ in range(effects["place_oceans_without_tr"]):
            if new_globals["oceans_placed"] >= OCEANS_MAX:
                break
            p2, g2 = place_ocean(PlayerState(**new_player), GlobalParameters(**new_globals))  # type: ignore[typeddict-item]
            new_player, new_globals = dict(p2), dict(g2)
            new_player = _raise_tr(new_player, -1)  # el TR se revierte: este oceano no lo otorga

    if "place_city_tiles" in effects:
        for _ in range(effects["place_city_tiles"]):
            new_globals = dict(place_city_tile(GlobalParameters(**new_globals)))  # type: ignore[typeddict-item]

    if "tr_delta" in effects:
        new_player = _raise_tr(new_player, effects["tr_delta"])

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

    if "spend_any_card_resource" in effects:
        # Soil Enrichment (X67, bloque 38): "spend 1 microbe from ANY of your
        # cards to gain 5 plants", como efecto INMEDIATO de un evento. El
        # analogo `cost.any_card_resource` ya existia, pero solo para acciones
        # repetibles (use_card_action); esta es su version para
        # apply_card_effect. El recurso se DESTRUYE (no se mueve a otra carta,
        # a diferencia de move_from_target_card_resource_delta).
        spec = effects["spend_any_card_resource"]
        needed = spec.get("amount", 1)
        if target_card_id is None:
            raise CardEffectError("Esta carta requiere target_card_id (de que carta sacar el recurso)")
        active_cards = new_player["active_cards"]
        if target_card_id not in active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        resource_type = spec.get("resource_type")
        if resource_type is not None and active_cards[target_card_id].get("resource_type") != resource_type:
            raise CardEffectError(f"'{target_card_id}' no guarda recursos de tipo '{resource_type}'")
        if active_cards[target_card_id]["resources"] < needed:
            raise InsufficientResourcesError(
                f"'{target_card_id}' tiene {active_cards[target_card_id]['resources']} recursos, "
                f"se necesitan {needed}"
            )
        new_player["active_cards"] = {
            **active_cards,
            target_card_id: {
                **active_cards[target_card_id],
                "resources": active_cards[target_card_id]["resources"] - needed,
            },
        }

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

    if "target_card_resource_delta_typed" in effects:
        spec = effects["target_card_resource_delta_typed"]
        if target_card_id is None:
            raise CardEffectError("Esta carta requiere target_card_id")
        active_cards = new_player["active_cards"]
        if target_card_id not in active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id}' no esta activa para este jugador")
        if active_cards[target_card_id].get("resource_type") != spec["resource_type"]:
            raise CardEffectError(
                f"'{target_card_id}' no guarda recursos de tipo '{spec['resource_type']}'"
            )
        amount = influence if spec.get("amount_per_influence") else spec["amount"]
        new_active_cards = dict(active_cards)
        new_active_cards[target_card_id] = {
            **new_active_cards[target_card_id],
            "resources": max(0, new_active_cards[target_card_id]["resources"] + amount),
        }
        new_player["active_cards"] = new_active_cards

    if "add_resource_to_all_matching_type" in effects:
        spec = effects["add_resource_to_all_matching_type"]
        new_active_cards = dict(new_player["active_cards"])
        for cid, c in new_active_cards.items():
            if c.get("resource_type") == spec["resource_type"]:
                new_active_cards[cid] = {**c, "resources": max(0, c["resources"] + spec["amount"])}
        new_player["active_cards"] = new_active_cards

    if "resource_delta_per_card_resource_type" in effects:
        spec = effects["resource_delta_per_card_resource_type"]
        total = sum_card_resources_by_type(PlayerState(**new_player), spec["resource_type"])  # type: ignore[typeddict-item]
        units = total // spec.get("divisor", 1)
        key = spec["resource"]
        new_player[key] = max(0, new_player[key] + units * spec.get("per_unit", 1))

    if "production_delta_per_card_resource_type" in effects:
        spec = effects["production_delta_per_card_resource_type"]
        total = sum_card_resources_by_type(PlayerState(**new_player), spec["resource_type"])  # type: ignore[typeddict-item]
        units = total // spec.get("divisor", 1)
        key = spec["production"]
        new_player = _increase_production(new_player, key, units * spec.get("per_unit", 1))

    if "draw_cards_per_influence" in effects and effects["draw_cards_per_influence"]:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), influence))  # type: ignore[typeddict-item]

    if "target_card_resource_delta_3" in effects:
        amount = effects["target_card_resource_delta_3"]
        if target_card_id_3 is None:
            raise CardEffectError("Esta carta requiere target_card_id_3")
        active_cards = new_player["active_cards"]
        if target_card_id_3 not in active_cards:
            raise CardEffectError(f"La carta objetivo '{target_card_id_3}' no esta activa para este jugador")
        new_active_cards = dict(active_cards)
        new_active_cards[target_card_id_3] = {
            **new_active_cards[target_card_id_3],
            "resources": max(0, new_active_cards[target_card_id_3]["resources"] + amount),
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

def register_active_card(
    player: PlayerState, card_id: str, initial_resources: int = 0, resource_type: str | None = None,
) -> PlayerState:
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

    resource_type: OPCIONAL -- etiqueta el TIPO de recurso que guarda esta
    carta (ej. "floater", "microbe", "animal", "data", "science"), viene de
    `effects.active_card_resource_type`. Antes de esta pieza,
    `active_cards[card_id]["resources"]` era un contador sin tipo -- no
    permitia sumar "solo los floaters" entre varias cartas activas.
    Necesario para requisitos/efectos que cuentan un tipo de recurso
    especifico a traves de TODAS las cartas activas del jugador (ej.
    Aerosport Tournament: "Requires that you have 5 floaters"; Floater
    Leasing: "+1 produccion MC por cada 3 floaters que tengas" -- ver
    sum_card_resources_by_type, requirement "min_total_card_resources" en
    check_card_requirements, y las piezas nuevas en apply_card_effect
    documentadas ahi). None si la carta no necesita esta distincion (la
    inmensa mayoria -- solo importa cuando una carta DISTINTA necesita
    sumar/filtrar por tipo).
    """
    new_active_cards = dict(player["active_cards"])
    new_active_cards[card_id] = {
        "resources": initial_resources, "action_used": False, "resource_type": resource_type,
    }
    return {**player, "active_cards": new_active_cards}


def sum_card_resources_by_type(player: PlayerState, resource_type: str) -> int:
    """
    Suma `resources` de TODAS las cartas activas del jugador cuyo
    `resource_type` (ver register_active_card) coincida (ej. todos los
    floaters guardados en cualquier carta, sin importar cual). Cartas
    activas registradas ANTES de esta pieza (o sin `resource_type` pasado)
    no tienen esa clave -- `.get(...)` las trata como None, nunca matchean.
    """
    return sum(
        c["resources"] for c in player["active_cards"].values() if c.get("resource_type") == resource_type
    )


#: Los 6 recursos de stock del tablero de jugador. Junto con los tipos de
#: recurso que se guardan EN cartas (microbios, animales, floaters, ...)
#: forman los "tipos de recurso" que cuenta count_distinct_resource_types.
STOCK_RESOURCE_KEYS = ("mc", "steel", "titanium", "plants", "energy", "heat")


def count_distinct_resource_types(player: PlayerState) -> int:
    """
    Cuantos TIPOS de recurso distintos tiene el jugador ahora mismo: los 6 de
    stock con cantidad > 0, mas cada tipo distinto guardado en sus cartas
    activas (microbe, animal, floater, asteroid, graphene, ...) con total > 0.

    Usado por el requisito "min_distinct_resource_types" (Diversity Support:
    9 tipos distintos). Depende de que las cartas que guardan recursos
    declaren `active_card_resource_type` -- por eso esta carta estuvo
    pendiente hasta el retrofit de microbios/animales del bloque 34.
    """
    from_stock = sum(1 for key in STOCK_RESOURCE_KEYS if player[key] > 0)
    from_cards = sum(1 for total in snapshot_card_resource_totals(player).values() if total > 0)
    return from_stock + from_cards


def snapshot_card_resource_totals(player: PlayerState) -> dict[str, int]:
    """
    Total de recursos guardados por TIPO ("microbe", "animal", "floater",
    "asteroid", ...) sumando todas las cartas activas. Se usa junto con
    apply_card_resource_gained_bonuses para detectar cuantos recursos de
    cada tipo GANO el jugador durante una jugada, comparando un snapshot
    de antes contra el estado de despues -- mismo patron de "diff de
    contadores" que tools.play_card ya usa para oceanos/ciudades, y la
    unica forma razonable de cubrir los muchos caminos que agregan
    recursos a cartas (accion propia, target_card_resource_delta, pasivos
    on_tag_played/on_greenery_placed, recursos iniciales, etc.) sin
    enganchar cada uno por separado.
    """
    totals: dict[str, int] = {}
    for card in player["active_cards"].values():
        resource_type = card.get("resource_type")
        if resource_type is None:
            continue
        totals[resource_type] = totals.get(resource_type, 0) + card["resources"]
    return totals


def apply_card_resource_gained_bonuses(
    player: PlayerState, totals_before: dict[str, int],
    active_cards_before: dict | None = None,
) -> PlayerState:
    """
    Aplica el pasivo "on_card_resource_gained": {"resource_type": "<tipo>",
    "mc_delta": N} -- suma N MC al jugador por CADA unidad de ese tipo de
    recurso que haya ganado en CUALQUIER carta activa desde `totals_before`
    (ej. Meat Industry: "when you gain an animal to ANY CARD, gain 2 M€";
    Topsoil Contract: 1 M€ por microbio).

    Solo cuenta ganancias netas positivas: gastar recursos (ej. Regolith
    Eaters removiendo 2 microbios) nunca resta MC. Mover un recurso entre
    dos cartas del mismo tipo tampoco paga, porque el total no cambia --
    coherente con el texto oficial, que premia GANAR el recurso, no
    reubicarlo.
    """
    gained_mc = 0
    gains: dict[str, int] = {}
    for effect in player["passive_effects"]:
        spec = effect.get("on_card_resource_gained")
        if spec is None:
            continue
        resource_type = spec["resource_type"]
        if spec.get("own_card_only"):
            # Main Belt Asteroids: "when gaining an asteroid HERE" -- solo
            # cuentan los recursos ganados en LA CARTA que registro el pasivo,
            # no en cualquier carta del jugador.
            card_id = effect["card_id"]
            after = player["active_cards"].get(card_id, {}).get("resources", 0)
            before = (active_cards_before or {}).get(card_id, {}).get("resources", 0)
            delta = after - before
        else:
            delta = sum_card_resources_by_type(player, resource_type) - totals_before.get(resource_type, 0)
        if delta > 0:
            for key, per_unit in spec.get("resource_deltas", {}).items():
                gains[key] = gains.get(key, 0) + delta * per_unit
            gained_mc += delta * spec.get("mc_delta", 0)
    if gained_mc == 0 and not gains:
        return player
    new_player: dict = {**player, "mc": player["mc"] + gained_mc}
    for key, amount in gains.items():
        new_player[key] = new_player[key] + amount
    return PlayerState(**new_player)  # type: ignore[typeddict-item]


def resolve_active_card_starting_resources(player: PlayerState, effects: dict) -> int:
    """
    Cuantos recursos arranca una carta activa recien jugada: el entero fijo de
    `effects.active_card_starting_resources` (ej. Herbivores: 1) o, si esta
    presente, `effects.active_card_starting_resources_per_tag`
    ({"tag", "per_tag" (default 1), "include_this": bool}) -- escala segun los
    tags ya jugados (ej. Floating Refinery: 1 floater por cada tag venus,
    incluido el suyo). `include_this` hace falta porque tools.play_card
    registra la carta activa ANTES de incrementar `tags_played`. Si estan las
    dos claves gana la version per_tag (ninguna carta necesita sumarlas hoy).
    """
    spec = effects.get("active_card_starting_resources_per_tag")
    if spec is not None:
        count = player["tags_played"].get(spec["tag"], 0) + (1 if spec.get("include_this") else 0)
        return count * spec.get("per_tag", 1)
    return effects.get("active_card_starting_resources", 0)


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
    steel_to_pay: int = 0,
) -> tuple[PlayerState, GlobalParameters]:
    """
    Ejecuta la accion repetible de una carta activa (columna `effects.action`
    en `cards`). Vocabulario de `action_spec`:

      - "convert_resource_amount": {"from": "<recurso>", "to": "<recurso>",
        "ratio": N (default 1)} -- convierte `effect_amount` (X, elegido por
        el jugador) unidades de stock de un recurso a X*ratio del otro,
        limitado al stock disponible (ej. Power Infrastructure: gastar
        cualquier cantidad de energia para ganar esa cantidad de MC).
        `ratio` puede ser fraccionario (ej. Energy Market, bloque 31: 0.5,
        "spend 2X MC to gain X energy" -- effect_amount es el MC gastado,
        no el energy ganado); lanza CardEffectError si X*ratio no da un
        entero exacto (ej. effect_amount impar con ratio 0.5). A
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
      - "requires_zero_resource": "<recurso>" -- la accion (o esa opcion del
        `choice`) solo esta disponible si el jugador tiene 0 de ese recurso en
        stock (ej. Factorum: "increase your energy production 1 step IF YOU
        HAVE NO ENERGY RESOURCES"). Va al nivel del action_spec, no dentro de
        `gains`.
      - "cost": {"<recurso>": N, ...} -- recursos de stock del jugador que se
        gastan (ej. Ironworks: {"energy": 4}). La clave especial
        "mc_or_titanium": N -- cuesta N MC, pero el jugador puede cubrir
        parte o todo con titanio (parametro `titanium_to_pay`, valorizado
        igual que al pagar cartas -- ver compute_conversion_rates, asi
        Advanced Alloys tambien lo beneficia) (ej. Rotator Impacts: 6 MC,
        "titanium may be used"). Otra clave especial
        "card_resource" gasta N recursos guardados en la propia carta (ej.
        Regolith Eaters: remover 2 microbios). El VALOR de cualquier clave
        (no solo las especiales de arriba) puede ser el string literal
        "effect_amount" en vez de un N fijo -- costo VARIABLE, X elegido
        por el jugador via `effect_amount` (ej. Hi-Tech Lab, bloque 31:
        gastar X energia sin tope, combinado con gains.start_research.n
        tambien en "effect_amount" para robar esa misma cantidad).
      - "gains": {"resource_deltas": {...}, "production_deltas": {...},
        "raise_oxygen_steps": N, "raise_temperature_steps": N, "raise_venus_steps": N,
        "card_resource_delta": N, "target_card_resource_delta": N,
        "move_from_target_card_resource_delta": N, "tr_delta": N,
        "card_resource_delta_per_tag": {"tag": "<tag>", "per_tag": N
        (default 1)} -- agrega a la PROPIA carta tantos recursos como tags de
        ese tipo tenga el jugador (ej. Kuiper Cooperative: 1 asteroide por
        cada tag space). Version escalada por tags de card_resource_delta,
        analoga a mc_per_tag.
        "raise_global_parameter_without_bonuses": "<parametro>" (sube UN
        paso de "temperature"/"oxygen"/"venus"/"ocean" sin TR, sin bonus de
        umbral y sin disparar pasivos; ej. World Government Advisor, P67 --
        la ELECCION del jugador se modela como una opcion de "choice" por
        parametro, porque effect_choice es el indice de esa lista),
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
        Center); start_research: {"n": N} roba N cartas a pending_research (N
        puede ser el string "effect_amount" para un N variable, ver la
        entrada de "cost" arriba) -- el
        jugador todavia tiene que resolver la compra por separado con
        resolve_research_phase (tipicamente a costo 0, ej. Inventors' Guild: n=1).
        "mc_per_card_resource": {"per_resource": N (default 1), "cap": M
        (opcional)} -- da tanto MC como recursos guardados en la propia
        carta, SIN gastarlos (a diferencia de convert_card_resource_amount,
        que si los gasta), limitado a `cap` si esta presente (ej. Jupiter
        Floating Station: 1 MC por floater guardado, maximo 4).
        "mc_per_card_resource_including_spent": {"per_resource": N (default
        1), "cap": M (opcional)} -- igual que mc_per_card_resource, pero
        pensado para acciones que TAMBIEN gastan 1+ del mismo recurso como
        parte de su "cost" (ej. Saturn Surfing, bloque 32: "spend 1 floater
        to gain 1 M€ per floater here, including the paid one, max 5") --
        suma de vuelta lo gastado (`action_spec["cost"]["card_resource"]`)
        antes de contar, para que el floater pagado SI cuente.
        "mc_per_tag": {"tag": "<tag>", "per_tag": N (default 1)} -- da tanto
        MC como tags de ese tipo tenga el jugador (version de STOCK
        inmediato de production_delta_per_tag, para una accion repetible en
        vez de un efecto de produccion) (ej. Orbital Cleanup, bloque 32: 1
        MC por tag science).
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
        "reveal_top_deck_card_add_resource_if_tag": {"tag": "<tag>"} -- NO
        se procesa aca (necesita el catalogo para leer los tags de la
        carta revelada, mismo criterio que free_trade): `tools.
        use_card_action` la detecta ANTES de llamar a esta funcion, saca la
        primera carta de `player.deck` (la descarta, no vuelve a la mano
        ni al mazo), y si tiene ese tag inyecta un `card_resource_delta: 1`
        equivalente antes de resolver el resto de la accion (ej. Asteroid
        Deflection System, bloque 32: "reveal and discard the top card of
        the deck, if it has a space tag add an asteroid here").
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
        new_active_cards[card_id] = {
            **new_active_cards[card_id], "resources": card_resources, "action_used": True,
        }
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
        gained = effect_amount * spec.get("ratio", 1)
        if gained != int(gained):
            raise CardEffectError(
                f"effect_amount {effect_amount} con ratio {spec.get('ratio', 1)} no da un {to_key} entero"
            )
        new_player[from_key] -= effect_amount
        new_player[to_key] += int(gained)
        new_active_cards[card_id] = {
            **new_active_cards[card_id], "resources": card_resources, "action_used": True,
        }
        new_player["active_cards"] = new_active_cards
        return PlayerState(**new_player), globals_  # type: ignore[typeddict-item]

    for key, amount in action_spec.get("cost", {}).items():
        if key == "card_resource":
            if card_resources < amount:
                raise InsufficientResourcesError(
                    f"'{card_id}' tiene {card_resources} recursos guardados, se necesitan {amount}"
                )
            card_resources -= amount
        elif key == "production_delta":
            # Pagar BAJANDO produccion, no gastando stock (ej. Utopia Invest:
            # "decrease any production to gain 4 resources of that kind"). El
            # piso es el mismo del resto del motor: 0, o -5 para la de MC.
            for prod_key, steps in amount.items():
                floor = MC_PRODUCTION_FLOOR if prod_key == "mc_production" else 0
                if new_player[prod_key] - steps < floor:
                    raise InsufficientResourcesError(
                        f"No se puede bajar {prod_key} {steps} paso(s): esta en "
                        f"{new_player[prod_key]} y el piso es {floor}"
                    )
                new_player[prod_key] -= steps
        elif key == "any_card_resource":
            # Gasta (destruye) recursos guardados en CUALQUIER carta activa
            # elegida con target_card_id -- por defecto la propia. Distinto de
            # "card_resource" (solo la propia) y de
            # move_from_target_card_resource_delta (que los MUEVE en vez de
            # gastarlos). Ej. Floating Refinery: "remove 2 floaters from ANY
            # CARD to gain 1 titanium and 2 M€".
            needed = amount["amount"]
            dest_id = target_card_id if target_card_id is not None else card_id
            if dest_id != card_id and dest_id not in new_active_cards:
                raise CardEffectError(f"La carta objetivo '{dest_id}' no esta activa para este jugador")
            dest_resources = card_resources if dest_id == card_id else new_active_cards[dest_id]["resources"]
            resource_type = amount.get("resource_type")
            if resource_type is not None:
                dest_type = new_active_cards[dest_id].get("resource_type")
                if dest_type != resource_type:
                    raise CardEffectError(f"'{dest_id}' no guarda recursos de tipo '{resource_type}'")
            if dest_resources < needed:
                raise InsufficientResourcesError(
                    f"'{dest_id}' tiene {dest_resources} recursos guardados, se necesitan {needed}"
                )
            if dest_id == card_id:
                card_resources -= needed
            else:
                new_active_cards[dest_id] = {
                    **new_active_cards[dest_id], "resources": dest_resources - needed,
                }
        elif key == "mc_reduced_by_tag":
            # Costo en MC que baja con cada tag jugado, sin tope salvo `min`
            # (ej. Venus Shuttles: 12 MC, -1 por cada tag venus).
            count = new_player["tags_played"].get(amount["tag"], 0)
            mc_needed = max(amount.get("min", 0), amount["base"] - count * amount.get("reduction_per_tag", 1))
            if new_player["mc"] < mc_needed:
                raise InsufficientResourcesError(f"Se necesitan {mc_needed} MC, hay {new_player['mc']}")
            new_player["mc"] -= mc_needed
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
        elif key == "mc_or_steel":
            # Igual que mc_or_titanium pero con acero (ej. St. Joseph of
            # Cupertino Mission: "spend 5 M€, steel may be used").
            if steel_to_pay < 0:
                raise CardEffectError("steel_to_pay no puede ser negativo")
            if new_player["steel"] < steel_to_pay:
                raise InsufficientResourcesError(
                    f"Se necesita {steel_to_pay} de acero, hay {new_player['steel']}"
                )
            steel_value_mc, _ = compute_conversion_rates(PlayerState(**new_player))  # type: ignore[typeddict-item]
            mc_needed = max(0, amount - steel_to_pay * steel_value_mc)
            if new_player["mc"] < mc_needed:
                raise InsufficientResourcesError(f"Se necesita {mc_needed} de MC, hay {new_player['mc']}")
            new_player["steel"] -= steel_to_pay
            new_player["mc"] -= mc_needed
        else:
            # amount == "effect_amount": costo VARIABLE, el jugador elige
            # cuanto gastar de `key` (ej. Hi-Tech Lab: gastar X energia, sin
            # tope fijo -- distinto de convert_resource_amount porque el
            # "destino" de este gasto no es otro recurso numerico sino
            # start_research, ver gains.start_research abajo).
            resolved_amount = effect_amount if amount == "effect_amount" else amount
            if amount == "effect_amount" and (effect_amount is None or effect_amount < 0):
                raise CardEffectError("Esta accion requiere effect_amount (X) >= 0")
            if new_player[key] < resolved_amount:
                raise InsufficientResourcesError(f"Se necesita {resolved_amount} de {key}, hay {new_player[key]}")
            new_player[key] -= resolved_amount

    gains = action_spec.get("gains", {})
    new_globals: dict = dict(globals_)

    for key, delta in gains.get("resource_deltas", {}).items():
        new_player[key] = max(0, new_player[key] + delta)
    for key, delta in gains.get("production_deltas", {}).items():
        new_player = _increase_production(new_player, key, delta)
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
        # Applied Science (P43): "add 1 resource to ANY CARD WITH A RESOURCE"
        # -- el destino tiene que tener ya al menos N recursos guardados,
        # mismo criterio que target_min_resources en apply_card_effect.
        min_target_resources = gains.get("target_min_resources")
        if min_target_resources is not None:
            dest_resources = (
                card_resources if dest_id == card_id
                else new_active_cards.get(dest_id, {}).get("resources", 0)
            )
            if dest_resources < min_target_resources:
                raise CardEffectError(
                    f"La carta objetivo '{dest_id}' tiene {dest_resources} recursos guardados; "
                    f"la accion de '{card_id}' exige al menos {min_target_resources}"
                )
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
    if "requires_zero_resource" in action_spec:
        # Factorum: "increase your energy production 1 step IF YOU HAVE NO
        # ENERGY RESOURCES". Es una condicion sobre el STOCK propio, no sobre
        # tags ni parametros globales, asi que no pasa por
        # check_card_requirements.
        recurso = action_spec["requires_zero_resource"]
        if new_player[recurso] != 0:
            raise CardEffectError(
                f"Esta opcion de '{card_id}' solo esta disponible con 0 de {recurso}; "
                f"el jugador tiene {new_player[recurso]}"
            )
    if "card_resource_delta_per_tag" in gains:
        # Kuiper Cooperative: "add 1 asteroid here for every space tag you
        # have". Version de card_resource_delta escalada por tags, analoga a
        # gains.mc_per_tag.
        spec = gains["card_resource_delta_per_tag"]
        card_resources = card_resources + (
            player["tags_played"].get(spec["tag"], 0) * spec.get("per_tag", 1)
        )
    if "raise_global_parameter_without_bonuses" in gains:
        # World Government Advisor (P67). El parametro NO viaja en
        # effect_choice (que es el INDICE de la lista "choice", un int): cada
        # parametro es una opcion propia de esa lista, y el valor de esta
        # clave dice cual sube.
        new_globals = dict(raise_global_parameter_without_bonuses(
            GlobalParameters(**new_globals), gains["raise_global_parameter_without_bonuses"],  # type: ignore[typeddict-item]
        ))
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
        new_player = _raise_tr(new_player, gains["tr_delta"])
    if "mc_per_counter" in gains:
        new_player["mc"] = new_player["mc"] + new_globals[gains["mc_per_counter"]]
    if "mc_per_card_resource" in gains:
        spec = gains["mc_per_card_resource"]
        counted = min(card_resources, spec["cap"]) if "cap" in spec else card_resources
        new_player["mc"] = new_player["mc"] + counted * spec.get("per_resource", 1)
    if "mc_per_card_resource_including_spent" in gains:
        # Saturn Surfing (X11, bloque 32): "spend 1 floater from here to
        # gain 1 M€ for each floater here, INCLUDING THE PAID FLOATER (max
        # 5)". A diferencia de mc_per_card_resource (que NO gasta nada), el
        # cost.card_resource de esta misma accion ya restó el floater
        # pagado de `card_resources` -- se sabe cuanto se gasto mirando
        # action_spec.get("cost", {}).get("card_resource", 0) y se suma de
        # vuelta antes de contar.
        spec = gains["mc_per_card_resource_including_spent"]
        spent = action_spec.get("cost", {}).get("card_resource", 0)
        counted = card_resources + spent
        if "cap" in spec:
            counted = min(counted, spec["cap"])
        new_player["mc"] = new_player["mc"] + counted * spec.get("per_resource", 1)
    if "mc_per_tag" in gains:
        # Orbital Cleanup (X08, bloque 32): "gain 1 M€ per science tag you
        # have" -- version de use_card_action de production_delta_per_tag,
        # pero como STOCK inmediato de una accion repetible, no produccion.
        spec = gains["mc_per_tag"]
        count = new_player["tags_played"].get(spec["tag"], 0)
        new_player["mc"] = new_player["mc"] + count * spec.get("per_tag", 1)
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
        n_spec = gains["start_research"]["n"]
        n = effect_amount if n_spec == "effect_amount" else n_spec
        if n_spec == "effect_amount" and (effect_amount is None or effect_amount < 0):
            raise CardEffectError("Esta accion requiere effect_amount (X) >= 0")
        new_player = dict(start_research_phase(PlayerState(**new_player), n))  # type: ignore[typeddict-item]
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

    new_active_cards[card_id] = {
            **new_active_cards[card_id], "resources": card_resources, "action_used": True,
        }
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
      - "on_temperature_raised": {"mc_delta": N, "heat_delta": N} -- se suma
        cada vez que el jugador sube la temperatura, UNA VEZ POR PASO
        APLICADO y sin importar la fuente (proyecto estandar Asteroid, una
        carta, una accion, 8 de calor) (ej. Homeostasis Bureau, bloque 36:
        +3 M€). Aplicado directo dentro de raise_temperature, igual que
        on_ocean_placed en place_ocean: si la temperatura ya estaba al
        tope no paga nada, mismo criterio que el TR.
      - "stock_resource_payment": {"resource": "<recurso>", "required_tag":
        "<tag>" (o LISTA, u OMITIDO para cualquier carta), "value_mc": N} --
        habilita pagar cartas con ese
        tag usando un recurso de STOCK del jugador distinto de acero y
        titanio, a N M€ cada uno (ej. Martian Lumber Corp, bloque 36: las
        plantas valen 3 M€ al jugar cartas building). Es la cuarta via de
        pago: acero/titanio estan cableados en el motor, card_resource_payment
        gasta recursos guardados EN UNA CARTA, y esta gasta stock normal.
        La consume `tools.play_card` con el parametro `stock_resource_to_pay`.
        Si `required_tag` NO esta, el recurso paga CUALQUIER carta (ej.
        Helion: "you may use heat as M€", sin restriccion de tag).
      - "optional_energy_to_heat": true -- hace OPCIONAL (unidad por unidad)
        la conversion de energia a calor de la fase de produccion, que la
        regla base aplica entera y sin preguntar (ej. Supercapacitors,
        bloque 35). Lo consume `run_production_phase` via su parametro
        `energy_to_convert`; ver player_has_optional_energy_to_heat.
      - "card_resource_payment": ademas de un tag suelto, `required_tag`
        acepta una LISTA de tags, y alcanza con que la carta pagada tenga
        alguno (ej. Carbon Nanosystems, bloque 35: los graphenes pagan
        cartas con tag space O city). Ver tools._matches_required_tag.
      - "on_card_resource_gained": {"resource_type": "<tipo>", "mc_delta": N
        (default 1)} -- suma N MC por cada unidad de ese tipo de recurso
        que el jugador gane en CUALQUIER carta activa, venga de donde
        venga (ej. Meat Industry, bloque 34: 2 MC por animal; Topsoil
        Contract: 1 MC por microbio). No se resuelve con un enganche por
        cada camino que agrega recursos: tools.play_card/use_card_action
        toman un snapshot con snapshot_card_resource_totals antes de la
        jugada y llaman apply_card_resource_gained_bonuses al final (ver
        esas funciones). Requiere que las cartas que guardan ese recurso
        declaren `active_card_resource_type` -- ver el retrofit de
        microbe/animal en seed_cards.sql.
        Dos claves opcionales: "resource_deltas": {"<recurso>": N, ...} --
        en vez de (o ademas de) MC, suma N de ese recurso por unidad ganada;
        y "own_card_only": true -- solo cuentan los recursos ganados en LA
        CARTA que registro el pasivo, no en cualquier carta del jugador (ej.
        Main Belt Asteroids, P53: "when gaining an asteroid HERE, gain 1
        titanium"). Con own_card_only el delta se mide contra el estado
        previo de esa carta (`active_cards_before`), no contra el total por
        tipo.
      - "on_card_played_cost_threshold_production_delta": {"min_cost": N,
        "production": "<recurso>_production", "delta": M (default 1)} --
        analogo a on_card_played_cost_threshold_draw pero suma produccion
        en vez de robar cartas (ej. Advertising, bloque 32: N=20,
        mc_production +1). Tambien chequeado en tools.play_card.
      - "on_tag_played_resource_delta": {"matching_tags": ["<tag>", ...],
        "resource": "<recurso>", "resource_delta": N} -- suma N de ese
        recurso al STOCK del jugador por cada tag coincidente de la carta
        recien jugada (ej. Albedo Plants: +3 calor por cada tag plant,
        incluida ella misma). Forma general de "on_tag_played_mc_delta"
        (que sigue funcionando y equivale a resource="mc"). Distinto de
        "on_tag_played_add_resource", que suma a la carta activa que tiene
        el pasivo en vez de al stock del jugador.
      - "mc_delta_on_trade": N -- suma N MC cada vez que el jugador
        comercia (ej. Venus Trade Hub: "when you trade, gain 3 M€").
        Aplicado en tools.use_trade_fleet junto al trade income --
        distinto de "trade_cost_discount", que abarata el costo en vez de
        premiar.
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
      - "on_venus_raised": {"mc_delta": N, "heat_delta": N} -- se suma una vez
        por cada PASO de Venus scale realmente aplicado, venga de donde venga
        (ej. Aphrodite: +2 M€). Aplicado dentro de raise_venus, igual que
        on_temperature_raised.
      - "on_new_distinct_tag_played": {"production_deltas": {...},
        "resource_deltas": {...}} -- se dispara una vez por cada tag que el
        jugador ve por PRIMERA VEZ en la partida; los eventos no cuentan
        (ej. Aridor: +1 produccion de M€). Ver apply_new_distinct_tag_bonuses,
        llamado desde tools.play_card ANTES de increment_tags_played.
      - "on_cost_threshold_paid": {"min_cost": N, "mc_delta": M} -- se suma
        despues de pagar una carta O un proyecto estandar cuyo costo BASICO
        (impreso/de tabla) llegue a N (ej. CrediCor: 20+ M€ -> +4 M€). Ver
        apply_cost_threshold_mc_bonuses.
      - "standard_project_card_resource_payment": {"resource_type":
        "<tipo>", "applies_to": ["<proyecto>", ...], "value_mc": N (default
        1)} -- habilita pagar ESOS proyectos estandar con los recursos
        guardados en una carta activa de ese tipo (ej. Kuiper Cooperative:
        cada asteroide vale 1 M€ para Asteroid y Aquifer). Distinto de
        card_resource_payment, que paga CARTAS con cierto tag. Lo consume
        tools.use_standard_project con el parametro `card_resource_to_pay`.
      - "ocean_adjacency_bonus_mc": N -- sube a N (default 2) los M€ que da
        cada oceano adyacente al colocar un tile (ej. Lakefront Resorts: 3).
        Ver ocean_adjacency_bonus_mc.
      - "on_hex_bonus_tile_placed": {"matching_resources": ["steel",
        "titanium"], "production_deltas": {...}, "resource_deltas": {...}} --
        se dispara al colocar un tile sobre un hexagono cuyo bonus impreso
        incluya alguno de esos recursos (ej. Mining Guild: +1 produccion de
        acero). Ver apply_hex_bonus_tile_bonuses, llamado desde
        tools._apply_hex_bonus.
      - "plants_per_greenery": N -- baja a N las plantas que cuesta convertir
        a greenery (ej. EcoLine: 7 en vez de 8). Ver plants_per_greenery.
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
      - "on_production_phase_if_tr_not_raised": {"mc_delta": N,
        "card_resource_delta": M} -- se cobra DENTRO de run_production_phase,
        y solo si el jugador NO subio su TR en esa generacion (ej. Pristar:
        +6 M€ y +1 preservation). Lee `tr_raised_this_generation` ANTES del
        reset; ver el comentario en run_production_phase, que explica por que
        el orden importa.
      - "on_tag_played_conditional_by_own_resource": {"matching_tags":
        ["<tag>", ...], "resource_threshold": N (default 1), "if_at_least":
        {"card_resource_delta": M, "tr_delta": K}, "if_below": {...}} -- la
        rama "if_at_least" se aplica sola cuando la carta tiene al menos N
        recursos guardados; la rama "if_below" es OPCIONAL y la cobra la tool
        retire_card_as_event, porque ademas retira la carta (ej. Pharmacy
        Union: con diseases, -1 disease y +1 TR; sin ninguno, el jugador puede
        llevarse 3 TR y mandarla a la pila de eventos).
      - "on_card_played_tag_count_resource_delta": {"count": N, "resource":
        "<recurso>", "resource_delta": M} (o una LISTA de specs) -- paga por
        la CANTIDAD EXACTA de tags de la carta jugada, no por cuales son (ej.
        Sagitta Frontier Services: 4 M€ por carta sin tags, 1 M€ por carta de
        exactamente 1 tag). Hermana de on_card_played_min_tags_add_resource
        (Spire), que usa un minimo en vez de una cantidad exacta.
      - "card_resource_as_heat": {"resource_type": "<tipo>", "heat_value": N}
        -- los recursos guardados en esa carta activa se pueden gastar como
        CALOR, a N cada uno (ej. Stormcraft Incorporated: floaters a 2). No es
        una via de pago mas: el calor no compra nada, se gasta en los dos
        unicos sumideros del motor (convertir 8 en temperatura, y las acciones
        con cost.heat), asi que se acredita antes de que esos cobren. Ver
        spend_card_resource_as_heat y el parametro `card_resources_as_heat` de
        tools.convert_resources / tools.use_card_action.
      - "on_build_on_own_community": {"mc_delta": N} -- N M€ al colocar un
        tile sobre un hexagono que el jugador tenia reservado con un marcador
        de "community" (ej. Arcadian Communities: 3). Ver board.place_community
        y tools._apply_community_build_bonus, enganchado en las tres vias de
        colocacion real en el mapa.
      - "standard_project_discount_mc": {"projects": ["<nombre>", ...]
        (opcional: sin el campo vale para todos), "amount": N} -- paga N M€
        menos por esos proyectos estandar (ej. Thorgate, corporaciones
        bloque 5: -3 M€ en el proyecto power_plant, ademas del descuento en
        cartas con tag power que ya da card_cost_discount_mc). Ver
        compute_standard_project_discount, consumido por
        tools.use_standard_project.
      - "on_city_tile_placed_resource_delta": {"<recurso>": N, ...} -- suma
        al STOCK del jugador al colocarse una ciudad en el mapa, a
        diferencia de on_city_tile_placed_add_resource, que suma a la carta
        activa (ej. Tharsis Republic, corporaciones bloque 5: +3 M€). Ver
        apply_city_placed_bonuses.
      - "venus_requirements_tolerance_steps": N -- como
        global_requirements_tolerance_steps pero SOLO para los requisitos de
        Venus (ej. Morning Star Inc, corporaciones bloque 3: "your Venus
        requirements are +/- 2 steps, your choice in each case"). Se separa
        porque el pasivo general relaja tambien temperatura/oxigeno/oceanos,
        que esta carta no toca. Ver check_card_requirements.
      - "on_event_played" acepta ademas "resource_deltas": {"<recurso>": N}
        -- forma generica para recursos que no son M€ ni calor, sin agregar
        un "<recurso>_delta" hardcodeado por cada uno (ej. Palladin
        Shipping, corporaciones bloque 3: "when you play a space event, gain
        1 titanium", con tag_filter "space").
      - "on_tag_played_production_delta": {"matching_tags": ["<tag>", ...],
        "production": "<recurso>_production", "production_delta": N
        (default 1)} -- misma familia que on_tag_played_resource_delta pero
        sobre PRODUCCION en vez de stock (ej. Saturn Systems, corporaciones
        bloque 4: "each time any Jovian tag is put into play, including
        this, increase your M€ production 1 step"). Pasa por
        _increase_production, asi que se combina con Manutech.
      - "on_tag_played_draw_cards": {"matching_tags": ["<tag>", ...],
        "cards": N (default 1)} -- roba N cartas por cada tag coincidente de
        la carta recien jugada, AUTOMATICO (a diferencia de
        on_any_tag_played_choice, que es una eleccion) (ej. Point Luna,
        corporaciones bloque 3: "when you play an Earth tag, including this,
        draw a card").
      - "on_card_played_min_tags_add_resource": {"min_tags": N (default 2),
        "resource_delta": M (default 1)} -- suma M recursos a la propia
        carta activa cuando la carta recien jugada trae AL MENOS N tags. No
        mira cuales son los tags sino cuantos, asi que dispara una sola vez
        por carta (ej. Spire, corporaciones bloque 4: "when you play a card
        with at least 2 tags, add 1 science resource here").
      - "on_colony_placed": {"production_deltas": {...}, "resource_deltas":
        {...}} -- se dispara cada vez que se coloca una colonia, sin importar
        la fuente (proyecto estandar, efecto de carta, prelude) (ej.
        Poseidon, corporaciones bloque 3: +1 produccion de M€). Ver
        apply_colony_placed_bonuses, llamado desde tools.build_colony y
        desde las dos vias de carta que construyen colonia.
      - "research_cost_delta_mc": N -- corre lo que cuesta comprar cada carta
        en la fase de investigacion (default RESEARCH_PHASE_COST_MC = 3): +2
        en Polyphemos ("pay 5 M€ instead of 3"), -2 en TerraLabs Research
        ("buying cards to hand costs 1 M€"). Ver
        compute_research_cost_per_card, consumido por
        tools.resolve_research_phase. Una fase GRATUITA (Inventors' Guild,
        costo 0) no se toca.
      - "on_production_increased": true -- cada vez que CUALQUIER produccion
        del jugador sube, sin excepcion (proyecto estandar, production_deltas,
        production_delta_per_tag, etc. -- cualquier via, incluida M€), gana
        tambien esa cantidad de unidades del recurso correspondiente en
        stock (ej. Manutech, corporaciones bloque 2: texto literal "for each
        step you increase the production of a resource, including this, you
        also gain that resource", sin excepcion de M€). Aplicado dentro de
        _increase_production, el unico punto por el que pasan todos los
        aumentos de produccion del motor -- no hace falta cablearlo en cada
        efecto.

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


def compute_card_cost_discount(
    player: PlayerState, card_tags: tuple[str, ...], has_requirement: bool = False,
) -> int:
    """
    Suma los descuentos de costo ("card_cost_discount_mc") de todos los
    efectos pasivos activos del jugador que apliquen a esta carta (segun
    `tag_filter`, si el efecto lo tiene) (ej. Mass Converter: -2 MC en
    cartas con tag "space"). `tag_filter` puede ser un tag suelto o una
    LISTA de tags, en cuyo caso alcanza con que la carta tenga alguno (ej.
    Space Lanes: "planet tag" = jovian/earth/venus). Se resta del costo antes de calcular el pago
    en tools.play_card -- nunca deja el costo por debajo de 0.

    `requires_requirement`: bool en el efecto -- en vez de filtrar por tag,
    filtra por si la carta jugada TIENE algun `requirements` propio (ej.
    Cutting Edge Technology, bloque 33: -2 MC en cartas con requisito,
    sin importar sus tags). Necesita `has_requirement` (si `cards.
    requirements` de la carta jugada no es null/vacio), que tools.play_card
    calcula del catalogo.
    """
    discount = 0
    for effect in player["passive_effects"]:
        bonus = effect.get("card_cost_discount_mc")
        if bonus is None:
            continue
        if effect.get("requires_requirement") and not has_requirement:
            continue
        tag_filter = effect.get("tag_filter")
        # `tag_filter` acepta un tag suelto o una LISTA (ej. Space Lanes:
        # "planet tag" son tres tags distintos -- jovian/earth/venus).
        if isinstance(tag_filter, list):
            tag_filter = None if any(t in card_tags for t in tag_filter) else "__no_match__"
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


def retire_card_as_event(player: PlayerState, card_id: str) -> PlayerState:
    """
    Retira una carta activa "a la pila de eventos": la saca de `active_cards`
    y de `passive_effects` (deja de estar en juego), y aplica el `tr_delta`
    que declare la rama `if_below` de su pasivo
    "on_tag_played_conditional_by_own_resource".

    La usa Pharmacy Union: *"if there are no diseases here, you MAY raise your
    TR 3 steps and place this card in your event pile. It now counts as a
    played event."* Es la rama OPCIONAL, por eso vive en su propia funcion en
    vez de dispararse sola dentro de apply_tag_played_resource_bonuses.

    `played_cards` no se toca: la carta ya figura ahi desde que se jugo, y ese
    historial es justamente lo que el motor entiende por "pila de eventos"
    (ver el effect retrieve_played_events_to_hand de Astra Mechanica). Sumar
    la carta al contador global `events_played` es responsabilidad del caller
    (tools), que es quien tiene el estado compartido.

    Lanza CardEffectError si la carta no esta activa, si no tiene el pasivo, o
    si todavia le quedan recursos guardados (la rama opcional exige 0).
    """
    if card_id not in player["active_cards"]:
        raise CardEffectError(f"La carta '{card_id}' no esta activa para este jugador")
    spec = next(
        (e.get("on_tag_played_conditional_by_own_resource") for e in player["passive_effects"]
         if e["card_id"] == card_id and "on_tag_played_conditional_by_own_resource" in e),
        None,
    )
    if spec is None:
        raise CardEffectError(f"La carta '{card_id}' no se puede retirar a la pila de eventos")
    if player["active_cards"][card_id]["resources"] >= spec.get("resource_threshold", 1):
        raise CardEffectError(
            f"'{card_id}' todavia guarda recursos: esta rama solo aplica cuando no le queda ninguno"
        )

    branch = spec.get("if_below", {})
    new_player: dict = {
        **player,
        "active_cards": {k: v for k, v in player["active_cards"].items() if k != card_id},
        "passive_effects": [e for e in player["passive_effects"] if e["card_id"] != card_id],
    }
    return PlayerState(**_raise_tr(new_player, branch.get("tr_delta", 0)))  # type: ignore[typeddict-item]


def spend_card_resource_as_heat(player: PlayerState, amount: int) -> PlayerState:
    """
    Gasta `amount` recursos guardados en la carta activa que tenga el pasivo
    "card_resource_as_heat": {"resource_type": "<tipo>", "heat_value": N} y
    acredita su equivalente en CALOR (ej. Stormcraft Incorporated: "floaters
    on this card may be used as 2 heat each").

    A diferencia de las otras vias de pago (que pagan CARTAS o PROYECTOS
    ESTANDAR), esta acredita calor de stock: el calor no se usa para comprar
    nada, se gasta en los dos unicos sumideros del motor -- convertir 8 calor
    en un paso de temperatura, y las acciones de carta con `cost.heat`. Por
    eso alcanza con acreditarlo ANTES de que esos dos caminos cobren, en vez
    de agregar una sexta via de pago generica: el calor acreditado se gasta
    solo, por el camino de siempre.

    Lanza CardEffectError si el jugador no tiene el pasivo, e
    InsufficientResourcesError si la carta no tiene tantos recursos.
    """
    if amount <= 0:
        return player
    for effect in player["passive_effects"]:
        spec = effect.get("card_resource_as_heat")
        if spec is None:
            continue
        card_id = effect["card_id"]
        available = player["active_cards"].get(card_id, {}).get("resources", 0)
        if available < amount:
            raise InsufficientResourcesError(
                f"'{card_id}' tiene {available} {spec.get('resource_type', 'recurso')}(s), "
                f"se quisieron gastar {amount}"
            )
        new_player = spend_active_card_resource(player, card_id, amount)
        return {**new_player, "heat": new_player["heat"] + amount * spec.get("heat_value", 1)}
    raise CardEffectError(
        "Ningun efecto pasivo del jugador permite usar recursos de carta como calor"
    )


def compute_standard_project_discount(player: PlayerState, project_name: str) -> int:
    """
    Descuento en M€ que tiene ESTE jugador sobre el costo de un proyecto
    estandar puntual, por el pasivo "standard_project_discount_mc":
    {"projects": ["power_plant", ...], "amount": N} (ej. Thorgate: "when
    playing a power card OR THE STANDARD PROJECT POWER PLANT, you pay 3 M€
    less for it" -- la mitad de las cartas la cubre card_cost_discount_mc,
    esta es la otra mitad). Si el pasivo no trae "projects", vale para
    todos. Se suman varios; el costo nunca baja de 0 (lo acota el caller).
    """
    discount = 0
    for effect in player["passive_effects"]:
        spec = effect.get("standard_project_discount_mc")
        if spec is None:
            continue
        projects = spec.get("projects")
        if projects is None or project_name in projects:
            discount += spec.get("amount", 0)
    return discount


def compute_research_cost_per_card(
    player: PlayerState, base_cost: int = RESEARCH_PHASE_COST_MC
) -> int:
    """
    Cuanto le cuesta a ESTE jugador comprar una carta en la fase de
    investigacion. Por defecto RESEARCH_PHASE_COST_MC (3), pero el pasivo
    "research_cost_delta_mc" lo corre (ej. Polyphemos: +2, paga 5; TerraLabs
    Research: -2, paga 1). Nunca baja de 0.

    `base_cost` 0 (fases GRATUITAS como la de Inventors' Guild) no se toca:
    una accion que regala la carta la sigue regalando, el pasivo solo mueve
    el precio de la investigacion que efectivamente se paga.
    """
    if base_cost <= 0:
        return base_cost
    delta = 0
    for effect in player["passive_effects"]:
        delta += effect.get("research_cost_delta_mc", 0)
    return max(0, base_cost + delta)


def apply_colony_placed_bonuses(player: PlayerState) -> PlayerState:
    """
    Aplica el pasivo "on_colony_placed": {"production_deltas": {...},
    "resource_deltas": {...}} -- se dispara cada vez que se coloca una
    colonia, sin importar la fuente (proyecto estandar build_colony, un
    efecto de carta, el setup de la propia corporacion) (ej. Poseidon:
    "when any colony is placed, including this, raise your M€ production 1
    step"). Mismo criterio que on_ocean_placed: el hook vive en un solo
    lugar (tools.build_colony y el efecto build_colony de una carta) para
    que todos los caminos se beneficien.
    """
    new_player: dict = dict(player)
    changed = False
    for effect in player["passive_effects"]:
        spec = effect.get("on_colony_placed")
        if spec is None:
            continue
        for key, delta in spec.get("resource_deltas", {}).items():
            new_player[key] = max(0, new_player[key] + delta)
            changed = True
        for key, delta in spec.get("production_deltas", {}).items():
            new_player = _increase_production(new_player, key, delta)
            changed = True
    return PlayerState(**new_player) if changed else player  # type: ignore[typeddict-item]


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
        # El tag_filter puede vivir DENTRO del bonus, no solo al nivel del
        # pasivo: hace falta cuando una misma carta registra dos pasivos con
        # filtros distintos (ej. Solar Logistics, bloque 36: descuento en
        # cartas "earth" Y robo al jugar un evento "space" -- un solo
        # tag_filter compartido no alcanzaria).
        tag_filter = bonus.get("tag_filter", effect.get("tag_filter"))
        if tag_filter is not None and tag_filter not in played_card_tags:
            continue
        new_player["mc"] = new_player["mc"] + bonus.get("mc_delta", 0)
        new_player["heat"] = new_player["heat"] + bonus.get("heat_delta", 0)
        # Forma generica para cualquier otro recurso, sin tener que agregar un
        # "<recurso>_delta" hardcodeado por cada uno (ej. Palladin Shipping,
        # corporaciones bloque 3: "when you play a space event, gain 1
        # titanium").
        for key, delta in bonus.get("resource_deltas", {}).items():
            new_player[key] = max(0, new_player[key] + delta)
        # Solar Logistics (X63, bloque 36): "when any player plays a space
        # event, draw 1 card" -- mismo pasivo, pero robando en vez de sumar
        # recursos. En single-player "any player" es el propio jugador.
        if bonus.get("draw_cards"):
            new_player = dict(draw_cards_to_hand(PlayerState(**new_player), bonus["draw_cards"]))  # type: ignore[typeddict-item]
    return PlayerState(**new_player)  # type: ignore[typeddict-item]


def apply_new_distinct_tag_bonuses(
    player: PlayerState, played_card_tags: tuple[str, ...], is_event: bool = False,
) -> PlayerState:
    """
    Aplica el pasivo "on_new_distinct_tag_played": {"production_deltas": {...}}
    -- se dispara UNA VEZ por cada tag que el jugador ve por PRIMERA VEZ en la
    partida (ej. Aridor: "when you get a new type of tag in play, increase your
    M€ production 1 step"). Los eventos NO cuentan: `is_event=True` no dispara
    nada (regla impresa en la propia carta).

    Hay que llamarla ANTES de increment_tags_played, que es lo que convierte un
    tag en "ya visto". Un tag repetido de la misma carta cuenta una sola vez.
    """
    if is_event:
        return player
    specs = [e["on_new_distinct_tag_played"] for e in player["passive_effects"]
             if "on_new_distinct_tag_played" in e]
    if not specs:
        return player
    nuevos = {tag for tag in played_card_tags if player["tags_played"].get(tag, 0) == 0}
    if not nuevos:
        return player
    new_player: dict = dict(player)
    for spec in specs:
        for key, delta in spec.get("production_deltas", {}).items():
            new_player = _increase_production(new_player, key, delta * len(nuevos))
        for key, delta in spec.get("resource_deltas", {}).items():
            new_player[key] = new_player[key] + delta * len(nuevos)
    return PlayerState(**new_player)  # type: ignore[typeddict-item]


def apply_cost_threshold_mc_bonuses(player: PlayerState, basic_cost: int) -> PlayerState:
    """
    Aplica el pasivo "on_cost_threshold_paid": {"min_cost": N, "mc_delta": M}
    -- se dispara despues de pagar una carta O un proyecto estandar cuyo costo
    BASICO (impreso / de tabla, antes de descuentos) llegue a `min_cost`
    (ej. CrediCor: "after you pay for a card or standard project with a basic
    cost of 20 M€ or more, you gain 4 M€").

    Es la union de on_card_played_cost_threshold_draw (que solo mira cartas y
    solo roba) con on_standard_project_used (que solo mira proyectos y no tiene
    umbral). Se llama desde tools.play_card y tools.use_standard_project.
    """
    gained = 0
    for effect in player["passive_effects"]:
        spec = effect.get("on_cost_threshold_paid")
        if spec is None:
            continue
        if basic_cost >= spec["min_cost"]:
            gained += spec.get("mc_delta", 0)
    if gained == 0:
        return player
    return PlayerState(**{**player, "mc": player["mc"] + gained})  # type: ignore[typeddict-item]


def apply_corporation_start(player: PlayerState, starting_mc: int) -> PlayerState:
    """
    Deja al jugador en el estado de arranque de una CORPORACION: `starting_mc`
    de M€ y produccion 0 en los seis recursos.

    El rulebook oficial dice, en el setup: "You start with 1 production of each
    resource on the player board... (ONLY IN STANDARD GAME.)" -- o sea, esa
    produccion 1 es de la partida ESTANDAR (la de Beginner Corporation). En una
    partida con corporaciones se arranca en 0 y la corporacion otorga lo que
    diga su carta. Por eso Beginner Corporation se carga con production_deltas
    +1 en cada recurso: asi reproduce la partida estandar sin caso especial en
    el codigo.

    No toca TR, mazo, mano ni tags: solo M€ y produccion.
    """
    return PlayerState(**{
        **player,
        "mc": starting_mc,
        "mc_production": 0, "steel_production": 0, "titanium_production": 0,
        "plant_production": 0, "energy_production": 0, "heat_production": 0,
    })  # type: ignore[typeddict-item]


OCEAN_ADJACENCY_BONUS_MC = 2   # M€ por cada oceano adyacente al colocar un tile


def ocean_adjacency_bonus_mc(player: PlayerState) -> int:
    """
    Cuanto vale para ESTE jugador cada oceano adyacente al colocar un tile.
    Por defecto 2 (regla base); el pasivo "ocean_adjacency_bonus_mc" lo sube
    (ej. Lakefront Resorts: 3). Si hubiera varios, gana el mas alto.
    """
    value = OCEAN_ADJACENCY_BONUS_MC
    for effect in player["passive_effects"]:
        override = effect.get("ocean_adjacency_bonus_mc")
        if override is not None:
            value = max(value, override)
    return value


def apply_hex_bonus_tile_bonuses(
    player: PlayerState, hex_bonus: list[tuple[str, int]],
) -> PlayerState:
    """
    Aplica el pasivo "on_hex_bonus_tile_placed": {"matching_resources":
    [...], "production_deltas": {...}} -- se dispara al colocar un tile sobre
    un hexagono cuyo BONUS IMPRESO incluya alguno de esos recursos (ej. Mining
    Guild: acero o titanio -> +1 produccion de acero).

    Dispara UNA vez por colocacion aunque el hex de varios recursos que
    matcheen. Se llama desde tools._apply_hex_bonus, que es el unico punto por
    donde pasan todos los caminos de colocacion (oceano, ciudad, greenery,
    special tile).
    """
    recursos = {resource for resource, _ in hex_bonus}
    new_player: dict = dict(player)
    for effect in player["passive_effects"]:
        spec = effect.get("on_hex_bonus_tile_placed")
        if spec is None:
            continue
        if not recursos & set(spec.get("matching_resources", [])):
            continue
        for key, delta in spec.get("production_deltas", {}).items():
            new_player = _increase_production(new_player, key, delta)
        for key, delta in spec.get("resource_deltas", {}).items():
            new_player[key] = new_player[key] + delta
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

    Tambien resuelve las variantes que premian con PRODUCCION
    ("on_tag_played_production_delta", ej. Saturn Systems) y las que miran la
    CANTIDAD de tags de la carta jugada en vez de cuales son
    ("on_card_played_min_tags_add_resource", ej. Spire).
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

    # Acumulador de TR de los pasivos por tag (ej. Pharmacy Union). Se aplica
    # al final via _raise_tr, para que marque tr_raised_this_generation.
    tr_gains = 0

    # Spire: "when you play a card with AT LEAST 2 tags, add 1 science resource
    # here". No mira CUALES son los tags -- mira cuantos trae la carta jugada,
    # asi que dispara una sola vez por carta, no una vez por tag.
    for effect in player["passive_effects"]:
        spec = effect.get("on_card_played_min_tags_add_resource")
        if spec is None:
            continue
        target_card_id = effect["card_id"]
        if target_card_id not in new_active_cards:
            continue
        if len(played_card_tags) >= spec.get("min_tags", 2):
            current_res = new_active_cards[target_card_id]["resources"]
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": current_res + spec.get("resource_delta", 1),
            }
            changed = True

    # Variante que premia con MC al JUGADOR en vez de sumar recursos a una
    # carta activa (ej. GMO Contract: "each time you play a plant, animal or
    # microbe tag, including this, gain 2 M€"). El FAQ aclara que cada tag
    # distinto de la misma carta dispara por separado -- por eso se cuenta
    # `matches`, no un booleano.
    stock_gains: dict[str, int] = {}
    for effect in player["passive_effects"]:
        # "on_tag_played_mc_delta" es la forma vieja, equivalente a
        # on_tag_played_resource_delta con resource="mc".
        spec = effect.get("on_tag_played_resource_delta") or effect.get("on_tag_played_mc_delta")
        if spec is None:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        matches = sum(1 for t in played_card_tags if t in matching_tags)
        if not matches:
            continue
        key = spec.get("resource", "mc")
        amount = spec.get("resource_delta", spec.get("mc_delta", 0))
        stock_gains[key] = stock_gains.get(key, 0) + matches * amount

    # Misma familia, pero sobre PRODUCCION en vez de stock (ej. Saturn Systems:
    # "each time any Jovian tag is put into play, including this, increase your
    # M€ production 1 step"). Pasa por _increase_production como todo el resto
    # del motor, asi que se combina bien con Manutech.
    production_gains: list[tuple[str, int]] = []
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_production_delta")
        if spec is None:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        matches = sum(1 for t in played_card_tags if t in matching_tags)
        if matches:
            production_gains.append((spec["production"], matches * spec.get("production_delta", 1)))

    # Pharmacy Union: "when you play a science tag, remove 1 disease from here
    # and raise your TR 1 step, OR, if there are no diseases here, you may
    # raise your TR 3 steps and place this card in your event pile". La rama
    # AUTOMATICA (hay recursos) se resuelve aca; la otra es OPCIONAL y ademas
    # retira la carta, asi que se cobra con la tool retire_card_as_event --
    # mismo criterio que on_ocean_placed_offer, que tampoco se puede resolver
    # dentro de un camino que corre sin interaccion.
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_conditional_by_own_resource")
        if spec is None:
            continue
        target_card_id = effect["card_id"]
        if target_card_id not in new_active_cards:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        matches = sum(1 for t in played_card_tags if t in matching_tags)
        if not matches:
            continue
        branch = spec.get("if_at_least")
        if branch is None:
            continue
        for _ in range(matches):
            current_res = new_active_cards[target_card_id]["resources"]
            if current_res < spec.get("resource_threshold", 1):
                break
            new_active_cards[target_card_id] = {
                **new_active_cards[target_card_id],
                "resources": current_res + branch.get("card_resource_delta", 0),
            }
            tr_gains += branch.get("tr_delta", 0)
            changed = True

    # Sagitta Frontier Services: "when you play a card with NO TAGS, including
    # this, gain 4 M€. When you play a card with EXACTLY 1 TAG, gain 1 M€".
    # Misma familia que on_card_played_min_tags_add_resource (Spire), pero
    # sobre cantidad EXACTA y pagando al stock: por eso acepta una lista de
    # specs, una por cada cantidad de tags premiada.
    for effect in player["passive_effects"]:
        spec = effect.get("on_card_played_tag_count_resource_delta")
        if spec is None:
            continue
        for entry in (spec if isinstance(spec, list) else [spec]):
            if len(played_card_tags) == entry["count"]:
                key = entry.get("resource", "mc")
                stock_gains[key] = stock_gains.get(key, 0) + entry.get("resource_delta", 0)

    # Point Luna: "when you play an Earth tag, including this, draw a card".
    # Automatico, no una eleccion (a diferencia de on_any_tag_played_choice).
    cards_to_draw = 0
    for effect in player["passive_effects"]:
        spec = effect.get("on_tag_played_draw_cards")
        if spec is None:
            continue
        matching_tags = set(spec.get("matching_tags", []))
        matches = sum(1 for t in played_card_tags if t in matching_tags)
        cards_to_draw += matches * spec.get("cards", 1)

    if not changed and not stock_gains and not production_gains and not cards_to_draw and not tr_gains:
        return player
    new_player = {**player, "active_cards": new_active_cards}
    for key, amount in stock_gains.items():
        new_player[key] = max(0, new_player[key] + amount)
    for key, amount in production_gains:
        new_player = _increase_production(new_player, key, amount)
    if cards_to_draw:
        new_player = dict(draw_cards_to_hand(PlayerState(**new_player), cards_to_draw))  # type: ignore[typeddict-item]
    if tr_gains:
        new_player = _raise_tr(new_player, tr_gains)
    return new_player


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
      - "on_city_tile_placed_resource_delta": {"<recurso>": N, ...} -- suma
        al STOCK del jugador, no a una carta activa (ej. Tharsis Republic,
        corporaciones bloque 5: "when you place a city tile, gain 3 M€").
        La carta distingue "when YOU place" de "when ANY city tile is
        placed", pero este motor es de UN jugador y este hook solo corre
        para ciudades reales del mapa (ver de donde se llama), asi que los
        dos disparadores coinciden -- las ciudades fuera del tablero (ej.
        Phobos Space Haven) no pasan por aca ni por el otro.
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
        stock_spec = effect.get("on_city_tile_placed_resource_delta")
        if stock_spec is not None:
            for key, delta in stock_spec.items():
                new_player[key] = max(0, new_player[key] + delta)
            changed = True
        production_spec = effect.get("on_city_tile_placed_production_delta")
        if production_spec is not None:
            key = production_spec["production"]
            new_player = _increase_production(new_player, key, production_spec.get("per_tile", 1))
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
    player: PlayerState, played_card_id: str, played_card_tags: tuple[str, ...], choice: str | None,
    target_card_id: str | None = None,
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

    Con "add_resource_choice": {"target_any_card": true} el destino deja de
    ser la carta recien jugada y pasa a ser el `target_card_id` que elige el
    jugador (ej. Ecotec: "gain 1 plant OR add 1 microbe to ANY CARD").

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
            add_spec = spec.get("add_resource_choice", {})
            # Ecotec: "add 1 microbe to ANY card" -- el destino lo elige el
            # jugador (`target_card_id`), no es la carta recien jugada como en
            # Viral Enhancers.
            destino = target_card_id if add_spec.get("target_any_card") else played_card_id
            if destino is None or destino not in player["active_cards"]:
                raise CardEffectError(
                    f"'{destino}' no tiene caja de recursos, no se le puede agregar recurso"
                )
            amount = add_spec.get("resource_delta", 1)
            current_res = player["active_cards"][destino]["resources"]
            new_active_cards = {
                **player["active_cards"],
                destino: {
                    **player["active_cards"][destino],
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
