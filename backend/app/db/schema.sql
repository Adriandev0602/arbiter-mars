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

    created_at timestamptz not null default now()
);

-- Parametros globales: compartidos por todos los jugadores de una partida.
-- game_id fijo en 'default' para el MVP (una sola partida activa a la vez).
create table if not exists global_parameters (
    game_id text primary key default 'default',
    temperature integer not null default -30,  -- rango: -30 a 8, pasos de 2
    oxygen integer not null default 0,          -- rango: 0 a 14, pasos de 1
    oceans_placed integer not null default 0,   -- rango: 0 a 9
    generation integer not null default 1
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
    effects jsonb not null default '{}'::jsonb   -- estructura libre, definida al implementar cada carta
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
