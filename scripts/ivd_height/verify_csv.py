"""
Verify the integrity and clinical plausibility of IVDHeights.csv.

Checks performed:
    1. Record count and unique Patient_ID count
    2. Missing-value detection
    3. Duplicate Patient_ID identification
    4. Descriptive statistics per disc level (mm)
    5. Coordinate format validation ("top_x,top_y;bottom_x,bottom_y")
    6. Height range plausibility (0.2 mm -- 20 mm)

Usage:
    python verify_csv.py --csv <IVDHeights.csv> [--expected_patients 515]
"""

import argparse

import pandas as pd


def verify(csv_path: str, expected: int) -> None:
    df = pd.read_csv(csv_path)

    print("=" * 80)
    print("IVD HEIGHTS CSV VERIFICATION REPORT")
    print("=" * 80)
    print(f"File   : {csv_path}")
    print(f"Records: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # ------- Missing values -------
    missing = df.isnull().sum()
    print(f"\nMissing values:\n{missing}")

    # ------- Patient ID analysis -------
    n_unique = df["Patient_ID"].nunique()
    print(f"\nUnique Patient_IDs: {n_unique} (expected {expected})")

    dups = df[df.duplicated(subset=["Patient_ID"], keep=False)].sort_values("Patient_ID")
    if len(dups):
        dup_ids = sorted(dups["Patient_ID"].unique())
        print(f"Duplicate IDs ({len(dup_ids)}): {dup_ids}")
        for pid in dup_ids:
            rows = df[df["Patient_ID"] == pid]
            print(f"  Patient {pid}: {len(rows)} entries  "
                  f"D5={rows['D5_Ht'].values}  D4={rows['D4_Ht'].values}  "
                  f"D3={rows['D3_Ht'].values}")
    else:
        print("No duplicate Patient_IDs.")

    # ------- Height statistics -------
    print("\nHeight Statistics (mm):")
    for col in ["D5_Ht", "D4_Ht", "D3_Ht"]:
        d = df[col]
        print(f"  {col}: min={d.min():.2f}  max={d.max():.2f}  "
              f"mean={d.mean():.2f}  median={d.median():.2f}  std={d.std():.2f}")

    # ------- Coordinate format -------
    coord_ok = all(
        df[c].dropna().str.contains(";").all()
        for c in ["D5_Coord", "D4_Coord", "D3_Coord"]
    )
    print(f"\nCoordinate format valid: {'YES' if coord_ok else 'NO'}")

    # ------- Final checklist -------
    height_cols = ["D5_Ht", "D4_Ht", "D3_Ht"]
    checks = [
        ("Record count >= expected", len(df) >= expected),
        ("Unique IDs == expected", n_unique == expected),
        ("No missing values", missing.sum() == 0),
        ("Heights positive", all((df[c] > 0).all() for c in height_cols)),
        ("Heights in [0.2, 20] mm",
         all(((df[c] > 0.2) & (df[c] < 20)).all() for c in height_cols)),
        ("Coordinate format valid", coord_ok),
    ]
    print("\nFinal Checklist:")
    all_pass = True
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}: {name}")
        if not ok:
            all_pass = False

    status = "ALL CHECKS PASSED" if all_pass else "ISSUES DETECTED"
    print(f"\n{status}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify IVDHeights CSV.")
    parser.add_argument("--csv", type=str, required=True)
    parser.add_argument("--expected_patients", type=int, default=515)
    args = parser.parse_args()
    verify(args.csv, args.expected_patients)
