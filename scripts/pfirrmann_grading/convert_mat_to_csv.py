"""
Convert Pfirrmann grade data from MATLAB .mat format to CSV.

Reads a .mat file containing the Pfirrmann degeneration grades matrix and
exports it as a CSV file.  The expected variable is a (N, 3) array with
columns corresponding to disc levels D5 (L5-S1), D4 (L4-L5), D3 (L3-L4).

Usage:
    python convert_mat_to_csv.py --mat_file <PfirrmannGrade.mat> --output <PfirrmannGrade.csv>
"""

import argparse
import os

import pandas as pd
import scipy.io


def convert(mat_path: str, output_csv: str) -> None:
    mat_data = scipy.io.loadmat(mat_path)

    print("Contents of .mat file:")
    print("=" * 60)
    for key, value in mat_data.items():
        if key.startswith("__"):
            continue
        print(f"Key: {key}  Shape: {value.shape}  Dtype: {value.dtype}")
        if value.size <= 20:
            print(f"  Values: {value}")
        else:
            print(f"  First 10: {value.flatten()[:10]}")

    data_keys = [k for k in mat_data if not k.startswith("__")]
    if not data_keys:
        raise ValueError("No data keys found in .mat file.")

    main_key = data_keys[0]
    data = mat_data[main_key]

    if data.ndim == 2:
        df = pd.DataFrame(data, columns=["D5", "D4", "D3"][:data.shape[1]])
    else:
        df = pd.DataFrame(data, columns=["Value"])

    df.to_csv(output_csv, index=False)

    print(f"\nConverted '{main_key}' -> {output_csv}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Pfirrmann .mat to CSV.")
    parser.add_argument("--mat_file", type=str, required=True)
    parser.add_argument("--output", type=str, default="PfirrmannGrade.csv")
    args = parser.parse_args()
    convert(args.mat_file, args.output)
