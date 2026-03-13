"""
Final validation of IVDHeights_Corrected.csv (515 patients).

Performs integrity checks on the fully merged CSV that combines automated
.mat-based extraction (505 patients) with manual JSON measurements (10
patients).

Usage:
    python validate_corrected.py --csv IVDHeights_Corrected.csv
"""

import argparse

import pandas as pd


# Patients recovered from manual JSON measurements
JSON_PATIENTS = [192, 245, 272, 290, 368, 428, 468, 472, 525, 568]


def validate(csv_path: str) -> None:
    df = pd.read_csv(csv_path)

    print("=" * 80)
    print("FINAL VALIDATION - IVDHeights_Corrected.csv")
    print("=" * 80)
    print(f"\nDimensions : {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns    : {list(df.columns)}")
    print(f"Duplicates : {df['Patient_ID'].duplicated().sum()} (expected 0)")
    print(f"Unique IDs : {df['Patient_ID'].nunique()} (expected 515)")
    print(f"ID range   : {df['Patient_ID'].min()} -- {df['Patient_ID'].max()}")
    print(f"Missing    : {df.isnull().sum().sum()} (expected 0)")

    print("\nHeight Statistics (mm):")
    for col in ["D5_Ht", "D4_Ht", "D3_Ht"]:
        s = df[col]
        print(f"  {col}: min={s.min():.2f}  max={s.max():.2f}  "
              f"mean={s.mean():.2f}  std={s.std():.2f}")

    print("\nCoordinate Format:")
    for col in ["D5_Coord", "D4_Coord", "D3_Coord"]:
        valid = sum(1 for v in df[col] if isinstance(v, str) and ";" in v)
        print(f"  {col}: {valid}/{len(df)} valid")

    print(f"\nManually Recovered Patients ({len(JSON_PATIENTS)}):")
    for pid in JSON_PATIENTS:
        row = df[df["Patient_ID"] == pid]
        if row.empty:
            print(f"  Patient {pid}: MISSING")
        else:
            r = row.iloc[0]
            print(f"  Patient {pid}: D5={r['D5_Ht']:.2f}  "
                  f"D4={r['D4_Ht']:.2f}  D3={r['D3_Ht']:.2f} mm")

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate corrected IVD heights CSV.")
    parser.add_argument("--csv", type=str, required=True)
    args = parser.parse_args()
    validate(args.csv)
