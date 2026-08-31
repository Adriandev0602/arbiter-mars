# Cartas descargadas, pendientes de revisión

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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Gene Repair | Corporate Era | 091 | unreviewed |
| 2 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 3 | Bushes | Base | 093 | unreviewed |
| 4 | Mass Converter | Corporate Era | 094 | unreviewed |
| 5 | Physics Complex | Corporate Era | 095 | unreviewed |
| 6 | Greenhouses | Base | 096 | unreviewed |
| 7 | Nuclear Zone | Base | 097 | unreviewed |
| 8 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 9 | Toll Station | Corporate Era | 099 | unreviewed |
| 10 | Fueled Generators | Base | 100 | unreviewed |
| 11 | Power Grid | Base | 102 | unreviewed |
| 12 | Ore Processor | Base | 104 | unreviewed |
| 13 | Earth Office | Corporate Era | 105 | unreviewed |
| 14 | Media Archives | Corporate Era | 107 | unreviewed |
| 15 | Open City | Base | 108 | unreviewed |
| 16 | Media Group | Corporate Era | 109 | unreviewed |
| 17 | Business Network | Corporate Era | 110 | unreviewed |
| 18 | Business Contacts | Corporate Era | 111 | unreviewed |
| 19 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 20 | Breathing Filters | Base | 114 | unreviewed |

| 21 | Artificial Lake | Base | 116 | unreviewed |
| 22 | Geothermal Power | Base | 117 | unreviewed |
| 23 | Dust Seals | Base | 119 | unreviewed |
| 24 | Urbanized Area | Base | 120 | unreviewed |
| 25 | Sabotage | Corporate Era | 121 | unreviewed |
| 26 | Moss | Base | 122 | unreviewed |
| 27 | Industrial Center | Corporate Era | 123 | unreviewed |
| 28 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 29 | Hackers | Corporate Era | 125 | unreviewed |
| 30 | GHG Factories | Base | 126 | unreviewed |
| 31 | Subterranean Reservoir | Base | 127 | unreviewed |
| 32 | Ecological Zone | Base | 128 | unreviewed |
| 33 | Zeppelins | Base | 129 | unreviewed |
| 34 | Worms | Base | 130 | unreviewed |
| 35 | Decomposers | Base | 131 | unreviewed |
| 36 | Fusion Power | Base | 132 | unreviewed |
| 37 | Symbiotic Fungus | Base | 133 | unreviewed |
| 38 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 39 | Advanced Ecosystems | Base | 135 | unreviewed |
| 40 | Great Dam | Base | 136 | unreviewed |
| 41 | Cartel | Corporate Era | 137 | unreviewed |
| 42 | Strip Mine | Base | 138 | unreviewed |
| 43 | Wave Power | Base | 139 | unreviewed |
| 44 | Lava Flows | Base | 140 | unreviewed |
| 45 | Power Plant | Base | 141 | unreviewed |
| 46 | Mohole Area | Base | 142 | unreviewed |
| 47 | Large Convoy | Base | 143 | unreviewed |
| 48 | Tectonic Stress Power | Base | 145 | unreviewed |
| 49 | Herbivores | Base | 147 | unreviewed |
| 50 | Insects | Base | 148 | unreviewed |
| 51 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 52 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 53 | Adaptation Technology | Base | 153 | unreviewed |
| 54 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 55 | Designed Microorganisms | Base | 155 | unreviewed |
| 56 | Standard Technology | Corporate Era | 156 | unreviewed |
| 57 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 58 | Industrial Microbes | Base | 158 | unreviewed |
| 59 | Lichen | Base | 159 | unreviewed |
| 60 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 61 | Convoy from Europa | Base | 161 | unreviewed |
| 62 | Imported GHG | Base | 162 | unreviewed |
| 63 | Imported Nitrogen | Base | 163 | unreviewed |
| 64 | Micro-Mills | Base | 164 | unreviewed |
| 65 | Magnetic Field Generators | Base | 165 | unreviewed |
| 66 | Shuttles | Base | 166 | unreviewed |
| 67 | Import of Advanced GHG | Base | 167 | unreviewed |
| 68 | Windmills | Base | 168 | unreviewed |
| 69 | Tundra Farming | Base | 169 | unreviewed |
| 70 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 71 | Magnetic Field Dome | Base | 171 | unreviewed |
| 72 | Pets | Base | 172 | unreviewed |
| 73 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 74 | Protected Valley | Base | 174 | unreviewed |
| 75 | Satellites | Corporate Era | 175 | unreviewed |
| 76 | Noctis Farming | Base | 176 | unreviewed |
| 77 | Water Splitting Plant | Base | 177 | unreviewed |
| 78 | Heat Trappers | Base | 178 | unreviewed |
| 79 | Soil Factory | Base | 179 | unreviewed |
| 80 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 81 | Ice Cap Melting | Base | 181 | unreviewed |
| 82 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 83 | Biomass Combustors | Base | 183 | unreviewed |
| 84 | Livestock | Base | 184 | unreviewed |
| 85 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 86 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 87 | Aquifer Pumping | Base | 187 | unreviewed |
| 88 | Flooding | Base | 188 | unreviewed |
| 89 | Energy Saving | Base | 189 | unreviewed |
| 90 | Local Heat Trapping | Base | 190 | unreviewed |
| 91 | Permafrost Extraction | Base | 191 | unreviewed |
| 92 | Invention Contest | Corporate Era | 192 | unreviewed |
| 93 | Plantation | Base | 193 | unreviewed |
| 94 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 95 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 96 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 97 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 98 | Immigration Shuttles | Base | 198 | unreviewed |
| 99 | Restricted Area | Corporate Era | 199 | unreviewed |
| 100 | Immigrant City | Base | 200 | unreviewed |
| 101 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 102 | Underground Detonations | Base | 202 | unreviewed |
| 103 | Soletta | Base | 203 | unreviewed |
| 104 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 105 | Rad-Chem Factory | Base | 205 | unreviewed |
| 106 | Special Design | Base | 206 | unreviewed |
| 107 | Medical Lab | Corporate Era | 207 | unreviewed |
| 108 | AI Central | Corporate Era | 208 | unreviewed |
| 109 | Small Asteroid | Promo | 209 | unreviewed |
| 110 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 111 | Snow Algae | Promo | 211 | unreviewed |
| 112 | Penguins | Promo | 212 | unreviewed |
| 113 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 114 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 115 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 116 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 117 | Atmoscoop | Venus Next | 217 | unreviewed |
| 118 | Comet for Venus | Venus Next | 218 | unreviewed |
| 119 | Corroder Suits | Venus Next | 219 | unreviewed |
| 120 | Dawn City | Venus Next | 220 | unreviewed |
| 121 | Deuterium Export | Venus Next | 221 | unreviewed |
| 122 | Dirigibles | Venus Next | 222 | unreviewed |
| 123 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 124 | Extremophiles | Venus Next | 224 | unreviewed |
| 125 | Floating Habs | Venus Next | 225 | unreviewed |
| 126 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 127 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 128 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 129 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 130 | Gyropolis | Venus Next | 230 | unreviewed |
| 131 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 132 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 133 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 134 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 135 | Local Shading | Venus Next | 235 | unreviewed |
| 136 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 137 | Luxury Foods | Venus Next | 237 | unreviewed |
| 138 | Maxwell Base | Venus Next | 238 | unreviewed |
| 139 | Mining Quota | Venus Next | 239 | unreviewed |
| 140 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 141 | Omnicourt | Venus Next | 241 | unreviewed |
| 142 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 143 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 144 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 145 | Solarnet | Venus Next | 245 | unreviewed |
| 146 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 147 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 148 | Stratopolis | Venus Next | 248 | unreviewed |
| 149 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 150 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 151 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 152 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 153 | Thermophiles | Venus Next | 253 | unreviewed |
| 154 | Water to Venus | Venus Next | 254 | unreviewed |
| 155 | Venus Governor | Venus Next | 255 | unreviewed |
| 156 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 157 | Venus Soils | Venus Next | 257 | unreviewed |
| 158 | Venus Waystation | Venus Next | 258 | unreviewed |
| 159 | Venusian Animals | Venus Next | 259 | unreviewed |
| 160 | Venusian Insects | Venus Next | 260 | unreviewed |
| 161 | Venusian Plants | Venus Next | 261 | unreviewed |
| 162 | Airliners | Colonies | C01 | unreviewed |
| 163 | Air Raid | Colonies | C02 | unreviewed |
| 164 | Atmo Collectors | Colonies | C03 | unreviewed |
| 165 | Community Services | Colonies | C04 | unreviewed |
| 166 | Conscription | Colonies | C05 | unreviewed |
| 167 | Corona Extractor | Colonies | C06 | unreviewed |
| 168 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 169 | Earth Elevator | Colonies | C08 | unreviewed |
| 170 | Ecology Research | Colonies | C09 | unreviewed |
| 171 | Floater Leasing | Colonies | C10 | unreviewed |
| 172 | Floater Prototypes | Colonies | C11 | unreviewed |
| 173 | Floater Technology | Colonies | C12 | unreviewed |
| 174 | Galilean Waystation | Colonies | C13 | unreviewed |
| 175 | Heavy Taxation | Colonies | C14 | unreviewed |
| 176 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 177 | Impactor Swarm | Colonies | C16 | unreviewed |
| 178 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 179 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 180 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 181 | Luna Governor | Colonies | C20 | unreviewed |
| 182 | Lunar Exports | Colonies | C21 | unreviewed |
| 183 | Lunar Mining | Colonies | C22 | unreviewed |
| 184 | Market Manipulation | Colonies | C23 | unreviewed |
| 185 | Martian Zoo | Colonies | C24 | unreviewed |
| 186 | Mining Colony | Colonies | C25 | unreviewed |
| 187 | Minority Refuge | Colonies | C26 | unreviewed |
| 188 | Molecular Printing | Colonies | C27 | unreviewed |
| 189 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 190 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 191 | Productive Outpost | Colonies | C30 | unreviewed |
| 192 | Quantum Communications | Colonies | C31 | unreviewed |
| 193 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 194 | Refugee Camps | Colonies | C33 | unreviewed |
| 195 | Research Colony | Colonies | C34 | unreviewed |
| 196 | Rim Freighters | Colonies | C35 | unreviewed |
| 197 | Sky Docks | Colonies | C36 | unreviewed |
| 198 | Solar Probe | Colonies | C37 | unreviewed |
| 199 | Solar Reflectors | Colonies | C38 | unreviewed |
| 200 | Space Port | Colonies | C39 | unreviewed |
| 201 | Space Port Colony | Colonies | C40 | unreviewed |
| 202 | Spin-Off Department | Colonies | C41 | unreviewed |
| 203 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 204 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 205 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 206 | Titan Shuttles | Colonies | C45 | unreviewed |
| 207 | Trade Envoys | Colonies | C46 | unreviewed |
| 208 | Trading Colony | Colonies | C47 | unreviewed |
| 209 | Urban Decomposers | Colonies | C48 | unreviewed |
| 210 | Warp Drive | Colonies | C49 | unreviewed |
| 211 | House Printing | Prelude | P36 | unreviewed |
| 212 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 213 | Martian Survey | Prelude | P38 | unreviewed |
| 214 | Psychrophiles | Prelude | P39 | unreviewed |
| 215 | Research Coordination | Prelude | P40 | unreviewed |
| 216 | SF Memorial | Prelude | P41 | unreviewed |
| 217 | Space Hotels | Prelude | P42 | unreviewed |
| 218 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 219 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 220 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 221 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 222 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 223 | Floating Refinery | Venus Next | P73 | unreviewed |
| 224 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 225 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 226 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 227 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 228 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 229 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 230 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 231 | Soil Studies | Venus Next | P81 | unreviewed |
| 232 | Special Permit | Prelude 2 | P82 | unreviewed |
| 233 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 234 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 235 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 236 | Unexpected Application | Venus Next | P86 | unreviewed |
| 237 | Venus Allies | Venus Next | P87 | unreviewed |
| 238 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 239 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 240 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 241 | WG Project | Prelude 2 | P91 | unreviewed |
| 242 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 243 | Banned Delegate | Turmoil | T02 | unreviewed |
| 244 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 245 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 246 | Event Analysts | Turmoil | T05 | unreviewed |
| 247 | GMO Contract | Turmoil | T06 | unreviewed |
| 248 | Martian Media Center | Turmoil | T07 | unreviewed |
| 249 | Parliament Hall | Turmoil | T08 | unreviewed |
| 250 | PR Office | Turmoil | T09 | unreviewed |
| 251 | Public Celebrations | Turmoil | T10 | unreviewed |
| 252 | Recruitment | Turmoil | T11 | unreviewed |
| 253 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 254 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 255 | Supported Research | Turmoil | T14 | unreviewed |
| 256 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 257 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 258 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 259 | Project Inspection | Promo | X02 | unreviewed |
| 260 | Energy Market | Promo | X03 | unreviewed |
| 261 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 262 | Interplanetary Trade | Promo | X05 | unreviewed |
| 263 | Law Suit | Promo | X06 | unreviewed |
| 264 | Mercurian Alloys | Promo | X07 | unreviewed |
| 265 | Orbital Cleanup | Promo | X08 | unreviewed |
| 266 | Political Alliance | Promo | X09 | unreviewed |
| 267 | Rego Plastics | Promo | X10 | unreviewed |
| 268 | Saturn Surfing | Promo | X11 | unreviewed |
| 269 | Stanford Torus | Promo | X12 | unreviewed |
| 270 | Advertising | Promo | X13 | unreviewed |
| 271 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 272 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 273 | Comet Aiming | Promo | X16 | unreviewed |
| 274 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 275 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 276 | Directed Impactors | Promo | X19 | unreviewed |
| 277 | Diversity Support | Promo | X20 | unreviewed |
| 278 | Field-Capped City | Promo | X21 | unreviewed |
| 279 | Imported Nutrients | Promo | X22 | unreviewed |
| 280 | Jovian Embassy | Promo | X23 | unreviewed |
| 281 | Magnetic Shield | Promo | X24 | unreviewed |
| 282 | Meat Industry | Promo | X25 | unreviewed |
| 283 | Meltworks | Promo | X26 | unreviewed |
| 284 | Mohole Lake | Promo | X27 | unreviewed |
| 285 | Potatoes | Promo | X28 | unreviewed |
| 286 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 287 | Topsoil Contract | Promo | X30 | unreviewed |
| 288 | Asteroid Rights | Promo | X34 | unreviewed |
| 289 | Bactoviral Research | Promo | X35 | unreviewed |
| 290 | Bio Printing Facility | Promo | X36 | unreviewed |
| 291 | Harvest | Promo | X37 | unreviewed |
| 292 | Outdoor Sports | Promo | X38 | unreviewed |
| 293 | 16 Psyche | Promo | X44 | unreviewed |
| 294 | Robot Pollinators | Promo | X45 | unreviewed |
| 295 | Supercapacitors | Promo | X46 | unreviewed |
| 296 | Icy Impactors | Promo | X47 | unreviewed |
| 297 | Directed Heat Usage | Promo | X48 | unreviewed |
| 298 | Aqueduct Systems | Promo | X50 | unreviewed |
| 299 | Astra Mechanica | Promo | X51 | unreviewed |
| 300 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 301 | Cyberia Systems | Promo | X53 | unreviewed |
| 302 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 303 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 304 | Kaguya Tech | Promo | X58 | unreviewed |
| 305 | Mars Nomads | Promo | X59 | unreviewed |
| 306 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 307 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 308 | Red Ships | Promo | X62 | unreviewed |
| 309 | Solar Logistics | Promo | X63 | unreviewed |
| 310 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 311 | Teslaract | Promo | X66 | unreviewed |
| 312 | Soil Enrichment | Promo | X67 | unreviewed |
| 313 | Supermarkets | Promo | X68 | unreviewed |
| 314 | Hospitals | Promo | X69 | unreviewed |
| 315 | Public Baths | Promo | X70 | unreviewed |
| 316 | City Parks | Promo | X71 | unreviewed |
| 317 | Casinos | Promo | X72 | unreviewed |
| 318 | Protected Growth | Promo | X73 | unreviewed |
| 319 | Static Harvesting | Promo | X74 | unreviewed |
| 320 | Vermin | Promo | X75 | unreviewed |
| 321 | Weather Balloons | Promo | X76 | unreviewed |
| 322 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
