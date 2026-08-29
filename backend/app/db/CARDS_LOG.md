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

## Descartadas (evaluadas, fuera de alcance del MVP actual)

| # scan | Nombre | Motivo |
|---|---|---|
| 071 | Advanced Alloys | Efecto pasivo que modifica el valor de venta de steel/titanio — no hay mecánica de "efectos pasivos permanentes" en el motor todavía. |
| 109 | Media Group | Depende de trackear cartas de tipo "evento" jugadas — no modelado. |
| 190 | Local Heat Trapping | Acción con elección (plantas O animales en otra carta) que además requiere targetear otra carta en juego — no modelado. |
| 014 | Development Center | Acción de gastar energía para robar carta — no hay sistema de mano/robo de cartas todavía. |

## Vocabulario de `effects` soportado hoy en `rules_engine.apply_card_effect`

- `mc_production_delta`: entero fijo sumado a la producción de MC.
- `mc_delta`: entero fijo sumado al stock de MC.
- `convert_production`: `{"from": "<recurso>_production", "to": "<recurso>_production"}`,
  convierte `effect_amount` (X, provisto por el jugador) pasos de un recurso a otro.

Antes de cargar una carta nueva: si su efecto no encaja en este vocabulario, hay
que extender `apply_card_effect` (con su test) antes de agregarla a `seed_cards.sql`.

## Fuente de verificación

Scans oficiales vía https://tm.hadronikle.com (base de datos no oficial de cartas,
668 escaneos full-res). Cada carta se lee directamente del scan antes de cargarla —
nunca de memoria — para no romper el objetivo de "100% de precisión" del PRD.
