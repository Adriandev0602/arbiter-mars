"""
Carga en Supabase (tabla `card_review_queue`) la metadata (nombre, expansion,
numero de scan, URL de imagen) de TODAS las cartas que todavia figuran en
`backend/app/db/CARDS_PENDING_REVIEW.md` como pendientes de revisar.

Esto NO decide costo/tags/effects de ninguna carta -- eso sigue siendo
trabajo manual (leer el scan y extender el motor si hace falta, igual que
hasta ahora). Este script solo mueve el manifiesto de "pendientes" de un
archivo Markdown a una tabla de la base, para dejar de procesar bloques de a
10 a mano y poder trabajar contra la cola completa.

No descarga ninguna imagen (eso lo hace download_review_scans.py aparte, en
lotes con espera entre pedidos). Este script es rapido: un solo parseo local
del manifiesto + el catalogo ya cacheado del sitio, sin pegarle a
tm.hadronikle.com.

Uso:
    cd backend && source .venv/bin/activate
    python scripts/enqueue_card_review_queue.py \
        --pending-md app/db/CARDS_PENDING_REVIEW.md \
        --cards-json /ruta/a/index.html-o-cards.json

El segundo archivo puede ser el index.html cacheado del sitio (se le extrae
el array `const CARDS = [...]`) o un JSON ya extraido con esa misma forma.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import psycopg2
from psycopg2.extras import execute_values

BATCH_SIZE = 100


def parse_pending_manifest(path: str) -> list[tuple[str, str, str]]:
    """Devuelve [(nombre, expansion, scan_number), ...] de la tabla markdown."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    start = next(i for i, l in enumerate(lines) if l.strip().startswith("<!-- TABLE_START"))
    end = next(i for i, l in enumerate(lines) if l.strip().startswith("<!-- TABLE_END"))

    rows = []
    for line in lines[start + 1 : end]:
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) != 5:
            continue
        num, name, expansion, scan, estado = parts
        if not num.isdigit():
            continue  # header / separador
        rows.append((name, expansion, scan))
    return rows


def load_site_catalog(path: str) -> list[dict]:
    """Extrae el array `const CARDS = [...]` de un index.html cacheado, o
    carga directo un .json con la misma forma."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if path.endswith(".json"):
        return json.loads(content)
    match = re.search(r"const CARDS = (\[.*?\]);", content)
    if not match:
        raise ValueError(f"No se encontro 'const CARDS = [...]' en {path}")
    return json.loads(match.group(1))


def build_image_url_index(catalog: list[dict]) -> dict[tuple[str, str], str]:
    """Indexa por (scan_number, expansion) -> img url, solo categoria Project."""
    index: dict[tuple[str, str], str] = {}
    for card in catalog:
        if card.get("cat") != "Project":
            continue
        index[(card["num"], card["exp"])] = card["img"]
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pending-md", required=True)
    parser.add_argument("--cards-json", required=True)
    parser.add_argument("--db-url", default=os.environ.get("SUPABASE_DB_URL"))
    args = parser.parse_args()

    if not args.db_url:
        print("Falta --db-url o la variable de entorno SUPABASE_DB_URL", file=sys.stderr)
        sys.exit(1)

    pending = parse_pending_manifest(args.pending_md)
    catalog = load_site_catalog(args.cards_json)
    url_index = build_image_url_index(catalog)

    rows_to_insert = []
    missing = []
    for name, expansion, scan in pending:
        url = url_index.get((scan, expansion))
        if url is None:
            missing.append((name, expansion, scan))
            continue
        rows_to_insert.append((scan, name, expansion, url))

    print(f"Manifiesto: {len(pending)} cartas pendientes")
    print(f"Emparejadas con el catalogo del sitio: {len(rows_to_insert)}")
    if missing:
        print(f"SIN emparejar (revisar a mano, no se encolaron): {len(missing)}")
        for name, expansion, scan in missing[:20]:
            print(f"  - {name} ({expansion}, scan {scan})")
        if len(missing) > 20:
            print(f"  ... y {len(missing) - 20} mas")

    conn = psycopg2.connect(args.db_url, sslmode="require")
    conn.autocommit = True
    cur = conn.cursor()

    inserted_total = 0
    for i in range(0, len(rows_to_insert), BATCH_SIZE):
        batch = rows_to_insert[i : i + BATCH_SIZE]
        execute_values(
            cur,
            """
            insert into card_review_queue (scan_number, name, expansion, image_url)
            values %s
            on conflict (scan_number) do nothing
            """,
            batch,
        )
        inserted_total += len(batch)
        print(f"Encolado lote {i // BATCH_SIZE + 1}: {len(batch)} filas (acumulado {inserted_total})")

    cur.execute("select count(*) from card_review_queue where reviewed = false")
    print(f"Total en card_review_queue sin revisar: {cur.fetchone()[0]}")

    conn.close()


if __name__ == "__main__":
    main()
