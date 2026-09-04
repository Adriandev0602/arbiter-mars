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
