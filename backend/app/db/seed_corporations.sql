-- Catalogo de CORPORACIONES. Cada jugador elige una al empezar la partida.
--
-- Descubrimiento (2026-09-04): estas 48 cartas nunca habian entrado al
-- pipeline porque enqueue_card_review_queue.py filtraba solo cat=="Project".
-- Ver "Corporaciones" en CARDS_LOG.md.
--
-- `starting_mc` REEMPLAZA el M€ del jugador, y tools.choose_corporation ademas
-- pone las seis producciones en 0 antes de aplicar `effects`: el rulebook dice
-- que la produccion 1 de cada recurso es de la partida ESTANDAR ("only in
-- standard game"), no de una partida con corporaciones. Por eso Beginner
-- Corporation lleva production_deltas +1 en cada recurso.
--
-- Correr despues de schema.sql.

-- Bloque 1 (alfabetico, Aphrodite -> EcoLine): 9 de 10 cargadas.
-- Arcadian Communities queda pendiente por mecanica de tablero (marcadores de
-- "community" que reservan hexagonos), ver CARDS_LOG.md.
--
-- TAGS verificados contra los scans en hoja de contacto: dos informes de
-- agentes los leyeron mal. Celestic SI tiene tag `venus` (el circulo "V" del
-- extremo superior derecho es un TAG, no el banner de la expansion -- Aphrodite
-- lleva el mismo circulo junto al de plant), y Cheung Shing Mars SI tiene tag
-- `building` (el agente lo leyo como parte del texto del Effect).
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 47 M€, +1 produccion de plantas. Effect: +2 M€ por cada PASO de Venus,
    -- lo suba quien lo suba (pieza nueva `on_venus_raised`, dentro de raise_venus).
    ('aphrodite', 'Aphrodite', 'Venus Next', '{venus,plant}', 47,
     '{"production_deltas": {"plant_production": 1},
       "passive": {"on_venus_raised": {"mc_delta": 2}}}'::jsonb),

    -- 40 M€. Effect: +1 produccion de M€ cada vez que aparece un tipo de tag
    -- NUEVO (los eventos no cuentan) -- pieza nueva `on_new_distinct_tag_played`.
    -- La clausula de setup ("as your first action, put an ADDITIONAL colony tile
    -- into play") es una regla de SETUP: se resuelve con la tool setup_colonies
    -- agregando una colonia mas, no es un efecto de carta.
    ('aridor', 'Aridor', 'Colonies', '{}', 40,
     '{"passive": {"on_new_distinct_tag_played": {"production_deltas": {"mc_production": 1}}}}'::jsonb),

    -- 45 M€, +2 produccion de M€. Guarda animales. Effect: +1 animal aca por
    -- cada tag animal/plant jugado, incluido el suyo propio (por eso el tag
    -- animal de la propia corpo dispara el pasivo al elegirla).
    -- "1 VP per 2 animals" no se modela: el motor no puntua.
    ('arklight', 'Arklight', 'Colonies', '{animal}', 45,
     '{"production_deltas": {"mc_production": 2}, "becomes_active": true,
       "active_card_resource_type": "animal",
       "passive": {"on_tag_played_add_resource": {"matching_tags": ["animal", "plant"],
                                                  "resource_delta": 1}}}'::jsonb),

    -- 35 M€ y 3 asteroides en la carta. Accion: 1 asteroide a CUALQUIER carta,
    -- o ganar 1 recurso estandar, o gastar 1 asteroide de aca por 3 titanio.
    -- Las tres ramas del "OR" son opciones de un mismo `choice`, y el "recurso
    -- estandar a eleccion" son 6 opciones mas (mismo criterio que Applied Science).
    ('astrodrill', 'Astrodrill', 'Promo', '{space}', 35,
     '{"becomes_active": true, "active_card_resource_type": "asteroid",
       "active_card_starting_resources": 3,
       "action": {"choice": [
         {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}},
         {"cost": {}, "gains": {"resource_deltas": {"mc": 1}}},
         {"cost": {}, "gains": {"resource_deltas": {"steel": 1}}},
         {"cost": {}, "gains": {"resource_deltas": {"titanium": 1}}},
         {"cost": {}, "gains": {"resource_deltas": {"plants": 1}}},
         {"cost": {}, "gains": {"resource_deltas": {"energy": 1}}},
         {"cost": {}, "gains": {"resource_deltas": {"heat": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"titanium": 3}}}]}}'::jsonb),

    -- 42 M€ y produccion 1 en cada recurso: ES la partida estandar del rulebook
    -- ("you start with 1 production of each resource... only in standard game").
    -- Las 10 cartas gratis son una regla de SETUP (reemplazan la compra inicial),
    -- no un efecto de carta: se reparten con deal_starting_hand sin cobrar.
    ('beginner_corporation', 'Beginner Corporation', 'Base', '{}', 42,
     '{"production_deltas": {"mc_production": 1, "steel_production": 1, "titanium_production": 1,
                             "plant_production": 1, "energy_production": 1, "heat_production": 1}}'::jsonb),

    -- 42 M€. Guarda floaters. Accion: 1 floater a CUALQUIER carta.
    -- La clausula de setup ("reveal cards until 2 with a floater ICON") queda
    -- SIN modelar: el icono de floater no es un tag, es una marca del arte que
    -- el catalogo no guarda. "1 VP per 3 floaters" tampoco: el motor no puntua.
    ('celestic', 'Celestic', 'Venus Next', '{venus}', 42,
     '{"becomes_active": true, "active_card_resource_type": "floater",
       "action": {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}}}'::jsonb),

    -- 44 M€, +3 produccion de M€. Effect: las cartas con tag building cuestan
    -- 2 M€ menos (mismo vocabulario que Mass Converter con space).
    ('cheung_shing_mars', 'Cheung Shing MARS', 'Prelude', '{building}', 44,
     '{"production_deltas": {"mc_production": 3},
       "passive": {"card_cost_discount_mc": 2, "tag_filter": "building"}}'::jsonb),

    -- 57 M€. Effect: +4 M€ despues de pagar una carta O un proyecto estandar de
    -- costo BASICO 20+ (pieza nueva `on_cost_threshold_paid`: es la union de
    -- on_card_played_cost_threshold_draw con on_standard_project_used).
    ('credicor', 'CrediCor', 'Base', '{}', 57,
     '{"passive": {"on_cost_threshold_paid": {"min_cost": 20, "mc_delta": 4}}}'::jsonb),

    -- 36 M€, +2 produccion de plantas, 3 plantas. Effect: convertir plantas en
    -- greenery cuesta 7 en vez de 8 (pieza nueva `plants_per_greenery`).
    ('ecoline', 'EcoLine', 'Base', '{plant}', 36,
     '{"production_deltas": {"plant_production": 2}, "resource_deltas": {"plants": 3},
       "passive": {"plants_per_greenery": 7}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

-- Marcado de la cola de revision. Idempotente: se puede re-correr.
update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Aphrodite','aphrodite'),('Aridor','aridor'),('Arklight','arklight'),
    ('Astrodrill','astrodrill'),('Beginner Corporation','beginner_corporation'),
    -- OJO: la cola usa el nombre tal como lo escribe el indice del sitio, que
    -- no siempre respeta las mayusculas del arte de la carta ("Cheung Shing
    -- Mars", "Credicor", "Ecoline"). corporation_cards.name si lleva el
    -- nombre impreso.
    ('Celestic','celestic'),('Cheung Shing Mars','cheung_shing_mars'),
    ('Credicor','credicor'),('Ecoline','ecoline')
) as m(nombre, cid)
where q.name = m.nombre;

-- Revisada pero pendiente por mecanica (ver CARDS_LOG.md).
update corporation_review_queue set reviewed = true, corporation_id = null
where name = 'Arcadian Communities';
