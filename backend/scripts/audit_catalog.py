"""
Auditoria del catalogo: cruza las cartas cargadas en Supabase (proyecto,
corporaciones, preludes) contra los datos de la implementacion open-source de
referencia (github.com/terraforming-mars/terraforming-mars) y lista las
diferencias de costo, tags, tipo evento y VP negativo.

LA REFERENCIA NO ES LA FUENTE DE VERDAD. Cada diferencia se decide contra el
scan oficial de la carta (ver CARDS_LOG.md, "Auditoria del catalogo"). La
referencia sirve para encontrar rapido que mirar; en la primera auditoria
(2026-10-02) se equivoco en 3 de 81 cartas (tags que define por parametro del
constructor, que este parser no ve). Esas 3 van en KNOWN_OK.

Uso (desde backend/, con .env apuntando a la base):
    git clone --depth 1 --filter=blob:none --sparse \\
        https://github.com/terraforming-mars/terraforming-mars.git /tmp/tmref
    git -C /tmp/tmref sparse-checkout set src/server/cards src/common
    python3 scripts/audit_catalog.py --ref-dir /tmp/tmref

Sale con codigo 1 si hay diferencias nuevas (no listadas en KNOWN_OK), para
poder usarlo como chequeo antes de commitear cartas nuevas.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.db.supabase_client import supabase  # noqa: E402

# Verificadas contra el scan: el seed esta bien y la referencia no se parsea bien.
KNOWN_OK = {
    "mining_rights": "tag building (scan 067)",
    "mining_area": "tag building (scan 064)",
    "pharmacy_union": "2 tags microbe (scan R39)",
}


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def load_reference(ref_dir: Path) -> dict[str, dict]:
    src = ref_dir / "src"
    card_names = {
        m.group(1): m.group(2).replace("\\'", "'")
        for m in re.finditer(r"^\s*(\w+)\s*=\s*'((?:[^'\\]|\\.)*)'", (src / "common/cards/CardName.ts").read_text(), re.M)
    }
    ref: dict[str, dict] = {}
    for f in (src / "server/cards").rglob("*.ts"):
        if "/render/" in str(f) or "/requirements/" in str(f):
            continue
        t = f.read_text()
        nm = re.search(r"name(?::|\s*=)\s*CardName\.(\w+)", t)
        if not nm or nm.group(1) not in card_names:
            continue
        cost = re.search(r"\bcost(?::|\s*=)\s*(\d+)", t)
        tags = re.search(r"tags:\s*\[([^\]]*)\]", t)
        ctype = re.search(r"CardType\.(\w+)", t)
        vp = re.search(r"victoryPoints:\s*(-?\d+)", t)
        number = re.search(r"cardNumber:\s*'([^']+)'", t)
        entry = {
            "file": str(f.relative_to(src)),
            "cost": int(cost.group(1)) if cost else None,
            "tags": sorted(x.split(".")[1].lower() for x in re.findall(r"Tag\.\w+", tags.group(1))) if tags else [],
            "type": ctype.group(1) if ctype else None,
            "vp": int(vp.group(1)) if vp else None,
            "number": number.group(1) if number else None,
        }
        key = norm(card_names[nm.group(1)])
        if key in ref and ("/ares/" in entry["file"] or "/pathfinders/" in entry["file"]):
            continue
        ref[key] = entry
    return ref


def fetch(table: str, cols: str) -> list[dict]:
    rows, start = [], 0
    while True:
        batch = supabase.table(table).select(cols).range(start, start + 999).execute().data
        rows += batch
        if len(batch) < 1000:
            return rows
        start += 1000


def vitor_excluded() -> set[str]:
    row = supabase.table("corporation_cards").select("effects").eq("id", "vitor").execute().data
    passive = (row[0]["effects"] or {}).get("passive", {}) if row else {}
    return set(passive.get("on_card_played_with_vp_icon", {}).get("excluded_card_ids", []))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ref-dir", required=True, type=Path, help="clon del repo de referencia")
    parser.add_argument("--json", type=Path, help="guardar el detalle en este archivo")
    args = parser.parse_args()

    ref = load_reference(args.ref_dir)
    excluded = vitor_excluded()
    diffs, unmatched = [], []
    for table, kind in (("cards", "project"), ("corporation_cards", "corporation"), ("prelude_cards", "prelude")):
        cols = "id,name,tags" + (",cost,is_event" if table == "cards" else "")
        for row in fetch(table, cols):
            r = ref.get(norm(row["name"]))
            if r is None:
                unmatched.append(row["id"])
                continue
            diff = {}
            ref_tags = [t for t in r["tags"] if t != "event"]
            if Counter(row.get("tags") or []) != Counter(ref_tags):
                diff["tags"] = {"seed": sorted(row.get("tags") or []), "ref": ref_tags}
            if table == "cards":
                if r["cost"] is not None and row["cost"] != r["cost"]:
                    diff["cost"] = {"seed": row["cost"], "ref": r["cost"]}
                if bool(row["is_event"]) != (r["type"] == "EVENT"):
                    diff["is_event"] = {"seed": row["is_event"], "ref": r["type"]}
            # VP negativo impreso: Vitor tiene que excluir la carta.
            if r["vp"] is not None and r["vp"] < 0 and row["id"] not in excluded:
                diff["negative_vp_not_excluded_by_vitor"] = r["vp"]
            if diff and row["id"] not in KNOWN_OK:
                diffs.append({"kind": kind, "id": row["id"], "number": r["number"], **diff})

    for d in diffs:
        print(json.dumps(d, ensure_ascii=False))
    print(f"\nreferencia: {len(ref)} cartas | sin match por nombre: {len(unmatched)} {unmatched}")
    print(f"diferencias nuevas: {len(diffs)} (verificar cada una contra su scan)")
    if args.json:
        args.json.write_text(json.dumps({"diffs": diffs, "unmatched": unmatched}, indent=1, ensure_ascii=False))
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
