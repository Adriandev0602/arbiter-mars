# Graph Report - arbiter-mars  (2026-10-02)

## Corpus Check
- 52 files · ~179,832 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1635 nodes · 5262 edges · 99 communities (67 shown, 32 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 259 edges (avg confidence: 0.93)
- Token cost: 214,806 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor (1)
- Tools Supabase (tools.py) (1)
- Requisitos de cartas
- Turmoil: núcleo político (1)
- Núcleo rules_engine y parámetros (1)
- Colonies: colonias, Pluto/Europa y descartes
- Tests generales del motor (2)
- Parámetros globales y fixtures
- Cartas activas y recursos
- Acciones de cartas
- Errores, producción e investigación (1)
- Scripts de mantenimiento del catálogo
- Modelo Board
- Tablero: adyacencias
- First actions de corporaciones (motor)
- Tablero: greenery y special tiles
- Descuentos y pasivos por evento
- Núcleo rules_engine y parámetros (2)
- Config TypeScript
- Tools Supabase (tools.py) (2)
- Registro CARDS_LOG y recursos tipados (1)
- Grafo LangGraph
- API FastAPI (routes/schemas)
- Errores, producción e investigación (2)
- Las 3 cartas dudosas (cargadas)
- Marcadores: nomads y community (1)
- Errores, producción e investigación (3)
- Docs del repo y README desactualizado
- Bonus por recurso de carta ganado (1)
- package.json frontend
- Robo de preludes y Venus Orbital Survey (1)
- Visión del proyecto y alcance (1)
- Océanos en el tablero
- Efectos pasivos registrados
- Conversión y pasivos permanentes
- resolve_ocean_offer (Unity)
- Schema y base de datos
- Visión del proyecto y alcance (2)
- Océanos removibles y volcanes
- scripts/apply_db.py (schema + 4 seeds, i
- Turmoil: Ruling Bonus y TR Revision
- Robo de preludes y Venus Orbital Survey (2)
- Config y cliente Supabase
- Corporaciones: mecánicas resueltas
- Frontend: chat mockeado
- Pago de cartas
- devDependencies frontend
- Marcadores: nomads y community (2)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- Principio: el LLM nunca calcula
- Núcleo rules_engine y parámetros (3)
- Fuera de alcance por diseño (1)
- Entry point FastAPI
- Frontend: dashboard mockeado
- Visión del proyecto y alcance (3)
- Visión del proyecto y alcance (4)
- Fuentes del mapa Tharsis
- Pasivos por ciudad colocada
- Descuento de comercio
- Preludes: jugada y snapshots
- Fuera de alcance por diseño (2)
- Layout Next.js
- Scripts npm
- Tipos de recurso distintos
- Tools Supabase (tools.py) (3)
- Fuera de alcance por diseño (3)
- _stratopolis_player()
- Tests ruling_or_delegates
- dependencies frontend
- Volcanes y Noctis City
- GET /state
- Turmoil: núcleo político (2)
- Registro CARDS_LOG y recursos tipados (2)
- next.config
- Branch flow feat/review-block-N
- Diversity Support (min_distinct_resource
- Tools Supabase (tools.py) (4)
- Adyacencia precalculada
- Turmoil: núcleo político (3)
- Bonus por recurso de carta ganado (2)
- Global Events (36/36)
- Mapas alternativos (fuera)

## God Nodes (most connected - your core abstractions)
1. `new_player_state()` - 555 edges
2. `new_global_parameters()` - 457 edges
3. `apply_card_effect()` - 322 edges
4. `register_active_card()` - 157 edges
5. `check_card_requirements()` - 138 edges
6. `use_card_action()` - 117 edges
7. `CardRequirementNotMetError` - 106 edges
8. `PlayerState` - 104 edges
9. `register_passive_effect()` - 95 edges
10. `play_card()` - 68 edges

## Surprising Connections (you probably didn't know these)
- `TR Revision, Ruling Bonus, 6 Ruling Policies` --semantically_similar_to--> `apply_become_party_leader_bonus()`  [INFERRED] [semantically similar]
  AGENTS.md → backend/app/agent/rules_engine.py
- `Production phase and card payment (steel/titanium)` --references--> `run_production_phase()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `skip_first_tr_gain_per_generation (Preservation Program)` --references--> `_raise_tr()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `_increase_production single point (Manutech)` --references--> `_increase_production()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/rules_engine.py
- `Reds policy: diff at tools.py edge` --rationale_for--> `_apply_reds_ruling_policy()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Out-of-scope items** — agents_out_of_scope_milestones_awards, agents_out_of_scope_other_maps, backend_app_db_hex_map_research_ares_cross_payment, agents_out_of_scope_venus_solar_phase, agents_out_of_scope_solo_variant, agents_out_of_scope_autonomous_ai, agents_out_of_scope_multi_game, agents_out_of_scope_special_tiles_catalog [EXTRACTED 0.95]
- **Remaining pending work** — agents_frontend, agents_supabase_unreachable [EXTRACTED 0.95]
- **First actions de corporaciones resueltas** — backend_app_db_cards_log_first_actions_generic, backend_app_db_cards_log_valley_trust, backend_app_db_cards_log_celestic_first_action, backend_app_db_cards_log_philares_first_action, backend_app_db_cards_log_tharsis_first_action, backend_app_db_cards_log_aridor_first_action, backend_app_db_cards_log_poseidon_first_action, backend_app_db_cards_log_arcadian_first_action [EXTRACTED 1.00]
- **Exclusiones multijugador por diseno** — backend_app_db_cards_log_air_raid, backend_app_db_cards_log_law_suit, backend_app_db_cards_log_crash_site_cleanup, backend_app_db_cards_log_rover_construction, backend_app_db_cards_log_mons_insurance_opponent, backend_app_db_cards_log_herbivores_opponent_clause, backend_app_db_cards_log_philares_effect, backend_app_db_cards_log_nirgal_effect, backend_app_db_cards_log_protected_habitats [EXTRACTED 1.00]
- **T11 Recruitment completo: neutrales, track y Chairman TR** — backend_app_db_cards_log_t11_recruitment, backend_app_db_cards_log_neutral_delegates_official, backend_app_db_cards_log_global_event_party_cols, backend_app_db_cards_log_global_event_track, backend_app_db_cards_log_chairman_tr_bonus [EXTRACTED 1.00]
- **T11 closure (mechanism, migration, tech debt)** — agents_t11_neutral_delegates, agents_normalize_turmoil, agents_t11_tech_debt, agents_global_events_columns [INFERRED 0.85]
- **Static Tharsis board data model** — backend_app_db_hex_map_research_hex_table_61, backend_app_db_hex_map_research_precomputed_adjacency, backend_app_db_hex_map_research_ocean_hex_count_12, backend_app_db_hex_map_research_volcanic_hexes [INFERRED 0.85]

## Communities (99 total, 32 thin omitted)

### Community 0 - "Tests generales del motor (1)"
Cohesion: 0.03
Nodes (120): new_player_state(), test_acquired_company_gives_plus_3_mc_production(), test_adapted_lichen_gives_plus_1_plant_production(), test_aquifer_costs_18_mc_places_ocean_and_1_tr(), test_aquifer_released_places_ocean_without_granting_tr(), test_asteroid_card_raises_temperature_and_gives_titanium(), test_big_asteroid_raises_temperature_2_steps_and_gives_4_titanium(), test_black_polar_dust_places_ocean_and_changes_production() (+112 more)

### Community 1 - "Tools Supabase (tools.py) (1)"
Cohesion: 0.05
Nodes (63): Corporation first actions (effects.first_action, resolve_corporation_first_action), _load_player missing columns bug (KeyError), Nirgal and Philares Effect, on_ocean_placed_offer + resolve_ocean_offer (pending_ocean_offers), apply_card_played_vp_icon_bonus(), apply_colony_placed_bonuses(), apply_production_increased_bonus(), register_played_card() (+55 more)

### Community 2 - "Requisitos de cartas"
Cohesion: 0.04
Nodes (98): Wild tag (wild_tag_choice), CardRequirementNotMetError, check_card_requirements(), test_adaptation_technology_relaxes_global_requirements_2_steps(), test_advanced_ecosystems_multi_tag_requirements(), test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production(), test_archaebacteria_requires_max_temperature_minus_18() (+90 more)

### Community 3 - "Turmoil: núcleo político (1)"
Cohesion: 0.06
Nodes (64): global_events.revealed_party / current_party, normalize_turmoil auto-migration of old rows, T11 neutral delegates, official mechanism (14 neutrals, Global Event track, setup_global_events, Changing Times, Chairman +1 TR), Original T11 assumption: 2 fixed neutrals per party, T11 fixed-2-neutrals tech debt (resolved), Turmoil rulebook (TM_TURMOIL_ENG_RULES), _add_to_party(), can_play_party_gated_card() (+56 more)

### Community 4 - "Núcleo rules_engine y parámetros (1)"
Cohesion: 0.04
Nodes (47): adjust_mc_production(), apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_new_distinct_tag_bonuses(), apply_standard_project_used_bonuses(), compute_research_cost_per_card(), compute_standard_project_discount(), convert_heat_to_temperature() (+39 more)

### Community 5 - "Colonies: colonias, Pluto/Europa y descartes"
Cohesion: 0.06
Nodes (54): Colonies expansion and trading mechanic, Colony tiles 11/11 (Pluto, Europa added), Colonies rulebook (TM_COLONIES_ENG_RULES), Colony production did not trigger Manutech; build_colony KeyError, pending_card_discards + resolve_pending_discards (Pluto), Shared state (colonies, turmoil) must be snapshotted in smoke tests, add_colony_tile(), adjust_colony_track() (+46 more)

### Community 6 - "Tests generales del motor (2)"
Cohesion: 0.03
Nodes (67): apply_card_effect(), test_apply_card_effect_with_no_effects_is_a_noop(), test_archaebacteria_gives_plus_1_plant_production(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_artificial_photosynthesis_choice_1_gives_energy_production(), test_artificial_photosynthesis_requires_valid_effect_choice(), test_bribed_committee_raises_tr_2_steps_directly(), test_commercial_district_minus_1_energy_plus_4_mc_production() (+59 more)

### Community 7 - "Parámetros globales y fixtures"
Cohesion: 0.03
Nodes (64): new_global_parameters(), test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr(), test_asteroid_mining_gives_plus_2_titanium_production(), test_biomass_combustors_requires_6_oxygen(), test_callisto_penal_mines_gives_plus_3_mc_production(), test_check_card_requirements_none_or_empty_is_a_noop(), test_city_costs_25_mc_and_gives_1_mc_production(), test_comet_for_venus_raises_venus_omits_opponent_clause() (+56 more)

### Community 8 - "Cartas activas y recursos"
Cohesion: 0.04
Nodes (54): register_active_card(), test_accion_card_resource_delta_per_tag(), test_add_resource_to_all_matching_type(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_ants_action_moves_microbe_from_another_active_card(), test_any_card_resource_action_cost_spends_from_chosen_card() (+46 more)

### Community 9 - "Acciones de cartas"
Cohesion: 0.04
Nodes (53): use_card_action(), test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_accion_requires_zero_resource(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_any_card_resource_rejects_wrong_type_and_insufficient(), test_atmo_collectors_action_choice_add_or_spend_for_titanium_energy_heat(), test_business_network_minus_1_mc_production_and_repeatable_research_action(), test_card_action_available_again_after_production_phase() (+45 more)

### Community 10 - "Errores, producción e investigación (1)"
Cohesion: 0.05
Nodes (33): apply_any_tag_played_choice(), apply_hex_bonus_tile_bonuses(), _apply_production_floor(), CardEffectError, compute_reserved_card_discount(), deal_prelude_hand(), draw_random_preludes(), duplicate_reserved_card_resources() (+25 more)

### Community 11 - "Scripts de mantenimiento del catálogo"
Cohesion: 0.08
Nodes (12): main(), safe_filename(), build_image_url_index(), load_site_catalog(), main(), parse_pending_manifest(), connect(), load_corporations() (+4 more)

### Community 12 - "Modelo Board"
Cohesion: 0.10
Nodes (22): _build_adjacency(), _build_hex_defs(), count_adjacent_oceans(), count_adjacent_owned_by(), count_cathedrals(), count_empty_hexes_adjacent_to_owner(), count_tiles_adjacent_to_ocean(), count_tiles_of_type() (+14 more)

### Community 13 - "Tablero: adyacencias"
Cohesion: 0.11
Nodes (22): can_place_city(), can_place_city_adjacent_to_cities(), can_place_city_on_volcanic(), get_neighbors(), has_city_adjacent_to_ocean(), place_city_tile(), place_city_tile_adjacent_to_cities(), test_can_place_city_adjacent_to_cities_requires_min_count() (+14 more)

### Community 14 - "First actions de corporaciones (motor)"
Cohesion: 0.07
Nodes (29): Celestic: closed list of 33 floater-icon cards, corporation_cards table, corporation_review_queue, choose_corporation, Corporations 48/48, Vitor + on_card_played_with_vp_icon (excluded_card_ids list), apply_corporation_start(), consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching() (+21 more)

### Community 15 - "Tablero: greenery y special tiles"
Cohesion: 0.13
Nodes (24): can_place_greenery(), can_place_special_tile(), count_cities_and_special_tiles_adjacent_to_ocean(), InvalidPlacementError, new_board(), place_greenery_tile(), place_ocean_tile_on_land(), place_special_tile() (+16 more)

### Community 16 - "Descuentos y pasivos por evento"
Cohesion: 0.12
Nodes (24): apply_event_played_bonuses(), compute_card_cost_discount(), register_passive_effect(), test_anti_gravity_technology_discount_requires_7_science_tags(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_corridors_of_power_roba_al_volverse_party_leader(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter() (+16 more)

### Community 17 - "Núcleo rules_engine y parámetros (2)"
Cohesion: 0.11
Nodes (18): card_resource_payment (floaters/microbes pay cards), apply_tag_played_choice(), convert_plants_to_greenery(), InsufficientResourcesError, plants_per_greenery(), spend_active_card_resource(), spend_card_resource_as_heat(), standard_project_power_plant() (+10 more)

### Community 18 - "Config TypeScript"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 19 - "Tools Supabase (tools.py) (2)"
Cohesion: 0.14
Nodes (12): Comprehensive FAQ v1.7 (Jeffrey Anchan), Global Events 36/36, TR Revision, Ruling Bonus, 6 Ruling Policies, Turmoil core (6 parties, delegates, lobbying, influence), Old known gap: Unity not applied in resolve_ocean_offer, Unity in resolve_ocean_offer (gap closed; moved to pure engine), apply_become_party_leader_bonus(), _compute_player_influence() (+4 more)

### Community 20 - "Registro CARDS_LOG y recursos tipados (1)"
Cohesion: 0.12
Nodes (16): Cartas activas: accion repetible, Sistema de mazo / mano, Vocabulario de effects soportado en apply_card_effect, Vias de pago: acero/titanio, card_resource, stock_resource, standard_project_card_resource, Global Events bloque 5 (multi-agente), Colocaciones inversas en el tablero, optional_energy_to_heat (Supercapacitors), Efectos pasivos permanentes (+8 more)

### Community 21 - "Grafo LangGraph"
Cohesion: 0.17
Nodes (3): build_graph(), call_model(), AgentState

### Community 22 - "API FastAPI (routes/schemas)"
Cohesion: 0.20
Nodes (4): chat(), ChatRequest, ChatResponse, PlayerState

### Community 23 - "Errores, producción e investigación (2)"
Cohesion: 0.15
Nodes (9): CardNotInHandError, draw_cards_to_hand(), player_has_tag_swap_passive(), remove_card_from_hand(), swap_card_for_draw(), test_mars_university_passive_offers_discard_for_draw_on_matching_tag(), test_remove_card_from_hand_raises_if_not_present(), test_remove_card_from_hand_removes_it() (+1 more)

### Community 24 - "Las 3 cartas dudosas (cargadas)"
Cohesion: 0.14
Nodes (11): Air Raid exclusion (single-player), Card catalog (412 project cards, hand-verified), CARDS_LOG.md (card registry), 3 doubtful cards (self_replicating_robots, venus_orbital_survey, wg_project), Law Suit / Crash Site Cleanup exclusion (opponent-dependent), Clauses omitted by design (remove from any player, opponent-dependent, VP-only), Promo/Turmoil blocks 31-36, Review blocks 21-38 (engine pieces) (+3 more)

### Community 25 - "Marcadores: nomads y community (1)"
Cohesion: 0.19
Nodes (9): Board markers: nomad, cathedral, remove_greenery_tile, find_nomads(), HexOccupiedError, move_nomads(), place_nomads(), Marcadores en el tablero (nomad, cathedral, remove greenery), Kaguya Tech, Mars Nomads, Neptunian, St. Joseph (bloque 37), pending_ocean_offers + resolve_ocean_offer (+1 more)

### Community 26 - "Errores, producción e investigación (3)"
Cohesion: 0.14
Nodes (11): _increase_production single point (Manutech), _raise_tr single TR choke-point + tr_raised_this_generation, run_production_phase(), test_pristar_paga_solo_si_no_subio_el_tr_esta_generacion(), test_production_phase_base_case_tr_20_all_production_1(), test_production_phase_converts_leftover_energy_to_heat(), test_production_phase_mc_never_goes_negative_even_with_negative_production(), test_production_phase_optional_energy_requiere_el_pasivo() (+3 more)

### Community 27 - "Docs del repo y README desactualizado"
Cohesion: 0.19
Nodes (11): AGENTS.md (project context), board.py: Tharsis hex map, Supabase data model (players, global_parameters, cards, queues, transactions), HEX_MAP_RESEARCH.md, Inverse placements (Artificial Lake, Urbanized Area), Rules Arbiter for Terraforming Mars (project overview), schema.sql missing 7 columns on fresh DB, Migration block pattern in schema.sql (+3 more)

### Community 28 - "Bonus por recurso de carta ganado (1)"
Cohesion: 0.19
Nodes (10): apply_card_resource_gained_bonuses(), snapshot_card_resource_totals(), sum_card_resources_by_type(), Recursos tipados por carta activa (floaters), test_on_card_resource_gained_ignora_gastos_y_otros_tipos(), test_on_card_resource_gained_no_paga_por_mover_entre_cartas(), test_on_card_resource_gained_own_card_only_solo_cuenta_su_propia_carta(), test_on_card_resource_gained_paga_por_unidad_ganada() (+2 more)

### Community 29 - "package.json frontend"
Cohesion: 0.15
Nodes (12): name, private, version, autoprefixer, next, postcss, react-dom, tailwindcss (+4 more)

### Community 30 - "Robo de preludes y Venus Orbital Survey (1)"
Cohesion: 0.17
Nodes (9): Play a card inside another (nested_card_id, reveal_prelude), pending_prelude_draw / resolve_prelude_draw, Prelude setup draw (deal_prelude_hand/keep_preludes: 4 dealt, keep 2), Preludes 70/70, skip_first_tr_gain_per_generation (Preservation Program), deal_starting_hand(buy_with_research), Suitable Infrastructure: once per action production diff, start_prelude_draw() (+1 more)

### Community 31 - "Visión del proyecto y alcance (1)"
Cohesion: 0.17
Nodes (11): Autonomous AI playing humans, Milestones and awards (incl. Hoverlord, Venuphile), Simultaneous games, Hellas/Elysium maps, Official solo variant (TR 14, 14 generations), Hardcoded special tile catalog, Venus Solar Phase, In-scope list (chat sidebar, dashboard, Tharsis, Venus Next, Colonies, Prelude, Turmoil) (+3 more)

### Community 32 - "Océanos en el tablero"
Cohesion: 0.21
Nodes (10): can_place_ocean(), is_hex_empty(), place_ocean_tile(), Tile placement legality rules (ocean, greenery, city, special), test_can_place_ocean_only_on_ocean_hex(), test_new_board_is_empty(), test_place_ocean_tile_occupies_hex(), test_place_ocean_tile_on_land_hex_raises() (+2 more)

### Community 33 - "Efectos pasivos registrados"
Cohesion: 0.17
Nodes (11): apply_tag_played_resource_bonuses(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_on_tag_played_mc_delta_counts_each_matching_tag(), test_on_tag_played_resource_delta_generalizes_to_any_resource(), test_pharmacy_union_gasta_disease_y_sube_tr_con_tag_science(), test_point_luna_roba_carta_por_tag_earth(), test_sagitta_paga_segun_la_cantidad_exacta_de_tags() (+3 more)

### Community 34 - "Conversión y pasivos permanentes"
Cohesion: 0.17
Nodes (11): compute_conversion_rates(), Reds Ruling Policy en el borde de tools.py, Gap resolve_ocean_offer y Unity, Ruling Bonus de los 6 partidos, TR Revision (-1 TR por generacion), Turmoil: TR Revision, Ruling Bonus y Ruling Policy, Correccion regla Unity: titanio vale +1 M EUR extra, test_advanced_alloys_changes_calculate_card_payment_result() (+3 more)

### Community 35 - "resolve_ocean_offer (Unity)"
Cohesion: 0.27
Nodes (11): resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises(), test_resolve_ocean_offer_steel_overpayment_not_refunded(), test_resolve_ocean_offer_steel_worth_2_mc_each() (+3 more)

### Community 36 - "Schema y base de datos"
Cohesion: 0.24
Nodes (11): card_review_queue, cards, corporation_cards, corporation_review_queue, global_event_review_queue, global_events, global_parameters, players (+3 more)

### Community 37 - "Visión del proyecto y alcance (2)"
Cohesion: 0.20
Nodes (10): Deck/hand/research system, tags, passives, played_cards, Extensible effects/requirements vocabulary, pending_mc_discount / pending_requirement_tolerance_steps, Production phase and card payment (steel/titanium), rules_engine.py: pure rules engine, Six standard projects + conversions, Stratopolis fix (floaters; add 2 floaters to ANY Venus card), Tests: 703 passing at last retoma (715 in README) (+2 more)

### Community 38 - "Océanos removibles y volcanes"
Cohesion: 0.22
Nodes (6): can_place_ocean_on_land(), remove_greenery_tile(), remove_ocean_tile(), UnknownHexError, test_can_place_ocean_on_land_only_on_land_hex(), test_remove_ocean_tile_rejects_empty_hex_and_non_ocean()

### Community 39 - "scripts/apply_db.py (schema + 4 seeds, i"
Cohesion: 0.22
Nodes (8): scripts/apply_db.py (schema + 4 seeds, idempotent), Development commands (apply_db.py, pytest, uvicorn), Supabase host resolves IPv6 only, Smoke test on local Postgres 16 + PostgREST (14/14 flows), Repo structure, Supabase project unreachable (NXDOMAIN): restore, then push schema + seeds, scripts/apply_db.py, README quick start

### Community 40 - "Turmoil: Ruling Bonus y TR Revision"
Cohesion: 0.22
Nodes (8): apply_ruling_bonus(), test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production(), test_apply_ruling_bonus_mars_first_pays_per_building_tag(), test_apply_ruling_bonus_reds_raises_tr_only_if_20_or_below(), test_apply_ruling_bonus_scientists_pays_per_science_tag(), test_apply_ruling_bonus_unity_pays_per_venus_earth_jovian_tags(), test_apply_ruling_bonus_unknown_party_raises()

### Community 41 - "Robo de preludes y Venus Orbital Survey (2)"
Cohesion: 0.22
Nodes (8): resolve_research_phase(), test_business_contacts_starts_research_of_4_and_resolves_exactly_2(), test_inventors_guild_action_draws_1_card_to_pending_research(), test_resolve_research_phase_buying_zero_cards_is_valid(), test_resolve_research_phase_buys_selected_cards_at_standard_cost(), test_resolve_research_phase_free_cost_for_inventors_guild_style(), test_resolve_research_phase_insufficient_mc_raises(), test_resolve_research_phase_rejects_id_not_in_pending()

### Community 43 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.22
Nodes (9): Arcadian Communities: TileType community, Corporaciones bloque 2 (Ecotec a Manutech), Corporaciones: mecanicas pendientes resueltas (_raise_tr), _increase_production (Manutech), Manutech, Mons Insurance: clausulas de oponentes, Pharmacy Union (retire_card_as_event), Hook unico _raise_tr y tr_raised_this_generation (+1 more)

### Community 44 - "Frontend: chat mockeado"
Cohesion: 0.31
Nodes (5): Message, SidebarChat(), handleSend(), ChatResponse, sendChatMessage()

### Community 45 - "Pago de cartas"
Cohesion: 0.25
Nodes (7): calculate_card_payment(), test_calculate_card_payment_exact_mc(), test_calculate_card_payment_insufficient_raises(), test_calculate_card_payment_overpaying_gives_no_refund_but_no_error(), test_calculate_card_payment_steel_on_non_building_card_raises(), test_calculate_card_payment_with_steel_on_building_card(), test_calculate_card_payment_with_titanium_on_space_card()

### Community 46 - "devDependencies frontend"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 47 - "Marcadores: nomads y community (2)"
Cohesion: 0.38
Nodes (5): community_owner(), place_community(), test_community_exige_adyacencia_salvo_la_primera(), test_community_no_va_en_oceano_ni_en_hex_reservado(), test_community_reserva_el_hex_sin_ocuparlo()

### Community 48 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 49 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 51 - "Núcleo rules_engine y parámetros (3)"
Cohesion: 0.33
Nodes (5): is_blue_card(), Dry Deserts, Mud Slides, Solarnet Shutdown, Comprehensive FAQ v1.7: 4 bugs corregidos en Global Events, Global Events bloque 6 (3 pendientes, mazo completo), test_is_blue_card_classification_rule()

### Community 52 - "Fuera de alcance por diseño (1)"
Cohesion: 0.33
Nodes (6): Air Raid (C02), Crash Site Cleanup (X17), Herbivores: clausula de oponente, Law Suit (X06), Fuera de alcance por diseno, Rover Construction (038)

### Community 55 - "Visión del proyecto y alcance (3)"
Cohesion: 0.40
Nodes (4): card_review_queue workflow (queue empty), CARDS_PENDING_REVIEW.md (deprecated), Conventions (type hints, pure functions, tests with exact numbers, Spanish imperative commits), SUPABASE_DB_URL password with @ breaks psycopg2 URL parsing

### Community 56 - "Visión del proyecto y alcance (4)"
Cohesion: 0.40
Nodes (5): Frontend (Next.js, still mocked), LLM model via env var (Claude suggested), Stack: LangGraph, FastAPI, Supabase, Next.js, Docker, supabase >= 2.8.0 for new API keys, README next iteration: frontend

### Community 57 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 58 - "Pasivos por ciudad colocada"
Cohesion: 0.40
Nodes (4): apply_city_placed_bonuses(), test_pets_starts_with_1_animal_and_reacts_to_city_tiles(), test_tharsis_first_action_city_gratis_sin_produccion_del_proyecto_estandar(), test_tharsis_republic_gana_mc_al_colocarse_una_ciudad()

### Community 59 - "Descuento de comercio"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 60 - "Preludes: jugada y snapshots"
Cohesion: 0.40
Nodes (4): Ecology Experts y Board of Directors (preludes 70 de 70), Jugar una carta dentro de otra (nested_card_id), Prelude bloque 2: 26 de 46 y bug de draw_cards_matching_tag, Bugs de cableado en tools.py (played_cards, discard_card_id, effect_choice, _load_player)

### Community 61 - "Fuera de alcance por diseño (2)"
Cohesion: 0.40
Nodes (5): Herbivores (147, cargada), Tabla de cartas de proyecto cargadas (~408), Protected Habitats (173), Stratopolis (corregida), VP impresos no se modelan (Interstellar Colony Ship, Public Celebrations)

### Community 63 - "Scripts npm"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 64 - "Tipos de recurso distintos"
Cohesion: 0.50
Nodes (3): count_distinct_resource_types(), test_min_distinct_resource_types_cuenta_stock_y_recursos_de_carta(), test_min_distinct_resource_types_ignora_recursos_en_cero()

### Community 65 - "Tools Supabase (tools.py) (3)"
Cohesion: 0.50
Nodes (3): setup_colonies(), Colonies: mecanica de colonias/comercio (11 de 11 colonias), Colony bonus se cobra al comerciar siendo dueno (single-player)

### Community 66 - "Fuera de alcance por diseño (3)"
Cohesion: 0.50
Nodes (4): Corporaciones bloques 3-5 (41 de 48), Nirgal Enterprises: Effect de awards/milestones, Philares: Effect de adyacencia con tiles de oponente, Valley Trust (first action reveal_preludes)

### Community 67 - "_stratopolis_player()"
Cohesion: 0.50
Nodes (4): _stratopolis_player(), test_stratopolis_agrega_2_floaters_a_otra_carta_de_floaters(), test_stratopolis_puede_agregarse_floaters_a_si_misma(), test_stratopolis_rechaza_destino_que_no_guarda_floaters()

### Community 68 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 69 - "dependencies frontend"
Cohesion: 0.50
Nodes (4): dependencies, next, react, react-dom

### Community 72 - "Turmoil: núcleo político (2)"
Cohesion: 0.67
Nodes (3): Bloque 31 segunda tanda: cierre de pendientes, Self-Replicating Robots (210), WG Project (P91)

### Community 73 - "Registro CARDS_LOG y recursos tipados (2)"
Cohesion: 0.67
Nodes (3): Auditoria power/space: 42 de 62 mal, corregidas, tag_contact_sheet.py (hojas de contacto), Iconografia de tags: power vs space (auditoria de 62 cartas)

## Knowledge Gaps
- **150 isolated node(s):** `Config`, `Message`, `ChatResponse`, `allowJs`, `esModuleInterop` (+145 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 463 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `new_player_state()` connect `Tests generales del motor (1)` to `Requisitos de cartas`, `Núcleo rules_engine y parámetros (1)`, `Colonies: colonias, Pluto/Europa y descartes`, `Tests generales del motor (2)`, `Parámetros globales y fixtures`, `Cartas activas y recursos`, `Acciones de cartas`, `Errores, producción e investigación (1)`, `First actions de corporaciones (motor)`, `Descuentos y pasivos por evento`, `Núcleo rules_engine y parámetros (2)`, `Errores, producción e investigación (2)`, `Errores, producción e investigación (3)`, `Bonus por recurso de carta ganado (1)`, `Efectos pasivos registrados`, `Conversión y pasivos permanentes`, `resolve_ocean_offer (Unity)`, `Turmoil: Ruling Bonus y TR Revision`, `Robo de preludes y Venus Orbital Survey (2)`, `Pasivos por ciudad colocada`, `Descuento de comercio`, `Tipos de recurso distintos`, `_stratopolis_player()`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `apply_card_effect()` connect `Tests generales del motor (2)` to `Tests generales del motor (1)`, `Tools Supabase (tools.py) (1)`, `Requisitos de cartas`, `Núcleo rules_engine y parámetros (1)`, `Visión del proyecto y alcance (2)`, `Parámetros globales y fixtures`, `Cartas activas y recursos`, `Acciones de cartas`, `Errores, producción e investigación (1)`, `Robo de preludes y Venus Orbital Survey (2)`, `Descuentos y pasivos por evento`, `Núcleo rules_engine y parámetros (2)`, `Registro CARDS_LOG y recursos tipados (1)`, `Errores, producción e investigación (2)`, `Bonus por recurso de carta ganado (1)`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `AGENTS.md (project context)` connect `Docs del repo y README desactualizado` to `Visión del proyecto y alcance (2)`, `Principio: el LLM nunca calcula`, `Visión del proyecto y alcance (3)`, `Las 3 cartas dudosas (cargadas)`, `Visión del proyecto y alcance (1)`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **What connects `Config`, `Message`, `ChatResponse` to the rest of the system?**
  _150 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tests generales del motor (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.03147128245476003 - nodes in this community are weakly interconnected._
- **Should `Tools Supabase (tools.py) (1)` be split into smaller, more focused modules?**
  _Cohesion score 0.052100840336134456 - nodes in this community are weakly interconnected._
- **Should `Requisitos de cartas` be split into smaller, more focused modules?**
  _Cohesion score 0.039191919191919194 - nodes in this community are weakly interconnected._