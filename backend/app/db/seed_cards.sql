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
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;
