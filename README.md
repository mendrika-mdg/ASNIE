# ASNIE — Data Availability and Paths

This file documents the locations, temporal coverage, and known caveats for datasets used in the ASNIE project. All paths refer to JASMIN / SWIFT unless stated otherwise.

---

## CRR (Convective Rain Rate)

### Object Store (Near-Real-Time)
- Path: `s3://nwcsaf/CRR/`
- Coverage: 2024-01-05 to present
- Notes: Pan-African coverage; primary near-real-time CRR archive; overlaps with SWIFT-stored CRR data.

### SWIFT GWS — Leeds CRR Archive
- Path: `/gws/ssde/j25b/swift/WISER-EWSA/Leeds_CRR/data`
- Coverage: 2023-12-12 to 2024-08-05
- Notes: Operational mirror of CRR; useful for redundancy and consistency checks.

---

## RoA (Rainfall over Africa)

### SWIFT GWS — CEH RoA Archive
- Path: `/gws/ssde/j25b/swift/RoA`
- Coverage: 2020 to 2024
- Notes: Produced by CEH; regridded onto a regular latitude–longitude grid (~0.027°); minor variable-name inconsistencies (`latitude`/`longitude` vs `lat`/`lon`).

### Object Store (Near-Real-Time)
- Path: `s3://rain-over-africa/`
- Coverage: 2024 to present
- Notes: Near-real-time continuation of RoA; overlaps with SWIFT archive.

---

## DWD-TS (Thunderstorm Product)

### SWIFT GWS — Leeds WISER-EWSA Archive
- Path: `/gws/ssde/j25b/swift/WISER-EWSA/DWD_AI_TS/data`
- Coverage: 2023-10-08 to present
- Notes: Pan-African thunderstorm detections; used as an independent detection benchmark.

---

## RDT (Rapidly Developing Thunderstorms)

### SWIFT GWS — NWCSAF Historical Archive
- Path: `/gws/ssde/j25b/swift/earajr/NWCSAF_archive/netcdf_2018/RDT`
- Coverage: 2018 to 2022
- Notes: Historical archive stored by year.

### SWIFT GWS — Leeds RDT Archive
- Path: `/gws/ssde/j25b/swift/WISER-EWSA/Leeds_RDT/data`
- Coverage: November 2023 to July 2024
- Notes: More recent operational subset.

---

## Convective Cores (Wavelet-based)

### Core Climatology Archive
- Path: `/gws/nopw/j04/cocoon/SSA_domain/ch9_wavelet`
- Coverage: 2004 to 2024
- Notes: Full historical MSG-based convective core dataset used for core detection and training.

### Near-Real-Time Cores
- Path: `/gws/ssde/j25b/swift/rt_cores`
- Coverage: 2024 to present
- Notes: Real-time extension of the core detection pipeline.

---

## MTG Lightning (Lightning Imager)

### SWIFT GWS — Pan-Africa Archive
- Path: `/gws/ssde/j25b/swift/MTG_LI_pan_Africa`
- Coverage: 2025-04-01 to 2025-11-17
- Notes: 15-minute accumulated flashes; early mission data for comparison and evaluation.

---

## Recommended Analysis Periods

- Multi-dataset comparison (CRR + RoA + DWD-TS + cores): 2024 to present
- Including MTG Lightning: 2025-04-01 onward
- Long-term core climatology studies: 2004 to present
- Historical CRR/RDT comparison: 2019 to 2022
