# Investigación: mecánica del tablero hexagonal de Terraforming Mars

Investigación de referencia (2026-08-31) para extender el motor con el mapa de Marte.
**Decisión de alcance confirmada por el usuario el 2026-08-31**: el mapa Tharsis se
implementa (ver CLAUDE.md sección 6, actualizada). Motivada por tres cartas del catálogo que
lo necesitan de verdad: Mining Area, Land Claim, Mining Rights (ver "Pendientes" en
`CARDS_LOG.md`).

**Estado de implementación:** `backend/app/agent/board.py` (61 hexágonos, adyacencia,
colocación de ocean/city/greenery, bonus de hex y de adyacencia oceánica),
`backend/tests/test_board.py` (22 tests), y el cableado a `tools.py` (`use_standard_project`,
`convert_resources`, `play_card`, `use_card_action` ahora aceptan `hex_id`/`ocean_hex_ids`/
`city_hex_ids` según corresponda, más la tool nueva `get_board_state`) están implementados y
**probados end-to-end contra Supabase real** (2026-08-31): aquifer/city con bonus de hex y de
adyacencia oceánica, rechazo de hex inválido/ocupado, Comet y Lake Marineris colocando 1 y 2
océanos respectivamente vía `play_card`, Water Import from Europa colocando océano vía
`use_card_action`, y el bonus de adyacencia oceánica acumulándose correctamente entre
colocaciones sucesivas dentro de la misma carta. Persistencia: columna `board` (jsonb) en
`global_parameters`.

Nota de dependencia: hubo que actualizar `supabase` de 2.7.4 a 2.31.0 en `requirements.txt` —
la versión vieja del cliente Python rechazaba las API keys del formato nuevo de Supabase
(`sb_publishable_...`/`sb_secret_...`) porque validaba con una regex que exigía forma de JWT.

Mining Area, Mining Rights y Land Claim (las 3 cartas de "Pendientes" en `CARDS_LOG.md`)
siguen sin cargar porque necesitan una pieza más: `place_special_tile` genérica parametrizada
por `requirement` (ver sección 11 más abajo) — el resto del cableado ya está listo para
soportarlas.

**Corrección importante sobre la premisa inicial de esta investigación:** se asumió al
arrancar que había 9 hexágonos reservados para océano (confundiendo el límite de 9 océanos
JUGABLES en toda la partida — regla real y distinta — con la cantidad de hexágonos donde se
pueden colocar). El número real, **verificado con dos fuentes independientes**, es **12**:
1. Código fuente de `TharsisBoard.ts` (terraforming-mars/terraforming-mars): 12 llamadas
   `.ocean(...)`.
2. Reglamento oficial, transcripción textual en rulespal.com: *"12 areas on the game board
   that are reserved for ocean tiles"*.

Los BONUS específicos de cada hexágono individual (qué hexágono da steel/titanium/plants/
cards y cuánto) y la asignación de nombres a los 4 hexágonos volcánicos (Tharsis Tholus/
Ascraeus/Pavonis/Arsia Mons) salen **únicamente** del código fuente — no se re-verificó cada
uno contra una segunda fuente independiente (solo el conteo total de océanos se verificó así).
El código es igualmente la fuente más confiable disponible (motor ampliamente jugado y
testeado en producción), pero queda anotado por transparencia.

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
- Océano reservado (12 espacios, ver corrección más abajo) — solo admite tile de océano.
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

## 9. Tabla completa de 61 hexágonos (implementada en `board.py`)

Transcrita directo de `TharsisBoard.ts`. Convención: `id` = string de 2 dígitos (03-63, los
ids 01/02 son Ganymede Colony/Phobos Space Haven, fuera del mapa de Marte), `row` = fila
0-based (0 arriba, 8 abajo), `x` = columna absoluta 0-8 (`xOffset + posición_en_la_fila`,
`xOffset = 9 - hexágonos_en_esa_fila`).

| Fila | Hexágonos (id: tipo, bonus) |
|---|---|
| 0 (5, xOffset 4) | 03:land[steel2] · 04:ocean[steel2] · 05:land · 06:ocean[card1] · 07:ocean |
| 1 (6, xOffset 3) | 08:land · 09:land☡[steel1] · 10:land · 11:land · 12:land · 13:ocean[card2] |
| 2 (7, xOffset 2) | 14:land☡[card1] · 15:land · 16:land · 17:land · 18:land · 19:land · 20:land[steel1] |
| 3 (8, xOffset 1) | 21:land☡[plant1,titanium1] · 22:land[plant1] · 23:land[plant1] · 24:land[plant1] · 25:land[plant2] · 26:land[plant1] · 27:land[plant1] · 28:ocean[plant2] |
| 4 (9, xOffset 0) | 29:land☡[plant2] · 30:land[plant2] · **31:land[plant2] (Noctis City)** · 32:ocean[plant2] · 33:ocean[plant2] · 34:ocean[plant2] · 35:land[plant2] · 36:land[plant2] · 37:land[plant2] |
| 5 (8, xOffset 1) | 38:land[plant1] · 39:land[plant2] · 40:land[plant1] · 41:land[plant1] · 42:land[plant1] · 43:ocean[plant1] · 44:ocean[plant1] · 45:ocean[plant1] |
| 6 (7, xOffset 2) | 46:land · 47:land · 48:land · 49:land · 50:land · 51:land[plant1] · 52:land |
| 7 (6, xOffset 3) | 53:land[steel2] · 54:land · 55:land[card1] · 56:land[card1] · 57:land · 58:land[titanium1] |
| 8 (5, xOffset 4) | 59:land[steel1] · 60:land[steel2] · 61:land · 62:land · 63:ocean[titanium2] |

`☡` = hexágono volcánico (4 en total: 09, 14, 21, 29 — forman la diagonal noroeste). El código
fuente no asigna nombre individual (Tharsis Tholus/Ascraeus Mons/Pavonis Mons/Arsia Mons) a
cada uno — dato no verificado, se dejó sin asignar en `board.py`.

Conteo de verificación: 12 hexágonos `ocean` (04,06,07,13,28,32,33,34,43,44,45,63) ✓ coincide
con las dos fuentes citadas arriba.

## 11. Estructura de datos y funciones — YA IMPLEMENTADO en `board.py`

```python
TileType = Literal["city", "greenery", "ocean"]
HexType  = Literal["land", "ocean"]

class HexDef(TypedDict):   # ESTATICO, nunca cambia -- constante HEX_DEFS
    id: str
    row: int
    x: int
    hex_type: HexType
    volcanic: bool
    bonus: list[tuple[str, int]]
    reserved_city: str | None

class HexState(TypedDict):  # MUTABLE, esto es lo que se persiste
    tile_type: TileType
    owner: str | None       # None = neutral (oceano)
    bonus_consumed: bool

Board = dict[str, HexState]
```

Implementadas y testeadas (22 tests en `test_board.py`): `get_neighbors`, `is_hex_empty`,
`get_adjacent_tiles`, `count_adjacent_oceans`, `count_adjacent_owned_by`,
`count_tiles_of_type`, `can_place_ocean`, `can_place_city`, `can_place_greenery`,
`resolve_hex_bonus`, `resolve_ocean_adjacency_bonus`, `place_ocean_tile`, `place_city_tile`,
`place_greenery_tile`. La adyacencia (`ADJACENCY`) se precalcula una sola vez al importar el
módulo, igual que recomienda la investigación (sección 2) -- no se recalcula en cada consulta.

### Pendiente para una segunda iteración (fuera de esta primera pasada, a propósito)

- ~~Cablear `board.py` a `tools.py`/`cards`~~ — HECHO (2026-08-31, ver arriba).
- `place_special_tile(board, hex_id, player, card_name, requirement)` genérica, para
  desbloquear Mining Area/Mining Rights/Land Claim sin hardcodear cada una.
- No hardcodear las ~20 special tiles particulares del catálogo completo.
- No implementar mapas alternativos (Hellas/Elysium) ni el pago cruzado de Ares.
- Nombrar los 4 hexágonos volcánicos (Tharsis Tholus/Ascraeus/Pavonis/Arsia Mons) si alguna
  carta futura los distingue individualmente (no verificado, ver sección 9).

## Fuente

Reglas oficiales resumidas, wikis de fans, BoardGameGeek, e implementación open-source
`terraforming-mars/terraforming-mars` (TypeScript) como referencia de modelo de datos.
