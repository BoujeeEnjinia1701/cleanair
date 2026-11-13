---
doc_id: CAR-REG-001
title: CleanAir Retrofit Kit regulatory and standards register
project: CleanAir Retrofit Kit
doc_type: Regulatory register
version: "0.1"
status: Draft
date: 2026-11-12
author: Amish Chadha
license: CC-BY-4.0
revisions:
  - version: "0.1"
    date: 2026-11-12
    author: Amish Chadha
    change: First register for the air profile (STANDARDS 25.5a and 25.6a)
---

# CleanAir Retrofit Kit regulatory and standards register

The kit has no electrical part and makes no medical claim; the standards that matter are the host fan's safety listing, the media ratings it is bought to, the ozone rules it stays clear of, and the CADR method it will be measured by. Benchmarks are targets, never passes, until an accredited laboratory has tested the product. Whether any jurisdiction treats a filtration kit for clinics as a regulated product is to assess with a regulatory consultant. Sources checked 2026-11-12.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | UL 507, Electric Fans ([ANSI webstore](https://webstore.ansi.org/standards/ul/ul507ed1020172026)) | US, Canada | Safety of electric fans | Applies to the host fan. Whether a listing covers a fan run flat with filters strapped to it is to assess (C3) | Safety lead | To assess |
| R2 | IEC 60335-2-80:2024, Household appliances, particular requirements for fans ([EVS](https://evs.ee/en/iec-60335-2-80-2024)) | International, EU (EN IEC 60335-2-80) | Safety of fans | As R1, outside North America | Safety lead | To assess |
| R3 | IEC 60335-1 stability (10 deg incline test) | International | General appliance safety | Used as the stability benchmark for the cube with its fan (PR-012); clause to confirm against the current edition | Mechanical lead | Benchmark, met on paper |
| R4 | UL 2998, zero ozone emissions validation ([UL](https://ul.com/services/zero-ozone-emissions-validation)) | Voluntary | Ozone under 0.005 ppm | Benchmark; the kit has no ozone source (PR-009) | Safety lead | Met by design (no active stage) |
| R5 | CARB indoor air cleaning device regulation, 0.050 ppm ozone by the UL 867 method ([UL](https://ul.com/services/zero-ozone-emissions-validation)) | California | Ozone from air cleaners | Would apply to any active stage; none fitted | Regulatory consultant | Does not apply while no active stage |
| R6 | AHAM AC-1, CADR for portable air cleaners ([AHAM FAQ](https://ahamverifide.org/wp-content/uploads/2020/06/Air-Cleaner-Performance-FAQs.pdf)) | Voluntary, US | Smoke 0.09 to 1 um, dust 0.5 to 3 um, pollen 0.5 to 11 um, in a 28.4 m3 chamber; reportable CADR up to 450 cfm | Benchmark method for V2; the cube's CADR is cited as a target, not a pass | Test lead | Benchmark |
| R7 | ASHRAE 52.2, MERV ratings ([NAFA guide](https://www.nafahq.org/assets/pdf/522BrochureJanuary2026)) | International practice | Size-resolved efficiency E1, E2, E3; MERV-13: at least 50, 85, 90 % | The panels are bought with this rating (PR-005) | Purchasing | Met by design (bought rating) |
| R8 | ISO 16890 ([NAFA guide](https://www.nafahq.org/assets/pdf/ISO+16890+January+2026)) | International, EU | ePM1, ePM2.5, ePM10 classes | MERV-13 roughly corresponds to the ePM1 group; no direct conversion; buy by MERV or ePM1 rating where supplied | Purchasing | Benchmark |
| R9 | EN 1822 and ISO 29463, HEPA and EPA classes ([MANN+HUMMEL](https://airfiltration.mann-hummel.com/air-knowledge/filtration-standards/en1822)) | International, EU | E10 85 % to H14 99.995 % at the most penetrating particle size | Not used: HEPA-grade media (for example H13 class) is not offered until its airflow on a box fan is assessed | Design lead | Does not apply now |
| R10 | UL 900, air filter units (fire behaviour) | US | Flammability of filters | Ask the panel supplier for a classification (C2) | Purchasing | To assess |
| R11 | IEC 62471, photobiological safety; ACGIH TLV for UV ([Alaska DOL](https://dol.alaska.gov/lss/pads/uv.htm)) | International | Eye and skin exposure to UV | Would apply to any UV-C module; module removed (F2) | Safety lead | Does not apply while no UV-C |
| R12 | US FDA and EU MDR device rules | US, EU | Medical devices | Not intended to apply: no medical claim (CAR-CLM-001); classification to assess with a regulatory consultant before any clinical deployment | Regulatory consultant | To assess |
| R13 | CDC "Aim for 5" and Lancet Commission NADR | Guidance | Clean-air targets | Design targets for PR-002 and PR-003 | Design lead | Benchmark |
| R14 | Local electrical, fire and building rules at each site | Site | Cords, fire load, egress | Site placement rules in the label and the build plan | Field partner | To assess per site |

Licence: this document is licensed under CC-BY-4.0 (Creative Commons Attribution 4.0 International), following the Helpful Engineering licensing guide. Design Molecule Labs with Helpful Engineering.
