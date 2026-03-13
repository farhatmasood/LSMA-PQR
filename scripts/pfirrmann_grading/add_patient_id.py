"""
Add Patient_ID column to PfirrmannGrade.csv from a clinical notes file.

The original .mat export lacks patient identifiers.  This script extracts
Patient_IDs from a clinical notes CSV and inserts them as the first column.

Usage:
    python add_patient_id.py --notes <notes.csv> --pfirrmann <PfirrmannGrade.csv>
"""

import argparse

import pandas as pd


def add_ids(notes_path: str, pfirrmann_path: str) -> None:
    patient_ids = []
    with open(notes_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.split(",", 1)
            if parts:
                patient_ids.append(int(parts[0].strip()))

    print(f"Extracted {len(patient_ids)} Patient_IDs from {notes_path}")

    df = pd.read_csv(pfirrmann_path)
    df.insert(0, "Patient_ID", patient_ids)
    df.to_csv(pfirrmann_path, index=False)

    print(f"Updated: {pfirrmann_path}")
    print(f"Shape  : {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add Patient_ID to Pfirrmann CSV.")
    parser.add_argument("--notes", type=str, required=True,
                        help="Path to clinical notes CSV (first column = Patient_ID).")
    parser.add_argument("--pfirrmann", type=str, required=True,
                        help="Path to PfirrmannGrade.csv to update in-place.")
    args = parser.parse_args()
    add_ids(args.notes, args.pfirrmann)
