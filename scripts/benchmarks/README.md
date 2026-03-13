# Baseline Benchmarks

This document describes the model architectures, training procedures and evaluation protocols for the three baseline experiments reported in the LSMA-PQR manuscript. All experiments were conducted on a single NVIDIA RTX 4070 (8 GB) with PyTorch 2.5.1, CUDA 12.1, and seed = 42.

---

## 1. Multi-Plane Anatomical Segmentation

### Architecture

- **Backbone**: YOLO11m with multi-scale feature fusion
- **Parameters**: 54.1M total; 17% trainable (encoder weights frozen)
- **Input**: 384 x 384 RGB images (axial and sagittal jointly)
- **Output**: Per-pixel class masks
  - Axial: c0 (IVD), c1 (PE), c2 (SC)
  - Sagittal: c3 (VB), c4 (IVD), c5 (Sacrum), c6 (SC)

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimiser | AdamW |
| Learning rate | 1e-4 |
| Scheduler | OneCycleLR |
| Epochs | 100 |
| Precision | Mixed (GradScaler) |
| Loss | Dice + Focal + Boundary (Sobel-based MSE) |
| Split | 70% train / 15% val / 15% test (patient-stratified) |

### Results

| View | Class | Dice | IoU | Precision | Recall |
|------|-------|:----:|:---:|:---------:|:------:|
| Axial | IVD (c0) | 0.978 | 0.956 | 0.976 | 0.979 |
| Axial | PE (c1) | 0.935 | 0.878 | 0.936 | 0.935 |
| Axial | SC (c2) | 0.919 | 0.850 | 0.921 | 0.917 |
| Sagittal | VB (c3) | 0.958 | 0.919 | 0.953 | 0.963 |
| Sagittal | IVD (c4) | 0.936 | 0.879 | 0.934 | 0.937 |
| Sagittal | Sacrum (c5) | 0.958 | 0.920 | 0.960 | 0.957 |
| Sagittal | SC (c6) | 0.939 | 0.884 | 0.941 | 0.936 |
| **Overall** | | **0.946** | **0.898** | **0.946** | **0.946** |

---

## 2. Disc-Aware Pfirrmann Grading

### Architecture (GradingAdapter)

- **Vision encoder**: DINOv2-base ViT (frozen) with Low-Rank Adaptation (LoRA)
  - LoRA rank *r* = 8, alpha = 16
  - Applied to: `qkv`, `proj`, `fc1`, `fc2` layers
- **Disc-level embedding**: Learnable positional embeddings for D3, D4, D5
- **Regression head**: OrdinalRegressionHead with cumulative sigmoid thresholds
- **Trainable parameters**: ~2.39M

### Input Pipeline

1. Run segmentation model on sagittal T2 images
2. Extract IVD mask (class c4) using connected-component analysis
3. Sort components by Y-position; map bottom 3 to D3, D4, D5
4. Crop each disc region with 2.5x context padding
5. Resize to 224 x 224

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimiser | AdamW |
| Learning rate | 5e-5 |
| Scheduler | CosineAnnealingLR |
| Epochs | 50 |
| Precision | Mixed (GradScaler) |
| Loss | Ordinal BCE + CE (stenosis) + BCE (pathology) |
| Best checkpoint | By validation quadratic weighted kappa |

### Results

| Setting | *n* | Accuracy | Kappa | F1-W |
|---------|----:|:--------:|:-----:|:----:|
| D3 (L3-L4) | 79 | 64.6% | 0.592 | 0.641 |
| D4 (L4-L5) | 83 | 44.6% | 0.379 | 0.451 |
| D5 (L5-S1) | 69 | 30.4% | 0.408 | 0.293 |
| **Overall** | **231** | **47.2%** | **0.505** | **0.482** |
| Best Validation | -- | -- | 0.585 | -- |
| Ablation (no disc embeddings) | -- | -- | 0.358 | -- |

Disc-aware positional embeddings improve kappa by +63% (0.358 to 0.585).

### Error Analysis

- 93% of errors are single-grade deviations
- 7% are two-grade deviations; 0% exceed two grades
- Grade 2/3 boundary accounts for 50% of errors (expected given subjective ordinal boundaries)

---

## 3. Structured Clinical Findings Extraction

### Architecture (StructuredFindingsAdapter)

- **Feature extractor**: ResNet-18 (pretrained, optionally frozen)
  - Extracts 512-dim features per disc crop via global average pooling
- **Aggregator**: MultiDiscAggregator
  - Input: 3 disc features (D3, D4, D5) + Pfirrmann grade embeddings (32-dim)
  - 4-head multi-head self-attention across disc positions
  - Output: 256-dim aggregated patient representation
- **Classification heads**:
  - 36 binary pathology labels (sigmoid)
  - L4-L5 disc type (6 classes: None, Diffuse Bulge, Central/Paracentral/Foraminal Protrusion, Extrusion)
  - L5-S1 disc type (6 classes)
  - Severity (3 classes: Mild, Moderate, Severe)
- **Total parameters**: 12.28M

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimiser | AdamW |
| Learning rate | 1e-4 |
| Scheduler | OneCycleLR |
| Epochs | 50 (early stopping, patience = 15; best at epoch 14) |
| Binary loss | BCE with per-label pos\_weight = N\_neg / N\_pos (clamped at 20) |
| Severity loss | CE with class weights (clamped at 10) |
| Best checkpoint | By validation F1-weighted |

### Results

| Metric | Score |
|--------|:-----:|
| Hamming Loss | 0.261 |
| F1 (Macro) | 0.318 |
| F1 (Micro) | 0.500 |
| **F1 (Weighted)** | **0.585** |
| L4-L5 Type Accuracy | 57.1% |
| L5-S1 Type Accuracy | 66.2% |
| Severity Accuracy | 54.5% |

### Top Label-Wise F1

| Label | F1 |
|-------|:--:|
| L4-L5 Involvement | 0.822 |
| Thecal Sac Compression | 0.821 |
| L4-L5 Compression | 0.796 |
| Disc Bulge | 0.729 |
| Disc Protrusion | 0.556 |

High-prevalence labels (>30%) achieve mean F1 = 0.680; low-prevalence labels (<10%) achieve mean F1 = 0.094, consistent with the strong prevalence dependence of binary classifiers on imbalanced data.

---

## Reproducibility

- Hardware: NVIDIA RTX 4070 (8 GB VRAM)
- Software: Python 3.12, PyTorch 2.5.1, CUDA 12.1
- Random seed: 42 (note: GPU non-determinism introduces kappa variance of ~0.50--0.55 across grading runs)
- All splits are deterministic and patient-stratified
