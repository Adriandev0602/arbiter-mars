# Registro de cartas cargadas

Control de qué cartas del catálogo (~668 en la base de tm.hadronikle.com, ~200 son
de proyecto) ya están en `seed_cards.sql` con efecto implementado y testeado, para
no reverificar ni repetir trabajo en sesiones futuras.

No borrar filas al implementar una carta nueva — solo agregar.

**Regla de oro: no descartar cartas por falta de mecánica.** Si un efecto no encaja en el
vocabulario actual, la prioridad es extender el motor (nueva pieza en `apply_card_effect`,
`use_card_action`, o lo que haga falta) y agregar la carta con su test — no dejarla afuera.
"Descartada" es solo para el puñado de casos genuinamente irreducibles con el diseño actual
(típicamente: requieren un segundo jugador/tablero — el MVP es de un solo jugador — o
requieren el mapa hexagonal con adyacencia, que está fuera de alcance por decisión explícita
de sección 6 de CLAUDE.md, no por falta de tiempo). Cuando dudes, extendé el motor.

## Cargadas (en `seed_cards.sql`, con efecto en `apply_card_effect` y test)

| id | Nombre | # scan | Costo | Efecto |
|---|---|---|---|---|
| `sponsors` | Sponsors | 068 | 6 MC | +2 producción MC |
| `acquired_company` | Acquired Company | 106 | 10 MC | +3 producción MC |
| `investment_loan` | Investment Loan | 151 | 3 MC | -1 producción MC, +10 MC |
| `insulation` | Insulation | 152 | 2 MC | -X producción calor, +X producción MC (X a elección) |
| `nuclear_power` | Nuclear Power | 045 | 10 MC | -2 producción MC, +3 producción energía |
| `solar_power` | Solar Power | 113 | 11 MC | +1 producción energía |
| `titanium_mine` | Titanium Mine | 144 | 7 MC | +1 producción titanio |
| `solar_wind_power` | Solar Wind Power | 077 | 11 MC | +1 producción energía, +2 titanio (stock) |
| `artificial_photosynthesis` | Artificial Photosynthesis | 115 | 12 MC | Elección: +1 producción plantas O +2 producción energía |
| `mine` | Mine | 056 | 4 MC | +1 producción steel |
| `farming` | Farming | 118 | 16 MC | Requiere +4°C o más. +2 producción MC, +2 producción plantas, +2 plantas (stock) |
| `nitrophilic_moss` | Nitrophilic Moss | 146 | 8 MC | Requiere 3 océanos colocados. -2 plantas (costo obligatorio), +2 producción plantas |
| `ironworks` | Ironworks | 101 | 11 MC | Acción repetible: -4 energía, +1 steel, +1 paso oxígeno |
| `steelworks` | Steelworks | 103 | 15 MC | Acción repetible: -4 energía, +2 steel, +1 paso oxígeno |
| `regolith_eaters` | Regolith Eaters | 033 | 13 MC | Acción repetible con elección: +1 microbio (en la carta) O -2 microbios/+1 paso oxígeno |
| `comet` | Comet | 010 | 21 MC | +1 paso temperatura, coloca 1 océano (+2 TR) |
| `asteroid_card` | Asteroid | 009 | 14 MC | +1 paso temperatura, +2 titanio |
| `big_asteroid` | Big Asteroid | 011 | 27 MC | +2 pasos temperatura, +4 titanio |
| `capital` | Capital | 008 | 26 MC | Requiere 4 océanos. -2 producción energía, +5 producción MC, +1 ciudad (contador) |
| `martian_rails` | Martian Rails | 007 | 13 MC | Acción repetible: -1 energía → +1 MC por cada ciudad en Marte |
| `space_elevator` | Space Elevator | 013 | 27 MC | +1 producción titanio; acción repetible: -1 steel → +5 MC |
| `equatorial_magnetizer` | Equatorial Magnetizer | 015 | 11 MC | Acción repetible: -1 producción energía → +1 TR |
| `water_import_from_europa` | Water Import from Europa | 012 | 25 MC | Acción repetible: -12 MC → coloca 1 océano |
| `advanced_alloys` | Advanced Alloys | 071 | 9 MC | Pasivo permanente: steel y titanio valen +1 MC extra al pagar cartas |
| `media_group` | Media Group | 109 | 6 MC | Pasivo permanente: +3 MC cada vez que se juega un evento |
| `optimal_aerobraking` | Optimal Aerobraking | 031 | 7 MC | Pasivo permanente: +3 MC y +3 calor cada vez que se juega un evento con tag space |
| `mass_converter` | Mass Converter | 094 | 8 MC | Requiere 5 tags de ciencia jugados. Pasivo: cartas espaciales cuestan 2 MC menos; acción repetible: -6 energía → +6 producción energía |
| `inventors_guild` | Inventors' Guild | 006 | 9 MC | Acción repetible: roba 1 carta a investigación pendiente (compra a costo 0 vía `resolve_research_phase`) |
| `development_center` | Development Center | 014 | 11 MC | Acción repetible: -1 energía → roba 1 carta directo a la mano |
| `domed_crater` | Domed Crater | 016 | 24 MC | Requiere oxígeno ≤7%. +3 plantas, -1 producción energía, +3 producción MC, +1 ciudad |
| `noctis_city` | Noctis City | 017 | 18 MC | -1 producción energía, +3 producción MC, +1 ciudad |
| `methane_from_titan` | Methane from Titan | 018 | 28 MC | Requiere oxígeno ≥2%. +2 producción calor, +2 producción plantas |
| `research_outpost` | Research Outpost | 020 | 18 MC | Pasivo: -1 MC en TODAS las cartas futuras (sin tag_filter); +1 ciudad |
| `phobos_space_haven` | Phobos Space Haven | 021 | 25 MC | +1 producción titanio, +1 ciudad |
| `black_polar_dust` | Black Polar Dust | 022 | 15 MC | Coloca 1 océano, -2 producción MC, +3 producción calor |
| `arctic_algae` | Arctic Algae | 023 | 12 MC | Requiere temperatura ≤-12°C. +1 planta. Pasivo: +2 plantas cada vez que se coloca un océano (cualquier fuente) |
| `space_station` | Space Station | 025 | 10 MC | Pasivo: cartas espaciales cuestan 2 MC menos |
| `interstellar_colony_ship` | Interstellar Colony Ship | 027 | 24 MC | Requiere 5 tags de ciencia jugados. Sin efecto de tablero (solo puntos, no trackeados) |
| `security_fleet` | Security Fleet | 028 | 12 MC | Acción repetible: -1 titanio → +1 recurso en la carta |
| `cupola_city` | Cupola City | 029 | 16 MC | Requiere oxígeno ≤9%. -1 producción energía, +3 producción MC, +1 ciudad |
| `lunar_beam` | Lunar Beam | 030 | 13 MC | -2 producción MC, +2 producción calor, +2 producción energía |
| `underground_city` | Underground City | 032 | 18 MC | -2 producción energía, +2 producción steel, +1 ciudad |
| `ghg_producing_bacteria` | GHG Producing Bacteria | 034 | 8 MC | Requiere oxígeno ≥4%. Acción repetible con elección: +1 microbio (en la carta) O -2 microbios/+1 paso temperatura |
| `release_of_inert_gases` | Release of Inert Gases | 036 | 14 MC | +2 TR directo (evento) |
| `nitrogen_rich_asteroid` | Nitrogen-Rich Asteroid | 037 | 31 MC | +1 paso temperatura; +1 producción plantas, o +4 si ya jugó 3 tags de planta (`tag_count_choice`) |
| `deimos_down` | Deimos Down | 039 | 31 MC | +3 pasos temperatura, +4 steel (stock) |
| `asteroid_mining` | Asteroid Mining | 040 | 30 MC | +2 producción titanio |
| `food_factory` | Food Factory | 041 | 12 MC | -1 producción plantas, +4 producción MC |
| `archaebacteria` | Archaebacteria | 042 | 6 MC | Requiere temperatura ≤-18°C. +1 producción plantas |
| `carbonate_processing` | Carbonate Processing | 043 | 6 MC | -1 producción energía, +3 producción calor |
| `natural_preserve` | Natural Preserve | 044 | 9 MC | Requiere oxígeno ≤4%. +1 producción MC (restricción de adyacencia de tile ignorada, sin mapa hexagonal) |
| `lightning_harvest` | Lightning Harvest | 046 | 8 MC | Requiere 3 tags de ciencia jugados. +1 producción energía, +1 producción MC |
| `algae` | Algae | 047 | 10 MC | Requiere 5 océanos colocados. +1 planta (stock), +2 producción plantas |
| `adapted_lichen` | Adapted Lichen | 048 | 9 MC | +1 producción plantas |
| `tardigrades` | Tardigrades | 049 | 4 MC | Acción repetible sin costo: +1 recurso en la carta |
| `virus` | Virus | 050 | 1 MC | Sin efecto modelado — toda la carta es la cláusula "remove up to 2 animales o 5 plantas de cualquier jugador" (omitida, MVP single-player) |
| `miranda_resort` | Miranda Resort | 051 | 12 MC | +1 producción MC por cada tag earth jugado (`production_delta_per_tag`) |
| `fish` | Fish | 052 | 9 MC | Requiere temperatura ≥2°C. -1 producción plantas; acción repetible sin costo: +1 recurso en la carta |
| `lake_marineris` | Lake Marineris | 053 | 18 MC | Requiere temperatura ≥0°C. Coloca 2 océanos (+2 TR) |
| `small_animals` | Small Animals | 054 | 6 MC | Requiere oxígeno ≥6%. -1 producción plantas; acción repetible sin costo: +1 recurso en la carta |
| `kelp_farming` | Kelp Farming | 055 | 17 MC | Requiere 6 océanos colocados. +2 producción MC, +3 producción plantas, +2 plantas (stock) |
| `vesta_shipyard` | Vesta Shipyard | 057 | 15 MC | +1 producción titanio |
| `beam_from_a_thorium_asteroid` | Beam from a Thorium Asteroid | 058 | 32 MC | Requiere 1 tag jovian jugado. +3 producción calor, +3 producción energía |
| `mangrove` | Mangrove | 059 | 12 MC | Requiere temperatura ≥4°C. +1 paso oxígeno (la restricción de colocación "en área reservada de océano" es irrelevante sin mapa modelado) |
| `trees` | Trees | 060 | 13 MC | Requiere temperatura ≥-4°C. +3 producción plantas, +1 planta (stock) |
| `great_escarpment_consortium` | Great Escarpment Consortium | 061 | 6 MC | Requiere producción propia de steel ≥1 (`min_production`). Sin efecto neto en single-player (-1 y +1 al mismo jugador se cancelan) |
| `mineral_deposit` | Mineral Deposit | 062 | 5 MC | +5 steel (stock) |
| `mining_expedition` | Mining Expedition | 063 | 12 MC | +1 paso oxígeno, -2 plantas (obligatorio), +2 steel |
| `building_industries` | Building Industries | 065 | 6 MC | -1 producción energía, +2 producción steel |
| `electro_catapult` | Electro Catapult | 069 | 17 MC | Requiere oxígeno ≤8%. -1 producción energía; acción repetible con elección: -1 planta O -1 steel → +7 MC |
| `mining_rights` | Mining Rights | 067 | 9 MC | Coloca special tile en un hex con bonus de steel o titanium (`place_special_tile`), +1 producción de ESE recurso |
| `mining_area` | Mining Area | 064 | 4 MC | Igual que Mining Rights, pero exige que el hex sea adyacente a un tile propio (`require_adjacency_to_own_tile`) |
| `land_claim` | Land Claim | 066 | 1 MC | Sin efecto modelado — "reservar un hexágono para uso exclusivo propio" no tiene consecuencia mecánica en single-player (nadie más podría disputarlo) |
| `earth_catapult` | Earth Catapult | 070 | 23 MC | Pasivo: -2 MC en TODAS las cartas futuras (sin `tag_filter`) |
| `birds` | Birds | 072 | 10 MC | Requiere oxígeno ≥13%. -2 producción plantas; acción repetible sin costo: +1 recurso en la carta |
| `mars_university` | Mars University | 073 | 8 MC | Pasivo nuevo: al jugar cualquier carta con tag science (incluida esta), puede descartar 1 carta y robar 1 (`on_tag_played_may_swap_card`) |
| `towing_a_comet` | Towing a Comet | 075 | 23 MC | +2 plantas, +1 paso oxígeno, +1 océano |
| `space_mirrors` | Space Mirrors | 076 | 3 MC | Acción repetible: -7 MC → +1 producción energía |
| `ice_asteroid` | Ice Asteroid | 078 | 23 MC | +2 océanos |
| `quantum_extractor` | Quantum Extractor | 079 | 13 MC | Requiere 4 tags de ciencia jugados. +4 producción energía; pasivo: cartas espaciales cuestan 2 MC menos |
| `giant_ice_asteroid` | Giant Ice Asteroid | 080 | 36 MC | +2 pasos temperatura, +2 océanos |
| `ganymede_colony` | Ganymede Colony | 081 | 20 MC | Sin efecto modelado — coloca tile en un slot de colonia fuera del mapa de Marte, VP por tag jovian (no trackeado) |
| `callisto_penal_mines` | Callisto Penal Mines | 082 | 24 MC | +3 producción MC |
| `giant_space_mirror` | Giant Space Mirror | 083 | 17 MC | +3 producción energía |
| `trans_neptune_probe` | Trans-Neptune Probe | 084 | 6 MC | Sin efecto modelado — solo puntos, no trackeados |
| `commercial_district` | Commercial District | 085 | 16 MC | -1 producción energía, +4 producción MC (VP por ciudad adyacente no trackeado) |
| `grass` | Grass | 087 | 11 MC | Requiere temperatura ≥-16°C. +1 producción plantas, +3 plantas (stock) |
| `heather` | Heather | 088 | 6 MC | Requiere temperatura ≥-14°C. +1 producción plantas, +1 planta (stock) |
| `peroxide_power` | Peroxide Power | 089 | 7 MC | -1 producción MC, +2 producción energía |
| `research` | Research | 090 | 11 MC | 2 tags de ciencia (propios). Roba 2 cartas (`draw_cards`) |
| `robotic_workforce` | Robotic Workforce | 086 | 9 MC | Duplica la `production_deltas` de una carta con tag building ya jugada (`duplicate_production`, requiere historial `played_cards`) |
| `gene_repair` | Gene Repair | 091 | 12 MC | Requiere 3 tags de ciencia jugados (esta carta tiene 3 tags de ciencia propios). +2 producción MC |
| `io_mining_industries` | IO Mining Industries | 092 | 41 MC | +2 producción titanio, +2 producción MC (VP por tag jovian no trackeado) |
| `bushes` | Bushes | 093 | 10 MC | Requiere temperatura ≥-10°C. +2 producción plantas, +2 plantas (stock) |
| `physics_complex` | Physics Complex | 095 | 12 MC | Acción repetible: -6 energía → +1 recurso en la carta (VP por recurso no trackeado) |
| `greenhouses` | Greenhouses | 096 | 6 MC | +1 planta por cada ciudad colocada (`resource_delta_per_counter`) |
| `nuclear_zone` | Nuclear Zone | 097 | 10 MC | +2 pasos temperatura (colocación de tile y -2 VP no trackeados) |
| `tropical_resort` | Tropical Resort | 098 | 13 MC | -2 producción calor, +3 producción MC |
| `toll_station` | Toll Station | 099 | 12 MC | Sin efecto modelado — depende de tags de OPONENTES, siempre 0 en single-player |
| `fueled_generators` | Fueled Generators | 100 | 1 MC | -1 producción MC, +1 producción energía |
| `power_grid` | Power Grid | 102 | 18 MC | +1 producción energía por cada tag power ya jugado, incluida esta (`production_delta_per_tag` + `production_deltas` combinados) |
| `ore_processor` | Ore Processor | 104 | 13 MC | Acción repetible: -4 energía → +1 titanio, +1 paso oxígeno |
| `earth_office` | Earth Office | 105 | 1 MC | Pasivo: -3 MC en cartas con tag earth |
| `media_archives` | Media Archives | 107 | 8 MC | +1 MC por cada evento jugado alguna vez (`resource_delta_per_counter`, contador `events_played`) |
| `open_city` | Open City | 108 | 23 MC | Requiere oxígeno ≥12%. -1 producción energía, +4 producción MC, +2 plantas, +1 ciudad |
| `business_network` | Business Network | 110 | 4 MC | -1 producción MC; acción repetible: roba 1 a investigación pendiente (mismo patrón que Inventors' Guild) |
| `business_contacts` | Business Contacts | 111 | 7 MC | Evento. Roba 4 a investigación pendiente (`start_research` inmediato); se resuelve con `resolve_research_phase(cost_per_card=0, max_take=2)` — exige tomar exactamente 2 |
| `bribed_committee` | Bribed Committee | 112 | 7 MC | Evento. +2 TR directo |
| `breathing_filters` | Breathing Filters | 114 | 11 MC | Requiere oxígeno ≥7%. Sin efecto modelado — solo puntos, no trackeados |
| `artificial_lake` | Artificial Lake | 116 | 15 MC | Requiere temperatura ≥-6°C. Coloca 1 océano en hex NO reservado para océano (`place_ocean_tile_on_land`, lo inverso de la regla normal) |
| `geothermal_power` | Geothermal Power | 117 | 11 MC | +2 producción energía |
| `dust_seals` | Dust Seals | 119 | 2 MC | Requiere máximo 3 océanos colocados (`max_oceans`, nuevo) |
| `urbanized_area` | Urbanized Area | 120 | 10 MC | -1 producción energía, +2 producción MC, +1 ciudad EXIGIENDO adyacencia a 2+ ciudades (`place_city_tile_adjacent_to_cities`, lo inverso de la regla normal) |
| `sabotage` | Sabotage | 121 | 1 MC | Evento. Sin efecto modelado — cláusula "steal up to" omitida (single-player) |
| `moss` | Moss | 122 | 4 MC | Requiere 3 océanos colocados. -1 planta (costo obligatorio), +1 producción plantas |
| `industrial_center` | Industrial Center | 123 | 4 MC | Special tile adyacente a una ciudad de cualquier dueño (`require_adjacency_to_city`, nuevo); acción repetible: -7 MC → +1 producción steel |
| `hired_raiders` | Hired Raiders | 124 | 1 MC | Evento. Sin efecto modelado — cláusula "steal up to" omitida |
| `hackers` | Hackers | 125 | 3 MC | -1 producción energía (swap de producción MC a "cualquiera" se cancela en single-player) |
| `ghg_factories` | GHG Factories | 126 | 11 MC | -1 producción energía, +4 producción calor |
| `subterranean_reservoir` | Subterranean Reservoir | 127 | 11 MC | Evento. Coloca 1 océano |
| `ecological_zone` | Ecological Zone | 128 | 12 MC | Requiere tener 1 greenery (`require_player_has_greenery`). Special tile adyacente a greenery (`require_adjacency_to_greenery`). Pasivo: +1 animal en esta carta al jugar tag animal o plant (incluidos los 2 de esta carta, arranca con 2 animales) (`on_tag_played_add_resource`) |
| `zeppelins` | Zeppelins | 129 | 13 MC | Requiere oxígeno ≥5%. +1 producción MC por cada ciudad colocada en Marte (`production_delta_per_counter`) |
| `worms` | Worms | 130 | 8 MC | Requiere oxígeno ≥4%. +1 producción plantas por cada 2 tags de microbio jugados, incluido este (`production_delta_per_tag` con `tags_per_step: 2, include_this: true`) |
| `decomposers` | Decomposers | 131 | 5 MC | Requiere oxígeno ≥3%. Pasivo: +1 microbio en esta carta al jugar tag animal, plant o microbe (arranca con 1 microbio por su propio tag) (`on_tag_played_add_resource`) |
| `fusion_power` | Fusion Power | 132 | 14 MC | Requiere 2 tags de power jugados (`min_tag_count`). +3 producción energía |
| `symbiotic_fungus` | Symbiotic Fungus | 133 | 4 MC | Requiere temperatura ≥-14°C. Acción repetible: agrega 1 microbio a OTRA carta activa (`target_card_resource_delta`) |
| `extreme_cold_fungus` | Extreme-Cold Fungus | 134 | 13 MC | Requiere temperatura ≤-10°C. Acción repetible con elección: +1 planta (stock) O agrega 2 microbios a OTRA carta activa (`target_card_resource_delta`) |
| `advanced_ecosystems` | Advanced Ecosystems | 135 | 11 MC | Requiere 1 tag plant, 1 tag microbe y 1 tag animal jugados (`min_tag_count` múltiple). Sin efecto directo (solo puntos) |
| `great_dam` | Great Dam | 136 | 12 MC | Requiere 4 océanos colocados. +2 producción energía |
| `local_heat_trapping` | Local Heat Trapping | 190 | 1 MC | Evento. Elección: -5 calor +4 plantas, O -5 calor y agregar 2 recursos a OTRA carta activa (`target_card_resource_delta`) |
| `imported_hydrogen` | Imported Hydrogen | 019 | 16 MC | Evento, tags Earth/Space. Coloca 1 océano y elección: +3 plantas, O agregar 3 recursos a OTRA carta activa, O agregar 2 recursos a OTRA carta activa (`target_card_resource_delta`) |
| `predators` | Predators | 024 | 14 MC | Requiere oxígeno ≥11%. Acción repetible: mueve 1 animal desde OTRA carta activa hacia esta (`move_from_target_card_resource_delta`) |
| `eos_chasma_national_park` | Eos Chasma National Park | 026 | 16 MC | Requiere temperatura ≥-12°C. Agrega 1 animal a OTRA carta activa (`target_card_resource_delta`), +3 plantas, +2 producción MC |
| `ants` | Ants | 035 | 9 MC | Requiere oxígeno ≥4%. Acción repetible: mueve 1 microbio desde OTRA carta activa hacia esta (`move_from_target_card_resource_delta`) |
| `cartel` | Cartel | 137 | 8 MC | +1 producción MC por cada tag Earth jugado, incluido este (`production_delta_per_tag` con `include_this: true`) |
| `strip_mine` | Strip Mine | 138 | 25 MC | -2 producción energía, +2 producción acero, +1 producción titanio, sube oxígeno 2 pasos |
| `wave_power` | Wave Power | 139 | 8 MC | Requiere 3 océanos colocados. +1 producción energía |
| `power_plant_card` | Power Plant | 141 | 4 MC | +1 producción energía (distinta del proyecto estándar homónimo) |
| `mohole_area` | Mohole Area | 142 | 20 MC | +4 producción calor. Coloca special tile en un hex reservado a océano (`place_special_tile` con nuevo `requirement.hex_type: "ocean"`, no cuenta como uno de los 9 océanos del parámetro global) |
| `large_convoy` | Large Convoy | 143 | 36 MC | Evento, tags Earth/Space. Coloca 1 océano, roba 2 cartas, y elección: +5 plantas O agregar 4 recursos a OTRA carta activa (`target_card_resource_delta`) |
| `tectonic_stress_power` | Tectonic Stress Power | 145 | 18 MC | Tags science×2/power/building. Requiere 2 tags de ciencia ya jugados (`min_tag_count`). +3 producción energía |
| `herbivores` | Herbivores | 147 | 12 MC | Requiere oxígeno ≥8%. Arranca con 1 animal en la propia carta (`active_card_starting_resources`, nuevo campo de `register_active_card`), -1 producción plantas. Pasivo: +1 animal cada vez que se coloca un tile de greenery (`on_greenery_placed_add_resource`, nuevo pasivo disparado desde `tools._place_greenery_and_apply_bonus`) |
| `insects` | Insects | 148 | 9 MC | Requiere oxígeno ≥6%. +1 producción plantas por cada tag plant ya jugado (`production_delta_per_tag`, sin `include_this` porque Insects no tiene tag plant) |
| `ceos_favorite_project` | CEO's Favorite Project | 149 | 1 MC | Evento. Agrega 1 recurso a OTRA carta activa que YA tenga al menos 1 recurso (`target_card_resource_delta` + nuevo `target_min_resources`) |
| `anti_gravity_technology` | Anti-Gravity Technology | 150 | 14 MC | Requiere 7 tags de ciencia ya jugados. Pasivo: -2 MC al costo de CUALQUIER carta futura (`card_cost_discount_mc` sin `tag_filter`) |
| `adaptation_technology` | Adaptation Technology | 153 | 12 MC | Pasivo: relaja 2 pasos los requisitos de temperatura/oxígeno/océanos de futuras cartas, en la dirección favorable (nuevo `global_requirements_tolerance_steps`, ver `check_card_requirements`) |
| `caretaker_contract` | Caretaker Contract | 154 | 3 MC | Requiere temperatura ≥0°C. Acción repetible: gasta 8 calor, +1 TR |
| `designed_microorganisms` | Designed Microorganisms | 155 | 16 MC | Requiere temperatura ≤-14°C. +2 producción plantas |
| `standard_technology` | Standard Technology | 156 | 6 MC | Pasivo: +3 MC cada vez que se paga un proyecto estándar (excepto Sell Patents) (nuevo `on_standard_project_used`, aplicado desde `tools.use_standard_project`) |
| `nitrite_reducing_bacteria` | Nitrite Reducing Bacteria | 157 | 11 MC | Arranca con 3 microbios (`active_card_starting_resources`). Acción repetible con elección: +1 microbio propio, O gastar 3 microbios propios (`cost.card_resource`) por +1 TR |
| `industrial_microbes` | Industrial Microbes | 158 | 12 MC | +1 producción energía, +1 producción acero |
| `lichen` | Lichen | 159 | 7 MC | Requiere temperatura ≥-24°C. +1 producción plantas |
| `power_supply_consortium` | Power Supply Consortium | 160 | 5 MC | Tags power×2. Requiere 2 tags de power ya jugados. "-1 producción energía de cualquier jugador, +1 propia" — en el MVP de un solo jugador ambos targetean al mismo jugador, neto 0 (mismo criterio que Fish/Small Animals, ver nota de diseño más abajo, extendida al caso de un mismo recurso) |
| `convoy_from_europa` | Convoy from Europa | 161 | 15 MC | Evento, tag space. Coloca 1 océano, roba 1 carta |
| `imported_ghg` | Imported GHG | 162 | 7 MC | Evento, tags Earth/Space. +1 producción calor, +3 calor (stock) |
| `imported_nitrogen` | Imported Nitrogen | 163 | 23 MC | Evento, tags Earth/Space. +1 TR, +4 plantas, agrega 3 recursos a una carta activa Y 2 recursos a OTRA carta activa distinta (nuevo `target_card_resource_delta_2`/`target_card_id_2`, dos objetivos en la misma jugada) |
| `micro_mills` | Micro-Mills | 164 | 3 MC | +1 producción calor |
| `magnetic_field_generators` | Magnetic Field Generators | 165 | 20 MC | -4 producción energía, +2 producción plantas, +3 TR |
| `shuttles` | Shuttles | 166 | 10 MC | Requiere oxígeno ≥5%. -1 producción energía, +2 producción MC. Pasivo: -2 MC al costo de cartas con tag space (`card_cost_discount_mc` + `tag_filter`) |
| `import_of_advanced_ghg` | Import of Advanced GHG | 167 | 9 MC | Evento, tags Earth/Space. +2 producción calor |
| `windmills` | Windmills | 168 | 6 MC | Requiere oxígeno ≥7%. +1 producción energía |
| `tundra_farming` | Tundra Farming | 169 | 16 MC | Requiere temperatura ≥-6°C. +1 producción plantas, +2 producción MC, +1 planta (stock) |
| `aerobraked_ammonia_asteroid` | Aerobraked Ammonia Asteroid | 170 | 26 MC | Evento, tags space×2. Agrega 2 recursos a OTRA carta activa (`target_card_resource_delta`), +3 producción calor, +1 producción plantas |
| `magnetic_field_dome` | Magnetic Field Dome | 171 | 5 MC | -2 producción energía, +1 producción plantas, +1 TR |
| `pets` | Pets | 172 | 10 MC | Arranca con 1 animal (`active_card_starting_resources`). Pasivo: +1 animal cada vez que se coloca CUALQUIER tile de ciudad en el mapa (nuevo `on_city_tile_placed_add_resource`, aplicado desde `tools._place_city_and_apply_bonus`) |
| `protected_habitats` | Protected Habitats | 173 | 5 MC | "Opponents may not remove your plant/animal/microbe resources" — fuera de alcance por diseño en el MVP de un solo jugador (no hay mecánica de remoción por otro jugador que proteger); se paga pero `effects: {}`, mismo criterio que Virus |
| `protected_valley` | Protected Valley | 174 | 23 MC | +2 producción MC, sube oxígeno 1 paso, coloca un tile de greenery ignorando restricciones normales (nuevo `effects.place_greenery` + `board.can_place_greenery(..., ignore_restrictions=True)`, permite colocarlo incluso en un hex reservado a océano) |
| `satellites` | Satellites | 175 | 10 MC | +1 producción MC por cada tag space jugado, incluido este (`production_delta_per_tag` con `include_this: true`) |
| `noctis_farming` | Noctis Farming | 176 | 10 MC | Requiere temperatura ≥-20°C. +1 producción MC, +2 plantas (stock) |
| `water_splitting_plant` | Water Splitting Plant | 177 | 12 MC | Requiere 2 océanos colocados. Acción repetible: gasta 3 energía, sube oxígeno 1 paso |
| `heat_trappers` | Heat Trappers | 178 | 6 MC | -2 producción calor, +1 producción energía |
| `soil_factory` | Soil Factory | 179 | 9 MC | -1 producción energía, +1 producción plantas |
| `fuel_factory` | Fuel Factory | 180 | 6 MC | -1 producción energía, +1 producción titanio, +1 producción MC |
| `ice_cap_melting` | Ice Cap Melting | 181 | 5 MC | Evento. Requiere temperatura ≥2°C. Coloca 1 océano |
| `corporate_stronghold` | Corporate Stronghold | 182 | 11 MC | -1 producción energía, +3 producción MC, coloca un tile de ciudad |
| `biomass_combustors` | Biomass Combustors | 183 | 4 MC | Requiere oxígeno ≥6%. -1 producción plantas, +2 producción energía |
| `livestock` | Livestock | 184 | 13 MC | Requiere oxígeno ≥9%. -1 producción plantas, +2 producción MC. Acción repetible gratis: +1 animal propio (`card_resource_delta`) |
| `olympus_conference` | Olympus Conference | 185 | 10 MC | Tags science/earth. Pasivo: al jugar CUALQUIER carta con tag science (incluida esta), elección opcional entre agregar 1 recurso propio O gastar 1 para robar 1 carta (nuevo `on_tag_played_choice`, ver `tools.play_card` param `tag_played_choice`) |
| `rad_suits` | Rad-Suits | 186 | 6 MC | Requiere 2 ciudades en juego (nuevo requirement `min_city_tiles`). +1 producción MC |
| `aquifer_pumping` | Aquifer Pumping | 187 | 18 MC | Acción repetible: gasta 8 MC, coloca 1 océano |
| `flooding` | Flooding | 188 | 7 MC | Evento. Coloca 1 océano (cláusula opcional de robar MC a otro jugador omitida, MVP de un solo jugador) |
| `energy_saving` | Energy Saving | 189 | 15 MC | +1 producción energía por cada tile de ciudad en el mapa (`production_delta_per_counter`) |
| `permafrost_extraction` | Permafrost Extraction | 191 | 8 MC | Evento. Requiere temperatura ≥-8°C. Coloca 1 océano |
| `invention_contest` | Invention Contest | 192 | 2 MC | Evento. Roba 3 a `pending_research` (`start_research`, se resuelve después con `resolve_research_phase(cost_per_card=0, max_take=1)`) |
| `plantation` | Plantation | 193 | 15 MC | Requiere 2 tags de ciencia ya jugados. Sube oxígeno 1 paso, coloca greenery con reglas normales (`place_greenery` sin `ignore_restrictions`) |
| `power_infrastructure` | Power Infrastructure | 194 | 4 MC | Acción repetible: convierte cualquier cantidad de energía a esa misma cantidad de MC (nuevo `action.convert_resource_amount` + `effect_amount` en `use_card_action`) |
| `indentured_workers` | Indentured Workers | 195 | 0 MC | Evento. La próxima carta que el jugador juegue esta generación cuesta 8 MC menos (nuevo campo `pending_mc_discount` en `players` + `effects.next_card_discount_mc`, se consume al jugar la siguiente carta o se pierde al terminar la generación) |
| `lagrange_observatory` | Lagrange Observatory | 196 | 9 MC | Roba 1 carta |
| `terraforming_ganymede` | Terraforming Ganymede | 197 | 33 MC | +1 TR por cada tag jovian jugado, incluido este (nuevo `tr_delta_per_tag`) |
| `immigration_shuttles` | Immigration Shuttles | 198 | 31 MC | +5 producción MC |
| `restricted_area` | Restricted Area | 199 | 11 MC | Coloca una special tile genérica sin requisito (`place_special_tile: {}`). Acción repetible: gasta 2 MC, roba 1 carta |
| `immigrant_city` | Immigrant City | 200 | 13 MC | -1 producción energía, -2 producción MC, coloca un tile de ciudad. Pasivo: +1 producción MC cada vez que se coloca CUALQUIER ciudad, incluida la propia (nuevo `on_city_tile_placed_production_delta`; se autodispara porque `tools.play_card` ahora registra la carta como activa/pasiva ANTES de colocar su tile) |
| `energy_tapping` | Energy Tapping | 201 | 3 MC | "-1 producción energía de cualquier jugador, +1 propia" — neto 0 en el MVP de un solo jugador (mismo criterio que Power Supply Consortium) |
| `underground_detonations` | Underground Detonations | 202 | 6 MC | Acción repetible: gasta 10 MC, +2 producción calor |
| `soletta` | Soletta | 203 | 35 MC | +7 producción calor |
| `technology_demonstration` | Technology Demonstration | 204 | 5 MC | Evento, tags science/space. Roba 2 cartas |
| `rad_chem_factory` | Rad-Chem Factory | 205 | 8 MC | -1 producción energía, +2 TR |
| `special_design` | Special Design | 206 | 4 MC | Evento, tag science. Relaja +/-2 pasos los requisitos globales de la PRÓXIMA carta jugada esta generación (nuevo campo `pending_requirement_tolerance_steps` en `players` + `effects.next_card_requirement_tolerance_steps`, análogo a `pending_mc_discount` del bloque 18) |
| `medical_lab` | Medical Lab | 207 | 13 MC | +1 producción MC por cada 2 tags building jugados, incluido este (`production_delta_per_tag` con `tags_per_step: 2`) |
| `ai_central` | AI Central | 208 | 21 MC | Requiere 3 tags de ciencia ya jugados. -1 producción energía. Acción repetible gratis: roba 2 cartas |
| `small_asteroid` | Small Asteroid | 209 | 10 MC | Evento, tag space. Sube temperatura 1 paso (cláusula opcional de robar plantas a otro jugador omitida, MVP de un solo jugador) |
| `snow_algae` | Snow Algae | 211 | 12 MC | Requiere 2 océanos colocados. +1 producción plantas, +1 producción calor |
| `penguins` | Penguins | 212 | 7 MC | Requiere 8 océanos. Acción repetible sin costo: +1 recurso (animal) en la carta |
| `aerial_mappers` | Aerial Mappers | 213 | 11 MC | Tag venus. Acción con elección: +1 floater a sí misma, O +1 floater a OTRA carta activa, O gastar 1 floater propio para robar 1 carta |
| `air_scrapping_expedition` | Air-Scrapping Expedition | 215 | 13 MC | Tag venus, evento. +1 paso Venus, +3 floaters a una carta Venus activa elegida |
| `atalanta_planitia_lab` | Atalanta Planitia Lab | 216 | 10 MC | Tags venus+science. Requiere 3 tags de ciencia. Roba 2 cartas |
| `atmoscoop` | Atmoscoop | 217 | 22 MC | Tags jovian+power. Requiere 3 tags de ciencia. Elección: +2 pasos temperatura O +2 pasos Venus; siempre +2 floaters a una carta Venus activa elegida |
| `comet_for_venus` | Comet for Venus | 218 | 11 MC | Tag power, evento. +1 paso Venus (cláusula "remove up to 4 MC de un oponente con tag Venus" omitida, regla de oro single-player) |
| `corroder_suits` | Corroder Suits | 219 | 8 MC | Tag venus. +2 producción MC, +1 floater a una carta Venus activa elegida |
| `dawn_city` | Dawn City | 220 | 15 MC | Tags power+city. Requiere 4 tags de ciencia. -1 producción energía, +1 producción titanio, +1 ciudad (mismo mecanismo genérico ya usado para Phobos Space Haven -- exige hex_id real de Tharsis, no modela el área reservada de Venus por separado) |
| `deuterium_export` | Deuterium Export | 221 | 11 MC | Tags venus+power+power (doble power, verificado contra el scan). Acción con elección: +1 floater a sí misma, O gastar 1 floater propio para +1 producción energía |
| `lava_flows` | Lava Flows | 140 | 18 MC | Evento, sin tag. +2 pasos temperatura, coloca tile especial en UNO de los 4 hexágonos volcánicos nombrados (Tharsis Tholus/Ascraeus/Pavonis/Arsia Mons, ver `VOLCANO_NAMES` en `board.py` y "Los 4 volcanes con nombre" en `HEX_MAP_RESEARCH.md`) |
| `extractor_balloons` | Extractor Balloons | 223 | 21 MC | Tag venus. Arranca con 3 floaters. Acción con elección: +1 floater a sí misma, O gastar 2 floaters para +1 paso Venus |
| `extremophiles` | Extremophiles | 224 | 3 MC | Tags venus+microbe. Requiere 2 tags de ciencia. Acción repetible sin costo: +1 microbio en la carta |
| `floating_habs` | Floating Habs | 225 | 5 MC | Tag venus. Requiere 2 tags de ciencia. Acción con elección: -2 MC → +1 floater a sí misma, O -2 MC → +1 floater a OTRA carta activa elegida |
| `forced_precipitation` | Forced Precipitation | 226 | 8 MC | Tag venus. Acción con elección: -2 MC → +1 floater a sí misma, O gastar 2 floaters propios → +1 paso Venus |
| `freyja_biodomes` | Freyja Biodomes | 227 | 14 MC | Tags venus+plant. Requiere Venus ≥10%. -1 producción energía, +2 producción MC, +2 recursos a OTRA carta Venus activa elegida (texto real ofrece elegir microbio O animal, mecánicamente idéntico en este motor — resuelto sin `choice`, ver nota en `seed_cards.sql`) |
| `ghg_import_from_venus` | GHG Import from Venus | 228 | 23 MC | Tags venus+power, evento. +1 paso Venus, +3 producción calor |
| `giant_solar_shade` | Giant Solar Shade | 229 | 27 MC | Tags venus+power. +3 pasos Venus |
| `gyropolis` | Gyropolis | 230 | 20 MC | Tags city+building. -2 producción energía, +1 producción MC por cada tag venus Y +1 por cada tag earth (pieza nueva: `production_delta_per_tag` ahora acepta lista de specs), +1 ciudad |
| `hydrogen_to_venus` | Hydrogen to Venus | 231 | 11 MC | Tag power, evento. +1 paso Venus, +1 floater a una carta Venus activa elegida por cada tag jovian (pieza nueva: `target_card_resource_delta_per_tag`, no exige target si el conteo da 0) |
| `io_sulphur_research` | IO Sulphur Research | 232 | 17 MC | Tags science+jovian. Roba 1 carta, o 3 si ya tiene 3 tags venus (`tag_count_choice`) |
| `ishtar_mining` | Ishtar Mining | 233 | 5 MC | Tag venus. Requiere Venus ≥8%. +1 producción titanio |
| `jet_stream_microscrappers` | Jet Stream Microscrappers | 234 | 12 MC | Tag venus. Acción con elección: -1 titanio → +2 floaters a sí misma, O gastar 2 floaters propios → +1 paso Venus |
| `local_shading` | Local Shading | 235 | 4 MC | Tag venus. Acción con elección: +1 floater a sí misma, O gastar 1 floater propio → +1 producción MC |
| `luna_metropolis` | Luna Metropolis | 236 | 21 MC | Tags power+earth+city. +1 producción MC por cada tag earth (incluida esta), +1 ciudad (mismo mecanismo genérico de Phobos Space Haven/Dawn City) |
| `luxury_foods` | Luxury Foods | 237 | 8 MC | Tags venus+earth+jovian. Requiere los 3 tags jugados. Sin efecto numérico (solo VP no trackeado) |
| `maxwell_base` | Maxwell Base | 238 | 18 MC | Tags venus+city. Requiere Venus ≥12%. -1 producción energía, +1 ciudad; acción repetible sin costo: +1 recurso a OTRA carta Venus activa elegida |
| `mining_quota` | Mining Quota | 239 | 5 MC | Tags venus+earth+jovian+building. Requiere los 3 tags jugados. +2 producción steel |
| `neutralizer_factory` | Neutralizer Factory | 240 | 7 MC | Tag venus. Requiere Venus ≥10%. +1 paso Venus |
| `omnicourt` | Omnicourt | 241 | 11 MC | Tags venus+earth+jovian+building. Requiere los 3 tags jugados. +2 TR directo |
| `orbital_reflectors` | Orbital Reflectors | 242 | 26 MC | Tags venus+power. +2 pasos Venus, +2 producción calor |
| `rotator_impacts` | Rotator Impacts | 243 | 6 MC | Tag power. Requiere Venus ≤14%. Acción con elección: -6 MC (titanio puede cubrir, pieza nueva `mc_or_titanium`) → +1 recurso a sí misma, O gastar 1 recurso propio → +1 paso Venus |
| `sister_planet_support` | Sister Planet Support | 244 | 7 MC | Tags venus+earth. Requiere ambos tags jugados. +3 producción MC |
| `solarnet` | Solarnet | 245 | 7 MC | Tags venus+earth+jovian. Requiere los 3 tags jugados. Roba 2 cartas |
| `spin_inducing_asteroid` | Spin-Inducing Asteroid | 246 | 16 MC | Tag power, evento. Requiere Venus ≤10%. +2 pasos Venus |
| `sponsored_academies` | Sponsored Academies | 247 | 9 MC | Sin tags propios. Requiere science+earth jugados. Descarta 1 carta elegida, roba 3 (pieza nueva `discard_card_then_draw`; cláusula "opponents draw 1" omitida, sin efecto en single-player) |
| `stratopolis` | Stratopolis | 248 | 22 MC | Tags venus+city. Requiere 2 tags de ciencia. +2 producción MC, +1 ciudad; acción repetible sin costo: +2 recursos a OTRA carta Venus activa elegida |
| `stratospheric_birds` | Stratospheric Birds | 249 | 12 MC | Tags venus+animal. Requiere Venus ≥12%. Acción repetible sin costo propio: mueve 1 floater desde OTRA carta activa elegida → +1 animal en esta |
| `sulphur_exports` | Sulphur Exports | 250 | 21 MC | Tag venus. +1 paso Venus, +1 producción MC por cada tag venus (incluida esta) |
| `sulphur_eating_bacteria` | Sulphur-Eating Bacteria | 251 | 6 MC | Tags venus+microbe. Requiere Venus ≥6%. Acción con elección: +1 microbio a sí misma, O gastar X microbios propios (pieza nueva `convert_card_resource_amount`) → +3X MC |
| `terraforming_contract` | Terraforming Contract | 252 | 8 MC | Tag earth. Requiere TR ≥25 (pieza nueva `min_tr`). +4 producción MC |
| `thermophiles` | Thermophiles | 253 | 9 MC | Tags venus+microbe. Requiere Venus ≥6%. Acción con elección: +1 microbio a OTRA carta Venus activa elegida, O gastar 2 microbios propios → +1 paso Venus |
| `water_to_venus` | Water to Venus | 254 | 9 MC | Tag power, evento. +1 paso Venus |
| `venus_governor` | Venus Governor | 255 | 4 MC | Doble tag venus (verificado contra el scan). Requiere 2 tags venus jugados. +2 producción MC |
| `venus_magnetizer` | Venus Magnetizer | 256 | 7 MC | Tag venus. Requiere Venus ≥10%. Acción repetible sin costo de stock: -1 producción energía, +1 paso Venus |
| `venus_soils` | Venus Soils | 257 | 20 MC | Tags venus+plant. +1 paso Venus, +1 producción plantas, +2 recursos a OTRA carta activa elegida |
| `venus_waystation` | Venus Waystation | 258 | 9 MC | Tags venus+power. Pasivo: cartas con tag venus cuestan 2 MC menos (mismo patrón de Space Station) |
| `venusian_animals` | Venusian Animals | 259 | 15 MC | Tags venus+science+animal. Requiere Venus ≥18%. Pasivo: +1 animal en la carta por cada tag science jugado (incluida esta, mismo patrón de Ecological Zone) |
| `venusian_insects` | Venusian Insects | 260 | 5 MC | Tags venus+microbe. Requiere Venus ≥12%. Acción repetible sin costo: +1 microbio en la carta |
| `venusian_plants` | Venusian Plants | 261 | 13 MC | Tags venus+plant. Requiere Venus ≥16%. +1 paso Venus, +1 recurso a OTRA carta Venus activa elegida (texto real ofrece elegir microbio O animal, mecánicamente idéntico, resuelto sin `choice`) |
| `atmo_collectors` | Atmo Collectors | C03 | 15 MC | Sin tags propios. Acción con elección de 4: +1 floater a sí misma, O gastar 1 floater propio → +2 titanio / +3 energía / +4 calor (mismo recurso, tres ramas separadas). Efecto inmediato al jugar: +2 floaters a cualquier carta (target puede ser ella misma) |
| `community_services` | Community Services | C04 | 13 MC | Sin tags propios. +1 producción MC por cada carta jugada SIN tags, incluida ella misma (pieza nueva `production_delta_per_zero_tag_card` + contador `zero_tag_cards_played`) |
| `conscription` | Conscription | C05 | 5 MC | Doble tag earth. Requiere 2 tags earth jugados. Próxima carta cuesta 16 MC menos (`next_card_discount_mc`, ya existente) |
| `corona_extractor` | Corona Extractor | C06 | 10 MC | Tag science. Requiere 4 tags de ciencia. +4 producción energía |
| `earth_elevator` | Earth Elevator | C08 | 43 MC | Tags earth+power. +3 producción titanio |
| `cryo_sleep` | Cryo-Sleep | C07 | 10 MC | Tag science. Pasivo: comerciar cuesta 1 recurso menos (mecánica de colonias/comercio, ver sección dedicada abajo) |
| `ecology_research` | Ecology Research | C09 | 21 MC | Tags science+animal+microbe+plant. +1 producción plantas por cada colonia propia, +1 recurso a una carta activa elegida y +2 a otra distinta |
| `floater_prototypes` | Floater Prototypes | C11 | 2 MC | Tag science, evento. +2 floaters a OTRA carta activa elegida |
| `floater_technology` | Floater Technology | C12 | 7 MC | Tag science. Acción repetible sin costo: +1 floater a OTRA carta activa elegida |
| `galilean_waystation` | Galilean Waystation | C13 | 15 MC | Tag power. +1 producción MC por cada tag jovian jugado |
| `heavy_taxation` | Heavy Taxation | C14 | 3 MC | Doble tag earth. Requiere 2 tags earth jugados. +4 MC, +2 producción MC |
| `ice_moon_colony` | Ice Moon Colony | C15 | 23 MC | Tag power. Construye 1 colonia (pieza nueva `build_colony`) y coloca 1 océano |
| `impactor_swarm` | Impactor Swarm | C16 | 11 MC | Doble tag jovian, evento. Requiere 2 tags jovian jugados. +12 calor (cláusula "remove up to 2 plants from any player" omitida) |
| `interplanetary_colony_ship` | Interplanetary Colony Ship | C17 | 12 MC | Tags earth+power, evento. Construye 1 colonia |
| `jovian_lanterns` | Jovian Lanterns | C18 | 20 MC | Tag jovian. Requiere 1 tag jovian jugado. +1 TR, +2 floaters a una carta activa elegida; acción repetible: -1 titanio → +2 floaters a sí misma |
| `jupiter_floating_station` | Jupiter Floating Station | C19 | 9 MC | Tag jovian. Requiere 3 tags de ciencia. Acción con elección: +1 floater a OTRA carta activa elegida, O +1 MC por cada floater guardado (sin gastarlos, pieza nueva `mc_per_card_resource`, tope 4) |
| `luna_governor` | Luna Governor | C20 | 4 MC | Doble tag earth. Requiere 3 tags earth jugados. +2 producción MC |
| `lunar_exports` | Lunar Exports | C21 | 19 MC | Tags power+earth. Elección: +2 producción plantas O +5 producción MC |
| `lunar_mining` | Lunar Mining | C22 | 11 MC | Tag earth. +1 producción titanio cada 2 tags earth (incluida esta) |
| `market_manipulation` | Market Manipulation | C23 | 1 MC | Tag earth, evento. +1 paso a una colonia elegida, -1 paso a otra (pieza nueva `adjust_colony_tracks`) |
| `martian_zoo` | Martian Zoo | C24 | 12 MC | Tags animal+building. Requiere 2 ciudades en juego. Pasivo: +1 animal por cada tag earth jugado; acción repetible sin costo: +1 MC por cada animal guardado (sin gastarlos) |
| `mining_colony` | Mining Colony | C25 | 20 MC | Tag power. +1 producción titanio, construye 1 colonia |
| `minority_refuge` | Minority Refuge | C26 | 5 MC | Tag power. -2 producción MC, construye 1 colonia |
| `molecular_printing` | Molecular Printing | C27 | 11 MC | Tag science. +1 MC por cada ciudad en el mapa, +1 MC por cada colonia en juego (pieza nueva `mc_per_colony_in_play`) |
| `nitrogen_from_titan` | Nitrogen from Titan | C28 | 25 MC | Tags jovian+power. +2 TR, +2 floaters a una carta Jovian activa elegida |
| `pioneer_settlement` | Pioneer Settlement | C29 | 13 MC | Tag power. Requiere máximo 1 colonia propia (pieza nueva `max_colonies_owned`). -2 producción MC, construye 1 colonia |
| `productive_outpost` | Productive Outpost | C30 | 0 MC | Sin tags propios. Aplica el colony bonus de cada colonia propia una vez (pieza nueva `gain_all_colony_bonuses`) |
| `quantum_communications` | Quantum Communications | C31 | 8 MC | Tag science. Requiere 4 tags de ciencia. +1 producción MC por cada colonia en juego (pieza nueva `production_delta_per_colony_in_play`) |
| `red_spot_observatory` | Red Spot Observatory | C32 | 17 MC | Tags science+jovian. Requiere 3 tags de ciencia. Roba 2 cartas; acción con elección: +1 floater a sí misma, O gastar 1 floater propio → roba 1 carta |
| `refugee_camps` | Refugee Camps | C33 | 10 MC | Tag earth. Acción repetible sin costo de stock: -1 producción MC → +1 recurso en la carta |
| `research_colony` | Research Colony | C34 | 20 MC | Tags science+power. Construye 1 colonia, puede repetirse en una donde ya tiene (pieza nueva `build_colony.allow_duplicate`) |
| `rim_freighters` | Rim Freighters | C35 | 4 MC | Tag power. Pasivo: comerciar cuesta 1 recurso menos (mismo patrón de Cryo-Sleep) |
| `sky_docks` | Sky Docks | C36 | 18 MC | Tags earth+power. Requiere 2 tags earth jugados. +1 flota de comercio (pieza nueva `trade_fleet_delta`) |
| `solar_probe` | Solar Probe | C37 | 9 MC | Tag power, evento. Roba 1 carta cada 3 tags de ciencia, incluida esta (pieza nueva `draw_cards_per_tag`) |
| `solar_reflectors` | Solar Reflectors | C38 | 23 MC | Tag power. +5 producción calor |
| `space_port` | Space Port | C39 | 22 MC | Tags city+building. Requiere 1 colonia propia (pieza nueva `min_colonies_owned`). +1 flota de comercio, +1 ciudad, -1 producción energía, +4 producción MC |
| `space_port_colony` | Space Port Colony | C40 | 27 MC | Tag power. Requiere 1 colonia propia. Construye 1 colonia (puede repetirse en una donde ya tiene), +1 flota de comercio |
| `spin_off_department` | Spin-Off Department | C41 | 10 MC | Tag building. +2 producción MC. Pasivo: roba 1 carta cada vez que juega una carta de costo impreso ≥20 MC (pieza nueva `on_card_played_cost_threshold_draw`) |
| `sub_zero_salt_fish` | Sub-Zero Salt Fish | C42 | 5 MC | Tag animal. Requiere temperatura ≤-6°C. -1 producción plantas; acción repetible sin costo: +1 animal en la carta |
| `titan_air_scrapping` | Titan Air-Scrapping | C43 | 21 MC | Tag jovian. Acción con elección: -1 titanio → +2 floaters a sí misma, O gastar 2 floaters propios → +1 TR |
| `titan_shuttles` | Titan Shuttles | C45 | 23 MC | Tags jovian+power. Acción con elección: +2 floaters a OTRA carta Jovian activa elegida, O convertir X floaters propios → X titanio |
| `trade_envoys` | Trade Envoys | C46 | 6 MC | Tag power. Pasivo: al comerciar puede subir 1 paso esa colonia antes de cobrar (pieza nueva `trade_bump_track_first`) |
| `trading_colony` | Trading Colony | C47 | 18 MC | Tag power. Mismo pasivo que Trade Envoys, construye 1 colonia |
| `urban_decomposers` | Urban Decomposers | C48 | 6 MC | Tags building+microbe. Requiere 1 ciudad y 1 colonia en juego. +1 producción plantas, +2 microbios a OTRA carta activa elegida |
| `warp_drive` | Warp Drive | C49 | 14 MC | Tag science. Requiere 5 tags de ciencia. Pasivo: cartas con tag space cuestan 4 MC menos |
| `house_printing` | House Printing | P36 | 10 MC | Tag building, expansión **Prelude** (primera carta cargada de esta expansión — no necesita mecánica propia, se dealt 2 gratis en el setup real, no modelado todavía). +1 producción steel |
| `titan_floating_launch_pad` | Titan Floating Launch-Pad | C44 | 18 MC | Tag jovian. +2 floaters a cualquier carta Jovian elegida. Acción con elección: +1 floater a OTRA carta Jovian elegida, O gastar 1 floater propio → comerciar GRATIS (pieza nueva `free_trade`, resuelta 2026-09-03 — ver sección dedicada abajo) |
| `lava_tube_settlement` | Lava Tube Settlement | P37 | 15 MC | Tags city+building, expansión **Prelude**. -1 producción energía, +2 producción MC. Coloca 1 ciudad EN UN HEXÁGONO VOLCÁNICO, ignorando la regla normal de no-adyacencia a otras ciudades (pieza nueva `board.can_place_city_on_volcanic` + flag `city_placement_on_volcanic` en `play_card`) |
| `martian_survey` | Martian Survey | P38 | 9 MC | Tag science. Requiere oxígeno ≤4%. Roba 2 cartas |
| `sf_memorial` | SF Memorial | P41 | 7 MC | Tag building. Roba 1 carta |
| `space_hotels` | Space Hotels | P42 | 12 MC | Tags earth+earth. Requiere 2 tags earth jugados. +4 producción MC |
| `ceres_tech_market` | Ceres Tech Market | P68 | 12 MC | Tags science+power, expansión **Venus Next** (promo). +2 MC por cada colonia propia (pieza nueva `resource_delta_per_colony`, análogo stock de `production_delta_per_colony`). Acción repetible sin costo: descartar N cartas → +2 MC por cada una (pieza nueva `mc_per_discarded_card`, mismo criterio de confianza en `effect_amount` que `standard_project_sell_patents` — no valida IDs puntuales de mano) |
| `cloud_tourism` | Cloud Tourism | P69 | 11 MC | Tags jovian+venus, expansión **Venus Next** (promo). +1 producción MC por cada par de tags earth+venus jugados (pieza nueva `production_delta_per_tag_pair`, usa el mínimo de ambos conteos). Acción repetible sin costo: +1 floater a sí misma |
| `dirigibles` | Dirigibles | 222 | 11 MC | Tag venus. Pasivo: floaters guardados en esta carta valen 3 M€ cada uno para pagar cartas con tag venus (pieza nueva `card_resource_payment`, resuelta 2026-09-04 — ver sección dedicada abajo). Acción repetible sin costo: +1 floater a CUALQUIER carta activa elegida, incluida ella misma (pieza nueva `target_card_resource_delta_allow_self`) |
| `psychrophiles` | Psychrophiles | P39 | 2 MC | Tag microbe, expansión **Prelude**. Requiere temperatura ≤-20°C. Pasivo: microbios guardados en esta carta valen 2 M€ cada uno para pagar cartas con tag plant (mismo `card_resource_payment` que Dirigibles). Acción repetible sin costo: +1 microbio a sí misma |
| `research_coordination` | Research Coordination | P40 | 4 MC | Tag **wild** (ícono "?"), expansión **Prelude**. Sin efecto inmediato. El tag "wild" cuenta como cualquier tag elegido por el jugador para cubrir un requisito `min_tag_count` puntual al jugar OTRA carta (pieza nueva `wild_tag_choice`, resuelta 2026-09-04 — ver sección dedicada abajo) |
| `colonial_envoys` | Colonial Envoys | P70 | 4 MC | Sin tags, expansión **Prelude 2**. Requiere que el partido Unity esté gobernando o tener 2 delegados propios ahí (pieza nueva `ruling_or_delegates`). Coloca 1 delegado por cada colonia propia, en los partidos que el jugador elija (pieza nueva `place_delegates_per_colony`, expansión **Turmoil** — ver sección dedicada abajo) |
| `colonial_representation` | Colonial Representation | P71 | 10 MC | Sin tags, expansión **Prelude 2**. +3 MC por cada colonia propia (`resource_delta_per_colony`, ya existente). Pasivo: +1 Influencia fija (pieza nueva `influence_bonus`, expansión **Turmoil** — ver sección dedicada abajo) |
| `aerosport_tournament` | Aerosport Tournament | 214 | 7 MC | Tag venus, evento, expansión **Venus Next**. Requiere 5 floaters guardados entre TODAS las cartas activas (pieza nueva `min_total_card_resources` — ver sección dedicada abajo). +1 MC por cada ciudad en el mapa (`mc_per_counter`, ya existente) |
| `airliners` | Airliners | C01 | 11 MC | Sin tags, expansión **Colonies**. Requiere 3 floaters guardados. +2 producción MC. +2 floaters a OTRA carta que coleccione floaters (pieza nueva `target_card_resource_delta_typed`) |
| `floater_leasing` | Floater Leasing | C10 | 3 MC | Sin tags, expansión **Colonies**. +1 producción MC por cada 3 floaters guardados entre todas las cartas activas (pieza nueva `production_delta_per_card_resource_type`) |

| `envoys_from_venus` | Envoys from Venus | P72 | 1 MC | Tag venus, evento, **Prelude 2**. Requiere 3 tags venus. Coloca 2 delegados en 1 partido (pieza nueva `place_delegates`) |
| `ghg_shipment` | GHG Shipment | P75 | 3 MC | Tag space, evento, **Prelude 2**. Requiere Kelvinists gobernando o 2 delegados propios ahí. +1 producción calor, +1 calor por cada floater guardado en cualquier carta activa (pieza nueva `resource_delta_per_card_resource_type`) |
| `ishtar_expedition` | Ishtar Expedition | P76 | 6 MC | Tag venus, evento, **Venus Next**. Requiere Venus ≥10%. +3 titanio, roba 2 cartas con tag venus (pieza nueva `draw_cards_matching_tag`) |
| `jovian_envoys` | Jovian Envoys | P77 | 2 MC | Sin tags, evento, **Prelude 2**. Requiere 2 tags jovian. Coloca 2 delegados en 1 partido |
| `microgravity_nutrition` | Microgravity Nutrition | P79 | 11 MC | Tags microbe+plant, **Prelude 2**. +1 producción MC por cada colonia propia |
| `soil_studies` | Soil Studies | P81 | 13 MC | Tags microbe+plant, evento, **Venus Next**. Requiere temperatura ≤-4°C. +1 planta por cada tag venus, por cada tag plant (incluida esta) y por cada colonia (pieza nueva `resource_delta_per_tag`) |
| `special_permit` | Special Permit | P82 | 5 MC | Tag plant, evento, **Prelude 2**. Requiere Greens gobernando o 2 delegados ahí. "Steal 4 plants from any player" → se omite entera en un solo jugador, `effects: {}` |
| `sponsoring_nation` | Sponsoring Nation | P83 | 21 MC | Tag earth, **Prelude 2**. Requiere 4 tags earth. +3 TR y coloca 2 delegados |
| `stratospheric_expedition` | Stratospheric Expedition | P84 | 12 MC | Tags venus+space, evento, **Venus Next**. +2 floaters a cualquier carta que coleccione floaters, roba 2 cartas venus |
| `summit_logistics` | Summit Logistics | P85 | 10 MC | Tags building+space, **Prelude 2**. Requiere Scientists gobernando o 2 delegados ahí. +1 MC por cada tag "de planeta" (jovian/earth/venus) y por cada colonia. Roba 2 cartas |
| `unexpected_application` | Unexpected Application | P86 | 4 MC | Tag venus, evento, **Venus Next**. Descarta 1 carta para subir Venus 1 paso (`discard_card_then_draw` con `draw: 0`) |
| `venus_allies` | Venus Allies | P87 | 30 MC | Tag venus, **Venus Next**. +2 pasos de Venus, +4 MC por cada colonia propia |
| `venus_trade_hub` | Venus Trade Hub | P90 | 12 MC | Tags venus+venus, **Venus Next**. Requiere 2 tags venus. Pasivo: +3 MC cada vez que comercia (pieza nueva `mc_delta_on_trade`) |
| `aerial_lenses` | Aerial Lenses | T01 | 2 MC | Tag power, **Turmoil**. Requiere Kelvinists gobernando o 2 delegados ahí. +2 producción calor (la cláusula "remove up to 2 plants from any player" se omite por diseño) |
| `banned_delegate` | Banned Delegate | T02 | 0 MC | Sin tags, evento, **Turmoil**. Requiere ser Chairman (requirement nuevo `is_chairman`). Remueve 1 delegado propio NO-líder, que vuelve a la Reserva (pieza nueva `turmoil.remove_delegate`; el FAQ confirma que puede cambiar el partido Dominante al instante) |
| `cultural_metropolis` | Cultural Metropolis | T03 | 20 MC | Tags city+building, **Turmoil**. Requiere Unity gobernando o 2 delegados ahí. -1 producción energía, +3 producción MC, coloca 1 ciudad y 2 delegados en 1 partido |

## Pendientes (requieren una pieza de mecánica que todavía no se agregó)

Estas NO son descartes definitivos — son casos donde ya se identificó qué falta agregar al
motor para desbloquearlas. Se resuelven agregando esa pieza, no evitando la carta.

| # scan | Nombre | Qué falta |
|---|---|---|

### Turmoil: núcleo político (Colonial Envoys, Colonial Representation)

**Resuelto (2026-09-04, decisión explícita del usuario).** Módulo nuevo
`backend/app/agent/turmoil.py` (mismo estilo que `colonies.py`/`board.py`), verificado contra el
rulebook oficial de la expansión (fryxgames.se, TM_TURMOIL_ENG_RULES.pdf, 8 páginas, leído
completo): 6 partidos (Mars First, Kelvinists, Reds, Greens, Unity, Scientists), delegados
(cada jugador arranca con 7: 1 en el Lobby, 6 en la Reserva), acción "Lobbying" (gratis desde el
Lobby, 5 MC desde la Reserva), Party Leader (primer delegado de un partido, reemplazado si otro
jugador consigue más ahí), partido Dominante (el de más delegados totales, se actualiza al
instante), requisitos de carta gateados por partido ("ruling_or_delegates": Ruling actual O 2+
delegados propios), Influencia (Chairman +1, líder del Dominante +1, o 1+ delegados no-líder ahí
+1 — mutuamente excluyente para el mismo jugador — más bonus de carta), y "New Government"
(Dominante pasa a Ruling, su líder se vuelve Chairman, delegados vuelven a la reserva).

**Alcance de esta primera pasada — QUEDAN EXPLÍCITAMENTE PENDIENTES, cada uno del tamaño de una
feature aparte** (mismo criterio que "solo Callisto cargada" en Colonies):
- Las Ruling Bonus / Ruling Policy de los 6 partidos (12 efectos distintos sobre recursos de
  TODOS los jugadores, ej. Reds: "Lose 3 M€ for each step your TR is raised").
- El mazo de Global Event cards -- EN PROGRESO desde 2026-09-04, ver sección dedicada
  "Turmoil: Global Events" abajo (2 de 36 cargadas).
- La revisión de TR (-1 a TODOS los jugadores cada generación).
- `resolve_new_government` está ACOTADO a un solo jugador (modo un jugador de este proyecto,
  ver sección 7 de `CLAUDE.md`) — no itera sobre otros jugadores ni aplica el TR gratis del
  Chairman.

Campos nuevos en `PlayerState`: `lobby_delegates` (arranca en 1), `reserve_delegates` (arranca
en 6). Estado compartido nuevo (cargado/guardado aparte, igual que `board`/`colonies`):
`turmoil` en `GlobalParameters`. Tools nuevas: `lobby`, `resolve_new_government`,
`get_turmoil_state`. Piezas nuevas en el motor: requirement `ruling_or_delegates` en
`check_card_requirements` (necesita `turmoil` + `player_id`), pasivo `influence_bonus` en
`register_passive_effect` (la fórmula base de Influencia vive en `turmoil.compute_influence`,
no en `rules_engine.py` — mismo criterio de desacople que `free_trade`), effect
`place_delegates_per_colony` resuelto en `tools.play_card` (parámetro nuevo
`delegate_party_choices`, sale de la Reserva del jugador, no del Lobby).

Esto desbloqueó **Colonial Envoys** (P70, Prelude 2) y **Colonial Representation** (P71,
Prelude 2), las 2 cartas pendientes que dependían de esto. Tests: `test_turmoil.py` (mecanismo
completo) y los tests de las 2 cartas en `test_rules_engine.py`.

### Bloque 31 (2026-09-04): multi-agente, y por qué la revisión importa

Segunda tanda de revisión de catálogo con 4 agentes en paralelo (30 cartas). **Hallazgo central
de la revisión: dos de los cuatro agentes leyeron mal los TAGS de varias cartas.** Confundieron
el recuadro de **requisito** (arriba a la izquierda, pegado al costo, dentro de una cajita) con
los **tags propios** de la carta (arriba a la derecha, íconos sueltos). Ejemplos reales:

| Carta | Reportado por el agente | Verificado contra el scan |
|---|---|---|
| P72 Envoys from Venus | `venus × 3` | **`venus` × 1** (el "VVV" era el requisito "3 tags venus") |
| P77 Jovian Envoys | `jovian × 2` | **sin tags** (los 2 Júpiter eran el requisito) |
| P78 L1 Trade Terminal | sin tags | **`space`** |
| P75 GHG Shipment | `power` | **`space`** |
| P83 Sponsoring Nation | `earth × 3` | **`earth` × 1** (los 3 íconos eran el "+3 TR" del efecto) |
| P85 Summit Logistics | `science, building, space` | **`building, space`** (el matraz era el requisito del partido Scientists) |
| P82 Special Permit | sin tags | **`plant`** |

Los tags no son cosméticos: alimentan requisitos (`min_tag_count`), descuentos por tag y el
conteo de otras cartas. Cargarlos mal habría roto silenciosamente varias interacciones. **Por eso
los tags de los grupos A y B se re-verificaron uno por uno contra los scans antes de cargar** —
los valores en `seed_cards.sql` son los verificados, no los reportados. El grupo C, en cambio,
distinguió correctamente los íconos de partido de los tags en todas sus cartas (verificado por
muestreo).

**Lección para próximas tandas:** el prompt del agente debe explicitar la diferencia entre el
recuadro de requisito y los tags, y pedir que reporte ambos por separado.

**Resultado: 16 de 30 cargadas.** 7 revisadas pero pendientes por mecánica (ver abajo) y 7
(T04-T10) sin analizar — el agente que las tenía asignadas se cortó por límite de sesión, quedan
en la cola con `reviewed = false`.

**Pendientes por mecánica de este bloque** (marcadas `reviewed = true` con `card_id = null`):
- **P73 Floating Refinery** — necesita dos piezas: recursos iniciales de carta activa escalados
  por tag (`active_card_starting_resources` hoy es un N fijo), y un costo de acción que gaste
  recursos de CUALQUIER carta activa, no solo de la propia.
- **P74 Frontier Town** — "gain the printed placement bonus 2 additional times": exige un
  multiplicador de bonus en `board.place_city_tile`, no una extensión de `effects`.
- **P78 L1 Trade Terminal** — necesita `trade_bump_track_first` parametrizable a N pasos (hoy es
  booleano y sube 1 fijo; retrofit menor sobre Trade Envoys/Trading Colony) y poder apuntar a 3
  cartas objetivo distintas (hoy el máximo es 2).
- **P80 Red Appeasement** — el costo de su acción es gastar 2 delegados propios; falta integrar
  el estado de Turmoil a `use_card_action` (hoy solo `check_card_requirements` lo recibe).
- **P88 Venus Orbital Survey** — revelar el tope del mazo, quedarse gratis con las que tengan tag
  venus y comprar/descartar el resto.
- **P89 Venus Shuttles** — costo de acción reducido por cada tag venus (costo dinámico, hoy los
  costos de acción son fijos).
- **P91 WG Project** — requiere ser Chairman (ya resuelto), pero además un sub-mazo de Prelude
  separado y un mecanismo para jugar gratis una carta arbitraria revelada.

### Recursos tipados por carta activa (floaters entre cartas)

**Resuelto (2026-09-04).** Hasta ahora `active_cards[card_id]["resources"]` era un contador SIN
tipo -- no distinguía si eran floaters, microbios o animales, así que no había forma de sumar
"solo los floaters" entre varias cartas activas. Bloqueaba 5 cartas desde el bloque 25/30
(Aerosport Tournament, Airliners, Floater Leasing, Cloud Societies, Corrosive Rain).

- `rules_engine.register_active_card` suma el parámetro `resource_type: str | None` (ej.
  "floater", "microbe"). Se guarda como una clave más en `active_cards[card_id]`. Viene de
  `effects.active_card_resource_type` en la fila de `cards`/`global_events`, leído por
  `tools.play_card`.
- `rules_engine.sum_card_resources_by_type(player, resource_type)`: suma `resources` de TODAS
  las cartas activas que matcheen ese tipo.
- Requirement nuevo `min_total_card_resources`: {"resource_type", "count"} en
  `check_card_requirements` (ej. Aerosport Tournament: 5 floaters).
- Effects nuevos en `apply_card_effect`:
  - `target_card_resource_delta_typed`: {"resource_type", "amount" | "amount_per_influence"} --
    como `target_card_resource_delta` pero exige que la carta objetivo tenga ese tipo (ej.
    Airliners: +2 floaters a otra carta que coleccione floaters; Corrosive Rain: -2 floaters de
    una carta elegida; Cloud Societies: +1 floater por Influencia a una carta elegida).
  - `add_resource_to_all_matching_type`: {"resource_type", "amount"} -- suma a TODAS las cartas
    activas que matcheen, sin elegir una (ej. Cloud Societies: +1 floater a cada carta que
    coleccione floaters).
  - `production_delta_per_card_resource_type`: {"resource_type", "production", "divisor",
    "per_unit"} -- produción según el total sumado, dividido entero (ej. Floater Leasing: +1
    producción MC cada 3 floaters).

Desbloqueó **Aerosport Tournament** (214, Venus Next), **Airliners** (C01, Colonies) y
**Floater Leasing** (C10, Colonies) en el catálogo normal, más **Cloud Societies** y
**Corrosive Rain** en Global Events (ver sección de abajo). El mecanismo es genérico -- futuras
cartas que acumulen floaters/microbios/etc. y necesiten sumarlos entre cartas solo declaran
`active_card_resource_type` al registrarse, sin tocar código nuevo.

### Turmoil: Global Events (mazo separado, EN PROGRESO)

**Fuente de datos:** a diferencia del catálogo normal de cartas de proyecto (`card_review_queue`,
scans de tm.hadronikle.com), los Global Events son un mazo APARTE de la expansión Turmoil. El
mismo sitio los cataloga bajo la categoría `"GlobalEvent"` en su índice cacheado
(`https://raw.githubusercontent.com/hadronikle/Complete-Terraforming-Mars-Card-Database/main/index.html`,
array `const CARDS = [...]`), con imágenes en `https://cards.hadronikle.com/global-events/<...>.png`.
Ese índice trae **36 Global Events** con tag `"GlobalEvent"` bajo expansión Turmoil — el rulebook
oficial dice "31 Global Event cards" en la lista de componentes (página 8), así que hay una
diferencia de 5 sin explicar todavía (posibles variantes/erratas de ediciones distintas
incluidas en el mismo índice) — **no bloquea empezar a cargarlas**: se verifica carta por carta
igual que el catálogo normal, y si alguna resulta ser una variante/duplicado se documenta acá al
encontrarla. Tabla nueva `global_event_review_queue` (mismo patrón que `card_review_queue`, sin
`scan_number` porque el sitio no numera esta categoría — el nombre es la clave única) tiene las
36 filas cargadas: 2 `reviewed = true`, 34 pendientes.

**Mecanismo de motor (2026-09-04):** los Global Events reusan el mismo `effects` jsonb y la
misma función `rules_engine.apply_card_effect` que las cartas de proyecto — no hace falta un
motor aparte, solo una tabla `global_events` (id, name, effects) distinta de `cards` porque no
tienen costo/tags/requirements. Pieza nueva de vocabulario: `resource_delta_per_capped_counter`
(ver `rules_engine.apply_card_effect`, docstring completo) -- implementa la regla del rulebook
(página 5): "Any Global Event that counts something... can only count up to a maximum of 5. This
number can then be modified up or down (even beyond 5) by your influence." El contador se resuelve
con `_resolve_capped_counter` (fuentes soportadas hoy: `city_tiles_placed`,
`tr_sets_of_5_over_15` — se agregan fuentes nuevas a medida que aparecen en cartas reales, no de
antemano). `tools.resolve_global_event(player_id, event_id)` calcula la Influencia del jugador
(`turmoil.compute_influence`) y se la pasa al motor como un entero simple (parámetro `influence`)
-- `rules_engine.py` NO importa `turmoil.py`, mismo desacople que el resto de las piezas de
Turmoil ya resueltas.

**33 de 36 cargadas** (bloque 1: 2, verificadas contra el rulebook oficial -- más fuerte que un
scan individual, trae el texto impreso Y un ejemplo numérico resuelto paso a paso, página 5;
bloques 2-5, 2026-09-04: 31 más, verificadas contra su scan real):

| id | Nombre | Efecto |
|---|---|---|
| `generous_funding` | Generous Funding | +2 M€ por cada set de 5 TR sobre 15 (tope 5 sets) + Influencia SUMA sets. Ejemplo del rulebook: TR 42 (5 sets) + 2 Influencia = 7 × 2 = 14 M€ |
| `riots` | Riots | -4 M€ por cada ciudad en el mapa (tope 5 ciudades) − Influencia RESTA ciudades contadas. Ejemplo del rulebook: 7 ciudades (capa a 5) − 1 Influencia = 4 × 4 = 16 M€ perdidos |
| `aquifer_released_by_public_council` | Aquifer Released by Public Council | Coloca 1 océano (+1 TR, `place_oceans`). +1 planta y +1 acero por cada punto de Influencia, SIN tope (pieza nueva `resource_delta_per_influence`) |
| `asteroid_mining` | Asteroid Mining | +1 titanio por cada tag jovian jugado (tope 5) + Influencia SUMA (mismo `resource_delta_per_capped_counter`, contador nuevo `tag:<tag>`) |
| `celebrity_leaders` | Celebrity Leaders | +2 M€ por cada evento jugado históricamente (tope 5) + Influencia SUMA (contador nuevo `events_played`) |
| `diversity` | Diversity | +10 M€ si el jugador tiene 9+ tags DISTINTOS jugados, contando la Influencia como tags extra (pieza nueva `resource_delta_if_tag_diversity`, umbral booleano SIN tope de 5 -- el tope de 5 solo aplica a contadores que se multiplican, no a un chequeo de umbral) |
| `cloud_societies` | Cloud Societies | +1 floater a CADA carta activa que coleccione floaters (pieza nueva `add_resource_to_all_matching_type`). +1 floater por Influencia a UNA carta elegida (pieza nueva, `target_card_resource_delta_typed` con `amount_per_influence`) |
| `corrosive_rain` | Corrosive Rain | Elección: perder 2 floaters de una carta propia (`target_card_resource_delta_typed`, amount=-2) O perder 10 M€. Cualquiera sea la elección: roba 1 carta por Influencia (pieza nueva `draw_cards_per_influence`) |
| `eco_sabotage` | Eco Sabotage | Pierde todas las plantas salvo 3 + Influencia (pieza nueva `resource_delta_clamp_to_capped_max`, techo -- nunca sube el stock) |
| `election` | Election | Puntaje = Influencia + tags building + ciudades en el mapa (sin tope). La carta imprime la regla exacta de un jugador: ≥10 gana 2 TR, ≥5 gana 1 TR (pieza nueva `tr_delta_by_threshold`) |
| `global_dust_storm` | Global Dust Storm | Pierde todo el calor (pieza nueva `resource_set_to_zero`). -2 M€ por cada tag building (tope 5) − Influencia (mismo `resource_delta_per_capped_counter`) |
| `homeworld_support` | Homeworld Support | +2 M€ por cada tag earth (tope 5) + Influencia (mismo `resource_delta_per_capped_counter`) |
| `improved_energy_templates` | Improved Energy Templates | +1 producción energía por cada 2 tags power + Influencia, SIN tope (pieza nueva `production_delta_per_tag_plus_influence`) |
| `interplanetary_trade` | Interplanetary Trade | +2 M€ por cada tag space (tope 5) + Influencia |
| `jovian_tax_rights` | Jovian Tax Rights | +1 producción MC por cada colonia propia. +1 titanio por Influencia |
| `microgravity_health_problems` | Microgravity Health Problems | -3 M€ por cada colonia propia (tope 5) − Influencia (contador nuevo `colonies_owned`) |
| `miners_on_strike` | Miners on Strike | -1 titanio por cada tag jovian (tope 5) − Influencia |
| `pandemic` | Pandemic | -3 M€ por cada tag building (tope 5) − Influencia |
| `productivity` | Productivity | +1 acero por cada punto de producción de acero (tope 5) + Influencia (contador nuevo `<recurso>_production`) |
| `revolution` | Revolution | La carta imprime su regla de solitario: si tags earth + Influencia ≥ 4, -2 TR (`tr_delta_by_threshold` con umbral negativo) |
| `sabotage` | Sabotage | -1 producción acero y -1 producción energía. +1 acero por Influencia |
| `paradigm_breakdown` | Paradigm Breakdown | Descarta 2 cartas elegidas de la mano (pieza nueva `discard_cards` + parámetro `discard_card_ids`). +2 M€ por Influencia |
| `red_influence` | Red Influence | -3 M€ por cada set de 5 TR sobre 10 (tope 5 sets) — la Influencia NO ajusta ese conteo acá (pieza nueva `influence_direction: "none"`, contador nuevo `tr_sets_of_5_over:<N>`). +1 producción MC por Influencia (pieza nueva `production_delta_per_influence`) |
| `scientific_community` | Scientific Community | +1 M€ por cada carta en mano + Influencia, SIN tope — la carta imprime "no limit" (piezas nuevas: contador `hand_size` y `cap: null`) |
| `snow_cover` | Snow Cover | BAJA la temperatura 2 pasos sin tocar el TR (pieza nueva `lower_temperature_steps`). Roba 1 carta por Influencia |
| `solar_flare` | Solar Flare | -3 M€ por cada tag space (tope 5) − Influencia |
| `spin_off_products` | Spin-off Products | +2 M€ por cada tag science (tope 5) + Influencia |
| `sponsored_projects` | Sponsored Projects | +1 recurso a TODA carta activa que ya tenga al menos 1, sin filtrar por tipo (pieza nueva `add_resource_to_all_cards_with_resources`). Roba 1 carta por Influencia |
| `strong_society` | Strong Society | +2 M€ por cada ciudad en el mapa (tope 5) + Influencia |
| `successful_organisms` | Successful Organisms | +1 planta por cada punto de producción de plantas (tope 5) + Influencia |
| `venus_infrastructure` | Venus Infrastructure | +2 M€ por cada tag venus (tope 5) + Influencia |
| `volcanic_eruptions` | Volcanic Eruptions | +2 pasos de temperatura (+2 TR). +1 producción calor por Influencia |
| `war_on_earth` | War on Earth | -4 TR, y cada punto de Influencia evita 1 paso; nunca se convierte en ganancia (pieza nueva `tr_delta_reduced_by_influence`) |

**1 pendiente del bloque 4 -- Dry Deserts**: "First player removes 1 ocean tile from the
gameboard. Gain 1 standard resource per influence." Dos piezas faltantes a la vez: (a) el
tablero hexagonal no está wireado a `resolve_global_event` (mismo alcance no resuelto que
`resolve_new_government`), y no está claro si "remover un tile" debería bajar
`globals_["oceans_placed"]` (el contador usado para fin de partida/TR) o solo liberar el hex
físico -- necesita una decisión antes de modelarlo, no un supuesto; (b) "gain 1 standard
resource" es una elección del jugador entre los 6 recursos básicos (MC/acero/titanio/planta/
energía/calor), pieza de "elección de recurso genérica" todavía no construida. Pospuesta hasta
resolver ambas.

### Bloque 5 (2026-09-04): las 22 restantes, analizadas en paralelo por 4 agentes

Único bloque hecho con **orquestación multi-agente**: se repartieron las 22 cartas que quedaban
en 4 grupos, un agente (Sonnet) por grupo. Cada agente leyó el vocabulario del motor
(`apply_card_effect` + `_resolve_capped_counter`), descargó sus scans espaciados 4s, transcribió
el texto exacto de cada carta y propuso el `effects` JSON + casos de test, **sin tocar ningún
archivo del repo** (así no competían por `rules_engine.py`/`seed_global_events.sql`; la
integración, verificación y escritura de código quedó en un solo lugar). Los scans se borraron
al terminar cada agente.

**Verificación de la revisión (no se aceptaron los informes a ciegas):** se re-descargaron y
releyeron 3 scans de muestra — Microgravity Health Problems (grupo A, motivó contador nuevo),
Red Influence y Scientific Community (grupo B, motivaron cambios de SEMÁNTICA del motor:
`influence_direction: "none"` y `cap: null`). Las 3 transcripciones coincidieron exactamente con
lo reportado.

| Grupo | Cartas | Resultado |
|---|---|---|
| **A** | Interplanetary Trade, Jovian Tax Rights, Microgravity Health Problems, Miners on Strike, Mud Slides, Pandemic | 5 cargadas, 1 pendiente (Mud Slides). Detectó que faltaba el contador `colonies_owned` |
| **B** | Paradigm Breakdown, Productivity, Red Influence, Revolution, Sabotage, Scientific Community | 6 cargadas. Detectó 3 huecos de semántica: `influence_direction: "none"` (Red Influence usa la Influencia en una cláusula APARTE, no ajustando el contador), `cap: null` (Scientific Community imprime "no limit", contradiciendo el tope 5 por defecto) y el umbral de TR parametrizable (`tr_sets_of_5_over:<N>`) |
| **C** | Snow Cover, Solar Flare, Solarnet Shutdown, Spin-off Products, Sponsored Projects | 4 cargadas, 1 pendiente (Solarnet Shutdown). Detectó que el motor solo sabía SUBIR temperatura, y que `add_resource_to_all_matching_type` no cubría "todas las cartas que ya tengan recursos" sin filtrar por tipo |
| **D** | Strong Society, Successful Organisms, Venus Infrastructure, Volcanic Eruptions, War on Earth | 5 cargadas. Detectó que no existía análogo de producción para `resource_delta_per_influence`, ni forma de expresar "resta fija de TR que la Influencia evita paso a paso" |

**Piezas nuevas de motor de este bloque** (todas extensiones chicas y compatibles hacia atrás):
contadores `colonies_owned`, `hand_size`, `<recurso>_production` y `tr_sets_of_5_over:<N>`;
`cap: null` (sin tope) e `influence_direction: "none"` en `resource_delta_per_capped_counter`;
`production_delta_per_influence`, `tr_delta_reduced_by_influence`, `lower_temperature_steps`,
`add_resource_to_all_cards_with_resources`, `discard_cards` (+ parámetro `discard_card_ids` en
`apply_card_effect` y `tools.resolve_global_event`).

### Bloque 6 (2026-09-04): las 3 pendientes por mecánica — mazo COMPLETO

Segunda tanda multi-agente, esta vez de DISEÑO (no de lectura de scans): 3 agentes, uno por
carta, cada uno investigando su problema a fondo y proponiendo implementación concreta, sin
tocar el repo.

| Agente | Carta | Aporte |
|---|---|---|
| **1** | Dry Deserts | Encontró un ruling del diseñador (BGG) confirmando que el océano removido vuelve a la reserva y puede volver a colocarse. Diseñó `board.remove_ocean_tile` + el effect `remove_ocean_tile` y la pieza de elección de recurso |
| **2** | Mud Slides | Diseñó `board.count_tiles_adjacent_to_ocean` y — evaluando dos alternativas — recomendó pasar el conteo ya calculado como `int` al motor, igual que `influence`, para no romper el desacople `rules_engine` ↔ `board`. Marcó honestamente que no pudo confirmar "cada tile una vez" (BGG le devolvía 403) |
| **3** | Solarnet Shutdown | **Refutó con datos el diagnóstico anterior.** El color de carta SÍ es derivable de `is_event` + `becomes_active`/`passive`: no hacía falta columna nueva ni retrofit de ~300 cartas. Validó la regla contra 6 scans reales (6/6), incluido el caso difícil (azul con solo `passive`) |

**Lo que aportó la revisión (además de integrar):** al buscar fuente para la duda de Dry Deserts
apareció el **Comprehensive FAQ v1.7** (compilado por Jeffrey Anchan, con fuentes citadas), que
tiene una tabla de aclaraciones de Global Events. Leerla completa resolvió las dudas abiertas de
los agentes Y **destapó 4 bugs en cartas ya cargadas en bloques anteriores**:

| Carta | Bug | Corrección |
|---|---|---|
| Aquifer Released by Public Council | Se cargó con `place_oceans` (que otorga +1 TR), pero el FAQ dice "no player gets any TR or placement bonuses" | Pieza nueva `place_oceans_without_tr` |
| Jovian Tax Rights | **Errata oficial**: el texto impreso omitió "(max 5)" en el conteo de colonias | `cap: 5` en `production_delta_per_colony` |
| Snow Cover | Bajaba la temperatura aun estando en el máximo; un parámetro maximizado no vuelve a ser afectado | Guarda contra `TEMPERATURE_MAX` |
| Diversity | Contaba el tag comodín "wild" como tag distinto; el FAQ aclara que el wild NO cuenta al resolver Global Events (solo en la fase de acción) | Se excluye "wild" del conteo |

También confirmó las dudas abiertas: **Mud Slides** — "Each tile is only counted once, even if
next to multiple ocean tiles" (la interpretación del agente 2 era correcta); **Dry Deserts** —
ningún jugador pierde TR, y **si los 9 océanos ya están colocados esta parte del evento NO tiene
efecto** (regla que el agente 1 no había detectado); y los 6 recursos estándar exactos.

**Piezas nuevas del bloque 6:** `board.remove_ocean_tile`, `board.count_tiles_adjacent_to_ocean`,
effect `remove_ocean_tile` (+ parámetro `remove_ocean_hex_id` en `tools.resolve_global_event`),
contadores `board_tiles_adjacent_to_ocean` y `blue_cards_played` (ambos precalculados por
`tools.py`, mismo desacople que `influence`), `resource_delta_per_influence_choice`,
`place_oceans_without_tr`, `cap` opcional en `production_delta_per_colony`, y el clasificador
puro `rules_engine.is_blue_card`.

**Estado final del mazo: 36 de 36 cargadas, 0 pendientes.**

| id | Nombre | Efecto |
|---|---|---|
| `dry_deserts` | Dry Deserts | Saca 1 océano del mapa: el tile vuelve a la reserva, el hex queda libre y NADIE pierde TR. Si los 9 océanos ya están colocados, esa parte no tiene efecto. Gana 1 recurso básico A ELECCIÓN por Influencia |
| `mud_slides` | Mud Slides | -4 M€ por cada tile del mapa adyacente a océano, contando cada tile UNA vez (tope 5) − Influencia |
| `solarnet_shutdown` | Solarnet Shutdown | -3 M€ por cada carta AZUL jugada (tope 5) − Influencia. El color se deriva del catálogo, sin columna nueva |

**Alcance no resuelto todavía, documentado para cuando aparezca en una carta real:** el reparto
de delegados neutrales al revelar la carta (Distant → Coming → Current) y el ciclo de
generaciones no están automatizados (`resolve_global_event` es de disparo manual, no forma parte
de un `run_production_phase`/fase Turmoil todavía) — mismo criterio de alcance que
`resolve_new_government`. El tablero hexagonal tampoco está wireado a Global Events (ver Dry
Deserts arriba).

### Tag comodín "wild" (Research Coordination)

**Resuelto (2026-09-04).** El texto impreso es "After being played, when you perform an
action, the wild tag counts as any tag of your choice" — se interpretó "perform an action" en
el sentido amplio del reglamento (una de las 4 acciones de turno, incluye jugar una carta), y
se buscó dónde vive HOY en el catálogo cargado algo que cuente tags de forma que este comodín
pueda cubrir de verdad: el único lugar es `check_card_requirements` → `min_tag_count` (ej. Mass
Converter: requiere 5 tags de ciencia), que se chequea al intentar JUGAR otra carta. El resto de
los usos de `tags_played` en el motor (`production_delta_per_tag`, `tr_delta_per_tag`,
`target_card_resource_delta_per_tag`, etc.) son efectos INMEDIATOS calculados al jugar la propia
carta que los tiene, no requisitos — extender el comodín ahí sería inventar alcance que la carta
no pide.

- No hace falta ningún campo nuevo en `PlayerState` ni pasivo registrado: basta con que
  `research_coordination` tenga tag `"wild"` en su fila de `cards` — `increment_tags_played` ya
  suma cualquier string de tag a `tags_played` sin cambios, así que `tags_played["wild"]` queda
  disponible automáticamente en cuanto se juega la carta.
- `check_card_requirements` suma el parámetro opcional `wild_tag_choice: str | None`. Si
  `requirements.min_tag_count.tag` coincide con `wild_tag_choice`, se suma
  `player["tags_played"].get("wild", 0)` al conteo de ese tag para ESE chequeo puntual (no
  altera `tags_played` real, no es permanente — el jugador re-declara la elección cada vez que
  la necesita).
- `tools.play_card` suma el parámetro `wild_tag_choice`, que reenvía directo al motor.

No cambia el requirement de ninguna carta ya cargada — solo hace que, si el jugador tiene
Research Coordination en juego, pueda declarar `wild_tag_choice` al jugar una carta con
`min_tag_count` que de otra forma no alcanzaría a cumplir.

### Pago con recurso de carta (Dirigibles, Psychrophiles)

**Resuelto (2026-09-04):** pieza nueva de motor que desbloqueó las 2 cartas que quedaban
pendientes por esto desde los bloques 20-24/30. Un recurso guardado en una carta activa
(floaters en Dirigibles, microbios en Psychrophiles) funciona como TERCERA moneda de pago —
como acero/titanio, pero el stock vive en una carta puntual del jugador, no en su stock general,
y solo cubre cartas con un tag específico.

- `rules_engine.register_passive_effect` suma la pieza `"card_resource_payment": {"required_tag":
  "<tag>", "value_mc": N (default 3)}` al vocabulario de `passive` (ej. Dirigibles: tag "venus",
  3 M€ por floater; Psychrophiles: tag "plant", 2 M€ por microbio).
- `rules_engine.spend_active_card_resource(player, card_id, amount)`: función nueva, descuenta
  recursos de una carta activa (lanza `InsufficientResourcesError` si no alcanza) — distinta de
  `move_from_target_card_resource_delta` (esa mueve recursos entre dos cartas activas, no los
  gasta como pago).
- `tools.play_card` suma el parámetro `card_resource_to_pay: int`. Busca automáticamente, entre
  `player["passive_effects"]`, cuál carta activa tiene un `card_resource_payment` cuyo
  `required_tag` esté en los tags de la carta que se está jugando — no hace falta que el LLM/
  usuario indique de qué carta sale el recurso, el motor lo resuelve por el tag. Si no hay match,
  `ValueError`. El valor (`card_resource_to_pay * value_mc`) se resta del costo efectivo igual
  que cualquier otro descuento (mismo lugar que `compute_card_cost_discount`/
  `pending_mc_discount`/`compute_reserved_card_discount`), sin reembolso por sobrepago (mismo
  criterio que el resto del pago de cartas).
- `use_card_action` suma `"target_card_resource_delta_allow_self": N` al vocabulario de `gains`
  -- igual que `target_card_resource_delta` pero el destino puede ser CUALQUIER carta activa,
  incluida la propia (`target_card_id` opcional, default = la propia carta) — necesario porque
  la acción de Dirigibles es "Add 1 floater to ANY card", a diferencia de otras cartas Jovian que
  siempre exigen "OTRA carta".

Mismo patrón se aplicará a futuras cartas Venus Next/Prelude que usen floaters/microbios/otro
recurso de carta como pago — solo hace falta declarar el pasivo `card_resource_payment` en su
`effects`, sin tocar código nuevo.

### Colonies: mecánica de colonias/comercio

**Resuelto (2026-09-03):** implementada en `backend/app/agent/colonies.py` (módulo nuevo, mismo
estilo que `board.py`), verificada contra el rulebook oficial de la expansión
(TM_COLONIES_ENG_RULES, 4 páginas, leído completo) — proyecto estándar `build_colony` (17 MC),
acción `use_trade_fleet` (9 MC / 3 energía / 3 titanio, a elección), reparto de "trade income" +
"colony bonus" al comerciar, reset del track al lado de las colonias construidas, y el paso de
producción de colonias de la fase solar (el marcador sube 1 paso, las flotas vuelven a estar
disponibles). Campos nuevos en `PlayerState`: `colonies_owned`, `trade_fleets`,
`trade_fleets_used`; en `GlobalParameters` (cargado/guardado aparte, igual que `board`):
`colonies`. Tools nuevas: `setup_colonies`, `build_colony`, `use_trade_fleet`.

**Catálogo de colonias — solo Callisto cargada por ahora.** El juego real tiene 11 Colony Tiles
con nombre (Ganymede, Europa, Callisto, Titan, Enceladus, Triton, Miranda, Luna, Pluto, Ceres,
Io), cada una con su propio track de valores. Mismo criterio que el catálogo de cartas: no se
generan datos al voleo. Callisto quedó verificada con dos fuentes independientes (el ejemplo
trabajado del rulebook oficial, que muestra el track completo 0/2/3/5/7/10/13 con el marcador en
10 energía y colony bonus 3 energía; y una búsqueda independiente que reporta el mismo track).
Las otras 10 quedan sin cargar hasta verificarlas de la misma forma — el mecanismo ya es
genérico (`COLONY_DEFS`) y no hace falta tocar código para agregar una colonia nueva, solo datos
verificados. Cartas que targeteen una colonia específica por nombre distinta de Callisto quedan
pendientes hasta cargar esa colonia (ninguna hasta ahora — Cryo-Sleep y Ecology Research no
dependían de una colonia puntual).

Esto desbloqueó **Cryo-Sleep** (pasivo `trade_cost_discount`) y **Ecology Research** (efecto
nuevo `production_delta_per_colony`, que cuenta `player["colonies_owned"]` sin importar cuál).
Tests: `test_colonies.py` (mecanismo completo) y los tests de `cryo_sleep`/`ecology_research` en
`test_rules_engine.py`.

**Actualización bloque 26:** agregada la pieza `build_colony` en `apply_card_effect`/`tools.play_card`
(manejada igual que `place_special_tile`: un flag en `effects`, el `colony_id` lo pasa el caller
via el parámetro nuevo `build_colony_id`) -- construye una colonia como parte del efecto de la
carta SIN cobrar los 17 MC del proyecto estándar (ya incluidos en el costo de la carta). Cargó
Ice Moon Colony e Interplanetary Colony Ship. También `mc_per_card_resource` en `use_card_action`
(da MC por recurso guardado en la carta SIN gastarlo, con tope opcional -- distinto de
`convert_card_resource_amount`, que sí gasta) para Jupiter Floating Station.

**Resuelto (2026-09-03):** la pieza que faltaba para Titan Floating Launch-Pad (C44) — su
acción "gastar 1 floater propio para comerciar GRATIS" — quedó implementada como flag nuevo
`free_trade` en el vocabulario de `gains` de `use_card_action`. A diferencia de las demás piezas
de colonias, `rules_engine.py` NO lo procesa (a propósito, ese módulo no conoce `colonies.py`,
ver CLAUDE.md sección 3) — `tools.use_card_action` lo detecta ANTES de llamar al motor (mirando
la rama de `choice` ya resuelta), exige el parámetro nuevo `trade_colony_id`, deja que el motor
cobre el costo declarado de la acción (ej. 1 floater guardado) y DESPUÉS llama
`colonies.trade_with_colony` directo, sin cobrar el costo normal de comerciar (9 MC/3 energía/3
titanio) ni gastar una flota de comercio propia. Tests:
`test_titan_floating_launch_pad_action_choice_target_or_cost_only_for_free_trade` en
`test_rules_engine.py` (la parte que sí vive en el motor); la integración completa con
`colonies.py` no se testea a nivel `rules_engine.py` por el mismo motivo que `build_colony`/
`place_special_tile` tampoco se testean ahí -- vive enteramente en `tools.py`.

**Resuelto (2026-09-02):** la pieza que faltaba para Lava Flows (140) — colocar
tile en uno de 4 hexágonos volcánicos nombrados individualmente — quedó
implementada en `board.py`: constante `VOLCANO_NAMES` (mapea los 4 hex_ids ya
marcados `volcanic=True` a su nombre real, ver "Los 4 volcanes con nombre" en
`HEX_MAP_RESEARCH.md` para las dos fuentes usadas: coordenadas areográficas
oficiales de cada volcán + verificación cruzada con la posición ya conocida de
Noctis City) y requirement nuevo `hex_id_in` en `can_place_special_tile`
(lista cerrada de hex_ids válidos, genérico, no hardcodea la carta). Carta
cargada con costo/texto verificados contra el scan real (18 MC, evento, sin
tag). Tests: `test_volcano_names_match_the_4_volcanic_hexes`,
`test_lava_flows_can_only_place_on_one_of_the_4_named_volcanoes` en
`test_board.py`.

**Resuelto (2026-09-02):** la pieza que faltaba para Viral Enhancers (074) —
pasivo con elección del jugador que dispara con CUALQUIER carta de tag
plant/microbe/animal jugada y targetea la carta RECIÉN JUGADA, no la que
tiene el pasivo — quedó implementada en `rules_engine.py` como
`on_any_tag_played_choice` (registrado vía `register_passive_effect`,
aplicado vía `apply_any_tag_played_choice`, cableado en
`tools.play_card` con el parámetro `any_tag_played_choice`). Distinto de
`on_tag_played_choice` (targetea siempre la carta portadora del pasivo, ej.
Olympus Conference): acá el target es `card_id`, la carta que se está
jugando en esa misma llamada — funciona tanto para el auto-disparo (Viral
Enhancers jugándose a sí misma) como para cualquier otra carta con tag
coincidente jugada después. Test:
`test_viral_enhancers_any_tag_played_choice_add_or_gain` en
`test_rules_engine.py`. La carta todavía no está cargada en
`seed_cards.sql` (falta releer el scan real y confirmar costo/tags exactos)
— queda disponible para el próximo bloque de revisión de cartas, ya sin
bloqueo de mecánica.

**Resuelto (2026-09-02):** la pieza de "slot de reserva" que faltaba para
Self-Replicating Robots (210) quedó implementada en `rules_engine.py`:
- Campo nuevo `PlayerState.reserved_cards`: `{reserved_card_id:
  {"resources": int, "holder_card_id": str}}` -- distinto de `active_cards`
  porque la carta reservada todavía no está jugada (no tags_played, no
  played_cards, no dispara sus propios pasivos/acción). Columna nueva
  `players.reserved_cards` (migración idempotente en `schema.sql`).
- `reserve_card_in_slot` / `duplicate_reserved_card_resources`: sacan una
  carta de la mano con 2 recursos encima, o duplican los de una ya
  reservada. Cableadas como nuevo vocabulario de `gains` en
  `use_card_action` (`reserve_card_from_hand`, `duplicate_reserved_card`,
  parámetro nuevo `reserved_card_id`) -- el chequeo del tag exigido
  (`requires_tag_any`, ej. space/building) vive en `tools.use_card_action`
  porque el motor puro no conoce el catálogo de cartas.
- `compute_reserved_card_discount` / `release_reserved_card`: `tools.play_card`
  ahora acepta jugar una carta que esté en `reserved_cards` en vez de en
  `hand` -- el costo se descuenta en los recursos acumulados sobre ella
  (sumado al resto de descuentos existentes) y la reserva se libera al
  jugarla en vez de sacarla de la mano.

Tests: `test_reserve_card_in_slot_moves_from_hand_and_stacks_resources`,
`test_duplicate_reserved_card_resources`, `test_release_reserved_card`,
`test_self_replicating_robots_action_reserve_or_duplicate_via_use_card_action`
en `test_rules_engine.py`. La carta todavía no está cargada en
`seed_cards.sql` (falta releer el scan real y confirmar costo/tags/número
de tags de ciencia exactos) — queda disponible para el próximo bloque de
revisión de cartas, ya sin bloqueo de mecánica.

**Resuelto (2026-09-01):** la pieza "mover/agregar un recurso a una carta específica elegida
por el jugador, distinta de la que se está jugando/usando" (identificada primero en Local Heat
Trapping) quedó implementada en dos partes de `rules_engine.py`:
- `apply_card_effect(..., target_card_id=...)`: nuevo vocabulario `target_card_resource_delta`
  (agrega N recursos a otra carta activa) para el efecto INMEDIATO al jugar una carta — cubre
  Local Heat Trapping, Imported Hydrogen y Eos Chasma National Park.
- `use_card_action(..., target_card_id=...)`: nuevo `gains.move_from_target_card_resource_delta`
  (resta N de la carta origen elegida y suma N a la propia) para acciones repetibles que MUEVEN
  recurso en vez de solo agregarlo — cubre Predators y Ants.

Tests: `test_apply_card_effect_target_card_resource_delta`,
`test_apply_card_effect_choice_threads_target_card_id`,
`test_predators_moves_animal_from_another_active_card` en `test_rules_engine.py`. Las 5 cartas
todavía no están cargadas en `seed_cards.sql` (falta releer sus scans reales y confirmar
números/tags exactos) — quedan disponibles para el próximo bloque de revisión de cartas, ya sin
bloqueo de mecánica. Viral Enhancers sigue pendiente por una pieza distinta (ver arriba).


**Nota sobre mapa hexagonal (resuelto 2026-08-31):** Mining Area, Mining Rights y Land Claim
fueron las primeras cartas del catálogo que genuinamente necesitaban modelar el tablero —
decisión de alcance confirmada por el usuario (ver sección 6 de CLAUDE.md). Investigación
verificada, `backend/app/agent/board.py` + `test_board.py`, y el cableado completo a
`tools.py` (incluida `place_special_tile` genérica) están documentados en
`HEX_MAP_RESEARCH.md`. Las 3 cartas ya están cargadas — ver tabla de arriba.

Cartas ya cargadas que ahora SÍ colocan tile real en el mapa (antes solo tocaban el contador
global): `comet` (1 océano), `lake_marineris` (2 océanos), `water_import_from_europa` (1
océano vía su acción). El resto de las cartas con `place_oceans`/`place_city_tiles` en su
efecto (`capital`, `domed_crater`, `noctis_city`, `cupola_city`, `underground_city`,
`phobos_space_haven`, `research_outpost`) también quedaron cableadas automáticamente por el
mismo mecanismo (diff del contador global antes/después de `apply_card_effect` decide cuántos
`ocean_hex_ids`/`city_hex_ids` exigir) — no hizo falta tocarlas una por una.

## Fuera de alcance por diseño (no por mecánica faltante — ver CLAUDE.md sección 6)

Estas SÍ implican un jugador humano o IA adicional, o el mapa hexagonal con adyacencia —
ambos excluidos explícitamente del MVP. Se reevalúan si el alcance del proyecto cambia.

| # scan | Nombre | Motivo |
|---|---|---|
| 038 | Rover Construction | Bonus disparado por colocación de tile de ciudad de **cualquier jugador** — depende de multi-jugador + tiles. |
| 147 | Herbivores | Puede decrementar la producción de otro jugador — depende de multi-jugador. |
| C02 | Air Raid (Colonies) | Evento cuyo ÚNICO efecto es "steal 5 M€ from any player" (robo obligatorio, no "hasta N" opcional como la regla de diseño de abajo) — a diferencia de Comet/Asteroid (donde el robo es una cláusula secundaria opcional sobre un efecto garantizado), acá TODO el efecto depende de un oponente. En single-player, jugarla costaría el recurso (perder 1 floater) sin ningún beneficio — no tiene sentido cargarla como una carta "vacía" a propósito. |

## Regla de diseño: "remove up to N &lt;recurso&gt; from any player"

Varias cartas (Comet, Asteroid, Big Asteroid, y probablemente más en el catálogo completo)
tienen una cláusula secundaria del tipo "remove up to N plants from any player". Es **opcional**
(0 a N) y sirve para hostigar a un oponente. Como el MVP es de un solo jugador, elegir 0 siempre
es una jugada legal — así que **se omite esta cláusula por completo** y se implementa el resto
del efecto (garantizado) de la carta normalmente. No es necesario targeting ni modelo
multi-jugador para estas cartas. Antes de descartar una carta por "targetea a otro jugador",
revisar si la cláusula es de este tipo opcional — si lo es, no bloquea nada.

## Vocabulario de `effects` soportado hoy en `rules_engine.apply_card_effect`

- `mc_production_delta` / `mc_delta`: formas antiguas (solo MC), mantenidas por compatibilidad.
- `production_deltas`: `{"<recurso>_production": delta, ...}` — forma genérica para cambiar
  una o más producciones a la vez (ej. Nuclear Power).
- `resource_deltas`: `{"<recurso>": delta, ...}` — forma genérica para cambiar stock de uno
  o más recursos (ej. Solar Wind Power).
- `convert_production`: `{"from": "<recurso>_production", "to": "<recurso>_production"}`,
  convierte `effect_amount` (X, provisto por el jugador) pasos de un recurso a otro.
- `raise_temperature_steps` / `raise_oxygen_steps`: N pasos, otorgan N de TR (ej. Comet).
- `place_oceans`: N — coloca N tiles de océano (+N TR) (ej. Comet).
- `place_city_tiles`: N — suma N al contador global `city_tiles_placed`, sin TR (ej. Capital).
- `tr_delta`: N — sube el TR directo, sin pasar por parámetro global (ej. Release of Inert Gases: +2).
- `draw_cards`: N — roba N cartas del mazo directo a la mano, sin fase de investigación (ej.
  Research: +2 cartas). Reusa `draw_cards_to_hand` (mismo mecanismo que `use_card_action.gains.draw_cards`,
  pero como efecto inmediato al jugar la carta).
- `resource_delta_per_counter`: `{"resource": "<recurso>", "counter": "<contador de
  GlobalParameters>", "per_counter": N (default 1)}` — suma al stock del recurso tanto como
  valga ese contador global (ej. Greenhouses: +1 planta por cada ciudad en
  `city_tiles_placed`; Media Archives: +1 MC por cada evento en `events_played`). Análogo a
  `mc_per_counter` de `use_card_action.gains`, pero como efecto inmediato y para cualquier
  recurso, no solo MC.
- `production_delta_per_counter`: `{"production": "<recurso>_production", "counter": "<contador>",
  "per_counter": N (default 1)}` — suma a la producción del recurso tanto como valga ese
  contador global (ej. Zeppelins: +1 producción de MC por cada ciudad en `city_tiles_placed`).
- `start_research`: `{"n": N}` — roba N cartas a `pending_research` como efecto inmediato al
  jugar la carta (ej. Business Contacts: n=4, después se resuelve con
  `resolve_research_phase(cost_per_card=0, max_take=2)` porque el texto exige tomar
  EXACTAMENTE 2 de las 4 — `max_take` es un tope nuevo en `resolve_research_phase`, lanza
  error si se pide más). Mismo mecanismo que `use_card_action.gains.start_research`
  (Inventors' Guild), pero disparado al jugar la carta en vez de por una acción repetible.
- `production_delta_per_tag`: `{"tag": "<tag>", "production": "<recurso>_production",
  "per_step": N, "tags_per_step": M, "include_this": bool}` — soporta escalado por cada M tags
  (ej. Worms: +1 producción de plantas por cada 2 tags de microbe, incluido este -> `tags_per_step: 2, include_this: true`)
  o N por cada tag previo (Miranda Resort).
- `duplicate_production`: `{"requires_tag": "<tag>"}` — a diferencia de todos los efectos de
  arriba (que solo miran el estado del jugador/tablero), este targetea OTRA carta que el
  jugador ya jugó, por catálogo, no por recursos guardados en ella (ej. Robotic Workforce:
  duplica la `production_deltas` de una carta con tag `building` ya jugada). Requiere
  `player.played_cards` (historial permanente de card_ids jugados, ver más abajo) y el
  parámetro `duplicate_production_target_card_id` en `tools.play_card`, que resuelve el
  catálogo (`cards` table) para leer los tags y `effects.production_deltas` de la carta
  objetivo — `apply_card_effect` en sí no conoce el catálogo, solo recibe el
  `production_deltas` ya resuelto.

## Colocaciones "inversas" en el tablero (`board.py`)

Algunas cartas piden exactamente lo opuesto de la regla normal de colocación. En vez de
generalizar prematuramente, se agregó una función pareja por cada caso encontrado —
`tools.play_card` decide cuál usar leyendo un marcador explícito en `effects` (ignorado por
`apply_card_effect`, que sigue sin saber nada del tablero):

- `ocean_placement_bypasses_reservation: true` (en el mismo `effects` que `place_oceans`) —
  usa `board.place_ocean_tile_on_land`/`can_place_ocean_on_land` en vez de los normales: coloca
  el océano en un hex de tierra NO reservado para océano (ej. Artificial Lake), justo lo
  inverso de la regla estándar.
- `city_placement_requires_adjacent_cities: N` (junto a `place_city_tiles`) — usa
  `board.place_city_tile_adjacent_to_cities`/`can_place_city_adjacent_to_cities`: EXIGE que el
  hex elegido sea adyacente a al menos N ciudades ya existentes (ej. Urbanized Area: 2), en vez
  de rechazar toda adyacencia a ciudad como la regla normal.
- `place_special_tile.require_adjacency_to_city: true` — variante de `place_special_tile` que
  exige adyacencia a un tile de ciudad de CUALQUIER dueño (ej. Industrial Center), distinta de
  `require_adjacency_to_own_tile` (que exige un tile propio de cualquier tipo).
- `place_special_tile.require_adjacency_to_greenery: true` y `place_special_tile.require_player_has_greenery: true`
  — variante que exige poseer al menos 1 greenery en el tablero y colocar la special tile adyacente a
  una greenery de cualquier dueño (ej. Ecological Zone).

## Historial de cartas jugadas (`PlayerState.played_cards`)

Lista de `card_id` en el orden en que se jugaron, sin sacar nunca ninguno (a diferencia de
`hand`). Se llena con `register_played_card`, llamado UNA vez por cada carta jugada
exitosamente en `tools.play_card` (todas, no solo las que tienen acción/pasivo). Hoy solo lo
usa `duplicate_production` (Robotic Workforce), pero cualquier carta futura que targetee "una
de tus cartas jugadas" por catálogo puede reusarlo.
- `choice`: lista de sub-effects (cualquiera de los de arriba); el jugador elige uno vía
  `effect_choice` (índice 0-based) (ej. Artificial Photosynthesis).
- `tag_count_choice`: `{"tag": "<tag>", "count": N, "if_met": <sub-effect>, "else":
  <sub-effect>}` — a diferencia de `choice`, esta rama NO la elige el jugador: se resuelve
  sola comparando `tags_played` contra `count` (ej. Nitrogen-Rich Asteroid: +4 producción de
  plantas si ya jugó 3 tags de planta, si no +1). Se lee ANTES de sumar los tags de la propia
  carta (`tools.play_card` llama `apply_card_effect` antes de `increment_tags_played`).
- `production_delta_per_tag`: `{"tag": "<tag>", "production": "<recurso>_production",
  "per_tag": N (default 1)}` — a diferencia de `tag_count_choice` (umbral binario), escala
  linealmente: suma N por cada tag ya jugado (ej. Miranda Resort: +1 producción de MC por cada
  tag earth jugado, sin mínimo).
- `place_special_tile`: `{"hex_bonus_resource": ["steel","titanium"], "require_adjacency_to_own_tile":
  bool (opcional)}` — a diferencia de `place_oceans`/`place_city_tiles` (que solo tocan un
  contador global), esta coloca una special tile de verdad en el mapa Tharsis
  (`board.place_special_tile`) y requiere `special_tile_hex_id` en `tools.play_card`. El bonus
  impreso del hex elegido (debe matchear `hex_bonus_resource`) se convierte en +1 producción
  PERMANENTE de ese recurso, no en stock de una sola vez (ej. Mining Rights: +1 producción de
  steel si el hex tenía bonus de steel). Ver `HEX_MAP_RESEARCH.md` para el detalle del tablero.

**Nota sobre "decrease any plant production 1 step" (sin "up to", ej. Fish, Small Animals):**
a diferencia de la cláusula opcional "remove up to N ... from any player" (sección de más
abajo), esta es obligatoria pero también targetea "cualquier jugador" — en el MVP de un solo
jugador no hay otro objetivo posible, así que se aplica al propio jugador con
`production_deltas` normal. No confundir con Virus (050), donde el ÚNICO efecto de la carta
es la cláusula opcional "remove up to" — ahí sí se omite entera y la carta queda con
`effects: {}` (se paga, pero no cambia nada más del estado; ver CARDS_LOG más abajo).

**Nota de firma:** `apply_card_effect(player, globals_, effects, effect_amount=None,
effect_choice=None)` recibe y devuelve SIEMPRE una tupla `(PlayerState, GlobalParameters)`,
incluso para cartas que no tocan el tablero global (necesario porque algunas cartas sí lo
hacen directamente, no solo via proyectos estándar).

Un `resource_deltas` negativo que dejaría el stock por debajo de 0 lanza
`InsufficientResourcesError` — se trata como costo obligatorio de la carta, no como tope
silencioso (ej. Nitrophilic Moss: "pierde 2 plantas" falla si el jugador tiene menos de 2).

Para cartas nuevas preferí `production_deltas`/`resource_deltas` sobre las formas antiguas
(son más generales). Si el efecto no encaja en este vocabulario, hay que extenderlo (con su
test) antes de agregar la carta a `seed_cards.sql`.

## Cartas activas: acción repetible + recursos propios (`rules_engine.use_card_action`)

Algunas cartas quedan "en juego" después de pagarlas porque tienen una acción que se puede
usar una vez por generación (ej. Ironworks) y/o guardan sus propios recursos (ej. microbios
de Regolith Eaters). Se activan con `effects.becomes_active: true` en `cards`, y su acción
vive en `effects.action`:

- `cost`: `{"<recurso>": N, ...}` gastado del stock del jugador. La clave especial
  `"card_resource"` gasta N recursos guardados en la propia carta.
- `gains`: `resource_deltas`, `production_deltas` (igual que en `apply_card_effect`),
  `raise_oxygen_steps` / `raise_temperature_steps` / `place_oceans` (suben el parámetro
  global y dan TR), `card_resource_delta` (agrega recursos a la propia carta),
  `target_card_resource_delta`: N (agrega N recursos a OTRA carta activa elegida por el
  jugador vía `target_card_id` — ej. Symbiotic Fungus: +1 microbio; Extreme-Cold Fungus: +2 microbios),
  `tr_delta` (sube el TR directo, sin pasar por un parámetro global — ej. Equatorial Magnetizer), y
  `mc_per_counter`: `"<contador>"` (da tanto MC como valga ese contador global — ej. Martian
  Rails: MC por cada ciudad en `city_tiles_placed`).
- `choice`: lista de sub-specs alternativos, elegidos con `effect_choice` (igual patrón que
  en `apply_card_effect` — ej. Extreme-Cold Fungus: +1 planta O +2 microbios a otra carta).

El tool `use_card_action(player_id, card_id, effect_choice, target_card_id)` la ejecuta. `action_used` se
resetea a `False` en cada `run_production_phase` (una acción por carta por generación, regla
oficial). `player.active_cards` (jsonb en Supabase) guarda `{card_id: {resources, action_used}}`.

## Requisitos de cartas (columna `requirements`, validados en `check_card_requirements`)

- `min_temperature` / `max_temperature`: en grados C (ej. Farming: min 4; Arctic Algae: max -12).
- `min_oxygen` / `max_oxygen`: en % (ej. Methane from Titan: min 2; Domed Crater: max 7).
- `min_oceans`: cantidad mínima de tiles de océano colocados (ej. Nitrophilic Moss: 3).
- `min_tag_count`: `{"tag": "<tag>", "count": N}` o lista de dicts `[{"tag": "plant", "count": 1}, ...]`
  (ej. Mass Converter: 5 tags science; Advanced Ecosystems: 1 plant, 1 microbe y 1 animal).
- `min_production`: `{"key": "<recurso>_production", "count": N}` — requiere que el jugador ya
  tenga esa producción propia en al menos N (ej. Great Escarpment Consortium: requiere
  producción de steel ≥1). Requiere pasar `player`.
- `max_oceans`: cantidad máxima de océanos colocados (ej. Dust Seals: máximo 3) — contraparte
  de `min_oceans`.

`tools.play_card` valida el requisito contra `global_parameters` antes de cobrar la carta —
si no se cumple, lanza `CardRequirementNotMetError` y no se paga nada.

## Contador global de ciudades (`GlobalParameters.city_tiles_placed`)

Igual que `oceans_placed`, cuenta tiles de ciudad colocados por **cualquier** jugador (no se
trackea de quién es cada uno — no hay mapa hexagonal, ver CLAUDE.md sección 6). Se incrementa
en `standard_project_city` y en cartas con `place_city_tiles` en `effects`. Suficiente para
cartas que pagan "por cada ciudad en Marte" (ej. Martian Rails) sin necesitar el tablero
completo con adyacencia.

## Tags jugados (`PlayerState.tags_played`)

Contador `{"<tag>": int}` que suma 1 por cada tag de cada carta pagada exitosamente (via
`tools.play_card` → `rules_engine.increment_tags_played`), nunca se resetea entre
generaciones. Alimenta el requisito `min_tag_count` en `check_card_requirements` (ej. Mass
Converter: 5 tags de ciencia; Advanced Ecosystems: 1 plant, 1 microbe, 1 animal). `check_card_requirements` acepta un tercer argumento
opcional `player` -- requerido solo si la carta usa `min_tag_count`.

## Efectos pasivos permanentes (`PlayerState.passive_effects`, `rules_engine.register_passive_effect`)

Cartas que, al jugarse, modifican reglas futuras para siempre (no son una acción repetible
como `active_cards` -- no hay "usarla", simplemente están activas). Se registran con
`effects.passive` en `cards` (distinto de `effects.action`, que sí se usa explícitamente vía
`use_card_action`). Vocabulario de `passive`:

- `steel_value_bonus` / `titanium_value_bonus`: MC extra por unidad al pagar OTRAS cartas
  con acero/titanio (ej. Advanced Alloys: +1 cada uno). Sumado en
  `compute_conversion_rates(player)`, que `tools.play_card` usa para parametrizar
  `calculate_card_payment` (antes hardcodeaba las constantes oficiales).
- `on_event_played`: `{"mc_delta": N, "heat_delta": N}` -- se suma al jugador cada vez que
  juega una carta con `cards.is_event = true` (ej. Media Group: +3 MC). Aplicado por
  `apply_event_played_bonuses`, llamado desde `tools.play_card` solo si la carta recién
  jugada es un evento.
- `card_cost_discount_mc`: N -- descuenta N MC del costo de OTRAS cartas antes de cobrarlas
  (ej. Mass Converter: -2 MC en cartas espaciales). Sumado en `compute_card_cost_discount`.
- `tag_filter`: `"<tag>"` opcional en `on_event_played` o junto a `card_cost_discount_mc` --
  limita el bonus/descuento a cartas que tengan ese tag (ej. Optimal Aerobraking: solo
  eventos con tag `space`; Mass Converter: solo cartas con tag `space`).
- `on_tag_played_add_resource`: `{"matching_tags": ["<tag>", ...], "resource_delta": N}` --
  suma N recurso(s) a la propia carta activa cada vez que el jugador juega una carta con alguno de esos tags
  (ej. Ecological Zone: tags `animal`/`plant`; Decomposers: tags `animal`/`plant`/`microbe`).
- `on_tag_played_may_swap_card`: `{"tag": "<tag>"}` -- a diferencia de `on_event_played`
  (automático, dispara solo con cartas `is_event`), este dispara con CUALQUIER carta que
  tenga ese tag (incluida la que registra el pasivo), y es una ELECCIÓN del jugador, no
  automático: puede descartar 1 carta de su mano para robar 1 del mazo (ej. Mars University:
  tag `science`). `tools.play_card` expone el parámetro opcional `discard_for_draw_card_id`;
  `rules_engine.player_has_tag_swap_passive`/`swap_card_for_draw` implementan la lógica.

`cards.is_event` (boolean, default false) marca las cartas "Event" del juego real (se
juegan una vez, no quedan con producción propia) -- necesario para saber cuándo disparar
`on_event_played`. Cargado a mano por carta, verificado contra el scan (ninguna carta
cargada hasta ahora tiene ambigüedad visible en el estilo del banner).

## Sistema de mazo / mano (`PlayerState.deck` / `.hand` / `.pending_research`)

Cada jugador tiene su propio mazo personal (barajado a partir de TODO el catálogo disponible
en `cards`, sin compartir con otros jugadores — coherente con el MVP single-player) y su
propia mano. **`play_card` ahora exige que la carta esté en `hand`** — antes se podía jugar
cualquier `card_id` del catálogo sin poseerlo, eso ya no es legal.

- `deal_starting_hand(player_id, hand_size=10)`: arma el mazo (barajado) y reparte la mano
  inicial gratis (regla oficial: 10 cartas). Se llama una sola vez por jugador, al arrancar.
- `start_research_phase(player_id, n=4)` / `resolve_research_phase(player_id,
  card_ids_to_buy, cost_per_card=3)`: la fase de investigación de cada generación, en dos
  pasos porque el usuario tiene que ver las cartas robadas antes de decidir. Las no
  compradas se descartan (no vuelven al mazo). No se puede iniciar una fase nueva mientras
  haya una pendiente sin resolver.
- Vocabulario nuevo en `use_card_action.gains`: `draw_cards: N` (roba N directo a la mano,
  ej. Development Center) y `start_research: {"n": N}` (roba N a `pending_research`, el
  jugador resuelve después por separado — ej. Inventors' Guild, con `resolve_research_phase`
  a `cost_per_card=0` porque su acción es gratis).

Esto desbloqueó **Inventors' Guild** y **Development Center**, que antes estaban pendientes
por "sistema de mazo/mano".

## Fuente de verificación

Scans oficiales vía https://tm.hadronikle.com (base de datos no oficial de cartas,
668 escaneos full-res). Cada carta se lee directamente del scan antes de cargarla —
nunca de memoria — para no romper el objetivo de "100% de precisión" del PRD.
