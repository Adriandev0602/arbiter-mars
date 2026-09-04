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
