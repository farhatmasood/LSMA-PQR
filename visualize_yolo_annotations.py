import argparse
import glob
import os
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


@dataclass(frozen=True)
class YoloBox:
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float


CLASS_NAMES = {
    0: "IVD",
    1: "PE",
    2: "SC",
    3: "VBs",
    4: "IVD_sag",
    5: "Sacrum",
    6: "SC_sag",
}

CLASS_COLORS = {
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 255, 0),
    4: (255, 0, 255),
    5: (0, 255, 255),
    6: (128, 128, 128),
}


def load_image(path: str) -> Image.Image:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return Image.open(path)


def label_path_for_image(image_path: str, labels_dir: str) -> str:
    stem = os.path.splitext(os.path.basename(image_path))[0]
    return os.path.join(labels_dir, f"{stem}.txt")


def load_yolo_boxes(label_path: str) -> list[YoloBox]:
    if not os.path.exists(label_path):
        return []
    boxes: list[YoloBox] = []
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 5:
                continue
            class_id = int(float(parts[0]))
            x_center, y_center, width, height = map(float, parts[1:])
            boxes.append(YoloBox(class_id, x_center, y_center, width, height))
    return boxes


def draw_boxes(image: Image.Image, boxes: list[YoloBox], thickness: int = 2) -> Image.Image:
    img = np.array(image)
    if img.ndim == 2:
        img = np.stack([img, img, img], axis=-1)
    elif img.shape[2] == 4:
        img = img[:, :, :3]

    h, w = img.shape[:2]
    out = img.copy()

    for b in boxes:
        x1 = int((b.x_center - b.width / 2) * w)
        y1 = int((b.y_center - b.height / 2) * h)
        x2 = int((b.x_center + b.width / 2) * w)
        y2 = int((b.y_center + b.height / 2) * h)
        x1, x2 = max(0, x1), min(w - 1, x2)
        y1, y2 = max(0, y1), min(h - 1, y2)

        color = CLASS_COLORS.get(b.class_id, (255, 255, 255))

        out[y1 : y1 + thickness, x1:x2] = color
        out[y2 - thickness : y2, x1:x2] = color
        out[y1:y2, x1 : x1 + thickness] = color
        out[y1:y2, x2 - thickness : x2] = color

    return Image.fromarray(out)


def summarize_boxes(boxes: list[YoloBox]) -> str:
    if not boxes:
        return "0"
    counts: dict[int, int] = {}
    for b in boxes:
        counts[b.class_id] = counts.get(b.class_id, 0) + 1
    parts = []
    for cid in sorted(counts):
        parts.append(f"{CLASS_NAMES.get(cid, str(cid))}:{counts[cid]}")
    return ", ".join(parts)


def show_image_with_boxes(image_path: str, labels_dir: str) -> None:
    img = load_image(image_path)
    boxes = load_yolo_boxes(label_path_for_image(image_path, labels_dir))
    overlay = draw_boxes(img, boxes)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(img, cmap="gray")
    axes[0].set_title("Image")
    axes[0].axis("off")

    axes[1].imshow(overlay)
    axes[1].set_title(f"YOLO ({len(boxes)}): {summarize_boxes(boxes)}")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()


def browse(sequence: str, images_dir: str, labels_dir: str, patient_id: str | None) -> None:
    if patient_id:
        pattern = os.path.join(images_dir, f"{sequence}_{patient_id}_*.png")
    else:
        pattern = os.path.join(images_dir, f"{sequence}_*.png")

    image_files = sorted(glob.glob(pattern))
    if not image_files:
        raise FileNotFoundError(f"No images found for pattern: {pattern}")

    for i, img_path in enumerate(image_files, start=1):
        label_path = label_path_for_image(img_path, labels_dir)
        n = len(load_yolo_boxes(label_path))
        print(f"{i:4d}  {os.path.basename(img_path)}  boxes={n}")

    while True:
        choice = input("Enter image number (q to quit): ").strip()
        if choice.lower() == "q":
            return
        try:
            idx = int(choice) - 1
        except ValueError:
            continue
        if 0 <= idx < len(image_files):
            show_image_with_boxes(image_files[idx], labels_dir)


def main() -> None:
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_images_dir = os.path.join(repo_dir, "images_png")
    default_labels_dir = os.path.join(repo_dir, "labels_yolo")

    parser = argparse.ArgumentParser(description="LSMA-PQR YOLO bbox visualizer")
    parser.add_argument("--images_dir", type=str, default=default_images_dir)
    parser.add_argument("--labels_dir", type=str, default=default_labels_dir)
    parser.add_argument("--image_path", type=str)
    parser.add_argument("--browse", action="store_true")
    parser.add_argument("--sequence", type=str)
    parser.add_argument("--patient_id", type=str)
    args = parser.parse_args()

    if args.image_path:
        show_image_with_boxes(args.image_path, args.labels_dir)
        return

    if args.browse:
        if not args.sequence:
            raise SystemExit("--browse requires --sequence")
        browse(args.sequence, args.images_dir, args.labels_dir, args.patient_id)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
