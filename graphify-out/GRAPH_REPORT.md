# Graph Report - arbiter-mars  (2026-10-03)

## Corpus Check
- 60 files · ~186,848 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1792 nodes · 5541 edges · 118 communities (76 shown, 42 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 276 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor (1)
- Tests generales del motor (2)
- Colonies: colonias, Pluto/Europa y descartes
- Errores, producción e investigación (1)
- Tools Supabase (1)
- Tests generales del motor (3)
- Tools Supabase (2)
- Tests generales del motor (4)
- Tests generales del motor (5)
- Tests generales del motor (6)
- Errores, producción e investigación (2)
- Tests generales del motor (7)
- Docs del repo y README desactualizado (1)
- Errores, producción e investigación (3)
- Modelo Board (1)
- Tests generales del motor (8)
- Tablero: adyacencias (1)
- Tablero: greenery y special tiles (1)
- Tests generales del motor (9)
- Tablero: adyacencias (2)
- Errores, producción e investigación (4)
- Tests generales del motor (10)
- Turmoil: núcleo político (1)
- Tools Supabase (3)
- Errores, producción e investigación (5)
- Turmoil: núcleo político (2)
- Núcleo rules_engine y parámetros
- Turmoil: núcleo político (3)
- Config TypeScript
- Grafo LangGraph (1)
- Scripts de mantenimiento del catálogo (1)
- package.json frontend (1)
- Turmoil: núcleo político (4)
- Card catalog
- Modelo Board (2)
- audit_catalog.py
- Tests generales del motor (11)
- First actions de corporaciones
- Corporaciones: mecánicas resueltas
- Turmoil: núcleo político (5)
- ui_e2e.py
- API FastAPI (routes/schemas) (1)
- Tests generales del motor (12)
- Frontend: chat mockeado (1)
- Marcadores: nomads y community (1)
- Frontend: chat mockeado (2)
- Tablero: greenery y special tiles (2)
- resolve_ocean_offer
- Schema y base de datos
- Scripts de mantenimiento del catálogo (2)
- Docs del repo y README desactualizado (2)
- Las 3 cartas dudosas (1)
- Marcadores: nomads y community (2)
- Tools Supabase (4)
- Scripts de mantenimiento del catálogo (3)
- Turmoil: Ruling Bonus y TR Revision (1)
- Tests generales del motor (13)
- Config y cliente Supabase
- GET /state (1)
- Scripts de mantenimiento del catálogo (4)
- package.json frontend (2)
- Tests generales del motor (14)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- Entry point FastAPI
- Frontend: chat mockeado (3)
- Fuentes del mapa Tharsis
- Tests generales del motor (15)
- Tests generales del motor (16)
- Turmoil: Ruling Bonus y TR Revision (2)
- Turmoil: núcleo político (6)
- API FastAPI (routes/schemas) (2)
- Frontend: chat mockeado (4)
- package.json frontend (3)
- Volcanes y Noctis City
- _stratopolis_player()
- Tests ruling_or_delegates
- Frontend: chat mockeado (5)
- Docs del repo y README desactualizado (3)
- resolve_global_event tool
- Punto de retoma 2026-09-10: T11 Recruitm
- Stack: Python, LangGraph, FastAPI, Supab
- next.config
- Diversity Support
- Tests generales del motor (17)
- Adyacencia precalculada
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
8. `PlayerState` - 96 edges
9. `register_passive_effect()` - 95 edges
10. `play_card()` - 82 edges

## Surprising Connections (you probably didn't know these)
- `Old tech debt: T11 fixed 2 neutrals per party (superseded)` --references--> `exchange_neutral_delegate()`  [INFERRED]
  AGENTS.md → backend/app/agent/turmoil.py
- `Hex board scope decision 2026-08-31` --semantically_similar_to--> `Hex board Tharsis: 61 hexes, 12 reserved ocean, Noctis, 4 volcanic`  [INFERRED] [semantically similar]
  backend/app/db/CARDS_LOG.md → AGENTS.md
- `Permanent passive effects` --references--> `register_passive_effect()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `Golden rule: do not discard cards for lack of mechanics` --references--> `apply_card_effect()`  [INFERRED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `choice/tag_count_choice silently ignore sibling keys (early return)` --references--> `apply_card_effect()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py

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

## Communities (118 total, 42 thin omitted)

### Community 0 - "Tests generales del motor (1)"
Cohesion: 0.03
Nodes (131): Extensible effects vocabulary in apply_card_effect, apply_card_effect(), new_global_parameters(), effects vocabulary reference section, test_acquired_company_gives_plus_3_mc_production(), test_apply_card_effect_with_no_effects_is_a_noop(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_asteroid_card_raises_temperature_and_gives_titanium() (+123 more)

### Community 1 - "Tests generales del motor (2)"
Cohesion: 0.03
Nodes (123): new_player_state(), test_adapted_lichen_gives_plus_1_plant_production(), test_apply_corporation_start_pone_produccion_en_cero(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production(), test_apply_ruling_bonus_mars_first_pays_per_building_tag(), test_apply_ruling_bonus_reds_raises_tr_only_if_20_or_below(), test_apply_ruling_bonus_scientists_pays_per_science_tag(), test_aquifer_costs_18_mc_places_ocean_and_1_tr() (+115 more)

### Community 2 - "Colonies: colonias, Pluto/Europa y descartes"
Cohesion: 0.06
Nodes (51): add_colony_tile(), adjust_colony_track(), build_colony(), ColonyDef, ColonyFullError, ColonyOccupiedError, ColonyTileState, new_colonies() (+43 more)

### Community 3 - "Errores, producción e investigación (1)"
Cohesion: 0.04
Nodes (42): adjust_mc_production(), apply_card_played_vp_icon_bonus(), apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_standard_project_used_bonuses(), compute_research_cost_per_card(), compute_standard_project_discount(), convert_heat_to_temperature() (+34 more)

### Community 4 - "Tools Supabase (1)"
Cohesion: 0.08
Nodes (36): Bug: play_prelude never added prelude to played_cards, Prelude block 3: wiring gaps in play_prelude/use_card_action, Punto de retoma 2026-09-09: 10 of 12 pending preludes loaded, Stormcraft card_resource_as_heat, apply_production_increased_bonus(), snapshot_production_totals(), _apply_colony_placement_bonus(), _apply_community_build_bonus() (+28 more)

### Community 5 - "Tests generales del motor (3)"
Cohesion: 0.03
Nodes (57): Requirements vocabulary in check_card_requirements, Wild tag (wild_tag_choice), check_card_requirements(), Card requirements section, Wild tag Research Coordination, test_adaptation_technology_relaxes_global_requirements_2_steps(), test_advanced_ecosystems_multi_tag_requirements(), test_anti_gravity_technology_discount_requires_7_science_tags() (+49 more)

### Community 6 - "Tools Supabase (2)"
Cohesion: 0.06
Nodes (39): deal_starting_hand(buy_with_research=True), Colonies Pluto and Europa: catalog 11 of 11, deal_prelude_hand / keep_preludes, Corporation first actions (effects.first_action, resolve_corporation_first_action), graphify-out graph (always committed, nodes carry status), Bug: _load_player missed 3 columns (KeyError vs real Supabase), Milestones and awards, Neptunian Power Consultants (on_ocean_placed_offer) (+31 more)

### Community 7 - "Tests generales del motor (4)"
Cohesion: 0.04
Nodes (48): use_card_action(), Stormcraft Incorporated card_resource_as_heat, target_card_resource_delta piece, Active cards and use_card_action, test_accion_card_resource_delta_per_tag(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_any_card_resource_action_cost_spends_from_chosen_card(), test_atmo_collectors_action_choice_add_or_spend_for_titanium_energy_heat() (+40 more)

### Community 8 - "Tests generales del motor (5)"
Cohesion: 0.04
Nodes (47): register_active_card(), test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_add_resource_to_all_matching_type(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_ants_action_moves_microbe_from_another_active_card(), test_apply_card_effect_choice_threads_target_card_id(), test_aquifer_pumping_action_spends_mc_for_ocean() (+39 more)

### Community 9 - "Tests generales del motor (6)"
Cohesion: 0.04
Nodes (46): CardRequirementNotMetError, test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production(), test_archaebacteria_requires_max_temperature_minus_18(), test_beam_from_a_thorium_asteroid_requires_jovian_tag_and_gives_heat_and_energy(), test_birds_requires_13_oxygen_and_decreases_plant_production(), test_capital_requires_4_oceans_and_changes_production(), test_check_card_requirements_min_oxygen() (+38 more)

### Community 10 - "Errores, producción e investigación (2)"
Cohesion: 0.06
Nodes (25): Bug: cities_delta ignored place_city_tiles (block 32), apply_any_tag_played_choice(), apply_become_party_leader_bonus(), apply_colony_placed_bonuses(), apply_hex_bonus_tile_bonuses(), apply_new_distinct_tag_bonuses(), _apply_production_floor(), apply_tag_played_choice() (+17 more)

### Community 11 - "Tests generales del motor (7)"
Cohesion: 0.06
Nodes (35): CardEffectError, duplicate_reserved_card_resources(), reserve_card_in_slot(), test_accion_requires_zero_resource(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_any_card_resource_rejects_wrong_type_and_insufficient(), test_apply_card_effect_target_card_resource_delta(), test_artificial_photosynthesis_requires_valid_effect_choice() (+27 more)

### Community 12 - "Docs del repo y README desactualizado (1)"
Cohesion: 0.06
Nodes (34): action_used reset after reveal_prelude branch, API: /api/players, /api/state/{id}, /api/game, /api/chat, board.py Tharsis hex map module, Board wiring in tools (hex_id params, get_board_state), Chat end-to-end test pending (ANTHROPIC_API_KEY is placeholder), Colonies expansion, Deck/hand/research system, Layer 2: StateGraph always routes through ToolNode (+26 more)

### Community 13 - "Errores, producción e investigación (3)"
Cohesion: 0.07
Nodes (27): card_resource_payment passive, Reds policy resolved at tools.py edge via diff before/after, Ruling Policy (Mars First, Greens, Unity, Kelvinists, Scientists, Reds), scientists_policy_used_this_generation flag, InsufficientResourcesError, resolve_research_phase(), spend_active_card_resource(), spend_card_resource_as_heat() (+19 more)

### Community 14 - "Modelo Board (1)"
Cohesion: 0.12
Nodes (18): _build_adjacency(), _build_hex_defs(), count_adjacent_oceans(), count_adjacent_owned_by(), count_empty_hexes_adjacent_to_owner(), count_tiles_adjacent_to_ocean(), get_adjacent_tiles(), HexDef (+10 more)

### Community 15 - "Tests generales del motor (8)"
Cohesion: 0.08
Nodes (23): _increase_production single choke-point (Manutech), Manutech corporation (on_production_increased), 4 preludes unblocked (Preservation Program, Suitable Infrastructure, Terraforming Deal, Colony Trade Hub), Pristar order in run_production_phase (read flag before reset), _raise_tr single choke-point for TR changes, Punto de retoma 2026-09-09: corporations 48/48, Vitor corporation (excluded_card_ids list of negative-VP cards), Vitor excluded_card_ids list (now 13 negative-VP cards) (+15 more)

### Community 16 - "Tablero: adyacencias (1)"
Cohesion: 0.11
Nodes (18): can_place_city_adjacent_to_cities(), can_place_ocean(), can_place_ocean_on_land(), is_hex_empty(), place_ocean_tile(), remove_ocean_tile(), UnknownHexError, get_board_state() (+10 more)

### Community 17 - "Tablero: greenery y special tiles (1)"
Cohesion: 0.15
Nodes (20): can_place_greenery(), can_place_special_tile(), count_cities_and_special_tiles_adjacent_to_ocean(), new_board(), place_greenery_tile(), place_special_tile(), Generic place_special_tile parametrized by requirement, test_can_place_special_tile_requires_matching_hex_bonus() (+12 more)

### Community 18 - "Tests generales del motor (9)"
Cohesion: 0.08
Nodes (21): place_ocean(), raise_temperature(), _raise_tr(), retire_card_as_event(), test_multiple_ocean_placements_trigger_passive_each_time(), test_on_ocean_placed_acepta_production_deltas(), test_on_temperature_raised_no_paga_pasos_no_aplicados(), test_on_temperature_raised_paga_por_paso_aplicado() (+13 more)

### Community 19 - "Tablero: adyacencias (2)"
Cohesion: 0.14
Nodes (13): can_place_city(), can_place_city_on_volcanic(), count_cathedrals(), has_city_adjacent_to_ocean(), place_city_tile(), test_can_place_city_on_volcanic_ignores_city_adjacency(), test_can_place_city_on_volcanic_rejects_non_volcanic_hex(), test_cannot_place_city_adjacent_to_another_city() (+5 more)

### Community 20 - "Errores, producción e investigación (4)"
Cohesion: 0.11
Nodes (20): apply_card_resource_gained_bonuses(), count_distinct_resource_types(), snapshot_card_resource_totals(), sum_card_resources_by_type(), Block 33 pending: X17 out of scope, X20 unblocked, Diff before/after snapshot pattern, Diversity Support (X20), Retrofit active_card_resource_type for 11 microbe + 13 animal cards (+12 more)

### Community 21 - "Tests generales del motor (10)"
Cohesion: 0.12
Nodes (22): apply_tag_played_resource_bonuses(), register_passive_effect(), test_corridors_of_power_roba_al_volverse_party_leader(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_olympus_conference_tag_played_choice_add_or_spend(), test_on_cost_threshold_paid_usa_el_costo_basico(), test_on_tag_played_mc_delta_counts_each_matching_tag() (+14 more)

### Community 22 - "Turmoil: núcleo político (1)"
Cohesion: 0.17
Nodes (14): _add_to_party(), _check_party(), exchange_neutral_delegate(), neutral_non_leader_count(), _party_total(), PartyState, _recompute_dominant(), remove_delegate() (+6 more)

### Community 23 - "Tools Supabase (3)"
Cohesion: 0.10
Nodes (16): Action choice key is 'choice' not 'options', Colonies mechanic (colonies.py), free_trade gain handled in tools.use_card_action, prelude_draw_candidates(), start_prelude_draw(), take_pending_prelude(), _draw_cards_matching_tag(), _reveal_random_preludes() (+8 more)

### Community 24 - "Errores, producción e investigación (5)"
Cohesion: 0.11
Nodes (15): CardNotInHandError, GlobalParameterMaxedError, raise_global_parameter_without_bonuses(), raise_venus(), remove_card_from_hand(), swap_card_for_draw(), Bug: play_prelude registered passive twice, Prelude block 3 active preludes (+7 more)

### Community 25 - "Turmoil: núcleo político (2)"
Cohesion: 0.16
Nodes (18): compute_influence(), new_turmoil(), place_delegate(), resolve_new_government(), test_compute_influence_adds_card_bonus_and_can_exceed_3(), test_compute_influence_chairman_bonus(), test_compute_influence_dominant_party_leader_vs_non_leader_delegate(), test_dominant_party_shifts_only_on_strictly_more_delegates() (+10 more)

### Community 26 - "Núcleo rules_engine y parámetros"
Cohesion: 0.11
Nodes (17): is_blue_card(), _resolve_capped_counter(), Global Events block 5 multi-agent (22 cards), Global Events block 6 design agents (3 cards), resource_delta_per_capped_counter (cap 5 + Influence), Comprehensive FAQ v1.7, Bug: draw_cards_matching_tag left revealed cards in deck, Dry Deserts (+9 more)

### Community 27 - "Turmoil: núcleo político (3)"
Cohesion: 0.19
Nodes (13): changing_times(), place_neutral_delegate(), setup_global_events(), Changing Times + setup_global_events, test_changing_times_avanza_el_track_y_reparte_neutrales(), test_changing_times_con_mazo_vacio_deja_distant_vacia(), test_exchange_neutral_delegate_puede_volver_leader_al_jugador(), test_jugador_con_mas_delegados_reemplaza_al_leader_neutral() (+5 more)

### Community 28 - "Config TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 29 - "Grafo LangGraph (1)"
Cohesion: 0.15
Nodes (3): build_graph(), call_model(), AgentState

### Community 30 - "Scripts de mantenimiento del catálogo (1)"
Cohesion: 0.17
Nodes (7): build_image_url_index(), load_site_catalog(), main(), parse_pending_manifest(), connect(), load_corporations(), main()

### Community 31 - "package.json frontend (1)"
Cohesion: 0.12
Nodes (16): dependencies, next, react, react-dom, name, private, version, autoprefixer (+8 more)

### Community 32 - "Turmoil: núcleo político (4)"
Cohesion: 0.12
Nodes (15): scripts/apply_db.py (schema + 4 seeds, idempotent), Conventions, SUPABASE_DB_URL password contains @ (use individual psycopg2 params), Development commands, Operational note: Supabase host resolves only via IPv6, normalize_turmoil migrates old turmoil rows automatically, README updated: 412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, Second batch 2026-10-02: official neutral delegates, Stratopolis, README, Supabase migration (+7 more)

### Community 33 - "Card catalog"
Cohesion: 0.12
Nodes (14): Typical catalog errors (requirement read as tag, missing city/space tag, unmarked events, cost from production box, invented effects), Audit result: 81 differences, 78 cards fixed, 3 reference errors (KNOWN_OK), Card catalog (hand-loaded, verified against official scans), No script automates cost/tags/effects decisions, Progress: 408 project cards, 36 Global Events, preludes, queues empty, Audit error patterns (requirement read as tag, missing city/space, 16 unmarked events, cost misread), Block 31 multi-agent batch review, Block 34 multi-agent batch: 4 of 10 reports misread (+6 more)

### Community 34 - "Modelo Board (2)"
Cohesion: 0.14
Nodes (13): Arcadian Communities (community TileType), Review blocks 31-38 (promos, CEO set, board markers), Board markers: nomad, cathedral, remove_greenery_tile, Kaguya Tech, Mars Nomads, St Joseph Cathedral, place_cathedral(), remove_greenery_tile(), Board markers (block 37), Overlay cathedral marker on city HexState (+5 more)

### Community 35 - "audit_catalog.py"
Cohesion: 0.19
Nodes (11): New workflow rule: run audit_catalog.py after touching cards, Audit method: two sources, the scan decides, Branch flow feat/review-block-N chained, choice/tag_count_choice silently ignore sibling keys (early return), Punto de retoma 2026-10-02: full catalog audit (branch feat/auditoria-catalogo), Smoke test vs real Supabase 19/19, tests 718/718, fetch(), load_reference() (+3 more)

### Community 36 - "Tests generales del motor (11)"
Cohesion: 0.15
Nodes (10): Automa (78 cards) never entered the pipeline, Corporations infrastructure (corporation_cards, choose_corporation, queue), Scope gap: Prelude, Corporation, Automa categories were filtered out, apply_corporation_start(), register_played_card(), choose_corporation(), Corporations block 1 (Aphrodite to EcoLine), Corporation blocks 3-5: 41 of 48 (+2 more)

### Community 37 - "First actions de corporaciones"
Cohesion: 0.16
Nodes (12): consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching(), Celestic closed list of 33 floater-icon cards, Corporation first actions resolved (Philares, Tharsis, Aridor, Poseidon, Arcadian), Valley Trust first action reveal_preludes, test_celestic_first_action_reveal_until_matching_se_anota_una_sola_vez(), test_consume_corporation_first_action_se_usa_una_sola_vez() (+4 more)

### Community 38 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.13
Nodes (15): 81 differences; scan agreed with reference in 78, seed in 3, Run audit_catalog.py after loading new cards, Catalog audit 2026-10-02, choice/tag_count_choice ignore sibling keys, Design decisions kept (Mining Expedition, Hackers, Energy Tapping), Red Appeasement, Mass Converter, Nitrogen-Rich Asteroid fixes, Heavy Taxation corrected (-1 VP), KNOWN_OK: Mining Rights, Mining Area, Pharmacy Union (+7 more)

### Community 39 - "Turmoil: núcleo político (5)"
Cohesion: 0.13
Nodes (15): Block 31 second batch: 12 more cards, allow_leader, Old pending list: Floating Refinery, Frontier Town, L1 Trade Terminal, Red Appeasement, Venus Shuttles, P74 Frontier Town placement bonus multiplier, global_events.revealed_party/current_party columns (72/72 verified), Official neutral delegate mechanism (14 total, via Global Events), Superseded assumption: 2 fixed neutrals per party, P73 Floating Refinery, P78 L1 Trade Terminal (+7 more)

### Community 40 - "ui_e2e.py"
Cohesion: 0.17
Nodes (6): api_get(), assert_ui_matches_api(), player_id_by_name(), record(), step(), ui_numbers()

### Community 41 - "API FastAPI (routes/schemas) (1)"
Cohesion: 0.26
Nodes (6): ChatRequest, ChatResponse, CreatePlayerRequest, GameState, PlayerStateResponse, PlayerSummary

### Community 42 - "Tests generales del motor (12)"
Cohesion: 0.14
Nodes (12): calculate_card_payment(), compute_conversion_rates(), Passive effects vocabulary, test_advanced_alloys_changes_calculate_card_payment_result(), test_advanced_alloys_raises_steel_and_titanium_conversion_rates(), test_calculate_card_payment_exact_mc(), test_calculate_card_payment_insufficient_raises(), test_calculate_card_payment_overpaying_gives_no_refund_but_no_error() (+4 more)

### Community 43 - "Frontend: chat mockeado (1)"
Cohesion: 0.22
Nodes (11): CardList(), Dashboard(), GlobalParameters(), humanize(), PARAMETERS, PARTY_LABELS, ResourcePanel(), RESOURCES (+3 more)

### Community 44 - "Marcadores: nomads y community (1)"
Cohesion: 0.19
Nodes (10): count_tiles_of_type(), find_nomads(), get_neighbors(), move_nomads(), test_corner_hex_has_3_neighbors(), test_count_empty_hexes_adjacent_to_owner_counts_each_hex_once(), test_count_tiles_of_type_and_owner(), test_get_neighbors_unknown_hex_raises() (+2 more)

### Community 45 - "Frontend: chat mockeado (2)"
Cohesion: 0.37
Nodes (10): Home(), PlayerPicker(), handleCreate(), ChatResponse, createPlayer(), getGame(), getPlayerState(), listPlayers() (+2 more)

### Community 46 - "Tablero: greenery y special tiles (2)"
Cohesion: 0.23
Nodes (9): InvalidPlacementError, place_city_tile_adjacent_to_cities(), place_ocean_tile_on_land(), Inverse board placements, test_place_city_tile_adjacent_to_cities_illegal_raises(), test_place_city_tile_adjacent_to_cities_succeeds_when_legal(), test_place_ocean_tile_on_land_occupies_hex_as_ocean(), test_place_ocean_tile_on_land_rejects_noctis_city_hex() (+1 more)

### Community 47 - "resolve_ocean_offer"
Cohesion: 0.27
Nodes (11): resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each() (+3 more)

### Community 48 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 50 - "Docs del repo y README desactualizado (2)"
Cohesion: 0.18
Nodes (10): card_review_queue table, CARDS_PENDING_REVIEW.md (deprecated), Supabase data model, download_review_scans.py (2.5s spacing, scan_cache gitignored), Card review queue workflow in Supabase, cards table, global_events table, global_parameters table (+2 more)

### Community 51 - "Las 3 cartas dudosas (1)"
Cohesion: 0.20
Nodes (7): Air Raid (Colonies) out of scope, Law Suit and Crash Site Cleanup out of scope, Clauses omitted by design (remove from any player, opponent-dependent, VP-only), Loaded cards table (412 project cards), Nirgal Enterprises (out of scope), Out-of-scope by design table (Rover Construction, Herbivores, Air Raid, Law Suit, Crash Site), Verification source: tm.hadronikle.com scans

### Community 52 - "Marcadores: nomads y community (2)"
Cohesion: 0.27
Nodes (6): community_owner(), HexOccupiedError, place_community(), test_community_exige_adyacencia_salvo_la_primera(), test_community_no_va_en_oceano_ni_en_hex_reservado(), test_community_reserva_el_hex_sin_ocuparlo()

### Community 53 - "Tools Supabase (4)"
Cohesion: 0.28
Nodes (6): Global Event generation cycle not automated (manual trigger), Global Events track: setup_global_events + Changing Times, _load_global_event_parties(), resolve_new_government(), _save_turmoil(), setup_global_events()

### Community 54 - "Scripts de mantenimiento del catálogo (3)"
Cohesion: 0.28
Nodes (4): power vs space audit (62 cards, 42 wrong), build_sheets(), _font(), main()

### Community 55 - "Turmoil: Ruling Bonus y TR Revision (1)"
Cohesion: 0.22
Nodes (8): Punto de retoma 2026-09-10: Turmoil TR Revision, Ruling Bonus, 6 Ruling Policies, Ruling Bonus (6 formulas, one per party), TR Revision (-1 TR at each New Government), apply_ruling_bonus(), Ruling Bonus per party, test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_unity_pays_per_venus_earth_jovian_tags(), test_apply_ruling_bonus_unknown_party_raises()

### Community 56 - "Tests generales del motor (13)"
Cohesion: 0.22
Nodes (8): compute_card_cost_discount(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter(), test_earth_office_discount_only_applies_to_earth_tag(), test_mass_converter_discount_does_not_apply_to_non_space_cards(), test_mass_converter_gives_2_mc_discount_on_space_cards(), test_venus_waystation_passive_discounts_venus_tag_cards()

### Community 58 - "GET /state (1)"
Cohesion: 0.25
Nodes (4): _card_catalog(), get_state(), list_players(), _player_or_404()

### Community 59 - "Scripts de mantenimiento del catálogo (4)"
Cohesion: 0.32
Nodes (4): main(), parse_db_url(), read_env_db_url(), README quick start

### Community 60 - "package.json frontend (2)"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 61 - "Tests generales del motor (14)"
Cohesion: 0.29
Nodes (6): apply_event_played_bonuses(), test_media_group_gives_3_mc_when_event_card_is_played(), test_multiple_passive_effects_stack(), test_on_event_played_puede_robar_cartas_con_su_propio_tag_filter(), test_optimal_aerobraking_only_triggers_on_space_events(), test_palladin_shipping_gana_titanio_por_evento_espacial()

### Community 62 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 63 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 65 - "Frontend: chat mockeado (3)"
Cohesion: 0.47
Nodes (5): EXAMPLES, Message, SidebarChat(), send(), sendChatMessage()

### Community 66 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 67 - "Tests generales del motor (15)"
Cohesion: 0.40
Nodes (4): apply_city_placed_bonuses(), test_pets_starts_with_1_animal_and_reacts_to_city_tiles(), test_tharsis_first_action_city_gratis_sin_produccion_del_proyecto_estandar(), test_tharsis_republic_gana_mc_al_colocarse_una_ciudad()

### Community 68 - "Tests generales del motor (16)"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 69 - "Turmoil: Ruling Bonus y TR Revision (2)"
Cohesion: 0.40
Nodes (4): start_research_phase(), test_start_research_phase_draws_fewer_if_deck_is_short(), test_start_research_phase_draws_n_cards_from_deck_top(), test_start_research_phase_fails_if_already_pending()

### Community 70 - "Turmoil: núcleo político (6)"
Cohesion: 0.40
Nodes (4): can_play_party_gated_card(), test_can_play_party_gated_card_false_otherwise(), test_can_play_party_gated_card_true_if_ruling(), test_can_play_party_gated_card_true_with_min_delegates()

### Community 73 - "package.json frontend (3)"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 74 - "Volcanes y Noctis City"
Cohesion: 0.50
Nodes (3): VOLCANO_NAMES, Lava Flows (VOLCANO_NAMES, hex_id_in), Noctis City reserved hex (id 31)

### Community 75 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 76 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 77 - "Frontend: chat mockeado (5)"
Cohesion: 0.50
Nodes (3): KIND_LABEL, ActiveCard, CardInfo

### Community 79 - "resolve_global_event tool"
Cohesion: 0.67
Nodes (3): Comprehensive FAQ v1.7 (Jeffrey Anchan), resolve_global_event tool, Turmoil Global Events: 36 of 36

### Community 80 - "Punto de retoma 2026-09-10: T11 Recruitm"
Cohesion: 0.67
Nodes (3): Orphan PR problem (recovery PR #56 merged immediately), Pending table in CARDS_LOG empty, Punto de retoma 2026-09-10: T11 Recruitment loaded

### Community 81 - "Stack: Python, LangGraph, FastAPI, Supab"
Cohesion: 0.67
Nodes (3): Repo structure, supabase>=2.8.0 required for new API key format, Stack: Python, LangGraph, FastAPI, Supabase, Next.js, Docker

## Knowledge Gaps
- **197 isolated node(s):** `Hellas/Elysium alternative maps`, `Expansions covered: Base, Corporate Era, Venus Next, Colonies, Prelude, Turmoil, Promo`, `README next iteration: frontend`, `README status table (412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, 715 tests)`, `Generic place_special_tile parametrized by requirement` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 514 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `apply_card_effect()` connect `Tests generales del motor (1)` to `Tests generales del motor (2)`, `Errores, producción e investigación (1)`, `Tools Supabase (1)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Errores, producción e investigación (2)`, `Tests generales del motor (7)`, `Errores, producción e investigación (3)`, `Tests generales del motor (9)`, `Errores, producción e investigación (4)`, `Errores, producción e investigación (5)`, `Núcleo rules_engine y parámetros`, `audit_catalog.py`, `Tests generales del motor (11)`, `Corporaciones: mecánicas resueltas`, `Las 3 cartas dudosas (1)`, `Turmoil: Ruling Bonus y TR Revision (2)`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `play_card()` connect `Errores, producción e investigación (2)` to `Tests generales del motor (1)`, `Colonies: colonias, Pluto/Europa y descartes`, `Errores, producción e investigación (1)`, `Tools Supabase (1)`, `Tests generales del motor (3)`, `Tools Supabase (2)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Errores, producción e investigación (3)`, `Modelo Board (1)`, `Tablero: adyacencias (1)`, `Tablero: greenery y special tiles (1)`, `Tablero: adyacencias (2)`, `Errores, producción e investigación (4)`, `Tests generales del motor (10)`, `Turmoil: núcleo político (1)`, `Tools Supabase (3)`, `Errores, producción e investigación (5)`, `Turmoil: núcleo político (2)`, `Modelo Board (2)`, `Tests generales del motor (11)`, `Tests generales del motor (12)`, `Marcadores: nomads y community (1)`, `Tablero: greenery y special tiles (2)`, `Tools Supabase (4)`, `Tests generales del motor (13)`, `Tests generales del motor (14)`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `new_player_state()` connect `Tests generales del motor (2)` to `Tests generales del motor (1)`, `Colonies: colonias, Pluto/Europa y descartes`, `Errores, producción e investigación (1)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Errores, producción e investigación (2)`, `Tests generales del motor (7)`, `Errores, producción e investigación (3)`, `Tests generales del motor (8)`, `Tests generales del motor (9)`, `Errores, producción e investigación (4)`, `Tests generales del motor (10)`, `Errores, producción e investigación (5)`, `First actions de corporaciones`, `Tests generales del motor (12)`, `resolve_ocean_offer`, `Turmoil: Ruling Bonus y TR Revision (1)`, `Tests generales del motor (13)`, `Tests generales del motor (14)`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `Turmoil: Ruling Bonus y TR Revision (2)`, `_stratopolis_player()`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **What connects `Hellas/Elysium alternative maps`, `Expansions covered: Base, Corporate Era, Venus Next, Colonies, Prelude, Turmoil, Promo`, `README next iteration: frontend` to the rest of the system?**
  _197 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.02833680314596345 - nodes in this community are weakly interconnected._
- **Should `Tests generales del motor (2)` be split into smaller, more focused modules?**
  _Cohesion score 0.0307461567304087 - nodes in this community are weakly interconnected._
- **Should `Colonies: colonias, Pluto/Europa y descartes` be split into smaller, more focused modules?**
  _Cohesion score 0.0595679012345679 - nodes in this community are weakly interconnected._