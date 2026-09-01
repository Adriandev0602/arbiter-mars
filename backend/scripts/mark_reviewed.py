"""
Marca filas de `card_review_queue` como reviewed=true y las linkea al id
que terminaron teniendo en `cards`, una vez que ya se cargaron en
seed_cards.sql. Reemplaza el paso manual de "borrar del manifiesto" -- ahora
es "marcar revisado en la cola".

Uso:
    python scripts/mark_reviewed.py --scan-number 037 --card-id nitrogen_rich_asteroid
    python scripts/mark_reviewed.py --scan-number 038 --skip  # revisada pero no cargada
                                                                 # (fuera de alcance / pendiente)
"""
from __future__ import annotations

import argparse
import os
import sys

import psycopg2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan-number", required=True)
    parser.add_argument("--card-id", default=None, help="id en `cards` si se cargo")
    parser.add_argument("--skip", action="store_true", help="marcar revisada sin card_id (no cargada)")
    parser.add_argument("--db-url", default=os.environ.get("SUPABASE_DB_URL"))
    args = parser.parse_args()

    if not args.db_url:
        print("Falta --db-url o la variable de entorno SUPABASE_DB_URL", file=sys.stderr)
        sys.exit(1)
    if not args.card_id and not args.skip:
        print("Pasa --card-id o --skip", file=sys.stderr)
        sys.exit(1)

    conn = psycopg2.connect(args.db_url, sslmode="require")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        "update card_review_queue set reviewed = true, card_id = %s where scan_number = %s returning name",
        (args.card_id, args.scan_number),
    )
    row = cur.fetchone()
    if row is None:
        print(f"No se encontro scan_number '{args.scan_number}' en card_review_queue", file=sys.stderr)
        sys.exit(1)
    print(f"Marcada revisada: {row[0]} (scan {args.scan_number}) -> card_id={args.card_id}")
    conn.close()


if __name__ == "__main__":
    main()
