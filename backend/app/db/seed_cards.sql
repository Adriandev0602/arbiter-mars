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
    )
on conflict (id) do update set
    name = excluded.name,
    cost = excluded.cost,
    tags = excluded.tags,
    requirements = excluded.requirements,
    effects = excluded.effects;
