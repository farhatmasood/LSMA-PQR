"""
Image Visualization Script for LSMA-PQR Dataset

This script provides functionality to visualize images from the LSMA-PQR dataset.
It supports loading and displaying individual images or browsing through multiple images.

Usage:
    python visualize_images.py --image_path "path/to/image.png"
    python visualize_images.py --browse --sequence "axial_T1" --patient_id "0112"
    python visualize_images.py --list_sequences

Author: Generated for LSMA-PQR Dataset Visualization
"""

import os
import argparse
import matplotlib.pyplot as plt
from PIL import Image
import glob

def load_image(image_path):
    """Load an image from the given path."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    return Image.open(image_path)

def display_image(image, title="Medical Image", figsize=(10, 8)):
    """Display a single image with matplotlib."""
    plt.figure(figsize=figsize)
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def browse_images_by_sequence(sequence, patient_id=None, base_path="D:\\2.2 Dataset_s\\LSMA-PQR\\images_png"):
    """Browse images for a specific sequence and optionally patient."""
    if patient_id:
        pattern = os.path.join(base_path, f"{sequence}_{patient_id}_*.png")
    else:
        pattern = os.path.join(base_path, f"{sequence}_*.png")

    image_files = sorted(glob.glob(pattern))

    if not image_files:
        print(f"No images found for pattern: {pattern}")
        return

    print(f"Found {len(image_files)} images for {sequence}")
    if patient_id:
        print(f"Patient ID: {patient_id}")

    for i, img_path in enumerate(image_files):
        print(f"{i+1:2d}. {os.path.basename(img_path)}")

    # Interactive browsing
    while True:
        try:
            choice = input("\nEnter image number to view (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                break

            idx = int(choice) - 1
            if 0 <= idx < len(image_files):
                image = load_image(image_files[idx])
                title = f"{os.path.basename(image_files[idx])}"
                display_image(image, title)
            else:
                print("Invalid image number.")

        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
        except KeyboardInterrupt:
            break

def list_available_sequences(base_path="D:\\2.2 Dataset_s\\LSMA-PQR\\images_png"):
    """List all available sequences in the dataset."""
    all_files = glob.glob(os.path.join(base_path, "*.png"))
    sequences = set()

    for file_path in all_files:
        filename = os.path.basename(file_path)
        # Extract sequence (e.g., "axial_T1", "sag_T2")
        parts = filename.split('_')
        if len(parts) >= 2:
            sequence = f"{parts[0]}_{parts[1]}"
            sequences.add(sequence)

    print("Available sequences:")
    for seq in sorted(sequences):
        count = len([f for f in all_files if seq in os.path.basename(f)])
        print(f"  {seq}: {count} images")

def main():
    parser = argparse.ArgumentParser(description="Visualize images from LSMA-PQR dataset")
    parser.add_argument("--image_path", type=str, help="Path to specific image file")
    parser.add_argument("--browse", action="store_true", help="Browse images interactively")
    parser.add_argument("--sequence", type=str, help="Sequence to browse (e.g., axial_T1, sag_T2)")
    parser.add_argument("--patient_id", type=str, help="Patient ID to filter (e.g., 0112)")
    parser.add_argument("--list_sequences", action="store_true", help="List all available sequences")

    args = parser.parse_args()

    if args.list_sequences:
        list_available_sequences()
        return

    if args.image_path:
        # Display single image
        try:
            image = load_image(args.image_path)
            title = os.path.basename(args.image_path)
            display_image(image, title)
        except Exception as e:
            print(f"Error loading image: {e}")

    elif args.browse:
        if not args.sequence:
            print("Please specify --sequence when using --browse")
            return
        browse_images_by_sequence(args.sequence, args.patient_id)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()