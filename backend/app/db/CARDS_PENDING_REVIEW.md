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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Domed Crater | Base | 016 | unreviewed |
| 2 | Noctis City | Base | 017 | unreviewed |
| 3 | Methane from Titan | Base | 018 | unreviewed |
| 4 | Imported Hydrogen | Base | 019 | unreviewed |
| 5 | Research Outpost | Base | 020 | unreviewed |
| 6 | Phobos Space Haven | Base | 021 | unreviewed |
| 7 | Black Polar Dust | Base | 022 | unreviewed |
| 8 | Arctic Algae | Base | 023 | unreviewed |
| 9 | Predators | Base | 024 | unreviewed |
| 10 | Space Station | Corporate Era | 025 | unreviewed |
| 11 | Eos Chasma National Park | Base | 026 | unreviewed |
| 12 | Interstellar Colony Ship | Corporate Era | 027 | unreviewed |
| 13 | Security Fleet | Corporate Era | 028 | unreviewed |
| 14 | Cupola City | Base | 029 | unreviewed |
| 15 | Lunar Beam | Base | 030 | unreviewed |
| 16 | Optimal Aerobraking | Base | 031 | unreviewed |
| 17 | Underground City | Base | 032 | unreviewed |
| 18 | GHG Producing Bacteria | Base | 034 | unreviewed |
| 19 | Ants | Base | 035 | unreviewed |
| 20 | Release of Inert Gases | Base | 036 | unreviewed |
| 21 | Nitrogen-Rich Asteroid | Base | 037 | unreviewed |
| 22 | Rover Construction | Base | 038 | unreviewed |
| 23 | Deimos Down | Base | 039 | unreviewed |
| 24 | Asteroid Mining | Base | 040 | unreviewed |
| 25 | Food Factory | Base | 041 | unreviewed |
| 26 | Archaebacteria | Base | 042 | unreviewed |
| 27 | Carbonate Processing | Base | 043 | unreviewed |
| 28 | Natural Preserve | Base | 044 | unreviewed |
| 29 | Lightning Harvest | Corporate Era | 046 | unreviewed |
| 30 | Algae | Base | 047 | unreviewed |
| 31 | Adapted Lichen | Base | 048 | unreviewed |
| 32 | Tardigrades | Corporate Era | 049 | unreviewed |
| 33 | Virus | Corporate Era | 050 | unreviewed |
| 34 | Miranda Resort | Corporate Era | 051 | unreviewed |
| 35 | Fish | Base | 052 | unreviewed |
| 36 | Lake Marineris | Base | 053 | unreviewed |
| 37 | Small Animals | Base | 054 | unreviewed |
| 38 | Kelp Farming | Base | 055 | unreviewed |
| 39 | Vesta Shipyard | Corporate Era | 057 | unreviewed |
| 40 | Beam from a Thorium Asteroid | Base | 058 | unreviewed |
| 41 | Mangrove | Base | 059 | unreviewed |
| 42 | Trees | Base | 060 | unreviewed |
| 43 | Great Escarpment Consortium | Corporate Era | 061 | unreviewed |
| 44 | Mineral Deposit | Corporate Era | 062 | unreviewed |
| 45 | Mining Expedition | Base | 063 | unreviewed |
| 46 | Mining Area | Corporate Era | 064 | unreviewed |
| 47 | Building Industries | Corporate Era | 065 | unreviewed |
| 48 | Land Claim | Corporate Era | 066 | unreviewed |
| 49 | Mining Rights | Base | 067 | unreviewed |
| 50 | Electro Catapult | Corporate Era | 069 | unreviewed |
| 51 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 52 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 53 | Birds | Base | 072 | unreviewed |
| 54 | Mars University | Corporate Era | 073 | unreviewed |
| 55 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 56 | Towing a Comet | Base | 075 | unreviewed |
| 57 | Space Mirrors | Base | 076 | unreviewed |
| 58 | Ice Asteroid | Base | 078 | unreviewed |
| 59 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 60 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 61 | Ganymede Colony | Base | 081 | unreviewed |
| 62 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 63 | Giant Space Mirror | Base | 083 | unreviewed |
| 64 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 65 | Commercial District | Corporate Era | 085 | unreviewed |
| 66 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 67 | Grass | Base | 087 | unreviewed |
| 68 | Heather | Base | 088 | unreviewed |
| 69 | Peroxide Power | Base | 089 | unreviewed |
| 70 | Research | Corporate Era | 090 | unreviewed |
| 71 | Gene Repair | Corporate Era | 091 | unreviewed |
| 72 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 73 | Bushes | Base | 093 | unreviewed |
| 74 | Mass Converter | Corporate Era | 094 | unreviewed |
| 75 | Physics Complex | Corporate Era | 095 | unreviewed |
| 76 | Greenhouses | Base | 096 | unreviewed |
| 77 | Nuclear Zone | Base | 097 | unreviewed |
| 78 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 79 | Toll Station | Corporate Era | 099 | unreviewed |
| 80 | Fueled Generators | Base | 100 | unreviewed |
| 81 | Power Grid | Base | 102 | unreviewed |
| 82 | Ore Processor | Base | 104 | unreviewed |
| 83 | Earth Office | Corporate Era | 105 | unreviewed |
| 84 | Media Archives | Corporate Era | 107 | unreviewed |
| 85 | Open City | Base | 108 | unreviewed |
| 86 | Media Group | Corporate Era | 109 | unreviewed |
| 87 | Business Network | Corporate Era | 110 | unreviewed |
| 88 | Business Contacts | Corporate Era | 111 | unreviewed |
| 89 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 90 | Breathing Filters | Base | 114 | unreviewed |

| 91 | Artificial Lake | Base | 116 | unreviewed |
| 92 | Geothermal Power | Base | 117 | unreviewed |
| 93 | Dust Seals | Base | 119 | unreviewed |
| 94 | Urbanized Area | Base | 120 | unreviewed |
| 95 | Sabotage | Corporate Era | 121 | unreviewed |
| 96 | Moss | Base | 122 | unreviewed |
| 97 | Industrial Center | Corporate Era | 123 | unreviewed |
| 98 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 99 | Hackers | Corporate Era | 125 | unreviewed |
| 100 | GHG Factories | Base | 126 | unreviewed |
| 101 | Subterranean Reservoir | Base | 127 | unreviewed |
| 102 | Ecological Zone | Base | 128 | unreviewed |
| 103 | Zeppelins | Base | 129 | unreviewed |
| 104 | Worms | Base | 130 | unreviewed |
| 105 | Decomposers | Base | 131 | unreviewed |
| 106 | Fusion Power | Base | 132 | unreviewed |
| 107 | Symbiotic Fungus | Base | 133 | unreviewed |
| 108 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 109 | Advanced Ecosystems | Base | 135 | unreviewed |
| 110 | Great Dam | Base | 136 | unreviewed |
| 111 | Cartel | Corporate Era | 137 | unreviewed |
| 112 | Strip Mine | Base | 138 | unreviewed |
| 113 | Wave Power | Base | 139 | unreviewed |
| 114 | Lava Flows | Base | 140 | unreviewed |
| 115 | Power Plant | Base | 141 | unreviewed |
| 116 | Mohole Area | Base | 142 | unreviewed |
| 117 | Large Convoy | Base | 143 | unreviewed |
| 118 | Tectonic Stress Power | Base | 145 | unreviewed |
| 119 | Herbivores | Base | 147 | unreviewed |
| 120 | Insects | Base | 148 | unreviewed |
| 121 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 122 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 123 | Adaptation Technology | Base | 153 | unreviewed |
| 124 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 125 | Designed Microorganisms | Base | 155 | unreviewed |
| 126 | Standard Technology | Corporate Era | 156 | unreviewed |
| 127 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 128 | Industrial Microbes | Base | 158 | unreviewed |
| 129 | Lichen | Base | 159 | unreviewed |
| 130 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 131 | Convoy from Europa | Base | 161 | unreviewed |
| 132 | Imported GHG | Base | 162 | unreviewed |
| 133 | Imported Nitrogen | Base | 163 | unreviewed |
| 134 | Micro-Mills | Base | 164 | unreviewed |
| 135 | Magnetic Field Generators | Base | 165 | unreviewed |
| 136 | Shuttles | Base | 166 | unreviewed |
| 137 | Import of Advanced GHG | Base | 167 | unreviewed |
| 138 | Windmills | Base | 168 | unreviewed |
| 139 | Tundra Farming | Base | 169 | unreviewed |
| 140 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 141 | Magnetic Field Dome | Base | 171 | unreviewed |
| 142 | Pets | Base | 172 | unreviewed |
| 143 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 144 | Protected Valley | Base | 174 | unreviewed |
| 145 | Satellites | Corporate Era | 175 | unreviewed |
| 146 | Noctis Farming | Base | 176 | unreviewed |
| 147 | Water Splitting Plant | Base | 177 | unreviewed |
| 148 | Heat Trappers | Base | 178 | unreviewed |
| 149 | Soil Factory | Base | 179 | unreviewed |
| 150 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 151 | Ice Cap Melting | Base | 181 | unreviewed |
| 152 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 153 | Biomass Combustors | Base | 183 | unreviewed |
| 154 | Livestock | Base | 184 | unreviewed |
| 155 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 156 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 157 | Aquifer Pumping | Base | 187 | unreviewed |
| 158 | Flooding | Base | 188 | unreviewed |
| 159 | Energy Saving | Base | 189 | unreviewed |
| 160 | Local Heat Trapping | Base | 190 | unreviewed |
| 161 | Permafrost Extraction | Base | 191 | unreviewed |
| 162 | Invention Contest | Corporate Era | 192 | unreviewed |
| 163 | Plantation | Base | 193 | unreviewed |
| 164 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 165 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 166 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 167 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 168 | Immigration Shuttles | Base | 198 | unreviewed |
| 169 | Restricted Area | Corporate Era | 199 | unreviewed |
| 170 | Immigrant City | Base | 200 | unreviewed |
| 171 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 172 | Underground Detonations | Base | 202 | unreviewed |
| 173 | Soletta | Base | 203 | unreviewed |
| 174 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 175 | Rad-Chem Factory | Base | 205 | unreviewed |
| 176 | Special Design | Base | 206 | unreviewed |
| 177 | Medical Lab | Corporate Era | 207 | unreviewed |
| 178 | AI Central | Corporate Era | 208 | unreviewed |
| 179 | Small Asteroid | Promo | 209 | unreviewed |
| 180 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 181 | Snow Algae | Promo | 211 | unreviewed |
| 182 | Penguins | Promo | 212 | unreviewed |
| 183 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 184 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 185 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 186 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 187 | Atmoscoop | Venus Next | 217 | unreviewed |
| 188 | Comet for Venus | Venus Next | 218 | unreviewed |
| 189 | Corroder Suits | Venus Next | 219 | unreviewed |
| 190 | Dawn City | Venus Next | 220 | unreviewed |
| 191 | Deuterium Export | Venus Next | 221 | unreviewed |
| 192 | Dirigibles | Venus Next | 222 | unreviewed |
| 193 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 194 | Extremophiles | Venus Next | 224 | unreviewed |
| 195 | Floating Habs | Venus Next | 225 | unreviewed |
| 196 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 197 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 198 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 199 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 200 | Gyropolis | Venus Next | 230 | unreviewed |
| 201 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 202 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 203 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 204 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 205 | Local Shading | Venus Next | 235 | unreviewed |
| 206 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 207 | Luxury Foods | Venus Next | 237 | unreviewed |
| 208 | Maxwell Base | Venus Next | 238 | unreviewed |
| 209 | Mining Quota | Venus Next | 239 | unreviewed |
| 210 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 211 | Omnicourt | Venus Next | 241 | unreviewed |
| 212 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 213 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 214 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 215 | Solarnet | Venus Next | 245 | unreviewed |
| 216 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 217 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 218 | Stratopolis | Venus Next | 248 | unreviewed |
| 219 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 220 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 221 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 222 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 223 | Thermophiles | Venus Next | 253 | unreviewed |
| 224 | Water to Venus | Venus Next | 254 | unreviewed |
| 225 | Venus Governor | Venus Next | 255 | unreviewed |
| 226 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 227 | Venus Soils | Venus Next | 257 | unreviewed |
| 228 | Venus Waystation | Venus Next | 258 | unreviewed |
| 229 | Venusian Animals | Venus Next | 259 | unreviewed |
| 230 | Venusian Insects | Venus Next | 260 | unreviewed |
| 231 | Venusian Plants | Venus Next | 261 | unreviewed |
| 232 | Airliners | Colonies | C01 | unreviewed |
| 233 | Air Raid | Colonies | C02 | unreviewed |
| 234 | Atmo Collectors | Colonies | C03 | unreviewed |
| 235 | Community Services | Colonies | C04 | unreviewed |
| 236 | Conscription | Colonies | C05 | unreviewed |
| 237 | Corona Extractor | Colonies | C06 | unreviewed |
| 238 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 239 | Earth Elevator | Colonies | C08 | unreviewed |
| 240 | Ecology Research | Colonies | C09 | unreviewed |
| 241 | Floater Leasing | Colonies | C10 | unreviewed |
| 242 | Floater Prototypes | Colonies | C11 | unreviewed |
| 243 | Floater Technology | Colonies | C12 | unreviewed |
| 244 | Galilean Waystation | Colonies | C13 | unreviewed |
| 245 | Heavy Taxation | Colonies | C14 | unreviewed |
| 246 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 247 | Impactor Swarm | Colonies | C16 | unreviewed |
| 248 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 249 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 250 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 251 | Luna Governor | Colonies | C20 | unreviewed |
| 252 | Lunar Exports | Colonies | C21 | unreviewed |
| 253 | Lunar Mining | Colonies | C22 | unreviewed |
| 254 | Market Manipulation | Colonies | C23 | unreviewed |
| 255 | Martian Zoo | Colonies | C24 | unreviewed |
| 256 | Mining Colony | Colonies | C25 | unreviewed |
| 257 | Minority Refuge | Colonies | C26 | unreviewed |
| 258 | Molecular Printing | Colonies | C27 | unreviewed |
| 259 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 260 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 261 | Productive Outpost | Colonies | C30 | unreviewed |
| 262 | Quantum Communications | Colonies | C31 | unreviewed |
| 263 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 264 | Refugee Camps | Colonies | C33 | unreviewed |
| 265 | Research Colony | Colonies | C34 | unreviewed |
| 266 | Rim Freighters | Colonies | C35 | unreviewed |
| 267 | Sky Docks | Colonies | C36 | unreviewed |
| 268 | Solar Probe | Colonies | C37 | unreviewed |
| 269 | Solar Reflectors | Colonies | C38 | unreviewed |
| 270 | Space Port | Colonies | C39 | unreviewed |
| 271 | Space Port Colony | Colonies | C40 | unreviewed |
| 272 | Spin-Off Department | Colonies | C41 | unreviewed |
| 273 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 274 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 275 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 276 | Titan Shuttles | Colonies | C45 | unreviewed |
| 277 | Trade Envoys | Colonies | C46 | unreviewed |
| 278 | Trading Colony | Colonies | C47 | unreviewed |
| 279 | Urban Decomposers | Colonies | C48 | unreviewed |
| 280 | Warp Drive | Colonies | C49 | unreviewed |
| 281 | House Printing | Prelude | P36 | unreviewed |
| 282 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 283 | Martian Survey | Prelude | P38 | unreviewed |
| 284 | Psychrophiles | Prelude | P39 | unreviewed |
| 285 | Research Coordination | Prelude | P40 | unreviewed |
| 286 | SF Memorial | Prelude | P41 | unreviewed |
| 287 | Space Hotels | Prelude | P42 | unreviewed |
| 288 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 289 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 290 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 291 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 292 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 293 | Floating Refinery | Venus Next | P73 | unreviewed |
| 294 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 295 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 296 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 297 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 298 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 299 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 300 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 301 | Soil Studies | Venus Next | P81 | unreviewed |
| 302 | Special Permit | Prelude 2 | P82 | unreviewed |
| 303 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 304 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 305 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 306 | Unexpected Application | Venus Next | P86 | unreviewed |
| 307 | Venus Allies | Venus Next | P87 | unreviewed |
| 308 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 309 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 310 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 311 | WG Project | Prelude 2 | P91 | unreviewed |
| 312 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 313 | Banned Delegate | Turmoil | T02 | unreviewed |
| 314 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 315 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 316 | Event Analysts | Turmoil | T05 | unreviewed |
| 317 | GMO Contract | Turmoil | T06 | unreviewed |
| 318 | Martian Media Center | Turmoil | T07 | unreviewed |
| 319 | Parliament Hall | Turmoil | T08 | unreviewed |
| 320 | PR Office | Turmoil | T09 | unreviewed |
| 321 | Public Celebrations | Turmoil | T10 | unreviewed |
| 322 | Recruitment | Turmoil | T11 | unreviewed |
| 323 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 324 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 325 | Supported Research | Turmoil | T14 | unreviewed |
| 326 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 327 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 328 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 329 | Project Inspection | Promo | X02 | unreviewed |
| 330 | Energy Market | Promo | X03 | unreviewed |
| 331 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 332 | Interplanetary Trade | Promo | X05 | unreviewed |
| 333 | Law Suit | Promo | X06 | unreviewed |
| 334 | Mercurian Alloys | Promo | X07 | unreviewed |
| 335 | Orbital Cleanup | Promo | X08 | unreviewed |
| 336 | Political Alliance | Promo | X09 | unreviewed |
| 337 | Rego Plastics | Promo | X10 | unreviewed |
| 338 | Saturn Surfing | Promo | X11 | unreviewed |
| 339 | Stanford Torus | Promo | X12 | unreviewed |
| 340 | Advertising | Promo | X13 | unreviewed |
| 341 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 342 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 343 | Comet Aiming | Promo | X16 | unreviewed |
| 344 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 345 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 346 | Directed Impactors | Promo | X19 | unreviewed |
| 347 | Diversity Support | Promo | X20 | unreviewed |
| 348 | Field-Capped City | Promo | X21 | unreviewed |
| 349 | Imported Nutrients | Promo | X22 | unreviewed |
| 350 | Jovian Embassy | Promo | X23 | unreviewed |
| 351 | Magnetic Shield | Promo | X24 | unreviewed |
| 352 | Meat Industry | Promo | X25 | unreviewed |
| 353 | Meltworks | Promo | X26 | unreviewed |
| 354 | Mohole Lake | Promo | X27 | unreviewed |
| 355 | Potatoes | Promo | X28 | unreviewed |
| 356 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 357 | Topsoil Contract | Promo | X30 | unreviewed |
| 358 | Asteroid Rights | Promo | X34 | unreviewed |
| 359 | Bactoviral Research | Promo | X35 | unreviewed |
| 360 | Bio Printing Facility | Promo | X36 | unreviewed |
| 361 | Harvest | Promo | X37 | unreviewed |
| 362 | Outdoor Sports | Promo | X38 | unreviewed |
| 363 | 16 Psyche | Promo | X44 | unreviewed |
| 364 | Robot Pollinators | Promo | X45 | unreviewed |
| 365 | Supercapacitors | Promo | X46 | unreviewed |
| 366 | Icy Impactors | Promo | X47 | unreviewed |
| 367 | Directed Heat Usage | Promo | X48 | unreviewed |
| 368 | Aqueduct Systems | Promo | X50 | unreviewed |
| 369 | Astra Mechanica | Promo | X51 | unreviewed |
| 370 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 371 | Cyberia Systems | Promo | X53 | unreviewed |
| 372 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 373 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 374 | Kaguya Tech | Promo | X58 | unreviewed |
| 375 | Mars Nomads | Promo | X59 | unreviewed |
| 376 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 377 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 378 | Red Ships | Promo | X62 | unreviewed |
| 379 | Solar Logistics | Promo | X63 | unreviewed |
| 380 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 381 | Teslaract | Promo | X66 | unreviewed |
| 382 | Soil Enrichment | Promo | X67 | unreviewed |
| 383 | Supermarkets | Promo | X68 | unreviewed |
| 384 | Hospitals | Promo | X69 | unreviewed |
| 385 | Public Baths | Promo | X70 | unreviewed |
| 386 | City Parks | Promo | X71 | unreviewed |
| 387 | Casinos | Promo | X72 | unreviewed |
| 388 | Protected Growth | Promo | X73 | unreviewed |
| 389 | Static Harvesting | Promo | X74 | unreviewed |
| 390 | Vermin | Promo | X75 | unreviewed |
| 391 | Weather Balloons | Promo | X76 | unreviewed |
| 392 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
