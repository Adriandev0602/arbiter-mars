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

<!-- TABLE_START -->
| # | Nombre | Expansión | # scan | Estado |
|---|---|---|---|---|
| 1 | Inventors' Guild | Corporate Era | 006 | unreviewed |
| 2 | Martian Rails | Base | 007 | unreviewed |
| 3 | Capital | Base | 008 | unreviewed |
| 4 | Asteroid | Base | 009 | unreviewed |
| 5 | Comet | Base | 010 | unreviewed |
| 6 | Big Asteroid | Base | 011 | unreviewed |
| 7 | Water Import from Europa | Base | 012 | unreviewed |
| 8 | Space Elevator | Corporate Era | 013 | unreviewed |
| 9 | Development Center | Corporate Era | 014 | unreviewed |
| 10 | Equatorial Magnetizer | Base | 015 | unreviewed |
| 11 | Domed Crater | Base | 016 | unreviewed |
| 12 | Noctis City | Base | 017 | unreviewed |
| 13 | Methane from Titan | Base | 018 | unreviewed |
| 14 | Imported Hydrogen | Base | 019 | unreviewed |
| 15 | Research Outpost | Base | 020 | unreviewed |
| 16 | Phobos Space Haven | Base | 021 | unreviewed |
| 17 | Black Polar Dust | Base | 022 | unreviewed |
| 18 | Arctic Algae | Base | 023 | unreviewed |
| 19 | Predators | Base | 024 | unreviewed |
| 20 | Space Station | Corporate Era | 025 | unreviewed |
| 21 | Eos Chasma National Park | Base | 026 | unreviewed |
| 22 | Interstellar Colony Ship | Corporate Era | 027 | unreviewed |
| 23 | Security Fleet | Corporate Era | 028 | unreviewed |
| 24 | Cupola City | Base | 029 | unreviewed |
| 25 | Lunar Beam | Base | 030 | unreviewed |
| 26 | Optimal Aerobraking | Base | 031 | unreviewed |
| 27 | Underground City | Base | 032 | unreviewed |
| 28 | GHG Producing Bacteria | Base | 034 | unreviewed |
| 29 | Ants | Base | 035 | unreviewed |
| 30 | Release of Inert Gases | Base | 036 | unreviewed |
| 31 | Nitrogen-Rich Asteroid | Base | 037 | unreviewed |
| 32 | Rover Construction | Base | 038 | unreviewed |
| 33 | Deimos Down | Base | 039 | unreviewed |
| 34 | Asteroid Mining | Base | 040 | unreviewed |
| 35 | Food Factory | Base | 041 | unreviewed |
| 36 | Archaebacteria | Base | 042 | unreviewed |
| 37 | Carbonate Processing | Base | 043 | unreviewed |
| 38 | Natural Preserve | Base | 044 | unreviewed |
| 39 | Lightning Harvest | Corporate Era | 046 | unreviewed |
| 40 | Algae | Base | 047 | unreviewed |
| 41 | Adapted Lichen | Base | 048 | unreviewed |
| 42 | Tardigrades | Corporate Era | 049 | unreviewed |
| 43 | Virus | Corporate Era | 050 | unreviewed |
| 44 | Miranda Resort | Corporate Era | 051 | unreviewed |
| 45 | Fish | Base | 052 | unreviewed |
| 46 | Lake Marineris | Base | 053 | unreviewed |
| 47 | Small Animals | Base | 054 | unreviewed |
| 48 | Kelp Farming | Base | 055 | unreviewed |
| 49 | Vesta Shipyard | Corporate Era | 057 | unreviewed |
| 50 | Beam from a Thorium Asteroid | Base | 058 | unreviewed |
| 51 | Mangrove | Base | 059 | unreviewed |
| 52 | Trees | Base | 060 | unreviewed |
| 53 | Great Escarpment Consortium | Corporate Era | 061 | unreviewed |
| 54 | Mineral Deposit | Corporate Era | 062 | unreviewed |
| 55 | Mining Expedition | Base | 063 | unreviewed |
| 56 | Mining Area | Corporate Era | 064 | unreviewed |
| 57 | Building Industries | Corporate Era | 065 | unreviewed |
| 58 | Land Claim | Corporate Era | 066 | unreviewed |
| 59 | Mining Rights | Base | 067 | unreviewed |
| 60 | Electro Catapult | Corporate Era | 069 | unreviewed |
| 61 | Earth Catapult | Corporate Era | 070 | unreviewed |
| 62 | Advanced Alloys | Corporate Era | 071 | unreviewed |
| 63 | Birds | Base | 072 | unreviewed |
| 64 | Mars University | Corporate Era | 073 | unreviewed |
| 65 | Viral Enhancers | Corporate Era | 074 | unreviewed |
| 66 | Towing a Comet | Base | 075 | unreviewed |
| 67 | Space Mirrors | Base | 076 | unreviewed |
| 68 | Ice Asteroid | Base | 078 | unreviewed |
| 69 | Quantum Extractor | Corporate Era | 079 | unreviewed |
| 70 | Giant Ice Asteroid | Base | 080 | unreviewed |
| 71 | Ganymede Colony | Base | 081 | unreviewed |
| 72 | Callisto Penal Mines | Corporate Era | 082 | unreviewed |
| 73 | Giant Space Mirror | Base | 083 | unreviewed |
| 74 | Trans-Neptune Probe | Corporate Era | 084 | unreviewed |
| 75 | Commercial District | Corporate Era | 085 | unreviewed |
| 76 | Robotic Workforce | Corporate Era | 086 | unreviewed |
| 77 | Grass | Base | 087 | unreviewed |
| 78 | Heather | Base | 088 | unreviewed |
| 79 | Peroxide Power | Base | 089 | unreviewed |
| 80 | Research | Corporate Era | 090 | unreviewed |
| 81 | Gene Repair | Corporate Era | 091 | unreviewed |
| 82 | IO Mining Industries | Corporate Era | 092 | unreviewed |
| 83 | Bushes | Base | 093 | unreviewed |
| 84 | Mass Converter | Corporate Era | 094 | unreviewed |
| 85 | Physics Complex | Corporate Era | 095 | unreviewed |
| 86 | Greenhouses | Base | 096 | unreviewed |
| 87 | Nuclear Zone | Base | 097 | unreviewed |
| 88 | Tropical Resort | Corporate Era | 098 | unreviewed |
| 89 | Toll Station | Corporate Era | 099 | unreviewed |
| 90 | Fueled Generators | Base | 100 | unreviewed |
| 91 | Power Grid | Base | 102 | unreviewed |
| 92 | Ore Processor | Base | 104 | unreviewed |
| 93 | Earth Office | Corporate Era | 105 | unreviewed |
| 94 | Media Archives | Corporate Era | 107 | unreviewed |
| 95 | Open City | Base | 108 | unreviewed |
| 96 | Media Group | Corporate Era | 109 | unreviewed |
| 97 | Business Network | Corporate Era | 110 | unreviewed |
| 98 | Business Contacts | Corporate Era | 111 | unreviewed |
| 99 | Bribed Committee | Corporate Era | 112 | unreviewed |
| 100 | Breathing Filters | Base | 114 | unreviewed |

| 101 | Artificial Lake | Base | 116 | unreviewed |
| 102 | Geothermal Power | Base | 117 | unreviewed |
| 103 | Dust Seals | Base | 119 | unreviewed |
| 104 | Urbanized Area | Base | 120 | unreviewed |
| 105 | Sabotage | Corporate Era | 121 | unreviewed |
| 106 | Moss | Base | 122 | unreviewed |
| 107 | Industrial Center | Corporate Era | 123 | unreviewed |
| 108 | Hired Raiders | Corporate Era | 124 | unreviewed |
| 109 | Hackers | Corporate Era | 125 | unreviewed |
| 110 | GHG Factories | Base | 126 | unreviewed |
| 111 | Subterranean Reservoir | Base | 127 | unreviewed |
| 112 | Ecological Zone | Base | 128 | unreviewed |
| 113 | Zeppelins | Base | 129 | unreviewed |
| 114 | Worms | Base | 130 | unreviewed |
| 115 | Decomposers | Base | 131 | unreviewed |
| 116 | Fusion Power | Base | 132 | unreviewed |
| 117 | Symbiotic Fungus | Base | 133 | unreviewed |
| 118 | Extreme-Cold Fungus | Base | 134 | unreviewed |
| 119 | Advanced Ecosystems | Base | 135 | unreviewed |
| 120 | Great Dam | Base | 136 | unreviewed |
| 121 | Cartel | Corporate Era | 137 | unreviewed |
| 122 | Strip Mine | Base | 138 | unreviewed |
| 123 | Wave Power | Base | 139 | unreviewed |
| 124 | Lava Flows | Base | 140 | unreviewed |
| 125 | Power Plant | Base | 141 | unreviewed |
| 126 | Mohole Area | Base | 142 | unreviewed |
| 127 | Large Convoy | Base | 143 | unreviewed |
| 128 | Tectonic Stress Power | Base | 145 | unreviewed |
| 129 | Herbivores | Base | 147 | unreviewed |
| 130 | Insects | Base | 148 | unreviewed |
| 131 | CEO's Favorite Project | Corporate Era | 149 | unreviewed |
| 132 | Anti-Gravity Technology | Corporate Era | 150 | unreviewed |
| 133 | Adaptation Technology | Base | 153 | unreviewed |
| 134 | Caretaker Contract | Corporate Era | 154 | unreviewed |
| 135 | Designed Microorganisms | Base | 155 | unreviewed |
| 136 | Standard Technology | Corporate Era | 156 | unreviewed |
| 137 | Nitrite Reducing Bacteria | Base | 157 | unreviewed |
| 138 | Industrial Microbes | Base | 158 | unreviewed |
| 139 | Lichen | Base | 159 | unreviewed |
| 140 | Power Supply Consortium | Corporate Era | 160 | unreviewed |
| 141 | Convoy from Europa | Base | 161 | unreviewed |
| 142 | Imported GHG | Base | 162 | unreviewed |
| 143 | Imported Nitrogen | Base | 163 | unreviewed |
| 144 | Micro-Mills | Base | 164 | unreviewed |
| 145 | Magnetic Field Generators | Base | 165 | unreviewed |
| 146 | Shuttles | Base | 166 | unreviewed |
| 147 | Import of Advanced GHG | Base | 167 | unreviewed |
| 148 | Windmills | Base | 168 | unreviewed |
| 149 | Tundra Farming | Base | 169 | unreviewed |
| 150 | Aerobraked Ammonia Asteroid | Base | 170 | unreviewed |
| 151 | Magnetic Field Dome | Base | 171 | unreviewed |
| 152 | Pets | Base | 172 | unreviewed |
| 153 | Protected Habitats | Corporate Era | 173 | unreviewed |
| 154 | Protected Valley | Base | 174 | unreviewed |
| 155 | Satellites | Corporate Era | 175 | unreviewed |
| 156 | Noctis Farming | Base | 176 | unreviewed |
| 157 | Water Splitting Plant | Base | 177 | unreviewed |
| 158 | Heat Trappers | Base | 178 | unreviewed |
| 159 | Soil Factory | Base | 179 | unreviewed |
| 160 | Fuel Factory | Corporate Era | 180 | unreviewed |
| 161 | Ice Cap Melting | Base | 181 | unreviewed |
| 162 | Corporate Stronghold | Corporate Era | 182 | unreviewed |
| 163 | Biomass Combustors | Base | 183 | unreviewed |
| 164 | Livestock | Base | 184 | unreviewed |
| 165 | Olympus Conference | Corporate Era | 185 | unreviewed |
| 166 | Rad-Suits | Corporate Era | 186 | unreviewed |
| 167 | Aquifer Pumping | Base | 187 | unreviewed |
| 168 | Flooding | Base | 188 | unreviewed |
| 169 | Energy Saving | Base | 189 | unreviewed |
| 170 | Local Heat Trapping | Base | 190 | unreviewed |
| 171 | Permafrost Extraction | Base | 191 | unreviewed |
| 172 | Invention Contest | Corporate Era | 192 | unreviewed |
| 173 | Plantation | Base | 193 | unreviewed |
| 174 | Power Infrastructure | Corporate Era | 194 | unreviewed |
| 175 | Indentured Workers | Corporate Era | 195 | unreviewed |
| 176 | Lagrange Observatory | Corporate Era | 196 | unreviewed |
| 177 | Terraforming Ganymede | Corporate Era | 197 | unreviewed |
| 178 | Immigration Shuttles | Base | 198 | unreviewed |
| 179 | Restricted Area | Corporate Era | 199 | unreviewed |
| 180 | Immigrant City | Base | 200 | unreviewed |
| 181 | Energy Tapping | Corporate Era | 201 | unreviewed |
| 182 | Underground Detonations | Base | 202 | unreviewed |
| 183 | Soletta | Base | 203 | unreviewed |
| 184 | Technology Demonstration | Corporate Era | 204 | unreviewed |
| 185 | Rad-Chem Factory | Base | 205 | unreviewed |
| 186 | Special Design | Base | 206 | unreviewed |
| 187 | Medical Lab | Corporate Era | 207 | unreviewed |
| 188 | AI Central | Corporate Era | 208 | unreviewed |
| 189 | Small Asteroid | Promo | 209 | unreviewed |
| 190 | Self-Replicating Robots | Promo | 210 | unreviewed |
| 191 | Snow Algae | Promo | 211 | unreviewed |
| 192 | Penguins | Promo | 212 | unreviewed |
| 193 | Aerial Mappers | Venus Next | 213 | unreviewed |
| 194 | Aerosport Tournament | Venus Next | 214 | unreviewed |
| 195 | Air-Scrapping Expedition | Venus Next | 215 | unreviewed |
| 196 | Atalanta Planitia Lab | Venus Next | 216 | unreviewed |
| 197 | Atmoscoop | Venus Next | 217 | unreviewed |
| 198 | Comet for Venus | Venus Next | 218 | unreviewed |
| 199 | Corroder Suits | Venus Next | 219 | unreviewed |
| 200 | Dawn City | Venus Next | 220 | unreviewed |
| 201 | Deuterium Export | Venus Next | 221 | unreviewed |
| 202 | Dirigibles | Venus Next | 222 | unreviewed |
| 203 | Extractor Balloons | Venus Next | 223 | unreviewed |
| 204 | Extremophiles | Venus Next | 224 | unreviewed |
| 205 | Floating Habs | Venus Next | 225 | unreviewed |
| 206 | Forced Precipitation | Venus Next | 226 | unreviewed |
| 207 | Freyja Biodomes | Venus Next | 227 | unreviewed |
| 208 | GHG Import from Venus | Venus Next | 228 | unreviewed |
| 209 | Giant Solar Shade | Venus Next | 229 | unreviewed |
| 210 | Gyropolis | Venus Next | 230 | unreviewed |
| 211 | Hydrogen to Venus | Venus Next | 231 | unreviewed |
| 212 | IO Sulphur Research | Venus Next | 232 | unreviewed |
| 213 | Ishtar Mining | Venus Next | 233 | unreviewed |
| 214 | Jet Stream Microscrappers | Venus Next | 234 | unreviewed |
| 215 | Local Shading | Venus Next | 235 | unreviewed |
| 216 | Luna Metropolis | Venus Next | 236 | unreviewed |
| 217 | Luxury Foods | Venus Next | 237 | unreviewed |
| 218 | Maxwell Base | Venus Next | 238 | unreviewed |
| 219 | Mining Quota | Venus Next | 239 | unreviewed |
| 220 | Neutralizer Factory | Venus Next | 240 | unreviewed |
| 221 | Omnicourt | Venus Next | 241 | unreviewed |
| 222 | Orbital Reflectors | Venus Next | 242 | unreviewed |
| 223 | Rotator Impacts | Venus Next | 243 | unreviewed |
| 224 | Sister Planet Support | Venus Next | 244 | unreviewed |
| 225 | Solarnet | Venus Next | 245 | unreviewed |
| 226 | Spin-Inducing Asteroid | Venus Next | 246 | unreviewed |
| 227 | Sponsored Academies | Venus Next | 247 | unreviewed |
| 228 | Stratopolis | Venus Next | 248 | unreviewed |
| 229 | Stratospheric Birds | Venus Next | 249 | unreviewed |
| 230 | Sulphur Exports | Venus Next | 250 | unreviewed |
| 231 | Sulphur-Eating Bacteria | Venus Next | 251 | unreviewed |
| 232 | Terraforming Contract | Venus Next | 252 | unreviewed |
| 233 | Thermophiles | Venus Next | 253 | unreviewed |
| 234 | Water to Venus | Venus Next | 254 | unreviewed |
| 235 | Venus Governor | Venus Next | 255 | unreviewed |
| 236 | Venus Magnetizer | Venus Next | 256 | unreviewed |
| 237 | Venus Soils | Venus Next | 257 | unreviewed |
| 238 | Venus Waystation | Venus Next | 258 | unreviewed |
| 239 | Venusian Animals | Venus Next | 259 | unreviewed |
| 240 | Venusian Insects | Venus Next | 260 | unreviewed |
| 241 | Venusian Plants | Venus Next | 261 | unreviewed |
| 242 | Airliners | Colonies | C01 | unreviewed |
| 243 | Air Raid | Colonies | C02 | unreviewed |
| 244 | Atmo Collectors | Colonies | C03 | unreviewed |
| 245 | Community Services | Colonies | C04 | unreviewed |
| 246 | Conscription | Colonies | C05 | unreviewed |
| 247 | Corona Extractor | Colonies | C06 | unreviewed |
| 248 | Cryo-Sleep | Colonies | C07 | unreviewed |
| 249 | Earth Elevator | Colonies | C08 | unreviewed |
| 250 | Ecology Research | Colonies | C09 | unreviewed |
| 251 | Floater Leasing | Colonies | C10 | unreviewed |
| 252 | Floater Prototypes | Colonies | C11 | unreviewed |
| 253 | Floater Technology | Colonies | C12 | unreviewed |
| 254 | Galilean Waystation | Colonies | C13 | unreviewed |
| 255 | Heavy Taxation | Colonies | C14 | unreviewed |
| 256 | Ice Moon Colony | Colonies | C15 | unreviewed |
| 257 | Impactor Swarm | Colonies | C16 | unreviewed |
| 258 | Interplanetary Colony Ship | Colonies | C17 | unreviewed |
| 259 | Jovian Lanterns | Colonies | C18 | unreviewed |
| 260 | Jupiter Floating Station | Colonies | C19 | unreviewed |
| 261 | Luna Governor | Colonies | C20 | unreviewed |
| 262 | Lunar Exports | Colonies | C21 | unreviewed |
| 263 | Lunar Mining | Colonies | C22 | unreviewed |
| 264 | Market Manipulation | Colonies | C23 | unreviewed |
| 265 | Martian Zoo | Colonies | C24 | unreviewed |
| 266 | Mining Colony | Colonies | C25 | unreviewed |
| 267 | Minority Refuge | Colonies | C26 | unreviewed |
| 268 | Molecular Printing | Colonies | C27 | unreviewed |
| 269 | Nitrogen from Titan | Colonies | C28 | unreviewed |
| 270 | Pioneer Settlement | Colonies | C29 | unreviewed |
| 271 | Productive Outpost | Colonies | C30 | unreviewed |
| 272 | Quantum Communications | Colonies | C31 | unreviewed |
| 273 | Red Spot Observatory | Colonies | C32 | unreviewed |
| 274 | Refugee Camps | Colonies | C33 | unreviewed |
| 275 | Research Colony | Colonies | C34 | unreviewed |
| 276 | Rim Freighters | Colonies | C35 | unreviewed |
| 277 | Sky Docks | Colonies | C36 | unreviewed |
| 278 | Solar Probe | Colonies | C37 | unreviewed |
| 279 | Solar Reflectors | Colonies | C38 | unreviewed |
| 280 | Space Port | Colonies | C39 | unreviewed |
| 281 | Space Port Colony | Colonies | C40 | unreviewed |
| 282 | Spin-Off Department | Colonies | C41 | unreviewed |
| 283 | Sub-Zero Salt Fish | Colonies | C42 | unreviewed |
| 284 | Titan Air-Scrapping | Colonies | C43 | unreviewed |
| 285 | Titan Floating Launch-Pad | Colonies | C44 | unreviewed |
| 286 | Titan Shuttles | Colonies | C45 | unreviewed |
| 287 | Trade Envoys | Colonies | C46 | unreviewed |
| 288 | Trading Colony | Colonies | C47 | unreviewed |
| 289 | Urban Decomposers | Colonies | C48 | unreviewed |
| 290 | Warp Drive | Colonies | C49 | unreviewed |
| 291 | House Printing | Prelude | P36 | unreviewed |
| 292 | Lava Tube Settlement | Prelude | P37 | unreviewed |
| 293 | Martian Survey | Prelude | P38 | unreviewed |
| 294 | Psychrophiles | Prelude | P39 | unreviewed |
| 295 | Research Coordination | Prelude | P40 | unreviewed |
| 296 | SF Memorial | Prelude | P41 | unreviewed |
| 297 | Space Hotels | Prelude | P42 | unreviewed |
| 298 | Ceres Tech Market | Venus Next | P68 | unreviewed |
| 299 | Cloud Tourism | Venus Next | P69 | unreviewed |
| 300 | Colonial Envoys | Prelude 2 | P70 | unreviewed |
| 301 | Colonial Representation | Prelude 2 | P71 | unreviewed |
| 302 | Envoys from Venus | Venus Next | P72 | unreviewed |
| 303 | Floating Refinery | Venus Next | P73 | unreviewed |
| 304 | Frontier Town | Prelude 2 | P74 | unreviewed |
| 305 | GHG Shipment | Prelude 2 | P75 | unreviewed |
| 306 | Ishtar Expedition | Venus Next | P76 | unreviewed |
| 307 | Jovian Envoys | Prelude 2 | P77 | unreviewed |
| 308 | L1 Trade Terminal | Venus Next | P78 | unreviewed |
| 309 | Microgravity Nutrition | Prelude 2 | P79 | unreviewed |
| 310 | Red Appeasement | Prelude 2 | P80 | unreviewed |
| 311 | Soil Studies | Venus Next | P81 | unreviewed |
| 312 | Special Permit | Prelude 2 | P82 | unreviewed |
| 313 | Sponsoring Nation | Prelude 2 | P83 | unreviewed |
| 314 | Stratospheric Expedition | Venus Next | P84 | unreviewed |
| 315 | Summit Logistics | Prelude 2 | P85 | unreviewed |
| 316 | Unexpected Application | Venus Next | P86 | unreviewed |
| 317 | Venus Allies | Venus Next | P87 | unreviewed |
| 318 | Venus Orbital Survey | Venus Next | P88 | unreviewed |
| 319 | Venus Shuttles | Venus Next | P89 | unreviewed |
| 320 | Venus Trade Hub | Venus Next | P90 | unreviewed |
| 321 | WG Project | Prelude 2 | P91 | unreviewed |
| 322 | Aerial Lenses | Turmoil | T01 | unreviewed |
| 323 | Banned Delegate | Turmoil | T02 | unreviewed |
| 324 | Cultural Metropolis | Turmoil | T03 | unreviewed |
| 325 | Diaspora Movement | Turmoil | T04 | unreviewed |
| 326 | Event Analysts | Turmoil | T05 | unreviewed |
| 327 | GMO Contract | Turmoil | T06 | unreviewed |
| 328 | Martian Media Center | Turmoil | T07 | unreviewed |
| 329 | Parliament Hall | Turmoil | T08 | unreviewed |
| 330 | PR Office | Turmoil | T09 | unreviewed |
| 331 | Public Celebrations | Turmoil | T10 | unreviewed |
| 332 | Recruitment | Turmoil | T11 | unreviewed |
| 333 | Red Tourism Wave | Turmoil | T12 | unreviewed |
| 334 | Sponsored Mohole | Turmoil | T13 | unreviewed |
| 335 | Supported Research | Turmoil | T14 | unreviewed |
| 336 | Wildlife Dome | Turmoil | T15 | unreviewed |
| 337 | Vote of No Confidence | Turmoil | T16 | unreviewed |
| 338 | Dusk Laser Mining | Promo | X01 | unreviewed |
| 339 | Project Inspection | Promo | X02 | unreviewed |
| 340 | Energy Market | Promo | X03 | unreviewed |
| 341 | Hi-Tech Lab | Promo | X04 | unreviewed |
| 342 | Interplanetary Trade | Promo | X05 | unreviewed |
| 343 | Law Suit | Promo | X06 | unreviewed |
| 344 | Mercurian Alloys | Promo | X07 | unreviewed |
| 345 | Orbital Cleanup | Promo | X08 | unreviewed |
| 346 | Political Alliance | Promo | X09 | unreviewed |
| 347 | Rego Plastics | Promo | X10 | unreviewed |
| 348 | Saturn Surfing | Promo | X11 | unreviewed |
| 349 | Stanford Torus | Promo | X12 | unreviewed |
| 350 | Advertising | Promo | X13 | unreviewed |
| 351 | Asteroid Deflection System | Promo | X14 | unreviewed |
| 352 | Asteroid Hollowing | Promo | X15 | unreviewed |
| 353 | Comet Aiming | Promo | X16 | unreviewed |
| 354 | Crash Site Cleanup | Promo | X17 | unreviewed |
| 355 | Cutting Edge Technology | Promo | X18 | unreviewed |
| 356 | Directed Impactors | Promo | X19 | unreviewed |
| 357 | Diversity Support | Promo | X20 | unreviewed |
| 358 | Field-Capped City | Promo | X21 | unreviewed |
| 359 | Imported Nutrients | Promo | X22 | unreviewed |
| 360 | Jovian Embassy | Promo | X23 | unreviewed |
| 361 | Magnetic Shield | Promo | X24 | unreviewed |
| 362 | Meat Industry | Promo | X25 | unreviewed |
| 363 | Meltworks | Promo | X26 | unreviewed |
| 364 | Mohole Lake | Promo | X27 | unreviewed |
| 365 | Potatoes | Promo | X28 | unreviewed |
| 366 | Sub-Crust Measurements | Promo | X29 | unreviewed |
| 367 | Topsoil Contract | Promo | X30 | unreviewed |
| 368 | Asteroid Rights | Promo | X34 | unreviewed |
| 369 | Bactoviral Research | Promo | X35 | unreviewed |
| 370 | Bio Printing Facility | Promo | X36 | unreviewed |
| 371 | Harvest | Promo | X37 | unreviewed |
| 372 | Outdoor Sports | Promo | X38 | unreviewed |
| 373 | 16 Psyche | Promo | X44 | unreviewed |
| 374 | Robot Pollinators | Promo | X45 | unreviewed |
| 375 | Supercapacitors | Promo | X46 | unreviewed |
| 376 | Icy Impactors | Promo | X47 | unreviewed |
| 377 | Directed Heat Usage | Promo | X48 | unreviewed |
| 378 | Aqueduct Systems | Promo | X50 | unreviewed |
| 379 | Astra Mechanica | Promo | X51 | unreviewed |
| 380 | Carbon Nanosystems | Promo | X52 | unreviewed |
| 381 | Cyberia Systems | Promo | X53 | unreviewed |
| 382 | Hermetic Order of Mars | Promo | X56 | unreviewed |
| 383 | Homeostasis Bureau | Promo | X57 | unreviewed |
| 384 | Kaguya Tech | Promo | X58 | unreviewed |
| 385 | Mars Nomads | Promo | X59 | unreviewed |
| 386 | Martian Lumber Corp | Promo | X60 | unreviewed |
| 387 | Neptunian Power Consultants | Promo | X61 | unreviewed |
| 388 | Red Ships | Promo | X62 | unreviewed |
| 389 | Solar Logistics | Promo | X63 | unreviewed |
| 390 | St. Joseph of Cupertino Mission | Promo | X64 | unreviewed |
| 391 | Teslaract | Promo | X66 | unreviewed |
| 392 | Soil Enrichment | Promo | X67 | unreviewed |
| 393 | Supermarkets | Promo | X68 | unreviewed |
| 394 | Hospitals | Promo | X69 | unreviewed |
| 395 | Public Baths | Promo | X70 | unreviewed |
| 396 | City Parks | Promo | X71 | unreviewed |
| 397 | Casinos | Promo | X72 | unreviewed |
| 398 | Protected Growth | Promo | X73 | unreviewed |
| 399 | Static Harvesting | Promo | X74 | unreviewed |
| 400 | Vermin | Promo | X75 | unreviewed |
| 401 | Weather Balloons | Promo | X76 | unreviewed |
| 402 | Sterling Vents | Promo | X79 | unreviewed |
<!-- TABLE_END -->
