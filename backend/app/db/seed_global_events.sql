-- Catalogo de Global Event cards (expansion Turmoil). Mismo criterio que
-- seed_cards.sql: no se generan datos al voleo -- cada carta se verifica
-- contra su fuente antes de cargarla (ver CARDS_LOG.md, seccion "Turmoil:
-- Global Events").
--
-- Estas 2 primeras (Generous Funding, Riots) vienen del rulebook OFICIAL de
-- la expansion (TM_TURMOIL_ENG_RULES.pdf, pagina 5) -- son los 2 ejemplos
-- trabajados que el propio rulebook usa para explicar la formula de
-- Influencia + tope de 5, con el texto impreso Y un ejemplo numerico
-- resuelto paso a paso. Fuente mas fuerte que un scan individual.
--
-- Correr despues de schema.sql.

insert into global_events (id, name, effects) values
    (
        'generous_funding', 'Generous Funding',
        '{"resource_delta_per_capped_counter": {"counter": "tr_sets_of_5_over_15", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'riots', 'Riots',
        '{"resource_delta_per_capped_counter": {"counter": "city_tiles_placed", "resource": "mc", "per_unit": -4, "influence_direction": "subtract"}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    effects = excluded.effects;

-- Bloque 2 (2026-09-04): 4 de 6 cargadas -- Cloud Societies y Corrosive Rain
-- quedan pendientes (necesitan la mecanica de "floaters por carta activa",
-- ya pendiente por Aerosport Tournament/Airliners/Floater Leasing -- ver
-- CARDS_LOG.md). Piezas nuevas: contadores "events_played"/"tag:<tag>" en
-- _resolve_capped_counter, "resource_delta_per_influence" (sin tope),
-- "resource_delta_if_tag_diversity" (umbral booleano, sin tope).
insert into global_events (id, name, effects) values
    (
        'aquifer_released_by_public_council', 'Aquifer Released by Public Council',
        '{"place_oceans": 1, "resource_delta_per_influence": {"plants": 1, "steel": 1}}'::jsonb
    ),
    (
        'asteroid_mining', 'Asteroid Mining',
        '{"resource_delta_per_capped_counter": {"counter": "tag:jovian", "resource": "titanium", "per_unit": 1, "influence_direction": "add"}}'::jsonb
    ),
    (
        'celebrity_leaders', 'Celebrity Leaders',
        '{"resource_delta_per_capped_counter": {"counter": "events_played", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'diversity', 'Diversity',
        '{"resource_delta_if_tag_diversity": {"threshold": 9, "resource": "mc", "amount": 10}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    effects = excluded.effects;

-- Bloque 3 (2026-09-04): Cloud Societies y Corrosive Rain, resueltas gracias
-- a la pieza nueva de "recursos tipados por carta activa" (ver
-- seed_cards.sql, mismo bloque -- Aerosport Tournament/Airliners/Floater
-- Leasing). Piezas nuevas usadas: "add_resource_to_all_matching_type",
-- "target_card_resource_delta_typed" (con "amount_per_influence"),
-- "draw_cards_per_influence".
insert into global_events (id, name, effects) values
    (
        'cloud_societies', 'Cloud Societies',
        '{"add_resource_to_all_matching_type": {"resource_type": "floater", "amount": 1},
          "target_card_resource_delta_typed": {"resource_type": "floater", "amount_per_influence": true}}'::jsonb
    ),
    (
        'corrosive_rain', 'Corrosive Rain',
        '{"choice": [
            {"target_card_resource_delta_typed": {"resource_type": "floater", "amount": -2}, "draw_cards_per_influence": true},
            {"resource_deltas": {"mc": -10}, "draw_cards_per_influence": true}
          ]}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    effects = excluded.effects;

-- Bloque 4 (2026-09-04): 5 de 6 cargadas -- Dry Deserts queda pendiente
-- (necesita decidir la semantica de "remove 1 ocean tile" sin tablero
-- hexagonal wireado a Global Events, mas un mecanismo de "recurso estandar
-- a eleccion" -- ver CARDS_LOG.md). Piezas nuevas:
-- resource_delta_clamp_to_capped_max, resource_set_to_zero,
-- tr_delta_by_threshold, production_delta_per_tag_plus_influence.
insert into global_events (id, name, effects) values
    (
        'eco_sabotage', 'Eco Sabotage',
        '{"resource_delta_clamp_to_capped_max": {"resource": "plants", "base_max": 3}}'::jsonb
    ),
    (
        'election', 'Election',
        '{"tr_delta_by_threshold": {"score_tags": ["building"], "score_counters": ["city_tiles_placed"], "thresholds": [[10, 2], [5, 1]]}}'::jsonb
    ),
    (
        'global_dust_storm', 'Global Dust Storm',
        '{"resource_set_to_zero": ["heat"],
          "resource_delta_per_capped_counter": {"counter": "tag:building", "resource": "mc", "per_unit": -2, "influence_direction": "subtract"}}'::jsonb
    ),
    (
        'homeworld_support', 'Homeworld Support',
        '{"resource_delta_per_capped_counter": {"counter": "tag:earth", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'improved_energy_templates', 'Improved Energy Templates',
        '{"production_delta_per_tag_plus_influence": {"tag": "power", "production": "energy_production", "divisor": 2, "per_unit": 1}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    effects = excluded.effects;
