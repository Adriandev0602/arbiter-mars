# Graph Report - arbiter-mars  (2026-10-03)

## Corpus Check
- 68 files · ~201,750 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1886 nodes · 5828 edges · 125 communities (85 shown, 40 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 281 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor (1)
- Colonies: colonias, Pluto/Europa y descartes
- Tests generales del motor (2)
- Tests generales del motor (3)
- Tests generales del motor (4)
- Tests generales del motor (5)
- Tests generales del motor (6)
- Tests generales del motor (7)
- Tools Supabase (1)
- Modelo Board (1)
- Errores, producción e investigación (1)
- Docs del repo y README desactualizado (1)
- Tablero: adyacencias (1)
- Errores, producción e investigación (2)
- Tests generales del motor (8)
- Turmoil: núcleo político (1)
- Tools Supabase (2)
- Tools Supabase (3)
- package.json frontend (1)
- Tablero: greenery y special tiles
- Frontend: chat mockeado (1)
- Errores, producción e investigación (3)
- Tests generales del motor (9)
- Tablero: adyacencias (2)
- Turmoil: núcleo político (2)
- Tools Supabase (4)
- Errores, producción e investigación (4)
- Tools Supabase (5)
- Tests generales del motor (10)
- API FastAPI (1)
- Tests generales del motor (11)
- Tools Supabase (6)
- ui_e2e.py
- Tools Supabase (7)
- Scripts de mantenimiento del catálogo (1)
- Frontend: chat mockeado (2)
- Núcleo rules_engine y parámetros
- Config TypeScript
- Tests generales del motor (12)
- GET /state (1)
- Frontend: chat mockeado (3)
- Modelo Board (2)
- Grafo LangGraph (1)
- Scripts de mantenimiento del catálogo (2)
- Turmoil: núcleo político (3)
- Card catalog
- Tools Supabase (8)
- SetupFlow.tsx
- audit_catalog.py
- Turmoil: núcleo político (4)
- Corporaciones: mecánicas resueltas
- Frontend: chat mockeado (4)
- Errores, producción e investigación (5)
- Errores, producción e investigación (6)
- Errores, producción e investigación (7)
- Errores, producción e investigación (8)
- resolve_ocean_offer
- Config y cliente Supabase (1)
- Schema y base de datos
- Docs del repo y README desactualizado (2)
- Errores, producción e investigación (9)
- Las 3 cartas dudosas (1)
- Marcadores: nomads y community
- Turmoil: núcleo político (5)
- Tests generales del motor (13)
- First actions de corporaciones
- Tests generales del motor (14)
- Modelo Board (3)
- Config y cliente Supabase (2)
- Scripts de mantenimiento del catálogo (3)
- package.json frontend (2)
- Tests generales del motor (15)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- Tests generales del motor (16)
- Turmoil: núcleo político (6)
- Fuentes del mapa Tharsis
- Tests generales del motor (17)
- Tests generales del motor (18)
- Tests generales del motor (19)
- GET /state (2)
- Volcanes y Noctis City
- Tests generales del motor (20)
- _stratopolis_player()
- Tests ruling_or_delegates
- Docs del repo y README desactualizado (3)
- Punto de retoma 2026-09-10: T11 Recruitm
- Stack: Python, LangGraph, FastAPI, Supab
- next.config
- Diversity Support
- Adyacencia precalculada
- GET /state (3)
- API FastAPI (2)
- Visión del proyecto y alcance (1)
- Ares cross-payment mechanic
- Autonomous AI playing humans
- Alternative maps Hellas/Elysium
- Multiple simultaneous games
- Official solo variant
- Hardcoded catalog of special tiles
- Venus Solar Phase
- CARDS_LOG.md
- Mapas alternativos
- Visión del proyecto y alcance (2)
- Visión del proyecto y alcance (3)
- Las 3 cartas dudosas (2)

## God Nodes (most connected - your core abstractions)
1. `new_player_state()` - 558 edges
2. `new_global_parameters()` - 460 edges
3. `apply_card_effect()` - 327 edges
4. `register_active_card()` - 158 edges
5. `check_card_requirements()` - 139 edges
6. `use_card_action()` - 120 edges
7. `CardRequirementNotMetError` - 106 edges
8. `PlayerState` - 97 edges
9. `register_passive_effect()` - 95 edges
10. `play_card()` - 82 edges

## Surprising Connections (you probably didn't know these)
- `Old tech debt: T11 fixed 2 neutrals per party (superseded)` --references--> `exchange_neutral_delegate()`  [INFERRED]
  AGENTS.md → backend/app/agent/turmoil.py
- `Hex board scope decision 2026-08-31` --semantically_similar_to--> `Hex board Tharsis: 61 hexes, 12 reserved ocean, Noctis, 4 volcanic`  [INFERRED] [semantically similar]
  backend/app/db/CARDS_LOG.md → AGENTS.md
- `free_trade gain handled in tools.use_card_action` --references--> `use_card_action()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `Bug: _load_player missed 3 columns (KeyError vs real Supabase)` --references--> `_load_player()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `pending_card_discards + resolve_pending_discards (Pluto)` --references--> `resolve_pending_discards()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **2026-10-02 catalog audit workflow** — agents_audit_method, backend_scripts_audit_catalog, agents_audit_result, agents_audit_catalog_rule [EXTRACTED 1.00]
- **Two-layer enforcement of 'LLM never does math'** — agents_system_prompt_layer, agents_deterministic_graph_layer, agents_llm_never_math [EXTRACTED 1.00]
- **Four-plus payment paths** — backend_app_db_cards_log_payment_paths, backend_app_db_cards_log_stock_resource_payment, backend_app_db_cards_log_card_resource_payment [EXTRACTED 1.00]
- **Single choke-point refactors unlocking many cards** — agents_raise_tr_choke, agents_increase_production_choke, agents_reds_policy_edge [INFERRED 0.75]
- **Board marker family (nomad, cathedral, community, remove tile)** — backend_app_db_cards_log_nomad_marker, backend_app_db_cards_log_cathedral_marker, agents_arcadian_communities, backend_app_db_cards_log_remove_tile_piece [INFERRED 0.85]
- **Reveal-N-preludes-play-1 users** — backend_app_db_cards_log_wg_project, backend_app_db_cards_log_valley_trust, backend_app_db_cards_log_ecology_experts_board_directors [INFERRED 0.85]
- **Static Tharsis board data model** — backend_app_db_hex_map_research_hex_table_61, backend_app_db_hex_map_research_precomputed_adjacency, backend_app_db_hex_map_research_ocean_hex_count_12, backend_app_db_hex_map_research_volcanic_hexes [INFERRED 0.85]

## Communities (125 total, 40 thin omitted)

### Community 0 - "Tests generales del motor (1)"
Cohesion: 0.03
Nodes (125): new_player_state(), test_adjust_mc_production_respects_floor_of_minus_5(), test_apply_corporation_start_pone_produccion_en_cero(), test_aquifer_costs_18_mc_places_ocean_and_1_tr(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_artificial_photosynthesis_choice_1_gives_energy_production(), test_asteroid_card_raises_temperature_and_gives_titanium(), test_big_asteroid_raises_temperature_2_steps_and_gives_4_titanium() (+117 more)

### Community 1 - "Colonies: colonias, Pluto/Europa y descartes"
Cohesion: 0.06
Nodes (51): add_colony_tile(), adjust_colony_track(), build_colony(), ColonyDef, ColonyFullError, ColonyOccupiedError, ColonyTileState, new_colonies() (+43 more)

### Community 2 - "Tests generales del motor (2)"
Cohesion: 0.03
Nodes (69): Extensible effects vocabulary in apply_card_effect, apply_card_effect(), effects vocabulary reference section, test_acquired_company_gives_plus_3_mc_production(), test_adapted_lichen_gives_plus_1_plant_production(), test_aquifer_released_places_ocean_without_granting_tr(), test_black_polar_dust_places_ocean_and_changes_production(), test_comet_raises_temperature_and_places_ocean() (+61 more)

### Community 3 - "Tests generales del motor (3)"
Cohesion: 0.03
Nodes (66): new_global_parameters(), test_apply_card_effect_with_no_effects_is_a_noop(), test_archaebacteria_gives_plus_1_plant_production(), test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr(), test_asteroid_mining_gives_plus_2_titanium_production(), test_capped_counter_new_sources_colonies_hand_and_production(), test_check_card_requirements_none_or_empty_is_a_noop(), test_city_costs_25_mc_and_gives_1_mc_production() (+58 more)

### Community 4 - "Tests generales del motor (4)"
Cohesion: 0.03
Nodes (57): Requirements vocabulary in check_card_requirements, Wild tag (wild_tag_choice), check_card_requirements(), Card requirements section, Wild tag Research Coordination, test_adaptation_technology_relaxes_global_requirements_2_steps(), test_advanced_ecosystems_multi_tag_requirements(), test_anti_gravity_technology_discount_requires_7_science_tags() (+49 more)

### Community 5 - "Tests generales del motor (5)"
Cohesion: 0.04
Nodes (48): use_card_action(), Stormcraft Incorporated card_resource_as_heat, target_card_resource_delta piece, Active cards and use_card_action, test_accion_card_resource_delta_per_tag(), test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_ants_action_moves_microbe_from_another_active_card() (+40 more)

### Community 6 - "Tests generales del motor (6)"
Cohesion: 0.04
Nodes (46): CardRequirementNotMetError, test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production(), test_archaebacteria_requires_max_temperature_minus_18(), test_beam_from_a_thorium_asteroid_requires_jovian_tag_and_gives_heat_and_energy(), test_birds_requires_13_oxygen_and_decreases_plant_production(), test_capital_requires_4_oceans_and_changes_production(), test_check_card_requirements_min_oxygen() (+38 more)

### Community 7 - "Tests generales del motor (7)"
Cohesion: 0.04
Nodes (46): register_active_card(), test_add_resource_to_all_matching_type(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_any_card_resource_action_cost_spends_from_chosen_card(), test_apply_card_effect_choice_threads_target_card_id(), test_atmoscoop_choice_temperature_or_venus_plus_floaters_to_target(), test_cloud_tourism_mc_production_per_earth_venus_pair_action_adds_floater() (+38 more)

### Community 8 - "Tools Supabase (1)"
Cohesion: 0.10
Nodes (24): deal_starting_hand(buy_with_research=True), deal_prelude_hand / keep_preludes, Pharmacy Union + retire_card_as_event, Setup clauses: Celestic 33 floater cards, prelude deal, buy starting hand, Stormcraft card_resource_as_heat, convert_resources(), deal_prelude_hand(), deal_starting_hand() (+16 more)

### Community 9 - "Modelo Board (1)"
Cohesion: 0.10
Nodes (22): _build_adjacency(), _build_hex_defs(), count_adjacent_oceans(), count_adjacent_owned_by(), count_cities_and_special_tiles_adjacent_to_ocean(), count_empty_hexes_adjacent_to_owner(), count_tiles_of_type(), find_nomads() (+14 more)

### Community 10 - "Errores, producción e investigación (1)"
Cohesion: 0.08
Nodes (21): convert_heat_to_temperature(), corporation_first_action_greenery(), GlobalParameterMaxedError, GlobalParameters, place_ocean(), raise_global_parameter_without_bonuses(), raise_oxygen(), raise_temperature() (+13 more)

### Community 11 - "Docs del repo y README desactualizado (1)"
Cohesion: 0.07
Nodes (31): API: /api/players, /api/state/{id}, /api/game, /api/chat, board.py Tharsis hex map module, Board wiring in tools (hex_id params, get_board_state), Chat end-to-end test pending (ANTHROPIC_API_KEY is placeholder), Colonies expansion, Deck/hand/research system, Layer 2: StateGraph always routes through ToolNode, Further frontend iterations (+23 more)

### Community 12 - "Tablero: adyacencias (1)"
Cohesion: 0.11
Nodes (20): can_place_city(), can_place_city_adjacent_to_cities(), get_neighbors(), has_city_adjacent_to_ocean(), place_city_tile(), place_city_tile_adjacent_to_cities(), Inverse board placements, test_can_place_city_adjacent_to_cities_requires_min_count() (+12 more)

### Community 13 - "Errores, producción e investigación (2)"
Cohesion: 0.06
Nodes (19): apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_standard_project_used_bonuses(), compute_research_cost_per_card(), compute_standard_project_discount(), increment_zero_tag_cards_played(), ocean_adjacency_bonus_mc(), PlayerState (+11 more)

### Community 14 - "Tests generales del motor (8)"
Cohesion: 0.06
Nodes (31): CardEffectError, test_accion_requires_zero_resource(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_any_card_resource_rejects_wrong_type_and_insufficient(), test_apply_card_effect_target_card_resource_delta(), test_artificial_photosynthesis_requires_valid_effect_choice(), test_board_of_directors_reveal_cannot_be_played_for_free(), test_card_action_cannot_be_used_twice_same_generation() (+23 more)

### Community 15 - "Turmoil: núcleo político (1)"
Cohesion: 0.15
Nodes (22): can_play_party_gated_card(), compute_influence(), new_turmoil(), place_delegate(), resolve_new_government(), test_can_play_party_gated_card_false_otherwise(), test_can_play_party_gated_card_true_if_ruling(), test_can_play_party_gated_card_true_with_min_delegates() (+14 more)

### Community 16 - "Tools Supabase (2)"
Cohesion: 0.10
Nodes (17): Comprehensive FAQ v1.7 (Jeffrey Anchan), Global Event generation cycle not automated (manual trigger), Global Events track: setup_global_events + Changing Times, resolve_global_event tool, Turmoil Global Events: 36 of 36, _compute_player_influence(), _count_blue_cards_played(), _draw_cards_matching_requirement() (+9 more)

### Community 17 - "Tools Supabase (3)"
Cohesion: 0.14
Nodes (16): Bug: play_prelude never added prelude to played_cards, Prelude block 3: wiring gaps in play_prelude/use_card_action, Punto de retoma 2026-09-09: 10 of 12 pending preludes loaded, _apply_colony_placement_bonus(), _apply_community_build_bonus(), _apply_hex_bonus(), _apply_mars_first_ruling_bonus(), _load_board() (+8 more)

### Community 18 - "package.json frontend (1)"
Cohesion: 0.07
Nodes (24): interTight, metadata, dependencies, lucide-react, next, react, react-dom, name (+16 more)

### Community 19 - "Tablero: greenery y special tiles"
Cohesion: 0.16
Nodes (22): can_place_special_tile(), InvalidPlacementError, new_board(), place_greenery_tile(), place_ocean_tile_on_land(), place_special_tile(), Generic place_special_tile parametrized by requirement, test_can_place_special_tile_requires_matching_hex_bonus() (+14 more)

### Community 20 - "Frontend: chat mockeado (1)"
Cohesion: 0.17
Nodes (23): Home(), readStorage(), skipKey(), writeStorage(), PlayerPicker(), SetupStep, EXAMPLES, Message (+15 more)

### Community 21 - "Errores, producción e investigación (3)"
Cohesion: 0.10
Nodes (19): calculate_card_payment(), convert_plants_to_greenery(), InsufficientResourcesError, plants_per_greenery(), resolve_research_phase(), standard_project_air_scrapping(), standard_project_power_plant(), Polyphemos/TerraLabs starting hand purchase (+11 more)

### Community 22 - "Tests generales del motor (9)"
Cohesion: 0.08
Nodes (22): apply_ruling_bonus(), run_production_phase(), test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production(), test_apply_ruling_bonus_mars_first_pays_per_building_tag(), test_apply_ruling_bonus_reds_raises_tr_only_if_20_or_below(), test_apply_ruling_bonus_scientists_pays_per_science_tag(), test_apply_ruling_bonus_unity_pays_per_venus_earth_jovian_tags() (+14 more)

### Community 23 - "Tablero: adyacencias (2)"
Cohesion: 0.11
Nodes (17): can_place_city_on_volcanic(), can_place_greenery(), can_place_ocean(), can_place_ocean_on_land(), is_hex_empty(), remove_ocean_tile(), UnknownHexError, get_board() (+9 more)

### Community 24 - "Turmoil: núcleo político (2)"
Cohesion: 0.17
Nodes (14): _add_to_party(), _check_party(), exchange_neutral_delegate(), neutral_non_leader_count(), _party_total(), PartyState, _recompute_dominant(), remove_delegate() (+6 more)

### Community 25 - "Tools Supabase (4)"
Cohesion: 0.13
Nodes (13): Colonies mechanic (colonies.py), free_trade gain handled in tools.use_card_action, apply_colony_placed_bonuses(), apply_production_increased_bonus(), snapshot_production_totals(), build_colony(), _load_colonies(), _load_global_parameters() (+5 more)

### Community 26 - "Errores, producción e investigación (4)"
Cohesion: 0.11
Nodes (13): adjust_mc_production(), deal_prelude_hand(), draw_random_preludes(), increment_events_played(), initialize_deck(), keep_preludes(), prelude_draw_candidates(), Prelude own deck (prelude_cards, prelude_review_queue) (+5 more)

### Community 27 - "Tools Supabase (5)"
Cohesion: 0.11
Nodes (13): Bug: cities_delta ignored place_city_tiles (block 32), apply_become_party_leader_bonus(), apply_card_played_vp_icon_bonus(), draw_cards_to_hand(), register_played_card(), resolve_active_card_starting_resources(), _apply_colony_gain(), choose_corporation() (+5 more)

### Community 28 - "Tests generales del motor (10)"
Cohesion: 0.13
Nodes (20): One-use fields pending_mc_discount / pending_requirement_tolerance_steps, Permanent passive effects, apply_tag_played_resource_bonuses(), register_passive_effect(), test_corridors_of_power_roba_al_volverse_party_leader(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_on_hex_bonus_tile_placed_solo_con_el_recurso_pedido() (+12 more)

### Community 29 - "API FastAPI (1)"
Cohesion: 0.20
Nodes (13): BoardResponse, ChatRequest, ChatResponse, ChooseCorporationRequest, CorporationSummary, CreatePlayerRequest, DealHandRequest, GameState (+5 more)

### Community 30 - "Tests generales del motor (11)"
Cohesion: 0.09
Nodes (17): apply_city_placed_bonuses(), apply_hex_bonus_tile_bonuses(), apply_new_distinct_tag_bonuses(), _increase_production(), increment_tags_played(), Corporation block 2 (Ecotec to Manutech), Manutech and _increase_production, Mons Insurance (mostly multiplayer) (+9 more)

### Community 31 - "Tools Supabase (6)"
Cohesion: 0.10
Nodes (18): Colonies Pluto and Europa: catalog 11 of 11, Corporation first actions (effects.first_action, resolve_corporation_first_action), graphify-out graph (always committed, nodes carry status), Bug: _load_player missed 3 columns (KeyError vs real Supabase), Milestones and awards, Neptunian Power Consultants (on_ocean_placed_offer), Nirgal and Philares Effects out of scope by design, pending_ocean_offers + resolve_ocean_offer (+10 more)

### Community 32 - "ui_e2e.py"
Cohesion: 0.12
Nodes (8): api_get(), assert_ui_matches_api(), board_city(), player_id_by_name(), record(), setup_matches_engine(), step(), ui_numbers()

### Community 33 - "Tools Supabase (7)"
Cohesion: 0.12
Nodes (16): action_used reset after reveal_prelude branch, Action choice key is 'choice' not 'options', Play a card within another play/action (Ecology Experts, Board of Directors), Punto de retoma 2026-09-10: prelude catalog complete 70/70, _draw_cards_matching_tag(), _reveal_random_preludes(), use_card_action(), Celestic closed list of 33 floater-icon cards (+8 more)

### Community 34 - "Scripts de mantenimiento del catálogo (1)"
Cohesion: 0.14
Nodes (6): power vs space audit (62 cards, 42 wrong), main(), safe_filename(), build_sheets(), _font(), main()

### Community 35 - "Frontend: chat mockeado (2)"
Cohesion: 0.21
Nodes (16): CreatePlayer(), Dashboard(), GlobalParameters(), PARTY_LABELS, Track(), TRACKS, handleCreate(), Before() (+8 more)

### Community 36 - "Núcleo rules_engine y parámetros"
Cohesion: 0.11
Nodes (17): is_blue_card(), _resolve_capped_counter(), Global Events block 5 multi-agent (22 cards), Global Events block 6 design agents (3 cards), resource_delta_per_capped_counter (cap 5 + Influence), Comprehensive FAQ v1.7, Bug: draw_cards_matching_tag left revealed cards in deck, Dry Deserts (+9 more)

### Community 37 - "Config TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 38 - "Tests generales del motor (12)"
Cohesion: 0.11
Nodes (12): Automa (78 cards) never entered the pipeline, Corporations infrastructure (corporation_cards, choose_corporation, queue), Scope gap: Prelude, Corporation, Automa categories were filtered out, apply_corporation_start(), corporation_first_action_city(), place_city_tile(), standard_project_city(), Global city counter city_tiles_placed (+4 more)

### Community 39 - "GET /state (1)"
Cohesion: 0.24
Nodes (11): chat(), choose_corporation(), deal_preludes(), deal_starting_hand(), get_state(), keep_preludes(), place_tile(), play_prelude() (+3 more)

### Community 40 - "Frontend: chat mockeado (3)"
Cohesion: 0.16
Nodes (17): humanize(), ACTIONS, BONUS_STYLE, BonusMarks(), bonusText(), center(), HEX_POINTS, MarsBoard() (+9 more)

### Community 41 - "Modelo Board (2)"
Cohesion: 0.12
Nodes (15): Arcadian Communities (community TileType), Review blocks 31-38 (promos, CEO set, board markers), Board markers: nomad, cathedral, remove_greenery_tile, Kaguya Tech, Mars Nomads, St Joseph Cathedral, count_cathedrals(), place_cathedral(), remove_greenery_tile(), Board markers (block 37) (+7 more)

### Community 42 - "Grafo LangGraph (1)"
Cohesion: 0.15
Nodes (3): build_graph(), call_model(), AgentState

### Community 43 - "Scripts de mantenimiento del catálogo (2)"
Cohesion: 0.17
Nodes (7): build_image_url_index(), load_site_catalog(), main(), parse_pending_manifest(), connect(), load_corporations(), main()

### Community 44 - "Turmoil: núcleo político (3)"
Cohesion: 0.12
Nodes (15): scripts/apply_db.py (schema + 4 seeds, idempotent), Conventions, SUPABASE_DB_URL password contains @ (use individual psycopg2 params), Development commands, Operational note: Supabase host resolves only via IPv6, normalize_turmoil migrates old turmoil rows automatically, README updated: 412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, Second batch 2026-10-02: official neutral delegates, Stratopolis, README, Supabase migration (+7 more)

### Community 45 - "Card catalog"
Cohesion: 0.12
Nodes (14): Typical catalog errors (requirement read as tag, missing city/space tag, unmarked events, cost from production box, invented effects), Audit result: 81 differences, 78 cards fixed, 3 reference errors (KNOWN_OK), Card catalog (hand-loaded, verified against official scans), No script automates cost/tags/effects decisions, Progress: 408 project cards, 36 Global Events, preludes, queues empty, Audit error patterns (requirement read as tag, missing city/space, 16 unmarked events, cost misread), Block 31 multi-agent batch review, Block 34 multi-agent batch: 4 of 10 reports misread (+6 more)

### Community 46 - "Tools Supabase (8)"
Cohesion: 0.15
Nodes (13): Reds policy resolved at tools.py edge via diff before/after, Punto de retoma 2026-09-10: Turmoil TR Revision, Ruling Bonus, 6 Ruling Policies, Ruling Bonus (6 formulas, one per party), Ruling Policy (Mars First, Greens, Unity, Kelvinists, Scientists, Reds), scientists_policy_used_this_generation flag, TR Revision (-1 TR at each New Government), _apply_production_floor(), _apply_reds_ruling_policy() (+5 more)

### Community 47 - "SetupFlow.tsx"
Cohesion: 0.30
Nodes (15): CardPicker(), CorporationStep(), ErrorLine(), HandStep(), PreludeStep(), SetupFlow(), Stepper(), STEPS (+7 more)

### Community 48 - "audit_catalog.py"
Cohesion: 0.19
Nodes (11): New workflow rule: run audit_catalog.py after touching cards, Audit method: two sources, the scan decides, Branch flow feat/review-block-N chained, choice/tag_count_choice silently ignore sibling keys (early return), Punto de retoma 2026-10-02: full catalog audit (branch feat/auditoria-catalogo), Smoke test vs real Supabase 19/19, tests 718/718, fetch(), load_reference() (+3 more)

### Community 49 - "Turmoil: núcleo político (4)"
Cohesion: 0.15
Nodes (13): changing_times(), setup_global_events(), Changing Times + setup_global_events, global_events.revealed_party/current_party columns (72/72 verified), Official neutral delegate mechanism (14 total, via Global Events), Superseded assumption: 2 fixed neutrals per party, Pendientes section (no rows), T11 Recruitment (+5 more)

### Community 50 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.13
Nodes (15): 81 differences; scan agreed with reference in 78, seed in 3, Run audit_catalog.py after loading new cards, Catalog audit 2026-10-02, choice/tag_count_choice ignore sibling keys, Design decisions kept (Mining Expedition, Hackers, Energy Tapping), Red Appeasement, Mass Converter, Nitrogen-Rich Asteroid fixes, Heavy Taxation corrected (-1 VP), KNOWN_OK: Mining Rights, Mining Area, Pharmacy Union (+7 more)

### Community 51 - "Frontend: chat mockeado (4)"
Cohesion: 0.21
Nodes (12): CardRow(), CardTabs(), KIND_LABEL, Tab, TAG_DOT, Tags(), FIRST_ACTION_TEXT, PendingActions() (+4 more)

### Community 52 - "Errores, producción e investigación (5)"
Cohesion: 0.18
Nodes (9): compute_reserved_card_discount(), duplicate_reserved_card_resources(), release_reserved_card(), reserve_card_in_slot(), reserved_cards slot (Self-Replicating Robots), 210 Self-Replicating Robots, test_duplicate_reserved_card_resources(), test_release_reserved_card() (+1 more)

### Community 53 - "Errores, producción e investigación (6)"
Cohesion: 0.15
Nodes (11): count_distinct_resource_types(), sum_card_resources_by_type(), Block 33 pending: X17 out of scope, X20 unblocked, Diversity Support (X20), Retrofit active_card_resource_type for 11 microbe + 13 animal cards, security_fleet excluded (stores fighters), Stratopolis corrected, Typed card resources (floaters) (+3 more)

### Community 54 - "Errores, producción e investigación (7)"
Cohesion: 0.17
Nodes (10): card_resource_payment passive, spend_active_card_resource(), spend_card_resource_as_heat(), card_resource_payment (Dirigibles, Psychrophiles), Martian Lumber Corp (X60), Payment paths: steel/titanium, card_resource_payment, stock_resource_payment, standard-project card resource, stock_resource_payment (4th payment path, block 36), test_dirigibles_passive_pays_venus_card_with_floaters() (+2 more)

### Community 55 - "Errores, producción e investigación (8)"
Cohesion: 0.20
Nodes (7): CardNotInHandError, player_has_tag_swap_passive(), remove_card_from_hand(), swap_card_for_draw(), test_mars_university_passive_offers_discard_for_draw_on_matching_tag(), test_remove_card_from_hand_raises_if_not_present(), test_swap_card_for_draw_requires_card_in_hand()

### Community 56 - "resolve_ocean_offer"
Cohesion: 0.27
Nodes (11): resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each() (+3 more)

### Community 57 - "Config y cliente Supabase (1)"
Cohesion: 0.17
Nodes (3): Config, Settings, health()

### Community 58 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 59 - "Docs del repo y README desactualizado (2)"
Cohesion: 0.18
Nodes (10): card_review_queue table, CARDS_PENDING_REVIEW.md (deprecated), Supabase data model, download_review_scans.py (2.5s spacing, scan_cache gitignored), Card review queue workflow in Supabase, cards table, global_events table, global_parameters table (+2 more)

### Community 60 - "Errores, producción e investigación (9)"
Cohesion: 0.25
Nodes (9): apply_card_resource_gained_bonuses(), snapshot_card_resource_totals(), Diff before/after snapshot pattern, on_card_resource_gained passive (Meat Industry, Topsoil Contract), test_on_card_resource_gained_ignora_gastos_y_otros_tipos(), test_on_card_resource_gained_no_paga_por_mover_entre_cartas(), test_on_card_resource_gained_own_card_only_solo_cuenta_su_propia_carta(), test_on_card_resource_gained_paga_por_unidad_ganada() (+1 more)

### Community 61 - "Las 3 cartas dudosas (1)"
Cohesion: 0.20
Nodes (7): Air Raid (Colonies) out of scope, Law Suit and Crash Site Cleanup out of scope, Clauses omitted by design (remove from any player, opponent-dependent, VP-only), Loaded cards table (412 project cards), Nirgal Enterprises (out of scope), Out-of-scope by design table (Rover Construction, Herbivores, Air Raid, Law Suit, Crash Site), Verification source: tm.hadronikle.com scans

### Community 62 - "Marcadores: nomads y community"
Cohesion: 0.27
Nodes (6): community_owner(), HexOccupiedError, place_community(), test_community_exige_adyacencia_salvo_la_primera(), test_community_no_va_en_oceano_ni_en_hex_reservado(), test_community_reserva_el_hex_sin_ocuparlo()

### Community 63 - "Turmoil: núcleo político (5)"
Cohesion: 0.20
Nodes (10): Block 31 second batch: 12 more cards, allow_leader, Old pending list: Floating Refinery, Frontier Town, L1 Trade Terminal, Red Appeasement, Venus Shuttles, P74 Frontier Town placement bonus multiplier, P73 Floating Refinery, P78 L1 Trade Terminal, P89 Venus Shuttles, Public Celebrations: VP read as TR (effects {}), trade_bump_track_first N steps (+2 more)

### Community 64 - "Tests generales del motor (13)"
Cohesion: 0.22
Nodes (8): compute_card_cost_discount(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter(), test_earth_office_discount_only_applies_to_earth_tag(), test_mass_converter_discount_does_not_apply_to_non_space_cards(), test_mass_converter_gives_2_mc_discount_on_space_cards(), test_venus_waystation_passive_discounts_venus_tag_cards()

### Community 65 - "First actions de corporaciones"
Cohesion: 0.28
Nodes (6): consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching(), test_celestic_first_action_reveal_until_matching_se_anota_una_sola_vez(), test_consume_corporation_first_action_se_usa_una_sola_vez(), test_register_corporation_first_action_reveal_preludes_conserva_n()

### Community 66 - "Tests generales del motor (14)"
Cohesion: 0.25
Nodes (8): _increase_production single choke-point (Manutech), Manutech corporation (on_production_increased), 4 preludes unblocked (Preservation Program, Suitable Infrastructure, Terraforming Deal, Colony Trade Hub), Pristar order in run_production_phase (read flag before reset), _raise_tr single choke-point for TR changes, Punto de retoma 2026-09-09: corporations 48/48, Vitor corporation (excluded_card_ids list of negative-VP cards), Vitor excluded_card_ids list (now 13 negative-VP cards)

### Community 67 - "Modelo Board (3)"
Cohesion: 0.25
Nodes (6): count_tiles_adjacent_to_ocean(), place_ocean_tile(), Tile placement legality rules (ocean, greenery, city, special), test_count_tiles_adjacent_to_ocean_counts_each_tile_once(), test_place_ocean_tile_on_land_hex_raises(), test_place_ocean_tile_on_occupied_hex_raises()

### Community 69 - "Scripts de mantenimiento del catálogo (3)"
Cohesion: 0.32
Nodes (4): main(), parse_db_url(), read_env_db_url(), README quick start

### Community 70 - "package.json frontend (2)"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 71 - "Tests generales del motor (15)"
Cohesion: 0.29
Nodes (6): apply_event_played_bonuses(), test_media_group_gives_3_mc_when_event_card_is_played(), test_multiple_passive_effects_stack(), test_on_event_played_puede_robar_cartas_con_su_propio_tag_filter(), test_optimal_aerobraking_only_triggers_on_space_events(), test_palladin_shipping_gana_titanio_por_evento_espacial()

### Community 72 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 73 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 74 - "Tests generales del motor (16)"
Cohesion: 0.33
Nodes (5): apply_any_tag_played_choice(), apply_tag_played_choice(), Viral Enhancers on_any_tag_played_choice, test_any_tag_played_choice_target_any_card(), test_olympus_conference_tag_played_choice_add_or_spend()

### Community 75 - "Turmoil: núcleo político (6)"
Cohesion: 0.33
Nodes (5): place_neutral_delegate(), test_exchange_neutral_delegate_puede_volver_leader_al_jugador(), test_jugador_con_mas_delegados_reemplaza_al_leader_neutral(), test_neutral_delegate_con_reserva_vacia_no_hace_nada(), test_neutral_delegate_sale_de_la_reserva_y_puede_ser_leader_y_dominante()

### Community 76 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 77 - "Tests generales del motor (17)"
Cohesion: 0.40
Nodes (4): compute_conversion_rates(), Passive effects vocabulary, test_advanced_alloys_changes_calculate_card_payment_result(), test_advanced_alloys_raises_steel_and_titanium_conversion_rates()

### Community 78 - "Tests generales del motor (18)"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 79 - "Tests generales del motor (19)"
Cohesion: 0.40
Nodes (4): start_research_phase(), test_start_research_phase_draws_fewer_if_deck_is_short(), test_start_research_phase_draws_n_cards_from_deck_top(), test_start_research_phase_fails_if_already_pending()

### Community 81 - "Volcanes y Noctis City"
Cohesion: 0.50
Nodes (3): VOLCANO_NAMES, Lava Flows (VOLCANO_NAMES, hex_id_in), Noctis City reserved hex (id 31)

### Community 82 - "Tests generales del motor (20)"
Cohesion: 0.50
Nodes (3): player_has_optional_energy_to_heat(), optional_energy_to_heat (Supercapacitors), Supercapacitors (X46)

### Community 83 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 84 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 86 - "Punto de retoma 2026-09-10: T11 Recruitm"
Cohesion: 0.67
Nodes (3): Orphan PR problem (recovery PR #56 merged immediately), Pending table in CARDS_LOG empty, Punto de retoma 2026-09-10: T11 Recruitment loaded

### Community 87 - "Stack: Python, LangGraph, FastAPI, Supab"
Cohesion: 0.67
Nodes (3): Repo structure, supabase>=2.8.0 required for new API key format, Stack: Python, LangGraph, FastAPI, Supabase, Next.js, Docker

## Knowledge Gaps
- **209 isolated node(s):** `Bug: cities_delta ignored place_city_tiles (block 32)`, `Smoke-test bug block 32: cities_delta ignoring place_city_tiles`, `Prelude block 3: wiring gaps in play_prelude/use_card_action`, `Stormcraft card_resource_as_heat`, `Viral Enhancers on_any_tag_played_choice` (+204 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 538 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `apply_card_effect()` connect `Tests generales del motor (2)` to `Tests generales del motor (1)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Errores, producción e investigación (1)`, `Errores, producción e investigación (2)`, `Tests generales del motor (8)`, `Tools Supabase (2)`, `Tools Supabase (3)`, `Errores, producción e investigación (3)`, `Tests generales del motor (9)`, `Errores, producción e investigación (4)`, `Tools Supabase (5)`, `Tests generales del motor (11)`, `Núcleo rules_engine y parámetros`, `Tests generales del motor (12)`, `Tools Supabase (8)`, `audit_catalog.py`, `Corporaciones: mecánicas resueltas`, `Errores, producción e investigación (6)`, `Errores, producción e investigación (8)`, `Las 3 cartas dudosas (1)`, `Tests generales del motor (19)`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `play_card()` connect `Tools Supabase (5)` to `Colonies: colonias, Pluto/Europa y descartes`, `Tests generales del motor (2)`, `Tests generales del motor (4)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Tools Supabase (1)`, `Modelo Board (1)`, `Errores, producción e investigación (1)`, `Tablero: adyacencias (1)`, `Errores, producción e investigación (2)`, `Turmoil: núcleo político (1)`, `Tools Supabase (2)`, `Tools Supabase (3)`, `Tablero: greenery y special tiles`, `Errores, producción e investigación (3)`, `Tablero: adyacencias (2)`, `Turmoil: núcleo político (2)`, `Tools Supabase (4)`, `Errores, producción e investigación (4)`, `Tests generales del motor (10)`, `Tests generales del motor (11)`, `Tools Supabase (7)`, `Tests generales del motor (12)`, `Modelo Board (2)`, `Tools Supabase (8)`, `Errores, producción e investigación (5)`, `Errores, producción e investigación (7)`, `Errores, producción e investigación (8)`, `Errores, producción e investigación (9)`, `Tests generales del motor (13)`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `Tests generales del motor (17)`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `new_player_state()` connect `Tests generales del motor (1)` to `Colonies: colonias, Pluto/Europa y descartes`, `Tests generales del motor (2)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Errores, producción e investigación (1)`, `Errores, producción e investigación (2)`, `Tests generales del motor (8)`, `Tablero: greenery y special tiles`, `Errores, producción e investigación (3)`, `Tests generales del motor (9)`, `Errores, producción e investigación (4)`, `Tests generales del motor (10)`, `Tests generales del motor (11)`, `Tests generales del motor (12)`, `Errores, producción e investigación (5)`, `Errores, producción e investigación (6)`, `Errores, producción e investigación (7)`, `Errores, producción e investigación (8)`, `resolve_ocean_offer`, `Errores, producción e investigación (9)`, `Tests generales del motor (13)`, `First actions de corporaciones`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `Tests generales del motor (17)`, `Tests generales del motor (18)`, `Tests generales del motor (19)`, `_stratopolis_player()`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **What connects `Bug: cities_delta ignored place_city_tiles (block 32)`, `Smoke-test bug block 32: cities_delta ignoring place_city_tiles`, `Prelude block 3: wiring gaps in play_prelude/use_card_action` to the rest of the system?**
  _209 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.030281007751937983 - nodes in this community are weakly interconnected._
- **Should `Colonies: colonias, Pluto/Europa y descartes` be split into smaller, more focused modules?**
  _Cohesion score 0.060759493670886074 - nodes in this community are weakly interconnected._
- **Should `Tests generales del motor (2)` be split into smaller, more focused modules?**
  _Cohesion score 0.02857142857142857 - nodes in this community are weakly interconnected._