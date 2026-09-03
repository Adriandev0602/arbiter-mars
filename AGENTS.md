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

### 📍 Punto de retoma (última sesión: 2026-09-03, bloques 12→22 + Venus Next + Lava Flows)

**Progreso:** catálogo en **231 cartas** cargadas en `cards`. `main` tiene mergeados los
bloques 13-20 y Lava Flows (140). `card_review_queue` tiene 121 filas `reviewed = true` y
**181 sin revisar** — el próximo bloque (23) son las filas #1-10 de `select * from
card_review_queue where reviewed = false order by id limit 10`.

**Decisión de alcance (2026-09-02):** la expansión **Venus Next** entró al alcance del proyecto
porque el bloque 20 completo resultó ser de esa expansión (ver sección 7). Motor extendido con
4to parámetro global `venus` + proyecto estándar `air_scrapping` — ver sección 3. Los bloques 21
y 22 también resultaron íntegramente Venus Next (181 filas sin revisar todavía, mayoría probable
de la misma expansión) -- si los próximos bloques siguen trayendo cartas de OTRAS expansiones
nuevas (Colonies, Prelude, Ares), la misma pregunta aplica: confirmar con el usuario antes de
asumir que entran al alcance.

**Verificación contra el rulebook oficial (2026-09-02):** se releyó el reglamento completo
(fryxgames/Stronghold Games, 16 páginas) y se cruzó contra el motor -- sin discrepancias
encontradas (proyectos estándar, colocación de tiles, bonus de adyacencia oceánica, fase de
investigación, todo coincide). Se documentó una decisión ya implícita: el modo "un jugador" de
este proyecto es una partida ESTÁNDAR (TR 20), no la variante solitario oficial del reglamento
(TR 14, 14 generaciones fijas, ciudades neutrales) -- ver sección 7 más abajo.

**Bloque 21 (Venus Next):** 9 de 10 cargadas -- Extractor Balloons, Extremophiles, Floating
Habs, Forced Precipitation, Freyja Biodomes, GHG Import from Venus, Giant Solar Shade,
Gyropolis, Hydrogen to Venus. Dos piezas de motor nuevas (ambas extensiones chicas de
vocabulario existente, no mecánica nueva): `production_delta_per_tag` ahora acepta una LISTA de
specs (antes solo un dict, ver Gyropolis) y `target_card_resource_delta_per_tag` (combina
target_card_resource_delta con production_delta_per_tag, ver Hydrogen to Venus).

**Bloque 22 (Venus Next): las 10 cargadas**, sin pieza de motor nueva -- IO Sulphur Research
(`tag_count_choice`), Ishtar Mining, Jet Stream Microscrappers, Local Shading, Luna Metropolis
(`production_delta_per_tag` con `include_this`), Luxury Foods (solo requirement, sin efecto
numérico), Maxwell Base, Mining Quota, Neutralizer Factory, Omnicourt (todas con
`min_tag_count` en lista de 3 tags, patrón ya usado en Advanced Ecosystems).

**Flujo de ramas:** cada bloque de revisión vive en su propia rama `feat/review-block-N`,
creada a partir de `main` una vez que el bloque anterior ya se mergeó, o de la rama del bloque
anterior si todavía no se mergeó (bloque 22 ramificado de `feat/review-block-21`, que sigue sin
mergear). Commiteada y pusheada a `origin` individualmente.

**Cartas pendientes identificadas (`CARDS_LOG.md`, sección "Pendientes"), cada una con su
pieza de mecánica ya diagnosticada pero no implementada:**
- **Aerosport Tournament** (214, Venus Next): requisito "tener 5 floaters" — suma de un recurso
  de un tipo específico a través de TODAS las cartas activas del jugador, no solo una carta
  puntual. `active_cards[card_id]["resources"]` no distingue tipo de recurso hoy (microbio,
  animal o floater son el mismo contador sin etiqueta) — necesita esa etiqueta por carta más un
  requirement nuevo (`min_total_card_resources`) que sume sobre las que matcheen.
- **Dirigibles** (222, Venus Next): pasivo "floaters guardados en ESTA carta valen 3 M€ cada
  uno al pagar cartas con tag Venus" -- una TERCERA moneda de pago (como acero/titanio) cuyo
  stock vive en una carta activa, no en el jugador. Necesita parámetro nuevo en `tools.play_card`
  (`floater_card_id` + cantidad) y extender el cálculo de pago. Misma categoría que
  Self-Replicating Robots (mecánica de pago no trivial) -- pospuesta para abordarla con foco
  dedicado, no forzada en un bloque de revisión normal. Es probable que se repita en más cartas
  Venus Next -- verificar cuando aparezcan antes de diseñar la pieza definitiva.

**Para retomar:** mismo flujo que bloques anteriores: `git checkout main && git pull && git
checkout -b feat/review-block-22`, consultar
la cola en Supabase (conexión directa con `psycopg2` y parámetros individuales de
host/user/password — el `SUPABASE_DB_URL` de `.env` tiene un `@` dentro de la password que
rompe el parseo de `psycopg2.connect(url)` con un solo string), descargar los 10 scans
espaciados 4s, leer cada uno, decidir vocabulario (extender el motor si hace falta), cargar en
`seed_cards.sql` + tests en `test_rules_engine.py`/`test_board.py`, probar contra Supabase real,
marcar `card_review_queue` con `card_id` (o `null` si queda pendiente/fuera de alcance),
actualizar `CARDS_LOG.md`, commitear, pushear la rama.

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
patrón que Phobos Space Haven/Research Outpost).

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
