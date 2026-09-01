"""
Descarga los scans de las cartas en `card_review_queue` (reviewed = false)
para poder leerlas despues y decidir su vocabulario de effects/requirements.

Respeta la regla de espaciado de CLAUDE.md (no bajar cartas en paralelo ni
en rafaga): un pedido a la vez, con pausa entre cada uno. Procesa en lotes
de 100 (imprime progreso por lote), es reanudable -- si un archivo ya existe
en el directorio de salida, lo salta sin volver a pedirlo.

Las imagenes NUNCA se commitean al repo (derechos de autor de FryxGames) --
el directorio de salida debe estar en .gitignore. Son material de trabajo
temporal para la sesion que las revisa; se pueden borrar despues de usarlas.

Uso:
    cd backend && source .venv/bin/activate
    python scripts/download_review_scans.py --out-dir /tmp/scan_cache --limit 100
    python scripts/download_review_scans.py --out-dir /tmp/scan_cache  # todas las pendientes
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import httpx
import psycopg2

BATCH_SIZE = 100
DELAY_SECONDS = 2.5


def safe_filename(expansion: str, scan_number: str, name: str) -> str:
    raw = f"{expansion} - {scan_number} - {name}.png"
    return raw.replace(" ", "_").replace("/", "_")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--db-url", default=os.environ.get("SUPABASE_DB_URL"))
    parser.add_argument("--limit", type=int, default=None, help="maximo de cartas a descargar en esta corrida")
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS)
    args = parser.parse_args()

    if not args.db_url:
        print("Falta --db-url o la variable de entorno SUPABASE_DB_URL", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out_dir, exist_ok=True)

    conn = psycopg2.connect(args.db_url, sslmode="require")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        "select id, scan_number, name, expansion, image_url from card_review_queue "
        "where reviewed = false order by id"
    )
    pending = cur.fetchall()
    if args.limit:
        pending = pending[: args.limit]

    print(f"Cartas a procesar en esta corrida: {len(pending)}")

    downloaded, skipped, failed = 0, 0, 0
    with httpx.Client(timeout=30.0) as client:
        for idx, (row_id, scan_number, name, expansion, image_url) in enumerate(pending, start=1):
            filename = safe_filename(expansion, scan_number, name)
            out_path = os.path.join(args.out_dir, filename)

            if os.path.exists(out_path):
                skipped += 1
            else:
                try:
                    resp = client.get(image_url)
                    resp.raise_for_status()
                    with open(out_path, "wb") as f:
                        f.write(resp.content)
                    downloaded += 1
                except httpx.HTTPError as exc:
                    print(f"  FALLO {name} ({scan_number}): {exc}", file=sys.stderr)
                    failed += 1
                time.sleep(args.delay)

            if idx % BATCH_SIZE == 0 or idx == len(pending):
                print(
                    f"Progreso: {idx}/{len(pending)} "
                    f"(descargadas {downloaded}, ya existian {skipped}, fallidas {failed})"
                )

    conn.close()
    print(f"Listo. Descargadas: {downloaded}, ya existian: {skipped}, fallidas: {failed}")
    print(f"Archivos en: {args.out_dir}")


if __name__ == "__main__":
    main()
