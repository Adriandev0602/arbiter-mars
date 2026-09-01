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

## Pendientes (requieren una pieza de mecánica que todavía no se agregó)

Estas NO son descartes definitivos — son casos donde ya se identificó qué falta agregar al
motor para desbloquearlas. Se resuelven agregando esa pieza, no evitando la carta.

| # scan | Nombre | Qué falta |
|---|---|---|
| 074 | Viral Enhancers | Pasivo que dispara con CUALQUIER carta de tag plant/microbe/animal jugada (no solo eventos, no automático como `on_event_played`) y le da al jugador una elección EN ESE MOMENTO: +1 planta O agregar 1 recurso a una carta específica ya en juego. Es distinto de `target_card_resource_delta`/`move_from_target_card_resource_delta` (resuelto abajo) porque esos dos son para un efecto inmediato al jugar la carta o una acción repetible — acá el trigger es el evento "se jugó una carta con tag X" y todavía falta la pieza de pasivo-con-elección-del-jugador-al-dispararse (los pasivos actuales, `on_tag_played_add_resource`, son automáticos sin elección). |
| 140 | Lava Flows | Sube temperatura 2 pasos (trivial) pero además coloca su tile en UNO de 4 hexágonos volcánicos nombrados específicamente (Tharsis Tholus, Ascraeus Mons, Pavonis Mons, Arsia Mons) — el mapa (`board.py`) todavía no asigna nombre individual a esos 4 hexágonos ni tiene un requirement tipo "uno de esta lista de hex_ids" en `can_place_special_tile` (hoy solo filtra por `hex_type`/bonus/adyacencia genérica, ver nota "Nombrar los 4 hexágonos volcánicos" en `HEX_MAP_RESEARCH.md`). Implementar esa pieza requeriría verificar contra la fuente qué hex_id corresponde a cada volcán — no reverificado todavía, no arriesgar la precisión cargando algo mal identificado. |

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
