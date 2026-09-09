# AGENTS.md

Contexto para cualquier agente de codificación (Claude Code, Codex, Cursor, etc.) que trabaje
en este repositorio. Léelo por completo antes de tocar código. Es la versión agnóstica de
herramienta de `CLAUDE.md` — mismo contenido de fondo, actualizado al estado real del proyecto.

## 1. Qué es este proyecto

**Árbitro Asistente de Reglas para Terraforming Mars**: un agente de IA que resuelve cálculos de
turnos (fase de producción, proyectos estándar, subida de parámetros globales, colocación de
tiles en el mapa) y valida el pago de cartas de proyecto. El usuario escribe una consulta en
lenguaje natural ("quiero usar el proyecto estándar Ciudad", "cerrá mi fase de producción",
"quiero jugar la carta X pagando 4 MC y 3 de acero") y el sistema responde con un veredicto y el
estado actualizado, calculado por Python puro, nunca por el LLM.

Es un proyecto de práctica/portfolio para demostrar habilidades de ML/AI Engineering — el
objetivo no es "un chatbot más", sino demostrar **control arquitectónico estricto sobre un LLM
probabilístico**.

## 2. Principio arquitectónico no-negociable

> **El LLM nunca hace matemática. Nunca.**

El LLM tiene exactamente un trabajo: parsear la intención del usuario y extraer argumentos
estructurados (`{"card_id": "X", "qty_titanio": 5, "qty_acero": 2, "hex_id": "24"}`). Todo
cálculo de saldo, validación de reglas de colocación/redención y comparación contra el estado
del juego se hace en **funciones Python puras y deterministas**
(`backend/app/agent/rules_engine.py`, `backend/app/agent/board.py`), nunca en el texto generado
por el modelo.

Esto se aplica en dos capas:
1. **System prompt** (`backend/app/agent/prompts.py`): le prohíbe explícitamente al modelo
   responder con números calculados por él mismo; su única salida legítima es una tool call o
   una respuesta que repite literalmente el resultado que le devolvió la tool.
2. **Grafo determinista** (`backend/app/agent/graph.py`): el `StateGraph` de LangGraph enruta
   *siempre* por el `ToolNode` antes de generar la respuesta final — no hay camino donde el LLM
   responda directo sin pasar por herramientas cuando la consulta implica un cálculo.

Cualquier cambio que le dé al LLM la posibilidad de "adivinar" un número es un bug de
arquitectura, no una mejora de UX.

## 3. El motor de reglas

Dos módulos puros, sin dependencias de LangGraph/FastAPI/Supabase, 100% testeados contra números
verificados del reglamento oficial. `tools.py` es un wrapper delgado que carga/guarda estado en
Supabase y orquesta llamadas a estos módulos.

### `backend/app/agent/rules_engine.py` — el corazón del repo

- Terraform Rating: arranca en 20, +1 por cada paso de parámetro global subido.
- Parámetros globales: temperatura (-30 a +8, pasos de 2°C), oxígeno (0 a 14%, pasos de 1%),
  océanos (0 a 9 tiles, con 12 hexágonos reservados donde colocarlos — ver sección 4), Venus
  scale (expansión Venus Next, 0% a 30%, pasos de 2%, con bonus de umbral: +1 carta gratis al
  cruzar 8%, +1 TR extra al cruzar 16% — no es condición de fin de partida), con clamping
  correcto al tope y sin otorgar TR por pasos no aplicados.
- Los 6 proyectos estándar con sus costos reales (sell_patents, power_plant, asteroid, aquifer,
  greenery, city).
- Conversiones del tablero de jugador (8 plantas → greenery, 8 calor → +1 paso de temperatura).
- Fase de producción completa, pago de cartas con acero/titanio sin reembolso por sobrepago.
- Sistema de mazo/mano/investigación (`deck`/`hand`/`pending_research`), tags jugados, efectos
  pasivos permanentes, historial de cartas jugadas (`played_cards`).
- Vocabulario extensible de `effects` en `apply_card_effect` (production_deltas, resource_deltas,
  choice, tag_count_choice, production_delta_per_tag, tr_delta_per_tag, resource_delta_per_counter,
  draw_cards, start_research, duplicate_production, target_card_resource_delta/`_2` + `target_min_resources`
  (agregar recursos a otra(s) carta(s) activa(s) elegida(s) por el jugador), place_greenery
  (con `ignore_restrictions` opcional), next_card_discount_mc, next_card_requirement_tolerance_steps,
  etc.) y de `requirements` en `check_card_requirements` (min/max_temperature, min/max_oxygen,
  min/max_oceans, min_city_tiles, min_tag_count, min_production). `use_card_action` suma
  `move_from_target_card_resource_delta` (mueve recurso desde otra carta activa) y
  `convert_resource_amount` + `effect_amount` (convierte una cantidad variable elegida por el
  jugador). Pasivos nuevos en `register_passive_effect`: `on_greenery_placed_add_resource`,
  `on_city_tile_placed_add_resource`/`_production_delta`, `on_tag_played_choice` (elección
  opcional del jugador al dispararse, no automática como `on_tag_played_add_resource`),
  `global_requirements_tolerance_steps`, `on_standard_project_used`. `players` tiene dos campos
  de un solo uso que se consumen al jugar/chequear la próxima carta y se pierden si no se usan
  en la generación: `pending_mc_discount` y `pending_requirement_tolerance_steps`. Ver el
  detalle completo y ejemplos reales en `backend/app/db/CARDS_LOG.md`.

### `backend/app/agent/board.py` — el mapa hexagonal (Tharsis)

Decisión de alcance explícita del usuario (2026-08-31): el tablero SÍ se modela (antes estaba
fuera del MVP). 61 hexágonos, adyacencia precalculada, bonus de colocación, océano reservado
(12 hexágonos, verificado con dos fuentes independientes — ver `HEX_MAP_RESEARCH.md`), Noctis
City reservada, 4 hexágonos volcánicos. Funciones de colocación de ocean/city/greenery/special
tiles, incluidas variantes "inversas" de las reglas normales (ver `CARDS_LOG.md`, sección
"Colocaciones inversas en el tablero") para cartas como Artificial Lake (océano en hex NO
reservado) o Urbanized Area (ciudad que EXIGE adyacencia a otras ciudades). Cableado completo a
`tools.py` (`use_standard_project`, `convert_resources`, `play_card`, `use_card_action` aceptan
`hex_id`/`ocean_hex_ids`/`city_hex_ids`/`special_tile_hex_id`; tool `get_board_state` para que el
LLM le muestre opciones al usuario). Alcance de esta primera pasada: solo Tharsis (no
Hellas/Elysium), sin pago cruzado de la expansión Ares, `place_special_tile` genérica
parametrizada por `requirement` (no hardcodea cada special tile de carta).

## 4. Catálogo de cartas

**No se generan datos al voleo** — un número mal recordado rompe el "100% de precisión" del
PRD. Cada carta se carga a mano, verificada contra su scan oficial (fuente: base de datos de
cartas de tm.hadronikle.com), con su efecto modelado en `rules_engine.py`/`board.py` y su test.

**Flujo de trabajo actual (reemplaza el viejo manifiesto markdown):**
- La cola de cartas pendientes de revisar vive en la tabla `card_review_queue` de Supabase
  (columnas: `scan_number`, `name`, `expansion`, `image_url`, `reviewed`, `card_id`). Consultar
  `select * from card_review_queue where reviewed = false order by id limit 10` para el próximo
  bloque.
- `backend/scripts/enqueue_card_review_queue.py`: puebla la cola parseando el manifiesto viejo +
  el catálogo cacheado del sitio (nombre/expansión/scan → URL de imagen). Ya corrido una vez
  para las ~302 cartas que quedaban del scrape original.
- `backend/scripts/download_review_scans.py`: descarga los scans pendientes de a uno, con pausa
  de 2.5s entre pedidos (no bajar en paralelo ni en ráfaga — riesgo de bloqueo del sitio), a
  `backend/scripts/scan_cache/` (gitignored, NUNCA se commitean — derechos de autor de
  FryxGames). Reanudable, salta archivos ya descargados.
- `backend/scripts/mark_reviewed.py`: marca una fila como revisada (con o sin `card_id`, según
  si terminó cargada o quedó pendiente/fuera de alcance) una vez que se decide su
  costo/tags/effects y se agrega a `seed_cards.sql`.
- **Lo que NINGÚN script automatiza**: decidir el costo/tags/efecto de cada carta. Eso requiere
  leer el scan y mapear su texto exacto al vocabulario del motor (o extenderlo si hace falta) —
  trabajo manual, carta por carta, el mismo criterio en cada sesión.

**Regla de oro (explícita del usuario): no descartar cartas por falta de mecánica.** Cuando una
carta no encaja en el vocabulario actual, la prioridad es extender el motor (nueva pieza en
`apply_card_effect`/`check_card_requirements`/`board.py`/`use_card_action`) y cargarla con su
test — no dejarla afuera. Las únicas exclusiones legítimas son: (a) mecánica genuinamente
multi-jugador sin sentido en single-player (ver sección "Fuera de alcance" en `CARDS_LOG.md`), o
(b) una pieza de mecánica ya identificada pero deliberadamente pospuesta para resolver varias
cartas juntas (ver sección "Pendientes" en `CARDS_LOG.md`).

**Cláusulas que se omiten por diseño (no por pereza), documentadas en `CARDS_LOG.md`:**
- "remove/steal up to N `<recurso>` from any player" (opcional, elegir 0 es siempre legal en
  single-player) → se omite entera, se implementa el resto del efecto garantizado.
- Cláusulas que dependen de tags/recursos de OPONENTES (ej. Toll Station) → siempre resuelven a
  0 en single-player, no es una mecánica faltante.
- Efectos que solo otorgan VP sin tocar ningún contador del motor (ej. Interstellar Colony Ship,
  Trans-Neptune Probe) → `effects: {}`, el motor no trackea puntuación.

**Antes de cargar cartas nuevas:** revisar `backend/app/db/CARDS_LOG.md` — lleva el registro de
qué cartas ya están cargadas, cuáles están "Pendientes" (con la pieza de mecánica que les falta)
y cuáles quedan "Fuera de alcance" por diseño. `backend/app/db/CARDS_PENDING_REVIEW.md` quedó
**deprecado** desde 2026-08-31 (congelado en el bloque 10) — no es la fuente de verdad, usar
`card_review_queue`.

### 📍 Punto de retoma (última sesión: 2026-09-08, corporaciones arrancadas)

**Corporaciones, bloque 1 (2026-09-08): infraestructura + 9 de 10 cargadas.** Era el hueco
grande que quedaba. Tabla nueva `corporation_cards` (id, name, expansion, tags, **starting_mc**,
effects), cola `corporation_review_queue` (clave = NOMBRE: el índice del sitio trae `num` vacío
para esta categoría), script `scripts/enqueue_corporation_review_queue.py` y tool
`tools.choose_corporation`. **Hay que correr `schema.sql` y `seed_corporations.sql` de nuevo
contra Supabase.**

**La decisión de reglas que define la mecánica:** hoy el motor arranca con producción 1 en cada
recurso, pero el scan de Beginner Corporation no muestra ninguna producción. El rulebook oficial
lo resuelve — *"You start with 1 production of each resource... **(only in standard game.)**"* —:
esa producción 1 es de la partida ESTÁNDAR; con corporación se arranca en **0** y la carta da lo
que diga. Por eso `apply_corporation_start` pone las seis producciones en 0 y **Beginner
Corporation se carga con production_deltas +1 en cada recurso**, reproduciendo la partida
estándar sin caso especial en el código.

Piezas nuevas: `on_venus_raised` (Aphrodite), `on_new_distinct_tag_played` (Aridor, va ANTES de
`increment_tags_played`), `on_cost_threshold_paid` (CrediCor: unión de
`on_card_played_cost_threshold_draw` con `on_standard_project_used`, sobre el costo BÁSICO) y
`plants_per_greenery` (EcoLine: 7 en vez de 8). Mismo hueco de cableado que las preludes:
`use_card_action` ahora también busca en `corporation_cards`. **Pendiente: Arcadian Communities**
(marcadores "community" que reservan hexágonos — familia de nomad/cathedral). Quedan 38
corporaciones sin revisar. Detalle en "Corporaciones" en `CARDS_LOG.md`.

**Tercera tanda seguida con errores de tags en los informes de agentes:** Celestic SÍ tiene tag
`venus` (leído como banner de expansión) y Cheung Shing Mars SÍ tiene `building` (leído como
parte del texto del Effect). Los atrapó la hoja de contacto. **La regla sigue firme: delegar el
análisis del efecto sí; verificar tags contra el scan, siempre.**

**Bloque de preludes 3 (2026-09-08): 4 de los 22 preludes "pendientes" cargados** -- Applied
Science (P43), Floating Trade Hub (P49), Main Belt Asteroids (P53) y World Government Advisor
(P67). No estaban trabados por el motor sino por **dos huecos de cableado en `tools.py`**:
`play_prelude` no registraba `becomes_active` (una prelude nunca llegaba a `active_cards`, así
que su acción no existía) y `use_card_action` buscaba el id solo en `cards`, no en
`prelude_cards`. Piezas nuevas: `raise_global_parameter_without_bonuses` (World Government
Advisor: subir un parámetro global SIN TR, sin bonus de umbral de Venus, sin pasivos y -- si es
océano -- sin bonus de hexágono); `own_card_only` + `resource_deltas` en el pasivo
`on_card_resource_gained` (Main Belt Asteroids paga "when gaining an asteroid HERE"); y
`gains.target_min_resources` en `use_card_action` (Applied Science: "any card WITH A RESOURCE").
**La elección del jugador -- qué parámetro global, qué recurso estándar -- se modela siempre como
una opción de `choice`**, porque `effect_choice` es el ÍNDICE de esa lista (un `int`), no un
nombre. **Bug agarrado por la prueba de humo, no por los tests:** `play_prelude` registraba el
pasivo dos veces y un pasivo duplicado paga dos veces (+2 titanio por 1 asteroide). Quedan 18
preludes pendientes. Detalle en "Prelude bloque 3" en `CARDS_LOG.md`.

**Progreso:** catálogo en **408 cartas de proyecto**, **36 Global Events** y **52 cartas
Prelude**. **La cola `card_review_queue` quedó en 0: no hay más cartas de proyecto por revisar.**
La cola de preludes también está en 0 (46 revisadas en el bloque 2: 26 cargadas, 20 pendientes
por mecánica).

**Bloque 38 (2026-09-08): las 11 últimas cargadas**, cerrando la cola. Piezas nuevas:
`spend_any_card_resource` (Soil Enrichment: gasta un recurso de CUALQUIER carta como efecto
inmediato — la versión de `apply_card_effect` del `cost.any_card_resource` que ya existía para
acciones), `min_own_city_tiles` (City Parks/Casinos: "requires that YOU have N city tiles", que
NO es lo mismo que `min_city_tiles`, el contador global) y `gains.mc_per_city_on_mars` (Weather
Balloons: cuenta los tiles del tablero, porque el contador global incluye las ciudades fuera del
mapa, que no están "on Mars").

**⚠️ ERROR DE ICONOGRAFÍA ENCONTRADO Y CORREGIDO (leer antes de cargar cartas nuevas):** el tag
`power` es un **RAYO blanco sobre círculo MORADO**; el **SOL DORADO de 8 puntas sobre negro es
`space`**. En los prompts multi-agente de los bloques 31-36 se describió mal ese ícono y varias
cartas quedaron con `power` donde va `space`. Hay prueba directa de ambos en el propio set:
Magnetic Shield dice "Requires 3 power tags" junto a rayos morados, y Asteroid Deflection System
dice "if it has a SPACE tag" junto al sol dorado. Se corrigieron 10 cartas verificadas una por
una (ver "Iconografía de tags" en `CARDS_LOG.md`).

**AUDITORÍA COMPLETADA (2026-09-08).** Se revisaron las 62 cartas con `power` de los bloques
1-30: **20 estaban bien, 42 mal.** El catálogo pasó de 71 a 33 cartas con `power` y de 46 a 84
con `space`. Aparecieron además tres errores de otro tipo: tags que faltaban
(`biomass_combustors`, `giant_space_mirror`, `solar_wind_power`, `solar_probe`), requisitos
leídos como tags propios (`power_supply_consortium`, `tectonic_stress_power` — el mismo error que
Mercurian Alloys) y dos cartas con un tag inventado que en el scan no tienen ninguno
(`aerial_lenses`, `trade_envoys`). Detalle completo en `CARDS_LOG.md`.

**Herramienta nueva, reusable:** `backend/scripts/tag_contact_sheet.py` recorta la banda superior
de cada scan (costo + recuadro de requisito + tags) y arma hojas de contacto de 8 cartas
etiquetadas. Verificar 62 cartas costó 8 hojas en vez de 62 scans completos, y con las bandas
apiladas la diferencia entre el rayo morado y el sol dorado salta a la vista. **Usarla para
cualquier auditoría visual futura del catálogo.**

**Bloque 37 (2026-09-08): NO fue revisión de cola, sino resolver mecánicas pendientes.** Se
cargaron las 5 cartas que estaban trabadas: las 4 del bloque 36 (Kaguya Tech, Mars Nomads,
Neptunian Power Consultants, St. Joseph of Cupertino Mission) más Diversity Support, pendiente
desde el bloque 33. **La tabla "Pendientes" de `CARDS_LOG.md` quedó con una sola fila: T11
Recruitment** (delegados neutrales por partido en Turmoil).

Las tres piezas de tablero nuevas se diseñaron juntas, no carta por carta (ver "Marcadores en el
tablero" en `CARDS_LOG.md`): `remove_greenery_tile`; el `TileType` nuevo `"nomad"` para un
marcador móvil que ocupa un hexágono pero que ningún conteo encuentra (`place_nomads` /
`move_nomads`); y `cathedral`, un campo opcional del `HexState` para un marcador SUPERPUESTO a
una ciudad que sigue existiendo debajo. Piezas nuevas fuera del tablero:
`min_distinct_resource_types` (Diversity Support), `cost.mc_or_steel` (análoga a
`mc_or_titanium`) y el par `on_ocean_placed_offer` + tool `resolve_ocean_offer`.

**Decisión de diseño que conviene recordar:** un pasivo OPCIONAL y PAGADO no se puede resolver
dentro de `place_ocean`, que corre sin interacción y desde muchísimos caminos. En vez de
propagar la decisión por todos ellos, `place_ocean` solo **anota** la oferta en el campo nuevo
`player.pending_ocean_offers` y una tool aparte la cobra después; las no usadas se pierden al
cerrar la generación. **`schema.sql` tiene una columna nueva (`pending_ocean_offers`), así que
hay que correrlo de nuevo contra Supabase** (la migración es idempotente).

**Bloque 36 (2026-09-08): 6 de 10 cargadas, 4 pendientes por mecánica grande.** Las 10 son del
set "CEO" de promos (ojo: el "CEO: APELLIDO" del encabezado es el crédito del diseñador, NO un
tag ni un requisito). Piezas nuevas: pasivo `on_temperature_raised` (Homeostasis Bureau, +3 M€
por PASO de temperatura, aplicado dentro de `raise_temperature` igual que `on_ocean_placed`);
pasivo `stock_resource_payment` (Martian Lumber Corp: las plantas pagan cartas building a 3 M€
— cuarta vía de pago, ver `CARDS_LOG.md`); `board.count_cities_and_special_tiles_adjacent_to_ocean`
+ `gains.mc_per_city_or_special_tile_adjacent_to_ocean` (Red Ships); `on_event_played` acepta
`draw_cards` y un `tag_filter` PROPIO dentro del bonus (Solar Logistics tiene dos pasivos con
filtros distintos, y el `tag_filter` compartido del dict no alcanzaba). Hermetic Order of Mars y
Teslaract salieron con vocabulario ya existente, sin tocar el motor.

**4 pendientes del bloque 36, todas por mecánica de TABLERO/decisión que no existe hoy** (ver la
tabla "Pendientes" de `CARDS_LOG.md` para el diagnóstico completo de cada una): Kaguya Tech
(remover un greenery propio y poner ciudad en ese hex), Mars Nomads (marcador móvil que no es un
tile y cobra bonus al moverse), Neptunian Power Consultants (`on_ocean_placed` opcional y pagado,
que necesita una decisión del jugador donde hoy el motor no puede pedirla) y St. Joseph of
Cupertino Mission (marcador de catedral SOBRE una ciudad ya colocada). Las tres primeras
comparten el mismo tema de fondo: **el tablero hoy solo sabe de tiles permanentes que ocupan un
hex vacío**; marcadores móviles, superpuestos o removibles son un concepto nuevo. Si se quiere
avanzar con ellas, conviene diseñarlo una sola vez para las cuatro.

**Bloque 35 (2026-09-07): 10 de 10 cargadas**, otra vez con orquestación multi-agente (10
subagentes Sonnet en paralelo). Piezas de motor nuevas: requisitos `any_city_adjacent_to_ocean`
y `own_city_adjacent_to_ocean` (Outdoor Sports / Aqueduct Systems, sobre
`board.has_city_adjacent_to_ocean`); pasivo `optional_energy_to_heat` + parámetro
`energy_to_convert` en `run_production_phase` (Supercapacitors: la conversión energía→calor deja
de ser obligatoria y la energía no convertida se conserva); effect
`retrieve_played_events_to_hand` (Astra Mechanica: la "pila de eventos" es `played_cards`
filtrado por `cards.is_event`); `card_resource_payment.required_tag` acepta LISTA (Carbon
Nanosystems: graphenes pagan space O city); `duplicate_production` acepta `count` +
`duplicate_production_target_card_ids` (Cyberia Systems: copia la producción de 2 cartas).

**Aprendizaje repetido de las tandas multi-agente:** 3 de 10 informes volvieron a fallar SOLO en
la lectura de tags/íconos (uno inventó un tag `water` inexistente confundiendo el recuadro de
requisito con los tags; otro reportó un tag `plant` en una carta sin tags, lo que además habría
metido un `include_this` de más; otro leyó "add 2 asteroids HERE" como "a cualquier carta"). El
mapeo del efecto al vocabulario, en cambio, sale bien. **Delegar el análisis del efecto sí;
verificar tags/banner/"here vs any card" contra el scan, siempre.**

**Bloque 34 (2026-09-07): 10 de 10 cargadas**, hecho con **orquestación multi-agente** (10
subagentes Sonnet en paralelo, uno por carta, analizando/diseñando sin tocar el repo;
integración y verificación centralizadas). Piezas de motor nuevas: pasivo
`on_card_resource_gained` (Meat Industry: +2 M€ por animal ganado en CUALQUIER carta; Topsoil
Contract: +1 M€ por microbio) -- implementado con **diff de totales** vía
`snapshot_card_resource_totals` + `apply_card_resource_gained_bonuses` en vez de enganchar los
~8 caminos que agregan recursos a cartas; y requirement `min_greenery_tiles_owned` (Harvest),
resuelto en `tools.play_card` porque necesita el tablero.

**Retrofit importante del bloque 34:** las cartas que guardan MICROBIOS (11) y ANIMALES (13) no
declaraban `active_card_resource_type` -- mismo hueco que tenían las de floaters. Ya está
corregido en `seed_cards.sql`, verificado carta por carta contra `CARDS_LOG.md`. Esto además
**desbloquea Diversity Support (X20)**, que quedó pendiente en el bloque 33 por esa misma
carencia: ahora se pueden contar los "9 tipos de recurso distintos" de verdad. Es el próximo
pendiente natural para retomar.

**Aprendizaje de la tanda multi-agente (confirma lo ya documentado):** 4 de los 10 informes
leyeron mal los tags o el banner (dos reportaron "sin tags" cartas que sí los tienen, uno omitió
`building`, otro marcó evento una carta de banner verde). Los efectos y el vocabulario propuesto,
en cambio, estuvieron bien en los 10. **Los agentes sirven para mapear el efecto al vocabulario;
los tags y el banner hay que verificarlos SIEMPRE contra el scan antes de cargar.**

**Bloque 33 (2026-09-07): 8 de 10 cargadas** (X15, X16, X18, X19, X21-X24 Promo; X17 Crash
Site Cleanup fuera de alcance -- mismo motivo que Law Suit; X20 Diversity Support pendiente
por mecánica -- necesita un retrofit de `active_card_resource_type` en las cartas de
microbio/animal ya cargadas, análogo al retrofit de floaters, para contar "9 tipos de recurso
distintos" con precisión; no se hizo a la ligera para no arriesgar un conteo incorrecto). Pieza
de motor nueva: `requires_requirement` en `card_cost_discount_mc` (Cutting Edge Technology,
filtra el descuento por si la carta jugada TIENE requisito propio, no por tag).

**Bloque 32 (2026-09-07): 9 de 10 cargadas** (X05, X07-X14 Promo; X06 Law Suit fuera de
alcance -- su requisito de juego depende de un oponente, nunca se cumple en single-player).
Piezas de motor nuevas: `production_delta_per_distinct_tag` (Interplanetary Trade, cuenta
tags DISTINTOS en vez de repeticiones de uno); `gains.mc_per_tag` en `use_card_action`
(Orbital Cleanup); requirement `min_party_leader_count` (Political Alliance); `gains.
mc_per_card_resource_including_spent` (Saturn Surfing, suma de vuelta lo gastado antes de
contar); passive `on_card_played_cost_threshold_production_delta` (Advertising, análoga a la
de robar cartas del bloque 29); `gains.reveal_top_deck_card_add_resource_if_tag`, resuelta en
`tools.use_card_action` por necesitar el catálogo (Asteroid Deflection System, mismo criterio
que `free_trade`). **Bug encontrado y corregido:** `cities_delta` en `tools.play_card`/
`play_prelude` no restaba lo aportado por un `place_city_tiles` propio (contador sin mapa),
rompiendo la jugabilidad real de Capital/Research Outpost/Phobos Space Haven (nunca agarrado
por los tests unitarios, que no pasan por `tools.py`) -- ver detalle en `CARDS_LOG.md`.

**Bloque 31 (2026-09-07): 9 de 10 cargadas** (T12-T16 Turmoil, X01-X04 Promo; T11 Recruitment
pendiente por mecánica). Piezas de motor nuevas: requirement
`party_leader_and_neutral_chairman` (Vote of No Confidence, reusa `turmoil["chairman"] is
None` sin tocar delegados) + effect `become_chairman_from_neutral`; `board.
count_empty_hexes_adjacent_to_owner` + effect `mc_per_empty_hex_adjacent_to_own_tiles` (Red
Tourism Wave); sentinel `"effect_amount"` como valor de `cost`/`gains.start_research.n` en
`use_card_action`, para costos/robos de cantidad VARIABLE elegida por el jugador sin tope fijo
(Hi-Tech Lab); `ratio` fraccionario en `convert_resource_amount` con validación de resultado
entero (Energy Market); effect `reset_card_action_used` + tool nueva `get_active_cards_state`
(Project Inspection, X02 -- repone el `action_used` de una carta activa elegida para poder
reusarla en la misma generación). Recruitment (T11) quedó pendiente: necesita delegados
NEUTRALES por partido, que `turmoil.py` no trackea hoy (ver "Pendientes" en `CARDS_LOG.md`).
**Bug encontrado en la prueba de humo, no en tests unitarios:** la clave real de
`use_card_action` para acciones con elección es `"choice"`, no `"options"` -- el primer intento
de Energy Market usó la clave equivocada y quedaba en un no-op silencioso (ver nota en
`CARDS_LOG.md`).

**Nota operativa:** el host de Supabase resuelve **solo por IPv6**. Si la máquina pierde
conectividad IPv6, la base queda inalcanzable aunque IPv4 ande bien (pasó una vez, 2026-09-04) --
`ip -6 addr show scope global` lo diagnostica en un segundo. Por eso los seeds se escriben
idempotentes (`on conflict do update`) e incluyen el marcado de sus colas: si un apply falla, se
re-corre entero sin efectos secundarios.

**Hueco de alcance descubierto (2026-09-04):** `enqueue_card_review_queue.py` filtra
`cat != "Project"`, así que tres categorías enteras del índice del sitio nunca entraron al
pipeline: **Prelude (70)**, **Corporation (48)** y **Automa (78)**. Las Prelude ya tienen su
tabla, su cola y su tool (`play_prelude`) -- ver "Prelude: mazo propio" en `CARDS_LOG.md`. Las
**corporaciones son el próximo hueco grande** y todavía no están modeladas en ningún lado (varias
cartas ya cargadas las mencionan).

**Mecánica pendiente con 3 cartas esperándola:** "jugar otra carta de la mano como parte de este
efecto" -- Ecology Experts (P10), Eccentric Sponsor (P11) y WG Project (P91). El FAQ ya tiene las
reglas exactas documentadas en `CARDS_LOG.md`.

**Aprendizajes de las tandas multi-agente (aplicar en las próximas):**
- Los agentes confunden el recuadro de **requisito** (arriba a la izquierda, junto al costo) con
  los **tags propios** (arriba a la derecha). El prompt debe explicitarlo y pedir requisito, tags
  e `is_event` **por separado** -- ya está incorporado, y con eso la segunda tanda tuvo muchos
  menos errores.
- También confunden los **puntos de victoria** (disco marrón abajo a la derecha) con TR. Un
  agente propuso `tr_delta: 2` para una carta cuyo único beneficio son 2 VP, que este motor no
  modela.
- Los agentes inventan nombres de campos del vocabulario (`megacredits` en vez de `mc`,
  contadores que no existen). Conviene pedirles que citen el docstring exacto de donde sacan cada
  clave, y mapear a mano al integrar.
- **Verificar siempre los tags contra los scans antes de cargar.** Es barato y atrapó ~8 errores
  entre las dos tandas.

**Turmoil: Global Events, COMPLETO (2026-09-04).** Mazo APARTE de 36 cartas, catalogado en el
índice del sitio (`hadronikle`, categoría `"GlobalEvent"`) en tabla propia `global_events` +
cola `global_event_review_queue`. Reusan `rules_engine.apply_card_effect` (mismo `effects`
jsonb que las cartas). Tool: `resolve_global_event(player_id, event_id, target_card_id=None,
effect_choice=None, discard_card_ids=None, remove_ocean_hex_id=None)`. **36 de 36 cargadas, 0
pendientes.** Los bloques 5 y 6 se hicieron con **orquestación multi-agente** (agentes Sonnet en
paralelo que analizan/diseñan sin tocar el repo; integración, verificación y código
centralizados) -- ver "Turmoil: Global Events" en `CARDS_LOG.md` para el detalle por agente.

**Fuente nueva de alto valor: el Comprehensive FAQ v1.7** (compilado por Jeffrey Anchan, con
fuentes citadas por entrada; PDF en tesera.ru, legible con `pypdf`). Tiene una tabla
"Global Event Clarifications" con errata y aclaraciones oficiales. Leerla destapó **4 bugs en
cartas ya cargadas** (Aquifer Released otorgaba TR y no debe; Jovian Tax Rights tenía errata
"(max 5)"; Snow Cover bajaba temperatura ya maximizada; Diversity contaba el tag "wild", que no
cuenta en Global Events). **Conviene consultarla antes de cargar cartas de cualquier expansión**,
no solo Turmoil -- también trae aclaraciones de Colonies y Prelude.

**Turmoil: núcleo político, implementado (2026-09-04, decisión explícita del usuario).**
Resolvió las últimas 2 cartas pendientes del catálogo normal: Colonial Envoys y Colonial
Representation (P70/P71, Prelude 2). Módulo nuevo `backend/app/agent/turmoil.py` (mismo estilo
que `colonies.py`), verificado contra el rulebook oficial (TM_TURMOIL_ENG_RULES.pdf, 8 páginas,
leído completo): 6 partidos, delegados (7 por jugador: 1 Lobby + 6 Reserva), acción Lobbying,
Party Leader/partido Dominante (se actualiza al instante), requisitos `ruling_or_delegates`
(Ruling O 2+ delegados propios), Influencia (Chairman/líder del Dominante/delegado no-líder ahí,
+1 cada uno, +bonus de carta), "New Government" (ACOTADO a un solo jugador, modo un jugador de
este proyecto). Campos nuevos en `PlayerState`: `lobby_delegates`, `reserve_delegates`; estado
compartido nuevo: `turmoil` en `GlobalParameters`. Tools nuevas: `lobby`, `resolve_new_government`,
`get_turmoil_state`. **Quedan explícitamente pendientes**, cada uno del tamaño de una feature
aparte: las Ruling Bonus/Ruling Policy de los 6 partidos (12 efectos), y la revisión de TR (-1 a
todos cada generación) -- ver sección dedicada "Turmoil: núcleo político" en `CARDS_LOG.md`.
Tests: `test_turmoil.py`.

**Tag comodín "wild", implementado (2026-09-04).** Resolvió Research Coordination (P40,
Prelude) -- pendiente desde el bloque 30. El texto impreso ("the wild tag counts as any tag of
your choice when performing an action") se acotó al único lugar del catálogo cargado donde tiene
sentido real: `check_card_requirements` → `min_tag_count` (requisito para JUGAR otra carta, ej.
Mass Converter: 5 tags de ciencia). No hace falta campo nuevo ni pasivo registrado -- basta con
que la carta tenga tag `"wild"` (`tags_played` ya lo cuenta solo). Pieza nueva: parámetro
`wild_tag_choice` en `check_card_requirements`/`tools.play_card` -- si coincide con el tag del
requisito, suma los tags "wild" en juego a ese conteo para ese chequeo puntual (no altera
`tags_played`, se re-declara cada vez). Ver sección dedicada "Tag comodín 'wild'" en
`CARDS_LOG.md`.

**Pago con recurso de carta, implementado (2026-09-04).** Resolvió Dirigibles (222, Venus Next)
y Psychrophiles (P39, Prelude) -- pendientes desde los bloques 20-30. Pieza nueva `passive:
card_resource_payment` ({"required_tag", "value_mc"}) en `register_passive_effect`: un recurso
guardado en una carta activa (floaters, microbios) paga cartas de un tag específico, a N M€ cada
uno -- tercera moneda de pago cuyo stock vive en una carta, no en el jugador. `tools.play_card`
suma el parámetro `card_resource_to_pay`, resuelve solo (por tag) qué carta activa habilita el
pago; `rules_engine.spend_active_card_resource` descuenta el recurso. `use_card_action` suma
`target_card_resource_delta_allow_self` (Dirigibles: "add floater to ANY card", incluida ella
misma). Ver sección dedicada "Pago con recurso de carta" en `CARDS_LOG.md`.

**Bloque 30 (2026-09-03):** 6 de 10 cargadas — Lava Tube Settlement, Martian Survey, SF
Memorial, Space Hotels (Prelude), Ceres Tech Market, Cloud Tourism (Venus Next promo). Piezas de
motor nuevas: `board.can_place_city_on_volcanic` + flag `city_placement_on_volcanic` (Lava Tube
Settlement), `mc_per_discarded_card` en `use_card_action`, `resource_delta_per_colony` (análogo
stock de `production_delta_per_colony`), `production_delta_per_tag_pair` (usa el mínimo de dos
conteos de tags) — las 3 últimas en Ceres Tech Market/Cloud Tourism. Ver detalle en
`CARDS_LOG.md`.

**Decisión de alcance (2026-09-02/03):** primero entró **Venus Next** (bloque 20 completo era
de esa expansión, ver sección 7). El bloque 25 trajo la primera tanda de **Colonies** -- el
usuario confirmó seguir cargando cartas de cualquier expansión que aparezca sin preguntar cada
vez, así que Colonies también entró, **incluida su mecánica central** (el usuario pidió
implementarla explícitamente después de ver el bloque 25). El bloque 29 cerró Colonies
(llegó a C49, el último) y trajo la primera carta de **Prelude** -- esa expansión NO necesita
mecánica propia (ver sección 7), así que sigue el mismo flujo de siempre sin nada especial que
construir. Si aparece una expansión que sí necesite mecánica grande nueva, la misma pregunta
aplica: cargar lo que se pueda con vocabulario existente, diagnosticar y posponer el resto.

**Verificación contra el rulebook oficial (2026-09-02):** se releyó el reglamento completo
(fryxgames/Stronghold Games, 16 páginas) y se cruzó contra el motor -- sin discrepancias
encontradas. Se documentó una decisión ya implícita: el modo "un jugador" de este proyecto es
una partida ESTÁNDAR (TR 20), no la variante solitario oficial del reglamento (TR 14, 14
generaciones fijas, ciudades neutrales) -- ver sección 7 más abajo.

**Colonies: mecánica de colonias/comercio, implementada (2026-09-03).** Módulo nuevo
`backend/app/agent/colonies.py` (mismo estilo que `board.py`), verificado contra el rulebook
oficial de la expansión (TM_COLONIES_ENG_RULES, leído completo): proyecto estándar
`build_colony` (17 MC), acción `use_trade_fleet` (9 MC/3 energía/3 titanio a elección), trade
income + colony bonus, reset de track, paso de producción de colonias en la fase solar,
`adjust_colony_track` (sube/baja un track directo, ej. Market Manipulation). Tools nuevas:
`setup_colonies`, `build_colony`, `use_trade_fleet`. Efectos de carta nuevos en `play_card`
(mismo patrón que `place_special_tile`, resueltos en `tools.py` no en `rules_engine.py`):
`build_colony` (construir sin pagar los 17 MC aparte, o con `{"allow_duplicate": true}` para
cartas que ignoran la restricción de 1 colonia por jugador por tile -- Research Colony, Space
Port Colony), `adjust_colony_tracks`, `gain_all_colony_bonuses`, `mc_per_colony_in_play`,
`production_delta_per_colony_in_play`. Requirements nuevos: `min_colonies_owned`/`max_colonies_owned`.
También `free_trade` (bloque 29, resuelto 2026-09-03) en el vocabulario de `gains` de
`use_card_action` -- a diferencia de las demás piezas de colonias, `rules_engine.py` NO lo
procesa (se mantiene sin depender de `colonies.py`, ver sección 3 más abajo): `tools.use_card_action`
lo detecta antes de llamar al motor y, después de que este cobre el costo declarado de la
acción, llama `colonies.trade_with_colony` directo sin cobrar el costo normal de comerciar ni
gastar flota (parámetro nuevo `trade_colony_id`) -- desbloqueó Titan Floating Launch-Pad, la
última carta pendiente de Colonies. Solo **Callisto** cargada en `COLONY_DEFS` (verificada con
dos fuentes independientes) -- las
otras 10 colonias reales del juego quedan sin cargar hasta verificarlas igual que el catálogo
de cartas; el mecanismo ya es genérico, agregar una colonia nueva es solo datos, no código. Ver
detalle completo en `CARDS_LOG.md`, sección "Colonies: mecánica de colonias/comercio". Tests:
`test_colonies.py`.

**Bloques 21-29, 86 de 90 cargadas** (4 pendientes, ver abajo). Piezas de motor nuevas
agregadas a lo largo de los nueve bloques, todas extensiones chicas de vocabulario existente:
- `production_delta_per_tag` acepta una LISTA de specs (Gyropolis, bloque 21).
- `target_card_resource_delta_per_tag` (Hydrogen to Venus, bloque 21).
- `min_tag_count` en lista de 3+ tags distintos, patrón reusado sin cambios en motor (bloques
  22-29).
- `mc_or_titanium` en el `cost` de `use_card_action` -- el titanio puede cubrir parte/todo un
  costo de acción en MC, igual que al pagar cartas (Rotator Impacts, bloque 23; nuevo parámetro
  `titanium_to_pay`).
- `convert_card_resource_amount` en `use_card_action` -- como `convert_resource_amount` pero el
  origen es el recurso guardado en la propia carta (Sulphur-Eating Bacteria, bloque 23).
- `discard_card_then_draw` en `apply_card_effect` -- descarta 1 carta elegida (parámetro nuevo
  `discard_card_id`, distinto de `discard_for_draw_card_id` que ya existía para el pasivo de
  Mars University) y roba N (Sponsored Academies, bloque 23).
- `min_tr` en `check_card_requirements` -- TR mínimo del jugador (Terraforming Contract,
  bloque 24).
- `zero_tag_cards_played` (campo nuevo en `PlayerState`) + `production_delta_per_zero_tag_card`
  -- cuenta cartas jugadas sin ningún tag, para producción escalada por esa cuenta (Community
  Services, bloque 25, primera carta Colonies cargada).
- `colonies_owned`/`trade_fleets`/`trade_fleets_used` (campos nuevos) + `production_delta_per_colony`
  + pasivo `trade_cost_discount` + `mc_per_card_resource` (gana MC por recurso guardado en la
  carta SIN gastarlo, con tope opcional) + `trade_fleet_delta` + `draw_cards_per_tag` + pasivo
  `trade_bump_track_first` (bloque 29: sube el track de una colonia 1 paso antes de comerciar,
  parámetro nuevo `bump_track_first` en `tools.use_trade_fleet`) + pasivo
  `on_card_played_cost_threshold_draw` (bloque 29: roba cartas al jugar una carta cuyo costo
  IMPRESO supere un umbral, chequeado en `tools.play_card` porque necesita el costo de catálogo)
  -- ver mecánica de colonias arriba (bloques 25-29).

**Flujo de ramas:** cada bloque de revisión vive en su propia rama `feat/review-block-N`,
creada a partir de `main` una vez que el bloque anterior ya se mergeó, o de la rama del bloque
anterior si todavía no se mergeó. Commiteada y pusheada a `origin` individualmente.

**Cartas pendientes identificadas (`CARDS_LOG.md`, sección "Pendientes"):** ninguna por ahora --
la última (suma de floaters entre cartas activas) se resolvió 2026-09-04, ver "Recursos tipados
por carta activa" arriba. Quedan las 28 filas sin revisar de `global_event_review_queue` (no son
"pendientes por mecánica", son bloques de Global Events todavía sin leer) y, en Air Raid (#C02,
Colonies), la única exclusión permanente por diseño (robo obligatorio sin sentido en
single-player, ver "Fuera de alcance" en `CARDS_LOG.md`).

**Para retomar: la cola de cartas de proyecto está VACÍA**, así que el flujo de "revisar un
bloque de 10" ya no aplica. Lo que queda, en orden de valor:

1. ~~Auditoría de tags `power`/`space`~~ — **hecha el 2026-09-08** (ver arriba).
2. ~~Las 10 colonias faltantes~~ — **9 de 11 cargadas el 2026-09-08** (ver `CARDS_LOG.md`).
   Quedan Pluto y Europa, que no entran en el modelo actual de `ColonyDef`.
3. **Corporaciones: seguir la cola** (38 sin revisar, bloques de 10 con subagentes Sonnet).
4. ~~Los 22 preludes pendientes~~ — **4 cargados el 2026-09-08** (ver arriba). Los 18 que
   quedan sí necesitan mecánicas grandes (sub-mazo de Prelude, hook genérico "subió el TR",
   corporaciones). Siguen pendientes también las 3 cartas dudosas de proyecto
   (`self_replicating_robots`, `venus_orbital_survey`, `wg_project`).
5. **T11 Recruitment**, la única fila que queda en "Pendientes" de `CARDS_LOG.md` (delegados
   neutrales por partido en Turmoil).
6. El **frontend**, todavía 100% mockeado.
7. Las piezas de Turmoil pospuestas: Ruling Bonus/Policy de los 6 partidos y la revisión de TR.

El flujo de trabajo, si vuelve a haber cartas para revisar: consultar la cola en Supabase
(conexión directa con `psycopg2` y parámetros individuales de host/user/password — el
`SUPABASE_DB_URL` de `.env` tiene un `@` dentro de la password que rompe el parseo de
`psycopg2.connect(url)` con un solo string), descargar los scans espaciados 3s, leer cada uno,
decidir vocabulario (extender el motor si hace falta), cargar en `seed_cards.sql` + tests,
probar contra Supabase real, marcar `card_review_queue`, actualizar `CARDS_LOG.md`, commitear.

## 5. Stack tecnológico

| Capa | Tecnología | Notas |
|---|---|---|
| Orquestación de IA | Python + LangGraph | `StateGraph` con tool-calling explícito |
| Backend API | FastAPI | Expone `/chat` y `/state/{player_id}` |
| Base de datos | Supabase (Postgres) | Estado del juego, catálogo, cola de revisión, transacciones |
| Frontend | Next.js (App Router) + TypeScript + Tailwind | Desplegado en Vercel |
| Infraestructura | Docker (solo backend) | El frontend corre vía `npm run dev` / Vercel, no se containeriza |

Modelo LLM sugerido: Claude (vía `langchain-anthropic` o API directa), como variable de entorno
para no acoplar el código a un proveedor específico.

**Nota de dependencia:** `supabase` debe estar en `>=2.8.0` — versiones viejas (`2.7.4`)
rechazan el formato nuevo de API keys de Supabase (`sb_publishable_.../sb_secret_...`) por
validar con una regex que exige forma de JWT.

## 6. Estructura del repo

```
arbiter-mars/
├── AGENTS.md / CLAUDE.md
├── backend/
│   ├── app/
│   │   ├── main.py            # Entry point FastAPI, CORS, incluye routers
│   │   ├── config.py          # Settings vía pydantic-settings (.env, extra="ignore")
│   │   ├── agent/
│   │   │   ├── state.py       # TypedDict del estado del grafo
│   │   │   ├── rules_engine.py # Motor de reglas puro (ver seccion 3)
│   │   │   ├── board.py       # Mapa hexagonal Tharsis, funciones puras (ver seccion 3)
│   │   │   ├── tools.py       # Wrappers @tool: cargan/guardan estado en Supabase
│   │   │   ├── prompts.py     # System prompt del nodo LLM
│   │   │   └── graph.py       # Definición del StateGraph (LLM -> ToolNode -> respuesta)
│   │   ├── db/
│   │   │   ├── supabase_client.py
│   │   │   ├── schema.sql             # DDL completo
│   │   │   ├── seed_cards.sql         # Catálogo de cartas cargadas hasta ahora
│   │   │   ├── CARDS_LOG.md           # Registro de cartas cargadas/pendientes/fuera de alcance
│   │   │   ├── CARDS_PENDING_REVIEW.md # DEPRECADO -- ver card_review_queue en Supabase
│   │   │   └── HEX_MAP_RESEARCH.md    # Investigación del mapa hexagonal (fuentes, layout, diseño)
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic: request/response de la API
│   │   └── api/
│   │       └── routes.py      # POST /chat, GET /state/{player_id}
│   ├── scripts/                # Herramientas de mantenimiento (no parte de la app en runtime)
│   │   ├── enqueue_card_review_queue.py
│   │   ├── download_review_scans.py
│   │   ├── mark_reviewed.py
│   │   └── scan_cache/          # gitignored, imagenes temporales de trabajo
│   ├── tests/
│   │   ├── test_rules_engine.py
│   │   └── test_board.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── app/ (layout.tsx, page.tsx, globals.css)
    ├── components/ (Dashboard.tsx, SidebarChat.tsx, ResourcePanel.tsx)
    ├── lib/api.ts
    └── package.json
```

## 7. Alcance (no expandir sin decidirlo explícitamente)

**Dentro de alcance:** interfaz conversacional en sidebar, dashboard de estado del jugador,
enrutamiento a herramientas para cálculos de redención, memoria persistente del estado de la
sesión actual, el mapa hexagonal Tharsis completo (ver sección 3), la expansión **Venus Next**
(decisión explícita del usuario, 2026-09-02): 4to parámetro global Venus scale (0% a 30%, pasos
de 2%, bonus de umbral verificados contra el rulebook oficial de FryxGames -- ver
`raise_venus`/`VENUS_BONUS_STEP_*` en `rules_engine.py`), proyecto estándar nuevo `air_scrapping`
(15 MC, +1 paso de Venus), requirements `min_venus`/`max_venus`, efecto `raise_venus_steps`. El
recurso "floater" de la expansión NO necesita campo nuevo -- se guarda en `active_cards` igual
que microbios/animales (mismo mecanismo, solo cambia el nombre del recurso en el efecto de la
carta). El tag "venus" tampoco necesita nada nuevo -- los tags ya son genéricos. Las 4 áreas de
ciudad fuera de tablero de Venus Next (Maxwell Base, Stratopolis, Luna Metropolis, Dawn City)
reusan el mecanismo genérico existente de `place_city_tiles` (contador global, sin mapa -- mismo
patrón que Phobos Space Haven/Research Outpost). También la expansión **Colonies** (decisión
del usuario, 2026-09-03: cargar cartas de cualquier expansión que aparezca en la cola), incluida
su mecánica central de colonias/comercio (`backend/app/agent/colonies.py`, verificada contra el
rulebook oficial: construir colonia 17 MC, comerciar 9 MC/3 energía/3 titanio, trade income +
colony bonus, reset de track, paso de producción de colonias en la fase solar) -- ver
"Colonies: mecánica de colonias/comercio" en `CARDS_LOG.md`. Solo **Callisto** está cargada en
`COLONY_DEFS` por ahora (verificada con dos fuentes independientes); las otras 10 colonias
reales del juego quedan sin cargar hasta verificarlas de la misma forma que el catálogo de
cartas -- el mecanismo ya es genérico, agregar una colonia nueva es solo agregar datos
verificados a `COLONY_DEFS`, no tocar código. Colonies terminó de revisarse en el bloque 29
(cierre C01-C49). También la expansión **Prelude** (primera carta bloque 29, House Printing) --
a diferencia de Venus Next/Colonies, Prelude NO necesita mecánica propia nueva: son ~24 cartas
con efecto inmediato simple que en el juego real se reparten 2 gratis en el setup (ese sorteo/
elección de setup no está modelado todavía, no bloquea cargar las cartas individuales). También
el **núcleo político de Turmoil** (decisión explícita del usuario, 2026-09-04):
`backend/app/agent/turmoil.py`, verificado contra el rulebook oficial -- 6 partidos, delegados,
acción Lobbying, Party Leader/partido Dominante, requisitos `ruling_or_delegates`, Influencia,
"New Government" (acotado a un solo jugador) -- ver "Turmoil: núcleo político" en `CARDS_LOG.md`.
**Explícitamente FUERA de esta primera pasada** (cada uno del tamaño de una feature aparte, no
decidido todavía si se construyen): las Ruling Bonus/Ruling Policy de los 6 partidos, el mazo de
31 Global Event cards, y la revisión de TR (-1 a todos cada generación).

**Fuera de alcance (MVP):** una IA que juegue de forma autónoma contra humanos, soporte para
múltiples juegos simultáneos, milestones y awards (incluidos los nuevos de Venus Next: Hoverlord
milestone, Venuphile award), mapas alternativos (Hellas/Elysium), la mecánica de pago cruzado de
la expansión Ares, el catálogo completo hardcodeado de special tiles de cartas
(`place_special_tile` es genérica a propósito), y la **Solar Phase** de Venus Next (fase
automática post-producción donde el "World Government" sube un parámetro global elegido por el
jugador que actúa como primer jugador) -- automatización de fin de generación, no una mecánica
de carta; se evalúa aparte si hace falta.

**Nota sobre el modo "un jugador" (verificado 2026-09-02 contra el rulebook oficial):** el
reglamento define una **variante en solitario** distinta a como juega este proyecto -- esa
variante arranca con TR 14 (no 20), juega exactamente 14 generaciones fijas, y usa 2 ciudades
neutrales que el jugador puede robar/reducir. Este proyecto NO implementa esa variante --
`TR_START = 20` (`rules_engine.py`) trata el modo de un jugador como una partida ESTÁNDAR
normal, sin oponente neutral ni límite fijo de generaciones. Decisión ya implícita en el motor
existente, dejada explícita acá para que quede claro que es intencional, no un olvido.

## 8. Comandos de desarrollo

```bash
# Backend (containerizado)
cd backend
cp .env.example .env          # completar SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY
docker build -t arbitro-backend .
docker run --env-file .env -p 8000:8000 arbitro-backend

# o local sin Docker, para iterar rápido (venv con Python 3.12+, ver nota de dependencia arriba)
pip install -r requirements.txt
uvicorn app.main:app --reload

# Tests (el criterio de éxito del PRD es 100% de precisión en cálculos)
cd backend && PYTHONPATH=. pytest tests/ -v

# Aplicar/actualizar schema + catálogo en Supabase real (necesita SUPABASE_DB_URL, connection
# string de Postgres -- distinto de SUPABASE_URL/KEY que usa la app)
python3 -c "
import psycopg2
conn = psycopg2.connect('TU_SUPABASE_DB_URL', sslmode='require'); conn.autocommit = True
cur = conn.cursor()
cur.execute(open('app/db/schema.sql').read())
cur.execute(open('app/db/seed_cards.sql').read())
"

# Scripts de mantenimiento del catálogo (ver seccion 4)
python3 scripts/enqueue_card_review_queue.py --pending-md app/db/CARDS_PENDING_REVIEW.md --cards-json <index.html cacheado> --db-url "$SUPABASE_DB_URL"
python3 scripts/download_review_scans.py --out-dir scripts/scan_cache --db-url "$SUPABASE_DB_URL"
python3 scripts/mark_reviewed.py --scan-number 116 --card-id artificial_lake --db-url "$SUPABASE_DB_URL"

# Frontend
cd frontend
cp .env.example .env.local    # NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

## 9. Modelo de datos (Supabase)

Ver `backend/app/db/schema.sql`. Tablas:
- `players`: recursos + producción + TR por jugador, `deck`/`hand`/`pending_research`
  (sistema de mazo), `active_cards` (acciones repetibles), `tags_played`, `passive_effects`,
  `played_cards` (historial permanente), `pending_mc_discount`/`pending_requirement_tolerance_steps`
  (descuentos/tolerancias de un solo uso para la PRÓXIMA carta jugada, ver sección 3).
  Migraciones de columnas nuevas van al bloque `do $$ begin alter table if exists players add
  column if not exists ... exception when undefined_table then null; end $$;` al principio de
  `schema.sql` (idempotente, no rompe si la tabla no existe todavía) — correr `schema.sql`
  contra Supabase real de nuevo después de agregar una columna.
- `global_parameters`: temperatura/oxígeno/océanos/ciudades colocadas/`events_played` (contador
  histórico de eventos jugados), `board` (jsonb con el estado mutable del mapa hexagonal —
  compartido, fila única `game_id='default'` para el MVP).
- `cards`: catálogo de cartas (id, name, cost, tags, requirements, effects, is_event).
- `card_review_queue`: cola de revisión del catálogo (ver sección 4) — reemplaza el manifiesto
  markdown viejo.
- `global_events`: catálogo de Global Event cards de la expansión Turmoil (id, name, effects —
  mismo `effects` jsonb que `cards`, sin costo/tags/requirements). Ver
  `backend/app/agent/turmoil.py` y "Turmoil: Global Events" en `CARDS_LOG.md`.
- `global_event_review_queue`: cola de revisión de Global Events, mismo patrón que
  `card_review_queue` pero sin `scan_number` (el nombre es la clave única).
- `transactions`: log de cada jugada resuelta, para auditar.

## 10. Convenciones

- Python: type hints en todo, `pydantic` para validación de I/O, funciones puras sin efectos
  secundarios ocultos (reciben estado, devuelven estado nuevo + resultado) en `rules_engine.py`
  y `board.py`; `tools.py` es la única capa con I/O (Supabase).
- Commits: mensajes en imperativo, en español.
- No commitear `.env` (solo `.env.example`) ni las imágenes de scans (`scripts/scan_cache/`,
  derechos de autor de FryxGames).
- Cualquier función que "calcule" algo debe tener un test que verifique el número exacto, no
  solo que "no explote". Cada extensión nueva del vocabulario de `effects`/`requirements` se
  documenta en `CARDS_LOG.md` con un ejemplo real de qué carta la necesitó.
- Antes de descargar scans nuevos: espaciar los pedidos (2.5s), nunca en paralelo ni en ráfaga.
- Cada bloque de revisión de cartas va en su propia rama `feat/review-block-N`, ramificada desde
  el bloque anterior (no desde `main`) y pusheada a `origin` al terminar — ver "Punto de retoma"
  en la sección 4.
- La password de `SUPABASE_DB_URL` (en `.env`) contiene un `@` — `psycopg2.connect(url)` con el
  string completo falla el parseo. Conectar con parámetros individuales
  (`host`/`port`/`dbname`/`user`/`password`) en vez de pasar la URL entera.
