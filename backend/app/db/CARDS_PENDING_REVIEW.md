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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Adapted Lichen | Base | 048 | unreviewed |
| 2 | Tardigrades | Corporate Era | 049 | unreviewed |
| 3 | Virus | Corporate Era | 050 | unreviewed |
| 4 | Miranda Resort | Corporate Era | 051 | unreviewed |
| 5 | Fish | Base | 052 | unreviewed |
| 6 | Lake Marineris | Base | 053 | unreviewed |
| 7 | Small Animals | Base | 054 | unreviewed |
| 8 | Kelp Farming | Base | 055 | unreviewed |
| 9 | Vesta Shipyard | Corporate Era | 057 | unreviewed |
| 10 | Beam from a Thorium Asteroid | Base | 058 | unreviewed |
| 11 | Mangrove | Base | 059 | unreviewed |
| 12 | Trees | Base | 060 | unreviewed |
| 13 | Great Escarpment Consortium | Corporate Era | 061 | unreviewed |
| 14 | Mineral Deposit | Corporate Era | 062 | unreviewed |
| 15 | Mining Expedition | Base | 063 | unreviewed |
| 16 | Mining Area | Corporate Era | 064 | unreviewed |
| 17 | Building Industries | Corporate Era | 065 | unreviewed |
| 18 | Land Claim | Corporate Era | 066 | unreviewed |
| 19 | Mining Rights | Base | 067 | unreviewed |
| 20 | Electro Catapult | Corporate Era | 069 | unreviewed |
| 21 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 22 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 23 | Birds | Base | 072 | unreviewed |
| 24 | Mars University | Corporate Era | 073 | unreviewed |
| 25 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 26 | Towing a Comet | Base | 075 | unreviewed |
| 27 | Space Mirrors | Base | 076 | unreviewed |
| 28 | Ice Asteroid | Base | 078 | unreviewed |
| 29 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 30 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 31 | Ganymede Colony | Base | 081 | unreviewed |
| 32 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 33 | Giant Space Mirror | Base | 083 | unreviewed |
| 34 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 35 | Commercial District | Corporate Era | 085 | unreviewed |
| 36 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 37 | Grass | Base | 087 | unreviewed |
| 38 | Heather | Base | 088 | unreviewed |
| 39 | Peroxide Power | Base | 089 | unreviewed |
| 40 | Research | Corporate Era | 090 | unreviewed |
| 41 | Gene Repair | Corporate Era | 091 | unreviewed |
| 42 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 43 | Bushes | Base | 093 | unreviewed |
| 44 | Mass Converter | Corporate Era | 094 | unreviewed |
| 45 | Physics Complex | Corporate Era | 095 | unreviewed |
| 46 | Greenhouses | Base | 096 | unreviewed |
| 47 | Nuclear Zone | Base | 097 | unreviewed |
| 48 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 49 | Toll Station | Corporate Era | 099 | unreviewed |
| 50 | Fueled Generators | Base | 100 | unreviewed |
| 51 | Power Grid | Base | 102 | unreviewed |
| 52 | Ore Processor | Base | 104 | unreviewed |
| 53 | Earth Office | Corporate Era | 105 | unreviewed |
| 54 | Media Archives | Corporate Era | 107 | unreviewed |
| 55 | Open City | Base | 108 | unreviewed |
| 56 | Media Group | Corporate Era | 109 | unreviewed |
| 57 | Business Network | Corporate Era | 110 | unreviewed |
| 58 | Business Contacts | Corporate Era | 111 | unreviewed |
| 59 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 60 | Breathing Filters | Base | 114 | unreviewed |

| 61 | Artificial Lake | Base | 116 | unreviewed |
| 62 | Geothermal Power | Base | 117 | unreviewed |
| 63 | Dust Seals | Base | 119 | unreviewed |
| 64 | Urbanized Area | Base | 120 | unreviewed |
| 65 | Sabotage | Corporate Era | 121 | unreviewed |
| 66 | Moss | Base | 122 | unreviewed |
| 67 | Industrial Center | Corporate Era | 123 | unreviewed |
| 68 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 69 | Hackers | Corporate Era | 125 | unreviewed |
| 70 | GHG Factories | Base | 126 | unreviewed |
| 71 | Subterranean Reservoir | Base | 127 | unreviewed |
| 72 | Ecological Zone | Base | 128 | unreviewed |
| 73 | Zeppelins | Base | 129 | unreviewed |
| 74 | Worms | Base | 130 | unreviewed |
| 75 | Decomposers | Base | 131 | unreviewed |
| 76 | Fusion Power | Base | 132 | unreviewed |
| 77 | Symbiotic Fungus | Base | 133 | unreviewed |
| 78 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 79 | Advanced Ecosystems | Base | 135 | unreviewed |
| 80 | Great Dam | Base | 136 | unreviewed |
| 81 | Cartel | Corporate Era | 137 | unreviewed |
| 82 | Strip Mine | Base | 138 | unreviewed |
| 83 | Wave Power | Base | 139 | unreviewed |
| 84 | Lava Flows | Base | 140 | unreviewed |
| 85 | Power Plant | Base | 141 | unreviewed |
| 86 | Mohole Area | Base | 142 | unreviewed |
| 87 | Large Convoy | Base | 143 | unreviewed |
| 88 | Tectonic Stress Power | Base | 145 | unreviewed |
| 89 | Herbivores | Base | 147 | unreviewed |
| 90 | Insects | Base | 148 | unreviewed |
| 91 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 92 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 93 | Adaptation Technology | Base | 153 | unreviewed |
| 94 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 95 | Designed Microorganisms | Base | 155 | unreviewed |
| 96 | Standard Technology | Corporate Era | 156 | unreviewed |
| 97 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 98 | Industrial Microbes | Base | 158 | unreviewed |
| 99 | Lichen | Base | 159 | unreviewed |
| 100 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 101 | Convoy from Europa | Base | 161 | unreviewed |
| 102 | Imported GHG | Base | 162 | unreviewed |
| 103 | Imported Nitrogen | Base | 163 | unreviewed |
| 104 | Micro-Mills | Base | 164 | unreviewed |
| 105 | Magnetic Field Generators | Base | 165 | unreviewed |
| 106 | Shuttles | Base | 166 | unreviewed |
| 107 | Import of Advanced GHG | Base | 167 | unreviewed |
| 108 | Windmills | Base | 168 | unreviewed |
| 109 | Tundra Farming | Base | 169 | unreviewed |
| 110 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 111 | Magnetic Field Dome | Base | 171 | unreviewed |
| 112 | Pets | Base | 172 | unreviewed |
| 113 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 114 | Protected Valley | Base | 174 | unreviewed |
| 115 | Satellites | Corporate Era | 175 | unreviewed |
| 116 | Noctis Farming | Base | 176 | unreviewed |
| 117 | Water Splitting Plant | Base | 177 | unreviewed |
| 118 | Heat Trappers | Base | 178 | unreviewed |
| 119 | Soil Factory | Base | 179 | unreviewed |
| 120 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 121 | Ice Cap Melting | Base | 181 | unreviewed |
| 122 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 123 | Biomass Combustors | Base | 183 | unreviewed |
| 124 | Livestock | Base | 184 | unreviewed |
| 125 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 126 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 127 | Aquifer Pumping | Base | 187 | unreviewed |
| 128 | Flooding | Base | 188 | unreviewed |
| 129 | Energy Saving | Base | 189 | unreviewed |
| 130 | Local Heat Trapping | Base | 190 | unreviewed |
| 131 | Permafrost Extraction | Base | 191 | unreviewed |
| 132 | Invention Contest | Corporate Era | 192 | unreviewed |
| 133 | Plantation | Base | 193 | unreviewed |
| 134 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 135 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 136 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 137 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 138 | Immigration Shuttles | Base | 198 | unreviewed |
| 139 | Restricted Area | Corporate Era | 199 | unreviewed |
| 140 | Immigrant City | Base | 200 | unreviewed |
| 141 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 142 | Underground Detonations | Base | 202 | unreviewed |
| 143 | Soletta | Base | 203 | unreviewed |
| 144 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 145 | Rad-Chem Factory | Base | 205 | unreviewed |
| 146 | Special Design | Base | 206 | unreviewed |
| 147 | Medical Lab | Corporate Era | 207 | unreviewed |
| 148 | AI Central | Corporate Era | 208 | unreviewed |
| 149 | Small Asteroid | Promo | 209 | unreviewed |
| 150 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 151 | Snow Algae | Promo | 211 | unreviewed |
| 152 | Penguins | Promo | 212 | unreviewed |
| 153 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 154 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 155 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 156 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 157 | Atmoscoop | Venus Next | 217 | unreviewed |
| 158 | Comet for Venus | Venus Next | 218 | unreviewed |
| 159 | Corroder Suits | Venus Next | 219 | unreviewed |
| 160 | Dawn City | Venus Next | 220 | unreviewed |
| 161 | Deuterium Export | Venus Next | 221 | unreviewed |
| 162 | Dirigibles | Venus Next | 222 | unreviewed |
| 163 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 164 | Extremophiles | Venus Next | 224 | unreviewed |
| 165 | Floating Habs | Venus Next | 225 | unreviewed |
| 166 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 167 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 168 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 169 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 170 | Gyropolis | Venus Next | 230 | unreviewed |
| 171 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 172 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 173 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 174 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 175 | Local Shading | Venus Next | 235 | unreviewed |
| 176 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 177 | Luxury Foods | Venus Next | 237 | unreviewed |
| 178 | Maxwell Base | Venus Next | 238 | unreviewed |
| 179 | Mining Quota | Venus Next | 239 | unreviewed |
| 180 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 181 | Omnicourt | Venus Next | 241 | unreviewed |
| 182 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 183 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 184 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 185 | Solarnet | Venus Next | 245 | unreviewed |
| 186 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 187 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 188 | Stratopolis | Venus Next | 248 | unreviewed |
| 189 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 190 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 191 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 192 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 193 | Thermophiles | Venus Next | 253 | unreviewed |
| 194 | Water to Venus | Venus Next | 254 | unreviewed |
| 195 | Venus Governor | Venus Next | 255 | unreviewed |
| 196 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 197 | Venus Soils | Venus Next | 257 | unreviewed |
| 198 | Venus Waystation | Venus Next | 258 | unreviewed |
| 199 | Venusian Animals | Venus Next | 259 | unreviewed |
| 200 | Venusian Insects | Venus Next | 260 | unreviewed |
| 201 | Venusian Plants | Venus Next | 261 | unreviewed |
| 202 | Airliners | Colonies | C01 | unreviewed |
| 203 | Air Raid | Colonies | C02 | unreviewed |
| 204 | Atmo Collectors | Colonies | C03 | unreviewed |
| 205 | Community Services | Colonies | C04 | unreviewed |
| 206 | Conscription | Colonies | C05 | unreviewed |
| 207 | Corona Extractor | Colonies | C06 | unreviewed |
| 208 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 209 | Earth Elevator | Colonies | C08 | unreviewed |
| 210 | Ecology Research | Colonies | C09 | unreviewed |
| 211 | Floater Leasing | Colonies | C10 | unreviewed |
| 212 | Floater Prototypes | Colonies | C11 | unreviewed |
| 213 | Floater Technology | Colonies | C12 | unreviewed |
| 214 | Galilean Waystation | Colonies | C13 | unreviewed |
| 215 | Heavy Taxation | Colonies | C14 | unreviewed |
| 216 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 217 | Impactor Swarm | Colonies | C16 | unreviewed |
| 218 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 219 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 220 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 221 | Luna Governor | Colonies | C20 | unreviewed |
| 222 | Lunar Exports | Colonies | C21 | unreviewed |
| 223 | Lunar Mining | Colonies | C22 | unreviewed |
| 224 | Market Manipulation | Colonies | C23 | unreviewed |
| 225 | Martian Zoo | Colonies | C24 | unreviewed |
| 226 | Mining Colony | Colonies | C25 | unreviewed |
| 227 | Minority Refuge | Colonies | C26 | unreviewed |
| 228 | Molecular Printing | Colonies | C27 | unreviewed |
| 229 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 230 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 231 | Productive Outpost | Colonies | C30 | unreviewed |
| 232 | Quantum Communications | Colonies | C31 | unreviewed |
| 233 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 234 | Refugee Camps | Colonies | C33 | unreviewed |
| 235 | Research Colony | Colonies | C34 | unreviewed |
| 236 | Rim Freighters | Colonies | C35 | unreviewed |
| 237 | Sky Docks | Colonies | C36 | unreviewed |
| 238 | Solar Probe | Colonies | C37 | unreviewed |
| 239 | Solar Reflectors | Colonies | C38 | unreviewed |
| 240 | Space Port | Colonies | C39 | unreviewed |
| 241 | Space Port Colony | Colonies | C40 | unreviewed |
| 242 | Spin-Off Department | Colonies | C41 | unreviewed |
| 243 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 244 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 245 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 246 | Titan Shuttles | Colonies | C45 | unreviewed |
| 247 | Trade Envoys | Colonies | C46 | unreviewed |
| 248 | Trading Colony | Colonies | C47 | unreviewed |
| 249 | Urban Decomposers | Colonies | C48 | unreviewed |
| 250 | Warp Drive | Colonies | C49 | unreviewed |
| 251 | House Printing | Prelude | P36 | unreviewed |
| 252 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 253 | Martian Survey | Prelude | P38 | unreviewed |
| 254 | Psychrophiles | Prelude | P39 | unreviewed |
| 255 | Research Coordination | Prelude | P40 | unreviewed |
| 256 | SF Memorial | Prelude | P41 | unreviewed |
| 257 | Space Hotels | Prelude | P42 | unreviewed |
| 258 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 259 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 260 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 261 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 262 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 263 | Floating Refinery | Venus Next | P73 | unreviewed |
| 264 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 265 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 266 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 267 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 268 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 269 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 270 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 271 | Soil Studies | Venus Next | P81 | unreviewed |
| 272 | Special Permit | Prelude 2 | P82 | unreviewed |
| 273 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 274 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 275 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 276 | Unexpected Application | Venus Next | P86 | unreviewed |
| 277 | Venus Allies | Venus Next | P87 | unreviewed |
| 278 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 279 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 280 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 281 | WG Project | Prelude 2 | P91 | unreviewed |
| 282 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 283 | Banned Delegate | Turmoil | T02 | unreviewed |
| 284 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 285 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 286 | Event Analysts | Turmoil | T05 | unreviewed |
| 287 | GMO Contract | Turmoil | T06 | unreviewed |
| 288 | Martian Media Center | Turmoil | T07 | unreviewed |
| 289 | Parliament Hall | Turmoil | T08 | unreviewed |
| 290 | PR Office | Turmoil | T09 | unreviewed |
| 291 | Public Celebrations | Turmoil | T10 | unreviewed |
| 292 | Recruitment | Turmoil | T11 | unreviewed |
| 293 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 294 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 295 | Supported Research | Turmoil | T14 | unreviewed |
| 296 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 297 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 298 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 299 | Project Inspection | Promo | X02 | unreviewed |
| 300 | Energy Market | Promo | X03 | unreviewed |
| 301 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 302 | Interplanetary Trade | Promo | X05 | unreviewed |
| 303 | Law Suit | Promo | X06 | unreviewed |
| 304 | Mercurian Alloys | Promo | X07 | unreviewed |
| 305 | Orbital Cleanup | Promo | X08 | unreviewed |
| 306 | Political Alliance | Promo | X09 | unreviewed |
| 307 | Rego Plastics | Promo | X10 | unreviewed |
| 308 | Saturn Surfing | Promo | X11 | unreviewed |
| 309 | Stanford Torus | Promo | X12 | unreviewed |
| 310 | Advertising | Promo | X13 | unreviewed |
| 311 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 312 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 313 | Comet Aiming | Promo | X16 | unreviewed |
| 314 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 315 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 316 | Directed Impactors | Promo | X19 | unreviewed |
| 317 | Diversity Support | Promo | X20 | unreviewed |
| 318 | Field-Capped City | Promo | X21 | unreviewed |
| 319 | Imported Nutrients | Promo | X22 | unreviewed |
| 320 | Jovian Embassy | Promo | X23 | unreviewed |
| 321 | Magnetic Shield | Promo | X24 | unreviewed |
| 322 | Meat Industry | Promo | X25 | unreviewed |
| 323 | Meltworks | Promo | X26 | unreviewed |
| 324 | Mohole Lake | Promo | X27 | unreviewed |
| 325 | Potatoes | Promo | X28 | unreviewed |
| 326 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 327 | Topsoil Contract | Promo | X30 | unreviewed |
| 328 | Asteroid Rights | Promo | X34 | unreviewed |
| 329 | Bactoviral Research | Promo | X35 | unreviewed |
| 330 | Bio Printing Facility | Promo | X36 | unreviewed |
| 331 | Harvest | Promo | X37 | unreviewed |
| 332 | Outdoor Sports | Promo | X38 | unreviewed |
| 333 | 16 Psyche | Promo | X44 | unreviewed |
| 334 | Robot Pollinators | Promo | X45 | unreviewed |
| 335 | Supercapacitors | Promo | X46 | unreviewed |
| 336 | Icy Impactors | Promo | X47 | unreviewed |
| 337 | Directed Heat Usage | Promo | X48 | unreviewed |
| 338 | Aqueduct Systems | Promo | X50 | unreviewed |
| 339 | Astra Mechanica | Promo | X51 | unreviewed |
| 340 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 341 | Cyberia Systems | Promo | X53 | unreviewed |
| 342 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 343 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 344 | Kaguya Tech | Promo | X58 | unreviewed |
| 345 | Mars Nomads | Promo | X59 | unreviewed |
| 346 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 347 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 348 | Red Ships | Promo | X62 | unreviewed |
| 349 | Solar Logistics | Promo | X63 | unreviewed |
| 350 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 351 | Teslaract | Promo | X66 | unreviewed |
| 352 | Soil Enrichment | Promo | X67 | unreviewed |
| 353 | Supermarkets | Promo | X68 | unreviewed |
| 354 | Hospitals | Promo | X69 | unreviewed |
| 355 | Public Baths | Promo | X70 | unreviewed |
| 356 | City Parks | Promo | X71 | unreviewed |
| 357 | Casinos | Promo | X72 | unreviewed |
| 358 | Protected Growth | Promo | X73 | unreviewed |
| 359 | Static Harvesting | Promo | X74 | unreviewed |
| 360 | Vermin | Promo | X75 | unreviewed |
| 361 | Weather Balloons | Promo | X76 | unreviewed |
| 362 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
