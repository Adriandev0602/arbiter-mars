---
name: Árbitro de Terraforming Mars
description: El tablero de cuentas de un jugador en la mesa; lo que el motor calculó se lee de un vistazo y cada cambio se ve.
colors:
  coral: "#ff6b4a"
  coral-bright: "#ff8467"
  coral-deep: "#e2502f"
  coral-ink: "#2b0b03"
  ground: "#0e0c0b"
  surface: "#171513"
  surface-raised: "#1f1c19"
  surface-sunk: "#121010"
  line: "rgb(255 240 225 / 0.08)"
  line-strong: "rgb(255 240 225 / 0.14)"
  ink: "#f5efe8"
  ink-muted: "#b0a69c"
  ink-faint: "#8f857b"
  res-mc: "#f2c14e"
  res-steel: "#c08a57"
  res-titanium: "#bdb5ac"
  res-plants: "#7cc463"
  res-energy: "#b083ee"
  res-heat: "#f0614f"
  track-temperature: "#e0634f"
  track-oxygen: "#8fc46b"
  track-oceans: "#4f9fe0"
  track-venus: "#d6a35c"
  good: "#7cc463"
  bad: "#ff7a66"
typography:
  display:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "4.5rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.035em"
    fontFeature: "\"tnum\""
  headline:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.035em"
    fontFeature: "\"tnum\""
  title:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.33
    letterSpacing: "-0.02em"
  card-name:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.625
    fontFeature: "\"ss01\", \"cv11\""
  label:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 500
  meta:
    fontFamily: "Inter Tight, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
rounded:
  track: "2px"
  bubble: "16px"
  cell-group: "12px"
  panel: "16px"
  pill: "9999px"
spacing:
  cell: "20px"
  cell-lg: "24px"
  stack: "24px"
  row: "12px"
components:
  button-primary:
    backgroundColor: "{colors.coral}"
    textColor: "{colors.coral-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "10px 20px"
  button-primary-hover:
    backgroundColor: "{colors.coral-bright}"
  button-primary-disabled:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink-faint}"
  button-quiet:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "8px 16px"
  icon-button:
    rounded: "{rounded.pill}"
    size: "40px"
  field:
    backgroundColor: "{colors.surface-sunk}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "10px 16px"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "24px"
  cost-chip:
    textColor: "{colors.res-mc}"
    rounded: "{rounded.pill}"
    padding: "2px 10px"
  before-chip:
    textColor: "{colors.coral-bright}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  chat-bubble-assistant:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.bubble}"
    padding: "10px 16px"
---

# Design System: Árbitro de Terraforming Mars

## Overview

**Creative North Star: "El libro de cuentas en la mesa"**

La interfaz es la hoja de cuentas de un jugador sentado a la mesa de Terraforming Mars, no un panel de métricas. Lo que el motor de reglas calculó se lee de un vistazo: TR y M€ en cifras enormes arriba a la izquierda, los otros cinco recursos al lado, la partida debajo, y a la derecha el chat con el árbitro, donde vive la acción primaria. Cada número que se muestra viene tal cual de la API; la interfaz nunca resta, suma ni deduce un valor del juego.

El mundo es grafito cálido casi negro, con un único acento coral reservado a dos cosas: lo que el jugador puede hacer (botón primario, pestaña activa, selección, paso actual) y lo que el motor acaba de cambiar. El resto del color pertenece al propio juego: dorado para M€, marrón para acero, verde para plantas, violeta para energía, rojo para calor, y en las pistas de parámetros globales los colores del tablero. Inter Tight con tracking cerrado lleva toda la jerarquía; las cifras del motor son siempre tabulares. Los botones son píldoras con sombra en capas (brillo interno arriba, sombra corta, halo cálido) tomadas de la referencia fijada por el usuario.

La densidad es de tablero, no de landing: celdas divididas por líneas de un píxel dentro de un solo contenedor, en lugar de una grilla de tarjetas iguales. El dashboard de tarjetas iguales es el anti-referente explícito.

**Key Characteristics:**
- Grafito cálido en tres niveles tonales (hundido, superficie, elevado) sobre un fondo casi negro.
- Coral solo para acción y cambio; todo otro color es semántica del juego.
- Cifras del motor grandes, semibold, tracking de display, tabulares.
- Listas como celdas divididas `gap-px` dentro de un contenedor, nunca tarjetas anidadas.
- El cambio se muestra con un pulso coral y el valor anterior del motor ("antes X"), sin mover el layout.

## Colors

Grafito cálido monocromo con un acento coral escaso y una paleta de recursos que es la del propio juego, apagada para fondo oscuro.

### Primary
- **Coral de acción** (`coral`): fondo del botón primario, subrayado de la pestaña activa, círculo del paso actual del setup, check de carta elegida, caret de texto, anillo de foco, spinner de carga.
- **Coral brillante** (`coral-bright`): hover del botón primario, texto del chip "antes X", primer cuadro del pulso de cambio de un número.
- **Coral profundo** (`coral-deep`): reserva oscura del acento.
- **Tinta sobre coral** (`coral-ink`): texto e íconos sobre relleno coral; nunca blanco sobre coral.
- Tintes de coral al 9-15% (`coral/[0.09]`, `coral/15`, `coral/[0.14]`) marcan carta seleccionada, fondo del chip "antes X" y burbuja del usuario en el chat. Borde coral al 50-60% es el hover de botones silenciosos y el foco de campos.

### Neutral
- **Suelo grafito** (`ground`): fondo de página y de la barra superior (al 90% con blur).
- **Superficie** (`surface`): paneles, celdas de listas, columna del chat.
- **Superficie elevada** (`surface-raised`): botón silencioso, burbuja del árbitro, botón primario deshabilitado.
- **Superficie hundida** (`surface-sunk`): campos de texto y sugerencias del chat.
- **Línea** (`line`) y **línea fuerte** (`line-strong`): crema translúcida; `line` es el fondo que asoma entre celdas `gap-px` y los divisores; `line-strong` es el borde de controles.
- **Tinta** (`ink`), **tinta apagada** (`ink-muted`), **tinta tenue** (`ink-faint`): texto principal, etiquetas y producción, metadatos y placeholders.

### Semántica del juego
- **Recursos** (`res-mc`, `res-steel`, `res-titanium`, `res-plants`, `res-energy`, `res-heat`): el punto de color junto a cada recurso; `res-mc` además tiñe la cifra grande de M€ y todo costo en M€.
- **Pistas del tablero** (`track-temperature`, `track-oxygen`, `track-oceans`, `track-venus`): las muescas alcanzadas de cada parámetro global.
- Los puntos de tags reutilizan los colores de recurso donde coinciden (building = acero, power = energía, plant = plantas) y hexadecimales propios del juego para el resto (earth, jovian, venus, microbe, animal, space con anillo dorado).
- **Bien** (`good`) para "acción disponible"; **mal** (`bad`) para errores, siempre como texto sobre su tinte al 10% con borde al 30%.

### Named Rules
**The Coral Is a Verb Rule.** Coral marca solo lo que se puede hacer o lo que acaba de cambiar. Un elemento estático, decorativo o informativo nunca es coral, aunque su color del juego se le parezca.

**The Board Owns Its Colors Rule.** Las pistas de parámetros globales y los recursos usan los colores del tablero, nunca el coral. La pista de temperatura es rojo de tablero (`track-temperature`), un hexadecimal distinto del coral, y debe seguir siéndolo.

## Typography

**Display Font:** Inter Tight (con ui-sans-serif, system-ui)
**Body Font:** Inter Tight
**Label/Mono Font:** la misma familia; las cifras usan `tabular-nums` mediante la clase `.num`.

**Character:** Una sola grotesca condensada de tracking cerrado; la jerarquía sale del tamaño y del peso, no de cambiar de familia. Cuerpo con alternativas estilísticas `ss01` y `cv11` activadas globalmente.

### Hierarchy
- **Display** (600, 3.75rem en celular / 4.5rem desde sm, line-height 1, -0.035em): solo TR y M€.
- **Headline** (600, 2.25rem, line-height 1, -0.035em): stock de los otros cinco recursos.
- **Title** (600, 1.5rem, -0.02em): título de cada paso del setup; 1.125rem para "Tenés cosas por resolver"; 1.25rem para el valor de cada parámetro global.
- **Card name** (500, 15px, -0.02em): nombre de carta en listas y selectores.
- **Body** (400, 0.875rem, line-height 1.625): mensajes del chat, explicaciones del setup (con `max-w-prose`).
- **Label** (500, 13px, `ink-muted`): etiqueta de cada recurso y parámetro, "producción +N".
- **Meta** (400, 0.75rem, `ink-faint`): tags, términos de Turmoil, "Probá con". El chip "antes X" baja a 11px.

### Named Rules
**The Tabular Engine Rule.** Todo número que sale del motor lleva `.num` (tabular). Las cifras no bailan cuando cambian.

**The Sentence-Case Rule.** Etiquetas en minúscula de oración, en español, sin mayúsculas sostenidas ni tracking abierto. No hay kickers ni eyebrows sobre los títulos.

## Layout

Dos columnas en escritorio (`lg`, 1024px): el dashboard a la izquierda, con scroll propio y un ancho máximo de 72rem (`max-w-6xl`) centrado, y el chat como columna fija de 400px a la derecha, separada por una línea, a pantalla completa de alto. Debajo de `lg` todo apila: barra, dashboard, chat.

La barra superior es sticky, de una sola fila, en todos los tamaños: "Árbitro" a la izquierda (el complemento "de Terraforming Mars" se oculta en celular), selector de jugador y botón de actualizar a la derecha.

El orden del dashboard es fijo: libro de recursos, luego lo pendiente o el paso de setup, luego la partida (parámetros globales y Turmoil), luego las cartas en pestañas. Los bloques se separan 24px (`gap-6`).

El libro de recursos es una grilla dividida: en `lg` dos zonas (1.15fr para TR y M€, 2fr para los cinco recursos en cinco columnas); en celular TR y M€ en dos columnas y los cinco recursos en dos. Los parámetros globales van en cuatro columnas desde `md`, dos en celular.

Ritmo: celdas con 20px de padding interior (24px desde `sm`), filas de lista con 12-14px vertical, separación de bloques 24px.

En celular la caja del chat queda fija abajo (`fixed bottom-0`, superficie al 95% con blur) y el contenido reserva 68px para no quedar tapado.

### Named Rules
**The Ledger Order Rule.** TR y M€ arriba a la izquierda, grandes, con su producción; nada se interpone por encima del libro de recursos.

## Elevation & Depth

Sistema híbrido: la profundidad estructural es tonal (hundido, superficie, elevado sobre el suelo grafito) y las sombras son materiales, no de estado. Los paneles llevan una sombra baja con brillo interno en el borde superior; las píldoras llevan sombra en capas. Las celdas internas no tienen sombra propia: se separan con la línea que asoma entre ellas.

### Shadow Vocabulary
- **Panel** (`box-shadow: inset 0 1px 0 rgb(255 240 225 / 0.05), 0 1px 2px rgb(0 0 0 / 0.5), 0 18px 40px -24px rgb(0 0 0 / 0.8)`): todo contenedor `.panel`.
- **Píldora** (`box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.35), inset 0 -1px 0 rgb(0 0 0 / 0.18), 0 1px 2px rgb(0 0 0 / 0.45), 0 10px 24px -10px rgb(255 107 74 / 0.6)`): solo el botón primario coral; el halo es coral porque el botón es acción.
- **Píldora silenciosa** (`box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.07), 0 1px 2px rgb(0 0 0 / 0.5)`): botones silenciosos y primario deshabilitado.

### Named Rules
**The One Container Rule.** Un panel es la única superficie con sombra en su zona. Lo que vive adentro se divide con líneas de un píxel, nunca con tarjetas anidadas con sombra o borde propio.

## Shapes

Tres formas: píldora completa para todo lo que se toca o se lee como valor suelto (botones, campos, chips de costo, chip "antes X", tags de tipo de carta); rectángulo suave de 16px para paneles y burbujas de chat; 12px para grupos de celdas dentro de un panel y sugerencias del chat. Las muescas de las pistas de parámetros tienen 2px, una por paso, separadas 3px, como las casillas del tablero. Las burbujas de chat recortan la esquina del lado de quien habla (6px abajo a la derecha para el usuario, abajo a la izquierda para el árbitro). Los puntos de tag y de recurso son círculos de 8-10px.

## Components

### Buttons
Táctiles y seguros, de la familia de la referencia.
- **Shape:** píldora completa (9999px).
- **Primary:** relleno coral, texto `coral-ink` semibold de 14px, 10px × 20px, sombra Píldora. Uno por zona: confirmar el paso de setup, crear jugador, enviar al árbitro.
- **Hover / Focus:** hover pasa a `coral-bright`; al presionar baja 1px; foco con contorno coral de 2px y 2px de separación. Transiciones de 200ms ease-out.
- **Disabled:** superficie elevada, tinta tenue, sombra silenciosa.
- **Quiet:** superficie elevada, borde `line-strong`, texto `ink` medium, 8px × 16px, sombra silenciosa; hover vuelve el borde coral al 50%. Para "Jugar", "Nuevo", acciones secundarias.
- **Icon button:** primario o silencioso de 40 × 40, ícono lucide de 16-18px (actualizar, enviar).

### Chips
- **Costo:** `res-mc` sobre su tinte al 10%, píldora, semibold 14px, "N M€".
- **Tipo de carta:** borde `line-strong`, texto 11px apagado ("Corporación", "Prelude"). "Evento" va en `bad` sobre su tinte.
- **"antes X":** ver componente distintivo.

### Cards / Containers
- **Corner Style:** 16px.
- **Background:** `surface`, borde `line`.
- **Shadow Strategy:** sombra Panel (ver Elevation & Depth).
- **Internal Padding:** 20px, 24px desde `sm`; los pasos de setup llegan a 32px.

### Lists de celdas divididas
Selector de cartas, preludes pendientes y grillas de setup: un contenedor de 12px con borde `line` y fondo `line`, con celdas `surface` separadas por `gap-px`, en una columna o dos desde `sm` (una celda impar final ocupa ambas columnas). La lista de mano, activas y jugadas usa divisores `line` entre filas. La celda elegida toma tinte coral al 9% y un check coral relleno; las no elegibles bajan a 40% de opacidad.

### Inputs / Fields
- **Style:** píldora, `surface-sunk`, borde `line-strong`, 10px × 16px, texto 14px, placeholder `ink-faint`.
- **Focus:** el borde pasa a coral al 60%, sin outline extra.
- **Disabled:** placeholder explica qué falta ("Elegí un jugador primero").

### Navigation
- **Pestañas de cartas:** texto 14px medium, activa en `ink` con subrayado coral de 2px redondeado, inactivas en `ink-faint` (hover `ink-muted`); el conteo entre paréntesis va tabular y tenue.
- **Pasos del setup:** círculos numerados unidos por una línea de 24px; hecho en tinte coral, actual en coral relleno, pendiente en blanco al 6%.

### Chat
Columna `surface`. Encabezado "Árbitro" con una línea de explicación. Sugerencias como filas de 12px de radio en `surface-sunk`. Burbujas hasta 88% de ancho: usuario a la derecha en tinte coral al 14%; árbitro a la izquierda en `surface-raised`; error en `bad` sobre su tinte. Cargando: spinner coral y "El árbitro está calculando…".

### Pistas de parámetros globales
Una muesca por paso real del parámetro (19 de temperatura, 14 de oxígeno, 9 de océanos, 15 de Venus), alcanzadas en el color del tablero y el resto en blanco al 7%. Valor a la derecha de la etiqueta en 20px semibold con unidad; el máximo ("/ 8°C") aparece en tenue solo desde `xl`.

### Mapa de Marte (`MarsBoard`)
- **Forma:** hexágonos SVG con punta arriba sobre un disco de óxido muy tenue (`#3a1d14` → transparente).
- **Hexágonos vacíos:** la tierra es `#2a1a14`; la reserva de océano es `#132634` con borde azul.
  Noctis lleva borde punteado.
- **Tiles:** usan los colores del tablero, igual que las pistas: océano `#4f9fe0`, greenery
  `#7cb35f`, ciudad `#aaa39b` y especial `#c08a57`, con un ícono oscuro encima.
- **Bonus impreso:** un ícono por unidad, como en el tablero físico, con los colores de recurso.
- **El coral es solo "legal ahora":**
  - Al elegir una jugada, los hexágonos que el motor permite llevan un borde coral al 50%.
  - Al pasar o elegir uno, el borde se enciende; el resto baja al 30% de opacidad.
  - Sin jugada elegida no hay coral en el mapa.
- **Tile recién colocado:** entra con `tile-in` (escala desde 0.55 y borde coral que se apaga).
  Es la versión espacial del pulso de "antes X".

### Número del motor con "antes X" (componente distintivo)
Cuando una lectura de la API cambia un número respecto de la lectura anterior del mismo ámbito (jugador o partida), el número se vuelve a montar y late: arranca en `coral-bright` y vuelve a su color propio en 1600ms (`cubic-bezier(0.16, 1, 0.3, 1)`). A su lado aparece el valor anterior que devolvió el motor, "antes X", como píldora de 11px en `coral-bright` sobre coral al 15%, que entra en 220ms subiendo 6px desde 92% de escala con un desenfoque de 2px. Queda visible hasta el próximo cambio o hasta cambiar de jugador. La producción muestra "(antes +N)" en línea, en el renglón que ya le pertenece.

**The No Arithmetic Rule.** La UI guarda el número anterior que devolvió el motor; nunca calcula una diferencia, un total ni un valor del juego.

**The Zero-Layout Delta Rule.** El chip "antes X" nunca ocupa lugar: va superpuesto en absoluto en una esquina de su celda o en un hueco que la fila ya reserva. Aparecer o irse no mueve nada.

## Do's and Don'ts

### Do:
- **Do** reservar coral (`#ff6b4a`) para acción y cambio: botón primario, pestaña activa, selección, paso actual, pulso y chip "antes X".
- **Do** pintar recursos, costos y pistas con los colores del juego (`res-*`, `track-*`).
- **Do** poner cada lista dentro de un solo contenedor como celdas `gap-px` sobre fondo `line`.
- **Do** marcar con `.num` toda cifra del motor y mostrarla tal cual llega de la API.
- **Do** mostrar el cambio con el pulso coral y "antes X" superpuesto, sin desplazar el layout.
- **Do** usar píldoras completas con sombra en capas para botones y campos, y paneles de 16px con la sombra Panel.
- **Do** mantener en celular la barra sticky en una fila y la caja del chat fija abajo.

### Don't:
- **Don't** construir un dashboard de tarjetas iguales ni anidar tarjetas con borde o sombra dentro de un panel.
- **Don't** usar coral para datos estáticos, decoración o una pista de parámetro global.
- **Don't** calcular, restar ni sumar valores del juego en el frontend, ni siquiera para mostrar una diferencia.
- **Don't** dejar que "antes X" empuje filas o cambie la altura de una celda.
- **Don't** poner kickers, eyebrows ni etiquetas en mayúsculas con tracking abierto sobre los títulos.
- **Don't** poner texto blanco sobre coral; va `coral-ink`.
