"""
Tests del modulo de tablero hexagonal (mapa Tharsis). Los datos de geometria
y bonus estan transcritos de TharsisBoard.ts (terraforming-mars/terraforming-mars);
el conteo de 12 hexagonos de oceano fue verificado ademas contra el reglamento
oficial -- ver HEX_MAP_RESEARCH.md.
"""
import pytest

from app.agent.board import (
    HEX_DEFS,
    VOLCANO_NAMES,
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
    count_tiles_adjacent_to_ocean,
    count_empty_hexes_adjacent_to_owner,
    has_city_adjacent_to_ocean,
    count_cities_and_special_tiles_adjacent_to_ocean,
    remove_greenery_tile,
    place_nomads,
    place_community,
    community_owner,
    move_nomads,
    find_nomads,
    place_cathedral,
    count_cathedrals,
    remove_ocean_tile,
    can_place_city_on_volcanic,
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


def test_volcano_names_match_the_4_volcanic_hexes():
    # Los 4 hex_ids marcados volcanic=True en HEX_DEFS son exactamente los
    # 4 nombrados en VOLCANO_NAMES (verificado en HEX_MAP_RESEARCH.md contra
    # coordenadas areograficas oficiales de cada volcan + la posicion ya
    # verificada de Noctis City).
    volcanic_hex_ids = {hex_id for hex_id, hex_def in HEX_DEFS.items() if hex_def["volcanic"]}
    assert volcanic_hex_ids == set(VOLCANO_NAMES.keys()) == {"09", "14", "21", "29"}
    assert VOLCANO_NAMES == {
        "09": "tharsis_tholus", "14": "ascraeus_mons", "21": "pavonis_mons", "29": "arsia_mons",
    }
    for hex_id, name in VOLCANO_NAMES.items():
        assert HEX_DEFS[hex_id]["volcano_name"] == name
    # Ningun otro hexagono tiene volcano_name asignado
    for hex_id, hex_def in HEX_DEFS.items():
        if hex_id not in VOLCANO_NAMES:
            assert hex_def["volcano_name"] is None


def test_lava_flows_can_only_place_on_one_of_the_4_named_volcanoes():
    board = new_board()
    requirement = {"hex_id_in": list(VOLCANO_NAMES.keys())}
    for volcano_hex in VOLCANO_NAMES:
        assert can_place_special_tile(board, volcano_hex, requirement, "player-1") is True
    non_volcanic_land_hex = "05"
    assert HEX_DEFS[non_volcanic_land_hex]["volcanic"] is False
    assert can_place_special_tile(board, non_volcanic_land_hex, requirement, "player-1") is False

    new_board_state, hex_bonus, _ = place_special_tile(board, "09", requirement, "player-1", "lava_flows")
    assert new_board_state["09"]["tile_type"] == "special"
    assert new_board_state["09"]["card"] == "lava_flows"
    assert hex_bonus == HEX_DEFS["09"]["bonus"]  # Lava Flows no consume el bonus impreso del hex

    with pytest.raises(InvalidPlacementError):
        place_special_tile(board, non_volcanic_land_hex, requirement, "player-1", "lava_flows")


def test_can_place_city_on_volcanic_ignores_city_adjacency():
    board = new_board()
    volcano_hex = "09"  # Tharsis Tholus
    assert can_place_city_on_volcanic(board, volcano_hex) is True

    # A diferencia de can_place_city, IGNORA la adyacencia a otra ciudad
    board, _, _ = place_city_tile(board, "08", "player-1")  # vecino de 09
    assert can_place_city(board, volcano_hex) is False  # rechazado por adyacencia normal
    assert can_place_city_on_volcanic(board, volcano_hex) is True  # Lava Tube Settlement la ignora


def test_can_place_city_on_volcanic_rejects_non_volcanic_hex():
    board = new_board()
    non_volcanic_land_hex = "05"
    assert HEX_DEFS[non_volcanic_land_hex]["volcanic"] is False
    assert can_place_city_on_volcanic(board, non_volcanic_land_hex) is False


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


def test_count_tiles_adjacent_to_ocean_counts_each_tile_once():
    # FAQ oficial (Mud Slides): "Each tile is only counted once, even if next
    # to multiple ocean tiles".
    board = new_board()
    assert count_tiles_adjacent_to_ocean(board) == 0

    board, _, _ = place_ocean_tile(board, "04")
    board, _, _ = place_city_tile(board, "05", "p1")  # "05" es vecino de "04"
    assert count_tiles_adjacent_to_ocean(board) == 1  # solo la ciudad

    # dos oceanos pegados se cuentan entre si: son tiles adyacentes a oceano
    board2 = new_board()
    board2, _, _ = place_ocean_tile(board2, "06")
    board2, _, _ = place_ocean_tile(board2, "07")
    assert count_tiles_adjacent_to_ocean(board2) == 2


def test_count_empty_hexes_adjacent_to_owner_counts_each_hex_once():
    # Red Tourism Wave (T12, bloque 31): "Gain 1 M€ for each EMPTY AREA
    # ADJACENT TO YOUR TILES" -- mismo criterio de conteo unico que
    # count_tiles_adjacent_to_ocean.
    board = new_board()
    assert count_empty_hexes_adjacent_to_owner(board, "p1") == 0

    board, _, _ = place_city_tile(board, "05", "p1")
    neighbors = get_neighbors("05")
    empty_neighbors = [n for n in neighbors if n not in board]
    assert count_empty_hexes_adjacent_to_owner(board, "p1") == len(empty_neighbors)
    assert count_empty_hexes_adjacent_to_owner(board, "p2") == 0


def test_has_city_adjacent_to_ocean_filtra_por_dueno():
    # Outdoor Sports (X38) mira cualquier ciudad; Aqueduct Systems (X50), solo las propias
    board = new_board()
    assert has_city_adjacent_to_ocean(board) is False

    board, _, _ = place_ocean_tile(board, "04")
    board, _, _ = place_city_tile(board, "05", "p2")  # "05" es vecino de "04"
    assert has_city_adjacent_to_ocean(board) is True
    assert has_city_adjacent_to_ocean(board, owner="p1") is False
    assert has_city_adjacent_to_ocean(board, owner="p2") is True


def test_count_cities_and_special_tiles_adjacent_to_ocean_ignora_greeneries():
    # Red Ships (X62, bloque 36): cuenta ciudades Y special tiles, de cualquier
    # dueno; los greeneries y los oceanos entre si NO cuentan
    board = new_board()
    board, _, _ = place_ocean_tile(board, "04")
    assert count_cities_and_special_tiles_adjacent_to_ocean(board) == 0

    board, _, _ = place_city_tile(board, "05", "p1")          # vecino de 04
    board, _, _ = place_greenery_tile(board, "03", "p2", ignore_restrictions=True)  # vecino de 04
    assert count_cities_and_special_tiles_adjacent_to_ocean(board) == 1  # solo la ciudad

    # un special tile pegado al mismo oceano SI suma (y es de otro dueno)
    free_neighbor = next(
        h for h in get_neighbors("04")
        if h not in board and can_place_special_tile(board, h, {}, "p2")
    )
    board = place_special_tile(board, free_neighbor, {}, "p2", "una_carta")[0]
    assert count_cities_and_special_tiles_adjacent_to_ocean(board) == 2


def test_has_city_adjacent_to_ocean_ignora_ciudad_lejos_del_agua():
    board = new_board()
    board, _, _ = place_city_tile(board, "35", "p1")
    assert has_city_adjacent_to_ocean(board, owner="p1") is False


def test_remove_greenery_tile_solo_saca_greeneries_propios():
    # Kaguya Tech (X58, bloque 37)
    board = new_board()
    board, _, _ = place_greenery_tile(board, "05", "p1", ignore_restrictions=True)
    with pytest.raises(InvalidPlacementError):
        remove_greenery_tile(board, "05", "p2")          # no es suyo
    city_hex = next(h for h in HEX_DEFS if h not in board and can_place_city(board, h))
    board2, _, _ = place_city_tile(board, city_hex, "p1")
    with pytest.raises(InvalidPlacementError):
        remove_greenery_tile(board2, city_hex, "p1")      # no es un greenery
    freed = remove_greenery_tile(board, "05", "p1")
    assert is_hex_empty(freed, "05")


def test_nomads_se_mueven_a_hex_adyacente_y_cobran_el_bonus():
    # Mars Nomads (X59, bloque 37): marcador movil que NO es un tile
    board = new_board()
    board = place_nomads(board, "10")
    assert find_nomads(board) == "10"
    assert is_hex_empty(board, "10") is False              # ocupa el hex
    # no cuenta como tile de ningun tipo real
    assert count_tiles_of_type(board, "city") == 0
    assert count_tiles_of_type(board, "greenery") == 0

    destino = next(h for h in get_neighbors("10") if h not in board and HEX_DEFS[h]["hex_type"] != "ocean")
    board, bonus = move_nomads(board, destino)
    assert find_nomads(board) == destino
    assert is_hex_empty(board, "10") is True               # libera el anterior
    assert bonus == HEX_DEFS[destino]["bonus"]

    # no se puede mover a un hex no adyacente
    lejano = next(h for h in HEX_DEFS if h not in board and h not in get_neighbors(destino))
    with pytest.raises(InvalidPlacementError):
        move_nomads(board, lejano)


def test_place_cathedral_se_superpone_a_una_ciudad_y_es_unica():
    # St. Joseph of Cupertino Mission (X64, bloque 37)
    board = new_board()
    board, _, _ = place_city_tile(board, "05", "p1")
    board = place_cathedral(board, "05")
    assert count_cathedrals(board) == 1
    assert board["05"]["tile_type"] == "city"             # sigue siendo la ciudad
    with pytest.raises(InvalidPlacementError):
        place_cathedral(board, "05")                      # maximo 1 por ciudad
    with pytest.raises(InvalidPlacementError):
        place_cathedral(board, "06")                      # no hay ciudad ahi


def test_remove_ocean_tile_frees_the_hex():
    board = new_board()
    board, _, _ = place_ocean_tile(board, "04")
    assert is_hex_empty(board, "04") is False
    board = remove_ocean_tile(board, "04")
    assert is_hex_empty(board, "04") is True
    assert can_place_ocean(board, "04") is True  # se puede volver a colocar


def test_remove_ocean_tile_rejects_empty_hex_and_non_ocean():
    board = new_board()
    with pytest.raises(UnknownHexError):
        remove_ocean_tile(board, "04")
    board, _, _ = place_city_tile(board, "05", "p1")
    with pytest.raises(InvalidPlacementError):
        remove_ocean_tile(board, "05")


def test_community_reserva_el_hex_sin_ocuparlo():
    # Arcadian Communities: el marcador NO es un tile -- reserva el hexagono
    # pero se puede construir encima (al reves que el marcador de nomads).
    board = new_board()
    land = next(h for h, d in HEX_DEFS.items()
                if d["hex_type"] == "land" and d["reserved_city"] is None)

    con_community = place_community(board, land, "p1", require_adjacency=False)
    assert community_owner(con_community, land) == "p1"
    # Sigue contando como VACIO: construir ahi es justamente el objetivo.
    assert is_hex_empty(con_community, land) is True
    assert can_place_city(con_community, land) is True
    # Y ningun conteo de tiles lo encuentra.
    assert count_tiles_of_type(con_community, "city") == 0

    # No se puede poner dos veces en el mismo hexagono.
    with pytest.raises(HexOccupiedError):
        place_community(con_community, land, "p1", require_adjacency=False)


def test_community_exige_adyacencia_salvo_la_primera():
    board = new_board()
    land = next(h for h, d in HEX_DEFS.items()
                if d["hex_type"] == "land" and d["reserved_city"] is None)
    lejano = next(h for h, d in HEX_DEFS.items()
                  if d["hex_type"] == "land" and d["reserved_city"] is None
                  and h != land and h not in ADJACENCY[land])

    board = place_community(board, land, "p1", require_adjacency=False)
    # Un hexagono que no toca nada propio se rechaza.
    with pytest.raises(InvalidPlacementError):
        place_community(board, lejano, "p1")
    # Uno adyacente al community anterior, si.
    vecino = next(h for h in ADJACENCY[land]
                  if HEX_DEFS[h]["hex_type"] == "land" and HEX_DEFS[h]["reserved_city"] is None)
    assert community_owner(place_community(board, vecino, "p1"), vecino) == "p1"


def test_community_no_va_en_oceano_ni_en_hex_reservado():
    board = new_board()
    oceano = next(h for h, d in HEX_DEFS.items() if d["hex_type"] == "ocean")
    with pytest.raises(InvalidPlacementError):
        place_community(board, oceano, "p1", require_adjacency=False)
    with pytest.raises(InvalidPlacementError):
        place_community(board, NOCTIS_CITY_HEX_ID, "p1", require_adjacency=False)
