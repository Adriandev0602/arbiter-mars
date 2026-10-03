# Graph Report - arbiter-mars  (2026-10-03)

## Corpus Check
- 67 files · ~198,180 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1855 nodes · 5749 edges · 125 communities (86 shown, 39 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 280 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor (1)
- Tools Supabase (1)
- Colonies: colonias, Pluto/Europa y descartes (1)
- Tests generales del motor (2)
- Tests generales del motor (3)
- Tests generales del motor (4)
- Tests generales del motor (5)
- Tests generales del motor (6)
- Tests generales del motor (7)
- Tools Supabase (2)
- Tests generales del motor (8)
- Errores, producción e investigación (1)
- Docs del repo y README desactualizado (1)
- Errores, producción e investigación (2)
- Turmoil: núcleo político (1)
- Tablero: adyacencias (1)
- API FastAPI (routes/schemas)
- Turmoil: núcleo político (2)
- Errores, producción e investigación (3)
- Errores, producción e investigación (4)
- Tools Supabase (3)
- Tests generales del motor (9)
- package.json frontend (1)
- Colonies: colonias, Pluto/Europa y descartes (2)
- Scripts de mantenimiento del catálogo (1)
- Tablero: greenery y special tiles (1)
- Modelo Board (1)
- Frontend: chat mockeado (1)
- Tools Supabase (4)
- Modelo Board (2)
- Errores, producción e investigación (5)
- ui_e2e.py
- Frontend: chat mockeado (2)
- Config TypeScript
- Modelo Board (3)
- Tests generales del motor (10)
- Tablero: greenery y special tiles (2)
- Grafo LangGraph (1)
- Núcleo rules_engine y parámetros
- Scripts de mantenimiento del catálogo (2)
- Turmoil: núcleo político (3)
- Errores, producción e investigación (6)
- Frontend: chat mockeado (3)
- Tests generales del motor (11)
- Tablero: adyacencias (2)
- Tests generales del motor (12)
- Turmoil: núcleo político (4)
- Config y cliente Supabase
- Corporaciones: mecánicas resueltas
- SetupFlow.tsx
- Scripts de mantenimiento del catálogo (3)
- First actions de corporaciones
- GET /state (1)
- Tools Supabase (5)
- Turmoil: Ruling Bonus y TR Revision
- Marcadores: nomads y community (1)
- Frontend: chat mockeado (4)
- Tests generales del motor (13)
- resolve_ocean_offer
- Schema y base de datos
- Docs del repo y README desactualizado (2)
- Las 3 cartas dudosas (1)
- audit_catalog.py (1)
- Card catalog
- Marcadores: nomads y community (2)
- Tests generales del motor (14)
- Errores, producción e investigación (7)
- Tests generales del motor (15)
- Turmoil: núcleo político (5)
- audit_catalog.py (2)
- package.json frontend (2)
- Tests generales del motor (16)
- Errores, producción e investigación (8)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- Turmoil: núcleo político (6)
- Fuentes del mapa Tharsis
- Tests generales del motor (17)
- GET /state (2)
- Errores, producción e investigación (9)
- Volcanes y Noctis City
- Errores, producción e investigación (10)
- _stratopolis_player()
- Tests ruling_or_delegates
- Docs del repo y README desactualizado (3)
- resolve_global_event tool
- Punto de retoma 2026-09-10: T11 Recruitm
- Stack: Python, LangGraph, FastAPI, Supab
- Errores, producción e investigación (11)
- next.config
- Diversity Support
- Adyacencia precalculada
- GET /state (3)
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
- `Pristar order in run_production_phase (read flag before reset)` --references--> `run_production_phase()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `Tag iconography: power (purple bolt) vs space (golden sun)` --semantically_similar_to--> `Tag iconography lessons: 12 icons, verify tags against scan`  [INFERRED] [semantically similar]
  backend/app/db/CARDS_LOG.md → AGENTS.md
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

## Communities (125 total, 39 thin omitted)

### Community 0 - "Tests generales del motor (1)"
Cohesion: 0.03
Nodes (120): count_distinct_resource_types(), new_player_state(), test_acquired_company_gives_plus_3_mc_production(), test_adapted_lichen_gives_plus_1_plant_production(), test_apply_card_effect_with_no_effects_is_a_noop(), test_archaebacteria_gives_plus_1_plant_production(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_asteroid_card_raises_temperature_and_gives_titanium() (+112 more)

### Community 1 - "Tools Supabase (1)"
Cohesion: 0.07
Nodes (42): Bug: cities_delta ignored place_city_tiles (block 32), Bug: play_prelude never added prelude to played_cards, Prelude block 3: wiring gaps in play_prelude/use_card_action, Punto de retoma 2026-09-09: 10 of 12 pending preludes loaded, Stormcraft card_resource_as_heat, apply_colony_placed_bonuses(), apply_production_increased_bonus(), _increase_production() (+34 more)

### Community 2 - "Colonies: colonias, Pluto/Europa y descartes (1)"
Cohesion: 0.07
Nodes (39): Colonies mechanic (colonies.py), add_colony_tile(), adjust_colony_track(), build_colony(), ColonyDef, ColonyFullError, ColonyOccupiedError, ColonyTileState (+31 more)

### Community 3 - "Tests generales del motor (2)"
Cohesion: 0.03
Nodes (64): Extensible effects vocabulary in apply_card_effect, apply_card_effect(), effects vocabulary reference section, test_aquifer_released_places_ocean_without_granting_tr(), test_artificial_photosynthesis_choice_1_gives_energy_production(), test_artificial_photosynthesis_requires_valid_effect_choice(), test_biomass_combustors_requires_6_oxygen(), test_colonial_representation_mc_per_colony() (+56 more)

### Community 4 - "Tests generales del motor (3)"
Cohesion: 0.03
Nodes (60): register_active_card(), test_accion_requires_zero_resource(), test_add_resource_to_all_matching_type(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_any_card_resource_rejects_wrong_type_and_insufficient(), test_any_tag_played_choice_target_any_card() (+52 more)

### Community 5 - "Tests generales del motor (4)"
Cohesion: 0.03
Nodes (60): new_global_parameters(), test_aquifer_costs_18_mc_places_ocean_and_1_tr(), test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr(), test_city_costs_25_mc_and_gives_1_mc_production(), test_comet_raises_temperature_and_places_ocean(), test_convert_8_heat_to_temperature(), test_discard_card_then_draw_requires_discard_card_id_and_draws_n(), test_draw_cards_per_tag_scales_and_includes_this() (+52 more)

### Community 6 - "Tests generales del motor (5)"
Cohesion: 0.03
Nodes (59): use_card_action(), Stormcraft Incorporated card_resource_as_heat, target_card_resource_delta piece, Active cards and use_card_action, test_accion_card_resource_delta_per_tag(), test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_ants_action_moves_microbe_from_another_active_card() (+51 more)

### Community 7 - "Tests generales del motor (6)"
Cohesion: 0.04
Nodes (56): Requirements vocabulary in check_card_requirements, Wild tag (wild_tag_choice), check_card_requirements(), Card requirements section, Wild tag Research Coordination, test_advanced_ecosystems_multi_tag_requirements(), test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production() (+48 more)

### Community 8 - "Tests generales del motor (7)"
Cohesion: 0.04
Nodes (46): CardRequirementNotMetError, test_adaptation_technology_relaxes_global_requirements_2_steps(), test_anti_gravity_technology_discount_requires_7_science_tags(), test_arctic_algae_requires_temperature_minus_12_or_colder(), test_birds_requires_13_oxygen_and_decreases_plant_production(), test_breathing_filters_requires_7_oxygen_no_modeled_effect(), test_bushes_requires_minus_10_degrees_and_gives_plant_production_and_stock(), test_electro_catapult_requires_max_8_oxygen_and_minus_1_energy_production() (+38 more)

### Community 9 - "Tools Supabase (2)"
Cohesion: 0.08
Nodes (29): deal_starting_hand(buy_with_research=True), deal_prelude_hand / keep_preludes, Pharmacy Union + retire_card_as_event, Reds policy resolved at tools.py edge via diff before/after, Ruling Policy (Mars First, Greens, Unity, Kelvinists, Scientists, Reds), scientists_policy_used_this_generation flag, Setup clauses: Celestic 33 floater cards, prelude deal, buy starting hand, _apply_production_floor() (+21 more)

### Community 10 - "Tests generales del motor (8)"
Cohesion: 0.06
Nodes (27): apply_any_tag_played_choice(), apply_tag_played_choice(), CardEffectError, duplicate_reserved_card_resources(), player_has_optional_energy_to_heat(), _resolve_capped_counter(), reveal_top_cards_take_tag(), run_production_phase() (+19 more)

### Community 11 - "Errores, producción e investigación (1)"
Cohesion: 0.07
Nodes (26): card_resource_payment passive, convert_plants_to_greenery(), InsufficientResourcesError, plants_per_greenery(), resolve_research_phase(), spend_active_card_resource(), spend_card_resource_as_heat(), standard_project_air_scrapping() (+18 more)

### Community 12 - "Docs del repo y README desactualizado (1)"
Cohesion: 0.07
Nodes (31): API: /api/players, /api/state/{id}, /api/game, /api/chat, board.py Tharsis hex map module, Board wiring in tools (hex_id params, get_board_state), Chat end-to-end test pending (ANTHROPIC_API_KEY is placeholder), Colonies expansion, Deck/hand/research system, Layer 2: StateGraph always routes through ToolNode, Further frontend iterations (+23 more)

### Community 13 - "Errores, producción e investigación (2)"
Cohesion: 0.06
Nodes (20): adjust_mc_production(), apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_hex_bonus_tile_bonuses(), apply_standard_project_used_bonuses(), compute_standard_project_discount(), increment_zero_tag_cards_played(), ocean_adjacency_bonus_mc() (+12 more)

### Community 14 - "Turmoil: núcleo político (1)"
Cohesion: 0.15
Nodes (22): can_play_party_gated_card(), compute_influence(), new_turmoil(), place_delegate(), resolve_new_government(), test_can_play_party_gated_card_false_otherwise(), test_can_play_party_gated_card_true_if_ruling(), test_can_play_party_gated_card_true_with_min_delegates() (+14 more)

### Community 15 - "Tablero: adyacencias (1)"
Cohesion: 0.11
Nodes (12): can_place_city_adjacent_to_cities(), can_place_ocean_on_land(), place_city_tile_adjacent_to_cities(), place_ocean_tile_on_land(), Inverse board placements, test_can_place_city_adjacent_to_cities_requires_min_count(), test_can_place_ocean_on_land_only_on_land_hex(), test_place_city_tile_adjacent_to_cities_illegal_raises() (+4 more)

### Community 16 - "API FastAPI (routes/schemas)"
Cohesion: 0.17
Nodes (13): chat(), create_player(), ChatRequest, ChatResponse, ChooseCorporationRequest, CorporationSummary, CreatePlayerRequest, DealHandRequest (+5 more)

### Community 17 - "Turmoil: núcleo político (2)"
Cohesion: 0.17
Nodes (14): _add_to_party(), _check_party(), exchange_neutral_delegate(), neutral_non_leader_count(), _party_total(), PartyState, _recompute_dominant(), remove_delegate() (+6 more)

### Community 18 - "Errores, producción e investigación (3)"
Cohesion: 0.11
Nodes (15): CardNotInHandError, compute_reserved_card_discount(), player_has_tag_swap_passive(), release_reserved_card(), remove_card_from_hand(), reserve_card_in_slot(), swap_card_for_draw(), reserved_cards slot (Self-Replicating Robots) (+7 more)

### Community 19 - "Errores, producción e investigación (4)"
Cohesion: 0.10
Nodes (12): convert_heat_to_temperature(), corporation_first_action_city(), corporation_first_action_greenery(), GlobalParameters, increment_events_played(), place_city_tile(), raise_oxygen(), standard_project_asteroid() (+4 more)

### Community 20 - "Tools Supabase (3)"
Cohesion: 0.10
Nodes (18): action_used reset after reveal_prelude branch, Action choice key is 'choice' not 'options', free_trade gain handled in tools.use_card_action, Play a card within another play/action (Ecology Experts, Board of Directors), Punto de retoma 2026-09-10: prelude catalog complete 70/70, take_pending_prelude(), _draw_cards_matching_tag(), use_card_action() (+10 more)

### Community 21 - "Tests generales del motor (9)"
Cohesion: 0.13
Nodes (20): One-use fields pending_mc_discount / pending_requirement_tolerance_steps, Permanent passive effects, apply_tag_played_resource_bonuses(), register_passive_effect(), test_corridors_of_power_roba_al_volverse_party_leader(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_influence_bonus_passive_stored() (+12 more)

### Community 22 - "package.json frontend (1)"
Cohesion: 0.09
Nodes (21): dependencies, lucide-react, next, react, react-dom, name, private, scripts (+13 more)

### Community 23 - "Colonies: colonias, Pluto/Europa y descartes (2)"
Cohesion: 0.15
Nodes (17): apply_become_party_leader_bonus(), draw_cards_then_require_discard(), draw_cards_to_hand(), resolve_pending_discards(), Colonies mechanic, card_resource:<type> prefix for colony prizes, Colony catalog 11 of 11, Colony Pluto (pending_card_discards) (+9 more)

### Community 24 - "Scripts de mantenimiento del catálogo (1)"
Cohesion: 0.14
Nodes (6): main(), parse_db_url(), read_env_db_url(), main(), safe_filename(), README quick start

### Community 25 - "Tablero: greenery y special tiles (1)"
Cohesion: 0.17
Nodes (16): can_place_special_tile(), count_cities_and_special_tiles_adjacent_to_ocean(), new_board(), place_special_tile(), Generic place_special_tile parametrized by requirement, test_can_place_special_tile_requires_matching_hex_bonus(), test_count_cities_and_special_tiles_adjacent_to_ocean_ignora_greeneries(), test_hex_bonus_is_consumed_only_once() (+8 more)

### Community 26 - "Modelo Board (1)"
Cohesion: 0.15
Nodes (14): count_adjacent_oceans(), count_tiles_adjacent_to_ocean(), has_city_adjacent_to_ocean(), _place(), place_ocean_tile(), resolve_hex_bonus(), resolve_ocean_adjacency_bonus(), Tile placement legality rules (ocean, greenery, city, special) (+6 more)

### Community 27 - "Frontend: chat mockeado (1)"
Cohesion: 0.21
Nodes (16): CreatePlayer(), Dashboard(), GlobalParameters(), humanize(), PARTY_LABELS, Track(), TRACKS, Before() (+8 more)

### Community 28 - "Tools Supabase (4)"
Cohesion: 0.11
Nodes (16): Colonies Pluto and Europa: catalog 11 of 11, Corporation first actions (effects.first_action, resolve_corporation_first_action), graphify-out graph (always committed, nodes carry status), Bug: _load_player missed 3 columns (KeyError vs real Supabase), Milestones and awards, Neptunian Power Consultants (on_ocean_placed_offer), Nirgal and Philares Effects out of scope by design, pending_ocean_offers + resolve_ocean_offer (+8 more)

### Community 29 - "Modelo Board (2)"
Cohesion: 0.16
Nodes (10): _build_adjacency(), _build_hex_defs(), count_adjacent_owned_by(), count_empty_hexes_adjacent_to_owner(), get_adjacent_tiles(), HexDef, HexState, _neighbor_coords() (+2 more)

### Community 30 - "Errores, producción e investigación (5)"
Cohesion: 0.14
Nodes (11): deal_prelude_hand(), draw_random_preludes(), initialize_deck(), keep_preludes(), prelude_draw_candidates(), Prelude own deck (prelude_cards, prelude_review_queue), Prelude setup deal (4 dealt, keep 2), test_deal_prelude_hand_deals_4_excluding_played_and_refuses_twice() (+3 more)

### Community 31 - "ui_e2e.py"
Cohesion: 0.13
Nodes (7): api_get(), assert_ui_matches_api(), player_id_by_name(), record(), setup_matches_engine(), step(), ui_numbers()

### Community 32 - "Frontend: chat mockeado (2)"
Cohesion: 0.23
Nodes (16): Home(), readStorage(), skipKey(), writeStorage(), PlayerPicker(), handleCreate(), SetupStep, ChatResponse (+8 more)

### Community 33 - "Config TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 34 - "Modelo Board (3)"
Cohesion: 0.12
Nodes (15): Arcadian Communities (community TileType), Review blocks 31-38 (promos, CEO set, board markers), Board markers: nomad, cathedral, remove_greenery_tile, Kaguya Tech, Mars Nomads, St Joseph Cathedral, count_cathedrals(), place_cathedral(), remove_greenery_tile(), Board markers (block 37) (+7 more)

### Community 35 - "Tests generales del motor (10)"
Cohesion: 0.12
Nodes (15): _increase_production single choke-point (Manutech), Manutech corporation (on_production_increased), Pristar order in run_production_phase (read flag before reset), _raise_tr single choke-point for TR changes, _raise_tr(), retire_card_as_event(), Corporation block 2 (Ecotec to Manutech), Manutech and _increase_production (+7 more)

### Community 36 - "Tablero: greenery y special tiles (2)"
Cohesion: 0.21
Nodes (14): can_place_city(), can_place_greenery(), InvalidPlacementError, place_city_tile(), place_greenery_tile(), get_board_state(), test_can_place_city_on_volcanic_ignores_city_adjacency(), test_cannot_place_city_adjacent_to_another_city() (+6 more)

### Community 37 - "Grafo LangGraph (1)"
Cohesion: 0.15
Nodes (3): build_graph(), call_model(), AgentState

### Community 38 - "Núcleo rules_engine y parámetros"
Cohesion: 0.12
Nodes (16): is_blue_card(), Global Events block 5 multi-agent (22 cards), Global Events block 6 design agents (3 cards), resource_delta_per_capped_counter (cap 5 + Influence), Comprehensive FAQ v1.7, Bug: draw_cards_matching_tag left revealed cards in deck, Dry Deserts, 4 bugs found via FAQ (Aquifer Released, Jovian Tax Rights, Snow Cover, Diversity) (+8 more)

### Community 39 - "Scripts de mantenimiento del catálogo (2)"
Cohesion: 0.17
Nodes (7): build_image_url_index(), load_site_catalog(), main(), parse_pending_manifest(), connect(), load_corporations(), main()

### Community 40 - "Turmoil: núcleo político (3)"
Cohesion: 0.12
Nodes (15): scripts/apply_db.py (schema + 4 seeds, idempotent), Conventions, SUPABASE_DB_URL password contains @ (use individual psycopg2 params), Development commands, Operational note: Supabase host resolves only via IPv6, normalize_turmoil migrates old turmoil rows automatically, README updated: 412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, Second batch 2026-10-02: official neutral delegates, Stratopolis, README, Supabase migration (+7 more)

### Community 41 - "Errores, producción e investigación (6)"
Cohesion: 0.15
Nodes (11): GlobalParameterMaxedError, place_ocean(), raise_global_parameter_without_bonuses(), raise_venus(), standard_project_aquifer(), Bug: play_prelude registered passive twice, Prelude block 3 active preludes, raise_global_parameter_without_bonuses (World Government Advisor) (+3 more)

### Community 42 - "Frontend: chat mockeado (3)"
Cohesion: 0.23
Nodes (13): CardRow(), CardTabs(), KIND_LABEL, Tab, TAG_DOT, Tags(), CardPicker(), FIRST_ACTION_TEXT (+5 more)

### Community 43 - "Tests generales del motor (11)"
Cohesion: 0.13
Nodes (11): Automa (78 cards) never entered the pipeline, Corporations infrastructure (corporation_cards, choose_corporation, queue), Scope gap: Prelude, Corporation, Automa categories were filtered out, apply_city_placed_bonuses(), apply_corporation_start(), Corporations block 1 (Aphrodite to EcoLine), Corporation blocks 3-5: 41 of 48, Corporations category (corporation_cards, 48 of 48) (+3 more)

### Community 44 - "Tablero: adyacencias (2)"
Cohesion: 0.18
Nodes (11): can_place_city_on_volcanic(), can_place_ocean(), is_hex_empty(), remove_ocean_tile(), UnknownHexError, test_can_place_city_on_volcanic_rejects_non_volcanic_hex(), test_can_place_ocean_only_on_ocean_hex(), test_new_board_is_empty() (+3 more)

### Community 45 - "Tests generales del motor (12)"
Cohesion: 0.13
Nodes (13): calculate_card_payment(), compute_conversion_rates(), Passive effects vocabulary, test_advanced_alloys_changes_calculate_card_payment_result(), test_advanced_alloys_raises_steel_and_titanium_conversion_rates(), test_calculate_card_payment_exact_mc(), test_calculate_card_payment_insufficient_raises(), test_calculate_card_payment_overpaying_gives_no_refund_but_no_error() (+5 more)

### Community 46 - "Turmoil: núcleo político (4)"
Cohesion: 0.15
Nodes (13): changing_times(), setup_global_events(), Changing Times + setup_global_events, global_events.revealed_party/current_party columns (72/72 verified), Official neutral delegate mechanism (14 total, via Global Events), Superseded assumption: 2 fixed neutrals per party, Pendientes section (no rows), T11 Recruitment (+5 more)

### Community 47 - "Config y cliente Supabase"
Cohesion: 0.13
Nodes (3): Config, Settings, health()

### Community 48 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.13
Nodes (15): 81 differences; scan agreed with reference in 78, seed in 3, Run audit_catalog.py after loading new cards, Catalog audit 2026-10-02, choice/tag_count_choice ignore sibling keys, Design decisions kept (Mining Expedition, Hackers, Energy Tapping), Red Appeasement, Mass Converter, Nitrogen-Rich Asteroid fixes, Heavy Taxation corrected (-1 VP), KNOWN_OK: Mining Rights, Mining Area, Pharmacy Union (+7 more)

### Community 49 - "SetupFlow.tsx"
Cohesion: 0.31
Nodes (14): CorporationStep(), ErrorLine(), HandStep(), PreludeStep(), SetupFlow(), Stepper(), STEPS, useAction() (+6 more)

### Community 50 - "Scripts de mantenimiento del catálogo (3)"
Cohesion: 0.16
Nodes (10): power vs space audit (62 cards, 42 wrong), Audit error patterns (requirement read as tag, missing city/space, 16 unmarked events, cost misread), Contact-sheet method (tag_contact_sheet.py), Audit found missing tags, requirements read as tags, invented tags, power/space audit: 62 cards, 20 correct, 42 wrong, Tag iconography: power (purple bolt) vs space (golden sun), 16 events not marked is_event, build_sheets() (+2 more)

### Community 51 - "First actions de corporaciones"
Cohesion: 0.16
Nodes (11): consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching(), test_celestic_first_action_reveal_until_matching_se_anota_una_sola_vez(), test_consume_corporation_first_action_se_usa_una_sola_vez(), test_register_corporation_first_action_anota_pendiente(), test_register_corporation_first_action_reveal_preludes_conserva_n(), test_register_corporation_first_action_sin_spec_no_anota_nada() (+3 more)

### Community 52 - "GET /state (1)"
Cohesion: 0.32
Nodes (9): choose_corporation(), deal_preludes(), deal_starting_hand(), get_state(), keep_preludes(), play_prelude(), _player_or_404(), resolve_research() (+1 more)

### Community 53 - "Tools Supabase (5)"
Cohesion: 0.18
Nodes (10): Global Event generation cycle not automated (manual trigger), Global Events track: setup_global_events + Changing Times, _load_global_event_parties(), resolve_new_government(), _save_turmoil(), setup_global_events(), Gap resolved: resolve_ocean_offer and Unity, Ruling Policy per party (+2 more)

### Community 54 - "Turmoil: Ruling Bonus y TR Revision"
Cohesion: 0.15
Nodes (12): Punto de retoma 2026-09-10: Turmoil TR Revision, Ruling Bonus, 6 Ruling Policies, Ruling Bonus (6 formulas, one per party), TR Revision (-1 TR at each New Government), apply_ruling_bonus(), Ruling Bonus per party, test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production(), test_apply_ruling_bonus_mars_first_pays_per_building_tag() (+4 more)

### Community 55 - "Marcadores: nomads y community (1)"
Cohesion: 0.19
Nodes (10): count_tiles_of_type(), find_nomads(), get_neighbors(), move_nomads(), test_corner_hex_has_3_neighbors(), test_count_empty_hexes_adjacent_to_owner_counts_each_hex_once(), test_count_tiles_of_type_and_owner(), test_get_neighbors_unknown_hex_raises() (+2 more)

### Community 56 - "Frontend: chat mockeado (4)"
Cohesion: 0.18
Nodes (9): interTight, metadata, EXAMPLES, Message, SidebarChat(), send(), sendChatMessage(), next (+1 more)

### Community 57 - "Tests generales del motor (13)"
Cohesion: 0.17
Nodes (11): raise_temperature(), test_on_temperature_raised_no_paga_pasos_no_aplicados(), test_on_temperature_raised_paga_por_paso_aplicado(), test_preservation_program_anula_el_primer_paso_de_tr_de_la_generacion(), test_pristar_paga_solo_si_no_subio_el_tr_esta_generacion(), test_raise_temperature_at_max_raises(), test_raise_temperature_caps_at_max_and_only_grants_tr_for_applied_steps(), test_raise_temperature_one_step_is_2_degrees_and_1_tr() (+3 more)

### Community 58 - "resolve_ocean_offer"
Cohesion: 0.27
Nodes (11): resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each() (+3 more)

### Community 59 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 60 - "Docs del repo y README desactualizado (2)"
Cohesion: 0.18
Nodes (10): card_review_queue table, CARDS_PENDING_REVIEW.md (deprecated), Supabase data model, download_review_scans.py (2.5s spacing, scan_cache gitignored), Card review queue workflow in Supabase, cards table, global_events table, global_parameters table (+2 more)

### Community 61 - "Las 3 cartas dudosas (1)"
Cohesion: 0.20
Nodes (7): Air Raid (Colonies) out of scope, Law Suit and Crash Site Cleanup out of scope, Clauses omitted by design (remove from any player, opponent-dependent, VP-only), Loaded cards table (412 project cards), Nirgal Enterprises (out of scope), Out-of-scope by design table (Rover Construction, Herbivores, Air Raid, Law Suit, Crash Site), Verification source: tm.hadronikle.com scans

### Community 62 - "audit_catalog.py (1)"
Cohesion: 0.20
Nodes (10): New workflow rule: run audit_catalog.py after touching cards, Audit method: two sources, the scan decides, Branch flow feat/review-block-N chained, choice/tag_count_choice silently ignore sibling keys (early return), 4 preludes unblocked (Preservation Program, Suitable Infrastructure, Terraforming Deal, Colony Trade Hub), Punto de retoma 2026-10-02: full catalog audit (branch feat/auditoria-catalogo), Punto de retoma 2026-09-09: corporations 48/48, Smoke test vs real Supabase 19/19, tests 718/718 (+2 more)

### Community 63 - "Card catalog"
Cohesion: 0.20
Nodes (8): Typical catalog errors (requirement read as tag, missing city/space tag, unmarked events, cost from production box, invented effects), Audit result: 81 differences, 78 cards fixed, 3 reference errors (KNOWN_OK), Card catalog (hand-loaded, verified against official scans), No script automates cost/tags/effects decisions, Progress: 408 project cards, 36 Global Events, preludes, queues empty, Block 31 multi-agent batch review, Block 34 multi-agent batch: 4 of 10 reports misread, Block 35 multi-agent batch: 3 of 10 reports misread tags

### Community 64 - "Marcadores: nomads y community (2)"
Cohesion: 0.27
Nodes (6): community_owner(), HexOccupiedError, place_community(), test_community_exige_adyacencia_salvo_la_primera(), test_community_no_va_en_oceano_ni_en_hex_reservado(), test_community_reserva_el_hex_sin_ocuparlo()

### Community 65 - "Tests generales del motor (14)"
Cohesion: 0.20
Nodes (6): apply_card_played_vp_icon_bonus(), register_played_card(), resolve_active_card_starting_resources(), choose_corporation(), played_cards history, test_register_played_card_appends_to_history()

### Community 66 - "Errores, producción e investigación (7)"
Cohesion: 0.29
Nodes (8): apply_card_resource_gained_bonuses(), snapshot_card_resource_totals(), Diff before/after snapshot pattern, on_card_resource_gained passive (Meat Industry, Topsoil Contract), test_on_card_resource_gained_ignora_gastos_y_otros_tipos(), test_on_card_resource_gained_no_paga_por_mover_entre_cartas(), test_on_card_resource_gained_own_card_only_solo_cuenta_su_propia_carta(), test_on_card_resource_gained_paga_por_unidad_ganada()

### Community 67 - "Tests generales del motor (15)"
Cohesion: 0.20
Nodes (9): compute_card_cost_discount(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_compute_card_cost_discount_with_no_passive_effects_is_0(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter(), test_earth_office_discount_only_applies_to_earth_tag(), test_mass_converter_discount_does_not_apply_to_non_space_cards(), test_mass_converter_gives_2_mc_discount_on_space_cards() (+1 more)

### Community 68 - "Turmoil: núcleo político (5)"
Cohesion: 0.20
Nodes (10): Block 31 second batch: 12 more cards, allow_leader, Old pending list: Floating Refinery, Frontier Town, L1 Trade Terminal, Red Appeasement, Venus Shuttles, P74 Frontier Town placement bonus multiplier, P73 Floating Refinery, P78 L1 Trade Terminal, P89 Venus Shuttles, Public Celebrations: VP read as TR (effects {}), trade_bump_track_first N steps (+2 more)

### Community 69 - "audit_catalog.py (2)"
Cohesion: 0.31
Nodes (5): fetch(), load_reference(), main(), norm(), vitor_excluded()

### Community 70 - "package.json frontend (2)"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 71 - "Tests generales del motor (16)"
Cohesion: 0.29
Nodes (6): apply_event_played_bonuses(), test_media_group_gives_3_mc_when_event_card_is_played(), test_multiple_passive_effects_stack(), test_on_event_played_puede_robar_cartas_con_su_propio_tag_filter(), test_optimal_aerobraking_only_triggers_on_space_events(), test_palladin_shipping_gana_titanio_por_evento_espacial()

### Community 72 - "Errores, producción e investigación (8)"
Cohesion: 0.29
Nodes (5): apply_new_distinct_tag_bonuses(), increment_tags_played(), tags_played counter, test_increment_tags_played_counts_each_tag(), test_on_new_distinct_tag_played_solo_la_primera_vez_y_no_con_eventos()

### Community 73 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 74 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 75 - "Turmoil: núcleo político (6)"
Cohesion: 0.33
Nodes (5): place_neutral_delegate(), test_exchange_neutral_delegate_puede_volver_leader_al_jugador(), test_jugador_con_mas_delegados_reemplaza_al_leader_neutral(), test_neutral_delegate_con_reserva_vacia_no_hace_nada(), test_neutral_delegate_sale_de_la_reserva_y_puede_ser_leader_y_dominante()

### Community 76 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 77 - "Tests generales del motor (17)"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 79 - "Errores, producción e investigación (9)"
Cohesion: 0.40
Nodes (5): Block 33 pending: X17 out of scope, X20 unblocked, Diversity Support (X20), Retrofit active_card_resource_type for 11 microbe + 13 animal cards, security_fleet excluded (stores fighters), X17 Crash Site Cleanup (out of scope)

### Community 80 - "Volcanes y Noctis City"
Cohesion: 0.50
Nodes (3): VOLCANO_NAMES, Lava Flows (VOLCANO_NAMES, hex_id_in), Noctis City reserved hex (id 31)

### Community 81 - "Errores, producción e investigación (10)"
Cohesion: 0.50
Nodes (3): sum_card_resources_by_type(), Stratopolis corrected, Typed card resources (floaters)

### Community 82 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 83 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 85 - "resolve_global_event tool"
Cohesion: 0.67
Nodes (3): Comprehensive FAQ v1.7 (Jeffrey Anchan), resolve_global_event tool, Turmoil Global Events: 36 of 36

### Community 86 - "Punto de retoma 2026-09-10: T11 Recruitm"
Cohesion: 0.67
Nodes (3): Orphan PR problem (recovery PR #56 merged immediately), Pending table in CARDS_LOG empty, Punto de retoma 2026-09-10: T11 Recruitment loaded

### Community 87 - "Stack: Python, LangGraph, FastAPI, Supab"
Cohesion: 0.67
Nodes (3): Repo structure, supabase>=2.8.0 required for new API key format, Stack: Python, LangGraph, FastAPI, Supabase, Next.js, Docker

## Knowledge Gaps
- **202 isolated node(s):** `Extensible effects vocabulary in apply_card_effect`, `effects vocabulary reference section`, `Viral Enhancers on_any_tag_played_choice`, `Bug: cities_delta ignored place_city_tiles (block 32)`, `Smoke-test bug block 32: cities_delta ignoring place_city_tiles` (+197 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 527 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `apply_card_effect()` connect `Tests generales del motor (2)` to `Tests generales del motor (1)`, `Tools Supabase (1)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Tools Supabase (2)`, `Tests generales del motor (8)`, `Errores, producción e investigación (1)`, `Errores, producción e investigación (2)`, `Errores, producción e investigación (3)`, `Errores, producción e investigación (4)`, `Colonies: colonias, Pluto/Europa y descartes (2)`, `Errores, producción e investigación (5)`, `Tests generales del motor (10)`, `Errores, producción e investigación (6)`, `Corporaciones: mecánicas resueltas`, `Tests generales del motor (13)`, `Las 3 cartas dudosas (1)`, `audit_catalog.py (1)`, `Tests generales del motor (14)`, `Errores, producción e investigación (10)`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `play_card()` connect `Tools Supabase (1)` to `Colonies: colonias, Pluto/Europa y descartes (1)`, `Tests generales del motor (2)`, `Tests generales del motor (3)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Tools Supabase (2)`, `Tests generales del motor (8)`, `Errores, producción e investigación (1)`, `Errores, producción e investigación (2)`, `Turmoil: núcleo político (1)`, `Tablero: adyacencias (1)`, `Turmoil: núcleo político (2)`, `Errores, producción e investigación (3)`, `Errores, producción e investigación (4)`, `Tools Supabase (3)`, `Tests generales del motor (9)`, `Colonies: colonias, Pluto/Europa y descartes (2)`, `Tablero: greenery y special tiles (1)`, `Modelo Board (1)`, `Modelo Board (2)`, `Modelo Board (3)`, `Tablero: greenery y special tiles (2)`, `Tablero: adyacencias (2)`, `Tests generales del motor (12)`, `Tools Supabase (5)`, `Marcadores: nomads y community (1)`, `Tests generales del motor (14)`, `Errores, producción e investigación (7)`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `Errores, producción e investigación (8)`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `new_player_state()` connect `Tests generales del motor (1)` to `Colonies: colonias, Pluto/Europa y descartes (1)`, `Tests generales del motor (2)`, `Tests generales del motor (3)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `Tests generales del motor (7)`, `Tests generales del motor (8)`, `Errores, producción e investigación (1)`, `Errores, producción e investigación (2)`, `Errores, producción e investigación (3)`, `Tests generales del motor (9)`, `Colonies: colonias, Pluto/Europa y descartes (2)`, `Tablero: greenery y special tiles (1)`, `Errores, producción e investigación (5)`, `Tests generales del motor (10)`, `Errores, producción e investigación (6)`, `Tests generales del motor (11)`, `Tests generales del motor (12)`, `First actions de corporaciones`, `Turmoil: Ruling Bonus y TR Revision`, `Tests generales del motor (13)`, `resolve_ocean_offer`, `Tests generales del motor (14)`, `Errores, producción e investigación (7)`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `Errores, producción e investigación (8)`, `Tests generales del motor (17)`, `_stratopolis_player()`, `Errores, producción e investigación (11)`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **What connects `Extensible effects vocabulary in apply_card_effect`, `effects vocabulary reference section`, `Viral Enhancers on_any_tag_played_choice` to the rest of the system?**
  _202 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.031096774193548386 - nodes in this community are weakly interconnected._
- **Should `Tools Supabase (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.0675990675990676 - nodes in this community are weakly interconnected._
- **Should `Colonies: colonias, Pluto/Europa y descartes (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.07067603160667252 - nodes in this community are weakly interconnected._