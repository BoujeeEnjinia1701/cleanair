---
doc_id: CAR-MKT-001
title: CleanAir Retrofit Kit market and viability
project: CleanAir Retrofit Kit
doc_type: Market
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First market and viability note with cited benchmarks (checked 2026-11-12) and cost per unit of clean air and per year
---

# CleanAir Retrofit Kit market and viability

The filter cube kit delivers clean air at about USD 0.24 to 0.28 of kit cost per m3/h of CADR, less than half the first cost per unit of clean air of either benchmark below, at the price of more power, more noise and four consumable panels. Its niche is humanitarian and low-resource settings that already have box fans. Prices are cited with the date checked; none is a quote.

Table 1. Market segments and benchmarks.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Field hospitals and clinics | Humanitarian operators, worldwide | Coway Airmega AP-1512HH, USD 239.99, AHAM CADR 233 cfm smoke (396 m3/h), 77 W, sold with a HEPA-rated filter ([Coway](https://cowaymega.com/products/coway-mighty-ap-1512hh), checked 2026-11-12) | 111.83 kit; 135.32 with a new box fan | About the same CADR per unit for half the price, flat packed, standard consumables |
| Shelters and communal spaces | Shelter managers | CleanAirKits Luggable XL-7 DIY kit about USD 229 plus filters USD 45.94; AHAM CADR 259 cfm smoke (440 m3/h), 10.5 W ([HouseFresh review](https://housefresh.com/cleanairkits-l), checked 2026-11-12) | 111.83 | Lower first cost; the benchmark is far quieter and more efficient per watt |
| Schools and offices with box fans | Facility managers | Self-built Corsi-Rosenthal box: four panels USD 54.00 ([Global Industrial](https://www.globalindustrial.com/p/20-w-x-20-h-x-2-d-pleated-merv-13-leed-compliant-air-filter-global-industrial)) and a box fan USD 23.49 ([Target](https://www.target.com/p/lasko-3733-box-fan-white/-/A-84195090)), plus tape, checked 2026-11-12 | 111.83 | Reusable tray, deck and straps; tool-free panel change; a sealed, documented build |

Table 2. Cost per unit of clean air and per year (CAR-CAL-001; panel change every 6 months at 24 h use is an assumption, A7).

| Item | CA2 kit | Coway AP-1512HH | CleanAirKits Luggable XL-7 |
| --- | --- | --- | --- |
| First cost (USD) | 111.83 (fan excluded) | 239.99 | About 275 with filters |
| CADR (m3/h) | 398 to 459 measured (not AHAM-rated) | 396 (smoke) | 440 (smoke) |
| First cost per m3/h of CADR (USD) | 0.24 to 0.28 | 0.61 | About 0.63 |
| Power (W) | 52.8 to 103 (the fan) | 77 | 10.5 |
| Energy at 24 h a day (kWh a year) | 587 to 858 | about 675 | about 92 |
| Consumables a year (USD) | About 108 (two sets of four panels) | Filter price not listed on the page | About 92 (two sets, if changed twice) |

The kit's weakness is energy: a box fan uses about 5 to 10 times the power of the benchmark kit for the same CADR. Where electricity is scarce or costly the low-power benchmark may cost less over its life; the comparison at a site's tariff is for the field partner.

## Open route

Open hardware under CERN-OHL-P-2.0: anyone may make and sell the tray and deck. Who would build it: sign and packaging shops (corrugated PP cutting is their daily work), makerspaces for the feet, and relief logistics teams assembling kits with locally bought panels. How it spreads: Helpful Engineering's network and field partners (UNHCR and MSF are named in the team deck as partners to explore), with a printable cutting template and the build plan. A cheaper path to the stretch target of under USD 80 is panels by the case and both sheet parts nested on one 1,220 x 2,440 mm sheet (CAR-DEC-001).

## Sources

All checked 2026-11-12: Coway Airmega AP-1512HH product page; HouseFresh review of the CleanAirKits Luggable XL-7; Global Industrial 20 x 20 x 2 in MERV 13 filter; Target Lasko 3733 listing; mybinding.com corrugated plastic 10-pack; Home Depot Husky 1 in x 8 ft strap; Walmart Frost King V27 weatherstrip; MatterHackers PP filament (links in `bom/bom.csv`).

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
