# Cartas descargadas, pendientes de revisión

**DEPRECADO desde 2026-08-31** — este archivo quedó congelado en el bloque 10. La cola de
revisión real ahora vive en la tabla `card_review_queue` de Supabase (poblada por
`backend/scripts/enqueue_card_review_queue.py`, marcada por `backend/scripts/mark_reviewed.py`
al cargar cada carta). Consultar `select * from card_review_queue where reviewed = false order
by id limit 10` para el próximo bloque, no este archivo. Se deja como referencia histórica de
cómo se llegó hasta acá.

Cartas cuyo scan ya se descargó de tm.hadronikle.com (prueba de capacidad de scraping
espaciado) pero cuya lógica **todavía no se leyó ni se implementó**. No confundir con
`CARDS_LOG.md` (cartas ya cargadas y verificadas) ni con la sección "Pendientes" de ese mismo
archivo (cartas ya revisadas a las que les falta una pieza de mecánica).

Estado de cada fila: `unreviewed` (default) hasta que una sesión futura lea el scan, decida
el vocabulario de `effects`/`requirements`/`action` que le corresponde, la mueva a
`seed_cards.sql` con su test, y la registre en `CARDS_LOG.md` (borrándola de acá).

No se commitean las imágenes de los scans (son escaneos con derechos de autor de FryxGames,
pesan ~8MB c/u) — solo este manifiesto con nombre/expansión/número, para volver a descargar
puntualmente cuando se revise cada una.

Fuente: https://tm.hadronikle.com (base de datos no oficial, 668 escaneos full-res).

**Prueba de capacidad de scraping (2026-08-29):** 3 tandas espaciadas, 402/402 descargas
exitosas (HTTP 200), 0 fallos, sin señales de bloqueo — incluso ajustando el espaciado de
2.5s a 1.5s entre pedidos. Con esto quedó descargada (sin revisar) prácticamente toda la
categoría "Project" del catálogo que faltaba. Conclusión: el sitio tolera bien este volumen
espaciado; no hace falta seguir con más tandas de prueba, el cuello de botella real de acá
en adelante es el trabajo de revisión (leer cada scan y decidir su `effects`), no la descarga.

**Bloque 1 revisado (2026-08-29):** cartas #1-10 ya procesadas y sacadas de esta tabla — 8
cargadas en `seed_cards.sql` (Martian Rails, Capital, Asteroid, Comet, Big Asteroid, Water
Import from Europa, Space Elevator, Equatorial Magnetizer) y 2 movidas a "Pendientes" en
`CARDS_LOG.md` (Inventors' Guild, Development Center — necesitan sistema de mazo/robo).

**Bloque 2 revisado (2026-08-29):** cartas #1-10 (Domed Crater, Noctis City, Methane from
Titan, Imported Hydrogen, Research Outpost, Phobos Space Haven, Black Polar Dust, Arctic
Algae, Predators, Space Station) ya procesadas y sacadas de esta tabla — 8 cargadas, 2
movidas a "Pendientes" en `CARDS_LOG.md` (Imported Hydrogen, Predators — necesitan mover
recursos hacia/desde otra carta específica, misma pieza que Local Heat Trapping).

**Bloque 3 revisado (2026-08-29):** cartas #1-10 (Eos Chasma National Park, Interstellar
Colony Ship, Security Fleet, Cupola City, Lunar Beam, Optimal Aerobraking — ya estaba cargada
de antes —, Underground City, GHG Producing Bacteria, Ants, Release of Inert Gases) ya
procesadas y sacadas de esta tabla — 7 cargadas, 2 movidas a "Pendientes" (Eos Chasma
National Park, Ants — misma pieza de targeting entre cartas).

**Bloque 4 revisado (2026-08-31):** cartas #1-10 (Nitrogen-Rich Asteroid, Rover Construction,
Deimos Down, Asteroid Mining, Food Factory, Archaebacteria, Carbonate Processing, Natural
Preserve, Lightning Harvest, Algae) ya procesadas y sacadas de esta tabla — 8 cargadas, 1
movida a "Fuera de alcance" en `CARDS_LOG.md` (Rover Construction — ya estaba documentada ahí
desde antes: depende de colocación de tile de ciudad de cualquier jugador, multi-jugador).
Única extensión al motor: `tag_count_choice` en `apply_card_effect` (Nitrogen-Rich Asteroid:
rama automática por conteo de tags, no por elección del jugador — distinta de `choice`).

**Bloque 5 revisado (2026-08-31):** cartas #1-10 (Adapted Lichen, Tardigrades, Virus, Miranda
Resort, Fish, Lake Marineris, Small Animals, Kelp Farming, Vesta Shipyard, Beam from a Thorium
Asteroid) ya procesadas y sacadas de esta tabla — las 10 cargadas (Virus con `effects: {}`,
toda su carta es la cláusula opcional "remove up to" que se omite). Única extensión al motor:
`production_delta_per_tag` en `apply_card_effect` (Miranda Resort: producción que escala
linealmente con la cantidad de tags earth jugados, sin umbral — distinta de
`tag_count_choice`).

**Bloque 6 revisado (2026-08-31):** cartas #1-10 (Mangrove, Trees, Great Escarpment
Consortium, Mineral Deposit, Mining Expedition, Mining Area, Building Industries, Land Claim,
Mining Rights, Electro Catapult) ya procesadas y sacadas de esta tabla — 7 cargadas
(Mangrove incluida: su restricción de colocación es irrelevante sin mapa modelado, se reduce
a "+1 paso oxígeno"), 3 movidas a "Pendientes" en `CARDS_LOG.md` (Mining Area, Land Claim,
Mining Rights — primeras cartas que genuinamente necesitan el mapa hexagonal; investigación
de esa mecánica documentada en `HEX_MAP_RESEARCH.md`, todavía sin implementar). Única
extensión al motor: requisito `min_production` en `check_card_requirements` (Great Escarpment
Consortium: requiere tener producción propia de un recurso, no solo tags o parámetros
globales). Nota: bloque 6 fue seguido de la implementación completa del mapa hexagonal y su
cableado a `tools.py` (ver commits `cb23238`, `d1daafd`, `93be43c`) antes de seguir con el
bloque 7 — Mining Area, Mining Rights y Land Claim quedaron cargadas ahí, ya no están
pendientes.

**Bloque 7 revisado (2026-08-31):** cartas #1-10 (Earth Catapult, Advanced Alloys, Birds, Mars
University, Viral Enhancers, Towing a Comet, Space Mirrors, Ice Asteroid, Quantum Extractor,
Giant Ice Asteroid) ya procesadas y sacadas de esta tabla — Advanced Alloys era un duplicado
(ya estaba cargada desde antes, no se reprocesó), 8 cargadas, 1 movida a "Pendientes"
(Viral Enhancers — misma pieza de targeting entre cartas que Local Heat Trapping y las
demás). Única extensión al motor: pasivo `on_tag_played_may_swap_card` (Mars University: a
diferencia de `on_event_played`, dispara con cualquier carta de un tag dado, y es una
elección opcional del jugador, no automática).

**Bloque 8 revisado (2026-08-31):** cartas #1-10 (Ganymede Colony, Callisto Penal Mines,
Giant Space Mirror, Trans-Neptune Probe, Commercial District, Robotic Workforce, Grass,
Heather, Peroxide Power, Research) ya procesadas y sacadas de esta tabla — 9 cargadas
(Ganymede Colony y Trans-Neptune Probe con `effects: {}`, solo dan puntos no trackeados), 1
movida a "Pendientes" (Robotic Workforce — pieza nueva y distinta a la de targeting: requiere
un historial de cartas jugadas por el jugador para poder "duplicar" la producción de una).
Única extensión al motor: `draw_cards` en `apply_card_effect` (Research: +2 cartas como
efecto inmediato, ya existía para `use_card_action` pero no para jugar una carta directo).

**Robotic Workforce implementada (2026-08-31, fuera del ritmo de bloques):** se agregó
`played_cards` (historial permanente de cartas jugadas) y el vocabulario `duplicate_production`
para desbloquearla — ver commit `599a53d` y la sección "Historial de cartas jugadas" en
`CARDS_LOG.md`.

**Bloque 9 revisado (2026-08-31):** cartas #1-10 (Gene Repair, IO Mining Industries, Bushes,
Mass Converter, Physics Complex, Greenhouses, Nuclear Zone, Tropical Resort, Toll Station,
Fueled Generators) ya procesadas y sacadas de esta tabla — Mass Converter era un duplicado
(ya estaba cargada desde antes, no se reprocesó), las 9 restantes cargadas (Toll Station con
`effects: {}`: depende de tags de OPONENTES, que en single-player son siempre 0, así que no
es que falte modelar nada — el efecto se resuelve matemáticamente a cero). Única extensión al
motor: `resource_delta_per_counter` en `apply_card_effect` (Greenhouses: +1 planta por cada
ciudad colocada, análogo a `mc_per_counter` de `use_card_action` pero para cualquier recurso).

**Bloque 10 revisado (2026-08-31):** cartas #1-10 (Power Grid, Ore Processor, Earth Office,
Media Archives, Open City, Media Group, Business Network, Business Contacts, Bribed
Committee, Breathing Filters) ya procesadas y sacadas de esta tabla — Media Group era un
duplicado (ya estaba cargada desde antes, no se reprocesó), las 9 restantes cargadas.
Extensiones al motor: contador global `events_played` + `increment_events_played` (Media
Archives, vía `resource_delta_per_counter`); `start_research` en `apply_card_effect` +
parámetro `max_take` nuevo en `resolve_research_phase` (Business Contacts: roba 4, exige
tomar EXACTAMENTE 2). Power Grid ("+1 energía por cada tag power, incluida esta") no
necesitó pieza nueva: se resuelve combinando `production_delta_per_tag` + `production_deltas`
en el mismo `effects`.

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Artificial Lake | Base | 116 | unreviewed |
| 2 | Geothermal Power | Base | 117 | unreviewed |
| 3 | Dust Seals | Base | 119 | unreviewed |
| 4 | Urbanized Area | Base | 120 | unreviewed |
| 5 | Sabotage | Corporate Era | 121 | unreviewed |
| 6 | Moss | Base | 122 | unreviewed |
| 7 | Industrial Center | Corporate Era | 123 | unreviewed |
| 8 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 9 | Hackers | Corporate Era | 125 | unreviewed |
| 10 | GHG Factories | Base | 126 | unreviewed |
| 11 | Subterranean Reservoir | Base | 127 | unreviewed |
| 12 | Ecological Zone | Base | 128 | unreviewed |
| 13 | Zeppelins | Base | 129 | unreviewed |
| 14 | Worms | Base | 130 | unreviewed |
| 15 | Decomposers | Base | 131 | unreviewed |
| 16 | Fusion Power | Base | 132 | unreviewed |
| 17 | Symbiotic Fungus | Base | 133 | unreviewed |
| 18 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 19 | Advanced Ecosystems | Base | 135 | unreviewed |
| 20 | Great Dam | Base | 136 | unreviewed |
| 21 | Cartel | Corporate Era | 137 | unreviewed |
| 22 | Strip Mine | Base | 138 | unreviewed |
| 23 | Wave Power | Base | 139 | unreviewed |
| 24 | Lava Flows | Base | 140 | unreviewed |
| 25 | Power Plant | Base | 141 | unreviewed |
| 26 | Mohole Area | Base | 142 | unreviewed |
| 27 | Large Convoy | Base | 143 | unreviewed |
| 28 | Tectonic Stress Power | Base | 145 | unreviewed |
| 29 | Herbivores | Base | 147 | unreviewed |
| 30 | Insects | Base | 148 | unreviewed |
| 31 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 32 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 33 | Adaptation Technology | Base | 153 | unreviewed |
| 34 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 35 | Designed Microorganisms | Base | 155 | unreviewed |
| 36 | Standard Technology | Corporate Era | 156 | unreviewed |
| 37 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 38 | Industrial Microbes | Base | 158 | unreviewed |
| 39 | Lichen | Base | 159 | unreviewed |
| 40 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 41 | Convoy from Europa | Base | 161 | unreviewed |
| 42 | Imported GHG | Base | 162 | unreviewed |
| 43 | Imported Nitrogen | Base | 163 | unreviewed |
| 44 | Micro-Mills | Base | 164 | unreviewed |
| 45 | Magnetic Field Generators | Base | 165 | unreviewed |
| 46 | Shuttles | Base | 166 | unreviewed |
| 47 | Import of Advanced GHG | Base | 167 | unreviewed |
| 48 | Windmills | Base | 168 | unreviewed |
| 49 | Tundra Farming | Base | 169 | unreviewed |
| 50 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 51 | Magnetic Field Dome | Base | 171 | unreviewed |
| 52 | Pets | Base | 172 | unreviewed |
| 53 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 54 | Protected Valley | Base | 174 | unreviewed |
| 55 | Satellites | Corporate Era | 175 | unreviewed |
| 56 | Noctis Farming | Base | 176 | unreviewed |
| 57 | Water Splitting Plant | Base | 177 | unreviewed |
| 58 | Heat Trappers | Base | 178 | unreviewed |
| 59 | Soil Factory | Base | 179 | unreviewed |
| 60 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 61 | Ice Cap Melting | Base | 181 | unreviewed |
| 62 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 63 | Biomass Combustors | Base | 183 | unreviewed |
| 64 | Livestock | Base | 184 | unreviewed |
| 65 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 66 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 67 | Aquifer Pumping | Base | 187 | unreviewed |
| 68 | Flooding | Base | 188 | unreviewed |
| 69 | Energy Saving | Base | 189 | unreviewed |
| 70 | Local Heat Trapping | Base | 190 | unreviewed |
| 71 | Permafrost Extraction | Base | 191 | unreviewed |
| 72 | Invention Contest | Corporate Era | 192 | unreviewed |
| 73 | Plantation | Base | 193 | unreviewed |
| 74 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 75 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 76 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 77 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 78 | Immigration Shuttles | Base | 198 | unreviewed |
| 79 | Restricted Area | Corporate Era | 199 | unreviewed |
| 80 | Immigrant City | Base | 200 | unreviewed |
| 81 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 82 | Underground Detonations | Base | 202 | unreviewed |
| 83 | Soletta | Base | 203 | unreviewed |
| 84 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 85 | Rad-Chem Factory | Base | 205 | unreviewed |
| 86 | Special Design | Base | 206 | unreviewed |
| 87 | Medical Lab | Corporate Era | 207 | unreviewed |
| 88 | AI Central | Corporate Era | 208 | unreviewed |
| 89 | Small Asteroid | Promo | 209 | unreviewed |
| 90 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 91 | Snow Algae | Promo | 211 | unreviewed |
| 92 | Penguins | Promo | 212 | unreviewed |
| 93 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 94 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 95 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 96 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 97 | Atmoscoop | Venus Next | 217 | unreviewed |
| 98 | Comet for Venus | Venus Next | 218 | unreviewed |
| 99 | Corroder Suits | Venus Next | 219 | unreviewed |
| 100 | Dawn City | Venus Next | 220 | unreviewed |
| 101 | Deuterium Export | Venus Next | 221 | unreviewed |
| 102 | Dirigibles | Venus Next | 222 | unreviewed |
| 103 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 104 | Extremophiles | Venus Next | 224 | unreviewed |
| 105 | Floating Habs | Venus Next | 225 | unreviewed |
| 106 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 107 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 108 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 109 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 110 | Gyropolis | Venus Next | 230 | unreviewed |
| 111 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 112 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 113 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 114 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 115 | Local Shading | Venus Next | 235 | unreviewed |
| 116 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 117 | Luxury Foods | Venus Next | 237 | unreviewed |
| 118 | Maxwell Base | Venus Next | 238 | unreviewed |
| 119 | Mining Quota | Venus Next | 239 | unreviewed |
| 120 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 121 | Omnicourt | Venus Next | 241 | unreviewed |
| 122 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 123 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 124 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 125 | Solarnet | Venus Next | 245 | unreviewed |
| 126 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 127 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 128 | Stratopolis | Venus Next | 248 | unreviewed |
| 129 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 130 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 131 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 132 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 133 | Thermophiles | Venus Next | 253 | unreviewed |
| 134 | Water to Venus | Venus Next | 254 | unreviewed |
| 135 | Venus Governor | Venus Next | 255 | unreviewed |
| 136 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 137 | Venus Soils | Venus Next | 257 | unreviewed |
| 138 | Venus Waystation | Venus Next | 258 | unreviewed |
| 139 | Venusian Animals | Venus Next | 259 | unreviewed |
| 140 | Venusian Insects | Venus Next | 260 | unreviewed |
| 141 | Venusian Plants | Venus Next | 261 | unreviewed |
| 142 | Airliners | Colonies | C01 | unreviewed |
| 143 | Air Raid | Colonies | C02 | unreviewed |
| 144 | Atmo Collectors | Colonies | C03 | unreviewed |
| 145 | Community Services | Colonies | C04 | unreviewed |
| 146 | Conscription | Colonies | C05 | unreviewed |
| 147 | Corona Extractor | Colonies | C06 | unreviewed |
| 148 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 149 | Earth Elevator | Colonies | C08 | unreviewed |
| 150 | Ecology Research | Colonies | C09 | unreviewed |
| 151 | Floater Leasing | Colonies | C10 | unreviewed |
| 152 | Floater Prototypes | Colonies | C11 | unreviewed |
| 153 | Floater Technology | Colonies | C12 | unreviewed |
| 154 | Galilean Waystation | Colonies | C13 | unreviewed |
| 155 | Heavy Taxation | Colonies | C14 | unreviewed |
| 156 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 157 | Impactor Swarm | Colonies | C16 | unreviewed |
| 158 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 159 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 160 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 161 | Luna Governor | Colonies | C20 | unreviewed |
| 162 | Lunar Exports | Colonies | C21 | unreviewed |
| 163 | Lunar Mining | Colonies | C22 | unreviewed |
| 164 | Market Manipulation | Colonies | C23 | unreviewed |
| 165 | Martian Zoo | Colonies | C24 | unreviewed |
| 166 | Mining Colony | Colonies | C25 | unreviewed |
| 167 | Minority Refuge | Colonies | C26 | unreviewed |
| 168 | Molecular Printing | Colonies | C27 | unreviewed |
| 169 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 170 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 171 | Productive Outpost | Colonies | C30 | unreviewed |
| 172 | Quantum Communications | Colonies | C31 | unreviewed |
| 173 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 174 | Refugee Camps | Colonies | C33 | unreviewed |
| 175 | Research Colony | Colonies | C34 | unreviewed |
| 176 | Rim Freighters | Colonies | C35 | unreviewed |
| 177 | Sky Docks | Colonies | C36 | unreviewed |
| 178 | Solar Probe | Colonies | C37 | unreviewed |
| 179 | Solar Reflectors | Colonies | C38 | unreviewed |
| 180 | Space Port | Colonies | C39 | unreviewed |
| 181 | Space Port Colony | Colonies | C40 | unreviewed |
| 182 | Spin-Off Department | Colonies | C41 | unreviewed |
| 183 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 184 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 185 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 186 | Titan Shuttles | Colonies | C45 | unreviewed |
| 187 | Trade Envoys | Colonies | C46 | unreviewed |
| 188 | Trading Colony | Colonies | C47 | unreviewed |
| 189 | Urban Decomposers | Colonies | C48 | unreviewed |
| 190 | Warp Drive | Colonies | C49 | unreviewed |
| 191 | House Printing | Prelude | P36 | unreviewed |
| 192 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 193 | Martian Survey | Prelude | P38 | unreviewed |
| 194 | Psychrophiles | Prelude | P39 | unreviewed |
| 195 | Research Coordination | Prelude | P40 | unreviewed |
| 196 | SF Memorial | Prelude | P41 | unreviewed |
| 197 | Space Hotels | Prelude | P42 | unreviewed |
| 198 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 199 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 200 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 201 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 202 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 203 | Floating Refinery | Venus Next | P73 | unreviewed |
| 204 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 205 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 206 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 207 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 208 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 209 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 210 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 211 | Soil Studies | Venus Next | P81 | unreviewed |
| 212 | Special Permit | Prelude 2 | P82 | unreviewed |
| 213 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 214 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 215 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 216 | Unexpected Application | Venus Next | P86 | unreviewed |
| 217 | Venus Allies | Venus Next | P87 | unreviewed |
| 218 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 219 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 220 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 221 | WG Project | Prelude 2 | P91 | unreviewed |
| 222 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 223 | Banned Delegate | Turmoil | T02 | unreviewed |
| 224 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 225 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 226 | Event Analysts | Turmoil | T05 | unreviewed |
| 227 | GMO Contract | Turmoil | T06 | unreviewed |
| 228 | Martian Media Center | Turmoil | T07 | unreviewed |
| 229 | Parliament Hall | Turmoil | T08 | unreviewed |
| 230 | PR Office | Turmoil | T09 | unreviewed |
| 231 | Public Celebrations | Turmoil | T10 | unreviewed |
| 232 | Recruitment | Turmoil | T11 | unreviewed |
| 233 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 234 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 235 | Supported Research | Turmoil | T14 | unreviewed |
| 236 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 237 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 238 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 239 | Project Inspection | Promo | X02 | unreviewed |
| 240 | Energy Market | Promo | X03 | unreviewed |
| 241 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 242 | Interplanetary Trade | Promo | X05 | unreviewed |
| 243 | Law Suit | Promo | X06 | unreviewed |
| 244 | Mercurian Alloys | Promo | X07 | unreviewed |
| 245 | Orbital Cleanup | Promo | X08 | unreviewed |
| 246 | Political Alliance | Promo | X09 | unreviewed |
| 247 | Rego Plastics | Promo | X10 | unreviewed |
| 248 | Saturn Surfing | Promo | X11 | unreviewed |
| 249 | Stanford Torus | Promo | X12 | unreviewed |
| 250 | Advertising | Promo | X13 | unreviewed |
| 251 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 252 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 253 | Comet Aiming | Promo | X16 | unreviewed |
| 254 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 255 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 256 | Directed Impactors | Promo | X19 | unreviewed |
| 257 | Diversity Support | Promo | X20 | unreviewed |
| 258 | Field-Capped City | Promo | X21 | unreviewed |
| 259 | Imported Nutrients | Promo | X22 | unreviewed |
| 260 | Jovian Embassy | Promo | X23 | unreviewed |
| 261 | Magnetic Shield | Promo | X24 | unreviewed |
| 262 | Meat Industry | Promo | X25 | unreviewed |
| 263 | Meltworks | Promo | X26 | unreviewed |
| 264 | Mohole Lake | Promo | X27 | unreviewed |
| 265 | Potatoes | Promo | X28 | unreviewed |
| 266 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 267 | Topsoil Contract | Promo | X30 | unreviewed |
| 268 | Asteroid Rights | Promo | X34 | unreviewed |
| 269 | Bactoviral Research | Promo | X35 | unreviewed |
| 270 | Bio Printing Facility | Promo | X36 | unreviewed |
| 271 | Harvest | Promo | X37 | unreviewed |
| 272 | Outdoor Sports | Promo | X38 | unreviewed |
| 273 | 16 Psyche | Promo | X44 | unreviewed |
| 274 | Robot Pollinators | Promo | X45 | unreviewed |
| 275 | Supercapacitors | Promo | X46 | unreviewed |
| 276 | Icy Impactors | Promo | X47 | unreviewed |
| 277 | Directed Heat Usage | Promo | X48 | unreviewed |
| 278 | Aqueduct Systems | Promo | X50 | unreviewed |
| 279 | Astra Mechanica | Promo | X51 | unreviewed |
| 280 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 281 | Cyberia Systems | Promo | X53 | unreviewed |
| 282 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 283 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 284 | Kaguya Tech | Promo | X58 | unreviewed |
| 285 | Mars Nomads | Promo | X59 | unreviewed |
| 286 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 287 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 288 | Red Ships | Promo | X62 | unreviewed |
| 289 | Solar Logistics | Promo | X63 | unreviewed |
| 290 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 291 | Teslaract | Promo | X66 | unreviewed |
| 292 | Soil Enrichment | Promo | X67 | unreviewed |
| 293 | Supermarkets | Promo | X68 | unreviewed |
| 294 | Hospitals | Promo | X69 | unreviewed |
| 295 | Public Baths | Promo | X70 | unreviewed |
| 296 | City Parks | Promo | X71 | unreviewed |
| 297 | Casinos | Promo | X72 | unreviewed |
| 298 | Protected Growth | Promo | X73 | unreviewed |
| 299 | Static Harvesting | Promo | X74 | unreviewed |
| 300 | Vermin | Promo | X75 | unreviewed |
| 301 | Weather Balloons | Promo | X76 | unreviewed |
| 302 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
