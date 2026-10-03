# Graph Report - arbiter-mars  (2026-10-02)

## Corpus Check
- 52 files · ~176,973 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1598 nodes · 5217 edges · 94 communities (65 shown, 29 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 409 edges (avg confidence: 0.9)
- Token cost: 73,952 input · 0 output

## Community Hubs (Navigation)
- Tests generales del motor
- Requisitos de cartas
- Tools Supabase (tools.py)
- Colonies: colonias, Pluto/Europa y descartes
- apply_card_effect
- Parámetros globales y fixtures
- Turmoil: núcleo político
- Cartas activas y recursos
- Acciones de cartas
- Errores, producción e investigación
- Núcleo rules_engine y parámetros
- PlayerState y colocación con bonus
- Scripts de mantenimiento del catálogo
- Tablero: greenery y special tiles
- play_card y hook de producción
- Preludes: jugada y snapshots
- Tablero: adyacencias
- Efectos pasivos registrados
- Robo de preludes y Venus Orbital Survey
- Visión del proyecto y alcance
- Marcadores: nomads y community
- First actions de corporaciones (motor)
- Config TypeScript
- Descuentos y pasivos por evento
- Schema y base de datos
- Modelo Board
- API FastAPI (routes/schemas)
- Océanos en el tablero
- resolve_ocean_offer (Unity)
- Turmoil: Ruling Bonus y TR Revision
- Grafo LangGraph
- Reparto de preludes del setup
- Conversión y pasivos permanentes
- package.json frontend
- Construcción del mapa (board.py)
- Marcadores: greenery removible y catedral
- Bonus por recurso de carta ganado
- Hook de TR por generación
- Corporaciones: mecánicas resueltas
- Corporaciones: catálogo y setup
- First actions por corporación
- Ciudades en el tablero
- Registro CARDS_LOG y recursos tipados
- Config y cliente Supabase
- Fuera de alcance por diseño
- Frontend: chat mockeado
- Hook _increase_production (Manutech)
- Océanos removibles y volcanes
- Pago de cartas
- devDependencies frontend
- Global Events (36/36)
- Investigación del mapa y doc deprecado
- Stack y dependencias
- Docs del repo y README desactualizado
- Ruling Policy de los 6 partidos
- Entry point FastAPI
- Frontend: dashboard mockeado
- Las 3 cartas dudosas (cargadas)
- Principio: el LLM nunca calcula
- Fuentes del mapa Tharsis
- Elección por tag jugado
- Pasivos por ciudad colocada
- Descuento de comercio
- Layout Next.js
- Scripts npm
- Costo de investigación (Polyphemos/TerraLabs)
- Tipos de recurso distintos
- Herbivores y cláusulas omitidas
- Tests ruling_or_delegates
- dependencies frontend
- Volcanes y Noctis City
- GET /state
- next.config
- Auditoría de tags power/space
- Adyacencia precalculada
- CARDS_PENDING_REVIEW (deprecado)
- Contador de ciudades
- Fuente: scans hadronikle
- Mapas alternativos (fuera)

## God Nodes (most connected - your core abstractions)
1. `new_player_state()` - 554 edges
2. `new_global_parameters()` - 454 edges
3. `apply_card_effect()` - 323 edges
4. `register_active_card()` - 156 edges
5. `check_card_requirements()` - 138 edges
6. `use_card_action()` - 116 edges
7. `CardRequirementNotMetError` - 106 edges
8. `PlayerState` - 104 edges
9. `register_passive_effect()` - 97 edges
10. `play_card()` - 70 edges

## Surprising Connections (you probably didn't know these)
- `Starting hand purchase (3 MC per card)` --references--> `deal_starting_hand()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `pending_prelude_draw + resolve_prelude_draw (reveal N preludes, play 1)` --references--> `resolve_prelude_draw()`  [EXTRACTED]
  AGENTS.md → backend/app/agent/tools.py
- `Mapa hexagonal: Mining Area, Mining Rights, Land Claim` --references--> `place_special_tile()`  [INFERRED]
  backend/app/db/CARDS_LOG.md → backend/app/agent/board.py
- `Corporaciones bloque 1 (Aphrodite a EcoLine)` --implements--> `plants_per_greenery()`  [INFERRED]
  backend/app/db/CARDS_LOG.md → backend/app/agent/rules_engine.py
- `Tag comodin wild (Research Coordination)` --references--> `check_card_requirements()`  [INFERRED]
  backend/app/db/CARDS_LOG.md → backend/app/agent/rules_engine.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pure rules modules orchestrated by tools.py (only I/O layer)** — backend_app_agent_rules_engine, backend_app_agent_board, backend_app_agent_colonies, backend_app_agent_turmoil, backend_app_agent_tools [EXTRACTED 1.00]
- **Static Tharsis board data model** — backend_app_db_hex_map_research_hex_table_61, backend_app_db_hex_map_research_precomputed_adjacency, backend_app_db_hex_map_research_ocean_hex_count_12, backend_app_db_hex_map_research_volcanic_hexes [INFERRED 0.85]
- **Corporation first actions unified mechanism** — agents_corp_first_actions, agents_first_action_philares, agents_first_action_tharsis_republic, agents_first_action_valley_trust, agents_first_action_celestic [EXTRACTED 1.00]
- **Single choke-point refactors** — agents_raise_tr_choke_point, agents_increase_production_choke_point, agents_llm_never_does_math [INFERRED 0.75]
- **Prelude draw and setup flow** — agents_prelude_draw, agents_prelude_setup_dealing, agents_prelude_expansion [INFERRED 0.75]
- **First actions de corporaciones via pending_corporation_first_action** — backend_app_db_cards_log_first_action_philares, backend_app_db_cards_log_first_action_tharsis, backend_app_db_cards_log_first_action_aridor, backend_app_db_cards_log_first_action_poseidon, backend_app_db_cards_log_first_action_arcadian, backend_app_db_cards_log_valley_trust, backend_app_db_cards_log_celestic_first_action [EXTRACTED 1.00]
- **Puntos unicos de paso: _raise_tr, _increase_production, diff antes/despues** — backend_app_db_cards_log_raise_tr_hook, backend_app_db_cards_log_increase_production_refactor, backend_app_db_cards_log_on_card_resource_gained, backend_app_db_cards_log_policy_reds [INFERRED 0.75]
- **Marcadores de tablero resueltos juntos** — backend_app_db_cards_log_kaguya_tech, backend_app_db_cards_log_mars_nomads, backend_app_db_cards_log_st_joseph, backend_app_db_cards_log_arcadian_communities, backend_app_db_cards_log_board_markers [INFERRED 0.85]

## Communities (94 total, 29 thin omitted)

### Community 0 - "Tests generales del motor"
Cohesion: 0.03
Nodes (118): new_player_state(), test_adapted_lichen_gives_plus_1_plant_production(), test_aquifer_costs_18_mc_places_ocean_and_1_tr(), test_archaebacteria_gives_plus_1_plant_production(), test_artificial_photosynthesis_choice_1_gives_energy_production(), test_asteroid_card_raises_temperature_and_gives_titanium(), test_asteroid_costs_14_mc_raises_temp_2_degrees_and_1_tr(), test_big_asteroid_raises_temperature_2_steps_and_gives_4_titanium() (+110 more)

### Community 1 - "Requisitos de cartas"
Cohesion: 0.04
Nodes (99): CardRequirementNotMetError, check_card_requirements(), Requisitos de cartas (check_card_requirements), test_adaptation_technology_relaxes_global_requirements_2_steps(), test_advanced_ecosystems_multi_tag_requirements(), test_ai_central_requires_3_science_tags_action_draws_2(), test_algae_requires_5_oceans_and_gives_plant_resource_and_production(), test_anti_gravity_technology_discount_requires_7_science_tags() (+91 more)

### Community 2 - "Tools Supabase (tools.py)"
Cohesion: 0.07
Nodes (47): Pluto and Europa colonies (colonies 11/11), pending_card_discards + resolve_pending_discards, Prelude setup dealing (4 dealt, keep 2), Turmoil TR Revision, Ruling Bonus and Ruling Policies, _apply_reds_ruling_policy, _apply_reds_ruling_policy(), build_colony(), choose_corporation() (+39 more)

### Community 3 - "Colonies: colonias, Pluto/Europa y descartes"
Cohesion: 0.06
Nodes (55): Colonies expansion mechanic, add_colony_tile(), adjust_colony_track(), build_colony(), ColonyDef, ColonyFullError, ColonyOccupiedError, ColonyTileState (+47 more)

### Community 4 - "apply_card_effect"
Cohesion: 0.03
Nodes (65): apply_card_effect(), test_acquired_company_gives_plus_3_mc_production(), test_apply_card_effect_with_no_effects_is_a_noop(), test_aquifer_released_places_ocean_without_granting_tr(), test_artificial_photosynthesis_choice_0_gives_plant_production(), test_callisto_penal_mines_gives_plus_3_mc_production(), test_capped_counter_new_sources_colonies_hand_and_production(), test_cartel_mc_production_per_earth_tag_including_this() (+57 more)

### Community 5 - "Parámetros globales y fixtures"
Cohesion: 0.03
Nodes (62): new_global_parameters(), test_artificial_photosynthesis_requires_valid_effect_choice(), test_asteroid_mining_gives_plus_2_titanium_production(), test_black_polar_dust_places_ocean_and_changes_production(), test_bribed_committee_raises_tr_2_steps_directly(), test_building_industries_minus_1_energy_plus_2_steel_production(), test_business_contacts_starts_research_of_4_and_resolves_exactly_2(), test_city_costs_25_mc_and_gives_1_mc_production() (+54 more)

### Community 6 - "Turmoil: núcleo político"
Cohesion: 0.09
Nodes (43): Global Events (36 of 36), T11 Recruitment card, Turmoil political core, can_play_party_gated_card(), compute_influence(), exchange_neutral_delegate(), new_turmoil(), _party_total() (+35 more)

### Community 7 - "Cartas activas y recursos"
Cohesion: 0.03
Nodes (58): register_active_card(), test_accion_card_resource_delta_per_tag(), test_add_resource_to_all_matching_type(), test_aerial_mappers_action_choice_add_self_add_other_or_spend_to_draw(), test_aerobraked_ammonia_asteroid_targets_card_and_raises_production(), test_air_scrapping_expedition_raises_venus_and_adds_floaters_to_target(), test_ants_action_moves_microbe_from_another_active_card(), test_apply_card_effect_choice_threads_target_card_id() (+50 more)

### Community 8 - "Acciones de cartas"
Cohesion: 0.03
Nodes (58): use_card_action(), Cartas activas: accion repetible (use_card_action), target_card_resource_delta / move_from_target_card_resource_delta, test_accion_raise_global_parameter_without_bonuses_por_opcion(), test_accion_requires_zero_resource(), test_accion_target_min_resources_exige_recursos_en_el_destino(), test_any_card_resource_action_cost_spends_from_chosen_card(), test_any_card_resource_rejects_wrong_type_and_insufficient() (+50 more)

### Community 9 - "Errores, producción e investigación"
Cohesion: 0.05
Nodes (37): CardEffectError, CardNotInHandError, compute_reserved_card_discount(), duplicate_reserved_card_resources(), GlobalParameterMaxedError, player_has_optional_energy_to_heat(), raise_global_parameter_without_bonuses(), release_reserved_card() (+29 more)

### Community 10 - "Núcleo rules_engine y parámetros"
Cohesion: 0.07
Nodes (25): Rules engine capabilities (TR, params, standard projects, production phase), convert_heat_to_temperature(), convert_plants_to_greenery(), corporation_first_action_city(), corporation_first_action_greenery(), GlobalParameters, increment_events_played(), InsufficientResourcesError (+17 more)

### Community 11 - "PlayerState y colocación con bonus"
Cohesion: 0.08
Nodes (22): adjust_mc_production(), apply_cost_threshold_mc_bonuses(), apply_greenery_placed_bonuses(), apply_hex_bonus_tile_bonuses(), apply_standard_project_used_bonuses(), compute_standard_project_discount(), ocean_adjacency_bonus_mc(), place_ocean() (+14 more)

### Community 12 - "Scripts de mantenimiento del catálogo"
Cohesion: 0.08
Nodes (12): main(), safe_filename(), build_image_url_index(), load_site_catalog(), main(), parse_pending_manifest(), connect(), load_corporations() (+4 more)

### Community 13 - "Tablero: greenery y special tiles"
Cohesion: 0.12
Nodes (25): can_place_greenery(), can_place_special_tile(), count_cities_and_special_tiles_adjacent_to_ocean(), InvalidPlacementError, new_board(), place_greenery_tile(), place_ocean_tile_on_land(), place_special_tile() (+17 more)

### Community 14 - "play_card y hook de producción"
Cohesion: 0.08
Nodes (19): apply_become_party_leader_bonus(), apply_colony_placed_bonuses(), apply_new_distinct_tag_bonuses(), _apply_production_floor(), apply_tag_played_choice(), draw_cards_to_hand(), _increase_production(), increment_tags_played() (+11 more)

### Community 15 - "Preludes: jugada y snapshots"
Cohesion: 0.08
Nodes (22): apply_card_played_vp_icon_bonus(), apply_production_increased_bonus(), register_played_card(), resolve_active_card_starting_resources(), snapshot_production_totals(), _draw_cards_matching_requirement(), _draw_cards_matching_tag(), play_prelude() (+14 more)

### Community 16 - "Tablero: adyacencias"
Cohesion: 0.10
Nodes (16): can_place_city_adjacent_to_cities(), can_place_ocean_on_land(), count_empty_hexes_adjacent_to_owner(), get_neighbors(), place_city_tile_adjacent_to_cities(), Mapa hexagonal: Mining Area, Mining Rights, Land Claim, Colocaciones inversas en el tablero (board.py), test_can_place_city_adjacent_to_cities_requires_min_count() (+8 more)

### Community 17 - "Efectos pasivos registrados"
Cohesion: 0.10
Nodes (26): apply_tag_played_resource_bonuses(), register_passive_effect(), test_corridors_of_power_roba_al_volverse_party_leader(), test_decomposers_passive_adds_microbes_on_bio_tags(), test_ecoline_paga_7_plantas_por_greenery(), test_ecological_zone_passive_adds_animals_on_animal_or_plant_tags(), test_influence_bonus_passive_stored(), test_ocean_adjacency_bonus_mc_override() (+18 more)

### Community 18 - "Robo de preludes y Venus Orbital Survey"
Cohesion: 0.09
Nodes (18): _load_player missing flags bug, prelude_draw_candidates(), resolve_research_phase(), reveal_top_cards_take_tag(), start_prelude_draw(), take_pending_prelude(), _load_player, _reveal_random_preludes() (+10 more)

### Community 19 - "Visión del proyecto y alcance"
Cohesion: 0.10
Nodes (20): Autonomous AI opponent, Branch flow feat/review-block-N, Card resource payment, card_review_queue (Supabase), Frontend (Next.js, 100% mocked), Alternative maps Hellas/Elysium, Milestones and awards, Multiple simultaneous games (+12 more)

### Community 20 - "Marcadores: nomads y community"
Cohesion: 0.14
Nodes (13): community_owner(), find_nomads(), HexOccupiedError, is_hex_empty(), move_nomads(), place_community(), place_nomads(), test_community_exige_adyacencia_salvo_la_primera() (+5 more)

### Community 21 - "First actions de corporaciones (motor)"
Cohesion: 0.12
Nodes (14): apply_corporation_start(), consume_corporation_first_action(), register_corporation_first_action(), reveal_cards_until_matching(), test_apply_corporation_start_pone_produccion_en_cero(), test_celestic_first_action_reveal_until_matching_se_anota_una_sola_vez(), test_consume_corporation_first_action_se_usa_una_sola_vez(), test_philares_first_action_greenery_gratis_sube_oxigeno_y_tr() (+6 more)

### Community 22 - "Config TypeScript"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 23 - "Descuentos y pasivos por evento"
Cohesion: 0.12
Nodes (15): apply_event_played_bonuses(), compute_card_cost_discount(), test_card_cost_discount_accepts_tag_filter_list(), test_card_cost_discount_requires_requirement(), test_compute_card_cost_discount_with_no_passive_effects_is_0(), test_earth_catapult_discount_applies_to_all_cards_no_tag_filter(), test_earth_office_discount_only_applies_to_earth_tag(), test_mass_converter_discount_does_not_apply_to_non_space_cards() (+7 more)

### Community 24 - "Schema y base de datos"
Cohesion: 0.17
Nodes (15): Smoke test on local Postgres 16 + PostgREST, schema.sql fresh-DB missing columns bug, Supabase (Postgres) database, Supabase project paused / real-DB smoke test pending, card_review_queue, cards, corporation_cards, corporation_review_queue (+7 more)

### Community 25 - "Modelo Board"
Cohesion: 0.20
Nodes (11): count_adjacent_oceans(), count_adjacent_owned_by(), count_tiles_of_type(), get_adjacent_tiles(), HexState, _place(), resolve_hex_bonus(), resolve_ocean_adjacency_bonus() (+3 more)

### Community 26 - "API FastAPI (routes/schemas)"
Cohesion: 0.18
Nodes (4): chat(), ChatRequest, ChatResponse, PlayerState

### Community 27 - "Océanos en el tablero"
Cohesion: 0.14
Nodes (13): can_place_ocean(), count_tiles_adjacent_to_ocean(), place_ocean_tile(), Dry Deserts, Global Events bloque 6 (3 pendientes: Dry Deserts, Mud Slides, Solarnet Shutdown), Mud Slides, Solarnet Shutdown, Tile placement legality rules (ocean, greenery, city, special) (+5 more)

### Community 28 - "resolve_ocean_offer (Unity)"
Cohesion: 0.22
Nodes (13): Neptunian Power Consultants ocean offer, Unity / resolve_ocean_offer gap, resolve_ocean_offer(), _neptunian_player(), test_resolve_ocean_offer_advanced_alloys_steel_bonus_applies(), test_resolve_ocean_offer_insufficient_mc_raises(), test_resolve_ocean_offer_pays_5_mc(), test_resolve_ocean_offer_steel_not_allowed_raises() (+5 more)

### Community 29 - "Turmoil: Ruling Bonus y TR Revision"
Cohesion: 0.14
Nodes (13): _raise_tr single TR choke-point, _raise_tr, apply_ruling_bonus(), Ruling Bonus de los 6 partidos, TR Revision (-1 TR por generacion), Turmoil: TR Revision, Ruling Bonus y Ruling Policy (COMPLETO), test_apply_ruling_bonus_greens_pays_per_plant_microbe_animal_tags(), test_apply_ruling_bonus_kelvinists_pays_per_heat_production() (+5 more)

### Community 30 - "Grafo LangGraph"
Cohesion: 0.19
Nodes (3): build_graph(), call_model(), AgentState

### Community 31 - "Reparto de preludes del setup"
Cohesion: 0.16
Nodes (8): deal_prelude_hand(), draw_random_preludes(), initialize_deck(), keep_preludes(), remove_prelude_from_hand(), Reparto de preludes en setup (4 repartidas, quedarse con 2), test_draw_random_preludes_is_seeded_distinct_and_respects_exclude(), test_initialize_deck_shuffles_but_keeps_same_cards()

### Community 32 - "Conversión y pasivos permanentes"
Cohesion: 0.15
Nodes (11): compute_conversion_rates(), swap_card_for_draw(), Gap resolve_ocean_offer y Unity, Efectos pasivos permanentes (register_passive_effect), Ruling Policy Unity (titanio +1 M€), test_advanced_alloys_changes_calculate_card_payment_result(), test_advanced_alloys_raises_steel_and_titanium_conversion_rates(), test_compute_conversion_rates_unity_ruling_leaves_steel_unchanged() (+3 more)

### Community 33 - "package.json frontend"
Cohesion: 0.15
Nodes (12): name, private, version, autoprefixer, next, postcss, react-dom, tailwindcss (+4 more)

### Community 34 - "Construcción del mapa (board.py)"
Cohesion: 0.23
Nodes (6): Hexagonal board Tharsis (61 hexes), _build_adjacency(), _build_hex_defs(), HexDef, _neighbor_coords(), _row()

### Community 35 - "Marcadores: greenery removible y catedral"
Cohesion: 0.20
Nodes (9): count_cathedrals(), place_cathedral(), remove_greenery_tile(), Marcadores en el tablero (bloque 37): nomad, cathedral, remove greenery, Kaguya Tech (X58), Mars Nomads (X59), Neptunian Power Consultants (X61), St. Joseph of Cupertino Mission (X64) (+1 more)

### Community 36 - "Bonus por recurso de carta ganado"
Cohesion: 0.23
Nodes (10): apply_card_resource_gained_bonuses(), snapshot_card_resource_totals(), Bloque 33: X20 Diversity Support desbloqueada, Diversity Support (X20), Retrofit active_card_resource_type microbio/animal (11+13 cartas), on_card_resource_gained: pasivo por diff de totales (bloque 34), test_on_card_resource_gained_ignora_gastos_y_otros_tipos(), test_on_card_resource_gained_no_paga_por_mover_entre_cartas() (+2 more)

### Community 37 - "Hook de TR por generación"
Cohesion: 0.17
Nodes (11): raise_temperature(), test_on_temperature_raised_no_paga_pasos_no_aplicados(), test_on_temperature_raised_paga_por_paso_aplicado(), test_preservation_program_anula_el_primer_paso_de_tr_de_la_generacion(), test_pristar_paga_solo_si_no_subio_el_tr_esta_generacion(), test_raise_temperature_at_max_raises(), test_raise_temperature_caps_at_max_and_only_grants_tr_for_applied_steps(), test_raise_temperature_one_step_is_2_degrees_and_1_tr() (+3 more)

### Community 38 - "Corporaciones: mecánicas resueltas"
Cohesion: 0.20
Nodes (11): Arcadian Communities (community marker), Corporaciones: mecanicas pendientes resueltas (47 de 48), Pharmacy Union, Pristar, Hook unico _raise_tr: tr_raised_this_generation, Sagitta Frontier Services, Stormcraft Incorporated (card_resource_as_heat), United Nations Mars Initiative (+3 more)

### Community 39 - "Corporaciones: catálogo y setup"
Cohesion: 0.18
Nodes (12): Celestic first action (reveal_until_matching, 33 cartas floater), Corporaciones bloque 1 (Aphrodite a EcoLine), Clausulas de setup de corporaciones, Corporaciones: categoria que faltaba (corporation_cards, 48 de 48), First action Arcadian (community), First action Aridor (add_colony_tile), First action Philares (greenery), First action Poseidon (colonia gratis) (+4 more)

### Community 40 - "First actions por corporación"
Cohesion: 0.18
Nodes (11): Celestic closed list of 33 floater cards, Corporation first actions (effects.first_action), First action: arcadian, First action: aridor, First action: celestic, First action: philares, First action: poseidon, First action: tharsis_republic (+3 more)

### Community 41 - "Ciudades en el tablero"
Cohesion: 0.31
Nodes (9): can_place_city(), has_city_adjacent_to_ocean(), place_city_tile(), test_can_place_city_on_volcanic_ignores_city_adjacency(), test_cannot_place_city_adjacent_to_another_city(), test_cannot_place_city_on_noctis_city_reserved_hex(), test_has_city_adjacent_to_ocean_filtra_por_dueno(), test_has_city_adjacent_to_ocean_ignora_ciudad_lejos_del_agua() (+1 more)

### Community 42 - "Registro CARDS_LOG y recursos tipados"
Cohesion: 0.20
Nodes (7): sum_card_resources_by_type(), Seccion Pendientes (por mecanica): vacia, CARDS_LOG: registro de cartas cargadas/pendientes/fuera de alcance, Herramienta tag_contact_sheet.py (hojas de contacto de tags), Iconografia de tags: power vs space (auditoria 62 cartas), Recursos tipados por carta activa (floaters entre cartas), Tag comodin wild (Research Coordination)

### Community 44 - "Fuera de alcance por diseño"
Cohesion: 0.28
Nodes (9): Air Raid (C02), Corporaciones bloques 3-5 (41 de 48), Crash Site Cleanup (X17), Law Suit (X06), Nirgal Enterprises: Effect de milestones/awards a 0 M€, Fuera de alcance por diseño, Philares: Effect de adyacencia con tile de oponente, Protected Habitats (173) (+1 more)

### Community 45 - "Frontend: chat mockeado"
Cohesion: 0.31
Nodes (5): Message, SidebarChat(), handleSend(), ChatResponse, sendChatMessage()

### Community 46 - "Hook _increase_production (Manutech)"
Cohesion: 0.25
Nodes (8): _increase_production single production choke-point (Manutech), _increase_production, Correcciones de cableado de colonias (Manutech, Reds, KeyError), Corporaciones bloque 2 (Ecotec a Manutech), Refactor _increase_production (punto unico de aumentos de produccion), Bug: update corporation_id=null sobrante de Manutech en seed, Manutech (on_production_increased), Mons Insurance (casi todo multijugador)

### Community 47 - "Océanos removibles y volcanes"
Cohesion: 0.29
Nodes (5): can_place_city_on_volcanic(), remove_ocean_tile(), UnknownHexError, test_can_place_city_on_volcanic_rejects_non_volcanic_hex(), test_remove_ocean_tile_rejects_empty_hex_and_non_ocean()

### Community 48 - "Pago de cartas"
Cohesion: 0.25
Nodes (7): calculate_card_payment(), test_calculate_card_payment_exact_mc(), test_calculate_card_payment_insufficient_raises(), test_calculate_card_payment_overpaying_gives_no_refund_but_no_error(), test_calculate_card_payment_steel_on_non_building_card_raises(), test_calculate_card_payment_with_steel_on_building_card(), test_calculate_card_payment_with_titanium_on_space_card()

### Community 49 - "devDependencies frontend"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 50 - "Global Events (36/36)"
Cohesion: 0.29
Nodes (6): _resolve_capped_counter(), Comprehensive FAQ v1.7: 4 bugs corregidos en Global Events, Global Events bloque 5 (22 por 4 agentes), Turmoil: Global Events (36 de 36), Reparto de delegados neutrales y ciclo de generaciones de Global Events no automatizados, Rulebook dice 31 Global Events, indice trae 36 (sin explicar)

### Community 51 - "Investigación del mapa y doc deprecado"
Cohesion: 0.29
Nodes (5): CARDS_PENDING_REVIEW.md (deprecated manifest, status: deprecated), card_review_queue (Supabase table replacing manifest), CARDS_LOG.md, tm.hadronikle.com (unofficial card scan source), HEX_MAP_RESEARCH.md (Tharsis hex board research)

### Community 52 - "Stack y dependencias"
Cohesion: 0.29
Nodes (6): fastapi 0.115.0, langchain-anthropic 0.2.3, langgraph 0.2.34, psycopg2-binary 2.9.9, supabase 2.31.0, docker-compose.yml (backend service)

### Community 53 - "Docs del repo y README desactualizado"
Cohesion: 0.33
Nodes (4): Corporations catalog (48 of 48), graphify-out (project knowledge graph), Corporate Era expansion, README.md (English public overview)

### Community 54 - "Ruling Policy de los 6 partidos"
Cohesion: 0.33
Nodes (6): Ruling Policy Greens (+4 M€ por greenery), Ruling Policy Kelvinists, Ruling Policy Mars First (+1 acero por tile), Ruling Policy Reds (-3 M€ por paso de TR), Ruling Policy Scientists (10 M€ por 3 cartas), Ruling Policy de los 6 partidos

### Community 57 - "Las 3 cartas dudosas (cargadas)"
Cohesion: 0.40
Nodes (5): Project card catalog (408 cards), pending_prelude_draw + resolve_prelude_draw (reveal N preludes, play 1), Card self_replicating_robots, Card venus_orbital_survey, Card wg_project

### Community 59 - "Fuentes del mapa Tharsis"
Cohesion: 0.40
Nodes (4): HEX_DEFS, 61-hex table (9 rows 5,6,7,8,9,8,7,6,5; ids 03-63), rulespal.com official rulebook transcript, TharsisBoard.ts (terraforming-mars/terraforming-mars)

### Community 60 - "Elección por tag jugado"
Cohesion: 0.40
Nodes (4): apply_any_tag_played_choice(), Viral Enhancers (on_any_tag_played_choice), test_any_tag_played_choice_target_any_card(), test_viral_enhancers_any_tag_played_choice_add_or_gain()

### Community 61 - "Pasivos por ciudad colocada"
Cohesion: 0.40
Nodes (4): apply_city_placed_bonuses(), test_pets_starts_with_1_animal_and_reacts_to_city_tiles(), test_tharsis_first_action_city_gratis_sin_produccion_del_proyecto_estandar(), test_tharsis_republic_gana_mc_al_colocarse_una_ciudad()

### Community 62 - "Descuento de comercio"
Cohesion: 0.40
Nodes (4): compute_trade_cost_discount(), test_compute_trade_cost_discount_from_passive(), test_cryo_sleep_passive_trade_discount(), test_rim_freighters_passive_trade_discount()

### Community 64 - "Scripts npm"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 65 - "Costo de investigación (Polyphemos/TerraLabs)"
Cohesion: 0.50
Nodes (3): compute_research_cost_per_card(), Polyphemos/TerraLabs: compra de mano inicial a 3 M€ por carta, test_research_cost_por_carta_lo_corren_polyphemos_y_terralabs()

### Community 66 - "Tipos de recurso distintos"
Cohesion: 0.50
Nodes (3): count_distinct_resource_types(), test_min_distinct_resource_types_cuenta_stock_y_recursos_de_carta(), test_min_distinct_resource_types_ignora_recursos_en_cero()

### Community 67 - "Herbivores y cláusulas omitidas"
Cohesion: 0.50
Nodes (3): Vocabulario de effects en apply_card_effect, Herbivores (147) cargada, Herbivores (147): clausula de reducir produccion de plantas de otro jugador

### Community 68 - "Tests ruling_or_delegates"
Cohesion: 0.50
Nodes (4): test_ruling_or_delegates_fails_otherwise(), test_ruling_or_delegates_passes_when_party_is_ruling(), test_ruling_or_delegates_passes_with_enough_own_delegates(), _turmoil_stub()

### Community 69 - "dependencies frontend"
Cohesion: 0.50
Nodes (4): dependencies, next, react, react-dom

## Ambiguous Edges - Review These
- `README.md (English public overview)` → `Corporations catalog (48 of 48)`  [AMBIGUOUS]
  README.md · relation: references

## Knowledge Gaps
- **142 isolated node(s):** `Config`, `Message`, `ChatResponse`, `allowJs`, `esModuleInterop` (+137 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 441 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `README.md (English public overview)` and `Corporations catalog (48 of 48)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `new_player_state()` connect `Tests generales del motor` to `Requisitos de cartas`, `Colonies: colonias, Pluto/Europa y descartes`, `apply_card_effect`, `Parámetros globales y fixtures`, `Cartas activas y recursos`, `Acciones de cartas`, `Errores, producción e investigación`, `Núcleo rules_engine y parámetros`, `PlayerState y colocación con bonus`, `play_card y hook de producción`, `Efectos pasivos registrados`, `Robo de preludes y Venus Orbital Survey`, `First actions de corporaciones (motor)`, `Descuentos y pasivos por evento`, `resolve_ocean_offer (Unity)`, `Turmoil: Ruling Bonus y TR Revision`, `Conversión y pasivos permanentes`, `Bonus por recurso de carta ganado`, `Hook de TR por generación`, `Elección por tag jugado`, `Pasivos por ciudad colocada`, `Descuento de comercio`, `Costo de investigación (Polyphemos/TerraLabs)`, `Tipos de recurso distintos`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `apply_card_effect()` connect `apply_card_effect` to `Tests generales del motor`, `Requisitos de cartas`, `Tools Supabase (tools.py)`, `Herbivores y cláusulas omitidas`, `Hook de TR por generación`, `Parámetros globales y fixtures`, `Cartas activas y recursos`, `Acciones de cartas`, `Errores, producción e investigación`, `Núcleo rules_engine y parámetros`, `PlayerState y colocación con bonus`, `Registro CARDS_LOG y recursos tipados`, `play_card y hook de producción`, `Preludes: jugada y snapshots`, `Global Events (36/36)`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Arbitro Asistente de Reglas para Terraforming Mars` connect `Visión del proyecto y alcance` to `Tools Supabase (tools.py)`, `Hook _increase_production (Manutech)`, `Investigación del mapa y doc deprecado`, `Docs del repo y README desactualizado`, `Schema y base de datos`, `Las 3 cartas dudosas (cargadas)`, `Principio: el LLM nunca calcula`, `Turmoil: Ruling Bonus y TR Revision`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `apply_card_effect()` (e.g. with `Vocabulario de effects en apply_card_effect` and `Turmoil: Global Events (36 de 36)`) actually correct?**
  _`apply_card_effect()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `check_card_requirements()` (e.g. with `Requisitos de cartas (check_card_requirements)` and `Turmoil: nucleo politico (Colonial Envoys, Colonial Representation)`) actually correct?**
  _`check_card_requirements()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Message`, `ChatResponse` to the rest of the system?**
  _142 weakly-connected nodes found - possible documentation gaps or missing edges._