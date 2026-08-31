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
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;

-- Marca como "Event" (dispara bonus pasivos "on_event_played" de otras
-- cartas al jugarse) las cartas que corresponden en el juego real.
update cards set is_event = true
where id in ('investment_loan', 'comet', 'asteroid_card', 'big_asteroid', 'release_of_inert_gases');
