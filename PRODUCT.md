# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Jugadores de Terraforming Mars en medio de una partida real, con el tablero físico delante. Consultan al árbitro mientras juegan, desde el celular o la laptop al lado de la mesa, para resolver cálculos de turno (pagos con acero/titanio, proyectos estándar, producción, subida de parámetros globales, colocación de tiles) sin hacer la cuenta a mano ni releer el reglamento.

## Product Purpose

El árbitro resuelve la contabilidad del juego: el jugador describe su jugada en lenguaje natural y recibe un veredicto (legal o no, cuánto cuesta, qué cambia) junto con su estado actualizado. Éxito es que el jugador confíe en el número sin verificarlo y vuelva al tablero en segundos.

## Positioning

El LLM nunca hace matemática: solo interpreta la intención y extrae argumentos; todo cálculo y validación lo hace un motor de reglas determinista en Python, testeado contra el reglamento oficial y con un catálogo verificado carta por carta contra los scans oficiales. Es también una pieza de portfolio que demuestra control arquitectónico estricto sobre un LLM probabilístico.

## Operating Context

- Partida estándar de un jugador (TR 20), con las expansiones Venus Next, Colonies, Prelude, Turmoil y promos; mapa Tharsis.
- Flujo típico de una generación: fase de investigación, acciones (jugar cartas, proyectos estándar, acciones de cartas activas, conversiones), fase de producción, y en Turmoil el nuevo gobierno.
- Interfaz actual: dashboard (parámetros globales, recursos y producción, TR, mano, cartas activas y jugadas) + chat con el árbitro. Backend FastAPI + LangGraph, base Supabase, frontend Next.js (App Router) + Tailwind.

## Capabilities and Constraints

- Catálogo cargado: 412 cartas de proyecto, 48 corporaciones, 70 preludes, 36 Global Events, 11 colonias.
- Todos los números que muestra la UI salen de la API (el motor); la UI nunca calcula.
- Un jugador nuevo arranca vacío (0 M€, sin corporación ni mano): hoy el setup de partida solo se hace por chat. Abierto: flujo de inicio de partida en la UI.
- Fuera de alcance: milestones/awards, mapas Hellas/Elysium, multijugador simultáneo, IA que juegue sola.

## Brand Commitments

- Nombre: **Árbitro de Terraforming Mars**. Sin logo propio.
- Proyecto de fans: sin afiliación con FryxGames. No se usan sus logos, su arte ni sus scans en la interfaz (los scans son material de trabajo con derechos de autor y nunca se commitean).
- Referencia visual elegida por el usuario para el rediseño de la app (2026-10-03): la plantilla Paymark de Lovable (https://lovable.dev/templates/websites/landing-page/paymark-template) — interfaz oscura con acentos coral, tipografía Inter Tight, botones tipo píldora con sombras en capas.

## Evidence on Hand

- Motor real con 718 tests y E2E de la UI con navegador real (`e2e/ui_e2e.py`).
- No hay testimonios, usuarios, métricas de uso ni prensa: no inventarlos.

## Product Principles

1. El número es del motor: la interfaz muestra resultados calculados, nunca estimaciones.
2. De vuelta al tablero en segundos: lo que el jugador necesita en la mesa (recursos, TR, parámetros) se lee de un vistazo.
3. Confianza verificable: cuando el árbitro rechaza o cobra algo, se entiende por qué.
4. Funciona en el celular al lado del tablero tanto como en la laptop.
