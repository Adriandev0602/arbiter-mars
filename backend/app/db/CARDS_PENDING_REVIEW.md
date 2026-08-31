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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Ganymede Colony | Base | 081 | unreviewed |
| 2 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 3 | Giant Space Mirror | Base | 083 | unreviewed |
| 4 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 5 | Commercial District | Corporate Era | 085 | unreviewed |
| 6 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 7 | Grass | Base | 087 | unreviewed |
| 8 | Heather | Base | 088 | unreviewed |
| 9 | Peroxide Power | Base | 089 | unreviewed |
| 10 | Research | Corporate Era | 090 | unreviewed |
| 11 | Gene Repair | Corporate Era | 091 | unreviewed |
| 12 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 13 | Bushes | Base | 093 | unreviewed |
| 14 | Mass Converter | Corporate Era | 094 | unreviewed |
| 15 | Physics Complex | Corporate Era | 095 | unreviewed |
| 16 | Greenhouses | Base | 096 | unreviewed |
| 17 | Nuclear Zone | Base | 097 | unreviewed |
| 18 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 19 | Toll Station | Corporate Era | 099 | unreviewed |
| 20 | Fueled Generators | Base | 100 | unreviewed |
| 21 | Power Grid | Base | 102 | unreviewed |
| 22 | Ore Processor | Base | 104 | unreviewed |
| 23 | Earth Office | Corporate Era | 105 | unreviewed |
| 24 | Media Archives | Corporate Era | 107 | unreviewed |
| 25 | Open City | Base | 108 | unreviewed |
| 26 | Media Group | Corporate Era | 109 | unreviewed |
| 27 | Business Network | Corporate Era | 110 | unreviewed |
| 28 | Business Contacts | Corporate Era | 111 | unreviewed |
| 29 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 30 | Breathing Filters | Base | 114 | unreviewed |

| 31 | Artificial Lake | Base | 116 | unreviewed |
| 32 | Geothermal Power | Base | 117 | unreviewed |
| 33 | Dust Seals | Base | 119 | unreviewed |
| 34 | Urbanized Area | Base | 120 | unreviewed |
| 35 | Sabotage | Corporate Era | 121 | unreviewed |
| 36 | Moss | Base | 122 | unreviewed |
| 37 | Industrial Center | Corporate Era | 123 | unreviewed |
| 38 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 39 | Hackers | Corporate Era | 125 | unreviewed |
| 40 | GHG Factories | Base | 126 | unreviewed |
| 41 | Subterranean Reservoir | Base | 127 | unreviewed |
| 42 | Ecological Zone | Base | 128 | unreviewed |
| 43 | Zeppelins | Base | 129 | unreviewed |
| 44 | Worms | Base | 130 | unreviewed |
| 45 | Decomposers | Base | 131 | unreviewed |
| 46 | Fusion Power | Base | 132 | unreviewed |
| 47 | Symbiotic Fungus | Base | 133 | unreviewed |
| 48 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 49 | Advanced Ecosystems | Base | 135 | unreviewed |
| 50 | Great Dam | Base | 136 | unreviewed |
| 51 | Cartel | Corporate Era | 137 | unreviewed |
| 52 | Strip Mine | Base | 138 | unreviewed |
| 53 | Wave Power | Base | 139 | unreviewed |
| 54 | Lava Flows | Base | 140 | unreviewed |
| 55 | Power Plant | Base | 141 | unreviewed |
| 56 | Mohole Area | Base | 142 | unreviewed |
| 57 | Large Convoy | Base | 143 | unreviewed |
| 58 | Tectonic Stress Power | Base | 145 | unreviewed |
| 59 | Herbivores | Base | 147 | unreviewed |
| 60 | Insects | Base | 148 | unreviewed |
| 61 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 62 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 63 | Adaptation Technology | Base | 153 | unreviewed |
| 64 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 65 | Designed Microorganisms | Base | 155 | unreviewed |
| 66 | Standard Technology | Corporate Era | 156 | unreviewed |
| 67 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 68 | Industrial Microbes | Base | 158 | unreviewed |
| 69 | Lichen | Base | 159 | unreviewed |
| 70 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 71 | Convoy from Europa | Base | 161 | unreviewed |
| 72 | Imported GHG | Base | 162 | unreviewed |
| 73 | Imported Nitrogen | Base | 163 | unreviewed |
| 74 | Micro-Mills | Base | 164 | unreviewed |
| 75 | Magnetic Field Generators | Base | 165 | unreviewed |
| 76 | Shuttles | Base | 166 | unreviewed |
| 77 | Import of Advanced GHG | Base | 167 | unreviewed |
| 78 | Windmills | Base | 168 | unreviewed |
| 79 | Tundra Farming | Base | 169 | unreviewed |
| 80 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 81 | Magnetic Field Dome | Base | 171 | unreviewed |
| 82 | Pets | Base | 172 | unreviewed |
| 83 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 84 | Protected Valley | Base | 174 | unreviewed |
| 85 | Satellites | Corporate Era | 175 | unreviewed |
| 86 | Noctis Farming | Base | 176 | unreviewed |
| 87 | Water Splitting Plant | Base | 177 | unreviewed |
| 88 | Heat Trappers | Base | 178 | unreviewed |
| 89 | Soil Factory | Base | 179 | unreviewed |
| 90 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 91 | Ice Cap Melting | Base | 181 | unreviewed |
| 92 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 93 | Biomass Combustors | Base | 183 | unreviewed |
| 94 | Livestock | Base | 184 | unreviewed |
| 95 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 96 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 97 | Aquifer Pumping | Base | 187 | unreviewed |
| 98 | Flooding | Base | 188 | unreviewed |
| 99 | Energy Saving | Base | 189 | unreviewed |
| 100 | Local Heat Trapping | Base | 190 | unreviewed |
| 101 | Permafrost Extraction | Base | 191 | unreviewed |
| 102 | Invention Contest | Corporate Era | 192 | unreviewed |
| 103 | Plantation | Base | 193 | unreviewed |
| 104 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 105 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 106 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 107 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 108 | Immigration Shuttles | Base | 198 | unreviewed |
| 109 | Restricted Area | Corporate Era | 199 | unreviewed |
| 110 | Immigrant City | Base | 200 | unreviewed |
| 111 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 112 | Underground Detonations | Base | 202 | unreviewed |
| 113 | Soletta | Base | 203 | unreviewed |
| 114 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 115 | Rad-Chem Factory | Base | 205 | unreviewed |
| 116 | Special Design | Base | 206 | unreviewed |
| 117 | Medical Lab | Corporate Era | 207 | unreviewed |
| 118 | AI Central | Corporate Era | 208 | unreviewed |
| 119 | Small Asteroid | Promo | 209 | unreviewed |
| 120 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 121 | Snow Algae | Promo | 211 | unreviewed |
| 122 | Penguins | Promo | 212 | unreviewed |
| 123 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 124 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 125 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 126 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 127 | Atmoscoop | Venus Next | 217 | unreviewed |
| 128 | Comet for Venus | Venus Next | 218 | unreviewed |
| 129 | Corroder Suits | Venus Next | 219 | unreviewed |
| 130 | Dawn City | Venus Next | 220 | unreviewed |
| 131 | Deuterium Export | Venus Next | 221 | unreviewed |
| 132 | Dirigibles | Venus Next | 222 | unreviewed |
| 133 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 134 | Extremophiles | Venus Next | 224 | unreviewed |
| 135 | Floating Habs | Venus Next | 225 | unreviewed |
| 136 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 137 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 138 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 139 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 140 | Gyropolis | Venus Next | 230 | unreviewed |
| 141 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 142 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 143 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 144 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 145 | Local Shading | Venus Next | 235 | unreviewed |
| 146 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 147 | Luxury Foods | Venus Next | 237 | unreviewed |
| 148 | Maxwell Base | Venus Next | 238 | unreviewed |
| 149 | Mining Quota | Venus Next | 239 | unreviewed |
| 150 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 151 | Omnicourt | Venus Next | 241 | unreviewed |
| 152 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 153 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 154 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 155 | Solarnet | Venus Next | 245 | unreviewed |
| 156 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 157 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 158 | Stratopolis | Venus Next | 248 | unreviewed |
| 159 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 160 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 161 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 162 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 163 | Thermophiles | Venus Next | 253 | unreviewed |
| 164 | Water to Venus | Venus Next | 254 | unreviewed |
| 165 | Venus Governor | Venus Next | 255 | unreviewed |
| 166 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 167 | Venus Soils | Venus Next | 257 | unreviewed |
| 168 | Venus Waystation | Venus Next | 258 | unreviewed |
| 169 | Venusian Animals | Venus Next | 259 | unreviewed |
| 170 | Venusian Insects | Venus Next | 260 | unreviewed |
| 171 | Venusian Plants | Venus Next | 261 | unreviewed |
| 172 | Airliners | Colonies | C01 | unreviewed |
| 173 | Air Raid | Colonies | C02 | unreviewed |
| 174 | Atmo Collectors | Colonies | C03 | unreviewed |
| 175 | Community Services | Colonies | C04 | unreviewed |
| 176 | Conscription | Colonies | C05 | unreviewed |
| 177 | Corona Extractor | Colonies | C06 | unreviewed |
| 178 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 179 | Earth Elevator | Colonies | C08 | unreviewed |
| 180 | Ecology Research | Colonies | C09 | unreviewed |
| 181 | Floater Leasing | Colonies | C10 | unreviewed |
| 182 | Floater Prototypes | Colonies | C11 | unreviewed |
| 183 | Floater Technology | Colonies | C12 | unreviewed |
| 184 | Galilean Waystation | Colonies | C13 | unreviewed |
| 185 | Heavy Taxation | Colonies | C14 | unreviewed |
| 186 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 187 | Impactor Swarm | Colonies | C16 | unreviewed |
| 188 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 189 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 190 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 191 | Luna Governor | Colonies | C20 | unreviewed |
| 192 | Lunar Exports | Colonies | C21 | unreviewed |
| 193 | Lunar Mining | Colonies | C22 | unreviewed |
| 194 | Market Manipulation | Colonies | C23 | unreviewed |
| 195 | Martian Zoo | Colonies | C24 | unreviewed |
| 196 | Mining Colony | Colonies | C25 | unreviewed |
| 197 | Minority Refuge | Colonies | C26 | unreviewed |
| 198 | Molecular Printing | Colonies | C27 | unreviewed |
| 199 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 200 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 201 | Productive Outpost | Colonies | C30 | unreviewed |
| 202 | Quantum Communications | Colonies | C31 | unreviewed |
| 203 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 204 | Refugee Camps | Colonies | C33 | unreviewed |
| 205 | Research Colony | Colonies | C34 | unreviewed |
| 206 | Rim Freighters | Colonies | C35 | unreviewed |
| 207 | Sky Docks | Colonies | C36 | unreviewed |
| 208 | Solar Probe | Colonies | C37 | unreviewed |
| 209 | Solar Reflectors | Colonies | C38 | unreviewed |
| 210 | Space Port | Colonies | C39 | unreviewed |
| 211 | Space Port Colony | Colonies | C40 | unreviewed |
| 212 | Spin-Off Department | Colonies | C41 | unreviewed |
| 213 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 214 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 215 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 216 | Titan Shuttles | Colonies | C45 | unreviewed |
| 217 | Trade Envoys | Colonies | C46 | unreviewed |
| 218 | Trading Colony | Colonies | C47 | unreviewed |
| 219 | Urban Decomposers | Colonies | C48 | unreviewed |
| 220 | Warp Drive | Colonies | C49 | unreviewed |
| 221 | House Printing | Prelude | P36 | unreviewed |
| 222 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 223 | Martian Survey | Prelude | P38 | unreviewed |
| 224 | Psychrophiles | Prelude | P39 | unreviewed |
| 225 | Research Coordination | Prelude | P40 | unreviewed |
| 226 | SF Memorial | Prelude | P41 | unreviewed |
| 227 | Space Hotels | Prelude | P42 | unreviewed |
| 228 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 229 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 230 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 231 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 232 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 233 | Floating Refinery | Venus Next | P73 | unreviewed |
| 234 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 235 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 236 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 237 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 238 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 239 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 240 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 241 | Soil Studies | Venus Next | P81 | unreviewed |
| 242 | Special Permit | Prelude 2 | P82 | unreviewed |
| 243 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 244 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 245 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 246 | Unexpected Application | Venus Next | P86 | unreviewed |
| 247 | Venus Allies | Venus Next | P87 | unreviewed |
| 248 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 249 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 250 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 251 | WG Project | Prelude 2 | P91 | unreviewed |
| 252 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 253 | Banned Delegate | Turmoil | T02 | unreviewed |
| 254 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 255 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 256 | Event Analysts | Turmoil | T05 | unreviewed |
| 257 | GMO Contract | Turmoil | T06 | unreviewed |
| 258 | Martian Media Center | Turmoil | T07 | unreviewed |
| 259 | Parliament Hall | Turmoil | T08 | unreviewed |
| 260 | PR Office | Turmoil | T09 | unreviewed |
| 261 | Public Celebrations | Turmoil | T10 | unreviewed |
| 262 | Recruitment | Turmoil | T11 | unreviewed |
| 263 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 264 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 265 | Supported Research | Turmoil | T14 | unreviewed |
| 266 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 267 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 268 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 269 | Project Inspection | Promo | X02 | unreviewed |
| 270 | Energy Market | Promo | X03 | unreviewed |
| 271 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 272 | Interplanetary Trade | Promo | X05 | unreviewed |
| 273 | Law Suit | Promo | X06 | unreviewed |
| 274 | Mercurian Alloys | Promo | X07 | unreviewed |
| 275 | Orbital Cleanup | Promo | X08 | unreviewed |
| 276 | Political Alliance | Promo | X09 | unreviewed |
| 277 | Rego Plastics | Promo | X10 | unreviewed |
| 278 | Saturn Surfing | Promo | X11 | unreviewed |
| 279 | Stanford Torus | Promo | X12 | unreviewed |
| 280 | Advertising | Promo | X13 | unreviewed |
| 281 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 282 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 283 | Comet Aiming | Promo | X16 | unreviewed |
| 284 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 285 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 286 | Directed Impactors | Promo | X19 | unreviewed |
| 287 | Diversity Support | Promo | X20 | unreviewed |
| 288 | Field-Capped City | Promo | X21 | unreviewed |
| 289 | Imported Nutrients | Promo | X22 | unreviewed |
| 290 | Jovian Embassy | Promo | X23 | unreviewed |
| 291 | Magnetic Shield | Promo | X24 | unreviewed |
| 292 | Meat Industry | Promo | X25 | unreviewed |
| 293 | Meltworks | Promo | X26 | unreviewed |
| 294 | Mohole Lake | Promo | X27 | unreviewed |
| 295 | Potatoes | Promo | X28 | unreviewed |
| 296 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 297 | Topsoil Contract | Promo | X30 | unreviewed |
| 298 | Asteroid Rights | Promo | X34 | unreviewed |
| 299 | Bactoviral Research | Promo | X35 | unreviewed |
| 300 | Bio Printing Facility | Promo | X36 | unreviewed |
| 301 | Harvest | Promo | X37 | unreviewed |
| 302 | Outdoor Sports | Promo | X38 | unreviewed |
| 303 | 16 Psyche | Promo | X44 | unreviewed |
| 304 | Robot Pollinators | Promo | X45 | unreviewed |
| 305 | Supercapacitors | Promo | X46 | unreviewed |
| 306 | Icy Impactors | Promo | X47 | unreviewed |
| 307 | Directed Heat Usage | Promo | X48 | unreviewed |
| 308 | Aqueduct Systems | Promo | X50 | unreviewed |
| 309 | Astra Mechanica | Promo | X51 | unreviewed |
| 310 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 311 | Cyberia Systems | Promo | X53 | unreviewed |
| 312 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 313 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 314 | Kaguya Tech | Promo | X58 | unreviewed |
| 315 | Mars Nomads | Promo | X59 | unreviewed |
| 316 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 317 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 318 | Red Ships | Promo | X62 | unreviewed |
| 319 | Solar Logistics | Promo | X63 | unreviewed |
| 320 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 321 | Teslaract | Promo | X66 | unreviewed |
| 322 | Soil Enrichment | Promo | X67 | unreviewed |
| 323 | Supermarkets | Promo | X68 | unreviewed |
| 324 | Hospitals | Promo | X69 | unreviewed |
| 325 | Public Baths | Promo | X70 | unreviewed |
| 326 | City Parks | Promo | X71 | unreviewed |
| 327 | Casinos | Promo | X72 | unreviewed |
| 328 | Protected Growth | Promo | X73 | unreviewed |
| 329 | Static Harvesting | Promo | X74 | unreviewed |
| 330 | Vermin | Promo | X75 | unreviewed |
| 331 | Weather Balloons | Promo | X76 | unreviewed |
| 332 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
