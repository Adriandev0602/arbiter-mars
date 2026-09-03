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
Ceres, Io), cada una con su propio track de valores de "trade income" y su
"colony bonus"/"placement bonus" especificos. Mismo criterio que el catalogo
de cartas (CLAUDE.md seccion 4): NO se generan datos al voleo. Por ahora
solo esta cargada **Callisto**, verificada con DOS fuentes independientes:
  1. El ejemplo trabajado del rulebook oficial (pagina 2): "the trade income
     is 10 energy resources, as indicated by the white marker... green
     player gets 3 energy" con el marcador en la 6ta casilla visible del
     track impreso en la imagen (0/2/3/5/7/10/13), y el placement bonus
     "+1 energia produccion" citado explicitamente en el texto.
  2. Busqueda independiente (resumen de terceros) que reporta el mismo
     track para Callisto: "Colony Bonus: 0 [MC], Trade Income track: 2, 3,
     5, 7, 10, 13" -- coincide exactamente con el track leido del rulebook
     (agregando el 0 inicial de la primera casilla, no citado en el resumen
     de terceros pero visible en la imagen del rulebook).
El resto de las 10 colonias reales quedan sin cargar hasta verificarlas de
la misma forma -- el MECANISMO ya es generico y funciona con cualquier
colonia que se agregue a COLONY_DEFS despues. Ver CARDS_LOG.md, seccion
"Colonies: mecanica de colonias/comercio".

Alcance de esta primera pasada: solo lo que hace falta para las cartas que
NO dependen de una colonia especifica por nombre (ej. Ecology Research:
"por cada colonia que tengas", sin importar cual; Cryo-Sleep: descuento
generico al comerciar). Cartas que targeteen una colonia puntual por nombre
distinta de Callisto quedan pendientes hasta cargar esa colonia.
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
    El marcador blanco arranca en la 2da casilla resaltada del track (index
    1) para las colonias "normales" -- Titan/Enceladus/Miranda arrancan
    distinto (marcador sobre la imagen de la luna, fuera del track) pero
    esas 3 todavia no estan cargadas en COLONY_DEFS, asi que no aplica hoy.
    """
    for cid in colony_ids:
        if cid not in COLONY_DEFS:
            raise UnknownColonyError(f"Colonia '{cid}' no esta cargada en COLONY_DEFS")
    return {cid: ColonyTileState(track_position=1, owners=[], trade_fleet_present=False) for cid in colony_ids}


def build_colony(colonies: Colonies, colony_id: str, player_id: str) -> tuple[Colonies, dict]:
    """
    Coloca el marcador del jugador en el slot mas bajo libre de `colony_id`
    (maximo 3 duenos por colonia, 1 por jugador). Si el marcador blanco
    esta en o por debajo de la nueva cantidad de duenos, sube 1 paso para
    dejarle lugar. NO cobra los 17 MC (eso lo hace el caller, ver
    tools.build_colony, junto con calculate_card_payment-style stock check).

    Devuelve (colonias actualizadas, placement_bonus a aplicar una vez).
    Lanza UnknownColonyError / ColonyFullError.
    """
    if colony_id not in COLONY_DEFS:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta cargada en COLONY_DEFS")
    if colony_id not in colonies:
        raise UnknownColonyError(f"Colonia '{colony_id}' no esta en juego esta partida")
    tile = colonies[colony_id]
    if player_id in tile["owners"]:
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
