-- Esquema de Supabase (Postgres) para Terraforming Mars.
-- Refleja el modelo de datos real del juego: recursos + produccion por
-- jugador, parametros globales compartidos, catalogo de cartas y log de
-- transacciones para auditar cada jugada.

-- create table if not exists no agrega columnas a una tabla que ya existe --
-- si corriste schema.sql antes de que existiera una columna nueva, este
-- ALTER la agrega sin tocar los datos existentes.
do $$ begin
    alter table if exists players add column if not exists active_cards jsonb not null default '{}'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists city_tiles_placed integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists tags_played jsonb not null default '{}'::jsonb;
    alter table if exists players add column if not exists passive_effects jsonb not null default '[]'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists cards add column if not exists is_event boolean not null default false;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists deck jsonb not null default '[]'::jsonb;
    alter table if exists players add column if not exists hand jsonb not null default '[]'::jsonb;
    alter table if exists players add column if not exists pending_research jsonb not null default '[]'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists board jsonb not null default '{}'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists played_cards jsonb not null default '[]'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists events_played integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists pending_mc_discount integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists pending_requirement_tolerance_steps integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists reserved_cards jsonb not null default '{}'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists venus integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists zero_tag_cards_played integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists colonies_owned jsonb not null default '[]'::jsonb;
    alter table if exists players add column if not exists trade_fleets integer not null default 1;
    alter table if exists players add column if not exists trade_fleets_used integer not null default 0;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists colonies jsonb not null default '{}'::jsonb;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists players add column if not exists lobby_delegates integer not null default 1;
    alter table if exists players add column if not exists reserve_delegates integer not null default 6;
exception when undefined_table then null;
end $$;

do $$ begin
    alter table if exists global_parameters add column if not exists turmoil jsonb not null default '{}'::jsonb;
exception when undefined_table then null;
end $$;

create table if not exists players (
    id uuid primary key default gen_random_uuid(),
    display_name text not null,

    -- Terraform Rating: arranca en 20, sube 1 por cada paso de parametro global
    tr integer not null default 20,

    -- Stock de recursos
    mc integer not null default 0,
    steel integer not null default 0,
    titanium integer not null default 0,
    plants integer not null default 0,
    energy integer not null default 0,
    heat integer not null default 0,

    -- Produccion por generacion (mc_production es la unica que puede ser
    -- negativa, con piso en -5; ver rules_engine.MC_PRODUCTION_FLOOR)
    mc_production integer not null default 1,
    steel_production integer not null default 1,
    titanium_production integer not null default 1,
    plant_production integer not null default 1,
    energy_production integer not null default 1,
    heat_production integer not null default 1,

    -- Cartas jugadas que quedan "activas" frente al jugador porque tienen
    -- una accion repetible y/o guardan recursos propios (ej. Ironworks:
    -- accion; Regolith Eaters: accion + microbios en la carta).
    -- Forma: {card_id: {"resources": int, "action_used": bool}}. Ver
    -- rules_engine.use_card_action / register_active_card.
    active_cards jsonb not null default '{}'::jsonb,

    -- Cuenta acumulada de tags en cartas ya jugadas (ej. Mass Converter
    -- requiere 5 tags de ciencia). Nunca se resetea entre generaciones.
    tags_played jsonb not null default '{}'::jsonb,

    -- Efectos pasivos permanentes de cartas ya jugadas que no son una
    -- accion repetible (ej. Advanced Alloys, Media Group). Ver
    -- rules_engine.register_passive_effect / compute_conversion_rates /
    -- apply_event_played_bonuses.
    passive_effects jsonb not null default '[]'::jsonb,

    -- Sistema de mazo/mano (ver rules_engine.py, seccion correspondiente).
    -- deck: card_ids restantes por robar (deck[0] = tope). hand: card_ids
    -- que el jugador posee y no jugo (play_card exige que la carta este
    -- aca). pending_research: card_ids robados en una fase de investigacion
    -- todavia sin resolver (start_research_phase / resolve_research_phase).
    deck jsonb not null default '[]'::jsonb,
    hand jsonb not null default '[]'::jsonb,
    pending_research jsonb not null default '[]'::jsonb,

    -- Historial permanente de card_ids jugados (nunca se sacan). Necesario
    -- para cartas que targetean "una de tus cartas jugadas" por catalogo/tag
    -- en vez de por recursos guardados en la carta (ej. Robotic Workforce).
    played_cards jsonb not null default '[]'::jsonb,

    -- Descuento de MC pendiente para la PROXIMA carta que se juegue esta
    -- generacion (ej. Indentured Workers: -8 MC). Se consume (vuelve a 0)
    -- al jugar la siguiente carta, la cubra entera o no, y tambien se
    -- pierde si termina la generacion sin usarse. Ver
    -- rules_engine.apply_card_effect ("next_card_discount_mc") y
    -- tools.play_card.
    pending_mc_discount integer not null default 0,

    -- Igual que pending_mc_discount, pero para relajar (o endurecer, puede
    -- ser negativo) los requisitos de temperatura/oxigeno/oceanos de la
    -- PROXIMA carta jugada esta generacion, en pasos (ej. Special Design:
    -- +/-2, a eleccion del jugador -- se guarda el signo que el jugador
    -- eligio). Se consume al chequear los requisitos de esa carta. Ver
    -- rules_engine.check_card_requirements ("next_card_requirement_tolerance_steps")
    -- y tools.play_card.
    pending_requirement_tolerance_steps integer not null default 0,

    -- reserved_cards: {reserved_card_id: {"resources": int,
    -- "holder_card_id": str}} -- cartas de la mano reservadas sobre otra
    -- carta activa (ej. Self-Replicating Robots) sin jugarlas ni pagarlas
    -- todavia, con recursos acumulables que despues descuentan su costo.
    -- Ver rules_engine.reserve_card_in_slot / compute_reserved_card_discount
    -- y tools.play_card / tools.use_card_action.
    reserved_cards jsonb not null default '{}'::jsonb,

    -- Cuenta de cartas jugadas SIN ningun tag (ej. Community Services: +1
    -- produccion MC por cada una, incluida ella misma). Ver
    -- rules_engine.increment_zero_tag_cards_played.
    zero_tag_cards_played integer not null default 0,

    -- Expansion Colonies: colonias propias (ver rules_engine.PlayerState,
    -- colonies.build_colony) y flotas de comercio (colonies.trade_with_colony,
    -- disponibles = trade_fleets - trade_fleets_used, este ultimo vuelve a
    -- 0 en cada fase de produccion).
    colonies_owned jsonb not null default '[]'::jsonb,
    trade_fleets integer not null default 1,
    trade_fleets_used integer not null default 0,

    -- Expansion Turmoil: delegados propios (ver backend/app/agent/turmoil.py).
    -- lobby_delegates arranca en 1 (se rellena en tools.resolve_new_government),
    -- reserve_delegates arranca en 6 -- 7 delegados totales, setup oficial.
    lobby_delegates integer not null default 1,
    reserve_delegates integer not null default 6,

    created_at timestamptz not null default now()
);

-- Parametros globales: compartidos por todos los jugadores de una partida.
-- game_id fijo en 'default' para el MVP (una sola partida activa a la vez).
create table if not exists global_parameters (
    game_id text primary key default 'default',
    temperature integer not null default -30,  -- rango: -30 a 8, pasos de 2
    oxygen integer not null default 0,          -- rango: 0 a 14, pasos de 1
    oceans_placed integer not null default 0,   -- rango: 0 a 9
    city_tiles_placed integer not null default 0,  -- ciudades colocadas por cualquier jugador
    events_played integer not null default 0,   -- cartas "Event" jugadas alguna vez, historico
    venus integer not null default 0,   -- Venus scale (expansion Venus Next), rango: 0 a 30, pasos de 2, no es condicion de fin de partida
    generation integer not null default 1,

    -- Tablero hexagonal (mapa Tharsis, ver backend/app/agent/board.py y
    -- HEX_MAP_RESEARCH.md). Forma: {hex_id: {"tile_type": str, "owner":
    -- str|None, "bonus_consumed": bool}}. La geometria/bonus de cada hex son
    -- constantes en board.py (HEX_DEFS/ADJACENCY), no se persisten -- solo
    -- el estado mutable (que hexagonos ya tienen tile) va aca. Un hex_id
    -- ausente de este jsonb se interpreta como vacio (board.is_hex_empty).
    -- Todavia NO esta cableado a tools.py -- ver "Pendiente" en
    -- HEX_MAP_RESEARCH.md.
    board jsonb not null default '{}'::jsonb,

    -- Expansion Colonies: Colony Tiles en juego esta partida. Forma:
    -- {colony_id: {"track_position": int, "owners": [player_id,...],
    -- "trade_fleet_present": bool}}. Los datos ESTATICOS de cada colonia
    -- (track de valores, bonus) viven en colonies.COLONY_DEFS, no aca.
    -- Arranca vacio hasta llamar tools.setup_colonies.
    colonies jsonb not null default '{}'::jsonb,

    -- Expansion Turmoil: estado de los 6 partidos (ver
    -- backend/app/agent/turmoil.py, TurmoilState). Arranca vacio hasta la
    -- primera llamada a tools.lobby/tools.play_card con una carta de
    -- Turmoil -- turmoil._load_turmoil (tools.py) devuelve
    -- turmoil.new_turmoil() por defecto cuando esta vacio.
    turmoil jsonb not null default '{}'::jsonb
);

-- Catalogo de cartas de proyecto.
--
-- IMPORTANTE: esta tabla arranca vacia a proposito. Terraforming Mars tiene
-- ~200 cartas de proyecto, cada una con costo, tags y efecto especifico.
-- No se generaron datos aqui para no arriesgar numeros incorrectos -- cargalas
-- vos mismo desde tu copia fisica del juego o una fuente verificada (ver
-- CLAUDE.md, seccion "Catalogo de cartas"). requirements/effects quedan como
-- jsonb libre para que definas el schema que mejor se ajuste a como vayas
-- implementando los efectos en tools.py.
create table if not exists cards (
    id text primary key,
    name text not null,
    cost integer not null,
    tags text[] not null default '{}',          -- ej. {'building'}, {'space'}, {'power'}
    requirements jsonb,                          -- ej. {"min_temperature": -20}
    effects jsonb not null default '{}'::jsonb,  -- estructura libre, definida al implementar cada carta
    is_event boolean not null default false      -- true = carta "Event" del juego real (dispara bonus pasivos de otras cartas al jugarse)
);

-- Cola de revision del catalogo: metadata (nombre/expansion/scan) de cartas
-- descargadas de tm.hadronikle.com que TODAVIA no se leyeron para decidir su
-- costo/tags/effects (ver backend/scripts/enqueue_card_review_queue.py).
-- Reemplaza el manifiesto manual CARDS_PENDING_REVIEW.md -- una vez que una
-- fila se revisa (se lee el scan, se decide el vocabulario, se carga en
-- `cards` via seed_cards.sql), se marca reviewed=true y se linkea a card_id.
-- NUNCA se guarda la imagen del scan aca (derechos de autor de FryxGames,
-- ver CLAUDE.md) -- solo la URL para poder descargarla puntualmente.
create table if not exists card_review_queue (
    id serial primary key,
    scan_number text not null unique,
    name text not null,
    expansion text not null,
    image_url text not null,
    reviewed boolean not null default false,
    card_id text references cards(id),
    discovered_at timestamptz not null default now()
);

create table if not exists transactions (
    id uuid primary key default gen_random_uuid(),
    player_id uuid references players(id) on delete cascade,
    action_type text not null,   -- 'standard_project' | 'convert_resources' | 'play_card' | 'use_card_action' | 'production_phase'
    detail jsonb not null,
    created_at timestamptz not null default now()
);

-- Seed inicial de parametros globales para que exista la fila 'default'
insert into global_parameters (game_id) values ('default')
on conflict (game_id) do nothing;
