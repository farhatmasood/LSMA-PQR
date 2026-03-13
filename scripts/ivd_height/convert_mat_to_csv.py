"""
Batch-extract IVD heights and endpoint coordinates from MATLAB .mat files.

Each .mat file encodes the disc heights and superior/inferior end-plate
midpoint coordinates for three lumbar disc levels (D5=L5-S1, D4=L4-L5,
D3=L3-L4) measured on a T2-weighted mid-sagittal MRI slice.

The script parses Patient_ID from the filename convention:
    XXXX_T2_TSE_SAG_384_0002_<PatientID>_008_R.mat

Output CSV columns:
    Patient_ID, D5_Ht, D4_Ht, D3_Ht, D5_Coord, D4_Coord, D3_Coord

Coordinate format: "top_x,top_y;bottom_x,bottom_y" (pixel space)

Usage:
    python convert_mat_to_csv.py --mat_dir <path> --output <IVDHeights.csv>
"""

import argparse
import os

import numpy as np
import pandas as pd
import scipy.io


def extract_all(mat_dir: str, output_csv: str) -> None:
    mat_files = sorted(f for f in os.listdir(mat_dir) if f.endswith(".mat"))
    print(f"Found {len(mat_files)} .mat files in {mat_dir}")

    rows = []
    for idx, mat_file in enumerate(mat_files, 1):
        try:
            mat_data = scipy.io.loadmat(os.path.join(mat_dir, mat_file))
            parts = mat_file.replace(".mat", "").split("_")
            patient_id = int(parts[6])

            heights = mat_data["ivdHeights"].flatten()
            top = mat_data["topPoints"]
            bot = mat_data["bottomPoints"]

            def fmt_coord(i: int) -> str:
                return f"{top[i,0]:.2f},{top[i,1]:.2f};{bot[i,0]:.2f},{bot[i,1]:.2f}"

            rows.append({
                "Patient_ID": patient_id,
                "D5_Ht": float(heights[0]),
                "D4_Ht": float(heights[1]),
                "D3_Ht": float(heights[2]),
                "D5_Coord": fmt_coord(0),
                "D4_Coord": fmt_coord(1),
                "D3_Coord": fmt_coord(2),
            })
            if idx % 100 == 0:
                print(f"  Processed {idx} files ...")
        except Exception as e:
            print(f"  ERROR processing {mat_file}: {e}")

    df = pd.DataFrame(rows).sort_values("Patient_ID").reset_index(drop=True)
    df.to_csv(output_csv, index=False)

    print(f"\nCSV saved: {output_csv}")
    print(f"Total records      : {len(df)}")
    print(f"Unique Patient_IDs : {df['Patient_ID'].nunique()}")
    for col in ["D5_Ht", "D4_Ht", "D3_Ht"]:
        print(f"{col}  min={df[col].min():.2f}  max={df[col].max():.2f}  "
              f"mean={df[col].mean():.2f}")

    dups = df[df.duplicated(subset=["Patient_ID"], keep=False)]
    if len(dups):
        print(f"\nWARNING: {len(dups)} duplicate Patient_ID entries detected.")
    else:
        print("\nNo duplicate Patient_IDs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract IVD heights from .mat files.")
    parser.add_argument("--mat_dir", type=str, required=True,
                        help="Directory containing .mat files.")
    parser.add_argument("--output", type=str, default="IVDHeights.csv",
                        help="Output CSV filename.")
    args = parser.parse_args()
    extract_all(args.mat_dir, args.output)
