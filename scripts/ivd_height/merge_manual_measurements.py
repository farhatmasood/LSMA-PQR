"""
Recover missing patients by merging manual JSON measurements into the CSV.

Ten patients (IDs: 192, 245, 272, 290, 368, 428, 468, 472, 525, 568) lacked
corresponding .mat files and were measured manually.  Their heights and
endpoint coordinates are stored in a JSON file with the structure:

    { "<patient_id>": {
        "disc_1_height_mm": <float>,   // D5 (L5-S1)
        "disc_2_height_mm": <float>,   // D4 (L4-L5)
        "disc_3_height_mm": <float>,   // D3 (L3-L4)
        "coordinates": {
            "D5": { "top": [x, y], "bottom": [x, y] }, ...
        }
    } }

Usage:
    python merge_manual_measurements.py \
        --csv IVDHeights_Cleaned.csv \
        --json manual_measurements_with_coordinates.json \
        --output IVDHeights_Corrected.csv
"""

import argparse
import json

import pandas as pd


def merge(csv_path: str, json_path: str, output_path: str) -> None:
    df = pd.read_csv(csv_path)
    with open(json_path, "r") as f:
        manual = json.load(f)

    csv_ids = set(df["Patient_ID"].values)
    new_rows = []

    for pid_str, data in sorted(manual.items(), key=lambda x: int(x[0])):
        pid = int(pid_str)
        if pid in csv_ids:
            continue

        coords = data.get("coordinates", {})

        def fmt(disc_key: str) -> str:
            c = coords.get(disc_key, {})
            t, b = c.get("top", []), c.get("bottom", [])
            return f"{t[0]},{t[1]};{b[0]},{b[1]}" if t and b else ""

        new_rows.append({
            "Patient_ID": pid,
            "D5_Ht": data.get("disc_1_height_mm"),
            "D4_Ht": data.get("disc_2_height_mm"),
            "D3_Ht": data.get("disc_3_height_mm"),
            "D5_Coord": fmt("D5"),
            "D4_Coord": fmt("D4"),
            "D3_Coord": fmt("D3"),
        })

    df_merged = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df_merged = df_merged.sort_values("Patient_ID").reset_index(drop=True)
    df_merged.to_csv(output_path, index=False)

    print("=" * 80)
    print("MERGE REPORT")
    print("=" * 80)
    print(f"Original CSV : {len(df)} patients")
    print(f"Added from JSON: {len(new_rows)} patients")
    print(f"  IDs: {[r['Patient_ID'] for r in new_rows]}")
    print(f"Merged CSV   : {len(df_merged)} patients "
          f"({df_merged['Patient_ID'].nunique()} unique)")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge manual measurements into CSV.")
    parser.add_argument("--csv", type=str, required=True)
    parser.add_argument("--json", type=str, required=True)
    parser.add_argument("--output", type=str, default="IVDHeights_Corrected.csv")
    args = parser.parse_args()
    merge(args.csv, args.json, args.output)
