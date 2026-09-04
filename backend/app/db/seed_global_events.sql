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

-- Bloque 5 (2026-09-04): 20 de 22 cargadas, analizadas en paralelo por 4
-- agentes (grupos A/B/C/D, ver CARDS_LOG.md para el detalle de quien tomo
-- cada carta). Pendientes: Mud Slides (necesita el tablero hexagonal
-- wireado -- contar tiles adyacentes a oceano) y Solarnet Shutdown
-- (necesita clasificar cartas por color en el catalogo, retrofit completo).
-- Piezas nuevas: contadores "colonies_owned", "hand_size",
-- "<recurso>_production" y "tr_sets_of_5_over:<N>"; "cap": null (sin tope)
-- e "influence_direction": "none" en resource_delta_per_capped_counter;
-- production_delta_per_influence, tr_delta_reduced_by_influence,
-- lower_temperature_steps, add_resource_to_all_cards_with_resources,
-- discard_cards.
insert into global_events (id, name, effects) values
    -- Grupo A
    (
        'interplanetary_trade', 'Interplanetary Trade',
        '{"resource_delta_per_capped_counter": {"counter": "tag:space", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'jovian_tax_rights', 'Jovian Tax Rights',
        '{"production_delta_per_colony": {"production": "mc_production", "per_colony": 1},
          "resource_delta_per_influence": {"titanium": 1}}'::jsonb
    ),
    (
        'microgravity_health_problems', 'Microgravity Health Problems',
        '{"resource_delta_per_capped_counter": {"counter": "colonies_owned", "resource": "mc", "per_unit": -3, "influence_direction": "subtract"}}'::jsonb
    ),
    (
        'miners_on_strike', 'Miners on Strike',
        '{"resource_delta_per_capped_counter": {"counter": "tag:jovian", "resource": "titanium", "per_unit": -1, "influence_direction": "subtract"}}'::jsonb
    ),
    (
        'pandemic', 'Pandemic',
        '{"resource_delta_per_capped_counter": {"counter": "tag:building", "resource": "mc", "per_unit": -3, "influence_direction": "subtract"}}'::jsonb
    ),
    -- Grupo B
    (
        'productivity', 'Productivity',
        '{"resource_delta_per_capped_counter": {"counter": "steel_production", "resource": "steel", "per_unit": 1, "influence_direction": "add"}}'::jsonb
    ),
    (
        'revolution', 'Revolution',
        '{"tr_delta_by_threshold": {"score_tags": ["earth"], "thresholds": [[4, -2]]}}'::jsonb
    ),
    (
        'sabotage', 'Sabotage',
        '{"production_deltas": {"steel_production": -1, "energy_production": -1},
          "resource_delta_per_influence": {"steel": 1}}'::jsonb
    ),
    (
        'paradigm_breakdown', 'Paradigm Breakdown',
        '{"discard_cards": {"n": 2}, "resource_delta_per_influence": {"mc": 2}}'::jsonb
    ),
    (
        'red_influence', 'Red Influence',
        '{"resource_delta_per_capped_counter": {"counter": "tr_sets_of_5_over:10", "resource": "mc", "per_unit": -3, "influence_direction": "none"},
          "production_delta_per_influence": {"mc_production": 1}}'::jsonb
    ),
    (
        'scientific_community', 'Scientific Community',
        '{"resource_delta_per_capped_counter": {"counter": "hand_size", "resource": "mc", "per_unit": 1, "cap": null, "influence_direction": "add"}}'::jsonb
    ),
    -- Grupo C
    (
        'snow_cover', 'Snow Cover',
        '{"lower_temperature_steps": 2, "draw_cards_per_influence": true}'::jsonb
    ),
    (
        'solar_flare', 'Solar Flare',
        '{"resource_delta_per_capped_counter": {"counter": "tag:space", "resource": "mc", "per_unit": -3, "influence_direction": "subtract"}}'::jsonb
    ),
    (
        'spin_off_products', 'Spin-off Products',
        '{"resource_delta_per_capped_counter": {"counter": "tag:science", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'sponsored_projects', 'Sponsored Projects',
        '{"add_resource_to_all_cards_with_resources": {"amount": 1}, "draw_cards_per_influence": true}'::jsonb
    ),
    -- Grupo D
    (
        'strong_society', 'Strong Society',
        '{"resource_delta_per_capped_counter": {"counter": "city_tiles_placed", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'successful_organisms', 'Successful Organisms',
        '{"resource_delta_per_capped_counter": {"counter": "plant_production", "resource": "plants", "per_unit": 1, "influence_direction": "add"}}'::jsonb
    ),
    (
        'venus_infrastructure', 'Venus Infrastructure',
        '{"resource_delta_per_capped_counter": {"counter": "tag:venus", "resource": "mc", "per_unit": 2, "influence_direction": "add"}}'::jsonb
    ),
    (
        'volcanic_eruptions', 'Volcanic Eruptions',
        '{"raise_temperature_steps": 2, "production_delta_per_influence": {"heat_production": 1}}'::jsonb
    ),
    (
        'war_on_earth', 'War on Earth',
        '{"tr_delta_reduced_by_influence": {"base_reduction": 4}}'::jsonb
    )
on conflict (id) do update set
    name = excluded.name,
    effects = excluded.effects;
