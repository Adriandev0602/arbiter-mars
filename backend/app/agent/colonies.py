"""
Mecanica de colonias/comercio de la expansion Colonies. Funciones puras,
mismo estilo que board.py -- sin dependencias de FastAPI/Supabase.

Fuente del MECANISMO (costos, orden de pasos, reglas de colocacion y
comercio): rulebook oficial de la expansion (fryxgames.se,
TM_COLONIES_ENG_RULES, 4 paginas, leido completo) -- alta confianza, fuente
primaria. Los numeros verificados de ahi:
  - Construir colonia (proyecto estandar): 17 MC.
  - Comerciar (accion, no proyecto estandar): 9 MC, o 3 energia, o 3 titanio
    (eleccion del jugador).
  - Maximo 3 colonias (de cualquier jugador) por Colony Tile; cada jugador
    solo 1 colonia por tile.
  - Al comerciar: se da el "trade income" segun la posicion actual del
    marcador blanco en el track, MAS el "colony bonus" a TODOS los duenos
    de esa colonia (no solo a quien comercia). Despues, el marcador blanco
    baja al lado de las colonias construidas (o al fondo si no hay ninguna).
  - Fase solar (fin de generacion): el marcador blanco sube 1 paso en CADA
    Colony Tile en juego, y todas las flotas de comercio vuelven a estar
    disponibles.

CATALOGO DE COLONIAS: el juego real tiene 11 Colony Tiles con nombre
(Ganymede, Europa, Callisto, Titan, Enceladus, Triton, Miranda, Luna, Pluto,
Ceres, Io). Hoy hay **9 cargadas**; faltan Pluto y Europa (ver la nota al
final de COLONY_DEFS).

Callisto se habia cargado antes verificandola con dos fuentes independientes
(el ejemplo trabajado del rulebook oficial, pagina 2, y un resumen de
terceros que reporta el mismo track). Las otras 8 se transcribieron del SCAN
de cada Colony Tile -- la fuente primaria, el tile impreso mismo. Callisto
sirvio de CONTROL del metodo: leida del scan da exactamente los valores que
ya estaban verificados por esas dos fuentes (colony bonus 3 energia, track
0/2/3/5/7/10/13, placement +1 produccion de energia), asi que la lectura de
los otros scans se apoya en un metodo ya validado.

Como leer un Colony Tile, por si hay que agregar mas:
  - "COLONY BONUS": iconos sueltos = recursos de stock para TODOS los duenos.
  - "TRADE INCOME": "X <recurso>", donde X sale de la casilla actual del track.
  - Fila de 7 casillas con sus numeros abajo = el track.
  - Los 3 PRIMEROS espacios de esa fila son los colony spots, y su icono es
    el placement bonus. Un icono DENTRO de un marco marron/dorado es
    PRODUCCION; el mismo icono sin marco es recurso de stock (comparar
    Callisto, que da produccion, con Triton, que da 3 titanios de stock).
"""
from typing import TypedDict

BUILD_COLONY_COST_MC = 17
TRADE_COST_MC = 9
TRADE_COST_ENERGY = 3
TRADE_COST_TITANIUM = 3
MAX_COLONISTS_PER_TILE = 3


class ColonyDef(TypedDict):
    """Definicion ESTATICA de una Colony Tile -- nunca cambia durante la partida."""
    id: str
    income_type: str  # clave de PlayerState que recibe el trade income (ej. "energy")
    track: list[int]  # valor de trade income en cada posicion del track, index 0..N
    colony_bonus: dict  # {"<recurso>": N} -- se da a TODOS los duenos de la colonia al comerciar
    placement_bonus: dict  # {"<recurso>_production": N} -- se da UNA VEZ al construir


COLONY_DEFS: dict[str, ColonyDef] = {
    "callisto": ColonyDef(
        id="callisto", income_type="energy", track=[0, 2, 3, 5, 7, 10, 13],
        colony_bonus={"energy": 3}, placement_bonus={"energy_production": 1},
    ),
    # Las 5 de abajo se transcribieron del SCAN de cada Colony Tile (fuente
    # primaria: el tile mismo). Callisto sirvio de control: leida del scan da
    # exactamente los valores que ya estaban verificados con dos fuentes
    # independientes, asi que el metodo de lectura es confiable. Anatomia del
    # tile: "COLONY BONUS" (iconos sueltos = stock del jugador), "TRADE
    # INCOME" (X + recurso), la fila de 7 casillas del track con sus numeros
    # abajo, y los 3 primeros espacios -- los colony spots -- cuyo icono es el
    # placement bonus. Un icono DENTRO de un marco marron/dorado es
    # PRODUCCION; sin marco es recurso de stock.
    "ceres": ColonyDef(
        id="ceres", income_type="steel", track=[1, 2, 3, 4, 6, 8, 10],
        colony_bonus={"steel": 2}, placement_bonus={"steel_production": 1},
    ),
    "ganymede": ColonyDef(
        id="ganymede", income_type="plants", track=[0, 1, 2, 3, 4, 5, 6],
        colony_bonus={"plants": 1}, placement_bonus={"plant_production": 1},
    ),
    "io": ColonyDef(
        id="io", income_type="heat", track=[2, 3, 4, 6, 8, 10, 13],
        colony_bonus={"heat": 2}, placement_bonus={"heat_production": 1},
    ),
    "luna": ColonyDef(
        id="luna", income_type="mc", track=[1, 2, 4, 7, 10, 13, 17],
        colony_bonus={"mc": 2}, placement_bonus={"mc_production": 2},
    ),
    # Triton es la unica de estas cinco cuyo placement bonus es STOCK y no
    # produccion: sus 3 colony spots muestran el titanio SIN el marco de
    # produccion. El dict de placement_bonus es generico (se suma clave por
    # clave al jugador), asi que no hizo falta tocar codigo para soportarlo.
    "triton": ColonyDef(
        id="triton", income_type="titanium", track=[0, 1, 1, 2, 3, 4, 5],
        colony_bonus={"titanium": 1}, placement_bonus={"titanium": 3},
    ),
    # Estas tres reparten recursos que NO viven en el stock del jugador sino
    # EN UNA CARTA (microbios, floaters, animales). Se expresan con el prefijo
    # "card_resource:<tipo>", que tools._apply_colony_gain resuelve pidiendo
    # `target_card_id` y validando que esa carta guarde ese tipo de recurso.
    # Miranda ademas da una CARTA como colony bonus ("cards": roba del mazo).
    "enceladus": ColonyDef(
        id="enceladus", income_type="card_resource:microbe", track=[0, 1, 2, 3, 4, 4, 5],
        colony_bonus={"card_resource:microbe": 1}, placement_bonus={"card_resource:microbe": 3},
    ),
    "titan": ColonyDef(
        id="titan", income_type="card_resource:floater", track=[0, 1, 1, 2, 3, 3, 4],
        colony_bonus={"card_resource:floater": 1}, placement_bonus={"card_resource:floater": 3},
    ),
    "miranda": ColonyDef(
        id="miranda", income_type="card_resource:animal", track=[0, 1, 1, 2, 2, 3, 3],
        colony_bonus={"cards": 1}, placement_bonus={"card_resource:animal": 1},
    ),
    # PENDIENTES, las dos que no entran con este modelo (ver CARDS_LOG.md):
    #   * Pluto: su colony bonus es "roba 1 carta y descarta 1", que necesita
    #     que el jugador ELIJA cual descartar -- el income ("cards": robar X)
    #     si entra, pero cargarla a medias seria peor que no cargarla.
    #   * Europa: su trade income no es "X de un recurso" sino "gana la
    #     PRODUCCION indicada", y cada casilla del track indica una produccion
    #     distinta (MC, MC, energia, energia, plantas, plantas, plantas). Eso
    #     rompe el tipo `track: list[int]` + `income_type: str`. Ademas su
    #     placement bonus es COLOCAR UN OCEANO, no un recurso.
}


class ColonyTileState(TypedDict):
    """Estado MUTABLE de una Colony Tile en juego -- se persiste en Supabase."""
    track_position: int
    owners: list[str]  # player_ids, en el orden en que construyeron ahi
    trade_fleet_present: bool


Colonies = dict[str, ColonyTileState]


class UnknownColonyError(Exception):
    """El colony_id no existe en COLONY_DEFS (todavia no cargada/verificada)."""


class ColonyFullError(Exception):
    """La colonia ya tiene el maximo de 3 duenos, o este jugador ya tiene una ahi."""


class ColonyOccupiedError(Exception):
    """La colonia ya tiene una flota de comercio visitandola."""


def new_colonies(colony_ids: list[str]) -> Colonies:
    """
    Arranca las colonias elegidas para esta partida (setup -- ver "Solo with
    Colonies" en el rulebook: en single-player se sortean 4 y se eligen 3).
    El marcador blanco arranca en la 2da casilla del track (index 1): en los
    scans de las 9 colonias cargadas es la casilla resaltada con borde
    blanco, y vale para todas ellas por igual (incluidas Titan, Enceladus y
    Miranda, cuyo scan muestra el mismo resaltado en la segunda casilla).
    """
    for cid in colony_ids:
        if cid not in COLONY_DEFS:
            raise UnknownColonyError(f"Colonia '{cid}' no esta cargada en COLONY_DEFS")
    return {cid: ColonyTileState(track_position=1, owners=[], trade_fleet_present=False) for cid in colony_ids}


def build_colony(
    colonies: Colonies, colony_id: str, player_id: str, allow_duplicate: bool = False
) -> tuple[Colonies, dict]:
    """
    Coloca el marcador del jugador en el slot mas bajo libre de `colony_id`
    (maximo 3 duenos por colonia, 1 por jugador salvo `allow_duplicate`).
    Si el marcador blanco esta en o por debajo de la nueva cantidad de
    duenos, sube 1 paso para dejarle lugar. NO cobra los 17 MC (eso lo hace
    el caller, ver tools.build_colony, junto con calculate_card_payment-style
    stock check).

    allow_duplicate: True para cartas que EXPLICITAMENTE ignoran la regla
    de "1 colonia por jugador por tile" (ej. Research Colony, Space Port
    Colony: "may be placed where you already have a colony") -- el jugador
    puede terminar con 2 de los 3 slots totales de esa colonia. Sigue
    respetando el maximo de 3 duenos en total.

    Devuelve (colonias actualizadas, placement_bonus a aplicar una vez).
    Lanza UnknownColonyError / ColonyFullError.
    """
    if colony_id not in COLONY_DEFS:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta cargada en COLONY_DEFS")
    if colony_id not in colonies:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta en juego esta partida")
    tile = colonies[colony_id]
    if not allow_duplicate and player_id in tile["owners"]:
        raise ColonyFullError(f"El jugador ya tiene una colonia en '{colony_id}'")
    if len(tile["owners"]) >= MAX_COLONISTS_PER_TILE:
        raise ColonyFullError(f"'{colony_id}' ya tiene el maximo de {MAX_COLONISTS_PER_TILE} colonias")
    new_owners = [*tile["owners"], player_id]
    new_track_position = max(tile["track_position"], len(new_owners))
    new_tile = ColonyTileState(
        track_position=new_track_position, owners=new_owners, trade_fleet_present=tile["trade_fleet_present"],
    )
    return {**colonies, colony_id: new_tile}, dict(COLONY_DEFS[colony_id]["placement_bonus"])


def trade_with_colony(colonies: Colonies, colony_id: str) -> tuple[Colonies, str, int, dict]:
    """
    Comercia con `colony_id`: da el trade income segun la posicion actual
    del marcador (antes de moverlo) y el colony_bonus a repartir entre
    TODOS sus duenos. Despues resetea el marcador a la posicion mas baja
    posible (al lado de las colonias construidas, o al fondo si no hay
    ninguna). El caller es responsable de cobrar el costo de comerciar
    (9 MC / 3 energia / 3 titanio, ver TRADE_COST_*) y de gastar/verificar
    la flota de comercio del jugador ANTES de llamar aca.

    Devuelve (colonias actualizadas, income_type, income_amount, colony_bonus).
    Lanza UnknownColonyError, ColonyOccupiedError.
    """
    if colony_id not in COLONY_DEFS:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta cargada en COLONY_DEFS")
    if colony_id not in colonies:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta en juego esta partida")
    tile = colonies[colony_id]
    if tile["trade_fleet_present"]:
        raise ColonyOccupiedError(f"'{colony_id}' ya tiene una flota de comercio visitandola")
    cdef = COLONY_DEFS[colony_id]
    income_amount = cdef["track"][tile["track_position"]]
    new_track_position = len(tile["owners"])
    new_tile = ColonyTileState(
        track_position=new_track_position, owners=tile["owners"], trade_fleet_present=True,
    )
    return {**colonies, colony_id: new_tile}, cdef["income_type"], income_amount, dict(cdef["colony_bonus"])


def adjust_colony_track(colonies: Colonies, colony_id: str, delta: int) -> Colonies:
    """
    Sube o baja el marcador blanco de `colony_id` `delta` pasos directo
    (positivo o negativo), sin pasar por build_colony/trade_with_colony
    (ej. Market Manipulation: +1 a una colonia, -1 a otra). Clampeado entre
    0 y el tope del track -- no lanza error si el delta se pasa de rango,
    simplemente lo clampea (igual que run_colony_production con el tope).
    """
    if colony_id not in COLONY_DEFS:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta cargada en COLONY_DEFS")
    if colony_id not in colonies:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta en juego esta partida")
    tile = colonies[colony_id]
    max_pos = len(COLONY_DEFS[colony_id]["track"]) - 1
    new_position = max(0, min(max_pos, tile["track_position"] + delta))
    return {**colonies, colony_id: ColonyTileState(
        track_position=new_position, owners=tile["owners"], trade_fleet_present=tile["trade_fleet_present"],
    )}


def run_colony_production(colonies: Colonies) -> Colonies:
    """
    Fase solar, paso 3 (ver rulebook): sube el marcador blanco 1 paso en
    CADA Colony Tile en juego (clampeado al tope de su track), y libera
    todas las flotas de comercio (vuelven a estar disponibles). Llamar una
    vez por generacion, junto con run_production_phase de cada jugador.
    """
    new_colonies_: Colonies = {}
    for cid, tile in colonies.items():
        max_pos = len(COLONY_DEFS[cid]["track"]) - 1
        new_colonies_[cid] = ColonyTileState(
            track_position=min(tile["track_position"] + 1, max_pos),
            owners=tile["owners"],
            trade_fleet_present=False,
        )
    return new_colonies_
