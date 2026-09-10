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

-- Arcadian Communities quedo pendiente hasta 2026-09-09, cuando se agrego el
-- marcador "community" al tablero (ver el bloque de mecanicas pendientes al
-- final de este archivo).

-- Bloque 2 (Ecotec -> Manutech): 10 de 10 cargadas. Manutech necesito el
-- hook generico "subio una produccion" (rules_engine._increase_production,
-- ver CARDS_LOG.md) antes de poder cargarse -- ya esta resuelto.
--
-- TAGS: esta tanda fue la peor de todas -- SIETE informes leyeron el circulo
-- del extremo superior derecho como "logo/insignia de la corporacion" cuando
-- es el TAG PROPIO. Verificado en hoja de contacto: el circulo marron con la
-- forma de casa es `building` (Interplanetary Cinematics, Lakefront Resorts,
-- Manutech, y DOS en Mining Guild), el sol dorado sobre negro es `space`
-- (Helion, y DOS en Kuiper Cooperative), el atomo en circulo blanco es
-- `science` (Inventrix) y Factorum lleva `power` + `building`. Que en el
-- bloque 1 varias corporaciones tuvieran esa esquina VACIA (CrediCor, Aridor,
-- Beginner) confirma que no es un adorno fijo de la plantilla.
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 42 M€, +1 produccion de plantas. Effect: al jugar un tag bio
    -- (microbe/plant/animal, incluidos los dos propios), ganar 1 planta O
    -- agregar 1 microbio a CUALQUIER carta (target_any_card, pieza nueva).
    ('ecotec', 'Ecotec', 'Prelude 2', '{microbe,plant}', 42,
     '{"production_deltas": {"plant_production": 1},
       "passive": {"on_any_tag_played_choice": {
           "matching_tags": ["microbe", "plant", "animal"],
           "add_resource_choice": {"resource_delta": 1, "target_any_card": true},
           "gain_resource_choice": {"resource": "plants", "amount": 1}}}}'::jsonb),

    -- 37 M€, +1 produccion de acero. Accion: +1 produccion de energia SOLO si
    -- el jugador tiene 0 de energia en stock (`requires_zero_resource`, pieza
    -- nueva), o pagar 3 M€ para robar una carta con tag building.
    ('factorum', 'Factorum', 'Promo', '{power,building}', 37,
     '{"production_deltas": {"steel_production": 1}, "becomes_active": true,
       "action": {"choice": [
         {"requires_zero_resource": "energy", "cost": {},
          "gains": {"production_deltas": {"energy_production": 1}}},
         {"cost": {"mc": 3}, "gains": {"draw_cards_matching_tag": {"tag": "building", "n": 1}}}]}}'::jsonb),

    -- 42 M€, +3 produccion de calor. Effect: el calor paga cartas como si
    -- fuera M€ (1:1). Es `stock_resource_payment` SIN required_tag: vale para
    -- cualquier carta, no solo para un tag (Martian Lumber Corp si lo filtra).
    ('helion', 'Helion', 'Base', '{space}', 42,
     '{"production_deltas": {"heat_production": 3},
       "passive": {"stock_resource_payment": {"resource": "heat", "value_mc": 1}}}'::jsonb),

    -- 30 M€ y 20 de acero en stock. Effect: +2 M€ por evento jugado (mismo
    -- pasivo que Media Group).
    ('interplanetary_cinematics', 'Interplanetary Cinematics', 'Base', '{building}', 30,
     '{"resource_deltas": {"steel": 20},
       "passive": {"on_event_played": {"mc_delta": 2}}}'::jsonb),

    -- 45 M€ y roba 3 cartas. Effect: los requisitos de temperatura/oxigeno/
    -- oceanos se relajan 2 pasos (idem Adaptation Technology).
    ('inventrix', 'Inventrix', 'Base', '{science}', 45,
     '{"draw_cards": 3, "passive": {"global_requirements_tolerance_steps": 2}}'::jsonb),

    -- 33 M€, +1 produccion de titanio. Guarda asteroides. Accion: +1 asteroide
    -- por cada tag space (pieza nueva `card_resource_delta_per_tag`). Effect:
    -- cada asteroide vale 1 M€ al pagar los proyectos Asteroid y Aquifer
    -- (pieza nueva `standard_project_card_resource_payment`).
    ('kuiper_cooperative', 'Kuiper Cooperative', 'Promo', '{space,space}', 33,
     '{"production_deltas": {"titanium_production": 1}, "becomes_active": true,
       "active_card_resource_type": "asteroid",
       "action": {"cost": {}, "gains": {"card_resource_delta_per_tag": {"tag": "space", "per_tag": 1}}},
       "passive": {"standard_project_card_resource_payment": {
           "resource_type": "asteroid", "applies_to": ["asteroid", "aquifer"], "value_mc": 1}}}'::jsonb),

    -- 54 M€. Dos efectos: +1 produccion de M€ cada vez que se coloca CUALQUIER
    -- oceano (on_ocean_placed ahora acepta production_deltas), y el bonus por
    -- colocar adyacente a oceanos pasa de 2 a 3 M€ (`ocean_adjacency_bonus_mc`).
    ('lakefront_resorts', 'Lakefront Resorts', 'Turmoil', '{building}', 54,
     '{"passive": {"on_ocean_placed": {"production_deltas": {"mc_production": 1}},
                   "ocean_adjacency_bonus_mc": 3}}'::jsonb),

    -- 30 M€, 5 de acero, +1 produccion de acero. Effect: +1 produccion de
    -- acero cada vez que coloca un tile sobre un hex con bonus de acero o
    -- titanio (pieza nueva `on_hex_bonus_tile_placed`, enganchada en el unico
    -- punto por el que pasan las cuatro vias de colocacion).
    ('mining_guild', 'Mining Guild', 'Base', '{building,building}', 30,
     '{"production_deltas": {"steel_production": 1}, "resource_deltas": {"steel": 5},
       "passive": {"on_hex_bonus_tile_placed": {"matching_resources": ["steel", "titanium"],
                                                "production_deltas": {"steel_production": 1}}}}'::jsonb),

    -- 48 M€, +4 produccion de M€. El resto de la carta es MULTIJUGADOR y en
    -- single-player resuelve a 0, no es mecanica faltante: "all opponents
    -- decrease their M€ production 2 steps" (no hay oponentes) y el Effect
    -- "when a player causes another player to lose production or resources,
    -- pay 3 M€ to the victim" (nunca se dispara).
    ('mons_insurance', 'Mons Insurance', 'Promo', '{}', 48,
     '{"production_deltas": {"mc_production": 4}}'::jsonb),

    -- 35 M€, +1 produccion de acero. Effect: "for each step you increase the
    -- production of a resource, including this, you also gain that resource"
    -- -- texto literal, sin excepcion de M€ (pasivo nuevo
    -- `on_production_increased`, ver rules_engine._increase_production).
    ('manutech', 'Manutech', 'Promo', '{building}', 35,
     '{"production_deltas": {"steel_production": 1},
       "passive": {"on_production_increased": true}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Ecotec','ecotec'),('Factorum','factorum'),('Helion','helion'),
    ('Interplanetary Cinematics','interplanetary_cinematics'),('Inventrix','inventrix'),
    ('Kuiper Cooperative','kuiper_cooperative'),('Lakefront Resorts','lakefront_resorts'),
    ('Mining Guild','mining_guild'),('Mons Insurance','mons_insurance'),
    ('Manutech','manutech')
) as m(nombre, cid)
where q.name = m.nombre;

-- ---------------------------------------------------------------------------
-- Bloque 3 (Morning Star Inc -> Pristar): 8 de 10 cargadas.
--
-- TAGS: la hoja de contacto (scripts/tag_contact_sheet.py, variante apaisada
-- para corporaciones) atrapo UN error en 10 informes -- Pharmacy Union tiene
-- DOS tags `microbe`, no `science`. El resto verificado: Polyphemos, Poseidon
-- y Pristar tienen la esquina VACIA (sin tags), Nirgal lleva TRES
-- (`power`+`plant`+`building`).
--
-- Piezas nuevas del bloque: `venus_requirements_tolerance_steps` (Morning
-- Star, acotado a Venus a diferencia del pasivo general),
-- `on_event_played.resource_deltas` (Palladin), `on_tag_played_draw_cards`
-- (Point Luna), `research_cost_delta_mc` (Polyphemos) y `on_colony_placed`
-- (Poseidon). Morning Star y Splice NO necesitaron pieza nueva para "revelar
-- hasta juntar N cartas de un tag": `draw_cards_matching_tag` ya hacia
-- exactamente eso (revela de a una y descarta las que no matchean).
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 50 M€. Setup: revelar hasta juntar 3 cartas con tag venus y tomarlas.
    -- Effect: los requisitos de VENUS (solo esos) se relajan 2 pasos.
    ('morning_star_inc', 'Morning Star Inc', 'Venus Next', '{venus}', 50,
     '{"draw_cards_matching_tag": {"tag": "venus", "n": 3},
       "passive": {"venus_requirements_tolerance_steps": 2}}'::jsonb),

    -- 30 M€, +1 produccion de energia, plantas y acero. Su Effect ("awards and
    -- milestones always cost 0 M€ for you") NO se modela: milestones/awards
    -- estan fuera de alcance del MVP entero (CLAUDE.md seccion 7), no es una
    -- pieza de vocabulario que falte.
    ('nirgal_enterprises', 'Nirgal Enterprises', 'Prelude 2', '{power,plant,building}', 30,
     '{"production_deltas": {"energy_production": 1, "plant_production": 1, "steel_production": 1}}'::jsonb),

    -- 36 M€ y 5 de titanio. Effect: +1 titanio al jugar un evento con tag
    -- space. Accion: 2 titanio -> +1 paso de temperatura.
    ('palladin_shipping', 'Palladin Shipping', 'Prelude 2', '{space}', 36,
     '{"resource_deltas": {"titanium": 5}, "becomes_active": true,
       "passive": {"on_event_played": {"resource_deltas": {"titanium": 1}, "tag_filter": "space"}},
       "action": {"cost": {"titanium": 2}, "gains": {"raise_temperature_steps": 1}}}'::jsonb),

    -- 47 M€. Su Effect ("each new adjacency between your tile and an
    -- OPPONENT's tile") depende de tiles de oponentes: en un jugador nunca se
    -- dispara, mismo criterio que Mons Insurance/Toll Station. La primera
    -- accion (greenery gratis + oxigeno) tampoco entra en `effects`:
    -- choose_corporation no coloca tiles (no recibe hex_id), asi que el
    -- jugador la resuelve con la tool de colocacion como cualquier greenery.
    ('philares', 'Philares', 'Promo', '{building}', 47, '{}'::jsonb),

    -- 23 M€ y 10 de titanio. Effect: cada titanio vale 1 M€ extra al pagar
    -- cartas (mismo mecanismo que Advanced Alloys).
    ('phobolog', 'Phobolog', 'Base', '{space}', 23,
     '{"resource_deltas": {"titanium": 10},
       "passive": {"titanium_value_bonus": 1}}'::jsonb),

    -- 38 M€, +1 produccion de titanio. Effect: robar 1 carta por cada tag
    -- earth jugado (automatico, no una eleccion).
    ('point_luna', 'Point Luna', 'Prelude', '{earth,space}', 38,
     '{"production_deltas": {"titanium_production": 1},
       "passive": {"on_tag_played_draw_cards": {"matching_tags": ["earth"], "cards": 1}}}'::jsonb),

    -- 50 M€, +5 produccion de M€, 5 de titanio. Effect: comprar cartas en la
    -- investigacion cuesta 5 M€ en vez de 3 (`research_cost_delta_mc` +2). La
    -- clausula "including the starting hand" no cambia nada en este motor:
    -- deal_starting_hand reparte la mano inicial GRATIS.
    ('polyphemos', 'Polyphemos', 'Colonies', '{}', 50,
     '{"production_deltas": {"mc_production": 5}, "resource_deltas": {"titanium": 5},
       "passive": {"research_cost_delta_mc": 2}}'::jsonb),

    -- 45 M€. Effect: +1 produccion de M€ cada vez que se coloca CUALQUIER
    -- colonia (pieza nueva `on_colony_placed`). La colonia gratis de su
    -- primera accion se resuelve con la tool build_colony, que ya dispara el
    -- pasivo -- por eso el "including this" del texto sale solo.
    ('poseidon', 'Poseidon', 'Colonies', '{}', 45,
     '{"passive": {"on_colony_placed": {"production_deltas": {"mc_production": 1}}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Morning Star Inc','morning_star_inc'),('Nirgal Enterprises','nirgal_enterprises'),
    ('Palladin Shipping','palladin_shipping'),('Philares','philares'),
    ('Phobolog','phobolog'),('Point Luna','point_luna'),
    ('Polyphemos','polyphemos'),('Poseidon','poseidon')
) as m(nombre, cid)
where q.name = m.nombre;

-- Revisadas pero pendientes por mecanica (ver CARDS_LOG.md):
--   * Pharmacy Union: rama condicional segun los recursos de la propia carta
--     + perdida de M€ "o lo maximo posible" + mover la carta a la pila de
--     eventos. Tres piezas, ninguna existente.
--   * Pristar: "during production phase, if you did not get TR so far this
--     generation" -- necesita el hook "subio el TR", la misma familia que
--     esperan Preservation Program / Suitable Infrastructure / Terraforming
--     Deal de las preludes pendientes.
-- Las dos se cargaron el 2026-09-09 (ver el bloque de mecanicas pendientes al
-- final de este archivo): Pristar con el hook "subio el TR" y Pharmacy Union
-- con la rama condicional por recursos propios + retire_card_as_event.

-- ---------------------------------------------------------------------------
-- Bloque 4 (Recyclon -> TerraLabs Research): 8 de 10 cargadas.
--
-- TAGS: 3 errores en 10 informes, los tres por iconos que faltaban en la
-- leyenda del prompt: el planeta rayado naranja (JUPITER) es `jovian` --
-- Saturn Systems (reportado `space`) y Stormcraft (reportado "decorativo,
-- sin tags") -- y el circulo gris con skyline de EDIFICIOS es `city`, no
-- `building` (Spire). Leccion para la proxima tanda: la leyenda del prompt
-- tiene que incluir jovian y city, no solo los seis basicos.
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 38 M€, +1 produccion de acero. Guarda microbios. Effect: +1 microbio al
    -- jugar un tag building. Accion: gastar 2 microbios -> +1 produccion de
    -- plantas (la carta ofrece las dos mitades como eleccion del jugador).
    ('recyclon', 'Recyclon', 'Promo', '{microbe,building}', 38,
     '{"production_deltas": {"steel_production": 1}, "becomes_active": true,
       "active_card_resource_type": "microbe",
       "passive": {"on_tag_played_add_resource": {"matching_tags": ["building"], "resource_delta": 1}},
       "action": {"cost": {"card_resource": 2},
                  "gains": {"production_deltas": {"plant_production": 1}}}}'::jsonb),

    -- 47 M€. Accion: 4 M€ -> +1 paso en la produccion mas baja, a eleccion
    -- del jugador (el motor no valida cual es la minima -- misma confianza
    -- que en el resto de las elecciones, ver CARDS_LOG.md).
    ('robinson_industries', 'Robinson Industries', 'Prelude', '{}', 47,
     '{"becomes_active": true,
       "action": {"cost": {"mc": 4}, "choice": [
         {"gains": {"production_deltas": {"mc_production": 1}}},
         {"gains": {"production_deltas": {"steel_production": 1}}},
         {"gains": {"production_deltas": {"titanium_production": 1}}},
         {"gains": {"production_deltas": {"plant_production": 1}}},
         {"gains": {"production_deltas": {"energy_production": 1}}},
         {"gains": {"production_deltas": {"heat_production": 1}}}]}}'::jsonb),

    -- 42 M€, +1 produccion de titanio. Effect: +1 produccion de M€ por cada
    -- tag jovian que entre en juego (pieza nueva
    -- `on_tag_played_production_delta`; el tag propio de la corp ya cuenta).
    ('saturn_systems', 'Saturn Systems', 'Corporate Era', '{jovian}', 42,
     '{"production_deltas": {"titanium_production": 1},
       "passive": {"on_tag_played_production_delta": {
           "matching_tags": ["jovian"], "production": "mc_production", "production_delta": 1}}}'::jsonb),

    -- 36 M€, tag comodin. Accion: 2 M€ por cada partido donde tenga al menos
    -- 1 delegado (pieza nueva `mc_per_party_with_delegate`, resuelta en
    -- tools.py porque contar delegados PROPIOS necesita el player_id).
    ('septem_tribus', 'Septem Tribus', 'Turmoil', '{wild}', 36,
     '{"becomes_active": true,
       "action": {"cost": {},
                  "gains": {"mc_per_party_with_delegate": {"per_party": 2, "min_delegates": 1}}}}'::jsonb),

    -- 50 M€. Setup: robar 4 cartas y descartar 3. Guarda recursos "science".
    -- Effects: +1 science al jugar una carta con AL MENOS 2 tags (pieza nueva
    -- `on_card_played_min_tags_add_resource`), y esos science pagan proyectos
    -- estandar a 2 M€ cada uno (mismo mecanismo que Kuiper Cooperative).
    ('spire', 'Spire', 'Prelude 2', '{city,earth}', 50,
     '{"draw_cards": 4, "discard_cards": {"n": 3}, "becomes_active": true,
       "active_card_resource_type": "science",
       "passive": {"on_card_played_min_tags_add_resource": {"min_tags": 2, "resource_delta": 1},
                   "standard_project_card_resource_payment": {
                       "resource_type": "science",
                       "applies_to": ["power_plant", "asteroid", "aquifer", "greenery", "city"],
                       "value_mc": 2}}}'::jsonb),

    -- 44 M€. Setup: revelar hasta encontrar una carta con tag microbe y
    -- tomarla. Effect: al jugar un tag microbe, el jugador elige entre +2 M€
    -- o +1 microbio a esa carta, y ADEMAS gana 2 M€ siempre (en un jugador,
    -- "that player" y "you" son la misma persona: los dos pasivos se suman).
    ('splice', 'Splice', 'Promo', '{microbe}', 44,
     '{"draw_cards_matching_tag": {"tag": "microbe", "n": 1},
       "passive": {"on_any_tag_played_choice": {
                       "matching_tags": ["microbe"],
                       "add_resource_choice": {"resource_delta": 1},
                       "gain_resource_choice": {"resource": "mc", "amount": 2}},
                   "on_tag_played_resource_delta": {
                       "matching_tags": ["microbe"], "resource": "mc", "resource_delta": 2}}}'::jsonb),

    -- 60 M€. Effect: las cartas con tag earth cuestan 3 M€ menos.
    ('teractor', 'Teractor', 'Corporate Era', '{earth}', 60,
     '{"passive": {"card_cost_discount_mc": 3, "tag_filter": "earth"}}'::jsonb),

    -- 14 M€ y TR 19 (arranca -1). Effect: comprar cartas cuesta 1 M€ en vez
    -- de 3 (`research_cost_delta_mc` -2, la contracara de Polyphemos).
    ('terralabs_research', 'TerraLabs Research', 'Turmoil', '{science,earth}', 14,
     '{"tr_delta": -1, "passive": {"research_cost_delta_mc": -2}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Recyclon','recyclon'),('Robinson Industries','robinson_industries'),
    ('Saturn Systems','saturn_systems'),('Septem Tribus','septem_tribus'),
    ('Spire','spire'),('Splice','splice'),('Teractor','teractor'),
    ('TerraLabs Research','terralabs_research')
) as m(nombre, cid)
where q.name = m.nombre;

-- Revisadas pero pendientes por mecanica (ver CARDS_LOG.md):
--   * Sagitta Frontier Services: robar una carta SIN NINGUN tag (filtro por
--     cantidad de tags, no por tag) + pagar segun cuantos tags trae la carta
--     jugada (0 o exactamente 1).
--   * Stormcraft Incorporated: "floaters on this card may be used as 2 heat
--     each" -- una carta activa que funciona como stock de CALOR en cualquier
--     punto donde el motor gaste calor (proyecto estandar, conversion 8->TR),
--     no solo para pagar cartas como card_resource_payment.
-- Las dos se cargaron el 2026-09-09 (ver el bloque de mecanicas pendientes al
-- final de este archivo).

-- ---------------------------------------------------------------------------
-- Bloque 5 (Tharsis Republic -> Vitor): 6 de 8 cargadas. Cierra la cola.
--
-- TAGS: 2 errores en 8 informes, otra vez el mismo: el GLOBO TERRAQUEO
-- (`earth`) leido como "logo de FryxGames" o "banner de la expansion" en
-- United Nations Mars Initiative y Valley Trust. Las dos SI tienen tag earth.
-- Con esto, el globo terraqueo ya es el icono que mas veces se leyo mal en
-- todo el pipeline: vale la pena nombrarlo explicitamente en el prompt.
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 40 M€. Dos efectos sobre ciudades: +1 produccion de M€ cuando se coloca
    -- CUALQUIER ciudad en Marte, y +3 M€ cuando la coloca el jugador. En un
    -- jugador los dos disparadores coinciden (ver apply_city_placed_bonuses).
    -- Su "first action: place a city tile" no va en `effects`:
    -- choose_corporation no coloca tiles, la resuelve el jugador aparte.
    ('tharsis_republic', 'Tharsis Republic', 'Base', '{building}', 40,
     '{"passive": {"on_city_tile_placed_production_delta": {"production": "mc_production", "per_tile": 1},
                   "on_city_tile_placed_resource_delta": {"mc": 3}}}'::jsonb),

    -- 48 M€, +1 produccion de energia. Effect: -3 M€ tanto en las cartas con
    -- tag power como en el PROYECTO ESTANDAR power plant (pieza nueva
    -- `standard_project_discount_mc` para la segunda mitad).
    ('thorgate', 'Thorgate', 'Base', '{power}', 48,
     '{"production_deltas": {"energy_production": 1},
       "passive": {"card_cost_discount_mc": 3, "tag_filter": "power",
                   "standard_project_discount_mc": {"projects": ["power_plant"], "amount": 3}}}'::jsonb),

    -- 42 M€, +1 produccion de energia. Accion: gastar X energia para robar X
    -- cartas y quedarse con las que pague -- mismo patron que Hi-Tech Lab
    -- (costo variable "effect_amount" + start_research por la misma X).
    ('tycho_magnetics', 'Tycho Magnetics', 'Promo', '{power,science}', 42,
     '{"production_deltas": {"energy_production": 1}, "becomes_active": true,
       "action": {"cost": {"energy": "effect_amount"},
                  "gains": {"start_research": {"n": "effect_amount"}}}}'::jsonb),

    -- 40 M€, +1 produccion de acero y de titanio. Accion: bajar una
    -- produccion a eleccion 1 paso para ganar 4 de ese recurso (pieza nueva
    -- `cost.production_delta`: pagar con produccion, no con stock).
    ('utopia_invest', 'Utopia Invest', 'Turmoil', '{building}', 40,
     '{"production_deltas": {"steel_production": 1, "titanium_production": 1},
       "becomes_active": true,
       "action": {"choice": [
         {"cost": {"production_delta": {"mc_production": 1}}, "gains": {"resource_deltas": {"mc": 4}}},
         {"cost": {"production_delta": {"steel_production": 1}}, "gains": {"resource_deltas": {"steel": 4}}},
         {"cost": {"production_delta": {"titanium_production": 1}}, "gains": {"resource_deltas": {"titanium": 4}}},
         {"cost": {"production_delta": {"plant_production": 1}}, "gains": {"resource_deltas": {"plants": 4}}},
         {"cost": {"production_delta": {"energy_production": 1}}, "gains": {"resource_deltas": {"energy": 4}}},
         {"cost": {"production_delta": {"heat_production": 1}}, "gains": {"resource_deltas": {"heat": 4}}}]}}'::jsonb),

    -- 37 M€. Effect: -2 M€ en las cartas con tag science. Su "first action:
    -- draw 3 Prelude cards and play one" NO se modela: el sorteo/eleccion de
    -- preludes del setup sigue sin existir (ver CARDS_LOG.md, "Prelude").
    ('valley_trust', 'Valley Trust', 'Prelude', '{earth}', 37,
     '{"passive": {"card_cost_discount_mc": 2, "tag_filter": "science"}}'::jsonb),

    -- 48 M€. Accion: reusar la accion de una carta activa ya usada esta
    -- generacion -- exactamente `reset_card_action_used`, que ya existia
    -- para Project Inspection (X02). Sin pieza nueva.
    ('viron', 'Viron', 'Venus Next', '{microbe}', 48,
     '{"becomes_active": true,
       "action": {"cost": {}, "gains": {"reset_card_action_used": true}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Tharsis Republic','tharsis_republic'),('Thorgate','thorgate'),
    ('Tycho Magnetics','tycho_magnetics'),('Utopia Invest','utopia_invest'),
    ('Valley Trust','valley_trust'),('Viron','viron')
) as m(nombre, cid)
where q.name = m.nombre;

-- Revisadas pero pendientes por mecanica (ver CARDS_LOG.md):
--   * United Nations Mars Initiative: "if your TR was raised this
--     generation, pay 3 M€ to raise it 1 step more" -- el mismo hook "subio
--     el TR" que espera Pristar y las 3 preludes pendientes. Cuarta carta de
--     la familia: cuando se diseñe, resuelve todas juntas.
--   * Vitor: "when you play a card with a NON-NEGATIVE VP icon, gain 3 M€".
--     No es solo vocabulario faltante: NINGUNA carta del catalogo tiene
--     cargado su VP impreso, asi que el pasivo no tendria de donde leerlo.
--     Necesita un retrofit de `vp_icon` en el catalogo entero primero.
-- United Nations Mars Initiative se cargo el 2026-09-09 con el hook "subio el
-- TR" (ver el bloque final). Vitor se cargo tambien ese dia (ver el final de
-- este archivo): no hacia falta un retrofit de vp_icon en las 408 cartas,
-- alcanzo con una lista corta y verificada de las pocas con VP NEGATIVO.

-- ---------------------------------------------------------------------------
-- Mecanicas pendientes resueltas (2026-09-09): 6 de las 7 corporaciones que
-- estaban trabadas por falta de mecanica. Solo queda Vitor.
--
-- Las cinco piezas nuevas, en orden de valor:
--   1. `_raise_tr` + `tr_raised_this_generation`: punto UNICO por el que pasa
--      todo cambio de TR del motor (11 sitios centralizados), analogo a lo que
--      `_increase_production` hizo por Manutech. Destraba Pristar y United
--      Nations Mars Initiative -- y las 3 preludes que esperaban lo mismo.
--   2. `on_tag_played_conditional_by_own_resource` + tool retire_card_as_event
--      (Pharmacy Union).
--   3. `on_card_played_tag_count_resource_delta` + `draw_cards_matching_tag`
--      con tag null = "carta SIN tags" (Sagitta Frontier Services).
--   4. `card_resource_as_heat` + parametro `card_resources_as_heat` en las dos
--      tools que gastan calor (Stormcraft Incorporated).
--   5. TileType "community" + place_community + `on_build_on_own_community`
--      (Arcadian Communities).
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 40 M€ y 10 de acero. Coloca marcadores de "community" que reservan
    -- hexagonos; construir sobre uno propio da 3 M€. El marcador NO es un
    -- tile: no lo encuentra ningun conteo y no impide construir ahi (al reves
    -- que el de nomads). El primero va en el setup sin exigir adyacencia
    -- (tool place_community con first_action=true); los demas, con la accion.
    -- Su accion NO va en `effects.action`: colocar el marcador necesita un
    -- hex_id, y las colocaciones en el mapa se piden siempre con su propia
    -- tool (place_community), igual que el greenery de Philares o la ciudad
    -- de Tharsis Republic. `effects` solo lleva lo que resuelve el motor.
    ('arcadian_communities', 'Arcadian Communities', 'Promo', '{}', 40,
     '{"resource_deltas": {"steel": 10},
       "passive": {"on_build_on_own_community": {"mc_delta": 3}}}'::jsonb),

    -- 54 M€ y roba una carta con tag science. Guarda "diseases". Dos mitades:
    -- al jugar CUALQUIER tag microbe (incluidos sus 2 propios, que se
    -- autodisparan al elegirla) suma 1 disease y pierde 4 M€ -- o lo que
    -- tenga, porque on_tag_played_resource_delta ya cappea en 0 sin lanzar
    -- error. Al jugar un tag science, saca 1 disease y sube 1 TR; si no le
    -- queda ninguno, el jugador PUEDE retirarla con la tool
    -- retire_card_as_event y llevarse 3 TR (esa rama es opcional, por eso no
    -- se dispara sola).
    ('pharmacy_union', 'Pharmacy Union', 'Promo', '{microbe,microbe}', 54,
     '{"draw_cards_matching_tag": {"tag": "science", "n": 1},
       "becomes_active": true, "active_card_resource_type": "disease",
       "passive": {"on_tag_played_add_resource": {"matching_tags": ["microbe"], "resource_delta": 1},
                   "on_tag_played_resource_delta": {"matching_tags": ["microbe"],
                                                    "resource": "mc", "resource_delta": -4},
                   "on_tag_played_conditional_by_own_resource": {
                       "matching_tags": ["science"], "resource_threshold": 1,
                       "if_at_least": {"card_resource_delta": -1, "tr_delta": 1},
                       "if_below": {"tr_delta": 3}}}}'::jsonb),

    -- 53 M€ y arranca en TR 18 (tr_delta -2 sobre el TR_START de 20). Guarda
    -- "preservation". En cada fase de produccion, si NO subio el TR en esa
    -- generacion, suma 1 preservation y 6 M€ (el "1 VP per preservation
    -- resource" no se modela: el motor no puntua).
    ('pristar', 'Pristar', 'Turmoil', '{}', 53,
     '{"tr_delta": -2, "becomes_active": true,
       "active_card_resource_type": "preservation",
       "passive": {"on_production_phase_if_tr_not_raised": {"mc_delta": 6,
                                                            "card_resource_delta": 1}}}'::jsonb),

    -- 31 M€, +1 produccion de energia y +2 de M€, y roba una carta SIN NINGUN
    -- tag (draw_cards_matching_tag con tag null). Effect: 4 M€ por cada carta
    -- sin tags jugada -- incluida ella misma al elegirla, que no tiene
    -- ninguno -- y 1 M€ por cada carta de EXACTAMENTE 1 tag.
    ('sagitta_frontier_services', 'Sagitta Frontier Services', 'Prelude 2', '{}', 31,
     '{"production_deltas": {"energy_production": 1, "mc_production": 2},
       "draw_cards_matching_tag": {"tag": null, "n": 1},
       "passive": {"on_card_played_tag_count_resource_delta": [
           {"count": 0, "resource": "mc", "resource_delta": 4},
           {"count": 1, "resource": "mc", "resource_delta": 1}]}}'::jsonb),

    -- 48 M€. Guarda floaters. Accion: 1 floater a CUALQUIER carta (igual que
    -- Celestic). Effect: cada floater de ESTA carta vale 2 de calor, que se
    -- gasta por el parametro `card_resources_as_heat` de convert_resources y
    -- use_card_action -- los dos unicos sumideros de calor del motor.
    ('stormcraft_incorporated', 'Stormcraft Incorporated', 'Colonies', '{jovian}', 48,
     '{"becomes_active": true, "active_card_resource_type": "floater",
       "passive": {"card_resource_as_heat": {"resource_type": "floater", "heat_value": 2}},
       "action": {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}}}'::jsonb),

    -- 40 M€. Accion: si YA subiste el TR en esta generacion, pagar 3 M€ para
    -- subirlo 1 paso mas (requisito `requires_tr_raised_this_generation`).
    ('united_nations_mars_initiative', 'United Nations Mars Initiative', 'Base', '{earth}', 40,
     '{"becomes_active": true,
       "action": {"requirements": {"requires_tr_raised_this_generation": true},
                  "cost": {"mc": 3}, "gains": {"tr_delta": 1}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values
    ('Arcadian Communities','arcadian_communities'),('Pharmacy Union','pharmacy_union'),
    ('Pristar','pristar'),('Sagitta Frontier Services','sagitta_frontier_services'),
    ('Stormcraft Incorporated','stormcraft_incorporated'),
    ('United Nations Mars Initiative','united_nations_mars_initiative')
) as m(nombre, cid)
where q.name = m.nombre;

-- Unica corporacion que sigue pendiente: Vitor ("when you play a card with a
-- NON-NEGATIVE VP icon, gain 3 M€"). CARGADA el 2026-09-09 (ver el bloque
-- final de este archivo): no hizo falta un retrofit de vp_icon en las 408
-- cartas -- alcanzo con una lista corta y verificada de las pocas con VP
-- NEGATIVO impreso (excluded_card_ids), no con cargar el VP de todo el
-- catalogo.


-- ---------------------------------------------------------------------------
-- Vitor, cargada (2026-09-09): la ultima corporacion. 48 de 48.
--
-- Pieza nueva `on_card_played_with_vp_icon` (rules_engine.py): en vez de
-- trackear el VP de las 408 cartas del catalogo, usa una lista CORTA y
-- verificada contra el scan de las pocas con VP NEGATIVO impreso --
-- confirmadas para este catalogo: nuclear_zone (-2 VP fija), bribed_committee
-- (-2 VP fija) y vermin (-1 VP condicional por ciudad, con >=10 animales
-- aca). No es necesariamente exhaustiva: se amplia si aparece otra carta con
-- VP negativo confirmada contra su scan. Ver "Vitor" en CARDS_LOG.md.
insert into corporation_cards (id, name, expansion, tags, starting_mc, effects) values
    -- 45 M€. Su Effect ("fund an award for free") sigue fuera de alcance:
    -- milestones/awards no estan modelados en el MVP (CLAUDE.md seccion 7).
    ('vitor', 'Vitor', 'Prelude', '{earth}', 45,
     '{"passive": {"on_card_played_with_vp_icon": {
         "mc_delta": 3,
         "excluded_card_ids": ["nuclear_zone", "bribed_committee", "vermin"]}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, expansion = excluded.expansion, tags = excluded.tags,
    starting_mc = excluded.starting_mc, effects = excluded.effects;

update corporation_review_queue q set reviewed = true, corporation_id = m.cid
from (values ('Vitor','vitor')) as m(nombre, cid)
where q.name = m.nombre;
