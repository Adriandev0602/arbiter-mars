# Graph Report - arbiter-mars  (2026-10-02)

## Corpus Check
- 57 files · ~182,876 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1664 nodes · 3184 edges · 81 communities (48 shown, 33 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Tools Supabase (1)
- Turmoil: núcleo político (1)
- Colonies: colonias, Pluto/Europa y descartes (1)
- Errores, producción e investigación (1)
- Núcleo rules_engine y parámetros (1)
- Errores, producción e investigación (2)
- Frontend: chat mockeado
- Scripts de mantenimiento del catálogo
- Tablero: adyacencias (1)
- package.json frontend
- Tablero: greenery y special tiles
- Docs del repo y README desactualizado (1)
- Marcadores: nomads y community
- Modelo Board (1)
- Registro CARDS_LOG y recursos tipados (1)
- Config TypeScript
- First actions de corporaciones (motor) (1)
- Colonies: colonias, Pluto/Europa y descartes (2)
- Visión del proyecto y alcance (1)
- Conversión y pasivos permanentes
- API FastAPI (routes/schemas) (1)
- Modelo Board (2)
- Tools Supabase (2)
- First actions de corporaciones (motor) (2)
- Grafo LangGraph (1)
- Océanos en el tablero
- Schema y base de datos
- Turmoil: Ruling Bonus y TR Revision
- Tablero: adyacencias (2)
- GET /state (1)
- Las 3 cartas dudosas (cargadas)
- Modelo Board (3)
- Config y cliente Supabase
- Corporaciones: mecánicas resueltas
- resolve_ocean_offer (Unity)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- scripts/apply_db.py (schema + 4 seeds, i
- Grafo LangGraph (2)
- Fuera de alcance por diseño (1)
- Entry point FastAPI
- Docs del repo y README desactualizado (2)
- Fuentes del mapa Tharsis
- Núcleo rules_engine y parámetros (2)
- API FastAPI (routes/schemas) (2)
- Preludes: jugada y snapshots
- Fuera de alcance por diseño (2)
- Descuentos y pasivos por evento
- Turmoil: núcleo político (2)
- Fuera de alcance por diseño (3)
- _stratopolis_player()
- Tests ruling_or_delegates
- Volcanes y Noctis City
- Registro CARDS_LOG y recursos tipados (2)
- next.config
- Adyacencia precalculada
- Visión del proyecto y alcance (2)
- Errores, producción e investigación (3)
- Mapas alternativos (fuera)
- Visión del proyecto y alcance (3)
- Visión del proyecto y alcance (4)

## God Nodes (most connected - your core abstractions)
1. `PlayerState` - 104 edges
2. `play_card()` - 69 edges
3. `new_board()` - 48 edges
4. `play_prelude()` - 40 edges
5. `new_turmoil()` - 37 edges
6. `use_card_action()` - 34 edges
7. `CARDS_LOG: registro de cartas cargadas/pendientes` - 34 edges
8. `InvalidPlacementError` - 33 edges
9. `_load_player()` - 33 edges
10. `resolve_corporation_first_action()` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Reds policy en el borde de tools.py (_apply_reds_ruling_policy)` --references--> `_apply_reds_ruling_policy()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `deal_prelude_hand / keep_preludes` --references--> `deal_prelude_hand()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `tool resolve_corporation_first_action` --references--> `resolve_corporation_first_action()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `pending_card_discards + resolve_pending_discards` --references--> `resolve_pending_discards()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `pending_prelude_draw + resolve_prelude_draw` --references--> `resolve_prelude_draw()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fuera de alcance del proyecto** — agents_oos_milestones, agents_oos_maps, agents_oos_ares, agents_oos_solar_phase, agents_oos_solo, agents_oos_ai [EXTRACTED 0.95]
- **Pendientes y huecos cerrados 2026-10-02 (A-E)** — agents_colonies_11, agents_doubtful_cards, agents_unity_ocean_offer, agents_first_actions, agents_setup_clauses [EXTRACTED 0.95]
- **First actions de corporaciones resueltas** — backend_app_db_cards_log_first_actions_generic, backend_app_db_cards_log_valley_trust, backend_app_db_cards_log_celestic_first_action, backend_app_db_cards_log_philares_first_action, backend_app_db_cards_log_tharsis_first_action, backend_app_db_cards_log_aridor_first_action, backend_app_db_cards_log_poseidon_first_action, backend_app_db_cards_log_arcadian_first_action [EXTRACTED 1.00]
- **Exclusiones multijugador por diseno** — backend_app_db_cards_log_air_raid, backend_app_db_cards_log_law_suit, backend_app_db_cards_log_crash_site_cleanup, backend_app_db_cards_log_rover_construction, backend_app_db_cards_log_mons_insurance_opponent, backend_app_db_cards_log_herbivores_opponent_clause, backend_app_db_cards_log_philares_effect, backend_app_db_cards_log_nirgal_effect, backend_app_db_cards_log_protected_habitats [EXTRACTED 1.00]
- **T11 Recruitment completo: neutrales, track y Chairman TR** — backend_app_db_cards_log_t11_recruitment, backend_app_db_cards_log_neutral_delegates_official, backend_app_db_cards_log_global_event_party_cols, backend_app_db_cards_log_global_event_track, backend_app_db_cards_log_chairman_tr_bonus [EXTRACTED 1.00]
- **Piezas de first action unificadas** — agents_first_actions, agents_resolve_first_action, agents_prelude_draw [INFERRED 0.75]
- **Static Tharsis board data model** — backend_app_db_hex_map_research_hex_table_61, backend_app_db_hex_map_research_precomputed_adjacency, backend_app_db_hex_map_research_ocean_hex_count_12, backend_app_db_hex_map_research_volcanic_hexes [INFERRED 0.85]

## Communities (81 total, 33 thin omitted)

### Community 1 - "Tools Supabase (1)"
Cohesion: 0.06
Nodes (58): tools.py wrapper de I/O Supabase, apply_production_increased_bonus(), remove_prelude_from_hand(), snapshot_production_totals(), _apply_colony_gain(), _apply_colony_placement_bonus(), _apply_community_build_bonus(), _apply_hex_bonus() (+50 more)

### Community 2 - "Turmoil: núcleo político (1)"
Cohesion: 0.07
Nodes (60): Track de eventos setup_global_events / Changing Times, T11 Recruitment: delegados neutrales oficiales (14, 1 Chairman, 13 reserva), _add_to_party(), can_play_party_gated_card(), changing_times(), _check_party(), compute_influence(), exchange_neutral_delegate() (+52 more)

### Community 3 - "Colonies: colonias, Pluto/Europa y descartes (1)"
Cohesion: 0.06
Nodes (50): add_colony_tile(), adjust_colony_track(), build_colony(), ColonyFullError, ColonyOccupiedError, ColonyTileState, new_colonies(), run_colony_production() (+42 more)

### Community 4 - "Errores, producción e investigación (1)"
Cohesion: 0.05
Nodes (37): adjust_mc_production(), apply_any_tag_played_choice(), apply_city_placed_bonuses(), apply_greenery_placed_bonuses(), apply_hex_bonus_tile_bonuses(), apply_standard_project_used_bonuses(), apply_tag_played_choice(), CardEffectError (+29 more)

### Community 5 - "Núcleo rules_engine y parámetros (1)"
Cohesion: 0.06
Nodes (30): apply_card_effect(), apply_colony_placed_bonuses(), _apply_production_floor(), apply_tag_played_resource_bonuses(), calculate_card_payment(), convert_heat_to_temperature(), corporation_first_action_city(), corporation_first_action_greenery() (+22 more)

### Community 6 - "Errores, producción e investigación (2)"
Cohesion: 0.05
Nodes (25): Vocabulario extensible de effects/requirements, Tag comodin wild, apply_become_party_leader_bonus(), apply_card_resource_gained_bonuses(), apply_cost_threshold_mc_bonuses(), apply_event_played_bonuses(), apply_new_distinct_tag_bonuses(), CardNotInHandError (+17 more)

### Community 7 - "Frontend: chat mockeado"
Cohesion: 0.09
Nodes (34): Layout responsivo (chat abajo en celular), Frontend v1 (Next 14 + Tailwind, dashboard, selector jugador), Selector/creacion de jugador (localStorage, ?player=), metadata, Home(), CardList(), KIND_LABEL, Dashboard() (+26 more)

### Community 8 - "Scripts de mantenimiento del catálogo"
Cohesion: 0.07
Nodes (16): main(), parse_db_url(), read_env_db_url(), main(), safe_filename(), build_image_url_index(), load_site_catalog(), main() (+8 more)

### Community 9 - "Tablero: adyacencias (1)"
Cohesion: 0.10
Nodes (17): can_place_city_adjacent_to_cities(), can_place_city_on_volcanic(), can_place_greenery(), can_place_ocean_on_land(), get_neighbors(), remove_ocean_tile(), UnknownHexError, test_can_place_city_adjacent_to_cities_requires_min_count() (+9 more)

### Community 10 - "package.json frontend"
Cohesion: 0.07
Nodes (29): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+21 more)

### Community 11 - "Tablero: greenery y special tiles"
Cohesion: 0.16
Nodes (21): can_place_special_tile(), InvalidPlacementError, new_board(), place_greenery_tile(), place_ocean_tile_on_land(), place_special_tile(), Generic place_special_tile parametrized by requirement, test_can_place_special_tile_requires_matching_hex_bonus() (+13 more)

### Community 12 - "Docs del repo y README desactualizado (1)"
Cohesion: 0.17
Nodes (16): Marcadores en tablero (nomad, cathedral, remove_greenery), board.py mapa hexagonal Tharsis, Flujo de ramas feat/review-block-N, Referencia a CARDS_LOG.md, Convenciones (type hints, funciones puras, tests con numero exacto), Sistema mazo/mano/investigacion, Grafo determinista LangGraph (graph.py, siempre via ToolNode), Frontend components Dashboard/SidebarChat/ResourcePanel (+8 more)

### Community 13 - "Marcadores: nomads y community"
Cohesion: 0.13
Nodes (13): community_owner(), count_tiles_of_type(), find_nomads(), HexOccupiedError, HexState, move_nomads(), place_community(), place_nomads() (+5 more)

### Community 14 - "Modelo Board (1)"
Cohesion: 0.13
Nodes (12): _build_adjacency(), _build_hex_defs(), count_cathedrals(), HexDef, _neighbor_coords(), place_cathedral(), remove_greenery_tile(), _row() (+4 more)

### Community 15 - "Registro CARDS_LOG y recursos tipados (1)"
Cohesion: 0.11
Nodes (18): Cartas activas: accion repetible, Bloque 31: multi-agente y revision de tags, Pago con recurso de carta (Dirigibles, Psychrophiles), Sistema de mazo / mano, Diversity Support (X20), Vocabulario de effects soportado en apply_card_effect, Vias de pago: acero/titanio, card_resource, stock_resource, standard_project_card_resource, Global Events bloque 5 (multi-agente) (+10 more)

### Community 16 - "Config TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 17 - "First actions de corporaciones (motor) (1)"
Cohesion: 0.12
Nodes (18): POST /api/chat con updated_state y errores 503/429, GET /api/game, GET/POST /api/players, GET /api/state/{id} devuelve {player, cards}, Auditoria completa de tags/requisitos/VP negativos del catalogo base, Prueba end-to-end del chat (ANTHROPIC_API_KEY placeholder), Corporaciones 48 de 48, Mas iteraciones del frontend (+10 more)

### Community 18 - "Colonies: colonias, Pluto/Europa y descartes (2)"
Cohesion: 0.14
Nodes (13): Expansion Colonies y mecanica colonies.py, Jugar carta dentro de otra (Ecology Experts, Board of Directors), IA autonoma contra humanos / multi-juego, Pago cruzado Ares, Mapas Hellas/Elysium, Milestones y awards, Solar Phase de Venus Next, Variante solitario oficial (TR 14) (+5 more)

### Community 19 - "Visión del proyecto y alcance (1)"
Cohesion: 0.14
Nodes (14): Colonias Pluto y Europa, catalogo 11 de 11, deal_prelude_hand / keep_preludes, 3 cartas dudosas cargadas (self_replicating_robots, venus_orbital_survey, wg_project), first actions de corporaciones (effects.first_action), graphify-out grafo del proyecto (se commitea siempre), Nirgal y Effect de Philares fuera de alcance por diseno, pending_card_discards + resolve_pending_discards, pending_prelude_draw + resolve_prelude_draw (+6 more)

### Community 20 - "Conversión y pasivos permanentes"
Cohesion: 0.15
Nodes (10): Unity en resolve_ocean_offer (hueco inexistente, funcion movida al motor), compute_conversion_rates(), resolve_ocean_offer(), _load_global_event_parties(), resolve_new_government(), Reds Ruling Policy en el borde de tools.py, Gap resolve_ocean_offer y Unity, TR Revision (-1 TR por generacion) (+2 more)

### Community 21 - "API FastAPI (routes/schemas) (1)"
Cohesion: 0.26
Nodes (6): ChatRequest, ChatResponse, CreatePlayerRequest, GameState, PlayerStateResponse, PlayerSummary

### Community 22 - "Modelo Board (2)"
Cohesion: 0.22
Nodes (9): count_adjacent_oceans(), count_adjacent_owned_by(), count_cities_and_special_tiles_adjacent_to_ocean(), count_empty_hexes_adjacent_to_owner(), count_tiles_adjacent_to_ocean(), get_adjacent_tiles(), resolve_ocean_adjacency_bonus(), test_count_tiles_adjacent_to_ocean_counts_each_tile_once() (+1 more)

### Community 23 - "Tools Supabase (2)"
Cohesion: 0.14
Nodes (7): apply_card_played_vp_icon_bonus(), apply_corporation_start(), increment_tags_played(), register_corporation_first_action(), register_played_card(), resolve_active_card_starting_resources(), choose_corporation()

### Community 24 - "First actions de corporaciones (motor) (2)"
Cohesion: 0.15
Nodes (12): reveal_cards_until_matching(), Arcadian Communities first action: place community, Aridor first action: add_colony_tile, Celestic first action reveal_until_matching (33 cartas con floater), Corporaciones: categoria completa 48 de 48, First actions de corporaciones (effects.first_action, resolve_corporation_first_action), Philares first action: greenery, Poseidon first action: place colony (+4 more)

### Community 26 - "Océanos en el tablero"
Cohesion: 0.21
Nodes (10): can_place_ocean(), is_hex_empty(), place_ocean_tile(), Tile placement legality rules (ocean, greenery, city, special), test_can_place_ocean_only_on_ocean_hex(), test_new_board_is_empty(), test_place_ocean_tile_occupies_hex(), test_place_ocean_tile_on_land_hex_raises() (+2 more)

### Community 27 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 28 - "Turmoil: Ruling Bonus y TR Revision"
Cohesion: 0.20
Nodes (9): Comprehensive FAQ v1.7 (fuente), Global Events 36 de 36, Reds policy en el borde de tools.py (_apply_reds_ruling_policy), Turmoil nucleo politico (turmoil.py), Turmoil: TR Revision + Ruling Bonus + 6 Ruling Policy, apply_ruling_bonus(), Ciclo de generaciones de Global Events no automatizado, Turmoil: Global Events (36 de 36) (+1 more)

### Community 29 - "Tablero: adyacencias (2)"
Cohesion: 0.31
Nodes (9): can_place_city(), has_city_adjacent_to_ocean(), place_city_tile(), test_can_place_city_on_volcanic_ignores_city_adjacency(), test_cannot_place_city_adjacent_to_another_city(), test_cannot_place_city_on_noctis_city_reserved_hex(), test_has_city_adjacent_to_ocean_filtra_por_dueno(), test_has_city_adjacent_to_ocean_ignora_ciudad_lejos_del_agua() (+1 more)

### Community 30 - "GET /state (1)"
Cohesion: 0.20
Nodes (5): _card_catalog(), get_game(), get_state(), list_players(), _player_or_404()

### Community 31 - "Las 3 cartas dudosas (cargadas)"
Cohesion: 0.22
Nodes (7): Catalogo de cartas (412 de proyecto), Tabla card_review_queue (cola vacia), Clausulas omitidas por diseno (remove from any player, oponentes, solo VP), Cartas dependientes de oponentes (Air Raid, Law Suit, Crash Site Cleanup, Rover Construction, Mons Insurance, Herbivores), scan_cache gitignored (derechos FryxGames), download_review_scans.py (2.5s entre pedidos), README status table (412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, 715 tests)

### Community 32 - "Modelo Board (3)"
Cohesion: 0.22
Nodes (6): _place(), place_city_tile_adjacent_to_cities(), resolve_hex_bonus(), test_hex_bonus_is_consumed_only_once(), test_place_city_tile_adjacent_to_cities_illegal_raises(), test_place_city_tile_adjacent_to_cities_succeeds_when_legal()

### Community 34 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.22
Nodes (9): Arcadian Communities: TileType community, Corporaciones bloque 2 (Ecotec a Manutech), Corporaciones: mecanicas pendientes resueltas (_raise_tr), _increase_production (Manutech), Manutech, Mons Insurance: clausulas de oponentes, Pharmacy Union (retire_card_as_event), Hook unico _raise_tr y tr_raised_this_generation (+1 more)

### Community 35 - "resolve_ocean_offer (Unity)"
Cohesion: 0.22
Nodes (9): _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each(), test_resolve_ocean_offer_triggers_manutech(), test_resolve_ocean_offer_unity_ruling_does_not_raise_steel_value() (+1 more)

### Community 36 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 37 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 38 - "scripts/apply_db.py (schema + 4 seeds, i"
Cohesion: 0.33
Nodes (6): Nota: host Supabase resuelve solo por IPv6, Password con @ rompe psycopg2.connect(url), RLS activo en 11 tablas sin policies; backend usa clave secret, apply_db.py aplica schema+seeds idempotente, Prueba de humo contra Supabase real 19 de 19, Migracion a Supabase nuevo proyecto

### Community 40 - "Fuera de alcance por diseño (1)"
Cohesion: 0.33
Nodes (6): Air Raid (C02), Crash Site Cleanup (X17), Herbivores: clausula de oponente, Law Suit (X06), Fuera de alcance por diseno, Rover Construction (038)

### Community 42 - "Docs del repo y README desactualizado (2)"
Cohesion: 0.40
Nodes (4): Modelo de datos Supabase (players, global_parameters, cards, queues, transactions), Bugs preexistentes (_load_player, schema.sql columnas, Manutech colonias), Stack: LangGraph, FastAPI, Supabase, Next.js, Docker, Dependencia supabase>=2.8.0

### Community 43 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 44 - "Núcleo rules_engine y parámetros (2)"
Cohesion: 0.40
Nodes (4): is_blue_card(), Dry Deserts, Mud Slides, Solarnet Shutdown, Comprehensive FAQ v1.7: 4 bugs corregidos en Global Events, Global Events bloque 6 (3 pendientes, mazo completo)

### Community 46 - "Preludes: jugada y snapshots"
Cohesion: 0.40
Nodes (4): Ecology Experts y Board of Directors (preludes 70 de 70), Jugar una carta dentro de otra (nested_card_id), Prelude bloque 2: 26 de 46 y bug de draw_cards_matching_tag, Bugs de cableado en tools.py (played_cards, discard_card_id, effect_choice, _load_player)

### Community 47 - "Fuera de alcance por diseño (2)"
Cohesion: 0.40
Nodes (5): Herbivores (147, cargada), Tabla de cartas de proyecto cargadas (~408), Protected Habitats (173), Stratopolis (corregida), VP impresos no se modelan (Interstellar Colony Ship, Public Celebrations)

### Community 48 - "Descuentos y pasivos por evento"
Cohesion: 0.50
Nodes (3): Pago con recurso de carta, register_passive_effect(), Efectos pasivos permanentes

### Community 49 - "Turmoil: núcleo político (2)"
Cohesion: 0.50
Nodes (4): Bloque 31 segunda tanda: cierre de pendientes, Self-Replicating Robots (210), Venus Orbital Survey (P88), WG Project (P91)

### Community 50 - "Fuera de alcance por diseño (3)"
Cohesion: 0.50
Nodes (4): Corporaciones bloques 3-5 (41 de 48), Nirgal Enterprises: Effect de awards/milestones, Philares: Effect de adyacencia con tiles de oponente, Valley Trust (first action reveal_preludes)

### Community 51 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 52 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 54 - "Registro CARDS_LOG y recursos tipados (2)"
Cohesion: 0.67
Nodes (3): Auditoria power/space: 42 de 62 mal, corregidas, tag_contact_sheet.py (hojas de contacto), Iconografia de tags: power vs space (auditoria de 62 cartas)

## Knowledge Gaps
- **134 isolated node(s):** `Config`, `metadata`, `nextConfig`, `Generic place_special_tile parametrized by requirement`, `Ares cross-payment` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1019 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Frontend v1 (Next 14 + Tailwind, dashboard, selector jugador)` connect `Frontend: chat mockeado` to `First actions de corporaciones (motor) (1)`, `Docs del repo y README desactualizado (2)`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `rules_engine.py motor de reglas puro` connect `Docs del repo y README desactualizado (1)` to `Tools Supabase (1)`, `Errores, producción e investigación (1)`, `Núcleo rules_engine y parámetros (1)`, `Errores, producción e investigación (2)`, `Descuentos y pasivos por evento`, `Conversión y pasivos permanentes`, `Turmoil: Ruling Bonus y TR Revision`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `tools.py wrapper de I/O Supabase` connect `Tools Supabase (1)` to `Docs del repo y README desactualizado (1)`, `Errores, producción e investigación (2)`, `Tools Supabase (2)`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **What connects `Config`, `metadata`, `nextConfig` to the rest of the system?**
  _134 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor` be split into smaller, more focused modules?**
  _Cohesion score 0.0034542314335060447 - nodes in this community are weakly interconnected._
- **Should `Tools Supabase (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.05814905814905815 - nodes in this community are weakly interconnected._
- **Should `Turmoil: núcleo político (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.0680517916290274 - nodes in this community are weakly interconnected._