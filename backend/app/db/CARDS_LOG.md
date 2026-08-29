# Registro de cartas cargadas

Control de qué cartas del catálogo (~668 en la base de tm.hadronikle.com, ~200 son
de proyecto) ya están en `seed_cards.sql` con efecto implementado y testeado, para
no reverificar ni repetir trabajo en sesiones futuras.

No borrar filas al implementar una carta nueva — solo agregar.

**Regla de oro: no descartar cartas por falta de mecánica.** Si un efecto no encaja en el
vocabulario actual, la prioridad es extender el motor (nueva pieza en `apply_card_effect`,
`use_card_action`, o lo que haga falta) y agregar la carta con su test — no dejarla afuera.
"Descartada" es solo para el puñado de casos genuinamente irreducibles con el diseño actual
(típicamente: requieren un segundo jugador/tablero — el MVP es de un solo jugador — o
requieren el mapa hexagonal con adyacencia, que está fuera de alcance por decisión explícita
de sección 6 de CLAUDE.md, no por falta de tiempo). Cuando dudes, extendé el motor.

## Cargadas (en `seed_cards.sql`, con efecto en `apply_card_effect` y test)

| id | Nombre | # scan | Costo | Efecto |
|---|---|---|---|---|
| `sponsors` | Sponsors | 068 | 6 MC | +2 producción MC |
| `acquired_company` | Acquired Company | 106 | 10 MC | +3 producción MC |
| `investment_loan` | Investment Loan | 151 | 3 MC | -1 producción MC, +10 MC |
| `insulation` | Insulation | 152 | 2 MC | -X producción calor, +X producción MC (X a elección) |
| `nuclear_power` | Nuclear Power | 045 | 10 MC | -2 producción MC, +3 producción energía |
| `solar_power` | Solar Power | 113 | 11 MC | +1 producción energía |
| `titanium_mine` | Titanium Mine | 144 | 7 MC | +1 producción titanio |
| `solar_wind_power` | Solar Wind Power | 077 | 11 MC | +1 producción energía, +2 titanio (stock) |
| `artificial_photosynthesis` | Artificial Photosynthesis | 115 | 12 MC | Elección: +1 producción plantas O +2 producción energía |
| `mine` | Mine | 056 | 4 MC | +1 producción steel |
| `farming` | Farming | 118 | 16 MC | Requiere +4°C o más. +2 producción MC, +2 producción plantas, +2 plantas (stock) |
| `nitrophilic_moss` | Nitrophilic Moss | 146 | 8 MC | Requiere 3 océanos colocados. -2 plantas (costo obligatorio), +2 producción plantas |
| `ironworks` | Ironworks | 101 | 11 MC | Acción repetible: -4 energía, +1 steel, +1 paso oxígeno |
| `steelworks` | Steelworks | 103 | 15 MC | Acción repetible: -4 energía, +2 steel, +1 paso oxígeno |
| `regolith_eaters` | Regolith Eaters | 033 | 13 MC | Acción repetible con elección: +1 microbio (en la carta) O -2 microbios/+1 paso oxígeno |
| `comet` | Comet | 010 | 21 MC | +1 paso temperatura, coloca 1 océano (+2 TR) |
| `asteroid_card` | Asteroid | 009 | 14 MC | +1 paso temperatura, +2 titanio |
| `big_asteroid` | Big Asteroid | 011 | 27 MC | +2 pasos temperatura, +4 titanio |
| `capital` | Capital | 008 | 26 MC | Requiere 4 océanos. -2 producción energía, +5 producción MC, +1 ciudad (contador) |
| `martian_rails` | Martian Rails | 007 | 13 MC | Acción repetible: -1 energía → +1 MC por cada ciudad en Marte |
| `space_elevator` | Space Elevator | 013 | 27 MC | +1 producción titanio; acción repetible: -1 steel → +5 MC |
| `equatorial_magnetizer` | Equatorial Magnetizer | 015 | 11 MC | Acción repetible: -1 producción energía → +1 TR |
| `water_import_from_europa` | Water Import from Europa | 012 | 25 MC | Acción repetible: -12 MC → coloca 1 océano |

## Pendientes (requieren una pieza de mecánica que todavía no se agregó)

Estas NO son descartes definitivos — son casos donde ya se identificó qué falta agregar al
motor para desbloquearlas. Se resuelven agregando esa pieza, no evitando la carta.

| # scan | Nombre | Qué falta |
|---|---|---|
| 071 | Advanced Alloys | Efectos pasivos permanentes (modifica el valor de venta de steel/titanio en `calculate_card_payment` mientras la carta este activa). |
| 109 | Media Group | Tracking de "tipo de carta jugada" (evento) para disparar bonus pasivos al jugar otras cartas. |
| 190 | Local Heat Trapping | Elección que además targetea otra carta en juego del propio jugador (agregar recursos a una carta distinta a la que se está jugando). |
| 006 | Inventors' Guild | Sistema de mazo/robo de cartas (ver top card del mazo, comprarla o descartarla). |
| 014 | Development Center | Sistema de mano/robo de cartas (deck, mano del jugador, robar N cartas). |
| 094 | Mass Converter | Tracking de tags jugados por el jugador (`tags_played` contador) para el requisito "5 tags de ciencia"; la parte de descuento pasivo depende de lo mismo que Advanced Alloys. |
| 059 | Mangrove | Colocación de tiles en general — decisión explícita de mantener fuera de alcance del MVP (sección 6 de CLAUDE.md: sin mapa hexagonal). |
| 031 | Optimal Aerobraking | Mismo tracking de "tipo de carta jugada" que Media Group. |

## Fuera de alcance por diseño (no por mecánica faltante — ver CLAUDE.md sección 6)

Estas SÍ implican un jugador humano o IA adicional, o el mapa hexagonal con adyacencia —
ambos excluidos explícitamente del MVP. Se reevalúan si el alcance del proyecto cambia.

| # scan | Nombre | Motivo |
|---|---|---|
| 038 | Rover Construction | Bonus disparado por colocación de tile de ciudad de **cualquier jugador** — depende de multi-jugador + tiles. |
| 147 | Herbivores | Puede decrementar la producción de otro jugador — depende de multi-jugador. |

## Regla de diseño: "remove up to N &lt;recurso&gt; from any player"

Varias cartas (Comet, Asteroid, Big Asteroid, y probablemente más en el catálogo completo)
tienen una cláusula secundaria del tipo "remove up to N plants from any player". Es **opcional**
(0 a N) y sirve para hostigar a un oponente. Como el MVP es de un solo jugador, elegir 0 siempre
es una jugada legal — así que **se omite esta cláusula por completo** y se implementa el resto
del efecto (garantizado) de la carta normalmente. No es necesario targeting ni modelo
multi-jugador para estas cartas. Antes de descartar una carta por "targetea a otro jugador",
revisar si la cláusula es de este tipo opcional — si lo es, no bloquea nada.

## Vocabulario de `effects` soportado hoy en `rules_engine.apply_card_effect`

- `mc_production_delta` / `mc_delta`: formas antiguas (solo MC), mantenidas por compatibilidad.
- `production_deltas`: `{"<recurso>_production": delta, ...}` — forma genérica para cambiar
  una o más producciones a la vez (ej. Nuclear Power).
- `resource_deltas`: `{"<recurso>": delta, ...}` — forma genérica para cambiar stock de uno
  o más recursos (ej. Solar Wind Power).
- `convert_production`: `{"from": "<recurso>_production", "to": "<recurso>_production"}`,
  convierte `effect_amount` (X, provisto por el jugador) pasos de un recurso a otro.
- `raise_temperature_steps` / `raise_oxygen_steps`: N pasos, otorgan N de TR (ej. Comet).
- `place_oceans`: N — coloca N tiles de océano (+N TR) (ej. Comet).
- `place_city_tiles`: N — suma N al contador global `city_tiles_placed`, sin TR (ej. Capital).
- `choice`: lista de sub-effects (cualquiera de los de arriba); el jugador elige uno vía
  `effect_choice` (índice 0-based) (ej. Artificial Photosynthesis).

**Nota de firma:** `apply_card_effect(player, globals_, effects, effect_amount=None,
effect_choice=None)` recibe y devuelve SIEMPRE una tupla `(PlayerState, GlobalParameters)`,
incluso para cartas que no tocan el tablero global (necesario porque algunas cartas sí lo
hacen directamente, no solo via proyectos estándar).

Un `resource_deltas` negativo que dejaría el stock por debajo de 0 lanza
`InsufficientResourcesError` — se trata como costo obligatorio de la carta, no como tope
silencioso (ej. Nitrophilic Moss: "pierde 2 plantas" falla si el jugador tiene menos de 2).

Para cartas nuevas preferí `production_deltas`/`resource_deltas` sobre las formas antiguas
(son más generales). Si el efecto no encaja en este vocabulario, hay que extenderlo (con su
test) antes de agregar la carta a `seed_cards.sql`.

## Cartas activas: acción repetible + recursos propios (`rules_engine.use_card_action`)

Algunas cartas quedan "en juego" después de pagarlas porque tienen una acción que se puede
usar una vez por generación (ej. Ironworks) y/o guardan sus propios recursos (ej. microbios
de Regolith Eaters). Se activan con `effects.becomes_active: true` en `cards`, y su acción
vive en `effects.action`:

- `cost`: `{"<recurso>": N, ...}` gastado del stock del jugador. La clave especial
  `"card_resource"` gasta N recursos guardados en la propia carta.
- `gains`: `resource_deltas`, `production_deltas` (igual que en `apply_card_effect`),
  `raise_oxygen_steps` / `raise_temperature_steps` / `place_oceans` (suben el parámetro
  global y dan TR), `card_resource_delta` (agrega recursos a la propia carta), `tr_delta`
  (sube el TR directo, sin pasar por un parámetro global — ej. Equatorial Magnetizer), y
  `mc_per_counter`: `"<contador>"` (da tanto MC como valga ese contador global — ej. Martian
  Rails: MC por cada ciudad en `city_tiles_placed`).
- `choice`: lista de sub-specs alternativos, elegidos con `effect_choice` (igual patrón que
  en `apply_card_effect`).

El tool `use_card_action(player_id, card_id, effect_choice)` la ejecuta. `action_used` se
resetea a `False` en cada `run_production_phase` (una acción por carta por generación, regla
oficial). `player.active_cards` (jsonb en Supabase) guarda `{card_id: {resources, action_used}}`.

## Requisitos de cartas (columna `requirements`, validados en `check_card_requirements`)

- `min_temperature`: temperatura mínima en grados C (ej. Farming: 4).
- `min_oxygen`: oxígeno mínimo en % (ninguna carta cargada lo usa todavía, pero está soportado).
- `min_oceans`: cantidad mínima de tiles de océano colocados (ej. Nitrophilic Moss: 3).

`tools.play_card` valida el requisito contra `global_parameters` antes de cobrar la carta —
si no se cumple, lanza `CardRequirementNotMetError` y no se paga nada.

## Contador global de ciudades (`GlobalParameters.city_tiles_placed`)

Igual que `oceans_placed`, cuenta tiles de ciudad colocados por **cualquier** jugador (no se
trackea de quién es cada uno — no hay mapa hexagonal, ver CLAUDE.md sección 6). Se incrementa
en `standard_project_city` y en cartas con `place_city_tiles` en `effects`. Suficiente para
cartas que pagan "por cada ciudad en Marte" (ej. Martian Rails) sin necesitar el tablero
completo con adyacencia.

## Fuente de verificación

Scans oficiales vía https://tm.hadronikle.com (base de datos no oficial de cartas,
668 escaneos full-res). Cada carta se lee directamente del scan antes de cargarla —
nunca de memoria — para no romper el objetivo de "100% de precisión" del PRD.
