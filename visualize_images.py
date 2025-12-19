import argparse
import glob
import os

import matplotlib.pyplot as plt
from PIL import Image


def load_image(image_path: str) -> Image.Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return Image.open(image_path)


def display_image(image: Image.Image, title: str, figsize=(10, 8)) -> None:
    plt.figure(figsize=figsize)
    plt.imshow(image, cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def list_available_sequences(images_dir: str) -> None:
    all_files = glob.glob(os.path.join(images_dir, "*.png"))
    sequences: set[str] = set()
    for file_path in all_files:
        filename = os.path.basename(file_path)
        parts = filename.split("_")
        if len(parts) >= 2:
            sequences.add(f"{parts[0]}_{parts[1]}")

    for seq in sorted(sequences):
        count = sum(1 for f in all_files if seq in os.path.basename(f))
        print(f"{seq}\t{count}")


def browse_images(sequence: str, images_dir: str, patient_id: str | None) -> None:
    if patient_id:
        pattern = os.path.join(images_dir, f"{sequence}_{patient_id}_*.png")
    else:
        pattern = os.path.join(images_dir, f"{sequence}_*.png")

    image_files = sorted(glob.glob(pattern))
    if not image_files:
        raise FileNotFoundError(f"No images found for pattern: {pattern}")

    for i, img_path in enumerate(image_files, start=1):
        print(f"{i:4d}  {os.path.basename(img_path)}")

    while True:
        choice = input("Enter image number (q to quit): ").strip()
        if choice.lower() == "q":
            return
        try:
            idx = int(choice) - 1
        except ValueError:
            continue
        if 0 <= idx < len(image_files):
            img_path = image_files[idx]
            image = load_image(img_path)
            display_image(image, os.path.basename(img_path))


def main() -> None:
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_images_dir = os.path.join(repo_dir, "images_png")

    parser = argparse.ArgumentParser(description="LSMA-PQR image viewer")
    parser.add_argument("--images_dir", type=str, default=default_images_dir)
    parser.add_argument("--image_path", type=str)
    parser.add_argument("--list_sequences", action="store_true")
    parser.add_argument("--browse", action="store_true")
    parser.add_argument("--sequence", type=str)
    parser.add_argument("--patient_id", type=str)
    args = parser.parse_args()

    if args.list_sequences:
        list_available_sequences(args.images_dir)
        return

    if args.image_path:
        image = load_image(args.image_path)
        display_image(image, os.path.basename(args.image_path))
        return

    if args.browse:
        if not args.sequence:
            raise SystemExit("--browse requires --sequence")
        browse_images(args.sequence, args.images_dir, args.patient_id)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
