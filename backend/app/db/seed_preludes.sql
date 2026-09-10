-- Catalogo de cartas PRELUDE (categoria propia de la expansion: las que se
-- reparten 2 gratis en el setup). Mismo criterio que seed_cards.sql: cada
-- carta verificada contra su scan oficial, sin inventar datos.
--
-- Descubrimiento (2026-09-04): estas 70 cartas nunca habian entrado al
-- pipeline porque enqueue_card_review_queue.py filtraba solo cat=="Project".
-- Ver CARDS_LOG.md, seccion "Prelude: mazo propio".
--
-- Correr despues de schema.sql.

-- Bloque 1 (P01-P24): 22 de 24 cargadas. Ecology Experts (P10) y Eccentric
-- Sponsor (P11) quedan pendientes: las dos exigen JUGAR OTRA CARTA de la mano
-- como parte de su propio efecto, mecanica que el motor no tiene (la misma
-- que bloquea WG Project). Los TAGS se re-verificaron contra los scans: el
-- agente habia descartado el globo terraqueo de Allied Bank y Business
-- Empire como "arte decorativo" cuando es exactamente asi como se dibuja el
-- tag earth.
insert into prelude_cards (id, name, tags, effects) values
    ('allied_bank', 'Allied Bank', '{earth}',
     '{"production_deltas": {"mc_production": 4}, "mc_delta": 3}'::jsonb),
    ('aquifer_turbines', 'Aquifer Turbines', '{power}',
     '{"place_oceans": 1, "production_deltas": {"energy_production": 2}, "mc_delta": -3}'::jsonb),
    ('biofuels', 'Biofuels', '{microbe}',
     '{"production_deltas": {"plant_production": 1, "energy_production": 1}, "resource_deltas": {"plants": 2}}'::jsonb),
    ('biolab', 'Biolab', '{science}',
     '{"production_deltas": {"plant_production": 1}, "draw_cards": 3}'::jsonb),
    ('biosphere_support', 'Biosphere Support', '{plant}',
     '{"production_deltas": {"mc_production": -1, "plant_production": 2}}'::jsonb),
    ('business_empire', 'Business Empire', '{earth}',
     '{"production_deltas": {"mc_production": 6}, "mc_delta": -6}'::jsonb),
    ('dome_farming', 'Dome Farming', '{plant,building}',
     '{"production_deltas": {"plant_production": 1, "mc_production": 2}}'::jsonb),
    ('donation', 'Donation', '{}',
     '{"mc_delta": 21}'::jsonb),
    ('early_settlement', 'Early Settlement', '{city}',
     '{"place_city_tiles": 1, "production_deltas": {"plant_production": 1}}'::jsonb),
    ('experimental_forest', 'Experimental Forest', '{plant}',
     '{"place_greenery": {}, "raise_oxygen_steps": 1,
       "draw_cards_matching_tag": {"tag": "plant", "n": 2}}'::jsonb),
    ('galilean_mining', 'Galilean Mining', '{jovian}',
     '{"production_deltas": {"titanium_production": 2}, "mc_delta": -5}'::jsonb),
    ('great_aquifer', 'Great Aquifer', '{}',
     '{"place_oceans": 2}'::jsonb),
    ('huge_asteroid', 'Huge Asteroid', '{}',
     '{"raise_temperature_steps": 3, "mc_delta": -5}'::jsonb),
    ('io_research_outpost', 'Io Research Outpost', '{science,jovian}',
     '{"production_deltas": {"titanium_production": 1}, "draw_cards": 1}'::jsonb),
    ('loan', 'Loan', '{}',
     '{"production_deltas": {"mc_production": -2}, "mc_delta": 30}'::jsonb),
    ('martian_industries', 'Martian Industries', '{building}',
     '{"production_deltas": {"energy_production": 1, "steel_production": 1}, "mc_delta": 6}'::jsonb),
    ('metal_rich_asteroid', 'Metal-Rich Asteroid', '{}',
     '{"raise_temperature_steps": 1, "resource_deltas": {"titanium": 4, "steel": 4}}'::jsonb),
    ('metals_company', 'Metals Company', '{}',
     '{"production_deltas": {"mc_production": 1, "steel_production": 1, "titanium_production": 1}}'::jsonb),
    ('mining_operations', 'Mining Operations', '{building}',
     '{"production_deltas": {"steel_production": 2}, "resource_deltas": {"steel": 4}}'::jsonb),
    ('mohole', 'Mohole', '{building}',
     '{"production_deltas": {"heat_production": 3}, "resource_deltas": {"heat": 3}}'::jsonb),
    ('mohole_excavation', 'Mohole Excavation', '{building}',
     '{"production_deltas": {"steel_production": 1, "heat_production": 2}, "resource_deltas": {"heat": 2}}'::jsonb),
    ('nitrogen_shipment', 'Nitrogen Shipment', '{}',
     '{"tr_delta": 1, "production_deltas": {"plant_production": 1}, "resource_deltas": {"mc": 5}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

-- Bloque 2 (P25-P35, P43, P44-P67, X39-X78): 26 de 46 cargadas.
-- Piezas nuevas: pasivo "on_tag_played_resource_delta" (generaliza
-- on_tag_played_mc_delta a cualquier recurso), `tag_filter` como LISTA en
-- card_cost_discount_mc, draw_cards_matching_tag acepta lista de specs y de
-- tags, y play_prelude ahora resuelve delegados, colonias, descartes y
-- pasivos.
--
-- CORRECCION del bloque: draw_cards_matching_tag descartaba mal. El FAQ
-- oficial dice "Once the card(s) have been obtained, all other revealed
-- cards are added to the discard pile" -- la implementacion dejaba las
-- reveladas no-coincidentes en el mazo. Afectaba a Experimental Forest,
-- Ishtar Expedition y Stratospheric Expedition, ya cargadas. El fix ademas
-- destrabo Acquired Space Agency.
insert into prelude_cards (id, name, tags, effects) values
    ('orbital_construction_yard', 'Orbital Construction Yard', '{space}',
     '{"production_deltas": {"titanium_production": 1}, "resource_deltas": {"titanium": 4}}'::jsonb),
    ('polar_industries', 'Polar Industries', '{building}',
     '{"place_oceans": 1, "production_deltas": {"heat_production": 2}}'::jsonb),
    ('power_generation', 'Power Generation', '{power}',
     '{"production_deltas": {"energy_production": 3}}'::jsonb),
    ('research_network', 'Research Network', '{wild}',
     '{"draw_cards": 3, "production_deltas": {"mc_production": 1}}'::jsonb),
    ('self_sufficient_settlement', 'Self-Sufficient Settlement', '{city,building}',
     '{"place_city_tiles": 1, "production_deltas": {"mc_production": 2}}'::jsonb),
    ('smelting_plant', 'Smelting Plant', '{building}',
     '{"raise_oxygen_steps": 2, "resource_deltas": {"steel": 5}}'::jsonb),
    ('society_support', 'Society Support', '{}',
     '{"production_deltas": {"mc_production": -1, "plant_production": 1, "energy_production": 1, "heat_production": 1}}'::jsonb),
    ('supplier', 'Supplier', '{power}',
     '{"production_deltas": {"energy_production": 2}, "resource_deltas": {"steel": 4}}'::jsonb),
    ('supply_drop', 'Supply Drop', '{}',
     '{"resource_deltas": {"titanium": 3, "steel": 8, "plants": 3}}'::jsonb),
    ('unmi_contractor', 'UNMI Contractor', '{earth}',
     '{"tr_delta": 3, "draw_cards": 1}'::jsonb),
    ('acquired_space_agency', 'Acquired Space Agency', '{}',
     '{"resource_deltas": {"titanium": 6}, "draw_cards_matching_tag": {"tag": "space", "n": 2}}'::jsonb),
    ('project_eden', 'Project Eden', '{city,plant}',
     '{"place_oceans": 1, "place_city_tiles": 1, "place_greenery": {}, "discard_cards": {"n": 3}}'::jsonb),
    ('recession', 'Recession', '{}',
     '{"mc_delta": 10}'::jsonb),
    ('venus_l1_shade', 'Venus L1 Shade', '{wild}',
     '{"raise_venus_steps": 3}'::jsonb),
    ('rise_to_power', 'Rise to Power', '{}',
     '{"production_deltas": {"mc_production": 3}, "place_delegates": 3}'::jsonb),
    ('space_lanes', 'Space Lanes', '{wild}',
     '{"resource_deltas": {"titanium": 3},
       "passive": {"card_cost_discount_mc": 2, "tag_filter": ["jovian", "earth", "venus"]}}'::jsonb),
    ('planetary_alliance', 'Planetary Alliance', '{earth,jovian,venus}',
     '{"tr_delta": 2, "draw_cards_matching_tag": [{"tag": "jovian", "n": 1}, {"tag": "venus", "n": 1}]}'::jsonb),
    ('soil_bacteria', 'Soil Bacteria', '{microbe}',
     '{"resource_deltas": {"plants": 3}, "draw_cards_matching_tag": {"tag": "microbe", "n": 2},
       "passive": {"on_tag_played_resource_delta": {"matching_tags": ["plant", "microbe"], "resource": "plants", "resource_delta": 1}}}'::jsonb),
    ('old_mining_colony', 'Old Mining Colony', '{space}',
     '{"production_deltas": {"titanium_production": 1}, "build_colony": true, "discard_cards": {"n": 1}}'::jsonb),
    ('corporate_archives', 'Corporate Archives', '{science}',
     '{"resource_deltas": {"mc": 13}, "start_research": {"n": 7}}'::jsonb),
    ('head_start', 'Head Start', '{}',
     '{"resource_deltas": {"steel": 2},
       "resource_delta_per_capped_counter": {"counter": "hand_size", "resource": "mc", "per_unit": 2, "cap": null, "influence_direction": "none"}}'::jsonb),
    ('anti_desertification_techniques', 'Anti-Desertification Techniques', '{plant,building}',
     '{"production_deltas": {"plant_production": 1, "steel_production": 1}, "resource_deltas": {"mc": 3}}'::jsonb),
    ('established_methods', 'Established Methods', '{}',
     '{"resource_deltas": {"mc": 30}}'::jsonb),
    ('giant_solar_collector', 'Giant Solar Collector', '{power,venus}',
     '{"production_deltas": {"energy_production": 2}, "raise_venus_steps": 1}'::jsonb),
    ('strategic_base_planning', 'Strategic Base Planning', '{city,building,venus}',
     '{"resource_deltas": {"mc": -3}, "place_city_tiles": 1, "build_colony": true}'::jsonb),
    ('albedo_plants', 'Albedo Plants', '{plant}',
     '{"production_deltas": {"plant_production": 1}, "resource_deltas": {"plants": 1},
       "passive": {"on_tag_played_resource_delta": {"matching_tags": ["plant"], "resource": "heat", "resource_delta": 3}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

-- Marcado de la cola de revision. Idempotente: se puede re-correr.
update prelude_review_queue q set reviewed = true, prelude_id = m.pid
from (values
    ('P25','orbital_construction_yard'),('P26','polar_industries'),('P27','power_generation'),
    ('P28','research_network'),('P29','self_sufficient_settlement'),('P30','smelting_plant'),
    ('P31','society_support'),('P32','supplier'),('P33','supply_drop'),('P34','unmi_contractor'),
    ('P35','acquired_space_agency'),('P55','old_mining_colony'),('P56','planetary_alliance'),
    ('P58','project_eden'),('P59','recession'),('P60','rise_to_power'),('P61','soil_bacteria'),
    ('P62','space_lanes'),('P66','venus_l1_shade'),('X39','corporate_archives'),('X43','head_start'),
    ('X49','anti_desertification_techniques'),('X54','established_methods'),
    ('X55','giant_solar_collector'),('X65','strategic_base_planning'),('X78','albedo_plants')
) as m(scan, pid)
where q.scan_number = m.scan;

-- Revisadas pero pendientes por mecanica (ver CARDS_LOG.md).
update prelude_review_queue set reviewed = true, prelude_id = null
where scan_number in ('P43','P44','P45','P46','P47','P48','P49','P50','P51','P52','P53','P54',
                      'P57','P63','P64','P65','P67','X40','X41','X42');

-- Bloque 3 (2026-09-08): 4 de los 22 preludes "pendientes" que el motor de
-- hoy YA cubre, mas dos piezas nuevas chicas. Las otras 18 siguen trabadas
-- por mecanicas grandes (mazo de Prelude propio, jugar otra carta de la mano,
-- corporaciones) -- ver "Prelude: mazo propio" en CARDS_LOG.md.
--
-- Ojo con los tags, verificados uno por uno contra los scans: Applied Science
-- lleva el "?" del tag COMODIN (wild), y Floating Trade Hub / Main Belt
-- Asteroids llevan el SOL DORADO sobre negro, que es `space`, no `power`.
insert into prelude_cards (id, name, tags, effects) values
    -- P43: "Add 6 science resources here." + accion: gastar 1 para agregar 1
    -- recurso a CUALQUIER carta QUE YA TENGA recursos, o ganar 1 recurso
    -- estandar (el jugador elige cual: las 6 opciones siguientes).
    ('applied_science', 'Applied Science', '{wild}',
     '{"becomes_active": true, "active_card_resource_type": "science",
       "active_card_starting_resources": 6,
       "action": {"choice": [
         {"cost": {"card_resource": 1}, "gains": {"target_card_resource_delta_allow_self": 1, "target_min_resources": 1}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"mc": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"steel": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"titanium": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"plants": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"energy": 1}}},
         {"cost": {"card_resource": 1}, "gains": {"resource_deltas": {"heat": 1}}}]}}'::jsonb),
    -- P49: sin efecto inmediato. Accion: +2 floaters a CUALQUIER carta (la
    -- propia incluida), o remover X floaters de aca para ganar X de UN
    -- recurso estandar (una opcion por recurso, X via effect_amount).
    ('floating_trade_hub', 'Floating Trade Hub', '{space}',
     '{"becomes_active": true, "active_card_resource_type": "floater",
       "action": {"choice": [
         {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 2}},
         {"convert_card_resource_amount": {"to": "mc"}, "cost": {}, "gains": {}},
         {"convert_card_resource_amount": {"to": "steel"}, "cost": {}, "gains": {}},
         {"convert_card_resource_amount": {"to": "titanium"}, "cost": {}, "gains": {}},
         {"convert_card_resource_amount": {"to": "plants"}, "cost": {}, "gains": {}},
         {"convert_card_resource_amount": {"to": "energy"}, "cost": {}, "gains": {}},
         {"convert_card_resource_amount": {"to": "heat"}, "cost": {}, "gains": {}}]}}'::jsonb),
    -- P53: "Lose 5 M€." + accion: 1 asteroide a CUALQUIER carta. El Effect
    -- ("when gaining an asteroid HERE, gain 1 titanium") es on_card_resource_gained
    -- con own_card_only: paga solo por los asteroides que caen en ESTA carta.
    -- Los VP (1 por cada 2 asteroides) no se modelan: el motor no puntua.
    ('main_belt_asteroids', 'Main Belt Asteroids', '{space}',
     '{"resource_deltas": {"mc": -5}, "becomes_active": true,
       "active_card_resource_type": "asteroid",
       "action": {"cost": {}, "gains": {"target_card_resource_delta_allow_self": 1}},
       "passive": {"on_card_resource_gained": {"resource_type": "asteroid", "own_card_only": true,
                                               "resource_deltas": {"titanium": 1}}}}'::jsonb),
    -- P67: "+2 TR, draw 1 card." + accion: subir 1 parametro global SIN TR ni
    -- ningun otro bonus. Un parametro por opcion de "choice" (effect_choice es
    -- el INDICE de esa lista, un int -- no admite el nombre del parametro).
    -- Si se elige "ocean" hay que pasar ocean_hex_ids: el tile se coloca igual,
    -- pero sin cobrar el bonus del hexagono.
    ('world_government_advisor', 'World Government Advisor', '{earth}',
     '{"tr_delta": 2, "draw_cards": 1, "becomes_active": true,
       "action": {"choice": [
         {"cost": {}, "gains": {"raise_global_parameter_without_bonuses": "temperature"}},
         {"cost": {}, "gains": {"raise_global_parameter_without_bonuses": "oxygen"}},
         {"cost": {}, "gains": {"raise_global_parameter_without_bonuses": "venus"}},
         {"cost": {}, "gains": {"raise_global_parameter_without_bonuses": "ocean"}}]}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

update prelude_review_queue q set reviewed = true, prelude_id = m.pid
from (values
    ('P43','applied_science'),('P49','floating_trade_hub'),
    ('P53','main_belt_asteroids'),('P67','world_government_advisor')
) as m(scan, pid)
where q.scan_number = m.scan;

-- ---------------------------------------------------------------------------
-- Las 4 preludes que esperaban el hook "subio el TR" / "subio produccion"
-- (2026-09-09), destrabadas por el refactor de corporaciones del mismo dia.
-- Tres piezas nuevas en rules_engine.py, todas centralizadas en los puntos
-- unicos ya existentes (_raise_tr / _increase_production), sin cablear nada
-- carta por carta: `on_tr_increased`, `skip_first_tr_gain_per_generation` y
-- `on_action_production_increased_bonus` (esta ultima con snapshot/diff de
-- produccion "antes/despues" en las cuatro vias de accion, mismo patron que
-- on_card_resource_gained). Ver "Corporaciones: mecanicas pendientes
-- resueltas" en CARDS_LOG.md para el detalle de diseño.
insert into prelude_cards (id, name, tags, effects) values
    -- P46: +1 produccion de energia, +2 titanio. Effect: +2 M€ cada vez que
    -- se coloca CUALQUIER colonia (pasivo ya existente desde Poseidon,
    -- bloque 3 de corporaciones -- no hizo falta pieza nueva).
    ('colony_trade_hub', 'Colony Trade Hub', '{space}',
     '{"production_deltas": {"energy_production": 1}, "resource_deltas": {"titanium": 2},
       "passive": {"on_colony_placed": {"resource_deltas": {"mc": 2}}}}'::jsonb),

    -- P57: +5 TR de entrada. Effect: el PRIMER paso de TR que el jugador
    -- ganaria en cada generacion se anula -- no sube, no paga nada de lo que
    -- dependa de subir TR (pieza nueva `skip_first_tr_gain_per_generation`).
    -- Sin tag propio (esquina vacia en el scan).
    ('preservation_program', 'Preservation Program', '{}',
     '{"tr_delta": 5, "passive": {"skip_first_tr_gain_per_generation": true}}'::jsonb),

    -- P63: +5 acero de entrada. Effect: una vez por accion, +2 M€ si subio
    -- CUALQUIER produccion (pieza nueva `on_action_production_increased_bonus`
    -- -- distinta de Manutech, que paga por cada paso, no una vez por accion).
    ('suitable_infrastructure', 'Suitable Infrastructure', '{building}',
     '{"resource_deltas": {"steel": 5},
       "passive": {"on_action_production_increased_bonus": {"mc_delta": 2}}}'::jsonb),

    -- P64: sin bonus de entrada. Effect: +2 M€ por cada paso que sube el TR,
    -- sin importar la fuente (pieza nueva `on_tr_increased`, centralizada en
    -- _raise_tr igual que el resto de las piezas de esta tanda).
    ('terraforming_deal', 'Terraforming Deal', '{earth}',
     '{"passive": {"on_tr_increased": {"mc_delta": 2}}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

update prelude_review_queue q set reviewed = true, prelude_id = m.pid
from (values
    ('P46','colony_trade_hub'),('P57','preservation_program'),
    ('P63','suitable_infrastructure'),('P64','terraforming_deal')
) as m(scan, pid)
where q.scan_number = m.scan;

-- ---------------------------------------------------------------------------
-- Bloque de preludes pendientes (2026-09-09): 10 de 12 cargadas. Quedan
-- Ecology Experts (P10) y Board of Directors (P45) pospuestas -- ver el
-- final de este archivo. Diseñadas con subagentes que verificaron cada scan
-- contra el codigo actual del motor (mucho mas grande que en bloques
-- anteriores: play_prelude ya soporta becomes_active/action, hooks de TR/
-- produccion, colonias, tablero...).
--
-- TAGS: la hoja de contacto atrapo 3 errores en 14 informes -- Atmospheric
-- Enhancers (venus), High Circles (earth) y Nobel Prize (wild, el mismo
-- circulo "?" que ya se habia identificado en Septem Tribus) reportadas
-- como "sin tags" por leer el circulo de expansion en vez del tag real.
--
-- Piezas nuevas, todas chicas:
--   * cost.discard_card + parametro discard_card_id en use_card_action
--     (Focused Organization: descartar 1 carta de la mano como parte del
--     costo de una accion -- motor puro, no necesita catalogo).
--   * raise_production_floor: {"min": N} en apply_card_effect (Industrial
--     Complex: sube cada produccion por debajo de N hasta N, via
--     _increase_production para combinarse con Manutech).
--   * on_become_party_leader + apply_become_party_leader_bonus (Corridors
--     of Power): turmoil.place_delegate es pura y no conoce pasivos, asi
--     que el disparo se detecta en tools.py comparando el leader de antes
--     y despues, en los 4 puntos donde se llama esa funcion.
--   * adjust_all_colony_tracks_in_play: {"delta": N} en play_prelude
--     (Early Colonization: sube TODAS las colonias EN JUEGO, no el
--     catalogo completo de COLONY_DEFS).
--   * _draw_cards_matching_requirement (tools.py), hermana de
--     _draw_cards_matching_tag pero filtrando por `cards.requirements` no
--     vacio, con un modo `party_requirement` para requisitos de partido
--     especificamente (`ruling_or_delegates`) -- compartida por High
--     Circles y Nobel Prize.
--   * reveal_random_preludes: {"n": N} en play_prelude (New Partner):
--     revela N preludes al azar entre las no jugadas, SIN mazo persistente
--     -- el jugador juega la elegida con una llamada normal a play_prelude.
--   * requires_corporation_choice: {"extra_cost_mc": N} en play_prelude
--     (Merger): dispara el MISMO flujo de choose_corporation con un costo
--     extra, en vez de effects genericos -- no rompe "una corporacion por
--     partida", solo cambia el costo de elegirla.
--   * tool nueva play_double_down: copia el efecto DIRECTO (sin passive/
--     action) de otra prelude ya jugada por este jugador y lo reaplica con
--     apply_card_effect -- no hace falta sub-mazo drafteable, el texto real
--     dice "your OTHER prelude", no "the prelude deck".
insert into prelude_cards (id, name, tags, effects) values
    -- P11: descuento de 25 M€ para la proxima carta. Identico patron a
    -- Indentured Workers, sin nada nuevo -- el analisis viejo que pedia la
    -- mecanica de "jugar carta anidada" estaba mal para esta carta puntual.
    ('eccentric_sponsor', 'Eccentric Sponsor', '{}',
     '{"next_card_discount_mc": 25}'::jsonb),

    -- P44: elegis subir temperatura, oxigeno o Venus 2 pasos, y robas 2
    -- cartas con tag venus (ya existe draw_cards_matching_tag, mismo
    -- patron que Stratospheric Expedition).
    ('atmospheric_enhancers', 'Atmospheric Enhancers', '{venus}',
     '{"choice": [
         {"raise_temperature_steps": 2},
         {"raise_oxygen_steps": 2},
         {"raise_venus_steps": 2}],
       "draw_cards_matching_tag": {"tag": "venus", "n": 2}}'::jsonb),

    -- P65: +1 TR y roba 1 carta al jugarla. Effect: +3 M€ por cada paso que
    -- suba Venus, de donde sea (on_venus_raised ya existia, Aphrodite paga
    -- 2 en vez de 3).
    ('venus_contract', 'Venus Contract', '{venus}',
     '{"draw_cards": 1, "tr_delta": 1,
       "passive": {"on_venus_raised": {"mc_delta": 3}}}'::jsonb),

    -- P50: al jugarla, elegis un recurso estandar: roba 1 carta y ganalo (6
    -- opciones). Accion repetible: descartar 1 carta + gastar 1 de un
    -- recurso estandar (elegido) para robar 1 carta y ganar 1 de ESE mismo
    -- recurso -- pieza nueva cost.discard_card.
    ('focused_organization', 'Focused Organization', '{}',
     '{"choice": [
         {"draw_cards": 1, "resource_deltas": {"mc": 1}},
         {"draw_cards": 1, "resource_deltas": {"steel": 1}},
         {"draw_cards": 1, "resource_deltas": {"titanium": 1}},
         {"draw_cards": 1, "resource_deltas": {"plants": 1}},
         {"draw_cards": 1, "resource_deltas": {"energy": 1}},
         {"draw_cards": 1, "resource_deltas": {"heat": 1}}],
       "becomes_active": true,
       "action": {"choice": [
         {"cost": {"discard_card": 1, "mc": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"mc": 1}}},
         {"cost": {"discard_card": 1, "steel": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"steel": 1}}},
         {"cost": {"discard_card": 1, "titanium": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"titanium": 1}}},
         {"cost": {"discard_card": 1, "plants": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"plants": 1}}},
         {"cost": {"discard_card": 1, "energy": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"energy": 1}}},
         {"cost": {"discard_card": 1, "heat": 1}, "gains": {"draw_cards": 1, "resource_deltas": {"heat": 1}}}]}}'::jsonb),

    -- P52: pierde 18 M€, sube a 1 cada produccion que este por debajo
    -- (pieza nueva raise_production_floor).
    ('industrial_complex', 'Industrial Complex', '{building}',
     '{"resource_deltas": {"mc": -18}, "raise_production_floor": {"min": 1}}'::jsonb),

    -- P47: +1 TR y 4 M€ al jugarla. Effect: +1 carta cada vez que el
    -- jugador se vuelve Party Leader de un partido (pieza nueva
    -- on_become_party_leader).
    ('corridors_of_power', 'Corridors of Power', '{earth}',
     '{"tr_delta": 1, "resource_deltas": {"mc": 4},
       "passive": {"on_become_party_leader": {"draw": 1}}}'::jsonb),

    -- P48: +3 energia, coloca 1 colonia (build_colony_id, sin bonus
    -- duplicado) y sube 2 pasos TODAS las colonias en juego (pieza nueva
    -- adjust_all_colony_tracks_in_play, incluye la recien construida).
    ('early_colonization', 'Early Colonization', '{space}',
     '{"resource_deltas": {"energy": 3}, "build_colony": true,
       "adjust_all_colony_tracks_in_play": {"delta": 2}}'::jsonb),

    -- P51: +1 TR, roba 1 carta CON REQUISITO DE PARTIDO (pieza nueva
    -- _draw_cards_matching_requirement con party_requirement), coloca 2
    -- delegados en un mismo partido (ya existia place_delegates), y +1 de
    -- influencia permanente (influence_bonus ya existia).
    ('high_circles', 'High Circles', '{earth}',
     '{"tr_delta": 1, "draw_cards_matching_requirement": {"n": 1, "party": true},
       "place_delegates": 2,
       "passive": {"influence_bonus": 1}}'::jsonb),

    -- P54: +5 M€, roba 2 cartas con CUALQUIER requisito (misma pieza nueva
    -- que High Circles, sin el filtro de partido).
    ('nobel_prize', 'Nobel Prize', '{wild}',
     '{"resource_deltas": {"mc": 5}, "draw_cards_matching_requirement": {"n": 2}}'::jsonb),

    -- X40: sin efecto automatico -- se juega con la tool nueva
    -- play_double_down, que copia el efecto DIRECTO de otra prelude ya
    -- jugada por este jugador.
    ('double_down', 'Double Down', '{}', '{}'::jsonb),

    -- X41: dispara el flujo de choose_corporation con un costo extra de 42
    -- M€ (pieza nueva requires_corporation_choice, resuelta en
    -- play_prelude). No rompe "una corporacion por partida": sigue siendo
    -- UNA sola, solo cambia el costo de elegirla.
    ('merger', 'Merger', '{}',
     '{"requires_corporation_choice": {"extra_cost_mc": 42}}'::jsonb),

    -- X42: +1 produccion de M€, revela 2 preludes al azar entre las no
    -- jugadas (pieza nueva reveal_random_preludes) -- sin mazo persistente,
    -- el jugador juega la elegida con una llamada normal a play_prelude.
    ('new_partner', 'New Partner', '{}',
     '{"production_deltas": {"mc_production": 1}, "reveal_random_preludes": {"n": 2}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

update prelude_review_queue q set reviewed = true, prelude_id = m.pid
from (values
    ('P11','eccentric_sponsor'),('P44','atmospheric_enhancers'),
    ('P65','venus_contract'),('P50','focused_organization'),
    ('P52','industrial_complex'),('P47','corridors_of_power'),
    ('P48','early_colonization'),('P51','high_circles'),
    ('P54','nobel_prize'),('X40','double_down'),
    ('X41','merger'),('X42','new_partner')
) as m(scan, pid)
where q.scan_number = m.scan;

-- ---------------------------------------------------------------------------
-- Las 2 ultimas preludes pendientes, cargadas (2026-09-10): CATALOGO DE
-- PRELUDES COMPLETO, 70 de 70.
--
-- Ambas necesitaban la misma pieza de infraestructura ("jugar una carta
-- dentro de otra jugada"), resuelta una sola vez:
--   * play_card suma dos parametros nuevos: `ignore_global_requirements`
--     (salta los 8 requisitos de parametro global -- temperatura/oxigeno/
--     oceanos/Venus, min y max de cada uno -- el resto se sigue exigiendo,
--     segun el FAQ oficial) y `cost_reduction_mc` (descuento extra antes de
--     calcular el pago, mismo mecanismo que next_card_discount_mc).
--   * play_prelude suma `nested_card_id` + los parametros de pago/eleccion
--     de esa carta: aplica el resto de `effects` de la prelude y lo guarda
--     primero, despues juega la carta anidada con el camino normal de
--     play_card (sale de la mano, paga de verdad, coloca tiles) y devuelve
--     ESA respuesta, no la de la prelude.
--   * use_card_action suma `reveal_prelude` (revela N preludes al azar sin
--     cobrar nada, mismo mecanismo que `reveal_random_preludes` de New
--     Partner pero como GANANCIA de una accion) y `play_revealed_prelude`
--     (despues de que el motor cobre el costo generico de la rama del
--     `choice`, llama a play_prelude.func de verdad sobre `target_card_id`
--     -- Board of Directors "juega" la prelude robada, no copia su efecto
--     como Double Down).
insert into prelude_cards (id, name, tags, effects) values
    -- P10: +1 produccion de plantas, despues jugar una carta de la mano
    -- ignorando los requisitos de parametro global. Sin descuento de costo.
    ('ecology_experts', 'Ecology Experts', '{plant,microbe}',
     '{"production_deltas": {"plant_production": 1},
       "play_card_from_hand": {"ignore_global_requirements": true}}'::jsonb),

    -- P45: +4 director resources. Accion repetible: revelar 1 prelude al
    -- azar (entre las no jugadas por este jugador) y, en una llamada
    -- separada, o no hacer nada con ella (= descartarla, preludes no tienen
    -- pila de descarte en este motor) o pagar 12 M€ + 1 director resource
    -- para jugarla de verdad.
    ('board_of_directors', 'Board of Directors', '{earth}',
     '{"active_card_resource_type": "director", "becomes_active": true,
       "active_card_starting_resources": 4,
       "action": {"choice": [
         {"cost": {}, "gains": {"reveal_prelude": {"n": 1}}},
         {"cost": {"mc": 12, "card_resource": 1}, "gains": {"play_revealed_prelude": true}}]}}'::jsonb)
on conflict (id) do update set
    name = excluded.name, tags = excluded.tags, effects = excluded.effects;

update prelude_review_queue q set reviewed = true, prelude_id = m.pid
from (values ('P10','ecology_experts'), ('P45','board_of_directors')) as m(scan, pid)
where q.scan_number = m.scan;
