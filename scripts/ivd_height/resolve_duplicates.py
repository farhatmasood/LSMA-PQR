"""
Resolve duplicate Patient_ID entries in IVDHeights.csv.

Patients with multiple sagittal slices produce more than one .mat file.
This script groups by Patient_ID, averages the disc heights, retains the
first coordinate set, and writes the deduplicated result.

Usage:
    python resolve_duplicates.py --input IVDHeights.csv --output IVDHeights_Cleaned.csv
"""

import argparse

import pandas as pd


def resolve(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv)

    df_clean = df.groupby("Patient_ID").agg({
        "D5_Ht": "mean",
        "D4_Ht": "mean",
        "D3_Ht": "mean",
        "D5_Coord": "first",
        "D4_Coord": "first",
        "D3_Coord": "first",
    }).reset_index()

    df_clean.to_csv(output_csv, index=False)

    print("=" * 80)
    print("DUPLICATE RESOLUTION REPORT")
    print("=" * 80)
    print(f"\nOriginal : {len(df)} records, {df['Patient_ID'].nunique()} unique")
    print(f"Cleaned  : {len(df_clean)} records, {df_clean['Patient_ID'].nunique()} unique")

    dups = df[df.duplicated(subset=["Patient_ID"], keep=False)].sort_values("Patient_ID")
    dup_ids = sorted(dups["Patient_ID"].unique())
    print(f"\nPatients with multiple measurements ({len(dup_ids)}):")
    for pid in dup_ids:
        rows = df[df["Patient_ID"] == pid]
        avg = df_clean[df_clean["Patient_ID"] == pid].iloc[0]
        print(f"  Patient {pid}: {len(rows)} entries")
        for _, r in rows.iterrows():
            print(f"    D5={r['D5_Ht']:.2f}  D4={r['D4_Ht']:.2f}  D3={r['D3_Ht']:.2f}")
        print(f"    Averaged -> D5={avg['D5_Ht']:.2f}  D4={avg['D4_Ht']:.2f}  "
              f"D3={avg['D3_Ht']:.2f}")

    print(f"\nSaved: {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolve duplicate IVD height entries.")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="IVDHeights_Cleaned.csv")
    args = parser.parse_args()
    resolve(args.input, args.output)
