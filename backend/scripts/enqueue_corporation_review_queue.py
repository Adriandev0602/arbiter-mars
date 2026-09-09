"""
Puebla `corporation_review_queue` con las 48 corporaciones del indice del
sitio (tm.hadronikle.com, categoria "Corporation").

Esta categoria, junto con Prelude y Automa, nunca entro al pipeline porque
`enqueue_card_review_queue.py` filtra `cat != "Project"`. A diferencia de las
cartas de proyecto, el indice trae `num` VACIO para las corporaciones, asi que
la clave unica de la cola es el NOMBRE (mismo criterio que global_events).

Como siempre: esto NO decide tags/starting_mc/effects de ninguna corporacion
-- eso es trabajo manual carta por carta contra el scan. Este script solo
mueve metadata. Tampoco descarga imagenes (ver download_corporation_scans.py,
que espacia los pedidos).

Uso:
    cd backend && source .venv/bin/activate
    python scripts/enqueue_corporation_review_queue.py \
        --cards-json <index.html cacheado del sitio> --db-url "$SUPABASE_DB_URL"
"""
from __future__ import annotations

import argparse
import json
import re

import psycopg2
from psycopg2.extras import execute_values


def load_corporations(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    try:
        cards = json.loads(raw)
    except json.JSONDecodeError:
        # index.html del sitio: el catalogo vive en un `const CARDS = [...]`.
        match = re.search(r"const CARDS\s*=\s*(\[.*?\]);", raw, re.S)
        if match is None:
            raise SystemExit("No se encontro el array CARDS en el archivo")
        cards = json.loads(match.group(1))
    return [c for c in cards if c.get("cat") == "Corporation"]


def connect(db_url: str):
    # La password del SUPABASE_DB_URL tiene un '@', que rompe el parseo de
    # psycopg2.connect(url) -- por eso se separa a mano (ver CLAUDE.md).
    match = re.match(r"postgresql://([^:]+):(.*)@([^:/]+):(\d+)/(\S+)", db_url.strip())
    if match is None:
        raise SystemExit("SUPABASE_DB_URL con formato inesperado")
    user, password, host, port, dbname = match.groups()
    return psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password, sslmode="require",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards-json", required=True)
    parser.add_argument("--db-url", required=True)
    args = parser.parse_args()

    corps = load_corporations(args.cards_json)
    rows = [(c["name"], c.get("exp") or "?", c["img"]) for c in corps]

    conn = connect(args.db_url)
    conn.autocommit = True
    with conn.cursor() as cur:
        execute_values(
            cur,
            """insert into corporation_review_queue (name, expansion, image_url)
               values %s on conflict (name) do nothing""",
            rows,
        )
        cur.execute("select count(*), count(*) filter (where reviewed) from corporation_review_queue")
        total, reviewed = cur.fetchone()
    print(f"{len(rows)} corporaciones procesadas; cola: {total} filas, {reviewed} revisadas")


if __name__ == "__main__":
    main()
