import argparse
import glob
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


CLASS_NAMES = {
    0: "Background",
    1: "IVD",
    2: "PE",
    3: "SC",
    4: "VBs",
    5: "IVD_sag",
    6: "Sacrum",
    7: "SC_sag",
}

COLORS_RGBA = np.array(
    [
        [0, 0, 0, 0],
        [255, 0, 0, 128],
        [0, 255, 0, 128],
        [0, 0, 255, 128],
        [255, 255, 0, 128],
        [255, 0, 255, 128],
        [0, 255, 255, 128],
        [128, 128, 128, 128],
    ],
    dtype=np.uint8,
)


def load_image(path: str) -> Image.Image:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return Image.open(path)


def mask_path_for_image(image_path: str, masks_dir: str) -> str:
    return os.path.join(masks_dir, os.path.basename(image_path))


def load_mask_indexed(mask_path: str) -> np.ndarray:
    if not os.path.exists(mask_path):
        raise FileNotFoundError(mask_path)
    return np.array(Image.open(mask_path))


def to_colored_rgba(mask: np.ndarray) -> np.ndarray:
    h, w = mask.shape[:2]
    out = np.zeros((h, w, 4), dtype=np.uint8)

    max_id = int(mask.max()) if mask.size else 0
    palette = COLORS_RGBA
    if max_id >= palette.shape[0]:
        pad = np.zeros((max_id + 1 - palette.shape[0], 4), dtype=np.uint8)
        pad[:, 3] = 128
        palette = np.concatenate([palette, pad], axis=0)

    out = palette[mask]
    return out


def overlay(image: Image.Image, mask: np.ndarray, alpha: float = 0.55) -> Image.Image:
    base = image.convert("RGBA")
    base_np = np.array(base).astype(np.float32)
    colored = to_colored_rgba(mask).astype(np.float32)

    m_a = (colored[:, :, 3:4] / 255.0) * alpha
    inv = 1.0 - m_a

    out = base_np.copy()
    out[:, :, :3] = base_np[:, :, :3] * inv + colored[:, :, :3] * m_a
    out[:, :, 3] = np.maximum(base_np[:, :, 3], (m_a * 255.0).squeeze())

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def mask_stats(mask: np.ndarray) -> dict[int, int]:
    ids, counts = np.unique(mask, return_counts=True)
    stats: dict[int, int] = {}
    for cid, cnt in zip(ids.tolist(), counts.tolist()):
        stats[int(cid)] = int(cnt)
    return stats


def show(image_path: str, masks_dir: str) -> None:
    img = load_image(image_path)
    mpath = mask_path_for_image(image_path, masks_dir)
    m = load_mask_indexed(mpath)
    ov = overlay(img, m)

    stats = mask_stats(m)
    summary = []
    for cid in sorted(stats):
        if cid == 0:
            continue
        summary.append(f"{CLASS_NAMES.get(cid, str(cid))}:{stats[cid]}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    axes[0].imshow(img, cmap="gray")
    axes[0].set_title("Image")
    axes[0].axis("off")

    axes[1].imshow(to_colored_rgba(m))
    axes[1].set_title("Mask")
    axes[1].axis("off")

    axes[2].imshow(ov)
    axes[2].set_title("Overlay" + ("\n" + ", ".join(summary) if summary else ""))
    axes[2].axis("off")

    plt.tight_layout()
    plt.show()


def browse(sequence: str, images_dir: str, masks_dir: str, patient_id: str | None) -> None:
    if patient_id:
        pattern = os.path.join(images_dir, f"{sequence}_{patient_id}_*.png")
    else:
        pattern = os.path.join(images_dir, f"{sequence}_*.png")

    image_files = sorted(glob.glob(pattern))
    if not image_files:
        raise FileNotFoundError(f"No images found for pattern: {pattern}")

    for i, img_path in enumerate(image_files, start=1):
        mpath = mask_path_for_image(img_path, masks_dir)
        ok = os.path.exists(mpath)
        print(f"{i:4d}  {os.path.basename(img_path)}  mask={'yes' if ok else 'no'}")

    while True:
        choice = input("Enter image number (q to quit): ").strip()
        if choice.lower() == "q":
            return
        try:
            idx = int(choice) - 1
        except ValueError:
            continue
        if 0 <= idx < len(image_files):
            show(image_files[idx], masks_dir)


def main() -> None:
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_images_dir = os.path.join(repo_dir, "images_png")
    default_masks_dir = os.path.join(repo_dir, "masks_indexed")

    parser = argparse.ArgumentParser(description="LSMA-PQR semantic mask visualizer")
    parser.add_argument("--images_dir", type=str, default=default_images_dir)
    parser.add_argument("--masks_dir", type=str, default=default_masks_dir)
    parser.add_argument("--image_path", type=str)
    parser.add_argument("--browse", action="store_true")
    parser.add_argument("--sequence", type=str)
    parser.add_argument("--patient_id", type=str)
    args = parser.parse_args()

    if args.image_path:
        show(args.image_path, args.masks_dir)
        return

    if args.browse:
        if not args.sequence:
            raise SystemExit("--browse requires --sequence")
        browse(args.sequence, args.images_dir, args.masks_dir, args.patient_id)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
