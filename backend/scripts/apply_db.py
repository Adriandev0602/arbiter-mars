"""
Aplica el schema y el catalogo completo a la base de Postgres (Supabase), en orden:
schema.sql -> seed_cards.sql -> seed_corporations.sql -> seed_preludes.sql ->
seed_global_events.sql. Todos los archivos son idempotentes (`if not exists`,
`on conflict do update`), asi que se puede correr las veces que haga falta.

La password de SUPABASE_DB_URL tiene un `@`, y psycopg2.connect(url) no la parsea
bien. Por eso la URL se separa a mano: todo lo que esta despues del ULTIMO `@` es
host:puerto/base, y todo lo que esta antes es usuario:password.

Uso (desde backend/):
    python3 scripts/apply_db.py                 # lee SUPABASE_DB_URL de .env
    python3 scripts/apply_db.py --db-url "postgresql://..."
    python3 scripts/apply_db.py --check         # solo conecta y cuenta filas
"""
import argparse
import os
from pathlib import Path
from urllib.parse import unquote

import psycopg2

DB_DIR = Path(__file__).resolve().parent.parent / "app" / "db"
FILES = ["schema.sql", "seed_cards.sql", "seed_corporations.sql", "seed_preludes.sql", "seed_global_events.sql"]
COUNTS = ["cards", "corporation_cards", "prelude_cards", "global_events", "players"]


def parse_db_url(url: str) -> dict:
    scheme_sep = url.index("://")
    rest = url[scheme_sep + 3:]
    credentials, _, location = rest.rpartition("@")
    user, _, password = credentials.partition(":")
    host_port, _, dbname = location.partition("/")
    dbname = dbname.split("?")[0] or "postgres"
    host, _, port = host_port.partition(":")
    return {
        "host": host, "port": int(port or 5432), "dbname": dbname,
        "user": unquote(user), "password": unquote(password),
    }


def read_env_db_url() -> str | None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if os.environ.get("SUPABASE_DB_URL"):
        return os.environ["SUPABASE_DB_URL"]
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("SUPABASE_DB_URL="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db-url", help="connection string de Postgres (por defecto SUPABASE_DB_URL de .env)")
    parser.add_argument("--check", action="store_true", help="solo conectar y mostrar conteos, sin aplicar nada")
    parser.add_argument("--no-ssl", action="store_true", help="sin sslmode=require (Postgres local)")
    args = parser.parse_args()

    url = args.db_url or read_env_db_url()
    if not url:
        raise SystemExit("Falta SUPABASE_DB_URL (en .env o con --db-url)")
    params = parse_db_url(url)
    conn = psycopg2.connect(**params, sslmode="disable" if args.no_ssl else "require", connect_timeout=15)
    conn.autocommit = True
    cur = conn.cursor()
    print(f"Conectado a {params['host']}:{params['port']}/{params['dbname']}")

    if not args.check:
        for name in FILES:
            cur.execute((DB_DIR / name).read_text())
            print(f"  aplicado {name}")

    for table in COUNTS:
        try:
            cur.execute(f"select count(*) from {table}")
            print(f"  {table}: {cur.fetchone()[0]}")
        except psycopg2.Error as exc:
            print(f"  {table}: (no existe: {exc.pgerror.strip() if exc.pgerror else exc})")
    conn.close()


if __name__ == "__main__":
    main()
