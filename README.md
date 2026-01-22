# ASNIE — Data Availability and Paths
This file documents the locations, temporal coverage, and known caveats for datasets used in the ASNIE project. All paths refer to JASMIN / SWIFT unless stated otherwise.

## CRR (Convective Rain Rate)

### Object Store (Near-Real-Time)
- Path: `s3://nwcsaf/CRR/`
- Coverage: 2024-01-05 to present
- Notes: Pan-African coverage; primary near-real-time CRR archive; overlaps with SWIFT-stored CRR data.

### SWIFT GWS — Leeds CRR Archive
- Path: `/gws/ssde/j25b/swift/WISER-EWSA/Leeds_CRR/data`
- Coverage: 2023-12-12 to 2024-08-05
- Notes: Overlaps with object-store CRR; useful for redundancy and consistency checks.

### SWIFT GWS — NWCSAF Historical CRR Archive
- Path: `/gws/ssde/j25b/swift/earajr/NWCSAF_archive/netcdf_2018/CRR`
- Coverage: 2019-09-18 to 2022-05-24
- Notes: Stored on multiple regional domains rather than a single pan-African grid; domains evolved from country-scale to larger regional domains; CRR is pixel-wise so scientific consistency is preserved, but handling is more awkward due to domain splitting.

## RoA (Rainfall over Africa)

### SWIFT GWS — CEH RoA Archive
- Path: `/gws/ssde/j25b/swift/RoA`
- Coverage: Approximately 2020 to 2024
- Notes: Produced by CEH; overlaps with RoA data on the object store; variable-name inconsistency across files (`latitude` / `longitude` versus `lat` / `lon`); otherwise scientifically equivalent; regridded onto a regular latitude–longitude grid (0.027°).

## Lightning Data
- Confirmed overlap period for CRR, RoA, and lightning: 2024-07-15 to present.
- DWD-TS Lightning: downloaded for August 2024 to present; currently being copied to JASMIN following GWS path changes; expected to reside under `/gws/ssde/j25b/swift/` (final path to be confirmed).

## MTG LI (Lightning Imager)
- Status: full pan-African 15-minute accumulated dataset not yet produced; partial datasets exist for comparison studies; full processing planned.

## Recommended Analysis Periods
- Multi-dataset comparison: 2024-07-15 to present.
- Long-term CRR analysis: 2019-09-18 to present.
