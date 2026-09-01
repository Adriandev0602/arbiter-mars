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
  océanos (0 a 9 tiles, con 12 hexágonos reservados donde colocarlos — ver sección 4), con
  clamping correcto al tope y sin otorgar TR por pasos no aplicados.
- Los 6 proyectos estándar con sus costos reales (sell_patents, power_plant, asteroid, aquifer,
  greenery, city).
- Conversiones del tablero de jugador (8 plantas → greenery, 8 calor → +1 paso de temperatura).
- Fase de producción completa, pago de cartas con acero/titanio sin reembolso por sobrepago.
- Sistema de mazo/mano/investigación (`deck`/`hand`/`pending_research`), tags jugados, efectos
  pasivos permanentes, historial de cartas jugadas (`played_cards`).
- Vocabulario extensible de `effects` en `apply_card_effect` (production_deltas, resource_deltas,
  choice, tag_count_choice, production_delta_per_tag, resource_delta_per_counter, draw_cards,
  start_research, duplicate_production, etc.) y de `requirements` en `check_card_requirements`
  (min/max_temperature, min/max_oxygen, min/max_oceans, min_tag_count, min_production). Ver el
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
sesión actual, el mapa hexagonal Tharsis completo (ver sección 3).

**Fuera de alcance (MVP):** una IA que juegue de forma autónoma contra humanos, soporte para
múltiples juegos simultáneos, milestones y awards, mapas alternativos (Hellas/Elysium), la
mecánica de pago cruzado de la expansión Ares, y el catálogo completo hardcodeado de special
tiles de cartas (`place_special_tile` es genérica a propósito).

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
  `played_cards` (historial permanente, ver sección 3).
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
