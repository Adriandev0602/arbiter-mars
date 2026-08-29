# Registro de cartas cargadas

Control de qué cartas del catálogo (~668 en la base de tm.hadronikle.com, ~200 son
de proyecto) ya están en `seed_cards.sql` con efecto implementado y testeado, para
no reverificar ni repetir trabajo en sesiones futuras.

No borrar filas al implementar una carta nueva — solo agregar. Si una carta se
descarta (efecto fuera de alcance del MVP), déjala en "Descartadas" con el motivo,
así no se vuelve a evaluar de cero.

## Cargadas (en `seed_cards.sql`, con efecto en `apply_card_effect` y test)

| id | Nombre | # scan | Costo | Efecto |
|---|---|---|---|---|
| `sponsors` | Sponsors | 068 | 6 MC | +2 producción MC |
| `acquired_company` | Acquired Company | 106 | 10 MC | +3 producción MC |
| `investment_loan` | Investment Loan | 151 | 3 MC | -1 producción MC, +10 MC |
| `insulation` | Insulation | 152 | 2 MC | -X producción calor, +X producción MC (X a elección) |
| `nuclear_power` | Nuclear Power | 045 | 10 MC | -2 producción MC, +3 producción energía |
| `solar_power` | Solar Power | 113 | 11 MC | +1 producción energía |
| `titanium_mine` | Titanium Mine | 144 | 7 MC | +1 producción titanio |
| `solar_wind_power` | Solar Wind Power | 077 | 11 MC | +1 producción energía, +2 titanio (stock) |
| `artificial_photosynthesis` | Artificial Photosynthesis | 115 | 12 MC | Elección: +1 producción plantas O +2 producción energía |

## Descartadas (evaluadas, fuera de alcance del MVP actual)

| # scan | Nombre | Motivo |
|---|---|---|
| 071 | Advanced Alloys | Efecto pasivo que modifica el valor de venta de steel/titanio — no hay mecánica de "efectos pasivos permanentes" en el motor todavía. |
| 109 | Media Group | Depende de trackear cartas de tipo "evento" jugadas — no modelado. |
| 190 | Local Heat Trapping | Acción con elección (plantas O animales en otra carta) que además requiere targetear otra carta en juego — no modelado. |
| 014 | Development Center | Acción de gastar energía para robar carta — no hay sistema de mano/robo de cartas todavía. |
| 011 | Big Asteroid | "Remove up to 4 plants from any player" requiere targetear a otro jugador — no hay modelo multi-jugador todavía. |
| 101 | Ironworks | Acción repetible (gastar energía cada turno), no efecto inmediato al jugar — no hay sistema de "acciones de carta activa" todavía. |
| 103 | Steelworks | Mismo motivo que Ironworks. |
| 038 | Rover Construction | Efecto pasivo disparado por colocación de tile de ciudad de cualquier jugador — no modelado (sin tracking de tiles). |

## Vocabulario de `effects` soportado hoy en `rules_engine.apply_card_effect`

- `mc_production_delta` / `mc_delta`: formas antiguas (solo MC), mantenidas por compatibilidad.
- `production_deltas`: `{"<recurso>_production": delta, ...}` — forma genérica para cambiar
  una o más producciones a la vez (ej. Nuclear Power).
- `resource_deltas`: `{"<recurso>": delta, ...}` — forma genérica para cambiar stock de uno
  o más recursos (ej. Solar Wind Power).
- `convert_production`: `{"from": "<recurso>_production", "to": "<recurso>_production"}`,
  convierte `effect_amount` (X, provisto por el jugador) pasos de un recurso a otro.
- `choice`: lista de sub-effects (cualquiera de los de arriba); el jugador elige uno vía
  `effect_choice` (índice 0-based) (ej. Artificial Photosynthesis).

Para cartas nuevas preferí `production_deltas`/`resource_deltas` sobre las formas antiguas
(son más generales). Si el efecto no encaja en este vocabulario, hay que extenderlo (con su
test) antes de agregar la carta a `seed_cards.sql`.

## Fuente de verificación

Scans oficiales vía https://tm.hadronikle.com (base de datos no oficial de cartas,
668 escaneos full-res). Cada carta se lee directamente del scan antes de cargarla —
nunca de memoria — para no romper el objetivo de "100% de precisión" del PRD.
