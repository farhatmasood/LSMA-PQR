# IVD Height Extraction Pipeline

This directory contains the complete data engineering pipeline used to extract, validate and finalise intervertebral disc (IVD) height measurements for the LSMA-PQR dataset.

## Pipeline Overview

```
                 .mat files (MATLAB IVD height tool output)
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
   inspect_mat_structure   │              │
   (diagnostic, single     │              │
    file exploration)      │              │
                           ▼              │
               convert_mat_to_csv.py      │
               (batch extraction)         │
               → IVDHeights.csv           │
                     │                    │
                     ▼                    │
               verify_csv.py              │
               (integrity checks)         │
               Found: 9 duplicates,       │
                      505 unique IDs      │
                     │                    │
                     ▼                    │
             resolve_duplicates.py        │
             (average multi-slice)        │
             → IVDHeights_Cleaned.csv     │
               (505 patients)             │
                     │                    │
                     ▼                    ▼
           merge_manual_measurements.py ← manual_measurements.json
           (recover 10 missing patients)    (10 manually measured)
           → IVDHeights_Corrected.csv
             (515 patients, FINAL)
                     │
                     ▼
            validate_corrected.py
            (final integrity check)
                     │
                     ▼
           visualize_ivd_heights.py
           (visual verification on MRI)
```

## Scripts

| Script | Purpose |
|--------|---------|
| `inspect_mat_structure.py` | Inspect internal structure of a single `.mat` file |
| `convert_mat_to_csv.py` | Batch-extract heights and coordinates from all `.mat` files |
| `verify_csv.py` | Verify CSV integrity (missing values, duplicates, range checks) |
| `resolve_duplicates.py` | Average heights for patients with multiple sagittal slices |
| `merge_manual_measurements.py` | Recover 10 missing patients from manual JSON measurements |
| `validate_corrected.py` | Final validation of the 515-patient corrected CSV |
| `visualize_ivd_heights.py` | Overlay measurement lines on sagittal MRI images |

## Data Format

Each `.mat` file contains three MATLAB variables:

| Variable | Shape | Description |
|----------|-------|-------------|
| `ivdHeights` | (3,) | Disc heights in mm: [D5, D4, D3] |
| `topPoints` | (3, 2) | Superior end-plate midpoints (x, y) in pixels |
| `bottomPoints` | (3, 2) | Inferior end-plate midpoints (x, y) in pixels |

The output CSV (`IVDHeights_Corrected.csv`) encodes coordinates as `top_x,top_y;bottom_x,bottom_y` strings in pixel space (384 x 384 image, pixel spacing = 0.6875 mm/pixel).

## Patients Recovered from Manual Measurements

Ten patients lacked `.mat` files and were measured manually by a radiologist:

> Patient IDs: 192, 245, 272, 290, 368, 428, 468, 472, 525, 568

## Usage

All scripts accept `--help` for argument documentation. Typical execution order:

```bash
python inspect_mat_structure.py --mat_file <sample.mat>
python convert_mat_to_csv.py --mat_dir <mat_directory> --output IVDHeights.csv
python verify_csv.py --csv IVDHeights.csv
python resolve_duplicates.py --input IVDHeights.csv --output IVDHeights_Cleaned.csv
python merge_manual_measurements.py --csv IVDHeights_Cleaned.csv --json manual_measurements.json --output IVDHeights_Corrected.csv
python validate_corrected.py --csv IVDHeights_Corrected.csv
```
