# Investigación: mecánica del tablero hexagonal de Terraforming Mars

Investigación de referencia (2026-08-31) para eventualmente extender `rules_engine.py` con
el mapa de Marte, hoy fuera de alcance del MVP (ver CLAUDE.md sección 6). Este documento
**no implica que la feature esté decidida ni implementada** — es la base técnica para cuando
se tome esa decisión de alcance explícitamente. Motivada por tres cartas del catálogo que la
necesitan de verdad: Mining Area, Land Claim, Mining Rights (ver "Pendientes" en
`CARDS_LOG.md`).

## 1. Estructura del tablero

**Mapa base (Tharsis):** ~61 hexágonos de terreno en una grilla romboidal de 9 filas
(5,6,7,8,9,8,7,6,5 hexágonos por fila), más un anillo no jugable (espacio/órbita).

**Coordenadas:** las implementaciones digitales conocidas (la referencia más sólida es
`terraforming-mars/terraforming-mars`, TypeScript, open-source) no usan coordenadas
axiales/cube académicas. Cada hex tiene un `id` único; el mapa es estático y su grafo de
adyacencia se **precalcula una sola vez** como dato constante, no se deriva geométricamente
en runtime (evita bugs de paridad de fila en el offset de la mitad superior/inferior del
rombo).

**Tipos de terreno:**
- Tierra normal (land) — sin restricción de tipo de tile.
- Océano reservado (9 espacios) — solo admite tile de océano.
- Reservado para ciudad específica (ej. Noctis City) — solo esa carta puede colocar ahí.
- Terreno con bonus impreso (steel, titanium, plants, cards, MC) — se consume la primera vez
  que se coloca un tile ahí.

## 2. Adyacencia

Cada hex tiene hasta 6 vecinos (menos en bordes: 3, 4 o 5). Adyacencia = comparten arista, no
solo vértice. No hay wraparound. La forma robusta de implementarlo (la que usan los motores
open-source) es una **tabla estática `hex_id -> [hex_ids vecinos]`** definida una sola vez al
crear el mapa, no una fórmula geométrica universal (la fila central del rombo invierte el
offset respecto a las mitades superior/inferior, lo cual es más simple de precalcular que de
computar caso por caso).

## 3. Colocación de tiles: tipos y legalidad

| Tile | Legalidad |
|---|---|
| Ocean | Solo en hex reservado para océano; sin requisito de adyacencia; sube TR 1 (hasta 9 océanos) |
| Greenery | Tierra normal; debe ser adyacente a un tile propio si existe alguna opción legal así; libre si el jugador no tiene tiles todavía. Sube oxígeno 1 |
| City | Tierra normal; NO puede ser adyacente a ninguna otra ciudad (de cualquier dueño) |
| Special tiles de cartas (Mining Rights/Area, Ecological Zone, Mohole Area, etc.) | Reglas por carta — normalmente exigen hex con bonus específico (steel/titanium), a veces con adyacencia a tile propio adicional |

Un hex ya ocupado no admite otro tile.

## 4. Bonus de colocación

1. **Bonus impreso en el hex**: al jugador que coloca, se consume una sola vez.
2. **Bonus de adyacencia oceánica**: +2 MC por cada océano YA colocado adyacente al hex donde
   se coloca (de cualquier dueño, el océano es neutral). Acumulativo.
3. *(Expansión Ares, no aplica al juego base)*: pago cruzado cuando otro jugador coloca
   adyacente a tu special tile.

## 5. Cartas que interactúan con el mapa (patrones recurrentes)

- Conteo de adyacencia propia ("+X por cada Y adyacente a esta carta/tile").
- Requisito de colocación en terreno con bonus específico (Mining Area/Rights).
- Requisito de adyacencia a tile propio para jugar la carta.
- Conteo global de tiles de cierto tipo en todo el mapa (sin importar adyacencia ni dueño).
- Bonus retroactivo por océanos adyacentes ya existentes.

## 6. Qué es inherentemente multi-jugador vs. modelable en single-player

**Inherentemente multi-jugador:** pago cruzado de Ares entre dueños distintos; cartas que
cuentan tiles de "otros jugadores" específicamente; puntuación competitiva de fin de partida.

**Igual de válido en single-player:** adyacencia con tiles propios, conteo de tiles propios o
totales en el mapa, bonus de hex, bonus de adyacencia oceánica (el océano es neutral),
legalidad de océano/ciudad (aplica aunque el jugador esté solo).

**Conclusión:** ~90% de la mecánica de tablero aplica igual en single-player. Lo único
omitible con seguridad es el pago cruzado entre dueños distintos (exclusivo de la expansión
Ares).

## 7. Modelo de datos de referencia (`terraforming-mars/terraforming-mars`)

Cada hex es un objeto `Space` con: `id`, `spaceType` (LAND/OCEAN), `bonus` (lista de recursos,
se vacía al usarse), `tile` (tipo + carta si es special tile), `player` (dueño, `undefined` si
es neutral como el océano), `x`/`y` solo para posicionamiento visual. La adyacencia se
resuelve con `getAdjacentSpaces(space)`, que aplica el offset correcto según la mitad del
rombo — no hardcodea 61 filas de tabla pero tampoco es una fórmula geométrica genérica de
grilla hexagonal estándar; está especializada al layout fijo de Tharsis/Hellas/Elysium.

## 8. Síntesis propia — tamaño del trabajo comparado con el motor actual

Salto de complejidad real pero acotado: el mapa es estático y conocido de antemano (no hay
que generar geometría dinámica), así que es más trabajo de "modelado de datos + enumerar
reglas de legalidad por tipo de hex/tile" que de algoritmos difíciles. El grueso del esfuerzo
real está en las ~15-20 cartas con special tiles particulares, no en la adyacencia en sí.
Estimación cualitativa: un módulo nuevo del orden de 3-4 veces el tamaño del módulo de
parámetros globales actual, con funciones individuales igual de pequeñas y puras que las
existentes (`raise_temperature`, `place_ocean`) — solo que trabajando sobre una estructura no
escalar.

## 9. Estructura de datos mínima propuesta (MVP single-player, sin implementar todavía)

```python
TileType = Literal["city", "greenery", "ocean", "special:<nombre>"]
HexType  = Literal["land", "ocean_reserved", "city_reserved"]

class Hex(TypedDict):
    id: str
    hex_type: HexType
    bonus: list[ResourceBonus]   # se vacía al usarse
    tile: Tile | None

class Tile(TypedDict):
    tile_type: TileType
    owner: str | None            # None = neutral (oceano)
    card: str | None             # si es special tile ligada a una carta

class Board(TypedDict):
    hexes: dict[str, Hex]
    adjacency: dict[str, list[str]]   # tabla ESTATICA, constante del modulo
```

### Funciones puras propuestas (mismo estilo que `raise_temperature`, `place_ocean`)

**Consultas:**
- `get_neighbors(board, hex_id) -> list[str]`
- `get_adjacent_tiles(board, hex_id) -> list[Tile]`
- `count_adjacent_oceans(board, hex_id) -> int`
- `count_adjacent_owned_by(board, hex_id, player) -> int`
- `is_hex_empty(board, hex_id) -> bool`

**Validación de legalidad (puras, bool o excepción, no mutan):**
- `can_place_ocean(board, hex_id) -> bool`
- `can_place_city(board, hex_id) -> bool`
- `can_place_greenery(board, hex_id, player) -> bool`
- `can_place_special_tile(board, hex_id, requirement) -> bool`

**Mutación (reciben estado, devuelven nuevo estado):**
- `place_tile(board, hex_id, tile) -> Board` (genérica, limpia el bonus consumido)
- `place_ocean(board, hex_id) -> Board`
- `place_city(board, hex_id, player) -> Board`
- `place_greenery(board, hex_id, player) -> Board` (dispara `raise_oxygen`)
- `place_special_tile(board, hex_id, player, card_name) -> Board`

**Bonus:**
- `resolve_hex_bonus(board, hex_id) -> ResourceDelta`
- `resolve_ocean_adjacency_bonus(board, hex_id) -> int` (2 × océanos vecinos)

**Puntuación (fin de partida, cuando corresponda):**
- `count_city_greenery_vp(board) -> dict[player, int]`
- `count_tiles_of_type(board, tile_type, owner=None) -> int`

### Alcance recomendado si se decide implementar

No hardcodear todavía las ~20 special tiles particulares — dejar `place_special_tile`
genérica con `requirement` parametrizable, y postergar el catálogo completo de cartas de mapa
para una segunda iteración. Tampoco implementar mapas alternativos (Hellas/Elysium) ni el pago
cruzado de Ares en esta primera pasada.

## Fuente

Reglas oficiales resumidas, wikis de fans, BoardGameGeek, e implementación open-source
`terraforming-mars/terraforming-mars` (TypeScript) como referencia de modelo de datos.
