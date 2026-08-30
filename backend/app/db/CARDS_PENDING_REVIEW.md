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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Eos Chasma National Park | Base | 026 | unreviewed |
| 2 | Interstellar Colony Ship | Corporate Era | 027 | unreviewed |
| 3 | Security Fleet | Corporate Era | 028 | unreviewed |
| 4 | Cupola City | Base | 029 | unreviewed |
| 5 | Lunar Beam | Base | 030 | unreviewed |
| 6 | Optimal Aerobraking | Base | 031 | unreviewed |
| 7 | Underground City | Base | 032 | unreviewed |
| 8 | GHG Producing Bacteria | Base | 034 | unreviewed |
| 9 | Ants | Base | 035 | unreviewed |
| 10 | Release of Inert Gases | Base | 036 | unreviewed |
| 11 | Nitrogen-Rich Asteroid | Base | 037 | unreviewed |
| 12 | Rover Construction | Base | 038 | unreviewed |
| 13 | Deimos Down | Base | 039 | unreviewed |
| 14 | Asteroid Mining | Base | 040 | unreviewed |
| 15 | Food Factory | Base | 041 | unreviewed |
| 16 | Archaebacteria | Base | 042 | unreviewed |
| 17 | Carbonate Processing | Base | 043 | unreviewed |
| 18 | Natural Preserve | Base | 044 | unreviewed |
| 19 | Lightning Harvest | Corporate Era | 046 | unreviewed |
| 20 | Algae | Base | 047 | unreviewed |
| 21 | Adapted Lichen | Base | 048 | unreviewed |
| 22 | Tardigrades | Corporate Era | 049 | unreviewed |
| 23 | Virus | Corporate Era | 050 | unreviewed |
| 24 | Miranda Resort | Corporate Era | 051 | unreviewed |
| 25 | Fish | Base | 052 | unreviewed |
| 26 | Lake Marineris | Base | 053 | unreviewed |
| 27 | Small Animals | Base | 054 | unreviewed |
| 28 | Kelp Farming | Base | 055 | unreviewed |
| 29 | Vesta Shipyard | Corporate Era | 057 | unreviewed |
| 30 | Beam from a Thorium Asteroid | Base | 058 | unreviewed |
| 31 | Mangrove | Base | 059 | unreviewed |
| 32 | Trees | Base | 060 | unreviewed |
| 33 | Great Escarpment Consortium | Corporate Era | 061 | unreviewed |
| 34 | Mineral Deposit | Corporate Era | 062 | unreviewed |
| 35 | Mining Expedition | Base | 063 | unreviewed |
| 36 | Mining Area | Corporate Era | 064 | unreviewed |
| 37 | Building Industries | Corporate Era | 065 | unreviewed |
| 38 | Land Claim | Corporate Era | 066 | unreviewed |
| 39 | Mining Rights | Base | 067 | unreviewed |
| 40 | Electro Catapult | Corporate Era | 069 | unreviewed |
| 41 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 42 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 43 | Birds | Base | 072 | unreviewed |
| 44 | Mars University | Corporate Era | 073 | unreviewed |
| 45 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 46 | Towing a Comet | Base | 075 | unreviewed |
| 47 | Space Mirrors | Base | 076 | unreviewed |
| 48 | Ice Asteroid | Base | 078 | unreviewed |
| 49 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 50 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 51 | Ganymede Colony | Base | 081 | unreviewed |
| 52 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 53 | Giant Space Mirror | Base | 083 | unreviewed |
| 54 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 55 | Commercial District | Corporate Era | 085 | unreviewed |
| 56 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 57 | Grass | Base | 087 | unreviewed |
| 58 | Heather | Base | 088 | unreviewed |
| 59 | Peroxide Power | Base | 089 | unreviewed |
| 60 | Research | Corporate Era | 090 | unreviewed |
| 61 | Gene Repair | Corporate Era | 091 | unreviewed |
| 62 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 63 | Bushes | Base | 093 | unreviewed |
| 64 | Mass Converter | Corporate Era | 094 | unreviewed |
| 65 | Physics Complex | Corporate Era | 095 | unreviewed |
| 66 | Greenhouses | Base | 096 | unreviewed |
| 67 | Nuclear Zone | Base | 097 | unreviewed |
| 68 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 69 | Toll Station | Corporate Era | 099 | unreviewed |
| 70 | Fueled Generators | Base | 100 | unreviewed |
| 71 | Power Grid | Base | 102 | unreviewed |
| 72 | Ore Processor | Base | 104 | unreviewed |
| 73 | Earth Office | Corporate Era | 105 | unreviewed |
| 74 | Media Archives | Corporate Era | 107 | unreviewed |
| 75 | Open City | Base | 108 | unreviewed |
| 76 | Media Group | Corporate Era | 109 | unreviewed |
| 77 | Business Network | Corporate Era | 110 | unreviewed |
| 78 | Business Contacts | Corporate Era | 111 | unreviewed |
| 79 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 80 | Breathing Filters | Base | 114 | unreviewed |

| 81 | Artificial Lake | Base | 116 | unreviewed |
| 82 | Geothermal Power | Base | 117 | unreviewed |
| 83 | Dust Seals | Base | 119 | unreviewed |
| 84 | Urbanized Area | Base | 120 | unreviewed |
| 85 | Sabotage | Corporate Era | 121 | unreviewed |
| 86 | Moss | Base | 122 | unreviewed |
| 87 | Industrial Center | Corporate Era | 123 | unreviewed |
| 88 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 89 | Hackers | Corporate Era | 125 | unreviewed |
| 90 | GHG Factories | Base | 126 | unreviewed |
| 91 | Subterranean Reservoir | Base | 127 | unreviewed |
| 92 | Ecological Zone | Base | 128 | unreviewed |
| 93 | Zeppelins | Base | 129 | unreviewed |
| 94 | Worms | Base | 130 | unreviewed |
| 95 | Decomposers | Base | 131 | unreviewed |
| 96 | Fusion Power | Base | 132 | unreviewed |
| 97 | Symbiotic Fungus | Base | 133 | unreviewed |
| 98 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 99 | Advanced Ecosystems | Base | 135 | unreviewed |
| 100 | Great Dam | Base | 136 | unreviewed |
| 101 | Cartel | Corporate Era | 137 | unreviewed |
| 102 | Strip Mine | Base | 138 | unreviewed |
| 103 | Wave Power | Base | 139 | unreviewed |
| 104 | Lava Flows | Base | 140 | unreviewed |
| 105 | Power Plant | Base | 141 | unreviewed |
| 106 | Mohole Area | Base | 142 | unreviewed |
| 107 | Large Convoy | Base | 143 | unreviewed |
| 108 | Tectonic Stress Power | Base | 145 | unreviewed |
| 109 | Herbivores | Base | 147 | unreviewed |
| 110 | Insects | Base | 148 | unreviewed |
| 111 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 112 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 113 | Adaptation Technology | Base | 153 | unreviewed |
| 114 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 115 | Designed Microorganisms | Base | 155 | unreviewed |
| 116 | Standard Technology | Corporate Era | 156 | unreviewed |
| 117 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 118 | Industrial Microbes | Base | 158 | unreviewed |
| 119 | Lichen | Base | 159 | unreviewed |
| 120 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 121 | Convoy from Europa | Base | 161 | unreviewed |
| 122 | Imported GHG | Base | 162 | unreviewed |
| 123 | Imported Nitrogen | Base | 163 | unreviewed |
| 124 | Micro-Mills | Base | 164 | unreviewed |
| 125 | Magnetic Field Generators | Base | 165 | unreviewed |
| 126 | Shuttles | Base | 166 | unreviewed |
| 127 | Import of Advanced GHG | Base | 167 | unreviewed |
| 128 | Windmills | Base | 168 | unreviewed |
| 129 | Tundra Farming | Base | 169 | unreviewed |
| 130 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 131 | Magnetic Field Dome | Base | 171 | unreviewed |
| 132 | Pets | Base | 172 | unreviewed |
| 133 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 134 | Protected Valley | Base | 174 | unreviewed |
| 135 | Satellites | Corporate Era | 175 | unreviewed |
| 136 | Noctis Farming | Base | 176 | unreviewed |
| 137 | Water Splitting Plant | Base | 177 | unreviewed |
| 138 | Heat Trappers | Base | 178 | unreviewed |
| 139 | Soil Factory | Base | 179 | unreviewed |
| 140 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 141 | Ice Cap Melting | Base | 181 | unreviewed |
| 142 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 143 | Biomass Combustors | Base | 183 | unreviewed |
| 144 | Livestock | Base | 184 | unreviewed |
| 145 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 146 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 147 | Aquifer Pumping | Base | 187 | unreviewed |
| 148 | Flooding | Base | 188 | unreviewed |
| 149 | Energy Saving | Base | 189 | unreviewed |
| 150 | Local Heat Trapping | Base | 190 | unreviewed |
| 151 | Permafrost Extraction | Base | 191 | unreviewed |
| 152 | Invention Contest | Corporate Era | 192 | unreviewed |
| 153 | Plantation | Base | 193 | unreviewed |
| 154 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 155 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 156 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 157 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 158 | Immigration Shuttles | Base | 198 | unreviewed |
| 159 | Restricted Area | Corporate Era | 199 | unreviewed |
| 160 | Immigrant City | Base | 200 | unreviewed |
| 161 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 162 | Underground Detonations | Base | 202 | unreviewed |
| 163 | Soletta | Base | 203 | unreviewed |
| 164 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 165 | Rad-Chem Factory | Base | 205 | unreviewed |
| 166 | Special Design | Base | 206 | unreviewed |
| 167 | Medical Lab | Corporate Era | 207 | unreviewed |
| 168 | AI Central | Corporate Era | 208 | unreviewed |
| 169 | Small Asteroid | Promo | 209 | unreviewed |
| 170 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 171 | Snow Algae | Promo | 211 | unreviewed |
| 172 | Penguins | Promo | 212 | unreviewed |
| 173 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 174 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 175 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 176 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 177 | Atmoscoop | Venus Next | 217 | unreviewed |
| 178 | Comet for Venus | Venus Next | 218 | unreviewed |
| 179 | Corroder Suits | Venus Next | 219 | unreviewed |
| 180 | Dawn City | Venus Next | 220 | unreviewed |
| 181 | Deuterium Export | Venus Next | 221 | unreviewed |
| 182 | Dirigibles | Venus Next | 222 | unreviewed |
| 183 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 184 | Extremophiles | Venus Next | 224 | unreviewed |
| 185 | Floating Habs | Venus Next | 225 | unreviewed |
| 186 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 187 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 188 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 189 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 190 | Gyropolis | Venus Next | 230 | unreviewed |
| 191 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 192 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 193 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 194 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 195 | Local Shading | Venus Next | 235 | unreviewed |
| 196 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 197 | Luxury Foods | Venus Next | 237 | unreviewed |
| 198 | Maxwell Base | Venus Next | 238 | unreviewed |
| 199 | Mining Quota | Venus Next | 239 | unreviewed |
| 200 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 201 | Omnicourt | Venus Next | 241 | unreviewed |
| 202 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 203 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 204 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 205 | Solarnet | Venus Next | 245 | unreviewed |
| 206 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 207 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 208 | Stratopolis | Venus Next | 248 | unreviewed |
| 209 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 210 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 211 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 212 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 213 | Thermophiles | Venus Next | 253 | unreviewed |
| 214 | Water to Venus | Venus Next | 254 | unreviewed |
| 215 | Venus Governor | Venus Next | 255 | unreviewed |
| 216 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 217 | Venus Soils | Venus Next | 257 | unreviewed |
| 218 | Venus Waystation | Venus Next | 258 | unreviewed |
| 219 | Venusian Animals | Venus Next | 259 | unreviewed |
| 220 | Venusian Insects | Venus Next | 260 | unreviewed |
| 221 | Venusian Plants | Venus Next | 261 | unreviewed |
| 222 | Airliners | Colonies | C01 | unreviewed |
| 223 | Air Raid | Colonies | C02 | unreviewed |
| 224 | Atmo Collectors | Colonies | C03 | unreviewed |
| 225 | Community Services | Colonies | C04 | unreviewed |
| 226 | Conscription | Colonies | C05 | unreviewed |
| 227 | Corona Extractor | Colonies | C06 | unreviewed |
| 228 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 229 | Earth Elevator | Colonies | C08 | unreviewed |
| 230 | Ecology Research | Colonies | C09 | unreviewed |
| 231 | Floater Leasing | Colonies | C10 | unreviewed |
| 232 | Floater Prototypes | Colonies | C11 | unreviewed |
| 233 | Floater Technology | Colonies | C12 | unreviewed |
| 234 | Galilean Waystation | Colonies | C13 | unreviewed |
| 235 | Heavy Taxation | Colonies | C14 | unreviewed |
| 236 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 237 | Impactor Swarm | Colonies | C16 | unreviewed |
| 238 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 239 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 240 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 241 | Luna Governor | Colonies | C20 | unreviewed |
| 242 | Lunar Exports | Colonies | C21 | unreviewed |
| 243 | Lunar Mining | Colonies | C22 | unreviewed |
| 244 | Market Manipulation | Colonies | C23 | unreviewed |
| 245 | Martian Zoo | Colonies | C24 | unreviewed |
| 246 | Mining Colony | Colonies | C25 | unreviewed |
| 247 | Minority Refuge | Colonies | C26 | unreviewed |
| 248 | Molecular Printing | Colonies | C27 | unreviewed |
| 249 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 250 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 251 | Productive Outpost | Colonies | C30 | unreviewed |
| 252 | Quantum Communications | Colonies | C31 | unreviewed |
| 253 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 254 | Refugee Camps | Colonies | C33 | unreviewed |
| 255 | Research Colony | Colonies | C34 | unreviewed |
| 256 | Rim Freighters | Colonies | C35 | unreviewed |
| 257 | Sky Docks | Colonies | C36 | unreviewed |
| 258 | Solar Probe | Colonies | C37 | unreviewed |
| 259 | Solar Reflectors | Colonies | C38 | unreviewed |
| 260 | Space Port | Colonies | C39 | unreviewed |
| 261 | Space Port Colony | Colonies | C40 | unreviewed |
| 262 | Spin-Off Department | Colonies | C41 | unreviewed |
| 263 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 264 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 265 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 266 | Titan Shuttles | Colonies | C45 | unreviewed |
| 267 | Trade Envoys | Colonies | C46 | unreviewed |
| 268 | Trading Colony | Colonies | C47 | unreviewed |
| 269 | Urban Decomposers | Colonies | C48 | unreviewed |
| 270 | Warp Drive | Colonies | C49 | unreviewed |
| 271 | House Printing | Prelude | P36 | unreviewed |
| 272 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 273 | Martian Survey | Prelude | P38 | unreviewed |
| 274 | Psychrophiles | Prelude | P39 | unreviewed |
| 275 | Research Coordination | Prelude | P40 | unreviewed |
| 276 | SF Memorial | Prelude | P41 | unreviewed |
| 277 | Space Hotels | Prelude | P42 | unreviewed |
| 278 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 279 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 280 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 281 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 282 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 283 | Floating Refinery | Venus Next | P73 | unreviewed |
| 284 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 285 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 286 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 287 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 288 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 289 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 290 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 291 | Soil Studies | Venus Next | P81 | unreviewed |
| 292 | Special Permit | Prelude 2 | P82 | unreviewed |
| 293 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 294 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 295 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 296 | Unexpected Application | Venus Next | P86 | unreviewed |
| 297 | Venus Allies | Venus Next | P87 | unreviewed |
| 298 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 299 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 300 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 301 | WG Project | Prelude 2 | P91 | unreviewed |
| 302 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 303 | Banned Delegate | Turmoil | T02 | unreviewed |
| 304 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 305 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 306 | Event Analysts | Turmoil | T05 | unreviewed |
| 307 | GMO Contract | Turmoil | T06 | unreviewed |
| 308 | Martian Media Center | Turmoil | T07 | unreviewed |
| 309 | Parliament Hall | Turmoil | T08 | unreviewed |
| 310 | PR Office | Turmoil | T09 | unreviewed |
| 311 | Public Celebrations | Turmoil | T10 | unreviewed |
| 312 | Recruitment | Turmoil | T11 | unreviewed |
| 313 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 314 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 315 | Supported Research | Turmoil | T14 | unreviewed |
| 316 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 317 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 318 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 319 | Project Inspection | Promo | X02 | unreviewed |
| 320 | Energy Market | Promo | X03 | unreviewed |
| 321 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 322 | Interplanetary Trade | Promo | X05 | unreviewed |
| 323 | Law Suit | Promo | X06 | unreviewed |
| 324 | Mercurian Alloys | Promo | X07 | unreviewed |
| 325 | Orbital Cleanup | Promo | X08 | unreviewed |
| 326 | Political Alliance | Promo | X09 | unreviewed |
| 327 | Rego Plastics | Promo | X10 | unreviewed |
| 328 | Saturn Surfing | Promo | X11 | unreviewed |
| 329 | Stanford Torus | Promo | X12 | unreviewed |
| 330 | Advertising | Promo | X13 | unreviewed |
| 331 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 332 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 333 | Comet Aiming | Promo | X16 | unreviewed |
| 334 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 335 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 336 | Directed Impactors | Promo | X19 | unreviewed |
| 337 | Diversity Support | Promo | X20 | unreviewed |
| 338 | Field-Capped City | Promo | X21 | unreviewed |
| 339 | Imported Nutrients | Promo | X22 | unreviewed |
| 340 | Jovian Embassy | Promo | X23 | unreviewed |
| 341 | Magnetic Shield | Promo | X24 | unreviewed |
| 342 | Meat Industry | Promo | X25 | unreviewed |
| 343 | Meltworks | Promo | X26 | unreviewed |
| 344 | Mohole Lake | Promo | X27 | unreviewed |
| 345 | Potatoes | Promo | X28 | unreviewed |
| 346 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 347 | Topsoil Contract | Promo | X30 | unreviewed |
| 348 | Asteroid Rights | Promo | X34 | unreviewed |
| 349 | Bactoviral Research | Promo | X35 | unreviewed |
| 350 | Bio Printing Facility | Promo | X36 | unreviewed |
| 351 | Harvest | Promo | X37 | unreviewed |
| 352 | Outdoor Sports | Promo | X38 | unreviewed |
| 353 | 16 Psyche | Promo | X44 | unreviewed |
| 354 | Robot Pollinators | Promo | X45 | unreviewed |
| 355 | Supercapacitors | Promo | X46 | unreviewed |
| 356 | Icy Impactors | Promo | X47 | unreviewed |
| 357 | Directed Heat Usage | Promo | X48 | unreviewed |
| 358 | Aqueduct Systems | Promo | X50 | unreviewed |
| 359 | Astra Mechanica | Promo | X51 | unreviewed |
| 360 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 361 | Cyberia Systems | Promo | X53 | unreviewed |
| 362 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 363 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 364 | Kaguya Tech | Promo | X58 | unreviewed |
| 365 | Mars Nomads | Promo | X59 | unreviewed |
| 366 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 367 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 368 | Red Ships | Promo | X62 | unreviewed |
| 369 | Solar Logistics | Promo | X63 | unreviewed |
| 370 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 371 | Teslaract | Promo | X66 | unreviewed |
| 372 | Soil Enrichment | Promo | X67 | unreviewed |
| 373 | Supermarkets | Promo | X68 | unreviewed |
| 374 | Hospitals | Promo | X69 | unreviewed |
| 375 | Public Baths | Promo | X70 | unreviewed |
| 376 | City Parks | Promo | X71 | unreviewed |
| 377 | Casinos | Promo | X72 | unreviewed |
| 378 | Protected Growth | Promo | X73 | unreviewed |
| 379 | Static Harvesting | Promo | X74 | unreviewed |
| 380 | Vermin | Promo | X75 | unreviewed |
| 381 | Weather Balloons | Promo | X76 | unreviewed |
| 382 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
