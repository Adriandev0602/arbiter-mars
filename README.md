# Rules Arbiter — Terraforming Mars

A conversational agent that resolves the calculations of a **Terraforming Mars** game: production
phase, standard projects, card payments, tile placement, colony trading, and Turmoil politics. The
user writes in natural language ("close my production phase", "I want to play Lava Tube Settlement
paying 4 MC and 3 steel") and gets back a verdict with the updated game state.

### What is Terraforming Mars?

[Terraforming Mars](https://www.fryxgames.se/games/terraforming-mars/) is a board game by
FryxGames in which players compete as corporations terraforming Mars over several generations
(turns). Each generation opens with a production phase, then players take turns playing project
cards, using standard projects, or converting resources — all funded by megacredits (MC) and
secondary resources like steel, titanium, plants, energy, and heat. Progress is tracked through
three global parameters (temperature, oxygen, and ocean tiles) that must reach their maximum
values to end the game, and through each player's Terraform Rating (TR), which acts as both score
and income. Cards add tags, one-time effects, or repeatable actions, and several expansions
(Venus Next, Colonies, Turmoil, Prelude, Corporate Era) layer extra mechanics — a Venus scale,
colony trading, political parties, faster starts — on top of that core loop. The rules involve a
lot of bookkeeping: tracking resource balances, checking placement adjacency, validating that a
card's requirements are met, and applying dozens of distinct card effects correctly. This project
exists to arbitrate exactly that bookkeeping.

This is a portfolio project, and its thesis is specific: **it isn't just another chatbot, it's a
demonstration of strict architectural control over a probabilistic LLM.**

## The core idea: the LLM never does math

The model has exactly one job: read the user's intent and extract structured arguments —
`{"card_id": "lava_tube_settlement", "mc_to_pay": 4, "steel_to_pay": 3}`. Every balance
calculation, rule validation, and comparison against game state happens in pure, deterministic
Python functions.

That's enforced by two layers:

1. **The system prompt** explicitly forbids the model from answering with numbers it computed
   itself; its only legitimate output is a tool call, or a response that literally repeats what
   the tool returned.
2. **The LangGraph graph** *always* routes through the `ToolNode` before the final response —
   there is no path where the model answers a calculation-bearing query directly.

Any change that lets the LLM "guess" a number is an architecture bug, not a UX improvement.

## How the code is split

```
backend/app/agent/
├── rules_engine.py   # pure engine: resources, production, TR, card effects
├── board.py          # Tharsis hex map (61 hexes, adjacency, tile placement)
├── colonies.py       # colonies and trading (Colonies expansion)
├── turmoil.py        # parties, delegates, influence (Turmoil expansion)
├── tools.py          # THE ONLY layer with I/O — loads/saves state in Supabase
├── graph.py          # StateGraph: LLM → ToolNode → response
└── prompts.py        # system prompt
```

The four rules modules are pure functions with no dependency on FastAPI, Supabase, or LangGraph:
they take state in and return new state. They're deliberately **decoupled from each other** —
`rules_engine.py` doesn't import `board.py`, `colonies.py`, or `turmoil.py`. When an effect needs
data from another subsystem (political influence, map tile counts), `tools.py` resolves it first
and passes it to the engine as plain values.

## Current status

| | |
|---|---|
| Project cards loaded | **340** |
| Global Events (Turmoil) | **36 / 36** — full deck |
| Prelude cards loaded | **48** |
| Cards pending review | 71 |

Expansions with cards loaded: Base, Venus Next, Colonies, Corporate Era, Prelude, Turmoil (Global
Events + political core), Promo.

**Implemented mechanics:** all 4 global parameters (temperature, oxygen, oceans, Venus scale), the
6 standard projects, deck/hand/research system, passive effects and repeatable card actions, the
full Tharsis map, colony building and trading, and Turmoil's political core (parties, delegates,
lobbying, party leader, dominant party, chairman, and influence).

**Explicitly out of scope:** an AI that plays autonomously, simultaneous games, milestones and
awards, alternate maps (Hellas/Elysium), and — within Turmoil — the Ruling Policies of the 6
parties. Single-player mode is treated as a standard game (TR 20), not the official rulebook's
solo variant. Corporations (the Corporation and Automa card categories) are a known gap not yet
modeled.

## How the catalog is built (and why it matters)

The project's success criterion is 100% calculation accuracy, and a misremembered number breaks
that. So **card data is never generated off the cuff**: each card is loaded by hand, reading its
official scan, mapping its exact text to the engine's vocabulary, and writing its test.

The practical consequences of that rule:

- When a card doesn't fit the existing vocabulary, the default response is to **extend the
  engine**, not skip the card. Only cards that need a large new mechanic get postponed, and they're
  documented with an exact diagnosis of what's missing.
- If a clause can't be modeled honestly, the card **isn't loaded halfway** — loading half a card is
  loading a different card.
- Interpretation decisions are written down with their source. When the rulebook isn't enough, the
  official community FAQ is cited — which, among other things, surfaced four already-loaded cards
  with wrong numbers (including one with an official printed errata).

The full record of what's loaded, what's pending, and under what criteria lives in
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

| Layer | Technology |
|---|---|
| AI orchestration | Python + LangGraph (`StateGraph` with explicit tool-calling) |
| Backend | FastAPI |
| Database | Supabase (Postgres) |
| Frontend | Next.js (App Router) + TypeScript + Tailwind |
| Infrastructure | Docker (backend) |

## Documentation

- [`CLAUDE.md`](./CLAUDE.md) — full architectural context and progress log. Read it before
  iterating with Claude Code. ([`AGENTS.md`](./AGENTS.md) is the same content, tool-agnostic.)
- [`backend/app/db/CARDS_LOG.md`](./backend/app/db/CARDS_LOG.md) — catalog: loaded, pending, and
  out-of-scope cards, with the effect vocabulary each one consumes.
- [`backend/app/db/HEX_MAP_RESEARCH.md`](./backend/app/db/HEX_MAP_RESEARCH.md) — research on the
  hex map and its sources.
