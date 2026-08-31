"""
Tablero hexagonal de Marte (mapa "Tharsis", el unico soportado por ahora --
ver CLAUDE.md seccion 6 y HEX_MAP_RESEARCH.md). Funciones puras, sin
dependencias de FastAPI/Supabase, en el mismo estilo que rules_engine.py.

Fuente de los 61 hexagonos y su geometria: transcrito directo de
`TharsisBoard.ts` y `BoardBuilder.ts` del proyecto open-source
terraforming-mars/terraforming-mars (motor ampliamente jugado y testeado).
El conteo de 12 hexagonos reservados para oceano fue verificado ademas
contra el texto del reglamento oficial (transcripcion en rulespal.com) --
ver HEX_MAP_RESEARCH.md para el detalle de ambas fuentes. Los BONUS
especificos de cada hexagono individual salen unicamente del codigo fuente
(no se re-verifico cada uno contra una segunda fuente independiente).

Alcance de esta primera pasada (decision explicita, ver CLAUDE.md seccion 6):
- Solo el mapa Tharsis (no Hellas/Elysium).
- Sin la mecanica de pago cruzado entre jugadores de la expansion Ares.
- Sin las ~20 special tiles especificas de cartas todavia (Mining Area,
  Mining Rights, Land Claim siguen en "Pendientes" en CARDS_LOG.md) --
  este modulo da los primitivos (adyacencia, bonus de hex, colocacion) pero
  todavia no esta conectado a tools.py/cards. Cablearlo es un paso aparte.
"""
from typing import Literal, TypedDict

TileType = Literal["city", "greenery", "ocean"]
HexType = Literal["land", "ocean"]


class HexDef(TypedDict):
    """Definicion ESTATICA de un hexagono -- nunca cambia durante la partida."""
    id: str
    row: int
    x: int
    hex_type: HexType
    volcanic: bool
    bonus: list[tuple[str, int]]
    reserved_city: str | None


class HexState(TypedDict):
    """Estado MUTABLE de un hexagono -- lo que se persiste en Supabase."""
    tile_type: TileType
    owner: str | None       # None = neutral (oceano)
    bonus_consumed: bool


Board = dict[str, HexState]


class HexOccupiedError(Exception):
    """El hexagono ya tiene un tile -- no se puede colocar otro encima."""


class InvalidPlacementError(Exception):
    """La colocacion viola una regla de legalidad (tipo de hexagono, adyacencia)."""


class UnknownHexError(Exception):
    """El hex_id no existe en el mapa Tharsis."""


# ---------------------------------------------------------------------------
# Definicion estatica del mapa Tharsis (61 hexagonos, 9 filas: 5,6,7,8,9,8,7,6,5)
# ---------------------------------------------------------------------------

def _row(row: int, x_offset: int, defs: list[tuple[HexType, bool, list[tuple[str, int]], str | None]]) -> list[HexDef]:
    out: list[HexDef] = []
    for i, (hex_type, volcanic, bonus, reserved_city) in enumerate(defs):
        out.append(HexDef(
            id="", row=row, x=x_offset + i, hex_type=hex_type,
            volcanic=volcanic, bonus=bonus, reserved_city=reserved_city,
        ))
    return out


_S = "steel"
_T = "titanium"
_P = "plant"
_C = "card"

# Cada fila, en orden izquierda a derecha, tal como en TharsisBoard.ts.
# Tupla: (hex_type, volcanic, bonus, reserved_city)
_ROWS_RAW: list[list[tuple[HexType, bool, list[tuple[str, int]], str | None]]] = [
    # y=0 (5 hex, xOffset=4)
    [("land", False, [(_S, 2)], None), ("ocean", False, [(_S, 2)], None), ("land", False, [], None),
     ("ocean", False, [(_C, 1)], None), ("ocean", False, [], None)],
    # y=1 (6 hex, xOffset=3)
    [("land", False, [], None), ("land", True, [(_S, 1)], None), ("land", False, [], None),
     ("land", False, [], None), ("land", False, [], None), ("ocean", False, [(_C, 2)], None)],
    # y=2 (7 hex, xOffset=2)
    [("land", True, [(_C, 1)], None), ("land", False, [], None), ("land", False, [], None),
     ("land", False, [], None), ("land", False, [], None), ("land", False, [], None),
     ("land", False, [(_S, 1)], None)],
    # y=3 (8 hex, xOffset=1)
    [("land", True, [(_P, 1), (_T, 1)], None), ("land", False, [(_P, 1)], None),
     ("land", False, [(_P, 1)], None), ("land", False, [(_P, 1)], None),
     ("land", False, [(_P, 2)], None), ("land", False, [(_P, 1)], None),
     ("land", False, [(_P, 1)], None), ("ocean", False, [(_P, 2)], None)],
    # y=4 (9 hex, xOffset=0) -- fila mas ancha, incluye Noctis City (pos 2)
    [("land", True, [(_P, 2)], None), ("land", False, [(_P, 2)], None),
     ("land", False, [(_P, 2)], "noctis_city"), ("ocean", False, [(_P, 2)], None),
     ("ocean", False, [(_P, 2)], None), ("ocean", False, [(_P, 2)], None),
     ("land", False, [(_P, 2)], None), ("land", False, [(_P, 2)], None),
     ("land", False, [(_P, 2)], None)],
    # y=5 (8 hex, xOffset=1)
    [("land", False, [(_P, 1)], None), ("land", False, [(_P, 2)], None),
     ("land", False, [(_P, 1)], None), ("land", False, [(_P, 1)], None),
     ("land", False, [(_P, 1)], None), ("ocean", False, [(_P, 1)], None),
     ("ocean", False, [(_P, 1)], None), ("ocean", False, [(_P, 1)], None)],
    # y=6 (7 hex, xOffset=2)
    [("land", False, [], None), ("land", False, [], None), ("land", False, [], None),
     ("land", False, [], None), ("land", False, [], None), ("land", False, [(_P, 1)], None),
     ("land", False, [], None)],
    # y=7 (6 hex, xOffset=3)
    [("land", False, [(_S, 2)], None), ("land", False, [], None), ("land", False, [(_C, 1)], None),
     ("land", False, [(_C, 1)], None), ("land", False, [], None), ("land", False, [(_T, 1)], None)],
    # y=8 (5 hex, xOffset=4)
    [("land", False, [(_S, 1)], None), ("land", False, [(_S, 2)], None), ("land", False, [], None),
     ("land", False, [], None), ("ocean", False, [(_T, 2)], None)],
]

_TILES_PER_ROW = [5, 6, 7, 8, 9, 8, 7, 6, 5]


def _build_hex_defs() -> dict[str, HexDef]:
    defs: dict[str, HexDef] = {}
    next_id = 3  # ids 01/02 estan reservados a Ganymede Colony/Phobos Space Haven (fuera del mapa)
    for row, tiles_in_row in enumerate(_TILES_PER_ROW):
        x_offset = 9 - tiles_in_row
        row_defs = _row(row, x_offset, _ROWS_RAW[row])
        for hex_def in row_defs:
            hex_id = f"{next_id:02d}"
            defs[hex_id] = HexDef(
                id=hex_id, row=hex_def["row"], x=hex_def["x"], hex_type=hex_def["hex_type"],
                volcanic=hex_def["volcanic"], bonus=hex_def["bonus"], reserved_city=hex_def["reserved_city"],
            )
            next_id += 1
    return defs


HEX_DEFS: dict[str, HexDef] = _build_hex_defs()

MAX_X = 8
MAX_Y = 8
_MIDDLE_ROW = MAX_Y // 2


def _neighbor_coords(x: int, y: int) -> list[tuple[int, int]]:
    """Orden horario empezando en top-left, igual que Board.ts::computeAdjacentSpaces."""
    left = (x - 1, y)
    right = (x + 1, y)
    top_left = [x, y - 1]
    top_right = [x, y - 1]
    bottom_left = [x, y + 1]
    bottom_right = [x, y + 1]
    if y < _MIDDLE_ROW:
        bottom_left[0] -= 1
        top_right[0] += 1
    elif y == _MIDDLE_ROW:
        bottom_right[0] += 1
        top_right[0] += 1
    else:
        bottom_right[0] += 1
        top_left[0] -= 1
    return [tuple(top_left), tuple(top_right), right, tuple(bottom_right), tuple(bottom_left), left]


def _build_adjacency() -> dict[str, list[str]]:
    coord_to_id = {(hex_def["x"], hex_def["row"]): hex_id for hex_id, hex_def in HEX_DEFS.items()}
    adjacency: dict[str, list[str]] = {}
    for hex_id, hex_def in HEX_DEFS.items():
        candidates = _neighbor_coords(hex_def["x"], hex_def["row"])
        adjacency[hex_id] = [coord_to_id[c] for c in candidates if c in coord_to_id]
    return adjacency


ADJACENCY: dict[str, list[str]] = _build_adjacency()

NOCTIS_CITY_HEX_ID = next(hex_id for hex_id, d in HEX_DEFS.items() if d["reserved_city"] == "noctis_city")


# ---------------------------------------------------------------------------
# Estado inicial del tablero (para persistir en Supabase)
# ---------------------------------------------------------------------------

def new_board() -> Board:
    """Tablero vacio: ningun hexagono tiene tile, ningun bonus fue consumido."""
    return {}


# ---------------------------------------------------------------------------
# Consultas de solo lectura
# ---------------------------------------------------------------------------

def get_neighbors(hex_id: str) -> list[str]:
    if hex_id not in HEX_DEFS:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    return ADJACENCY[hex_id]


def is_hex_empty(board: Board, hex_id: str) -> bool:
    if hex_id not in HEX_DEFS:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    return hex_id not in board


def get_adjacent_tiles(board: Board, hex_id: str) -> list[HexState]:
    return [board[n] for n in get_neighbors(hex_id) if n in board]


def count_adjacent_oceans(board: Board, hex_id: str) -> int:
    return sum(1 for tile in get_adjacent_tiles(board, hex_id) if tile["tile_type"] == "ocean")


def count_adjacent_owned_by(board: Board, hex_id: str, player_id: str) -> int:
    return sum(1 for tile in get_adjacent_tiles(board, hex_id) if tile["owner"] == player_id)


def count_tiles_of_type(board: Board, tile_type: TileType, owner: str | None = None) -> int:
    matches = (tile for tile in board.values() if tile["tile_type"] == tile_type)
    if owner is not None:
        matches = (tile for tile in matches if tile["owner"] == owner)
    return sum(1 for _ in matches)


# ---------------------------------------------------------------------------
# Validacion de legalidad (puras, lanzan InvalidPlacementError si no aplica)
# ---------------------------------------------------------------------------

def can_place_ocean(board: Board, hex_id: str) -> bool:
    hex_def = HEX_DEFS.get(hex_id)
    if hex_def is None:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    return hex_def["hex_type"] == "ocean" and is_hex_empty(board, hex_id)


def can_place_city(board: Board, hex_id: str) -> bool:
    hex_def = HEX_DEFS.get(hex_id)
    if hex_def is None:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    if hex_def["hex_type"] != "land" or not is_hex_empty(board, hex_id):
        return False
    if hex_def["reserved_city"] is not None:
        return False
    return not any(tile["tile_type"] == "city" for tile in get_adjacent_tiles(board, hex_id))


def can_place_greenery(board: Board, hex_id: str, player_id: str) -> bool:
    """
    Regla oficial: debe ser adyacente a un tile propio SI existe alguna opcion
    legal asi disponible en el mapa; si el jugador todavia no tiene ningun
    tile en el mapa, puede colocarse libremente en cualquier terreno vacio.
    Esta funcion valida un hex_id puntual -- quien la llama es responsable de
    ofrecer solo opciones adyacentes cuando el jugador ya tiene tiles propios.
    """
    hex_def = HEX_DEFS.get(hex_id)
    if hex_def is None:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    if hex_def["hex_type"] != "land" or not is_hex_empty(board, hex_id):
        return False
    if hex_def["reserved_city"] is not None:
        return False
    has_own_tile_anywhere = any(tile["owner"] == player_id for tile in board.values())
    if not has_own_tile_anywhere:
        return True
    return count_adjacent_owned_by(board, hex_id, player_id) > 0


# ---------------------------------------------------------------------------
# Mutacion (reciben Board, devuelven Board nuevo + bonus otorgado)
# ---------------------------------------------------------------------------

def resolve_hex_bonus(board: Board, hex_id: str) -> list[tuple[str, int]]:
    """Bonus impreso en el hex, solo si todavia no se consumio."""
    hex_def = HEX_DEFS[hex_id]
    if hex_id in board and board[hex_id]["bonus_consumed"]:
        return []
    return list(hex_def["bonus"])


def resolve_ocean_adjacency_bonus(board: Board, hex_id: str) -> int:
    """MC a otorgar por colocar un tile adyacente a oceanos ya existentes."""
    return 2 * count_adjacent_oceans(board, hex_id)


def _place(board: Board, hex_id: str, tile_type: TileType, owner: str | None) -> tuple[Board, list[tuple[str, int]], int]:
    if hex_id not in HEX_DEFS:
        raise UnknownHexError(f"Hexagono '{hex_id}' no existe en el mapa Tharsis")
    if not is_hex_empty(board, hex_id):
        raise HexOccupiedError(f"El hexagono '{hex_id}' ya tiene un tile")
    hex_bonus = resolve_hex_bonus(board, hex_id)
    ocean_bonus_mc = resolve_ocean_adjacency_bonus(board, hex_id)
    new_board = dict(board)
    new_board[hex_id] = HexState(tile_type=tile_type, owner=owner, bonus_consumed=True)
    return new_board, hex_bonus, ocean_bonus_mc


def place_ocean_tile(board: Board, hex_id: str) -> tuple[Board, list[tuple[str, int]], int]:
    """Coloca un tile de oceano (neutral, sin dueno). Lanza si el hex no es valido."""
    if not can_place_ocean(board, hex_id):
        raise InvalidPlacementError(f"No se puede colocar oceano en '{hex_id}'")
    return _place(board, hex_id, "ocean", owner=None)


def place_city_tile(board: Board, hex_id: str, player_id: str) -> tuple[Board, list[tuple[str, int]], int]:
    if not can_place_city(board, hex_id):
        raise InvalidPlacementError(f"No se puede colocar ciudad en '{hex_id}'")
    return _place(board, hex_id, "city", owner=player_id)


def place_greenery_tile(board: Board, hex_id: str, player_id: str) -> tuple[Board, list[tuple[str, int]], int]:
    if not can_place_greenery(board, hex_id, player_id):
        raise InvalidPlacementError(f"No se puede colocar greenery en '{hex_id}' para este jugador")
    return _place(board, hex_id, "greenery", owner=player_id)
