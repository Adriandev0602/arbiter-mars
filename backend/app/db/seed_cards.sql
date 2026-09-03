-- Seed de cartas del catalogo, verificadas a mano contra el scan oficial de
-- cada carta (fuente: base de datos de cartas de tm.hadronikle.com, cotejada
-- carta por carta -- ver CLAUDE.md, seccion "Catalogo de cartas").
--
-- Se eligieron primero cartas de efecto INMEDIATO sobre produccion/stock de
-- MC, sin colocacion de tiles, adyacencia, ni interaccion con otras cartas
-- (todo eso esta fuera del alcance del MVP, ver CLAUDE.md seccion 6). El
-- vocabulario de `effects` que consumen esta implementado en
-- rules_engine.apply_card_effect y probado en test_rules_engine.py.
--
-- Correr despues de schema.sql.

insert into cards (id, name, cost, tags, requirements, effects) values
    (
        'sponsors', 'Sponsors', 6, '{}', null,
        '{"mc_production_delta": 2}'::jsonb
    ),
    (
        'acquired_company', 'Acquired Company', 10, '{}', null,
        '{"mc_production_delta": 3}'::jsonb
    ),
    (
        'investment_loan', 'Investment Loan', 3, '{}', null,
        '{"mc_production_delta": -1, "mc_delta": 10}'::jsonb
    ),
    (
        'insulation', 'Insulation', 2, '{}', null,
        '{"convert_production": {"from": "heat_production", "to": "mc_production"}}'::jsonb
    ),
    (
        'nuclear_power', 'Nuclear Power', 10, '{power,building}', null,
        '{"production_deltas": {"mc_production": -2, "energy_production": 3}}'::jsonb
    ),
    (
        'solar_power', 'Solar Power', 11, '{power,building}', null,
        '{"production_deltas": {"energy_production": 1}}'::jsonb
    ),
    (
        'titanium_mine', 'Titanium Mine', 7, '{space}', null,
        '{"production_deltas": {"titanium_production": 1}}'::jsonb
    ),
    (
        'solar_wind_power', 'Solar Wind Power', 11, '{science,power}', null,
        '{"production_deltas": {"energy_production": 1}, "resource_deltas": {"titanium": 2}}'::jsonb
    ),
    (
        'artificial_photosynthesis', 'Artificial Photosynthesis', 12, '{science}', null,
        '{"choice": [{"production_deltas": {"plant_production": 1}}, {"production_deltas": {"energy_production": 2}}]}'::jsonb
    ),
    (
        'mine', 'Mine', 4, '{building}', null,
        '{"production_deltas": {"steel_production": 1}}'::jsonb
    ),
    (
        'farming', 'Farming', 16, '{plant}', '{"min_temperature": 4}'::jsonb,
        '{"resource_deltas": {"plants": 2}, "production_deltas": {"mc_production": 2, "plant_production": 2}}'::jsonb
    ),
    (
        'nitrophilic_moss', 'Nitrophilic Moss', 8, '{plant}', '{"min_oceans": 3}'::jsonb,
        '{"resource_deltas": {"plants": -2}, "production_deltas": {"plant_production": 2}}'::jsonb
    ),
    (
        'ironworks', 'Ironworks', 11, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 1}, "raise_oxygen_steps": 1}}}'::jsonb
    ),
    (
        'steelworks', 'Steelworks', 15, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 4}, "gains": {"resource_deltas": {"steel": 2}, "raise_oxygen_steps": 1}}}'::jsonb
    ),
    (
        'regolith_eaters', 'Regolith Eaters', 13, '{science,microbe}', null,
        '{"becomes_active": true, "action": {"choice": [{"cost": {}, "gains": {"card_resource_delta": 1}}, {"cost": {"card_resource": 2}, "gains": {"raise_oxygen_steps": 1}}]}}'::jsonb
    ),
    (
        'comet', 'Comet', 21, '{space}', null,
        '{"raise_temperature_steps": 1, "place_oceans": 1}'::jsonb
    ),
    (
        'asteroid_card', 'Asteroid', 14, '{space}', null,
        '{"raise_temperature_steps": 1, "resource_deltas": {"titanium": 2}}'::jsonb
    ),
    (
        'big_asteroid', 'Big Asteroid', 27, '{space}', null,
        '{"raise_temperature_steps": 2, "resource_deltas": {"titanium": 4}}'::jsonb
    ),
    (
        'capital', 'Capital', 26, '{building}', '{"min_oceans": 4}'::jsonb,
        '{"production_deltas": {"energy_production": -2, "mc_production": 5}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'martian_rails', 'Martian Rails', 13, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 1}, "gains": {"mc_per_counter": "city_tiles_placed"}}}'::jsonb
    ),
    (
        'space_elevator', 'Space Elevator', 27, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"steel": 1}, "gains": {"resource_deltas": {"mc": 5}}}, "production_deltas": {"titanium_production": 1}}'::jsonb
    ),
    (
        'equatorial_magnetizer', 'Equatorial Magnetizer', 11, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy_production": 1}, "gains": {"tr_delta": 1}}}'::jsonb
    ),
    (
        'water_import_from_europa', 'Water Import from Europa', 25, '{jovian}', null,
        '{"becomes_active": true, "action": {"cost": {"mc": 12}, "gains": {"place_oceans": 1}}}'::jsonb
    ),
    (
        'advanced_alloys', 'Advanced Alloys', 9, '{science}', null,
        '{"passive": {"steel_value_bonus": 1, "titanium_value_bonus": 1}}'::jsonb
    ),
    (
        'media_group', 'Media Group', 6, '{}', null,
        '{"passive": {"on_event_played": {"mc_delta": 3}}}'::jsonb
    ),
    (
        'optimal_aerobraking', 'Optimal Aerobraking', 7, '{}', null,
        '{"passive": {"tag_filter": "space", "on_event_played": {"mc_delta": 3, "heat_delta": 3}}}'::jsonb
    ),
    (
        'mass_converter', 'Mass Converter', 8, '{science}', '{"min_tag_count": {"tag": "science", "count": 5}}'::jsonb,
        '{"passive": {"tag_filter": "space", "card_cost_discount_mc": 2}, "becomes_active": true, "action": {"cost": {"energy": 6}, "gains": {"production_deltas": {"energy_production": 6}}}}'::jsonb
    ),
    (
        'inventors_guild', 'Inventors'' Guild', 9, '{science}', null,
        '{"becomes_active": true, "action": {"cost": {}, "gains": {"start_research": {"n": 1}}}}'::jsonb
    ),
    (
        'development_center', 'Development Center', 11, '{science,building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 1}, "gains": {"draw_cards": 1}}}'::jsonb
    ),
    (
        'domed_crater', 'Domed Crater', 24, '{building}', '{"max_oxygen": 7}'::jsonb,
        '{"resource_deltas": {"plants": 3}, "production_deltas": {"energy_production": -1, "mc_production": 3}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'noctis_city', 'Noctis City', 18, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "mc_production": 3}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'methane_from_titan', 'Methane from Titan', 28, '{jovian,power}', '{"min_oxygen": 2}'::jsonb,
        '{"production_deltas": {"heat_production": 2, "plant_production": 2}}'::jsonb
    ),
    (
        'research_outpost', 'Research Outpost', 18, '{science,building}', null,
        '{"passive": {"card_cost_discount_mc": 1}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'phobos_space_haven', 'Phobos Space Haven', 25, '{space}', null,
        '{"production_deltas": {"titanium_production": 1}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'black_polar_dust', 'Black Polar Dust', 15, '{}', null,
        '{"place_oceans": 1, "production_deltas": {"mc_production": -2, "heat_production": 3}}'::jsonb
    ),
    (
        'arctic_algae', 'Arctic Algae', 12, '{plant}', '{"max_temperature": -12}'::jsonb,
        '{"resource_deltas": {"plants": 1}, "passive": {"on_ocean_placed": {"plants_delta": 2}}}'::jsonb
    ),
    (
        'space_station', 'Space Station', 10, '{power}', null,
        '{"passive": {"tag_filter": "space", "card_cost_discount_mc": 2}}'::jsonb
    ),
    (
        'interstellar_colony_ship', 'Interstellar Colony Ship', 24, '{science,earth}',
        '{"min_tag_count": {"tag": "science", "count": 5}}'::jsonb,
        '{}'::jsonb
    ),
    (
        'security_fleet', 'Security Fleet', 12, '{power}', null,
        '{"becomes_active": true, "action": {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'cupola_city', 'Cupola City', 16, '{building}', '{"max_oxygen": 9}'::jsonb,
        '{"production_deltas": {"energy_production": -1, "mc_production": 3}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'lunar_beam', 'Lunar Beam', 13, '{earth,power}', null,
        '{"production_deltas": {"mc_production": -2, "heat_production": 2, "energy_production": 2}}'::jsonb
    ),
    (
        'underground_city', 'Underground City', 18, '{building}', null,
        '{"production_deltas": {"energy_production": -2, "steel_production": 2}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'ghg_producing_bacteria', 'GHG Producing Bacteria', 8, '{science}', '{"min_oxygen": 4}'::jsonb,
        '{"becomes_active": true, "action": {"choice": [{"cost": {}, "gains": {"card_resource_delta": 1}}, {"cost": {"card_resource": 2}, "gains": {"raise_temperature_steps": 1}}]}}'::jsonb
    ),
    (
        'release_of_inert_gases', 'Release of Inert Gases', 14, '{}', null,
        '{"tr_delta": 2}'::jsonb
    ),
    (
        'nitrogen_rich_asteroid', 'Nitrogen-Rich Asteroid', 31, '{space}', null,
        '{"tag_count_choice": {"tag": "plant", "count": 3,
            "if_met": {"raise_temperature_steps": 1, "production_deltas": {"plant_production": 4}},
            "else": {"raise_temperature_steps": 1, "production_deltas": {"plant_production": 1}}}}'::jsonb
    ),
    (
        'deimos_down', 'Deimos Down', 31, '{space}', null,
        '{"raise_temperature_steps": 3, "resource_deltas": {"steel": 4}}'::jsonb
    ),
    (
        'asteroid_mining', 'Asteroid Mining', 30, '{jovian}', null,
        '{"production_deltas": {"titanium_production": 2}}'::jsonb
    ),
    (
        'food_factory', 'Food Factory', 12, '{building}', null,
        '{"production_deltas": {"plant_production": -1, "mc_production": 4}}'::jsonb
    ),
    (
        'archaebacteria', 'Archaebacteria', 6, '{microbe}', '{"max_temperature": -18}'::jsonb,
        '{"production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'carbonate_processing', 'Carbonate Processing', 6, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "heat_production": 3}}'::jsonb
    ),
    (
        'natural_preserve', 'Natural Preserve', 9, '{building}', '{"max_oxygen": 4}'::jsonb,
        '{"production_deltas": {"mc_production": 1}}'::jsonb
    ),
    (
        'lightning_harvest', 'Lightning Harvest', 8, '{power}',
        '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"production_deltas": {"energy_production": 1, "mc_production": 1}}'::jsonb
    ),
    (
        'algae', 'Algae', 10, '{plant}', '{"min_oceans": 5}'::jsonb,
        '{"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 2}}'::jsonb
    ),
    (
        'adapted_lichen', 'Adapted Lichen', 9, '{plant}', null,
        '{"production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'tardigrades', 'Tardigrades', 4, '{microbe}', null,
        '{"becomes_active": true, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'virus', 'Virus', 1, '{microbe}', null,
        '{}'::jsonb
    ),
    (
        'miranda_resort', 'Miranda Resort', 12, '{jovian,space}', null,
        '{"production_delta_per_tag": {"tag": "earth", "production": "mc_production"}}'::jsonb
    ),
    (
        'fish', 'Fish', 9, '{animal}', '{"min_temperature": 2}'::jsonb,
        '{"production_deltas": {"plant_production": -1},
          "becomes_active": true, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'lake_marineris', 'Lake Marineris', 18, '{}', '{"min_temperature": 0}'::jsonb,
        '{"place_oceans": 2}'::jsonb
    ),
    (
        'small_animals', 'Small Animals', 6, '{animal}', '{"min_oxygen": 6}'::jsonb,
        '{"production_deltas": {"plant_production": -1},
          "becomes_active": true, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'kelp_farming', 'Kelp Farming', 17, '{plant}', '{"min_oceans": 6}'::jsonb,
        '{"resource_deltas": {"plants": 2}, "production_deltas": {"mc_production": 2, "plant_production": 3}}'::jsonb
    ),
    (
        'vesta_shipyard', 'Vesta Shipyard', 15, '{jovian,space}', null,
        '{"production_deltas": {"titanium_production": 1}}'::jsonb
    ),
    (
        'beam_from_a_thorium_asteroid', 'Beam from a Thorium Asteroid', 32, '{jovian,space,power}',
        '{"min_tag_count": {"tag": "jovian", "count": 1}}'::jsonb,
        '{"production_deltas": {"heat_production": 3, "energy_production": 3}}'::jsonb
    ),
    (
        'mangrove', 'Mangrove', 12, '{plant}', '{"min_temperature": 4}'::jsonb,
        '{"raise_oxygen_steps": 1}'::jsonb
    ),
    (
        'trees', 'Trees', 13, '{plant}', '{"min_temperature": -4}'::jsonb,
        '{"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 3}}'::jsonb
    ),
    (
        'great_escarpment_consortium', 'Great Escarpment Consortium', 6, '{}',
        '{"min_production": {"key": "steel_production", "count": 1}}'::jsonb,
        '{}'::jsonb
    ),
    (
        'mineral_deposit', 'Mineral Deposit', 5, '{}', null,
        '{"resource_deltas": {"steel": 5}}'::jsonb
    ),
    (
        'mining_expedition', 'Mining Expedition', 12, '{}', null,
        '{"raise_oxygen_steps": 1, "resource_deltas": {"plants": -2, "steel": 2}}'::jsonb
    ),
    (
        'building_industries', 'Building Industries', 6, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "steel_production": 2}}'::jsonb
    ),
    (
        'electro_catapult', 'Electro Catapult', 17, '{building}', '{"max_oxygen": 8}'::jsonb,
        '{"production_deltas": {"energy_production": -1}, "becomes_active": true,
          "action": {"choice": [
            {"cost": {"plants": 1}, "gains": {"resource_deltas": {"mc": 7}}},
            {"cost": {"steel": 1}, "gains": {"resource_deltas": {"mc": 7}}}
          ]}}'::jsonb
    ),
    (
        'mining_rights', 'Mining Rights', 9, '{building}', null,
        '{"place_special_tile": {"hex_bonus_resource": ["steel", "titanium"]}}'::jsonb
    ),
    (
        'mining_area', 'Mining Area', 4, '{building}', null,
        '{"place_special_tile": {"hex_bonus_resource": ["steel", "titanium"], "require_adjacency_to_own_tile": true}}'::jsonb
    ),
    (
        'land_claim', 'Land Claim', 1, '{}', null,
        '{}'::jsonb
    ),
    (
        'earth_catapult', 'Earth Catapult', 23, '{earth}', null,
        '{"passive": {"card_cost_discount_mc": 2}}'::jsonb
    ),
    (
        'birds', 'Birds', 10, '{animal}', '{"min_oxygen": 13}'::jsonb,
        '{"production_deltas": {"plant_production": -2},
          "becomes_active": true, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'mars_university', 'Mars University', 8, '{science,building}', null,
        '{"passive": {"on_tag_played_may_swap_card": {"tag": "science"}}}'::jsonb
    ),
    (
        'towing_a_comet', 'Towing a Comet', 23, '{space}', null,
        '{"resource_deltas": {"plants": 2}, "raise_oxygen_steps": 1, "place_oceans": 1}'::jsonb
    ),
    (
        'space_mirrors', 'Space Mirrors', 3, '{power,space}', null,
        '{"becomes_active": true, "action": {"cost": {"mc": 7}, "gains": {"production_deltas": {"energy_production": 1}}}}'::jsonb
    ),
    (
        'ice_asteroid', 'Ice Asteroid', 23, '{space}', null,
        '{"place_oceans": 2}'::jsonb
    ),
    (
        'quantum_extractor', 'Quantum Extractor', 13, '{science,power}',
        '{"min_tag_count": {"tag": "science", "count": 4}}'::jsonb,
        '{"production_deltas": {"energy_production": 4}, "passive": {"tag_filter": "space", "card_cost_discount_mc": 2}}'::jsonb
    ),
    (
        'giant_ice_asteroid', 'Giant Ice Asteroid', 36, '{space}', null,
        '{"raise_temperature_steps": 2, "place_oceans": 2}'::jsonb
    ),
    (
        'ganymede_colony', 'Ganymede Colony', 20, '{jovian}', null,
        '{}'::jsonb
    ),
    (
        'callisto_penal_mines', 'Callisto Penal Mines', 24, '{jovian}', null,
        '{"production_deltas": {"mc_production": 3}}'::jsonb
    ),
    (
        'giant_space_mirror', 'Giant Space Mirror', 17, '{power,space}', null,
        '{"production_deltas": {"energy_production": 3}}'::jsonb
    ),
    (
        'trans_neptune_probe', 'Trans-Neptune Probe', 6, '{science,space}', null,
        '{}'::jsonb
    ),
    (
        'commercial_district', 'Commercial District', 16, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "mc_production": 4}}'::jsonb
    ),
    (
        'grass', 'Grass', 11, '{plant}', '{"min_temperature": -16}'::jsonb,
        '{"resource_deltas": {"plants": 3}, "production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'heather', 'Heather', 6, '{plant}', '{"min_temperature": -14}'::jsonb,
        '{"resource_deltas": {"plants": 1}, "production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'peroxide_power', 'Peroxide Power', 7, '{power,building}', null,
        '{"production_deltas": {"mc_production": -1, "energy_production": 2}}'::jsonb
    ),
    (
        'research', 'Research', 11, '{science,science}', null,
        '{"draw_cards": 2}'::jsonb
    ),
    (
        'robotic_workforce', 'Robotic Workforce', 9, '{science}', null,
        '{"duplicate_production": {"requires_tag": "building"}}'::jsonb
    ),
    (
        'gene_repair', 'Gene Repair', 12, '{science,science,science}',
        '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"production_deltas": {"mc_production": 2}}'::jsonb
    ),
    (
        'io_mining_industries', 'IO Mining Industries', 41, '{jovian}', null,
        '{"production_deltas": {"titanium_production": 2, "mc_production": 2}}'::jsonb
    ),
    (
        'bushes', 'Bushes', 10, '{plant}', '{"min_temperature": -10}'::jsonb,
        '{"resource_deltas": {"plants": 2}, "production_deltas": {"plant_production": 2}}'::jsonb
    ),
    (
        'physics_complex', 'Physics Complex', 12, '{science,building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 6}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'greenhouses', 'Greenhouses', 6, '{plant,building}', null,
        '{"resource_delta_per_counter": {"resource": "plants", "counter": "city_tiles_placed"}}'::jsonb
    ),
    (
        'nuclear_zone', 'Nuclear Zone', 10, '{earth}', null,
        '{"raise_temperature_steps": 2}'::jsonb
    ),
    (
        'tropical_resort', 'Tropical Resort', 13, '{building}', null,
        '{"production_deltas": {"heat_production": -2, "mc_production": 3}}'::jsonb
    ),
    (
        'toll_station', 'Toll Station', 12, '{space}', null,
        '{}'::jsonb
    ),
    (
        'fueled_generators', 'Fueled Generators', 1, '{power,building}', null,
        '{"production_deltas": {"mc_production": -1, "energy_production": 1}}'::jsonb
    ),
    (
        'power_grid', 'Power Grid', 18, '{power}', null,
        '{"production_delta_per_tag": {"tag": "power", "production": "energy_production"},
          "production_deltas": {"energy_production": 1}}'::jsonb
    ),
    (
        'ore_processor', 'Ore Processor', 13, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"energy": 4}, "gains": {"resource_deltas": {"titanium": 1}, "raise_oxygen_steps": 1}}}'::jsonb
    ),
    (
        'earth_office', 'Earth Office', 1, '{earth}', null,
        '{"passive": {"card_cost_discount_mc": 3, "tag_filter": "earth"}}'::jsonb
    ),
    (
        'media_archives', 'Media Archives', 8, '{earth}', null,
        '{"resource_delta_per_counter": {"resource": "mc", "counter": "events_played"}}'::jsonb
    ),
    (
        'open_city', 'Open City', 23, '{building}', '{"min_oxygen": 12}'::jsonb,
        '{"production_deltas": {"energy_production": -1, "mc_production": 4},
          "resource_deltas": {"plants": 2}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'business_network', 'Business Network', 4, '{earth}', null,
        '{"production_deltas": {"mc_production": -1}, "becomes_active": true,
          "action": {"cost": {}, "gains": {"start_research": {"n": 1}}}}'::jsonb
    ),
    (
        'business_contacts', 'Business Contacts', 7, '{earth}', null,
        '{"start_research": {"n": 4}}'::jsonb
    ),
    (
        'bribed_committee', 'Bribed Committee', 7, '{earth}', null,
        '{"tr_delta": 2}'::jsonb
    ),
    (
        'breathing_filters', 'Breathing Filters', 11, '{science}', '{"min_oxygen": 7}'::jsonb,
        '{}'::jsonb
    ),
    (
        'artificial_lake', 'Artificial Lake', 15, '{building}', '{"min_temperature": -6}'::jsonb,
        '{"place_oceans": 1, "ocean_placement_bypasses_reservation": true}'::jsonb
    ),
    (
        'geothermal_power', 'Geothermal Power', 11, '{power,building}', null,
        '{"production_deltas": {"energy_production": 2}}'::jsonb
    ),
    (
        'dust_seals', 'Dust Seals', 2, '{}', '{"max_oceans": 3}'::jsonb,
        '{}'::jsonb
    ),
    (
        'urbanized_area', 'Urbanized Area', 10, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "mc_production": 2},
          "place_city_tiles": 1, "city_placement_requires_adjacent_cities": 2}'::jsonb
    ),
    (
        'sabotage', 'Sabotage', 1, '{}', null,
        '{}'::jsonb
    ),
    (
        'moss', 'Moss', 4, '{plant}', '{"min_oceans": 3}'::jsonb,
        '{"resource_deltas": {"plants": -1}, "production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'industrial_center', 'Industrial Center', 4, '{building}', null,
        '{"place_special_tile": {"require_adjacency_to_city": true}, "becomes_active": true,
          "action": {"cost": {"mc": 7}, "gains": {"production_deltas": {"steel_production": 1}}}}'::jsonb
    ),
    (
        'hired_raiders', 'Hired Raiders', 1, '{}', null,
        '{}'::jsonb
    ),
    (
        'hackers', 'Hackers', 3, '{science}', null,
        '{"production_deltas": {"energy_production": -1}}'::jsonb
    ),
    (
        'ghg_factories', 'GHG Factories', 11, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "heat_production": 4}}'::jsonb
    ),
    (
        'subterranean_reservoir', 'Subterranean Reservoir', 11, '{}', null,
        '{"place_oceans": 1}'::jsonb
    ),
    (
        'ecological_zone', 'Ecological Zone', 12, '{animal,plant}', null,
        '{"becomes_active": true, "place_special_tile": {"require_adjacency_to_greenery": true, "require_player_has_greenery": true}, "passive": {"on_tag_played_add_resource": {"matching_tags": ["animal", "plant"], "resource_delta": 1}}}'::jsonb
    ),
    (
        'zeppelins', 'Zeppelins', 13, '{}', '{"min_oxygen": 5}'::jsonb,
        '{"production_delta_per_counter": {"production": "mc_production", "counter": "city_tiles_placed", "per_counter": 1}}'::jsonb
    ),
    (
        'worms', 'Worms', 8, '{microbe}', '{"min_oxygen": 4}'::jsonb,
        '{"production_delta_per_tag": {"tag": "microbe", "production": "plant_production", "tags_per_step": 2, "include_this": true}}'::jsonb
    ),
    (
        'decomposers', 'Decomposers', 5, '{microbe}', '{"min_oxygen": 3}'::jsonb,
        '{"becomes_active": true, "passive": {"on_tag_played_add_resource": {"matching_tags": ["animal", "plant", "microbe"], "resource_delta": 1}}}'::jsonb
    ),
    (
        'fusion_power', 'Fusion Power', 14, '{science,power,building}', '{"min_tag_count": {"tag": "power", "count": 2}}'::jsonb,
        '{"production_deltas": {"energy_production": 3}}'::jsonb
    ),
    (
        'symbiotic_fungus', 'Symbiotic Fungus', 4, '{microbe}', '{"min_temperature": -14}'::jsonb,
        '{"becomes_active": true, "action": {"gains": {"target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'extreme_cold_fungus', 'Extreme-Cold Fungus', 13, '{microbe}', '{"max_temperature": -10}'::jsonb,
        '{"becomes_active": true, "action": {"choice": [{"gains": {"resource_deltas": {"plants": 1}}}, {"gains": {"target_card_resource_delta": 2}}]}}'::jsonb
    ),
    (
        'advanced_ecosystems', 'Advanced Ecosystems', 11, '{plant,microbe,animal}', '{"min_tag_count": [{"tag": "plant", "count": 1}, {"tag": "microbe", "count": 1}, {"tag": "animal", "count": 1}]}'::jsonb,
        '{}'::jsonb
    ),
    (
        'great_dam', 'Great Dam', 12, '{power,building}', '{"min_oceans": 4}'::jsonb,
        '{"production_deltas": {"energy_production": 2}}'::jsonb
    ),
    (
        'local_heat_trapping', 'Local Heat Trapping', 1, '{}', null,
        '{"choice": [{"resource_deltas": {"heat": -5, "plants": 4}}, {"resource_deltas": {"heat": -5}, "target_card_resource_delta": 2}]}'::jsonb
    ),
    (
        'imported_hydrogen', 'Imported Hydrogen', 16, '{earth,space}', null,
        '{"choice": [{"place_oceans": 1, "resource_deltas": {"plants": 3}}, {"place_oceans": 1, "target_card_resource_delta": 3}, {"place_oceans": 1, "target_card_resource_delta": 2}]}'::jsonb
    ),
    (
        'predators', 'Predators', 14, '{animal}', '{"min_oxygen": 11}'::jsonb,
        '{"becomes_active": true, "action": {"gains": {"move_from_target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'eos_chasma_national_park', 'Eos Chasma National Park', 16, '{plant,building}', '{"min_temperature": -12}'::jsonb,
        '{"target_card_resource_delta": 1, "resource_deltas": {"plants": 3}, "production_deltas": {"mc_production": 2}}'::jsonb
    ),
    (
        'ants', 'Ants', 9, '{microbe}', '{"min_oxygen": 4}'::jsonb,
        '{"becomes_active": true, "action": {"gains": {"move_from_target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'cartel', 'Cartel', 8, '{earth}', null,
        '{"production_delta_per_tag": {"tag": "earth", "production": "mc_production", "per_tag": 1, "include_this": true}}'::jsonb
    ),
    (
        'strip_mine', 'Strip Mine', 25, '{building}', null,
        '{"production_deltas": {"energy_production": -2, "steel_production": 2, "titanium_production": 1}, "raise_oxygen_steps": 2}'::jsonb
    ),
    (
        'wave_power', 'Wave Power', 8, '{power}', '{"min_oceans": 3}'::jsonb,
        '{"production_deltas": {"energy_production": 1}}'::jsonb
    ),
    (
        'power_plant_card', 'Power Plant', 4, '{power,building}', null,
        '{"production_deltas": {"energy_production": 1}}'::jsonb
    ),
    (
        'mohole_area', 'Mohole Area', 20, '{building}', null,
        '{"production_deltas": {"heat_production": 4}, "place_special_tile": {"hex_type": "ocean"}}'::jsonb
    ),
    (
        'large_convoy', 'Large Convoy', 36, '{earth,space}', null,
        '{"choice": [{"place_oceans": 1, "draw_cards": 2, "resource_deltas": {"plants": 5}}, {"place_oceans": 1, "draw_cards": 2, "target_card_resource_delta": 4}]}'::jsonb
    ),
    (
        'tectonic_stress_power', 'Tectonic Stress Power', 18, '{science,science,power,building}', '{"min_tag_count": {"tag": "science", "count": 2}}'::jsonb,
        '{"production_deltas": {"energy_production": 3}}'::jsonb
    ),
    (
        'herbivores', 'Herbivores', 12, '{animal}', '{"min_oxygen": 8}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 1, "production_deltas": {"plant_production": -1}, "passive": {"on_greenery_placed_add_resource": {"resource_delta": 1}}}'::jsonb
    ),
    (
        'insects', 'Insects', 9, '{microbe}', '{"min_oxygen": 6}'::jsonb,
        '{"production_delta_per_tag": {"tag": "plant", "production": "plant_production", "per_tag": 1}}'::jsonb
    ),
    (
        'ceos_favorite_project', 'CEO''s Favorite Project', 1, '{}', null,
        '{"target_card_resource_delta": 1, "target_min_resources": 1}'::jsonb
    ),
    (
        'anti_gravity_technology', 'Anti-Gravity Technology', 14, '{science}', '{"min_tag_count": {"tag": "science", "count": 7}}'::jsonb,
        '{"passive": {"card_cost_discount_mc": 2}}'::jsonb
    ),
    (
        'adaptation_technology', 'Adaptation Technology', 12, '{science}', null,
        '{"passive": {"global_requirements_tolerance_steps": 2}}'::jsonb
    ),
    (
        'caretaker_contract', 'Caretaker Contract', 3, '{}', '{"min_temperature": 0}'::jsonb,
        '{"becomes_active": true, "action": {"cost": {"heat": 8}, "gains": {"tr_delta": 1}}}'::jsonb
    ),
    (
        'designed_microorganisms', 'Designed Microorganisms', 16, '{science,microbe}', '{"max_temperature": -14}'::jsonb,
        '{"production_deltas": {"plant_production": 2}}'::jsonb
    ),
    (
        'standard_technology', 'Standard Technology', 6, '{science}', null,
        '{"passive": {"on_standard_project_used": {"mc_delta": 3}}}'::jsonb
    ),
    (
        'nitrite_reducing_bacteria', 'Nitrite Reducing Bacteria', 11, '{microbe}', null,
        '{"becomes_active": true, "active_card_starting_resources": 3, "action": {"choice": [{"gains": {"card_resource_delta": 1}}, {"cost": {"card_resource": 3}, "gains": {"tr_delta": 1}}]}}'::jsonb
    ),
    (
        'industrial_microbes', 'Industrial Microbes', 12, '{microbe,building}', null,
        '{"production_deltas": {"energy_production": 1, "steel_production": 1}}'::jsonb
    ),
    (
        'lichen', 'Lichen', 7, '{plant}', '{"min_temperature": -24}'::jsonb,
        '{"production_deltas": {"plant_production": 1}}'::jsonb
    ),
    (
        'power_supply_consortium', 'Power Supply Consortium', 5, '{power,power}', '{"min_tag_count": {"tag": "power", "count": 2}}'::jsonb,
        '{"production_deltas": {"energy_production": 0}}'::jsonb
    ),
    (
        'convoy_from_europa', 'Convoy from Europa', 15, '{space}', null,
        '{"place_oceans": 1, "draw_cards": 1}'::jsonb
    ),
    (
        'imported_ghg', 'Imported GHG', 7, '{earth,space}', null,
        '{"production_deltas": {"heat_production": 1}, "resource_deltas": {"heat": 3}}'::jsonb
    ),
    (
        'imported_nitrogen', 'Imported Nitrogen', 23, '{earth,space}', null,
        '{"tr_delta": 1, "resource_deltas": {"plants": 4}, "target_card_resource_delta": 3, "target_card_resource_delta_2": 2}'::jsonb
    ),
    (
        'micro_mills', 'Micro-Mills', 3, '{}', null,
        '{"production_deltas": {"heat_production": 1}}'::jsonb
    ),
    (
        'magnetic_field_generators', 'Magnetic Field Generators', 20, '{building}', null,
        '{"production_deltas": {"energy_production": -4, "plant_production": 2}, "tr_delta": 3}'::jsonb
    ),
    (
        'shuttles', 'Shuttles', 10, '{space}', '{"min_oxygen": 5}'::jsonb,
        '{"production_deltas": {"energy_production": -1, "mc_production": 2}, "passive": {"card_cost_discount_mc": 2, "tag_filter": "space"}}'::jsonb
    ),
    (
        'import_of_advanced_ghg', 'Import of Advanced GHG', 9, '{earth,space}', null,
        '{"production_deltas": {"heat_production": 2}}'::jsonb
    ),
    (
        'windmills', 'Windmills', 6, '{power,building}', '{"min_oxygen": 7}'::jsonb,
        '{"production_deltas": {"energy_production": 1}}'::jsonb
    ),
    (
        'tundra_farming', 'Tundra Farming', 16, '{plant}', '{"min_temperature": -6}'::jsonb,
        '{"production_deltas": {"plant_production": 1, "mc_production": 2}, "resource_deltas": {"plants": 1}}'::jsonb
    ),
    (
        'aerobraked_ammonia_asteroid', 'Aerobraked Ammonia Asteroid', 26, '{space,space}', null,
        '{"target_card_resource_delta": 2, "production_deltas": {"heat_production": 3, "plant_production": 1}}'::jsonb
    ),
    (
        'magnetic_field_dome', 'Magnetic Field Dome', 5, '{building}', null,
        '{"production_deltas": {"energy_production": -2, "plant_production": 1}, "tr_delta": 1}'::jsonb
    ),
    (
        'pets', 'Pets', 10, '{earth,animal}', null,
        '{"becomes_active": true, "active_card_starting_resources": 1, "passive": {"on_city_tile_placed_add_resource": {"resource_delta": 1}}}'::jsonb
    ),
    (
        'protected_habitats', 'Protected Habitats', 5, '{}', null,
        '{}'::jsonb
    ),
    (
        'protected_valley', 'Protected Valley', 23, '{plant,building}', null,
        '{"production_deltas": {"mc_production": 2}, "raise_oxygen_steps": 1, "place_greenery": {"ignore_restrictions": true}}'::jsonb
    ),
    (
        'satellites', 'Satellites', 10, '{space}', null,
        '{"production_delta_per_tag": {"tag": "space", "production": "mc_production", "per_tag": 1, "include_this": true}}'::jsonb
    ),
    (
        'noctis_farming', 'Noctis Farming', 10, '{plant,building}', '{"min_temperature": -20}'::jsonb,
        '{"production_deltas": {"mc_production": 1}, "resource_deltas": {"plants": 2}}'::jsonb
    ),
    (
        'water_splitting_plant', 'Water Splitting Plant', 12, '{building}', '{"min_oceans": 2}'::jsonb,
        '{"becomes_active": true, "action": {"cost": {"energy": 3}, "gains": {"raise_oxygen_steps": 1}}}'::jsonb
    ),
    (
        'heat_trappers', 'Heat Trappers', 6, '{power,building}', null,
        '{"production_deltas": {"heat_production": -2, "energy_production": 1}}'::jsonb
    ),
    (
        'soil_factory', 'Soil Factory', 9, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "plant_production": 1}}'::jsonb
    ),
    (
        'fuel_factory', 'Fuel Factory', 6, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "titanium_production": 1, "mc_production": 1}}'::jsonb
    ),
    (
        'ice_cap_melting', 'Ice Cap Melting', 5, '{}', '{"min_temperature": 2}'::jsonb,
        '{"place_oceans": 1}'::jsonb
    ),
    (
        'corporate_stronghold', 'Corporate Stronghold', 11, '{building}', null,
        '{"production_deltas": {"energy_production": -1, "mc_production": 3}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'biomass_combustors', 'Biomass Combustors', 4, '{power}', '{"min_oxygen": 6}'::jsonb,
        '{"production_deltas": {"plant_production": -1, "energy_production": 2}}'::jsonb
    ),
    (
        'livestock', 'Livestock', 13, '{animal}', '{"min_oxygen": 9}'::jsonb,
        '{"production_deltas": {"plant_production": -1, "mc_production": 2}, "becomes_active": true, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'olympus_conference', 'Olympus Conference', 10, '{science,earth}', null,
        '{"becomes_active": true, "passive": {"on_tag_played_choice": {"matching_tags": ["science"], "add_resource_choice": {"resource_delta": 1}, "spend_resource_choice": {"card_resource": 1, "draw_cards": 1}}}}'::jsonb
    ),
    (
        'rad_suits', 'Rad-Suits', 6, '{}', '{"min_city_tiles": 2}'::jsonb,
        '{"production_deltas": {"mc_production": 1}}'::jsonb
    ),
    (
        'aquifer_pumping', 'Aquifer Pumping', 18, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"mc": 8}, "gains": {"place_oceans": 1}}}'::jsonb
    ),
    (
        'flooding', 'Flooding', 7, '{}', null,
        '{"place_oceans": 1}'::jsonb
    ),
    (
        'energy_saving', 'Energy Saving', 15, '{power}', null,
        '{"production_delta_per_counter": {"production": "energy_production", "counter": "city_tiles_placed", "per_counter": 1}}'::jsonb
    ),
    (
        'permafrost_extraction', 'Permafrost Extraction', 8, '{}', '{"min_temperature": -8}'::jsonb,
        '{"place_oceans": 1}'::jsonb
    ),
    (
        'invention_contest', 'Invention Contest', 2, '{science}', null,
        '{"start_research": {"n": 3}}'::jsonb
    ),
    (
        'plantation', 'Plantation', 15, '{science,science}', '{"min_tag_count": {"tag": "science", "count": 2}}'::jsonb,
        '{"raise_oxygen_steps": 1, "place_greenery": {}}'::jsonb
    ),
    (
        'power_infrastructure', 'Power Infrastructure', 4, '{power,building}', null,
        '{"becomes_active": true, "action": {"convert_resource_amount": {"from": "energy", "to": "mc", "ratio": 1}}}'::jsonb
    ),
    (
        'indentured_workers', 'Indentured Workers', 0, '{}', null,
        '{"next_card_discount_mc": -8}'::jsonb
    ),
    (
        'lagrange_observatory', 'Lagrange Observatory', 9, '{science,space}', null,
        '{"draw_cards": 1}'::jsonb
    ),
    (
        'terraforming_ganymede', 'Terraforming Ganymede', 33, '{earth,jovian}', null,
        '{"tr_delta_per_tag": {"tag": "jovian", "per_tag": 1, "include_this": true}}'::jsonb
    ),
    (
        'immigration_shuttles', 'Immigration Shuttles', 31, '{earth,earth}', null,
        '{"production_deltas": {"mc_production": 5}}'::jsonb
    ),
    (
        'restricted_area', 'Restricted Area', 11, '{science}', null,
        '{"becomes_active": true, "place_special_tile": {}, "action": {"cost": {"mc": 2}, "gains": {"draw_cards": 1}}}'::jsonb
    ),
    (
        'immigrant_city', 'Immigrant City', 13, '{city,building}', null,
        '{"production_deltas": {"energy_production": -1, "mc_production": -2}, "place_city_tiles": 1, "becomes_active": true, "passive": {"on_city_tile_placed_production_delta": {"production": "mc_production", "per_tile": 1}}}'::jsonb
    ),
    (
        'energy_tapping', 'Energy Tapping', 3, '{power}', null,
        '{"production_deltas": {"energy_production": 0}}'::jsonb
    ),
    (
        'underground_detonations', 'Underground Detonations', 6, '{building}', null,
        '{"becomes_active": true, "action": {"cost": {"mc": 10}, "gains": {"production_deltas": {"heat_production": 2}}}}'::jsonb
    ),
    (
        'soletta', 'Soletta', 35, '{power}', null,
        '{"production_deltas": {"heat_production": 7}}'::jsonb
    ),
    (
        'technology_demonstration', 'Technology Demonstration', 5, '{science,space}', null,
        '{"draw_cards": 2}'::jsonb
    ),
    (
        'rad_chem_factory', 'Rad-Chem Factory', 8, '{building,earth,earth}', null,
        '{"production_deltas": {"energy_production": -1}, "tr_delta": 2}'::jsonb
    ),
    (
        'special_design', 'Special Design', 4, '{science}', null,
        '{"next_card_requirement_tolerance_steps": 2}'::jsonb
    ),
    (
        'medical_lab', 'Medical Lab', 13, '{science,building}', null,
        '{"production_delta_per_tag": {"tag": "building", "production": "mc_production", "tags_per_step": 2, "include_this": true}}'::jsonb
    ),
    (
        'ai_central', 'AI Central', 21, '{science,building}', '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"production_deltas": {"energy_production": -1}, "becomes_active": true, "action": {"cost": {}, "gains": {"draw_cards": 2}}}'::jsonb
    ),
    (
        'small_asteroid', 'Small Asteroid', 10, '{space}', null,
        '{"raise_temperature_steps": 1}'::jsonb
    ),
    (
        'snow_algae', 'Snow Algae', 12, '{plant}', '{"min_oceans": 2}'::jsonb,
        '{"production_deltas": {"plant_production": 1, "heat_production": 1}}'::jsonb
    ),

    -- Bloque de revision 20 (expansion Venus Next, ver CLAUDE.md seccion 7 y
    -- CARDS_LOG.md "Resuelto 2026-09-02: expansion Venus Next").
    (
        'penguins', 'Penguins', 7, '{animal}', '{"min_oceans": 8}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'aerial_mappers', 'Aerial Mappers', 11, '{venus}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"gains": {"target_card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"draw_cards": 1}}
        ]}}'::jsonb
    ),
    (
        'air_scrapping_expedition', 'Air-Scrapping Expedition', 13, '{venus}', null,
        '{"raise_venus_steps": 1, "target_card_resource_delta": 3}'::jsonb
    ),
    (
        'atalanta_planitia_lab', 'Atalanta Planitia Lab', 10, '{venus,science}',
        '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"draw_cards": 2}'::jsonb
    ),
    (
        'atmoscoop', 'Atmoscoop', 22, '{jovian,power}',
        '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"choice": [
            {"raise_temperature_steps": 2, "target_card_resource_delta": 2},
            {"raise_venus_steps": 2, "target_card_resource_delta": 2}
        ]}'::jsonb
    ),
    (
        'comet_for_venus', 'Comet for Venus', 11, '{power}', null,
        '{"raise_venus_steps": 1}'::jsonb
    ),
    (
        'corroder_suits', 'Corroder Suits', 8, '{venus}', null,
        '{"production_deltas": {"mc_production": 2}, "target_card_resource_delta": 1}'::jsonb
    ),
    (
        'dawn_city', 'Dawn City', 15, '{power,city}',
        '{"min_tag_count": {"tag": "science", "count": 4}}'::jsonb,
        '{"production_deltas": {"energy_production": -1, "titanium_production": 1}, "place_city_tiles": 1}'::jsonb
    ),
    (
        'deuterium_export', 'Deuterium Export', 11, '{venus,power,power}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"production_deltas": {"energy_production": 1}}}
        ]}}'::jsonb
    ),

    -- Lava Flows (#140): pieza pendiente resuelta 2026-09-02 -- ver
    -- HEX_MAP_RESEARCH.md "Los 4 volcanes con nombre" para las fuentes
    -- usadas en identificar cada hex_id (09/14/21/29).
    (
        'lava_flows', 'Lava Flows', 18, '{}', null,
        '{"raise_temperature_steps": 2, "place_special_tile": {"hex_id_in": ["09", "14", "21", "29"]}}'::jsonb
    ),

    -- Bloque de revision 21 (Venus Next). Dirigibles (#222) queda pendiente
    -- -- ver CARDS_LOG.md "Pendientes" (floaters como moneda de pago).
    (
        'extractor_balloons', 'Extractor Balloons', 21, '{venus}', null,
        '{"becomes_active": true, "active_card_starting_resources": 3, "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}}
        ]}}'::jsonb
    ),
    (
        'extremophiles', 'Extremophiles', 3, '{venus,microbe}',
        '{"min_tag_count": {"tag": "science", "count": 2}}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        'floating_habs', 'Floating Habs', 5, '{venus}',
        '{"min_tag_count": {"tag": "science", "count": 2}}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"cost": {"mc": 2}, "gains": {"card_resource_delta": 1}},
            {"cost": {"mc": 2}, "gains": {"target_card_resource_delta": 1}}
        ]}}'::jsonb
    ),
    (
        'forced_precipitation', 'Forced Precipitation', 8, '{venus}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"cost": {"mc": 2}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}}
        ]}}'::jsonb
    ),
    (
        -- El texto real ofrece elegir "2 microbios O 2 animales a OTRA carta
        -- Venus" -- mecanicamente identico en este motor (recursos sin tipo
        -- por carta), asi que se aplica directo sin choice (ver CARDS_LOG.md).
        'freyja_biodomes', 'Freyja Biodomes', 14, '{venus,plant}',
        '{"min_venus": 10}'::jsonb,
        '{"target_card_resource_delta": 2, "production_deltas": {"energy_production": -1, "mc_production": 2}}'::jsonb
    ),
    (
        'ghg_import_from_venus', 'GHG Import from Venus', 23, '{venus,power}', null,
        '{"raise_venus_steps": 1, "production_deltas": {"heat_production": 3}}'::jsonb
    ),
    (
        'giant_solar_shade', 'Giant Solar Shade', 27, '{venus,power}', null,
        '{"raise_venus_steps": 3}'::jsonb
    ),
    (
        'gyropolis', 'Gyropolis', 20, '{city,building}', null,
        '{"production_deltas": {"energy_production": -2}, "production_delta_per_tag": [
            {"tag": "venus", "production": "mc_production", "per_tag": 1},
            {"tag": "earth", "production": "mc_production", "per_tag": 1}
        ], "place_city_tiles": 1}'::jsonb
    ),
    (
        'hydrogen_to_venus', 'Hydrogen to Venus', 11, '{power}', null,
        '{"raise_venus_steps": 1, "target_card_resource_delta_per_tag": {"tag": "jovian", "per_tag": 1}}'::jsonb
    ),

    -- Bloque de revision 22 (Venus Next). Las 10 resueltas con vocabulario existente.
    (
        'io_sulphur_research', 'IO Sulphur Research', 17, '{science,jovian}', null,
        '{"tag_count_choice": {"tag": "venus", "count": 3, "if_met": {"draw_cards": 3}, "else": {"draw_cards": 1}}}'::jsonb
    ),
    (
        'ishtar_mining', 'Ishtar Mining', 5, '{venus}', '{"min_venus": 8}'::jsonb,
        '{"production_deltas": {"titanium_production": 1}}'::jsonb
    ),
    (
        'jet_stream_microscrappers', 'Jet Stream Microscrappers', 12, '{venus}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 2}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}}
        ]}}'::jsonb
    ),
    (
        'local_shading', 'Local Shading', 4, '{venus}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"production_deltas": {"mc_production": 1}}}
        ]}}'::jsonb
    ),
    (
        'luna_metropolis', 'Luna Metropolis', 21, '{power,earth,city}', null,
        '{"production_delta_per_tag": {"tag": "earth", "production": "mc_production", "per_tag": 1, "include_this": true}, "place_city_tiles": 1}'::jsonb
    ),
    (
        -- Sin efecto numerico modelado -- el texto real solo exige los 3 tags,
        -- sin ningun cambio de estado (VP no trackeado, ver CLAUDE.md seccion 4).
        'luxury_foods', 'Luxury Foods', 8, '{venus,earth,jovian}',
        '{"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}'::jsonb,
        '{}'::jsonb
    ),
    (
        'maxwell_base', 'Maxwell Base', 18, '{venus,city}', '{"min_venus": 12}'::jsonb,
        '{"production_deltas": {"energy_production": -1}, "place_city_tiles": 1, "becomes_active": true,
          "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'mining_quota', 'Mining Quota', 5, '{venus,earth,jovian,building}',
        '{"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}'::jsonb,
        '{"production_deltas": {"steel_production": 2}}'::jsonb
    ),
    (
        'neutralizer_factory', 'Neutralizer Factory', 7, '{venus}', '{"min_venus": 10}'::jsonb,
        '{"raise_venus_steps": 1}'::jsonb
    ),
    (
        'omnicourt', 'Omnicourt', 11, '{venus,earth,jovian,building}',
        '{"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}'::jsonb,
        '{"tr_delta": 2}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

-- Bloque de revision 23 (Venus Next). Las 10 resueltas. Dos piezas nuevas
-- chicas de motor: "mc_or_titanium" en el cost de use_card_action (Rotator
-- Impacts: el titanio puede cubrir parte/todo un costo en MC de una accion,
-- igual que al pagar cartas) y "discard_card_then_draw" en apply_card_effect
-- (Sponsored Academies: descartar 1 carta elegida, robar N).
insert into cards (id, name, cost, tags, requirements, effects) values
    (
        'orbital_reflectors', 'Orbital Reflectors', 26, '{venus,power}', null,
        '{"raise_venus_steps": 2, "production_deltas": {"heat_production": 2}}'::jsonb
    ),
    (
        'rotator_impacts', 'Rotator Impacts', 6, '{power}', '{"max_venus": 14}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"cost": {"mc_or_titanium": 6}, "gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"raise_venus_steps": 1}}
        ]}}'::jsonb
    ),
    (
        'sister_planet_support', 'Sister Planet Support', 7, '{venus,earth}',
        '{"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}]}'::jsonb,
        '{"production_deltas": {"mc_production": 3}}'::jsonb
    ),
    (
        'solarnet', 'Solarnet', 7, '{venus,earth,jovian}',
        '{"min_tag_count": [{"tag": "venus", "count": 1}, {"tag": "earth", "count": 1}, {"tag": "jovian", "count": 1}]}'::jsonb,
        '{"draw_cards": 2}'::jsonb
    ),
    (
        'spin_inducing_asteroid', 'Spin-Inducing Asteroid', 16, '{power}', '{"max_venus": 10}'::jsonb,
        '{"raise_venus_steps": 2}'::jsonb
    ),
    (
        -- "each opponent draws 1" omitida (no afecta al jugador en single-player).
        'sponsored_academies', 'Sponsored Academies', 9, '{}',
        '{"min_tag_count": [{"tag": "science", "count": 1}, {"tag": "earth", "count": 1}]}'::jsonb,
        '{"discard_card_then_draw": {"draw": 3}}'::jsonb
    ),
    (
        'stratopolis', 'Stratopolis', 22, '{venus,city}',
        '{"min_tag_count": {"tag": "science", "count": 2}}'::jsonb,
        '{"production_deltas": {"mc_production": 2}, "place_city_tiles": 1, "becomes_active": true,
          "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"target_card_resource_delta": 2}}}'::jsonb
    ),
    (
        'stratospheric_birds', 'Stratospheric Birds', 12, '{venus,animal}', '{"min_venus": 12}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"move_from_target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'sulphur_exports', 'Sulphur Exports', 21, '{venus}', null,
        '{"raise_venus_steps": 1, "production_delta_per_tag": {"tag": "venus", "production": "mc_production", "per_tag": 1, "include_this": true}}'::jsonb
    ),
    (
        'sulphur_eating_bacteria', 'Sulphur-Eating Bacteria', 6, '{venus,microbe}', '{"min_venus": 6}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"convert_card_resource_amount": {"to": "mc", "ratio": 3}}
        ]}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

update cards set is_event = true where id in ('spin_inducing_asteroid');

-- Marca como "Event" (dispara bonus pasivos "on_event_played" de otras
-- cartas al jugarse) las cartas que corresponden en el juego real.
update cards set is_event = true
where id in ('investment_loan', 'comet', 'asteroid_card', 'big_asteroid', 'release_of_inert_gases',
             'business_contacts', 'bribed_committee', 'sabotage', 'hired_raiders', 'subterranean_reservoir',
             'local_heat_trapping', 'imported_hydrogen', 'large_convoy', 'ceos_favorite_project',
             'convoy_from_europa', 'imported_ghg', 'imported_nitrogen', 'import_of_advanced_ghg',
             'aerobraked_ammonia_asteroid', 'ice_cap_melting', 'flooding', 'permafrost_extraction',
             'indentured_workers', 'technology_demonstration', 'special_design', 'small_asteroid',
             'air_scrapping_expedition', 'comet_for_venus', 'lava_flows',
             'ghg_import_from_venus', 'hydrogen_to_venus');

-- Bloque de revision 24 (Venus Next). Las 10 resueltas con vocabulario
-- existente, salvo el requirement nuevo "min_tr" (Terraforming Contract).
insert into cards (id, name, cost, tags, requirements, effects) values
    (
        'terraforming_contract', 'Terraforming Contract', 8, '{earth}', '{"min_tr": 25}'::jsonb,
        '{"production_deltas": {"mc_production": 4}}'::jsonb
    ),
    (
        'thermophiles', 'Thermophiles', 9, '{venus,microbe}', '{"min_venus": 6}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"target_card_resource_delta": 1}},
            {"cost": {"card_resource": 2}, "gains": {"raise_venus_steps": 1}}
        ]}}'::jsonb
    ),
    (
        'water_to_venus', 'Water to Venus', 9, '{power}', null,
        '{"raise_venus_steps": 1}'::jsonb
    ),
    (
        'venus_governor', 'Venus Governor', 4, '{venus,venus}',
        '{"min_tag_count": {"tag": "venus", "count": 2}}'::jsonb,
        '{"production_deltas": {"mc_production": 2}}'::jsonb
    ),
    (
        'venus_magnetizer', 'Venus Magnetizer', 7, '{venus}', '{"min_venus": 10}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {},
          "gains": {"production_deltas": {"energy_production": -1}, "raise_venus_steps": 1}}}'::jsonb
    ),
    (
        'venus_soils', 'Venus Soils', 20, '{venus,plant}', null,
        '{"raise_venus_steps": 1, "production_deltas": {"plant_production": 1}, "target_card_resource_delta": 2}'::jsonb
    ),
    (
        'venus_waystation', 'Venus Waystation', 9, '{venus,power}', null,
        '{"passive": {"card_cost_discount_mc": 2, "tag_filter": "venus"}}'::jsonb
    ),
    (
        'venusian_animals', 'Venusian Animals', 15, '{venus,science,animal}', '{"min_venus": 18}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0,
          "passive": {"on_tag_played_add_resource": {"matching_tags": ["science"], "resource_delta": 1}}}'::jsonb
    ),
    (
        'venusian_insects', 'Venusian Insects', 5, '{venus,microbe}', '{"min_venus": 12}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"card_resource_delta": 1}}}'::jsonb
    ),
    (
        -- "1 microbio O 1 animal a OTRA carta Venus" -- mecanicamente identico
        -- en este motor (recursos sin tipo por carta), aplicado sin choice.
        'venusian_plants', 'Venusian Plants', 13, '{venus,plant}', '{"min_venus": 16}'::jsonb,
        '{"raise_venus_steps": 1, "target_card_resource_delta": 1}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

update cards set is_event = true where id in ('water_to_venus');

-- Bloque de revision 25 (expansion Colonies). Bloque completo, incluida
-- primera vez que aparecen cartas Colonies -- 5 de 10 cargadas ahora, ver
-- CARDS_LOG.md "Pendientes" para las 5 restantes (4 necesitan piezas de
-- motor no triviales: suma de floaters entre todas las cartas activas, o
-- la mecanica completa de colonias/comercio; 1 es multi-jugador puro).
insert into cards (id, name, cost, tags, requirements, effects) values
    (
        'atmo_collectors', 'Atmo Collectors', 15, '{}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "target_card_resource_delta": 2,
          "action": {"choice": [
            {"gains": {"card_resource_delta": 1}},
            {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"titanium": 2}}},
            {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"energy": 3}}},
            {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"heat": 4}}}
        ]}}'::jsonb
    ),
    (
        'community_services', 'Community Services', 13, '{}', null,
        '{"production_delta_per_zero_tag_card": {"production": "mc_production", "per_card": 1, "include_this": true}}'::jsonb
    ),
    (
        'conscription', 'Conscription', 5, '{earth,earth}',
        '{"min_tag_count": {"tag": "earth", "count": 2}}'::jsonb,
        '{"next_card_discount_mc": 16}'::jsonb
    ),
    (
        'corona_extractor', 'Corona Extractor', 10, '{science}',
        '{"min_tag_count": {"tag": "science", "count": 4}}'::jsonb,
        '{"production_deltas": {"energy_production": 4}}'::jsonb
    ),
    (
        'earth_elevator', 'Earth Elevator', 43, '{earth,power}', null,
        '{"production_deltas": {"titanium_production": 3}}'::jsonb
    ),
    (
        -- Resueltas 2026-09-03 al implementar la mecanica de colonias/comercio.
        'cryo_sleep', 'Cryo-Sleep', 10, '{science}', null,
        '{"passive": {"trade_cost_discount": 1}}'::jsonb
    ),
    (
        'ecology_research', 'Ecology Research', 21, '{science,animal,microbe,plant}', null,
        '{"production_delta_per_colony": {"production": "plant_production", "per_colony": 1},
          "target_card_resource_delta": 1, "target_card_resource_delta_2": 2}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

-- Bloque de revision 26 (Colonies). Las 10 resueltas con vocabulario
-- existente, salvo dos piezas nuevas chicas: "build_colony" (efecto de
-- carta que construye una colonia, manejado en tools.play_card igual que
-- place_special_tile) y "mc_per_card_resource" en use_card_action (da MC
-- por recurso guardado en la carta SIN gastarlo, con tope opcional).
insert into cards (id, name, cost, tags, requirements, effects) values
    (
        'floater_prototypes', 'Floater Prototypes', 2, '{science}', null,
        '{"target_card_resource_delta": 2}'::jsonb
    ),
    (
        'floater_technology', 'Floater Technology', 7, '{science}', null,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"cost": {}, "gains": {"target_card_resource_delta": 1}}}'::jsonb
    ),
    (
        'galilean_waystation', 'Galilean Waystation', 15, '{power}', null,
        '{"production_delta_per_tag": {"tag": "jovian", "production": "mc_production", "per_tag": 1}}'::jsonb
    ),
    (
        'heavy_taxation', 'Heavy Taxation', 3, '{earth,earth}',
        '{"min_tag_count": {"tag": "earth", "count": 2}}'::jsonb,
        '{"resource_deltas": {"mc": 4}, "production_deltas": {"mc_production": 2}}'::jsonb
    ),
    (
        'ice_moon_colony', 'Ice Moon Colony', 23, '{power}', null,
        '{"build_colony": true, "place_oceans": 1}'::jsonb
    ),
    (
        -- "remove up to 2 plants from any player" omitida (regla de oro single-player).
        'impactor_swarm', 'Impactor Swarm', 11, '{jovian,jovian}',
        '{"min_tag_count": {"tag": "jovian", "count": 2}}'::jsonb,
        '{"resource_deltas": {"heat": 12}}'::jsonb
    ),
    (
        'interplanetary_colony_ship', 'Interplanetary Colony Ship', 12, '{earth,power}', null,
        '{"build_colony": true}'::jsonb
    ),
    (
        'jovian_lanterns', 'Jovian Lanterns', 20, '{jovian}',
        '{"min_tag_count": {"tag": "jovian", "count": 1}}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "tr_delta": 1, "target_card_resource_delta": 2,
          "action": {"cost": {"titanium": 1}, "gains": {"card_resource_delta": 2}}}'::jsonb
    ),
    (
        'jupiter_floating_station', 'Jupiter Floating Station', 9, '{jovian}',
        '{"min_tag_count": {"tag": "science", "count": 3}}'::jsonb,
        '{"becomes_active": true, "active_card_starting_resources": 0, "action": {"choice": [
            {"gains": {"target_card_resource_delta": 1}},
            {"gains": {"mc_per_card_resource": {"cap": 4}}}
        ]}}'::jsonb
    ),
    (
        'luna_governor', 'Luna Governor', 4, '{earth,earth}',
        '{"min_tag_count": {"tag": "earth", "count": 3}}'::jsonb,
        '{"production_deltas": {"mc_production": 2}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

update cards set is_event = true where id in
    ('floater_prototypes', 'impactor_swarm', 'interplanetary_colony_ship');
