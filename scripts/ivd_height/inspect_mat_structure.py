"""
Inspect the internal structure of IVD height .mat files.

This script loads a single MATLAB .mat file exported by the IVD height
measurement tool and prints all stored variables, their shapes, data types,
and values.  It is intended as a diagnostic step before batch extraction.

Each .mat file contains three variables:
    ivdHeights   : ndarray of shape (3,) -- disc heights in mm [D5, D4, D3]
    topPoints    : ndarray of shape (3, 2) -- superior end-plate midpoints (x, y)
    bottomPoints : ndarray of shape (3, 2) -- inferior end-plate midpoints (x, y)

Usage:
    python inspect_mat_structure.py --mat_file <path_to_mat_file>
"""

import argparse
import scipy.io


def inspect(mat_path: str) -> None:
    mat_data = scipy.io.loadmat(mat_path)

    print("=" * 80)
    print(f"CONTENTS OF .MAT FILE: {mat_path}")
    print("=" * 80)

    print("\nKeys (excluding metadata):")
    print("-" * 80)
    for key in mat_data:
        if not key.startswith("__"):
            print(f"  - {key}")

    print("\n" + "=" * 80)
    print("DETAILED INFORMATION:")
    print("=" * 80)

    for key, value in mat_data.items():
        if key.startswith("__"):
            continue
        print(f"\nKey: '{key}'")
        print(f"  Type : {type(value).__name__}")
        print(f"  Shape: {value.shape}")
        print(f"  Dtype: {value.dtype}")
        print(f"  Size : {value.size}")
        if value.size <= 30:
            print(f"  Values: {value}")
        else:
            print(f"  First 10: {value.flatten()[:10]}")
            print(f"  Min={value.min():.4f}  Max={value.max():.4f}  Mean={value.mean():.4f}")

    print("\n" + "=" * 80)
    print("END OF FILE INSPECTION")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inspect the structure of an IVD height .mat file."
    )
    parser.add_argument("--mat_file", type=str, required=True,
                        help="Path to a single .mat file to inspect.")
    args = parser.parse_args()
    inspect(args.mat_file)
