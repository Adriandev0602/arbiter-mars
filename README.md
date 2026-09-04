# Árbitro Asistente de Reglas — Terraforming Mars

Un agente conversacional que resuelve los cálculos de una partida de **Terraforming Mars**: fase de
producción, proyectos estándar, pago de cartas, colocación de tiles, comercio con colonias y la
política de Turmoil. El usuario escribe en lenguaje natural ("cerrá mi fase de producción", "quiero
jugar Lava Tube Settlement pagando 4 MC y 3 de acero") y recibe un veredicto con el estado
actualizado.

Es un proyecto de portfolio, y su tesis es específica: **no es un chatbot más, es una demostración
de control arquitectónico estricto sobre un LLM probabilístico.**

## La idea central: el LLM nunca hace matemática

El modelo tiene exactamente un trabajo: leer la intención del usuario y extraer argumentos
estructurados — `{"card_id": "lava_tube_settlement", "mc_to_pay": 4, "steel_to_pay": 3}`. Todo
cálculo de saldos, validación de reglas y comparación contra el estado del juego ocurre en
funciones Python puras y deterministas.

Eso se sostiene en dos capas:

1. **El system prompt** le prohíbe responder con números calculados por él mismo; su única salida
   legítima es una tool call o repetir literalmente lo que devolvió la tool.
2. **El grafo de LangGraph** enruta *siempre* por el `ToolNode` antes de la respuesta final: no
   existe un camino donde el modelo conteste directo una consulta que implique un cálculo.

Cualquier cambio que le permita al LLM "adivinar" un número es un bug de arquitectura, no una
mejora de UX.

## Cómo está separado el código

```
backend/app/agent/
├── rules_engine.py   # motor puro: recursos, producción, TR, efectos de cartas
├── board.py          # mapa hexagonal Tharsis (61 hexágonos, adyacencia, colocación)
├── colonies.py       # colonias y comercio (expansión Colonies)
├── turmoil.py        # partidos, delegados, influencia (expansión Turmoil)
├── tools.py          # ÚNICA capa con I/O — carga/guarda estado en Supabase
├── graph.py          # StateGraph: LLM → ToolNode → respuesta
└── prompts.py        # system prompt
```

Los cuatro módulos de reglas son funciones puras sin dependencias de FastAPI, Supabase ni
LangGraph: reciben estado y devuelven estado nuevo. Están deliberadamente **desacoplados entre
sí** — `rules_engine.py` no importa `board.py`, `colonies.py` ni `turmoil.py`. Cuando un efecto
necesita datos de otro subsistema (la influencia política, el conteo de tiles del mapa), `tools.py`
los resuelve antes y se los pasa al motor como valores simples.

## Estado actual

| | |
|---|---|
| Cartas de proyecto cargadas | **312** |
| Global Events (Turmoil) | **36 / 36** — mazo completo |
| Tests | **533**, todos verdes |
| Cartas pendientes de revisar | 101 |

Expansiones con cartas cargadas: Base (62), Venus Next (51), Colonies (48), Corporate Era (26),
Prelude (7), Prelude 2 (2), Promo (3).

**Mecánicas implementadas:** los 4 parámetros globales (temperatura, oxígeno, océanos, Venus scale),
los 6 proyectos estándar, mazo/mano/investigación, efectos pasivos y acciones repetibles, el mapa
Tharsis completo, colonias y comercio, y el núcleo político de Turmoil (partidos, delegados,
lobbying, party leader, partido dominante, chairman e influencia).

**Fuera de alcance, deliberadamente:** una IA que juegue sola, partidas simultáneas, milestones y
awards, mapas alternativos (Hellas/Elysium), y — dentro de Turmoil — las Ruling Policies de los 6
partidos. El modo de un jugador se trata como una partida estándar (TR 20), no como la variante
solitario oficial del reglamento.

## Cómo se construye el catálogo (y por qué importa)

El criterio de éxito del proyecto es 100% de precisión en los cálculos, y un número mal recordado
lo rompe. Por eso **no se generan datos de cartas al voleo**: cada carta se carga a mano, leyendo su
scan oficial, mapeando su texto exacto al vocabulario del motor y escribiendo su test.

Las consecuencias prácticas de esa regla:

- Cuando una carta no encaja en el vocabulario existente, la respuesta por defecto es **extender el
  motor**, no descartarla. Solo se posponen las que necesitan una pieza de mecánica grande, y
  quedan documentadas con el diagnóstico exacto de qué les falta.
- Si una cláusula no se puede modelar con honestidad, la carta **no se carga a medias**: cargar
  media carta es cargar una carta distinta.
- Las decisiones de interpretación quedan escritas con su fuente. Cuando el rulebook no alcanza, se
  cita el FAQ oficial de la comunidad — que, entre otras cosas, destapó cuatro cartas ya cargadas
  cuyos números estaban mal (incluida una con errata oficial del texto impreso).

El registro completo de qué está cargado, qué está pendiente y con qué criterio vive en
[`backend/app/db/CARDS_LOG.md`](./backend/app/db/CARDS_LOG.md).

## Quick start

```bash
# Backend
cd backend
cp .env.example .env      # SUPABASE_URL, SUPABASE_KEY, ANTHROPIC_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
cp .env.example .env.local
npm install && npm run dev

# Tests
cd backend && PYTHONPATH=. pytest tests/ -v
```

## Stack

| Capa | Tecnología |
|---|---|
| Orquestación de IA | Python + LangGraph (`StateGraph` con tool-calling explícito) |
| Backend | FastAPI |
| Base de datos | Supabase (Postgres) |
| Frontend | Next.js (App Router) + TypeScript + Tailwind |
| Infraestructura | Docker (backend) |

## Documentación

- [`CLAUDE.md`](./CLAUDE.md) — contexto arquitectónico completo y estado de avance. Leelo antes de
  iterar con Claude Code. ([`AGENTS.md`](./AGENTS.md) es el mismo contenido, agnóstico de herramienta.)
- [`backend/app/db/CARDS_LOG.md`](./backend/app/db/CARDS_LOG.md) — catálogo: cargadas, pendientes y
  fuera de alcance, con el vocabulario de efectos que consume cada una.
- [`backend/app/db/HEX_MAP_RESEARCH.md`](./backend/app/db/HEX_MAP_RESEARCH.md) — investigación del
  mapa hexagonal y sus fuentes.
