"""
Visualize IVD height measurements overlaid on sagittal MRI images.

Draws colour-coded measurement lines between the superior and inferior
end-plate midpoints for each of three lumbar disc levels:
    Red   = D5 (L5-S1)
    Green = D4 (L4-L5)
    Blue  = D3 (L3-L4)

Requires:
    - Sagittal MRI images (PNG, 384x384)
    - ivd_height_mapping.csv  (image-to-height mapping)
    - ivd_height_coordinates.json  (automated coordinates)
    - manual_measurements_with_coordinates.json  (manual coordinates)

Usage:
    python visualize_ivd_heights.py \
        --images_dir <path> \
        --mapping_csv <path> \
        --auto_json <path> \
        --manual_json <path> \
        [--num_samples 10] [--save <output.png>]
"""

import argparse
import json
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DISC_COLOURS = {
    "D5": (0, 0, 255),   # Red (BGR)
    "D4": (0, 255, 0),   # Green
    "D3": (255, 0, 0),   # Blue
}
DISC_LABELS = {"D5": "D5 (L5-S1)", "D4": "D4 (L4-L5)", "D3": "D3 (L3-L4)"}
HEIGHT_COLUMNS = {"D5": "disc_1_height_mm", "D4": "disc_2_height_mm", "D3": "disc_3_height_mm"}


def visualize(images_dir: str, mapping_csv: str, auto_json: str,
              manual_json: str, num_samples: int, save_path: str | None) -> None:
    df = pd.read_csv(mapping_csv)
    with open(auto_json) as f:
        auto_coords = json.load(f)
    with open(manual_json) as f:
        manual_coords = json.load(f)

    manual_pids = set(manual_coords.keys())
    available = df[df["has_ivd_height"] == True]  # noqa: E712
    n = min(num_samples, len(available))
    samples = available.sample(n=n, random_state=random.randint(0, 9999))

    cols = min(5, n)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    fig.suptitle("Sagittal IVD Height Measurements", fontsize=14, fontweight="bold")
    axes = np.atleast_1d(axes).flatten()

    for idx, (_, row) in enumerate(samples.iterrows()):
        ax = axes[idx]
        img_path = f"{images_dir}/{row['image_filename']}"
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            ax.text(0.5, 0.5, "Not found", ha="center", va="center")
            ax.axis("off")
            continue

        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        pid = str(row["patient_id"])
        fname = row["image_filename"]
        is_manual = pid in manual_pids

        for disc_key, label in DISC_LABELS.items():
            h_mm = row[HEIGHT_COLUMNS[disc_key]]
            if pd.isna(h_mm):
                continue

            top = bottom = None
            if is_manual and pid in manual_coords:
                c = manual_coords[pid]["coordinates"].get(disc_key)
                if c:
                    top, bottom = tuple(map(int, c["top"])), tuple(map(int, c["bottom"]))
            elif fname in auto_coords:
                d = auto_coords[fname]["disc_measurements"].get(disc_key)
                if d:
                    top, bottom = tuple(map(int, d["top"])), tuple(map(int, d["bottom"]))

            if top is None:
                continue

            colour = DISC_COLOURS[disc_key]
            cv2.line(img_bgr, top, bottom, colour, 2)
            cv2.circle(img_bgr, top, 4, colour, -1)
            cv2.circle(img_bgr, bottom, 4, colour, -1)

            mid_y = (top[1] + bottom[1]) // 2
            cv2.putText(img_bgr, f"{label}: {h_mm:.2f}mm", (10, mid_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, colour, 1)

        ax.imshow(img_bgr)
        source = "Manual" if is_manual else "Auto"
        ax.set_title(f"Patient {row['patient_id']} ({row['modality']}) [{source}]",
                     fontsize=9, fontweight="bold")
        ax.axis("off")

    for i in range(n, len(axes)):
        axes[i].axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize IVD height measurements.")
    parser.add_argument("--images_dir", type=str, required=True)
    parser.add_argument("--mapping_csv", type=str, required=True)
    parser.add_argument("--auto_json", type=str, required=True)
    parser.add_argument("--manual_json", type=str, required=True)
    parser.add_argument("--num_samples", type=int, default=10)
    parser.add_argument("--save", type=str, default=None)
    args = parser.parse_args()
    visualize(args.images_dir, args.mapping_csv, args.auto_json,
              args.manual_json, args.num_samples, args.save)
