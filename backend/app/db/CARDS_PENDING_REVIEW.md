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

<!-- TABLE_END -->
