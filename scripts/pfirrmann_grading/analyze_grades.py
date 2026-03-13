"""
Comprehensive statistical analysis of validated Pfirrmann grades.

Reads PfirrmannGrade_Updated.csv (output of the validation GUI) and outputs:
    1. Grade distribution by disc level (counts, percentages)
    2. Descriptive statistics (mean, median, mode, std, IQR)
    3. Multi-disc degeneration patterns (uniform, ascending, descending)
    4. Pearson correlation between disc levels
    5. Severity categorisation (max/min grade, severe disc count)
    6. Class imbalance metrics (imbalance ratio, Gini coefficient)
    7. Clinical interpretation summary

Usage:
    python analyze_grades.py --csv <PfirrmannGrade_Updated.csv>
"""

import argparse

import numpy as np
import pandas as pd
from scipy import stats


def analyze(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    N = len(df)
    level_map = {"D5": "L5-S1", "D4": "L4-L5", "D3": "L3-L4"}

    print("=" * 80)
    print("COMPREHENSIVE PFIRRMANN GRADE ANALYSIS")
    print("=" * 80)
    print(f"\nPatients   : {df['Patient_ID'].nunique()}")
    print(f"ID range   : {df['Patient_ID'].min()} -- {df['Patient_ID'].max()}")
    print(f"Missing    : {df.isnull().sum().sum()}")

    # ---- Distribution ----
    print("\n" + "=" * 80)
    print("GRADE DISTRIBUTION BY DISC LEVEL")
    print("=" * 80)
    for disc in ["D5", "D4", "D3"]:
        counts = df[disc].value_counts().sort_index()
        print(f"\n{disc} ({level_map[disc]}):")
        for g in range(1, 6):
            c = counts.get(g, 0)
            print(f"  Grade {g}: {c:3d} ({c / N * 100:5.2f}%)")

    # ---- Descriptive ----
    print("\n" + "=" * 80)
    print("STATISTICAL MEASURES")
    print("=" * 80)
    for disc in ["D5", "D4", "D3"]:
        d = df[disc]
        print(f"\n{disc}: mean={d.mean():.3f}  median={d.median():.1f}  "
              f"mode={d.mode().values[0]}  std={d.std():.3f}  "
              f"IQR={d.quantile(0.75) - d.quantile(0.25):.1f}")

    # ---- Multi-disc patterns ----
    print("\n" + "=" * 80)
    print("MULTI-DISC DEGENERATION PATTERNS")
    print("=" * 80)
    uniform = df[(df["D5"] == df["D4"]) & (df["D4"] == df["D3"])]
    print(f"\nUniform grades: {len(uniform)} ({len(uniform) / N * 100:.1f}%)")
    for g in range(1, 6):
        c = len(uniform[uniform["D5"] == g])
        if c:
            print(f"  Grade {g}: {c}")

    asc = df[(df["D5"] > df["D4"]) & (df["D4"] > df["D3"])]
    desc = df[(df["D5"] < df["D4"]) & (df["D4"] < df["D3"])]
    print(f"\nAscending (D5>D4>D3) : {len(asc)} ({len(asc) / N * 100:.1f}%)")
    print(f"Descending (D5<D4<D3): {len(desc)} ({len(desc) / N * 100:.1f}%)")

    # ---- Correlation ----
    print("\n" + "=" * 80)
    print("PEARSON CORRELATION")
    print("=" * 80)
    corr = df[["D5", "D4", "D3"]].corr()
    print(f"D5-D4: {corr.loc['D5', 'D4']:.3f}")
    print(f"D5-D3: {corr.loc['D5', 'D3']:.3f}")
    print(f"D4-D3: {corr.loc['D4', 'D3']:.3f}")

    # ---- Severity ----
    print("\n" + "=" * 80)
    print("SEVERITY CATEGORISATION")
    print("=" * 80)
    df["max_grade"] = df[["D5", "D4", "D3"]].max(axis=1)
    for g in range(1, 6):
        c = (df["max_grade"] == g).sum()
        print(f"  Max Grade {g}: {c:3d} ({c / N * 100:.2f}%)")

    severe = (df[["D5", "D4", "D3"]] >= 4).sum(axis=1)
    print("\nDiscs with Grade 4-5 per patient:")
    for n_disc in range(4):
        c = (severe == n_disc).sum()
        print(f"  {n_disc} discs: {c:3d} ({c / N * 100:.2f}%)")

    # ---- Worst disc ----
    df["worst_disc"] = df[["D5", "D4", "D3"]].idxmax(axis=1)
    print("\nWorst disc per patient:")
    for disc in ["D5", "D4", "D3"]:
        c = (df["worst_disc"] == disc).sum()
        print(f"  {disc} ({level_map[disc]}): {c} ({c / N * 100:.1f}%)")

    # ---- Class imbalance ----
    print("\n" + "=" * 80)
    print("CLASS IMBALANCE")
    print("=" * 80)
    for disc in ["D5", "D4", "D3"]:
        counts = df[disc].value_counts().sort_index()
        ratio = counts.max() / counts.min()
        vals = np.sort(counts.values)
        n_cls = len(vals)
        gini = (2 * np.sum(np.arange(1, n_cls + 1) * vals)) / (n_cls * vals.sum()) - (n_cls + 1) / n_cls
        print(f"\n{disc}: majority=Grade {counts.idxmax()} ({counts.max()}), "
              f"minority=Grade {counts.idxmin()} ({counts.min()}), "
              f"ratio={ratio:.1f}:1, Gini={gini:.3f}")

    # ---- Clinical summary ----
    print("\n" + "=" * 80)
    print("CLINICAL INTERPRETATION")
    print("=" * 80)
    avg = df[["D5", "D4", "D3"]].mean()
    for disc in ["D5", "D4", "D3"]:
        print(f"  {disc} ({level_map[disc]}): mean grade = {avg[disc]:.3f}")
    print(f"\nMost degenerated: {avg.idxmax()} (mean {avg.max():.3f})")
    pct_severe = (df[["D5", "D4", "D3"]] >= 4).any(axis=1).mean() * 100
    print(f"Patients with >= 1 severe disc: {pct_severe:.1f}%")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Pfirrmann grade distributions.")
    parser.add_argument("--csv", type=str, required=True)
    args = parser.parse_args()
    analyze(args.csv)
