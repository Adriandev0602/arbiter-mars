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
where id in ('investment_loan', 'comet', 'asteroid_card', 'big_asteroid');
