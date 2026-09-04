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
