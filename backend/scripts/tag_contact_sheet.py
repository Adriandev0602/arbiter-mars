"""
Arma "hojas de contacto" para auditar a mano el TAG de muchas cartas de una,
sin abrir 62 scans completos.

De cada scan recorta solo la BANDA SUPERIOR (donde viven el costo, el recuadro
de requisito y los tags propios), la escala a un alto comun y apila varias
cartas etiquetadas con su `card_id`. Una hoja de 8 cartas se lee de un vistazo
y evita el error clasico de esta auditoria: confundir el recuadro de REQUISITO
(arriba a la izquierda, pegado al costo) con los TAGS PROPIOS (extremo superior
derecho).

Recordatorio de iconografia, que es lo que se esta auditando:
  * power = RAYO blanco sobre circulo MORADO
  * space = SOL DORADO de 8 puntas sobre circulo NEGRO

Uso:
    python scripts/tag_contact_sheet.py --pattern 'scripts/scan_cache/AUDIT_*.png' \
        --out-dir /tmp/sheets --per-sheet 8
"""
from __future__ import annotations

import argparse
import glob
import os

from PIL import Image, ImageDraw, ImageFont

# La banda util es el ~13% superior de la carta: ahi entran el costo, el
# recuadro de requisito y los tags, y nada mas que distraiga.
BAND_RATIO = 0.13
TARGET_W = 1100          # ancho al que se normaliza cada banda
LABEL_W = 330            # columna izquierda para el card_id
PAD = 10


def _font(size: int):
    for path in (
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_sheets(paths: list[str], out_dir: str, per_sheet: int) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    font = _font(30)
    written: list[str] = []

    for sheet_idx in range(0, len(paths), per_sheet):
        chunk = paths[sheet_idx : sheet_idx + per_sheet]
        strips: list[tuple[str, Image.Image]] = []
        for path in chunk:
            card_id = os.path.basename(path).removeprefix("AUDIT_").removesuffix(".png")
            with Image.open(path) as img:
                band = img.convert("RGB").crop((0, 0, img.width, int(img.height * BAND_RATIO)))
            scale = TARGET_W / band.width
            band = band.resize((TARGET_W, int(band.height * scale)), Image.LANCZOS)
            strips.append((card_id, band))

        row_h = max(b.height for _, b in strips) + PAD
        sheet = Image.new("RGB", (LABEL_W + TARGET_W + PAD * 2, row_h * len(strips) + PAD), "white")
        draw = ImageDraw.Draw(sheet)

        for i, (card_id, band) in enumerate(strips):
            y = PAD + i * row_h
            draw.text((PAD, y + band.height // 2 - 16), card_id, fill="black", font=font)
            sheet.paste(band, (LABEL_W, y))
            draw.line([(0, y + row_h - PAD // 2), (sheet.width, y + row_h - PAD // 2)], fill="#BBBBBB", width=2)

        out = os.path.join(out_dir, f"sheet_{sheet_idx // per_sheet + 1:02d}.png")
        sheet.save(out)
        written.append(out)

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--per-sheet", type=int, default=8)
    args = parser.parse_args()

    paths = sorted(glob.glob(args.pattern))
    if not paths:
        raise SystemExit(f"Sin coincidencias para {args.pattern}")
    for out in build_sheets(paths, args.out_dir, args.per_sheet):
        print(out)


if __name__ == "__main__":
    main()
