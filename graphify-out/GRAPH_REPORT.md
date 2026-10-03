# Graph Report - arbiter-mars  (2026-10-02)

## Corpus Check
- 57 files · ~183,432 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1664 nodes · 5468 edges · 100 communities (67 shown, 33 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 254 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor (1)
- Tests generales del motor (2)
- Tests generales del motor (3)
- Errores, producción e investigación (1)
- Colonies: colonias, Pluto/Europa y descartes (1)
- Turmoil: núcleo político (1)
- Tools Supabase (1)
- Tools Supabase (2)
- Tests generales del motor (4)
- Tests generales del motor (5)
- Frontend: chat mockeado
- Scripts de mantenimiento del catálogo
- Tests generales del motor (6)
- Marcadores: nomads y community
- package.json frontend
- First actions de corporaciones (motor) (1)
- Tablero: greenery y special tiles
- Tests generales del motor (7)
- Tests generales del motor (8)
- Docs del repo y README desactualizado (1)
- Tablero: adyacencias (1)
- Registro CARDS_LOG y recursos tipados (1)
- Config TypeScript
- First actions de corporaciones (motor) (2)
- Grafo LangGraph (1)
- Errores, producción e investigación (2)
- Visión del proyecto y alcance (1)
- Modelo Board (1)
- Errores, producción e investigación (3)
- API FastAPI (routes/schemas) (1)
- Tablero: adyacencias (2)
- Turmoil: Ruling Bonus y TR Revision
- Modelo Board (2)
- Modelo Board (3)
- Colonies: colonias, Pluto/Europa y descartes (2)
- Conversión y pasivos permanentes
- resolve_ocean_offer
- Schema y base de datos
- Núcleo rules_engine y parámetros (1)
- Tablero: adyacencias (3)
- Las 3 cartas dudosas
- Tests generales del motor (9)
- Tests generales del motor (10)
- Config y cliente Supabase
- Corporaciones: mecánicas resueltas
- Tests generales del motor (11)
- Errores, producción e investigación (4)
- GET /state (1)
- Tests generales del motor (12)
- Núcleo rules_engine y parámetros (2)
- Tests generales del motor (13)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- scripts/apply_db.py
- Núcleo rules_engine y parámetros (3)
- Fuera de alcance por diseño (1)
- Entry point FastAPI
- Docs del repo y README desactualizado (2)
- Fuentes del mapa Tharsis
- Tests generales del motor (14)
- Tests generales del motor (15)
- Tests generales del motor (16)
- API FastAPI (routes/schemas) (2)
- Preludes: jugada y snapshots
- Fuera de alcance por diseño (2)
- Turmoil: núcleo político (2)
- Fuera de alcance por diseño (3)
- _stratopolis_player()
- Tests ruling_or_delegates
- Volcanes y Noctis City
- Registro CARDS_LOG y recursos tipados (2)
- next.config
- Adyacencia precalculada
- Errores, producción e investigación (5)
- Errores, producción e investigación (6)
- Tools Supabase (3)
- Errores, producción e investigación (7)
- Visión del proyecto y alcance (2)
- Mapas alternativos
- Visión del proyecto y alcance (3)
- Visión del proyecto y alcance (4)

## God Nodes (most connected - your core abstractions)
1. `new_player_state()` - 556 edges
2. `new_global_parameters()` - 458 edges
3. `apply_card_effect()` - 323 edges
4. `register_active_card()` - 158 edges
5. `check_card_requirements()` - 139 edges
6. `use_card_action()` - 119 edges
7. `CardRequirementNotMetError` - 106 edges
8. `PlayerState` - 96 edges
9. `register_passive_effect()` - 96 edges
10. `play_card()` - 81 edges

## Surprising Connections (you probably didn't know these)
- `_raise_tr punto unico de cambios de TR` --references--> `_raise_tr()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
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

## Communities (100 total, 33 thin omitted)

### Community 0 - "Tests generales del motor (1)"
Cohesion: 0.03
Nodes (123): apply_card_effect(), new_global_parameters(), test_acquired_company_gives_plus_3_mc_production(), test_apply_card_effect_with_no_effects_is_a_noop(), test_aquifer_released_places_ocean_without_granting_tr(), test_archaebacteria_gives_plus_1_plant_production(), test_artificial_photosynthesis_choice_1_gives_energy_production(), test_asteroid_mining_gives_plus_2_titanium_production() (+115 more)

### Community 1 - "Tests generales del motor (2)"
Cohesion: 0.03
Nodes (114): new_player_state(), test_adapted_lichen_gives_plus_1_plant_production(), test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production(), test_aquifer_costs_18_mc_places_ocean_and_1_tr(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_asteroid_card_raises_temperature_and_gives_titanium(), test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr() (+106 more)

### Community 2 - "Tests generales del motor (3)"
Cohesion: 0.04
Nodes (98): CardRequirementNotMetError, check_card_requirements(), test_adaptation_technology_relaxes_global_requirements_2_steps(), test_advanced_ecosystems_multi_tag_requirements(), test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production(), test_anti_gravity_technology_discount_requires_7_science_tags(), test_archaebacteria_requires_max_temperature_minus_18() (+90 more)

### Community 3 - "Errores, producción e investigación (1)"
Cohesion: 0.04
Nodes (51): adjust_mc_production(), apply_any_tag_played_choice(), apply_become_party_leader_bonus(), apply_card_played_vp_icon_bonus(), apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_new_distinct_tag_bonuses(), apply_standard_project_used_bonuses() (+43 more)

### Community 4 - "Colonies: colonias, Pluto/Europa y descartes (1)"
Cohesion: 0.06
Nodes (54): add_colony_tile(), adjust_colony_track(), build_colony(), ColonyDef, ColonyFullError, ColonyOccupiedError, ColonyTileState, new_colonies() (+46 more)

### Community 5 - "Turmoil: núcleo político (1)"
Cohesion: 0.07
Nodes (60): Track de eventos setup_global_events / Changing Times, T11 Recruitment: delegados neutrales oficiales (14, 1 Chairman, 13 reserva), _add_to_party(), can_play_party_gated_card(), changing_times(), _check_party(), compute_influence(), exchange_neutral_delegate() (+52 more)

### Community 6 - "Tools Supabase (1)"
Cohesion: 0.08
Nodes (33): tools.py wrapper de I/O Supabase, choose_corporation(), _compute_player_influence(), _count_blue_cards_played(), deal_prelude_hand(), deal_starting_hand(), get_active_cards_state(), get_board_state() (+25 more)

### Community 7 - "Tools Supabase (2)"
Cohesion: 0.08
Nodes (30): can_place_ocean(), apply_colony_placed_bonuses(), apply_production_increased_bonus(), remove_prelude_from_hand(), snapshot_production_totals(), _apply_colony_placement_bonus(), _apply_community_build_bonus(), _apply_hex_bonus() (+22 more)

### Community 8 - "Tests generales del motor (4)"
Cohesion: 0.04
Nodes (46): use_card_action(), test_accion_card_resource_delta_per_tag(), test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_ants_action_moves_microbe_from_another_active_card(), test_any_card_resource_action_cost_spends_from_chosen_card(), test_aquifer_pumping_action_spends_mc_for_ocean(), test_business_network_minus_1_mc_production_and_repeatable_research_action() (+38 more)

### Community 9 - "Tests generales del motor (5)"
Cohesion: 0.04
Nodes (45): register_active_card(), test_add_resource_to_all_matching_type(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_apply_card_effect_choice_threads_target_card_id(), test_atmo_collectors_action_choice_add_or_spend_for_titanium_energy_heat(), test_atmoscoop_choice_temperature_or_venus_plus_floaters_to_target(), test_caretaker_contract_spends_heat_for_tr() (+37 more)

### Community 10 - "Frontend: chat mockeado"
Cohesion: 0.09
Nodes (34): Layout responsivo (chat abajo en celular), Frontend v1 (Next 14 + Tailwind, dashboard, selector jugador), Selector/creacion de jugador (localStorage, ?player=), metadata, Home(), CardList(), KIND_LABEL, Dashboard() (+26 more)

### Community 11 - "Scripts de mantenimiento del catálogo"
Cohesion: 0.07
Nodes (16): main(), parse_db_url(), read_env_db_url(), main(), safe_filename(), build_image_url_index(), load_site_catalog(), main() (+8 more)

### Community 12 - "Tests generales del motor (6)"
Cohesion: 0.06
Nodes (35): CardEffectError, duplicate_reserved_card_resources(), reserve_card_in_slot(), test_accion_requires_zero_resource(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_any_card_resource_rejects_wrong_type_and_insufficient(), test_apply_card_effect_target_card_resource_delta(), test_artificial_photosynthesis_requires_valid_effect_choice() (+27 more)

### Community 13 - "Marcadores: nomads y community"
Cohesion: 0.10
Nodes (18): community_owner(), count_tiles_of_type(), find_nomads(), HexOccupiedError, HexState, is_hex_empty(), move_nomads(), _place() (+10 more)

### Community 14 - "package.json frontend"
Cohesion: 0.07
Nodes (29): dependencies, next, react, react-dom, devDependencies, autoprefixer, postcss, tailwindcss (+21 more)

### Community 15 - "First actions de corporaciones (motor) (1)"
Cohesion: 0.08
Nodes (25): apply_corporation_start(), consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching(), Arcadian Communities first action: place community, Aridor first action: add_colony_tile, Celestic first action reveal_until_matching (33 cartas con floater), Corporaciones: categoria completa 48 de 48 (+17 more)

### Community 16 - "Tablero: greenery y special tiles"
Cohesion: 0.14
Nodes (20): can_place_special_tile(), InvalidPlacementError, new_board(), place_city_tile_adjacent_to_cities(), place_ocean_tile_on_land(), place_special_tile(), Generic place_special_tile parametrized by requirement, test_can_place_ocean_only_on_ocean_hex() (+12 more)

### Community 17 - "Tests generales del motor (7)"
Cohesion: 0.11
Nodes (24): apply_tag_played_resource_bonuses(), register_passive_effect(), test_corridors_of_power_roba_al_volverse_party_leader(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_ocean_adjacency_bonus_mc_override(), test_olympus_conference_tag_played_choice_add_or_spend(), test_on_cost_threshold_paid_usa_el_costo_basico() (+16 more)

### Community 18 - "Tests generales del motor (8)"
Cohesion: 0.08
Nodes (23): raise_temperature(), run_production_phase(), test_card_action_available_again_after_production_phase(), test_indentured_workers_grants_pending_discount_consumed_next_card(), test_la_fase_de_produccion_limpia_el_flag_de_tr(), test_on_temperature_raised_no_paga_pasos_no_aplicados(), test_on_temperature_raised_paga_por_paso_aplicado(), test_preservation_program_anula_el_primer_paso_de_tr_de_la_generacion() (+15 more)

### Community 19 - "Docs del repo y README desactualizado (1)"
Cohesion: 0.14
Nodes (19): Marcadores en tablero (nomad, cathedral, remove_greenery), board.py mapa hexagonal Tharsis, Flujo de ramas feat/review-block-N, Pago con recurso de carta, Referencia a CARDS_LOG.md, Convenciones (type hints, funciones puras, tests con numero exacto), Sistema mazo/mano/investigacion, Grafo determinista LangGraph (graph.py, siempre via ToolNode) (+11 more)

### Community 20 - "Tablero: adyacencias (1)"
Cohesion: 0.13
Nodes (11): can_place_greenery(), count_adjacent_owned_by(), count_empty_hexes_adjacent_to_owner(), place_greenery_tile(), test_count_empty_hexes_adjacent_to_owner_counts_each_hex_once(), test_count_tiles_of_type_and_owner(), test_greenery_free_placement_when_player_has_no_tiles_yet(), test_greenery_requires_adjacency_once_player_has_a_tile() (+3 more)

### Community 21 - "Registro CARDS_LOG y recursos tipados (1)"
Cohesion: 0.10
Nodes (19): Cartas activas: accion repetible, Bloque 31: multi-agente y revision de tags, Sistema de mazo / mano, Diversity Support (X20), Vocabulario de effects soportado en apply_card_effect, Vias de pago: acero/titanio, card_resource, stock_resource, standard_project_card_resource, Global Events bloque 5 (multi-agente), Turmoil: Global Events (36 de 36) (+11 more)

### Community 22 - "Config TypeScript"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 23 - "First actions de corporaciones (motor) (2)"
Cohesion: 0.12
Nodes (18): POST /api/chat con updated_state y errores 503/429, GET /api/game, GET/POST /api/players, GET /api/state/{id} devuelve {player, cards}, Auditoria completa de tags/requisitos/VP negativos del catalogo base, Prueba end-to-end del chat (ANTHROPIC_API_KEY placeholder), Corporaciones 48 de 48, Mas iteraciones del frontend (+10 more)

### Community 24 - "Grafo LangGraph (1)"
Cohesion: 0.15
Nodes (3): build_graph(), call_model(), AgentState

### Community 25 - "Errores, producción e investigación (2)"
Cohesion: 0.15
Nodes (12): apply_card_resource_gained_bonuses(), count_distinct_resource_types(), snapshot_card_resource_totals(), sum_card_resources_by_type(), Recursos tipados por carta activa (floaters), test_min_distinct_resource_types_ignora_recursos_en_cero(), test_on_card_resource_gained_ignora_gastos_y_otros_tipos(), test_on_card_resource_gained_no_paga_por_mover_entre_cartas() (+4 more)

### Community 26 - "Visión del proyecto y alcance (1)"
Cohesion: 0.13
Nodes (15): Colonias Pluto y Europa, catalogo 11 de 11, deal_prelude_hand / keep_preludes, 3 cartas dudosas cargadas (self_replicating_robots, venus_orbital_survey, wg_project), first actions de corporaciones (effects.first_action), graphify-out grafo del proyecto (se commitea siempre), Nirgal y Effect de Philares fuera de alcance por diseno, pending_card_discards + resolve_pending_discards, pending_prelude_draw + resolve_prelude_draw (+7 more)

### Community 27 - "Modelo Board (1)"
Cohesion: 0.16
Nodes (11): count_adjacent_oceans(), count_cities_and_special_tiles_adjacent_to_ocean(), count_tiles_adjacent_to_ocean(), place_ocean_tile(), resolve_ocean_adjacency_bonus(), Tile placement legality rules (ocean, greenery, city, special), test_count_cities_and_special_tiles_adjacent_to_ocean_ignora_greeneries(), test_count_tiles_adjacent_to_ocean_counts_each_tile_once() (+3 more)

### Community 28 - "Errores, producción e investigación (3)"
Cohesion: 0.15
Nodes (10): deal_prelude_hand(), draw_random_preludes(), initialize_deck(), keep_preludes(), Prelude: mazo propio (70 de 70) y reparto de setup, Reparto de preludes en el setup (deal_prelude_hand, keep_preludes), test_deal_prelude_hand_deals_4_excluding_played_and_refuses_twice(), test_draw_random_preludes_is_seeded_distinct_and_respects_exclude() (+2 more)

### Community 29 - "API FastAPI (routes/schemas) (1)"
Cohesion: 0.26
Nodes (6): ChatRequest, ChatResponse, CreatePlayerRequest, GameState, PlayerStateResponse, PlayerSummary

### Community 30 - "Tablero: adyacencias (2)"
Cohesion: 0.19
Nodes (11): can_place_city_adjacent_to_cities(), get_adjacent_tiles(), get_neighbors(), remove_ocean_tile(), UnknownHexError, test_can_place_city_adjacent_to_cities_requires_min_count(), test_corner_hex_has_3_neighbors(), test_get_neighbors_unknown_hex_raises() (+3 more)

### Community 31 - "Turmoil: Ruling Bonus y TR Revision"
Cohesion: 0.15
Nodes (12): Comprehensive FAQ v1.7 (fuente), Global Events 36 de 36, Reds policy en el borde de tools.py (_apply_reds_ruling_policy), Turmoil nucleo politico (turmoil.py), Turmoil: TR Revision + Ruling Bonus + 6 Ruling Policy, apply_ruling_bonus(), Ciclo de generaciones de Global Events no automatizado, test_apply_ruling_bonus_mars_first_pays_per_building_tag() (+4 more)

### Community 32 - "Modelo Board (2)"
Cohesion: 0.21
Nodes (7): _build_adjacency(), _build_hex_defs(), can_place_city_on_volcanic(), HexDef, _neighbor_coords(), _row(), test_can_place_city_on_volcanic_rejects_non_volcanic_hex()

### Community 33 - "Modelo Board (3)"
Cohesion: 0.18
Nodes (9): can_place_ocean_on_land(), count_cathedrals(), place_cathedral(), remove_greenery_tile(), Marcadores en el tablero (nomad, cathedral, remove greenery), Kaguya Tech, Mars Nomads, Neptunian, St. Joseph (bloque 37), pending_ocean_offers + resolve_ocean_offer, test_can_place_ocean_on_land_only_on_land_hex() (+1 more)

### Community 34 - "Colonies: colonias, Pluto/Europa y descartes (2)"
Cohesion: 0.18
Nodes (12): Expansion Colonies y mecanica colonies.py, Jugar carta dentro de otra (Ecology Experts, Board of Directors), IA autonoma contra humanos / multi-juego, Pago cruzado Ares, Mapas Hellas/Elysium, Milestones y awards, Solar Phase de Venus Next, Variante solitario oficial (TR 14) (+4 more)

### Community 35 - "Conversión y pasivos permanentes"
Cohesion: 0.17
Nodes (11): compute_conversion_rates(), Reds Ruling Policy en el borde de tools.py, Gap resolve_ocean_offer y Unity, Ruling Bonus de los 6 partidos, TR Revision (-1 TR por generacion), Turmoil: TR Revision, Ruling Bonus y Ruling Policy, Correccion regla Unity: titanio vale +1 M EUR extra, test_advanced_alloys_changes_calculate_card_payment_result() (+3 more)

### Community 36 - "resolve_ocean_offer"
Cohesion: 0.27
Nodes (11): resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each() (+3 more)

### Community 37 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 38 - "Núcleo rules_engine y parámetros (1)"
Cohesion: 0.18
Nodes (6): apply_hex_bonus_tile_bonuses(), _apply_production_floor(), _increase_production(), standard_project_power_plant(), _apply_colony_gain(), test_power_plant_insufficient_funds_raises()

### Community 39 - "Tablero: adyacencias (3)"
Cohesion: 0.31
Nodes (9): can_place_city(), has_city_adjacent_to_ocean(), place_city_tile(), test_can_place_city_on_volcanic_ignores_city_adjacency(), test_cannot_place_city_adjacent_to_another_city(), test_cannot_place_city_on_noctis_city_reserved_hex(), test_has_city_adjacent_to_ocean_filtra_por_dueno(), test_has_city_adjacent_to_ocean_ignora_ciudad_lejos_del_agua() (+1 more)

### Community 40 - "Las 3 cartas dudosas"
Cohesion: 0.22
Nodes (7): Catalogo de cartas (412 de proyecto), Tabla card_review_queue (cola vacia), Clausulas omitidas por diseno (remove from any player, oponentes, solo VP), Cartas dependientes de oponentes (Air Raid, Law Suit, Crash Site Cleanup, Rover Construction, Mons Insurance, Herbivores), scan_cache gitignored (derechos FryxGames), download_review_scans.py (2.5s entre pedidos), README status table (412 cards, 48 corps, 70 preludes, 36 events, 11 colonies, 715 tests)

### Community 41 - "Tests generales del motor (9)"
Cohesion: 0.22
Nodes (8): compute_card_cost_discount(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter(), test_earth_office_discount_only_applies_to_earth_tag(), test_mass_converter_discount_does_not_apply_to_non_space_cards(), test_mass_converter_gives_2_mc_discount_on_space_cards(), test_venus_waystation_passive_discounts_venus_tag_cards()

### Community 42 - "Tests generales del motor (10)"
Cohesion: 0.22
Nodes (8): raise_venus(), test_on_venus_raised_paga_por_paso_aplicado(), test_raise_venus_at_max_raises(), test_raise_venus_bonus_step_16_percent_grants_extra_tr(), test_raise_venus_bonus_step_8_percent_draws_free_card(), test_raise_venus_caps_at_30(), test_raise_venus_multiple_steps_crossing_both_bonus_thresholds_at_once(), test_raise_venus_one_step_is_2_percent_and_1_tr()

### Community 44 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.22
Nodes (9): Arcadian Communities: TileType community, Corporaciones bloque 2 (Ecotec a Manutech), Corporaciones: mecanicas pendientes resueltas (_raise_tr), _increase_production (Manutech), Manutech, Mons Insurance: clausulas de oponentes, Pharmacy Union (retire_card_as_event), Hook unico _raise_tr y tr_raised_this_generation (+1 more)

### Community 45 - "Tests generales del motor (11)"
Cohesion: 0.25
Nodes (7): calculate_card_payment(), test_calculate_card_payment_exact_mc(), test_calculate_card_payment_insufficient_raises(), test_calculate_card_payment_overpaying_gives_no_refund_but_no_error(), test_calculate_card_payment_steel_on_non_building_card_raises(), test_calculate_card_payment_with_steel_on_building_card(), test_calculate_card_payment_with_titanium_on_space_card()

### Community 46 - "Errores, producción e investigación (4)"
Cohesion: 0.25
Nodes (6): spend_active_card_resource(), spend_card_resource_as_heat(), Pago con recurso de carta (Dirigibles, Psychrophiles), test_dirigibles_passive_pays_venus_card_with_floaters(), test_spend_active_card_resource_decrements(), test_spend_active_card_resource_raises_if_not_enough()

### Community 47 - "GET /state (1)"
Cohesion: 0.25
Nodes (4): _card_catalog(), get_state(), list_players(), _player_or_404()

### Community 48 - "Tests generales del motor (12)"
Cohesion: 0.29
Nodes (6): apply_event_played_bonuses(), test_media_group_gives_3_mc_when_event_card_is_played(), test_multiple_passive_effects_stack(), test_on_event_played_puede_robar_cartas_con_su_propio_tag_filter(), test_optimal_aerobraking_only_triggers_on_space_events(), test_palladin_shipping_gana_titanio_por_evento_espacial()

### Community 49 - "Núcleo rules_engine y parámetros (2)"
Cohesion: 0.33
Nodes (4): GlobalParameterMaxedError, raise_global_parameter_without_bonuses(), Prelude bloque 3: preludes activos, test_raise_global_parameter_without_bonuses_al_tope_y_desconocido()

### Community 50 - "Tests generales del motor (13)"
Cohesion: 0.29
Nodes (6): resolve_research_phase(), test_resolve_research_phase_buying_zero_cards_is_valid(), test_resolve_research_phase_buys_selected_cards_at_standard_cost(), test_resolve_research_phase_free_cost_for_inventors_guild_style(), test_resolve_research_phase_insufficient_mc_raises(), test_resolve_research_phase_rejects_id_not_in_pending()

### Community 51 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 52 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 53 - "scripts/apply_db.py"
Cohesion: 0.33
Nodes (6): Nota: host Supabase resuelve solo por IPv6, Password con @ rompe psycopg2.connect(url), RLS activo en 11 tablas sin policies; backend usa clave secret, apply_db.py aplica schema+seeds idempotente, Prueba de humo contra Supabase real 19 de 19, Migracion a Supabase nuevo proyecto

### Community 54 - "Núcleo rules_engine y parámetros (3)"
Cohesion: 0.33
Nodes (5): is_blue_card(), Dry Deserts, Mud Slides, Solarnet Shutdown, Comprehensive FAQ v1.7: 4 bugs corregidos en Global Events, Global Events bloque 6 (3 pendientes, mazo completo), test_is_blue_card_classification_rule()

### Community 55 - "Fuera de alcance por diseño (1)"
Cohesion: 0.33
Nodes (6): Air Raid (C02), Crash Site Cleanup (X17), Herbivores: clausula de oponente, Law Suit (X06), Fuera de alcance por diseno, Rover Construction (038)

### Community 57 - "Docs del repo y README desactualizado (2)"
Cohesion: 0.40
Nodes (4): Modelo de datos Supabase (players, global_parameters, cards, queues, transactions), Bugs preexistentes (_load_player, schema.sql columnas, Manutech colonias), Stack: LangGraph, FastAPI, Supabase, Next.js, Docker, Dependencia supabase>=2.8.0

### Community 58 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 59 - "Tests generales del motor (14)"
Cohesion: 0.40
Nodes (4): apply_city_placed_bonuses(), test_pets_starts_with_1_animal_and_reacts_to_city_tiles(), test_tharsis_first_action_city_gratis_sin_produccion_del_proyecto_estandar(), test_tharsis_republic_gana_mc_al_colocarse_una_ciudad()

### Community 60 - "Tests generales del motor (15)"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 61 - "Tests generales del motor (16)"
Cohesion: 0.40
Nodes (4): start_research_phase(), test_start_research_phase_draws_fewer_if_deck_is_short(), test_start_research_phase_draws_n_cards_from_deck_top(), test_start_research_phase_fails_if_already_pending()

### Community 63 - "Preludes: jugada y snapshots"
Cohesion: 0.40
Nodes (4): Ecology Experts y Board of Directors (preludes 70 de 70), Jugar una carta dentro de otra (nested_card_id), Prelude bloque 2: 26 de 46 y bug de draw_cards_matching_tag, Bugs de cableado en tools.py (played_cards, discard_card_id, effect_choice, _load_player)

### Community 64 - "Fuera de alcance por diseño (2)"
Cohesion: 0.40
Nodes (5): Herbivores (147, cargada), Tabla de cartas de proyecto cargadas (~408), Protected Habitats (173), Stratopolis (corregida), VP impresos no se modelan (Interstellar Colony Ship, Public Celebrations)

### Community 65 - "Turmoil: núcleo político (2)"
Cohesion: 0.50
Nodes (4): Bloque 31 segunda tanda: cierre de pendientes, Self-Replicating Robots (210), Venus Orbital Survey (P88), WG Project (P91)

### Community 66 - "Fuera de alcance por diseño (3)"
Cohesion: 0.50
Nodes (4): Corporaciones bloques 3-5 (41 de 48), Nirgal Enterprises: Effect de awards/milestones, Philares: Effect de adyacencia con tiles de oponente, Valley Trust (first action reveal_preludes)

### Community 67 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 68 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 70 - "Registro CARDS_LOG y recursos tipados (2)"
Cohesion: 0.67
Nodes (3): Auditoria power/space: 42 de 62 mal, corregidas, tag_contact_sheet.py (hojas de contacto), Iconografia de tags: power vs space (auditoria de 62 cartas)

## Knowledge Gaps
- **134 isolated node(s):** `Generic place_special_tile parametrized by requirement`, `Global Events bloque 5 (multi-agente)`, `Tag comodin wild (Research Coordination)`, `Diversity Support (X20)`, `Seccion Pendientes (vacia)` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 442 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `apply_card_effect()` connect `Tests generales del motor (1)` to `Tests generales del motor (2)`, `Tests generales del motor (3)`, `Errores, producción e investigación (1)`, `Colonies: colonias, Pluto/Europa y descartes (1)`, `Núcleo rules_engine y parámetros (1)`, `Tools Supabase (1)`, `Tools Supabase (2)`, `Tests generales del motor (5)`, `Tests generales del motor (10)`, `Errores, producción e investigación (6)`, `Tests generales del motor (6)`, `Tests generales del motor (4)`, `Tests generales del motor (8)`, `Docs del repo y README desactualizado (1)`, `Registro CARDS_LOG y recursos tipados (1)`, `Errores, producción e investigación (2)`, `Tests generales del motor (16)`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `play_card()` connect `Errores, producción e investigación (1)` to `Tests generales del motor (1)`, `Tests generales del motor (3)`, `Colonies: colonias, Pluto/Europa y descartes (1)`, `Turmoil: núcleo político (1)`, `Tools Supabase (1)`, `Tools Supabase (2)`, `Tests generales del motor (5)`, `Marcadores: nomads y community`, `Tablero: greenery y special tiles`, `Tests generales del motor (7)`, `Docs del repo y README desactualizado (1)`, `Tablero: adyacencias (1)`, `Errores, producción e investigación (2)`, `Tablero: adyacencias (2)`, `Modelo Board (2)`, `Modelo Board (3)`, `Conversión y pasivos permanentes`, `Núcleo rules_engine y parámetros (1)`, `Tablero: adyacencias (3)`, `Tests generales del motor (9)`, `Tests generales del motor (11)`, `Errores, producción e investigación (4)`, `Tests generales del motor (12)`, `Errores, producción e investigación (7)`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `new_player_state()` connect `Tests generales del motor (2)` to `Tests generales del motor (1)`, `Tests generales del motor (3)`, `Errores, producción e investigación (1)`, `Colonies: colonias, Pluto/Europa y descartes (1)`, `Tests generales del motor (4)`, `Tests generales del motor (5)`, `Tests generales del motor (6)`, `First actions de corporaciones (motor) (1)`, `Tests generales del motor (7)`, `Tests generales del motor (8)`, `Errores, producción e investigación (2)`, `Errores, producción e investigación (3)`, `Turmoil: Ruling Bonus y TR Revision`, `Conversión y pasivos permanentes`, `resolve_ocean_offer`, `Núcleo rules_engine y parámetros (1)`, `Tests generales del motor (9)`, `Tests generales del motor (10)`, `Errores, producción e investigación (4)`, `Tests generales del motor (12)`, `Tests generales del motor (13)`, `Tests generales del motor (14)`, `Tests generales del motor (15)`, `Tests generales del motor (16)`, `_stratopolis_player()`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **What connects `Generic place_special_tile parametrized by requirement`, `Global Events bloque 5 (multi-agente)`, `Tag comodin wild (Research Coordination)` to the rest of the system?**
  _134 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.03029110936270653 - nodes in this community are weakly interconnected._
- **Should `Tests generales del motor (2)` be split into smaller, more focused modules?**
  _Cohesion score 0.0331739823265247 - nodes in this community are weakly interconnected._
- **Should `Tests generales del motor (3)` be split into smaller, more focused modules?**
  _Cohesion score 0.03939393939393939 - nodes in this community are weakly interconnected._