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
globales).

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 2 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 3 | Birds | Base | 072 | unreviewed |
| 4 | Mars University | Corporate Era | 073 | unreviewed |
| 5 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 6 | Towing a Comet | Base | 075 | unreviewed |
| 7 | Space Mirrors | Base | 076 | unreviewed |
| 8 | Ice Asteroid | Base | 078 | unreviewed |
| 9 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 10 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 11 | Ganymede Colony | Base | 081 | unreviewed |
| 12 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 13 | Giant Space Mirror | Base | 083 | unreviewed |
| 14 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 15 | Commercial District | Corporate Era | 085 | unreviewed |
| 16 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 17 | Grass | Base | 087 | unreviewed |
| 18 | Heather | Base | 088 | unreviewed |
| 19 | Peroxide Power | Base | 089 | unreviewed |
| 20 | Research | Corporate Era | 090 | unreviewed |
| 21 | Gene Repair | Corporate Era | 091 | unreviewed |
| 22 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 23 | Bushes | Base | 093 | unreviewed |
| 24 | Mass Converter | Corporate Era | 094 | unreviewed |
| 25 | Physics Complex | Corporate Era | 095 | unreviewed |
| 26 | Greenhouses | Base | 096 | unreviewed |
| 27 | Nuclear Zone | Base | 097 | unreviewed |
| 28 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 29 | Toll Station | Corporate Era | 099 | unreviewed |
| 30 | Fueled Generators | Base | 100 | unreviewed |
| 31 | Power Grid | Base | 102 | unreviewed |
| 32 | Ore Processor | Base | 104 | unreviewed |
| 33 | Earth Office | Corporate Era | 105 | unreviewed |
| 34 | Media Archives | Corporate Era | 107 | unreviewed |
| 35 | Open City | Base | 108 | unreviewed |
| 36 | Media Group | Corporate Era | 109 | unreviewed |
| 37 | Business Network | Corporate Era | 110 | unreviewed |
| 38 | Business Contacts | Corporate Era | 111 | unreviewed |
| 39 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 40 | Breathing Filters | Base | 114 | unreviewed |

| 41 | Artificial Lake | Base | 116 | unreviewed |
| 42 | Geothermal Power | Base | 117 | unreviewed |
| 43 | Dust Seals | Base | 119 | unreviewed |
| 44 | Urbanized Area | Base | 120 | unreviewed |
| 45 | Sabotage | Corporate Era | 121 | unreviewed |
| 46 | Moss | Base | 122 | unreviewed |
| 47 | Industrial Center | Corporate Era | 123 | unreviewed |
| 48 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 49 | Hackers | Corporate Era | 125 | unreviewed |
| 50 | GHG Factories | Base | 126 | unreviewed |
| 51 | Subterranean Reservoir | Base | 127 | unreviewed |
| 52 | Ecological Zone | Base | 128 | unreviewed |
| 53 | Zeppelins | Base | 129 | unreviewed |
| 54 | Worms | Base | 130 | unreviewed |
| 55 | Decomposers | Base | 131 | unreviewed |
| 56 | Fusion Power | Base | 132 | unreviewed |
| 57 | Symbiotic Fungus | Base | 133 | unreviewed |
| 58 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 59 | Advanced Ecosystems | Base | 135 | unreviewed |
| 60 | Great Dam | Base | 136 | unreviewed |
| 61 | Cartel | Corporate Era | 137 | unreviewed |
| 62 | Strip Mine | Base | 138 | unreviewed |
| 63 | Wave Power | Base | 139 | unreviewed |
| 64 | Lava Flows | Base | 140 | unreviewed |
| 65 | Power Plant | Base | 141 | unreviewed |
| 66 | Mohole Area | Base | 142 | unreviewed |
| 67 | Large Convoy | Base | 143 | unreviewed |
| 68 | Tectonic Stress Power | Base | 145 | unreviewed |
| 69 | Herbivores | Base | 147 | unreviewed |
| 70 | Insects | Base | 148 | unreviewed |
| 71 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 72 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 73 | Adaptation Technology | Base | 153 | unreviewed |
| 74 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 75 | Designed Microorganisms | Base | 155 | unreviewed |
| 76 | Standard Technology | Corporate Era | 156 | unreviewed |
| 77 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 78 | Industrial Microbes | Base | 158 | unreviewed |
| 79 | Lichen | Base | 159 | unreviewed |
| 80 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 81 | Convoy from Europa | Base | 161 | unreviewed |
| 82 | Imported GHG | Base | 162 | unreviewed |
| 83 | Imported Nitrogen | Base | 163 | unreviewed |
| 84 | Micro-Mills | Base | 164 | unreviewed |
| 85 | Magnetic Field Generators | Base | 165 | unreviewed |
| 86 | Shuttles | Base | 166 | unreviewed |
| 87 | Import of Advanced GHG | Base | 167 | unreviewed |
| 88 | Windmills | Base | 168 | unreviewed |
| 89 | Tundra Farming | Base | 169 | unreviewed |
| 90 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 91 | Magnetic Field Dome | Base | 171 | unreviewed |
| 92 | Pets | Base | 172 | unreviewed |
| 93 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 94 | Protected Valley | Base | 174 | unreviewed |
| 95 | Satellites | Corporate Era | 175 | unreviewed |
| 96 | Noctis Farming | Base | 176 | unreviewed |
| 97 | Water Splitting Plant | Base | 177 | unreviewed |
| 98 | Heat Trappers | Base | 178 | unreviewed |
| 99 | Soil Factory | Base | 179 | unreviewed |
| 100 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 101 | Ice Cap Melting | Base | 181 | unreviewed |
| 102 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 103 | Biomass Combustors | Base | 183 | unreviewed |
| 104 | Livestock | Base | 184 | unreviewed |
| 105 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 106 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 107 | Aquifer Pumping | Base | 187 | unreviewed |
| 108 | Flooding | Base | 188 | unreviewed |
| 109 | Energy Saving | Base | 189 | unreviewed |
| 110 | Local Heat Trapping | Base | 190 | unreviewed |
| 111 | Permafrost Extraction | Base | 191 | unreviewed |
| 112 | Invention Contest | Corporate Era | 192 | unreviewed |
| 113 | Plantation | Base | 193 | unreviewed |
| 114 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 115 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 116 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 117 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 118 | Immigration Shuttles | Base | 198 | unreviewed |
| 119 | Restricted Area | Corporate Era | 199 | unreviewed |
| 120 | Immigrant City | Base | 200 | unreviewed |
| 121 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 122 | Underground Detonations | Base | 202 | unreviewed |
| 123 | Soletta | Base | 203 | unreviewed |
| 124 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 125 | Rad-Chem Factory | Base | 205 | unreviewed |
| 126 | Special Design | Base | 206 | unreviewed |
| 127 | Medical Lab | Corporate Era | 207 | unreviewed |
| 128 | AI Central | Corporate Era | 208 | unreviewed |
| 129 | Small Asteroid | Promo | 209 | unreviewed |
| 130 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 131 | Snow Algae | Promo | 211 | unreviewed |
| 132 | Penguins | Promo | 212 | unreviewed |
| 133 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 134 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 135 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 136 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 137 | Atmoscoop | Venus Next | 217 | unreviewed |
| 138 | Comet for Venus | Venus Next | 218 | unreviewed |
| 139 | Corroder Suits | Venus Next | 219 | unreviewed |
| 140 | Dawn City | Venus Next | 220 | unreviewed |
| 141 | Deuterium Export | Venus Next | 221 | unreviewed |
| 142 | Dirigibles | Venus Next | 222 | unreviewed |
| 143 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 144 | Extremophiles | Venus Next | 224 | unreviewed |
| 145 | Floating Habs | Venus Next | 225 | unreviewed |
| 146 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 147 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 148 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 149 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 150 | Gyropolis | Venus Next | 230 | unreviewed |
| 151 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 152 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 153 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 154 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 155 | Local Shading | Venus Next | 235 | unreviewed |
| 156 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 157 | Luxury Foods | Venus Next | 237 | unreviewed |
| 158 | Maxwell Base | Venus Next | 238 | unreviewed |
| 159 | Mining Quota | Venus Next | 239 | unreviewed |
| 160 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 161 | Omnicourt | Venus Next | 241 | unreviewed |
| 162 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 163 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 164 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 165 | Solarnet | Venus Next | 245 | unreviewed |
| 166 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 167 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 168 | Stratopolis | Venus Next | 248 | unreviewed |
| 169 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 170 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 171 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 172 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 173 | Thermophiles | Venus Next | 253 | unreviewed |
| 174 | Water to Venus | Venus Next | 254 | unreviewed |
| 175 | Venus Governor | Venus Next | 255 | unreviewed |
| 176 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 177 | Venus Soils | Venus Next | 257 | unreviewed |
| 178 | Venus Waystation | Venus Next | 258 | unreviewed |
| 179 | Venusian Animals | Venus Next | 259 | unreviewed |
| 180 | Venusian Insects | Venus Next | 260 | unreviewed |
| 181 | Venusian Plants | Venus Next | 261 | unreviewed |
| 182 | Airliners | Colonies | C01 | unreviewed |
| 183 | Air Raid | Colonies | C02 | unreviewed |
| 184 | Atmo Collectors | Colonies | C03 | unreviewed |
| 185 | Community Services | Colonies | C04 | unreviewed |
| 186 | Conscription | Colonies | C05 | unreviewed |
| 187 | Corona Extractor | Colonies | C06 | unreviewed |
| 188 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 189 | Earth Elevator | Colonies | C08 | unreviewed |
| 190 | Ecology Research | Colonies | C09 | unreviewed |
| 191 | Floater Leasing | Colonies | C10 | unreviewed |
| 192 | Floater Prototypes | Colonies | C11 | unreviewed |
| 193 | Floater Technology | Colonies | C12 | unreviewed |
| 194 | Galilean Waystation | Colonies | C13 | unreviewed |
| 195 | Heavy Taxation | Colonies | C14 | unreviewed |
| 196 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 197 | Impactor Swarm | Colonies | C16 | unreviewed |
| 198 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 199 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 200 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 201 | Luna Governor | Colonies | C20 | unreviewed |
| 202 | Lunar Exports | Colonies | C21 | unreviewed |
| 203 | Lunar Mining | Colonies | C22 | unreviewed |
| 204 | Market Manipulation | Colonies | C23 | unreviewed |
| 205 | Martian Zoo | Colonies | C24 | unreviewed |
| 206 | Mining Colony | Colonies | C25 | unreviewed |
| 207 | Minority Refuge | Colonies | C26 | unreviewed |
| 208 | Molecular Printing | Colonies | C27 | unreviewed |
| 209 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 210 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 211 | Productive Outpost | Colonies | C30 | unreviewed |
| 212 | Quantum Communications | Colonies | C31 | unreviewed |
| 213 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 214 | Refugee Camps | Colonies | C33 | unreviewed |
| 215 | Research Colony | Colonies | C34 | unreviewed |
| 216 | Rim Freighters | Colonies | C35 | unreviewed |
| 217 | Sky Docks | Colonies | C36 | unreviewed |
| 218 | Solar Probe | Colonies | C37 | unreviewed |
| 219 | Solar Reflectors | Colonies | C38 | unreviewed |
| 220 | Space Port | Colonies | C39 | unreviewed |
| 221 | Space Port Colony | Colonies | C40 | unreviewed |
| 222 | Spin-Off Department | Colonies | C41 | unreviewed |
| 223 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 224 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 225 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 226 | Titan Shuttles | Colonies | C45 | unreviewed |
| 227 | Trade Envoys | Colonies | C46 | unreviewed |
| 228 | Trading Colony | Colonies | C47 | unreviewed |
| 229 | Urban Decomposers | Colonies | C48 | unreviewed |
| 230 | Warp Drive | Colonies | C49 | unreviewed |
| 231 | House Printing | Prelude | P36 | unreviewed |
| 232 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 233 | Martian Survey | Prelude | P38 | unreviewed |
| 234 | Psychrophiles | Prelude | P39 | unreviewed |
| 235 | Research Coordination | Prelude | P40 | unreviewed |
| 236 | SF Memorial | Prelude | P41 | unreviewed |
| 237 | Space Hotels | Prelude | P42 | unreviewed |
| 238 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 239 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 240 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 241 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 242 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 243 | Floating Refinery | Venus Next | P73 | unreviewed |
| 244 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 245 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 246 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 247 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 248 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 249 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 250 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 251 | Soil Studies | Venus Next | P81 | unreviewed |
| 252 | Special Permit | Prelude 2 | P82 | unreviewed |
| 253 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 254 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 255 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 256 | Unexpected Application | Venus Next | P86 | unreviewed |
| 257 | Venus Allies | Venus Next | P87 | unreviewed |
| 258 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 259 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 260 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 261 | WG Project | Prelude 2 | P91 | unreviewed |
| 262 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 263 | Banned Delegate | Turmoil | T02 | unreviewed |
| 264 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 265 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 266 | Event Analysts | Turmoil | T05 | unreviewed |
| 267 | GMO Contract | Turmoil | T06 | unreviewed |
| 268 | Martian Media Center | Turmoil | T07 | unreviewed |
| 269 | Parliament Hall | Turmoil | T08 | unreviewed |
| 270 | PR Office | Turmoil | T09 | unreviewed |
| 271 | Public Celebrations | Turmoil | T10 | unreviewed |
| 272 | Recruitment | Turmoil | T11 | unreviewed |
| 273 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 274 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 275 | Supported Research | Turmoil | T14 | unreviewed |
| 276 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 277 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 278 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 279 | Project Inspection | Promo | X02 | unreviewed |
| 280 | Energy Market | Promo | X03 | unreviewed |
| 281 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 282 | Interplanetary Trade | Promo | X05 | unreviewed |
| 283 | Law Suit | Promo | X06 | unreviewed |
| 284 | Mercurian Alloys | Promo | X07 | unreviewed |
| 285 | Orbital Cleanup | Promo | X08 | unreviewed |
| 286 | Political Alliance | Promo | X09 | unreviewed |
| 287 | Rego Plastics | Promo | X10 | unreviewed |
| 288 | Saturn Surfing | Promo | X11 | unreviewed |
| 289 | Stanford Torus | Promo | X12 | unreviewed |
| 290 | Advertising | Promo | X13 | unreviewed |
| 291 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 292 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 293 | Comet Aiming | Promo | X16 | unreviewed |
| 294 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 295 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 296 | Directed Impactors | Promo | X19 | unreviewed |
| 297 | Diversity Support | Promo | X20 | unreviewed |
| 298 | Field-Capped City | Promo | X21 | unreviewed |
| 299 | Imported Nutrients | Promo | X22 | unreviewed |
| 300 | Jovian Embassy | Promo | X23 | unreviewed |
| 301 | Magnetic Shield | Promo | X24 | unreviewed |
| 302 | Meat Industry | Promo | X25 | unreviewed |
| 303 | Meltworks | Promo | X26 | unreviewed |
| 304 | Mohole Lake | Promo | X27 | unreviewed |
| 305 | Potatoes | Promo | X28 | unreviewed |
| 306 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 307 | Topsoil Contract | Promo | X30 | unreviewed |
| 308 | Asteroid Rights | Promo | X34 | unreviewed |
| 309 | Bactoviral Research | Promo | X35 | unreviewed |
| 310 | Bio Printing Facility | Promo | X36 | unreviewed |
| 311 | Harvest | Promo | X37 | unreviewed |
| 312 | Outdoor Sports | Promo | X38 | unreviewed |
| 313 | 16 Psyche | Promo | X44 | unreviewed |
| 314 | Robot Pollinators | Promo | X45 | unreviewed |
| 315 | Supercapacitors | Promo | X46 | unreviewed |
| 316 | Icy Impactors | Promo | X47 | unreviewed |
| 317 | Directed Heat Usage | Promo | X48 | unreviewed |
| 318 | Aqueduct Systems | Promo | X50 | unreviewed |
| 319 | Astra Mechanica | Promo | X51 | unreviewed |
| 320 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 321 | Cyberia Systems | Promo | X53 | unreviewed |
| 322 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 323 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 324 | Kaguya Tech | Promo | X58 | unreviewed |
| 325 | Mars Nomads | Promo | X59 | unreviewed |
| 326 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 327 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 328 | Red Ships | Promo | X62 | unreviewed |
| 329 | Solar Logistics | Promo | X63 | unreviewed |
| 330 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 331 | Teslaract | Promo | X66 | unreviewed |
| 332 | Soil Enrichment | Promo | X67 | unreviewed |
| 333 | Supermarkets | Promo | X68 | unreviewed |
| 334 | Hospitals | Promo | X69 | unreviewed |
| 335 | Public Baths | Promo | X70 | unreviewed |
| 336 | City Parks | Promo | X71 | unreviewed |
| 337 | Casinos | Promo | X72 | unreviewed |
| 338 | Protected Growth | Promo | X73 | unreviewed |
| 339 | Static Harvesting | Promo | X74 | unreviewed |
| 340 | Vermin | Promo | X75 | unreviewed |
| 341 | Weather Balloons | Promo | X76 | unreviewed |
| 342 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
