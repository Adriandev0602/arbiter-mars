# CLAUDE.md

Este archivo le da contexto a Claude Code sobre este repositorio. Léelo por completo antes de tocar código.

## 1. Qué es este proyecto

**Árbitro Asistente de Reglas para Terraforming Mars**: un agente de IA que resuelve cálculos de turnos
(fase de producción, proyectos estándar, subida de parámetros globales) y valida el pago de cartas de
proyecto. El usuario escribe una consulta en lenguaje natural ("quiero usar el proyecto estándar Ciudad",
"cerrá mi fase de producción", "quiero jugar la carta X pagando 4 MC y 3 de acero") y el sistema responde
con un veredicto y el estado actualizado, calculado por Python puro, nunca por el LLM.

Este es un proyecto de práctica/portfolio para demostrar habilidades de ML/AI Engineering — el objetivo
no es "un chatbot más", sino demostrar **control arquitectónico estricto sobre un LLM probabilístico**.

## 2. Principio arquitectónico no-negociable

> **El LLM nunca hace matemática. Nunca.**

El LLM tiene exactamente un trabajo: parsear la intención del usuario y extraer argumentos estructurados
(`{"card_id": "X", "qty_titanio": 5, "qty_acero": 2}`). Todo cálculo de saldo, validación de reglas de
redención y comparación contra el estado del juego se hace en **funciones Python puras y deterministas**
(`backend/app/agent/tools.py`), nunca en el texto generado por el modelo.

Esto se aplica en dos capas:
1. **System prompt** (`backend/app/agent/prompts.py`): le prohíbe explícitamente al modelo responder con
   números calculados por él mismo; su única salida legítima es una tool call o una respuesta que repite
   literalmente el resultado que le devolvió la tool.
2. **Grafo determinista** (`backend/app/agent/graph.py`): el `StateGraph` de LangGraph enruta *siempre*
   por el `ToolNode` antes de generar la respuesta final — no hay camino donde el LLM responda directo
   sin pasar por herramientas cuando la consulta implica un cálculo.

Cuando itero features en este repo, cualquier cambio que le dé al LLM la posibilidad de "adivinar" un
número es un bug de arquitectura, no una mejora de UX.

## 3. El motor de reglas (`backend/app/agent/rules_engine.py`)

Esta es la pieza central del repo: funciones Python puras, sin dependencias de LangGraph/FastAPI/Supabase,
100% testeadas contra números verificados del reglamento oficial. `tools.py` es solo un wrapper delgado
que carga/guarda estado en Supabase y llama estas funciones.

**Implementado y testeado (30 tests en `backend/tests/test_rules_engine.py`):**
- Terraform Rating: arranca en 20, +1 por cada paso de parámetro global subido.
- Parámetros globales: temperatura (-30 a +8, pasos de 2°C), oxígeno (0 a 14%, pasos de 1%),
  océanos (0 a 9 tiles) — con clamping correcto al tope y sin otorgar TR por pasos no aplicados.
- Los 6 proyectos estándar con sus costos reales: Sell Patents (gratis, 1 MC/carta descartada),
  Power Plant (11 MC → +1 producción de energía), Asteroid (14 MC → +1 paso de temperatura),
  Aquifer (18 MC → coloca océano), Greenery (23 MC → +1 paso de oxígeno), City (25 MC → +1
  producción de MC).
- Conversiones del tablero de jugador: 8 plantas → greenery (sube oxígeno), 8 calor → +1 paso de
  temperatura.
- Fase de producción completa: energía sobrante se convierte en calor, MC ganado = TR + producción
  de MC (con piso en 0, nunca negativo en stock), resto de recursos suman su producción.
- Pago de cartas con acero (2 MC/unidad, solo tag `building`) y titanio (3 MC/unidad, solo tag `space`),
  sin reembolso por sobrepago (regla oficial).

**Catálogo de cartas — en progreso:** la tabla `cards` arranca vacía en `schema.sql`. Terraforming Mars
tiene ~200 cartas de proyecto y no se generaron datos al voleo (un número mal recordado rompe el "100% de
precisión" del PRD) — se cargan a mano, carta por carta, verificadas contra el scan oficial de cada una
(fuente usada: la base de datos de cartas de tm.hadronikle.com).

27 cartas implementadas hoy en `backend/app/db/seed_cards.sql` (correr después de `schema.sql`), con su
efecto modelado en `rules_engine.py` y tests en `test_rules_engine.py` — ver el detalle completo en
`backend/app/db/CARDS_LOG.md`.

**Meta:** cargar las ~200 cartas de proyecto del catálogo (de las 668 en la fuente usada), a este ritmo
de tandas verificadas manualmente contra el scan oficial. Es un trabajo incremental de varias sesiones.

**Regla de oro (explícita del usuario): no descartar cartas por falta de mecánica.** Cuando una carta no
encaja en el motor actual, la prioridad es extenderlo (nueva pieza en `apply_card_effect`, en
`use_card_action`, un nuevo tool, lo que haga falta) y cargarla con su test — no dejarla afuera. Ver
`CARDS_LOG.md` para el detalle de qué se fue agregando por esta razón: cartas con efecto inmediato
(`apply_card_effect`: `production_deltas`/`resource_deltas`/`convert_production`/`choice`), cartas con
requisito de tablero (`check_card_requirements`: `min_temperature`/`min_oxygen`/`min_oceans`), y cartas
con acción repetible y/o recursos propios (`use_card_action`/`register_active_card`, tool `use_card_action`
además de `play_card`). Genuinamente fuera de alcance por diseño (sección 6, no por mecánica faltante):
solo lo que requiere un segundo jugador o el mapa hexagonal con adyacencia — ver la sección correspondiente
en `CARDS_LOG.md` antes de asumir que algo no se puede modelar.

**Nota sobre la fuente de scans:** las descargas de imagen a `tm.hadronikle.com` deben espaciarse (varios
segundos entre pedidos) para no arriesgar un bloqueo del sitio — no bajar cartas en paralelo ni en ráfaga.

**Antes de cargar cartas nuevas, revisar `backend/app/db/CARDS_LOG.md`** — lleva el registro de qué
cartas ya están cargadas (para no repetir el trabajo de verificación), cuáles están "pendientes" porque
ya se identificó qué pieza de mecánica les falta (se resuelven agregando esa pieza, no evitándolas), y
cuáles quedan fuera por diseño explícito del MVP (multi-jugador, mapa hexagonal).

## 4. Stack tecnológico

| Capa | Tecnología | Notas |
|---|---|---|
| Orquestación de IA | Python + LangGraph | `StateGraph` con tool-calling explícito |
| Backend API | FastAPI | Expone `/chat` y `/state/{player_id}` |
| Base de datos | Supabase (Postgres) | Estado del juego, perfiles, historial de transacciones |
| Frontend | Next.js (App Router) + TypeScript + Tailwind | Desplegado en Vercel |
| Infraestructura | Docker (solo backend) | El frontend corre vía `npm run dev` / Vercel, no se containeriza |

Modelo LLM sugerido: Claude (vía `langchain-anthropic` o API directa). Se deja como variable de entorno
para no acoplar el código a un proveedor específico.

## 5. Estructura del repo

```
arbitro-ia/
├── backend/
│   ├── app/
│   │   ├── main.py            # Entry point FastAPI, CORS, incluye routers
│   │   ├── config.py          # Settings vía pydantic-settings (.env)
│   │   ├── agent/
│   │   │   ├── state.py       # TypedDict del estado del grafo
│   │   │   ├── rules_engine.py # Motor de reglas puro (ver sección 3) -- el corazón del repo
│   │   │   ├── tools.py       # Wrappers @tool: cargan/guardan estado en Supabase, llaman rules_engine
│   │   │   ├── prompts.py     # System prompt del nodo LLM
│   │   │   └── graph.py       # Definición del StateGraph (LLM -> ToolNode -> respuesta)
│   │   ├── db/
│   │   │   ├── supabase_client.py
│   │   │   └── schema.sql     # DDL: players, global_parameters, cards, transactions
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic: request/response de la API
│   │   └── api/
│   │       └── routes.py      # POST /chat, GET /state/{player_id}
│   ├── tests/
│   │   ├── test_rules_engine.py  # 30 tests con números verificados (criterio de éxito del PRD)
│   │   └── test_tools.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx            # Layout de 2 columnas: Dashboard | Sidebar Chat
    │   └── globals.css
    ├── components/
    │   ├── Dashboard.tsx       # Panel principal: recursos, banderas condicionales, historial
    │   ├── SidebarChat.tsx     # Chat persistente donde el usuario consulta jugadas
    │   └── ResourcePanel.tsx
    ├── lib/
    │   └── api.ts              # Cliente fetch hacia el backend
    └── package.json
```

## 6. Alcance (del PRD original — no expandir sin decidirlo explícitamente)

**Dentro de alcance:** interfaz conversacional en sidebar, dashboard de estado del jugador, enrutamiento
a herramientas para cálculos de redención, memoria persistente del estado de la sesión actual.

**Fuera de alcance (MVP):** una IA que juegue de forma autónoma contra humanos, digitalización visual
completa del tablero (nos quedamos con datos tabulares/resúmenes de texto — no se modela el mapa
hexagonal, adyacencias ni bonus de colocación de tiles), soporte para múltiples juegos simultáneos,
milestones y awards (quedan fuera del MVP, se pueden agregar después siguiendo el mismo patrón que
`rules_engine.py`).

## 7. Comandos de desarrollo

```bash
# Backend (containerizado)
cd backend
cp .env.example .env          # completar SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY
docker build -t arbitro-backend .
docker run --env-file .env -p 8000:8000 arbitro-backend

# o local sin Docker, para iterar rápido
pip install -r requirements.txt
uvicorn app.main:app --reload

# Tests (el criterio de éxito del PRD es 100% de precisión en cálculos)
pytest tests/ -v          # correr desde backend/, con PYTHONPATH=. si hace falta

# Frontend
cd frontend
cp .env.example .env.local    # NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

## 8. Modelo de datos (Supabase)

Ver `backend/app/db/schema.sql`. Tablas: `players` (recursos + producción + TR por jugador),
`global_parameters` (temperatura/oxígeno/océanos, compartido por todos — fila única `game_id='default'`
para el MVP), `cards` (catálogo, **arranca vacío a propósito**, ver sección 3), `transactions`
(log de cada jugada resuelta, para auditar). Correr el `.sql` completo en el SQL editor de Supabase.

## 9. Estado actual del repo y próximos pasos

**Ya implementado y testeado:** el motor de reglas completo (`rules_engine.py`), sus 30 tests, las
tools que lo conectan a Supabase (`tools.py`), el `StateGraph` (`graph.py`), el system prompt con el
vocabulario real del juego (`prompts.py`), y el schema de Supabase (`schema.sql`).

**Orden sugerido para seguir iterando con Claude Code:**

1. Correr `schema.sql` y luego `seed_cards.sql` en un proyecto de Supabase real y completar `.env` con
   las credenciales.
2. Correr `pytest tests/ -v` para confirmar que el motor de reglas pasa en tu máquina (85 tests hoy).
3. Seguir cargando cartas reales en `seed_cards.sql` (a mano, verificadas contra tu copia del juego) e
   implementar/extender su efecto en `rules_engine.apply_card_effect` + un test por carta.
4. Probar `POST /api/chat` con casos reales ("quiero usar el proyecto estándar Ciudad", "cerrá mi fase
   de producción", "quiero jugar Sponsors") y ajustar `prompts.py` si el LLM extrae mal los argumentos.
5. Conectar el frontend (`Dashboard.tsx`, `SidebarChat.tsx`) a los endpoints reales, reemplazando los
   `TODO` de datos mock.
6. Si querés ampliar el motor: milestones, awards, o bonus de colocación de tiles son las piezas más
   grandes que quedaron fuera del MVP — cada una sigue el mismo patrón de `rules_engine.py` (función
   pura + test con número exacto).

## 10. Convenciones

- Python: type hints en todo, `pydantic` para validación de I/O, funciones de `tools.py` sin efectos
  secundarios ocultos (reciben estado, devuelven estado nuevo + resultado).
- Commits: mensajes en imperativo, en español o inglés (mantener consistencia una vez que se elija).
- No commitear `.env` — solo `.env.example`.
- Cualquier función que "calcule" algo debe tener un test que verifique el número exacto, no solo que
  "no explote".
