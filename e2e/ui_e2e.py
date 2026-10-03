"""
E2E del frontend con un navegador real (Chromium del sistema, via Playwright) contra el backend
y la base reales. Recorre lo que haria un usuario: crear jugador, ver el dashboard, jugar por
chat, y verifica que los numeros que pinta la UI sean los que devuelve la API (el LLM nunca
calcula: la UI solo puede mostrar lo que calculo el motor).

Requisitos: backend en :8000 y frontend en :3000 corriendo, y Chromium en /usr/bin/chromium.
    python3 -m venv e2e/.venv && e2e/.venv/bin/pip install playwright
    e2e/.venv/bin/python e2e/ui_e2e.py              # UI completa + chat si hay ANTHROPIC_API_KEY
    e2e/.venv/bin/python e2e/ui_e2e.py --keep       # no borrar el jugador de prueba al final

Si el backend no tiene una ANTHROPIC_API_KEY valida, los pasos de chat quedan SALTEADOS (no
fallan): el resto de la UI se prueba igual. Capturas en e2e/out/.
"""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "e2e" / "out"
OUT.mkdir(parents=True, exist_ok=True)
FRONT = "http://localhost:3000"
API = "http://localhost:8000/api"
NAME = f"E2E {int(time.time()) % 100000}"
KEEP = "--keep" in sys.argv

# Turnos de chat de una partida corta. Cada uno se verifica contra la API despues.
CHAT_TURNS = [
    "Elegí la corporación Beginner Corporation",
    "Repartime la mano inicial",
    "¿Cuál es mi estado actual?",
    "Quiero usar el proyecto estándar Planta de energía",
    "Cerrá mi fase de producción",
]

results: list[tuple[str, str, str]] = []


def record(name: str, status: str, detail: str = "") -> None:
    results.append((name, status, detail))


def step(name, fn):
    try:
        fn()
        record(name, "OK")
        return True
    except Exception as e:  # noqa: BLE001
        record(name, "FAIL", str(e).splitlines()[0][:300])
        return False


def api_get(path: str) -> dict:
    with urllib.request.urlopen(API + path, timeout=30) as r:
        return json.loads(r.read())


def player_id_by_name(name: str) -> str | None:
    return next((p["id"] for p in api_get("/players") if p["display_name"] == name), None)


def ui_numbers(page) -> dict:
    """Lee del DOM el TR y el stock/produccion de cada recurso tal como los ve el usuario."""
    section = page.get_by_test_id("resources")
    out = {"tr": int(section.get_by_test_id("tr").inner_text())}
    for key in ("mc", "steel", "titanium", "plants", "energy", "heat"):
        tile = section.get_by_test_id(f"resource-{key}")
        stock = int(tile.get_by_test_id("stock").inner_text())
        prod = int(tile.get_by_test_id("production").inner_text().replace("producción", "").strip())
        out[key] = (stock, prod)
    return out


PRODUCTION_KEY = {
    "mc": "mc_production", "steel": "steel_production", "titanium": "titanium_production",
    "plants": "plant_production", "energy": "energy_production", "heat": "heat_production",
}


def assert_ui_matches_api(page, pid: str) -> None:
    page.get_by_role("button", name="Actualizar").click()
    expect(page.get_by_role("button", name="Actualizar")).to_be_enabled(timeout=30_000)
    api = api_get(f"/state/{pid}")["player"]
    ui = ui_numbers(page)
    diffs = []
    if ui["tr"] != api["tr"]:
        diffs.append(f"TR ui={ui['tr']} api={api['tr']}")
    for key, prod_key in PRODUCTION_KEY.items():
        if ui[key] != (api[key], api[prod_key]):
            diffs.append(f"{key} ui={ui[key]} api={(api[key], api[prod_key])}")
    hand_ui = int(page.get_by_test_id("cards-Mano").get_by_test_id("count").inner_text().strip("()"))
    if hand_ui != len(api["hand"]):
        diffs.append(f"mano ui={hand_ui} api={len(api['hand'])}")
    assert not diffs, "; ".join(diffs)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    console_errors, bad_responses = [], []
    page.on("console", lambda m: m.type == "error" and console_errors.append(m.text))
    page.on("response", lambda r: r.status >= 400 and bad_responses.append(f"{r.status} {r.request.method} {r.url}"))

    step("carga la página", lambda: (page.goto(FRONT), expect(page.get_by_role("heading", name="Árbitro de Terraforming Mars")).to_be_visible()))
    step("muestra parámetros globales", lambda: expect(page.get_by_text("Temperatura")).to_be_visible())
    page.screenshot(path=OUT / "01_inicio.png")

    def create_player():
        page.get_by_role("button", name="Nuevo").click()
        page.get_by_placeholder("Nombre del jugador").fill(NAME)
        page.get_by_role("button", name="Crear").click()
        expect(page.locator("#player")).to_contain_text(NAME)
    step("crea un jugador desde la UI", create_player)
    pid = player_id_by_name(NAME)

    step("el dashboard coincide con la API (jugador nuevo)", lambda: assert_ui_matches_api(page, pid))
    page.screenshot(path=OUT / "02_jugador.png")

    def survives_reload():
        page.reload()
        expect(page.locator("#player")).to_contain_text(NAME)
        expect(page.get_by_text("Terraform Rating")).to_be_visible()
    step("recuerda el jugador al recargar", survives_reload)

    chat_available = True
    for i, msg in enumerate(CHAT_TURNS, 1):
        if not chat_available:
            record(f"chat {i}: {msg}", "SKIP", "sin ANTHROPIC_API_KEY valida en el backend")
            continue
        before = len(bad_responses)
        page.get_by_placeholder("Quiero jugar la carta X pagando…").fill(msg)
        page.get_by_role("button", name="Enviar").click()
        try:
            expect(page.get_by_text(msg, exact=True)).to_be_visible()
            expect(page.get_by_text("El árbitro está calculando…")).to_be_hidden(timeout=180_000)
        except Exception as e:  # noqa: BLE001
            record(f"chat {i}: {msg}", "FAIL", str(e).splitlines()[0][:200])
            continue
        bubbles = page.locator("aside .whitespace-pre-wrap")
        reply = bubbles.nth(bubbles.count() - 1).inner_text()
        page.screenshot(path=OUT / f"03_chat_{i}.png")
        if "ANTHROPIC_API_KEY" in reply:
            chat_available = False
            record(f"chat {i}: {msg}", "SKIP", "sin ANTHROPIC_API_KEY valida en el backend")
            continue
        if reply.startswith("No se pudo consultar"):
            record(f"chat {i}: {msg}", "FAIL", reply[:200])
            continue
        record(f"chat {i}: {msg}", "OK", reply[:300].replace("\n", " ⏎ "))
        step(f"  dashboard == API después del turno {i}", lambda: assert_ui_matches_api(page, pid))
        if len(bad_responses) > before:
            record(f"  requests con error en el turno {i}", "WARN", "; ".join(bad_responses[before:])[:300])

    mobile = browser.new_page(viewport={"width": 390, "height": 844})

    def mobile_ok():
        mobile.goto(FRONT + f"/?player={pid}")
        expect(mobile.get_by_role("heading", name="Árbitro de Terraforming Mars")).to_be_visible()
        expect(mobile.get_by_text("Terraform Rating")).to_be_visible()
        width = mobile.evaluate("document.documentElement.scrollWidth")
        assert width <= 390, f"scroll horizontal en celular: ancho {width}px"
    step("celular: carga el jugador y no hay scroll horizontal", mobile_ok)
    mobile.screenshot(path=OUT / "04_mobile.png", full_page=True)
    browser.close()

if pid and not KEEP:
    cleanup = (
        "import sys; sys.path.insert(0,'scripts')\n"
        "from apply_db import parse_db_url, read_env_db_url\n"
        "import psycopg2\n"
        "c=psycopg2.connect(**parse_db_url(read_env_db_url()), sslmode='require'); c.autocommit=True; cur=c.cursor()\n"
        f"cur.execute(\"delete from transactions where player_id=%s\", ('{pid}',))\n"
        f"cur.execute(\"delete from players where id=%s\", ('{pid}',))\n"
    )
    subprocess.run([str(ROOT / "backend/.venv/bin/python"), "-c", cleanup], cwd=ROOT / "backend", check=False)

width = max(len(n) for n, _, _ in results)
for name, status, detail in results:
    print(f"[{status:4}] {name.ljust(width)}" + (f"  {detail}" if detail else ""))
noise = [e for e in console_errors if "503" not in e]
print("\nerrores de consola:", json.dumps(noise[:10], ensure_ascii=False))
print("jugador de prueba:", NAME, "(borrado)" if not KEEP else "(conservado)")
sys.exit(1 if any(s == "FAIL" for _, s, _ in results) else 0)
