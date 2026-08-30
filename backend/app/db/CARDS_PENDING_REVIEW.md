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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Nitrogen-Rich Asteroid | Base | 037 | unreviewed |
| 2 | Rover Construction | Base | 038 | unreviewed |
| 3 | Deimos Down | Base | 039 | unreviewed |
| 4 | Asteroid Mining | Base | 040 | unreviewed |
| 5 | Food Factory | Base | 041 | unreviewed |
| 6 | Archaebacteria | Base | 042 | unreviewed |
| 7 | Carbonate Processing | Base | 043 | unreviewed |
| 8 | Natural Preserve | Base | 044 | unreviewed |
| 9 | Lightning Harvest | Corporate Era | 046 | unreviewed |
| 10 | Algae | Base | 047 | unreviewed |
| 11 | Adapted Lichen | Base | 048 | unreviewed |
| 12 | Tardigrades | Corporate Era | 049 | unreviewed |
| 13 | Virus | Corporate Era | 050 | unreviewed |
| 14 | Miranda Resort | Corporate Era | 051 | unreviewed |
| 15 | Fish | Base | 052 | unreviewed |
| 16 | Lake Marineris | Base | 053 | unreviewed |
| 17 | Small Animals | Base | 054 | unreviewed |
| 18 | Kelp Farming | Base | 055 | unreviewed |
| 19 | Vesta Shipyard | Corporate Era | 057 | unreviewed |
| 20 | Beam from a Thorium Asteroid | Base | 058 | unreviewed |
| 21 | Mangrove | Base | 059 | unreviewed |
| 22 | Trees | Base | 060 | unreviewed |
| 23 | Great Escarpment Consortium | Corporate Era | 061 | unreviewed |
| 24 | Mineral Deposit | Corporate Era | 062 | unreviewed |
| 25 | Mining Expedition | Base | 063 | unreviewed |
| 26 | Mining Area | Corporate Era | 064 | unreviewed |
| 27 | Building Industries | Corporate Era | 065 | unreviewed |
| 28 | Land Claim | Corporate Era | 066 | unreviewed |
| 29 | Mining Rights | Base | 067 | unreviewed |
| 30 | Electro Catapult | Corporate Era | 069 | unreviewed |
| 31 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 32 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 33 | Birds | Base | 072 | unreviewed |
| 34 | Mars University | Corporate Era | 073 | unreviewed |
| 35 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 36 | Towing a Comet | Base | 075 | unreviewed |
| 37 | Space Mirrors | Base | 076 | unreviewed |
| 38 | Ice Asteroid | Base | 078 | unreviewed |
| 39 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 40 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 41 | Ganymede Colony | Base | 081 | unreviewed |
| 42 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 43 | Giant Space Mirror | Base | 083 | unreviewed |
| 44 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 45 | Commercial District | Corporate Era | 085 | unreviewed |
| 46 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 47 | Grass | Base | 087 | unreviewed |
| 48 | Heather | Base | 088 | unreviewed |
| 49 | Peroxide Power | Base | 089 | unreviewed |
| 50 | Research | Corporate Era | 090 | unreviewed |
| 51 | Gene Repair | Corporate Era | 091 | unreviewed |
| 52 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 53 | Bushes | Base | 093 | unreviewed |
| 54 | Mass Converter | Corporate Era | 094 | unreviewed |
| 55 | Physics Complex | Corporate Era | 095 | unreviewed |
| 56 | Greenhouses | Base | 096 | unreviewed |
| 57 | Nuclear Zone | Base | 097 | unreviewed |
| 58 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 59 | Toll Station | Corporate Era | 099 | unreviewed |
| 60 | Fueled Generators | Base | 100 | unreviewed |
| 61 | Power Grid | Base | 102 | unreviewed |
| 62 | Ore Processor | Base | 104 | unreviewed |
| 63 | Earth Office | Corporate Era | 105 | unreviewed |
| 64 | Media Archives | Corporate Era | 107 | unreviewed |
| 65 | Open City | Base | 108 | unreviewed |
| 66 | Media Group | Corporate Era | 109 | unreviewed |
| 67 | Business Network | Corporate Era | 110 | unreviewed |
| 68 | Business Contacts | Corporate Era | 111 | unreviewed |
| 69 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 70 | Breathing Filters | Base | 114 | unreviewed |

| 71 | Artificial Lake | Base | 116 | unreviewed |
| 72 | Geothermal Power | Base | 117 | unreviewed |
| 73 | Dust Seals | Base | 119 | unreviewed |
| 74 | Urbanized Area | Base | 120 | unreviewed |
| 75 | Sabotage | Corporate Era | 121 | unreviewed |
| 76 | Moss | Base | 122 | unreviewed |
| 77 | Industrial Center | Corporate Era | 123 | unreviewed |
| 78 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 79 | Hackers | Corporate Era | 125 | unreviewed |
| 80 | GHG Factories | Base | 126 | unreviewed |
| 81 | Subterranean Reservoir | Base | 127 | unreviewed |
| 82 | Ecological Zone | Base | 128 | unreviewed |
| 83 | Zeppelins | Base | 129 | unreviewed |
| 84 | Worms | Base | 130 | unreviewed |
| 85 | Decomposers | Base | 131 | unreviewed |
| 86 | Fusion Power | Base | 132 | unreviewed |
| 87 | Symbiotic Fungus | Base | 133 | unreviewed |
| 88 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 89 | Advanced Ecosystems | Base | 135 | unreviewed |
| 90 | Great Dam | Base | 136 | unreviewed |
| 91 | Cartel | Corporate Era | 137 | unreviewed |
| 92 | Strip Mine | Base | 138 | unreviewed |
| 93 | Wave Power | Base | 139 | unreviewed |
| 94 | Lava Flows | Base | 140 | unreviewed |
| 95 | Power Plant | Base | 141 | unreviewed |
| 96 | Mohole Area | Base | 142 | unreviewed |
| 97 | Large Convoy | Base | 143 | unreviewed |
| 98 | Tectonic Stress Power | Base | 145 | unreviewed |
| 99 | Herbivores | Base | 147 | unreviewed |
| 100 | Insects | Base | 148 | unreviewed |
| 101 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 102 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 103 | Adaptation Technology | Base | 153 | unreviewed |
| 104 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 105 | Designed Microorganisms | Base | 155 | unreviewed |
| 106 | Standard Technology | Corporate Era | 156 | unreviewed |
| 107 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 108 | Industrial Microbes | Base | 158 | unreviewed |
| 109 | Lichen | Base | 159 | unreviewed |
| 110 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 111 | Convoy from Europa | Base | 161 | unreviewed |
| 112 | Imported GHG | Base | 162 | unreviewed |
| 113 | Imported Nitrogen | Base | 163 | unreviewed |
| 114 | Micro-Mills | Base | 164 | unreviewed |
| 115 | Magnetic Field Generators | Base | 165 | unreviewed |
| 116 | Shuttles | Base | 166 | unreviewed |
| 117 | Import of Advanced GHG | Base | 167 | unreviewed |
| 118 | Windmills | Base | 168 | unreviewed |
| 119 | Tundra Farming | Base | 169 | unreviewed |
| 120 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 121 | Magnetic Field Dome | Base | 171 | unreviewed |
| 122 | Pets | Base | 172 | unreviewed |
| 123 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 124 | Protected Valley | Base | 174 | unreviewed |
| 125 | Satellites | Corporate Era | 175 | unreviewed |
| 126 | Noctis Farming | Base | 176 | unreviewed |
| 127 | Water Splitting Plant | Base | 177 | unreviewed |
| 128 | Heat Trappers | Base | 178 | unreviewed |
| 129 | Soil Factory | Base | 179 | unreviewed |
| 130 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 131 | Ice Cap Melting | Base | 181 | unreviewed |
| 132 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 133 | Biomass Combustors | Base | 183 | unreviewed |
| 134 | Livestock | Base | 184 | unreviewed |
| 135 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 136 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 137 | Aquifer Pumping | Base | 187 | unreviewed |
| 138 | Flooding | Base | 188 | unreviewed |
| 139 | Energy Saving | Base | 189 | unreviewed |
| 140 | Local Heat Trapping | Base | 190 | unreviewed |
| 141 | Permafrost Extraction | Base | 191 | unreviewed |
| 142 | Invention Contest | Corporate Era | 192 | unreviewed |
| 143 | Plantation | Base | 193 | unreviewed |
| 144 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 145 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 146 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 147 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 148 | Immigration Shuttles | Base | 198 | unreviewed |
| 149 | Restricted Area | Corporate Era | 199 | unreviewed |
| 150 | Immigrant City | Base | 200 | unreviewed |
| 151 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 152 | Underground Detonations | Base | 202 | unreviewed |
| 153 | Soletta | Base | 203 | unreviewed |
| 154 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 155 | Rad-Chem Factory | Base | 205 | unreviewed |
| 156 | Special Design | Base | 206 | unreviewed |
| 157 | Medical Lab | Corporate Era | 207 | unreviewed |
| 158 | AI Central | Corporate Era | 208 | unreviewed |
| 159 | Small Asteroid | Promo | 209 | unreviewed |
| 160 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 161 | Snow Algae | Promo | 211 | unreviewed |
| 162 | Penguins | Promo | 212 | unreviewed |
| 163 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 164 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 165 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 166 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 167 | Atmoscoop | Venus Next | 217 | unreviewed |
| 168 | Comet for Venus | Venus Next | 218 | unreviewed |
| 169 | Corroder Suits | Venus Next | 219 | unreviewed |
| 170 | Dawn City | Venus Next | 220 | unreviewed |
| 171 | Deuterium Export | Venus Next | 221 | unreviewed |
| 172 | Dirigibles | Venus Next | 222 | unreviewed |
| 173 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 174 | Extremophiles | Venus Next | 224 | unreviewed |
| 175 | Floating Habs | Venus Next | 225 | unreviewed |
| 176 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 177 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 178 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 179 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 180 | Gyropolis | Venus Next | 230 | unreviewed |
| 181 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 182 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 183 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 184 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 185 | Local Shading | Venus Next | 235 | unreviewed |
| 186 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 187 | Luxury Foods | Venus Next | 237 | unreviewed |
| 188 | Maxwell Base | Venus Next | 238 | unreviewed |
| 189 | Mining Quota | Venus Next | 239 | unreviewed |
| 190 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 191 | Omnicourt | Venus Next | 241 | unreviewed |
| 192 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 193 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 194 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 195 | Solarnet | Venus Next | 245 | unreviewed |
| 196 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 197 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 198 | Stratopolis | Venus Next | 248 | unreviewed |
| 199 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 200 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 201 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 202 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 203 | Thermophiles | Venus Next | 253 | unreviewed |
| 204 | Water to Venus | Venus Next | 254 | unreviewed |
| 205 | Venus Governor | Venus Next | 255 | unreviewed |
| 206 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 207 | Venus Soils | Venus Next | 257 | unreviewed |
| 208 | Venus Waystation | Venus Next | 258 | unreviewed |
| 209 | Venusian Animals | Venus Next | 259 | unreviewed |
| 210 | Venusian Insects | Venus Next | 260 | unreviewed |
| 211 | Venusian Plants | Venus Next | 261 | unreviewed |
| 212 | Airliners | Colonies | C01 | unreviewed |
| 213 | Air Raid | Colonies | C02 | unreviewed |
| 214 | Atmo Collectors | Colonies | C03 | unreviewed |
| 215 | Community Services | Colonies | C04 | unreviewed |
| 216 | Conscription | Colonies | C05 | unreviewed |
| 217 | Corona Extractor | Colonies | C06 | unreviewed |
| 218 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 219 | Earth Elevator | Colonies | C08 | unreviewed |
| 220 | Ecology Research | Colonies | C09 | unreviewed |
| 221 | Floater Leasing | Colonies | C10 | unreviewed |
| 222 | Floater Prototypes | Colonies | C11 | unreviewed |
| 223 | Floater Technology | Colonies | C12 | unreviewed |
| 224 | Galilean Waystation | Colonies | C13 | unreviewed |
| 225 | Heavy Taxation | Colonies | C14 | unreviewed |
| 226 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 227 | Impactor Swarm | Colonies | C16 | unreviewed |
| 228 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 229 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 230 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 231 | Luna Governor | Colonies | C20 | unreviewed |
| 232 | Lunar Exports | Colonies | C21 | unreviewed |
| 233 | Lunar Mining | Colonies | C22 | unreviewed |
| 234 | Market Manipulation | Colonies | C23 | unreviewed |
| 235 | Martian Zoo | Colonies | C24 | unreviewed |
| 236 | Mining Colony | Colonies | C25 | unreviewed |
| 237 | Minority Refuge | Colonies | C26 | unreviewed |
| 238 | Molecular Printing | Colonies | C27 | unreviewed |
| 239 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 240 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 241 | Productive Outpost | Colonies | C30 | unreviewed |
| 242 | Quantum Communications | Colonies | C31 | unreviewed |
| 243 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 244 | Refugee Camps | Colonies | C33 | unreviewed |
| 245 | Research Colony | Colonies | C34 | unreviewed |
| 246 | Rim Freighters | Colonies | C35 | unreviewed |
| 247 | Sky Docks | Colonies | C36 | unreviewed |
| 248 | Solar Probe | Colonies | C37 | unreviewed |
| 249 | Solar Reflectors | Colonies | C38 | unreviewed |
| 250 | Space Port | Colonies | C39 | unreviewed |
| 251 | Space Port Colony | Colonies | C40 | unreviewed |
| 252 | Spin-Off Department | Colonies | C41 | unreviewed |
| 253 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 254 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 255 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 256 | Titan Shuttles | Colonies | C45 | unreviewed |
| 257 | Trade Envoys | Colonies | C46 | unreviewed |
| 258 | Trading Colony | Colonies | C47 | unreviewed |
| 259 | Urban Decomposers | Colonies | C48 | unreviewed |
| 260 | Warp Drive | Colonies | C49 | unreviewed |
| 261 | House Printing | Prelude | P36 | unreviewed |
| 262 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 263 | Martian Survey | Prelude | P38 | unreviewed |
| 264 | Psychrophiles | Prelude | P39 | unreviewed |
| 265 | Research Coordination | Prelude | P40 | unreviewed |
| 266 | SF Memorial | Prelude | P41 | unreviewed |
| 267 | Space Hotels | Prelude | P42 | unreviewed |
| 268 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 269 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 270 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 271 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 272 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 273 | Floating Refinery | Venus Next | P73 | unreviewed |
| 274 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 275 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 276 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 277 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 278 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 279 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 280 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 281 | Soil Studies | Venus Next | P81 | unreviewed |
| 282 | Special Permit | Prelude 2 | P82 | unreviewed |
| 283 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 284 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 285 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 286 | Unexpected Application | Venus Next | P86 | unreviewed |
| 287 | Venus Allies | Venus Next | P87 | unreviewed |
| 288 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 289 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 290 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 291 | WG Project | Prelude 2 | P91 | unreviewed |
| 292 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 293 | Banned Delegate | Turmoil | T02 | unreviewed |
| 294 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 295 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 296 | Event Analysts | Turmoil | T05 | unreviewed |
| 297 | GMO Contract | Turmoil | T06 | unreviewed |
| 298 | Martian Media Center | Turmoil | T07 | unreviewed |
| 299 | Parliament Hall | Turmoil | T08 | unreviewed |
| 300 | PR Office | Turmoil | T09 | unreviewed |
| 301 | Public Celebrations | Turmoil | T10 | unreviewed |
| 302 | Recruitment | Turmoil | T11 | unreviewed |
| 303 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 304 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 305 | Supported Research | Turmoil | T14 | unreviewed |
| 306 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 307 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 308 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 309 | Project Inspection | Promo | X02 | unreviewed |
| 310 | Energy Market | Promo | X03 | unreviewed |
| 311 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 312 | Interplanetary Trade | Promo | X05 | unreviewed |
| 313 | Law Suit | Promo | X06 | unreviewed |
| 314 | Mercurian Alloys | Promo | X07 | unreviewed |
| 315 | Orbital Cleanup | Promo | X08 | unreviewed |
| 316 | Political Alliance | Promo | X09 | unreviewed |
| 317 | Rego Plastics | Promo | X10 | unreviewed |
| 318 | Saturn Surfing | Promo | X11 | unreviewed |
| 319 | Stanford Torus | Promo | X12 | unreviewed |
| 320 | Advertising | Promo | X13 | unreviewed |
| 321 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 322 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 323 | Comet Aiming | Promo | X16 | unreviewed |
| 324 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 325 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 326 | Directed Impactors | Promo | X19 | unreviewed |
| 327 | Diversity Support | Promo | X20 | unreviewed |
| 328 | Field-Capped City | Promo | X21 | unreviewed |
| 329 | Imported Nutrients | Promo | X22 | unreviewed |
| 330 | Jovian Embassy | Promo | X23 | unreviewed |
| 331 | Magnetic Shield | Promo | X24 | unreviewed |
| 332 | Meat Industry | Promo | X25 | unreviewed |
| 333 | Meltworks | Promo | X26 | unreviewed |
| 334 | Mohole Lake | Promo | X27 | unreviewed |
| 335 | Potatoes | Promo | X28 | unreviewed |
| 336 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 337 | Topsoil Contract | Promo | X30 | unreviewed |
| 338 | Asteroid Rights | Promo | X34 | unreviewed |
| 339 | Bactoviral Research | Promo | X35 | unreviewed |
| 340 | Bio Printing Facility | Promo | X36 | unreviewed |
| 341 | Harvest | Promo | X37 | unreviewed |
| 342 | Outdoor Sports | Promo | X38 | unreviewed |
| 343 | 16 Psyche | Promo | X44 | unreviewed |
| 344 | Robot Pollinators | Promo | X45 | unreviewed |
| 345 | Supercapacitors | Promo | X46 | unreviewed |
| 346 | Icy Impactors | Promo | X47 | unreviewed |
| 347 | Directed Heat Usage | Promo | X48 | unreviewed |
| 348 | Aqueduct Systems | Promo | X50 | unreviewed |
| 349 | Astra Mechanica | Promo | X51 | unreviewed |
| 350 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 351 | Cyberia Systems | Promo | X53 | unreviewed |
| 352 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 353 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 354 | Kaguya Tech | Promo | X58 | unreviewed |
| 355 | Mars Nomads | Promo | X59 | unreviewed |
| 356 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 357 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 358 | Red Ships | Promo | X62 | unreviewed |
| 359 | Solar Logistics | Promo | X63 | unreviewed |
| 360 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 361 | Teslaract | Promo | X66 | unreviewed |
| 362 | Soil Enrichment | Promo | X67 | unreviewed |
| 363 | Supermarkets | Promo | X68 | unreviewed |
| 364 | Hospitals | Promo | X69 | unreviewed |
| 365 | Public Baths | Promo | X70 | unreviewed |
| 366 | City Parks | Promo | X71 | unreviewed |
| 367 | Casinos | Promo | X72 | unreviewed |
| 368 | Protected Growth | Promo | X73 | unreviewed |
| 369 | Static Harvesting | Promo | X74 | unreviewed |
| 370 | Vermin | Promo | X75 | unreviewed |
| 371 | Weather Balloons | Promo | X76 | unreviewed |
| 372 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
