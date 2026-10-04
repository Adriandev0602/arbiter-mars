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
# El setup (corporacion, mano, preludes) ya lo hace la UI; el chat juega la partida.
CHAT_TURNS = [
    "¿Cuál es mi estado actual?",
    "Quiero usar el proyecto estándar Planta de energía",
    "Cerrá mi fase de producción",
]

results: list[tuple[str, str, str]] = []

# El tablero es estado COMPARTIDO (global_parameters, fila 'default'): colocar un tile en la
# prueba lo cambia para todos. Se guarda una copia antes y se restaura siempre al final.
BOARD_SNAPSHOT = OUT / "global_parameters_snapshot.json"
_DB = (
    "import json, sys; sys.path.insert(0, '.')\n"
    "from app.db.supabase_client import supabase\n"
    "t = supabase.table('global_parameters')\n"
    "if sys.argv[1] == 'snap':\n"
    "    json.dump(t.select('*').eq('game_id', 'default').single().execute().data, open(sys.argv[2], 'w'))\n"
    "else:\n"
    "    row = json.load(open(sys.argv[2]))\n"
    "    t.update({k: v for k, v in row.items() if k != 'game_id'}).eq('game_id', 'default').execute()\n"
    "    print(t.select('*').eq('game_id', 'default').single().execute().data == row)\n"
)


def global_parameters(action: str) -> str:
    res = subprocess.run(
        [str(ROOT / "backend/.venv/bin/python"), "-c", _DB, action, str(BOARD_SNAPSHOT)],
        cwd=ROOT / "backend", capture_output=True, text=True, check=True,
    )
    return res.stdout.strip()


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
        # "producción +2", seguido de "(antes +1)" si acaba de cambiar: vale el valor actual.
        prod = int(tile.get_by_test_id("production").inner_text().replace("producción", "").split()[0])
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


global_parameters("snap")

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
        page.get_by_role("button", name="Nuevo jugador").click()
        page.get_by_placeholder("Nombre del jugador").fill(NAME)
        page.get_by_role("button", name="Crear", exact=True).click()
        expect(page.locator("#player")).to_contain_text(NAME)
    step("crea un jugador desde la UI", create_player)
    pid = player_id_by_name(NAME)

    # Inicio de partida guiado: corporacion -> mano inicial -> preludes.
    def setup_corporation():
        expect(page.get_by_role("heading", name="Elegí tu corporación")).to_be_visible()
        page.get_by_placeholder("Buscar por nombre o expansión").fill("Beginner")
        page.get_by_role("button", name="Beginner Corporation").click()
        page.get_by_role("button", name="Empezar con Beginner Corporation").click()
        expect(page.get_by_role("heading", name="Repartí tu mano inicial")).to_be_visible()
    step("setup: elige Beginner Corporation", setup_corporation)
    page.screenshot(path=OUT / "02a_setup_mano.png")

    def setup_hand():
        page.get_by_role("button", name="Repartir 10 cartas").click()
        expect(page.get_by_role("heading", name="¿Jugás con Preludes?")).to_be_visible()
    step("setup: reparte 10 cartas gratis (Beginner)", setup_hand)

    def setup_preludes():
        page.get_by_role("button", name="Repartir 4 Preludes").click()
        expect(page.get_by_role("heading", name="Quedate con 2 Preludes")).to_be_visible()
        picks = page.locator("section[aria-label='Inicio de partida'] ul button")
        picks.nth(0).click()
        picks.nth(1).click()
        page.get_by_role("button", name="Quedarme con estas 2").click()
        expect(page.get_by_test_id("resources")).to_be_visible()
        expect(page.get_by_text("Preludes para jugar")).to_be_visible()
    step("setup: reparte 4 Preludes y se queda con 2", setup_preludes)

    def setup_matches_engine():
        api = api_get(f"/state/{pid}")
        p_ = api["player"]
        assert api["corporation"]["id"] == "beginner_corporation", api["corporation"]
        assert len(p_["hand"]) == 10, f"mano {len(p_['hand'])}"
        assert len(p_["prelude_hand"]) == 2, p_["prelude_hand"]
        assert (p_["mc"], p_["mc_production"]) == (42, 1), (p_["mc"], p_["mc_production"])
    step("setup: el motor dejó Beginner con 42 M€, producción +1, 10 cartas y 2 Preludes", setup_matches_engine)

    step("el dashboard coincide con la API (después del setup)", lambda: assert_ui_matches_api(page, pid))
    page.screenshot(path=OUT / "02_jugador.png")

    def survives_reload():
        page.reload()
        expect(page.locator("#player")).to_contain_text(NAME)
        expect(page.get_by_text("Terraform Rating")).to_be_visible()
    step("recuerda el jugador al recargar", survives_reload)

    def board_city():
        board = page.get_by_test_id("board")
        board.scroll_into_view_if_needed()
        board.get_by_role("button", name="Ciudad", exact=True).click()
        legal = page.locator("[data-legal]")
        expect(legal.first).to_be_visible()
        hex_id = legal.first.get_attribute("data-hex")
        api_legal = [h["id"] for h in api_get(f"/board?player_id={pid}")["hexes"] if h["can_place_city"]]
        ui_legal = legal.evaluate_all("els => els.map(e => e.dataset.hex)")
        assert sorted(ui_legal) == sorted(api_legal), f"hexagonos legales ui={len(ui_legal)} api={len(api_legal)}"
        legal.first.click()
        board.get_by_role("button", name="Colocar").click()
        expect(page.locator(f'[data-hex="{hex_id}"] .animate-tile-in')).to_be_attached(timeout=15_000)
        tile = next(h for h in api_get(f"/board?player_id={pid}")["hexes"] if h["id"] == hex_id)["tile"]
        assert tile and tile["tile_type"] == "city" and tile["owner"] == pid, f"tile en {hex_id}: {tile}"
        page.screenshot(path=OUT / "02b_tablero.png")
    step("tablero: resalta lo que el motor permite y coloca una ciudad", board_city)
    step("el dashboard coincide con la API (después de la ciudad)", lambda: assert_ui_matches_api(page, pid))

    chat_available = True
    for i, msg in enumerate(CHAT_TURNS, 1):
        if not chat_available:
            record(f"chat {i}: {msg}", "SKIP", "sin ANTHROPIC_API_KEY valida en el backend")
            continue
        before = len(bad_responses)
        try:
            page.get_by_role("textbox", name="Mensaje para el árbitro").fill(msg, timeout=15_000)
            page.get_by_role("button", name="Enviar").click()
            expect(page.get_by_text(msg, exact=True).last).to_be_visible()
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

restored = global_parameters("restore")
record("tablero compartido restaurado", "OK" if restored == "True" else "FAIL", "" if restored == "True" else restored)

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
