"""
Tests del modulo de tablero hexagonal (mapa Tharsis). Los datos de geometria
y bonus estan transcritos de TharsisBoard.ts (terraforming-mars/terraforming-mars);
el conteo de 12 hexagonos de oceano fue verificado ademas contra el reglamento
oficial -- ver HEX_MAP_RESEARCH.md.
"""
import pytest

from app.agent.board import (
    HEX_DEFS,
    ADJACENCY,
    NOCTIS_CITY_HEX_ID,
    new_board,
    get_neighbors,
    is_hex_empty,
    count_adjacent_oceans,
    count_adjacent_owned_by,
    count_tiles_of_type,
    can_place_ocean,
    can_place_city,
    can_place_greenery,
    can_place_special_tile,
    resolve_hex_bonus,
    resolve_ocean_adjacency_bonus,
    place_ocean_tile,
    place_city_tile,
    place_greenery_tile,
    place_special_tile,
    can_place_ocean_on_land,
    place_ocean_tile_on_land,
    can_place_city_adjacent_to_cities,
    place_city_tile_adjacent_to_cities,
    HexOccupiedError,
    InvalidPlacementError,
    UnknownHexError,
)


def test_map_has_61_hexes():
    assert len(HEX_DEFS) == 61


def test_map_has_12_ocean_reserved_hexes():
    oceans = [h for h in HEX_DEFS.values() if h["hex_type"] == "ocean"]
    assert len(oceans) == 12


def test_map_has_4_volcanic_hexes():
    volcanic = [h for h in HEX_DEFS.values() if h["volcanic"]]
    assert len(volcanic) == 4


def test_noctis_city_hex_is_reserved():
    assert HEX_DEFS[NOCTIS_CITY_HEX_ID]["reserved_city"] == "noctis_city"
    assert HEX_DEFS[NOCTIS_CITY_HEX_ID]["row"] == 4


def test_row_widths_match_tharsis_layout():
    counts = {}
    for hex_def in HEX_DEFS.values():
        counts[hex_def["row"]] = counts.get(hex_def["row"], 0) + 1
    assert [counts[r] for r in range(9)] == [5, 6, 7, 8, 9, 8, 7, 6, 5]


def test_middle_row_hex_has_6_neighbors():
    # cualquier hex interior de la fila mas ancha (no en el borde del rombo)
    middle_row_ids = [h["id"] for h in HEX_DEFS.values() if h["row"] == 4]
    interior_id = middle_row_ids[4]  # posicion central, x=4
    assert len(get_neighbors(interior_id)) == 6


def test_corner_hex_has_3_neighbors():
    # primer hex del mapa (fila 0, primera posicion) es una esquina del rombo
    corner_id = min(h["id"] for h in HEX_DEFS.values() if h["row"] == 0)
    assert len(get_neighbors(corner_id)) == 3


def test_adjacency_is_symmetric():
    for hex_id, neighbors in ADJACENCY.items():
        for n in neighbors:
            assert hex_id in ADJACENCY[n], f"{hex_id} -> {n} no es simetrico"


def test_get_neighbors_unknown_hex_raises():
    with pytest.raises(UnknownHexError):
        get_neighbors("99")


def test_new_board_is_empty():
    board = new_board()
    assert is_hex_empty(board, "03")


def test_can_place_ocean_only_on_ocean_hex():
    board = new_board()
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    land_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)
    assert can_place_ocean(board, ocean_hex) is True
    assert can_place_ocean(board, land_hex) is False


def test_place_ocean_tile_occupies_hex():
    board = new_board()
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    new_board_state, bonus, ocean_bonus_mc = place_ocean_tile(board, ocean_hex)
    assert is_hex_empty(new_board_state, ocean_hex) is False
    assert new_board_state[ocean_hex]["owner"] is None
    assert ocean_bonus_mc == 0  # sin oceanos vecinos todavia


def test_place_ocean_tile_on_occupied_hex_raises():
    board = new_board()
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    board, _, _ = place_ocean_tile(board, ocean_hex)
    with pytest.raises(InvalidPlacementError):
        place_ocean_tile(board, ocean_hex)


def test_place_ocean_tile_on_land_hex_raises():
    board = new_board()
    land_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)
    with pytest.raises(InvalidPlacementError):
        place_ocean_tile(board, land_hex)


def test_hex_bonus_is_consumed_only_once():
    board = new_board()
    bonus_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["bonus"] and h["reserved_city"] is None)
    assert resolve_hex_bonus(board, bonus_hex) == HEX_DEFS[bonus_hex]["bonus"]
    board, granted_bonus, _ = place_city_tile(board, bonus_hex, "player-1")
    assert granted_bonus == HEX_DEFS[bonus_hex]["bonus"]
    assert resolve_hex_bonus(board, bonus_hex) == []


def test_cannot_place_city_adjacent_to_another_city():
    board = new_board()
    land_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None and len(get_neighbors(h["id"])) > 0
    )
    neighbor = next(
        n for n in get_neighbors(land_hex)
        if HEX_DEFS[n]["hex_type"] == "land" and HEX_DEFS[n]["reserved_city"] is None
    )
    board, _, _ = place_city_tile(board, land_hex, "player-1")
    assert can_place_city(board, neighbor) is False


def test_cannot_place_city_on_noctis_city_reserved_hex():
    board = new_board()
    assert can_place_city(board, NOCTIS_CITY_HEX_ID) is False
    with pytest.raises(InvalidPlacementError):
        place_city_tile(board, NOCTIS_CITY_HEX_ID, "player-1")


def test_greenery_free_placement_when_player_has_no_tiles_yet():
    board = new_board()
    any_land = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)
    assert can_place_greenery(board, any_land, "player-1") is True


def test_greenery_requires_adjacency_once_player_has_a_tile():
    board = new_board()
    land_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None and len(get_neighbors(h["id"])) > 0
    )
    board, _, _ = place_city_tile(board, land_hex, "player-1")
    far_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None
        and h["id"] != land_hex and h["id"] not in get_neighbors(land_hex)
    )
    assert can_place_greenery(board, far_hex, "player-1") is False
    neighbor = next(
        n for n in get_neighbors(land_hex)
        if HEX_DEFS[n]["hex_type"] == "land" and HEX_DEFS[n]["reserved_city"] is None
    )
    assert can_place_greenery(board, neighbor, "player-1") is True


def test_place_greenery_tile_illegal_raises():
    board = new_board()
    land_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None and len(get_neighbors(h["id"])) > 0
    )
    board, _, _ = place_city_tile(board, land_hex, "player-1")
    far_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None
        and h["id"] != land_hex and h["id"] not in get_neighbors(land_hex)
    )
    with pytest.raises(InvalidPlacementError):
        place_greenery_tile(board, far_hex, "player-1")


def test_ocean_adjacency_bonus_is_2_mc_per_adjacent_ocean():
    board = new_board()
    # buscar un hex de tierra con al menos 2 vecinos de oceano
    land_hex = None
    for h in HEX_DEFS.values():
        if h["hex_type"] != "land" or h["reserved_city"] is not None:
            continue
        ocean_neighbors = [n for n in get_neighbors(h["id"]) if HEX_DEFS[n]["hex_type"] == "ocean"]
        if len(ocean_neighbors) >= 2:
            land_hex = h["id"]
            oceans_to_place = ocean_neighbors
            break
    assert land_hex is not None, "el mapa deberia tener al menos un hex de tierra con 2+ vecinos de oceano"
    for ocean_hex in oceans_to_place:
        board, _, _ = place_ocean_tile(board, ocean_hex)
    assert count_adjacent_oceans(board, land_hex) == len(oceans_to_place)
    assert resolve_ocean_adjacency_bonus(board, land_hex) == 2 * len(oceans_to_place)


def test_count_tiles_of_type_and_owner():
    board = new_board()
    city_hex = next(
        h["id"] for h in HEX_DEFS.values()
        if h["hex_type"] == "land" and h["reserved_city"] is None and len(get_neighbors(h["id"])) > 0
    )
    board, _, _ = place_city_tile(board, city_hex, "player-1")
    greenery_hex = next(
        n for n in get_neighbors(city_hex)
        if HEX_DEFS[n]["hex_type"] == "land" and HEX_DEFS[n]["reserved_city"] is None
    )
    board, _, _ = place_greenery_tile(board, greenery_hex, "player-1")
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    board, _, _ = place_ocean_tile(board, ocean_hex)
    assert count_tiles_of_type(board, "city") == 1
    assert count_tiles_of_type(board, "city", owner="player-1") == 1
    assert count_tiles_of_type(board, "ocean") == 1
    assert count_tiles_of_type(board, "ocean", owner="player-1") == 0  # oceano es neutral
    assert count_adjacent_owned_by(board, ocean_hex, "player-1") >= 0  # no lanza


# ---------------------------------------------------------------------------
# Special tiles de cartas (Mining Rights / Mining Area)
# ---------------------------------------------------------------------------

def test_can_place_special_tile_requires_matching_hex_bonus():
    board = new_board()
    requirement = {"hex_bonus_resource": ["steel", "titanium"]}
    steel_hex = "03"  # bonus [steel,2]
    plain_hex = "05"  # sin bonus
    assert can_place_special_tile(board, steel_hex, requirement, "player-1") is True
    assert can_place_special_tile(board, plain_hex, requirement, "player-1") is False


def test_mining_rights_no_adjacency_required():
    board = new_board()
    requirement = {"hex_bonus_resource": ["steel", "titanium"]}
    steel_hex = "03"
    assert can_place_special_tile(board, steel_hex, requirement, "player-1") is True
    new_board_state, hex_bonus, _ = place_special_tile(board, steel_hex, requirement, "player-1", "mining_rights")
    assert new_board_state[steel_hex]["tile_type"] == "special"
    assert new_board_state[steel_hex]["card"] == "mining_rights"
    assert hex_bonus == [("steel", 2)]  # quien llama decide que hacer con esto (produccion, no stock)


def test_mining_area_requires_adjacency_to_own_tile():
    board = new_board()
    requirement = {"hex_bonus_resource": ["steel", "titanium"], "require_adjacency_to_own_tile": True}
    steel_hex = "03"
    assert can_place_special_tile(board, steel_hex, requirement, "player-1") is False
    # el jugador coloca una ciudad en un hex vecino de 03 (04 es oceano, no sirve para ciudad;
    # el vecino "08" si es land)
    assert "08" in get_neighbors(steel_hex)
    board, _, _ = place_city_tile(board, "08", "player-1")
    assert can_place_special_tile(board, steel_hex, requirement, "player-1") is True
    board, hex_bonus, _ = place_special_tile(board, steel_hex, requirement, "player-1", "mining_area")
    assert board[steel_hex]["owner"] == "player-1"
    assert hex_bonus == [("steel", 2)]


def test_place_special_tile_on_occupied_hex_raises():
    board = new_board()
    requirement = {"hex_bonus_resource": ["steel", "titanium"]}
    steel_hex = "03"
    board, _, _ = place_special_tile(board, steel_hex, requirement, "player-1", "mining_rights")
    with pytest.raises(InvalidPlacementError):
        place_special_tile(board, steel_hex, requirement, "player-1", "mining_rights")


def test_place_special_tile_without_matching_bonus_raises():
    board = new_board()
    requirement = {"hex_bonus_resource": ["steel", "titanium"]}
    plain_hex = "05"
    with pytest.raises(InvalidPlacementError):
        place_special_tile(board, plain_hex, requirement, "player-1", "mining_rights")


# ---------------------------------------------------------------------------
# Oceano sobre tierra (Artificial Lake: "place on an area NOT reserved for ocean")
# ---------------------------------------------------------------------------

def test_can_place_ocean_on_land_only_on_land_hex():
    board = new_board()
    land_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    assert can_place_ocean_on_land(board, land_hex) is True
    assert can_place_ocean_on_land(board, ocean_hex) is False


def test_place_ocean_tile_on_land_occupies_hex_as_ocean():
    board = new_board()
    land_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)
    new_board_state, _, _ = place_ocean_tile_on_land(board, land_hex)
    assert new_board_state[land_hex]["tile_type"] == "ocean"
    assert new_board_state[land_hex]["owner"] is None


def test_place_ocean_tile_on_land_rejects_ocean_reserved_hex():
    board = new_board()
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    with pytest.raises(InvalidPlacementError):
        place_ocean_tile_on_land(board, ocean_hex)


def test_place_ocean_tile_on_land_rejects_noctis_city_hex():
    board = new_board()
    with pytest.raises(InvalidPlacementError):
        place_ocean_tile_on_land(board, NOCTIS_CITY_HEX_ID)


# ---------------------------------------------------------------------------
# Ciudad que EXIGE adyacencia a otras ciudades (Urbanized Area)
# ---------------------------------------------------------------------------

def test_can_place_city_adjacent_to_cities_requires_min_count():
    # hex 08 tiene dos vecinos de tierra (03 y 15) que NO son adyacentes
    # entre si, asi que se puede colocar ciudad en ambos sin violar la regla
    # normal de "no ciudad adyacente a ciudad".
    board = new_board()
    center_hex, neighbor_a, neighbor_b = "08", "03", "15"
    assert neighbor_a in get_neighbors(center_hex) and neighbor_b in get_neighbors(center_hex)

    assert can_place_city_adjacent_to_cities(board, center_hex, 2) is False  # sin ciudades vecinas todavia

    board, _, _ = place_city_tile(board, neighbor_a, "player-1")
    assert can_place_city_adjacent_to_cities(board, center_hex, 2) is False  # solo 1 ciudad vecina

    board, _, _ = place_city_tile(board, neighbor_b, "player-1")
    assert can_place_city_adjacent_to_cities(board, center_hex, 2) is True  # ya hay 2


def test_place_city_tile_adjacent_to_cities_illegal_raises():
    board = new_board()
    with pytest.raises(InvalidPlacementError):
        place_city_tile_adjacent_to_cities(board, "08", "player-1", 2)


def test_place_city_tile_adjacent_to_cities_succeeds_when_legal():
    board = new_board()
    center_hex, neighbor_a, neighbor_b = "08", "03", "15"
    board, _, _ = place_city_tile(board, neighbor_a, "player-1")
    board, _, _ = place_city_tile(board, neighbor_b, "player-1")
    new_board_state, _, _ = place_city_tile_adjacent_to_cities(board, center_hex, "player-2", 2)
    assert new_board_state[center_hex]["tile_type"] == "city"
    assert new_board_state[center_hex]["owner"] == "player-2"


# ---------------------------------------------------------------------------
# Special tile adyacente a Greenery (Ecological Zone)
# ---------------------------------------------------------------------------

def test_place_special_tile_ecological_zone_requires_player_has_greenery():
    board = new_board()
    spec = {"require_adjacency_to_greenery": True, "require_player_has_greenery": True}
    # Sin greenerys en el mapa
    assert can_place_special_tile(board, "08", spec, "player-1") is False

    # Con greenery de otro jugador en hex 03
    board, _, _ = place_greenery_tile(board, "03", "player-2")
    # player-1 todavía no tiene greenery propia
    assert can_place_special_tile(board, "08", spec, "player-1") is False

    # player-1 coloca greenery en hex 20 (lejos)
    board, _, _ = place_greenery_tile(board, "20", "player-1")
    # Ahora player-1 sí tiene greenery propia, y 08 es adyacente a una greenery (la de 03)
    assert can_place_special_tile(board, "08", spec, "player-1") is True
    # Hex no adyacente a ninguna greenery (ej. 50) sigue siendo inválido
    assert can_place_special_tile(board, "50", spec, "player-1") is False

    new_board_state, _, _ = place_special_tile(board, "08", spec, "player-1", "ecological_zone")
    assert new_board_state["08"]["tile_type"] == "special"
    assert new_board_state["08"]["card"] == "ecological_zone"
    assert new_board_state["08"]["owner"] == "player-1"



def test_mohole_area_special_tile_requires_ocean_hex():
    board = new_board()
    spec = {"hex_type": "ocean"}
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")
    land_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "land" and h["reserved_city"] is None)

    assert can_place_special_tile(board, ocean_hex, spec, "player-1") is True
    assert can_place_special_tile(board, land_hex, spec, "player-1") is False

    new_board_state, _, _ = place_special_tile(board, ocean_hex, spec, "player-1", "mohole_area")
    assert new_board_state[ocean_hex]["tile_type"] == "special"
    assert new_board_state[ocean_hex]["card"] == "mohole_area"
    # No cuenta como uno de los 9 oceanos del parametro global -- eso lo
    # decide tools.play_card (solo detecta oceans_placed via place_oceans,
    # que Mohole Area no usa).


def test_protected_valley_places_greenery_on_ocean_hex_ignoring_restrictions():
    board = new_board()
    ocean_hex = next(h["id"] for h in HEX_DEFS.values() if h["hex_type"] == "ocean")

    # Sin ignore_restrictions, un hex de oceano nunca es valido para greenery
    assert can_place_greenery(board, ocean_hex, "player-1") is False
    with pytest.raises(InvalidPlacementError):
        place_greenery_tile(board, ocean_hex, "player-1")

    assert can_place_greenery(board, ocean_hex, "player-1", ignore_restrictions=True) is True
    new_board_state, _, _ = place_greenery_tile(board, ocean_hex, "player-1", ignore_restrictions=True)
    assert new_board_state[ocean_hex]["tile_type"] == "greenery"
    assert new_board_state[ocean_hex]["owner"] == "player-1"
