# Pfirrmann Grading Pipeline

This directory contains the scripts used during the creation and validation of Pfirrmann degeneration grades for the LSMA-PQR dataset.

## Pipeline Overview

```
      PfirrmannGrade.mat (MATLAB)
              │
              ▼
      convert_mat_to_csv.py
      → PfirrmannGrade.csv (grades only, no IDs)
              │
              ▼
      add_patient_id.py
      → PfirrmannGrade.csv (with Patient_ID column)
              │
              ▼
      pfirrmann_validator.py  ←── Interactive Tkinter GUI
      (radiologist review)
      → pfirrmann_edits.json (overrides + validation flags)
      → PfirrmannGrade_Updated.csv (validated)
      → validation_summary.txt
              │
              ▼
      analyze_grades.py
      → Statistical analysis output
```

## Scripts

| Script | Purpose |
|--------|---------|
| `convert_mat_to_csv.py` | Convert MATLAB `.mat` grade matrix to CSV |
| `add_patient_id.py` | Inject Patient_ID column from clinical notes |
| `pfirrmann_validator.py` | Interactive GUI for radiologist-driven grade validation |
| `analyze_grades.py` | Comprehensive statistical analysis of grade distributions |

## Pfirrmann Grading Scale

| Grade | T2-Weighted MRI Characteristics |
|:-----:|------|
| 1 | Homogeneous bright white; normal height; clear nucleus/annulus boundary |
| 2 | Inhomogeneous with horizontal bands; normal height; visible distinction |
| 3 | Inhomogeneous gray; normal to slightly decreased height; unclear boundary |
| 4 | Inhomogeneous dark gray; moderate height loss (30--40%); no distinction |
| 5 | Inhomogeneous black; collapsed disc space (>40% loss); no signal |

## Validation GUI

The `pfirrmann_validator.py` application provides:

- Side-by-side T1 and T2 sagittal MRI display (700 x 700 canvas)
- Colour-coded IVD height measurement overlays:
  - **Red** = D5 (L5-S1)
  - **Green** = D4 (L4-L5)
  - **Cyan** = D3 (L3-L4)
- Original grade display with override dropdowns (1--5)
- Per-disc validation checkboxes
- Patient navigation (Previous / Next)
- Export to `PfirrmannGrade_Updated.csv` with original, overridden and validation-flag columns

### Validation Statistics

- Total patients reviewed: 515
- Patients with grade edits: 324 (62.9%)
- D5 edited: 201; D4 edited: 222; D3 edited: 172

## CSV Format

**Input** (`PfirrmannGrade.csv`):

| Column | Description |
|--------|-------------|
| `Patient_ID` | Integer patient identifier |
| `D5` | Pfirrmann grade for L5-S1 (1--5) |
| `D4` | Pfirrmann grade for L4-L5 (1--5) |
| `D3` | Pfirrmann grade for L3-L4 (1--5) |

**Output** (`PfirrmannGrade_Updated.csv`) adds:

| Column | Description |
|--------|-------------|
| `D5_Original` | Pre-validation grade |
| `D5_Validated` | Boolean: radiologist confirmed |
| `D5_Edited` | Boolean: grade was overridden |
| *(same for D4, D3)* | |

## Usage

```bash
# Convert from MATLAB
python convert_mat_to_csv.py --mat_file PfirrmannGrade.mat --output PfirrmannGrade.csv

# Add patient IDs
python add_patient_id.py --notes notes.csv --pfirrmann PfirrmannGrade.csv

# Launch validation GUI
python pfirrmann_validator.py

# Analyse validated grades
python analyze_grades.py --csv PfirrmannGrade_Updated.csv
```
