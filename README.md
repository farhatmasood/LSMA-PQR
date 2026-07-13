<h1 align="center">LSMA-PQR</h1>
<h3 align="center">Lumbar Spine Multi-view Annotations with Pfirrmann Grading,<br>Quantitative Measurements and Structured Radiological Reports</h3>

<p align="center">
  <a href="https://doi.org/10.1007/s10278-026-02125-5"><img src="https://img.shields.io/badge/Paper-Journal%20of%20Imaging%20Informatics%20in%20Medicine-success" alt="Paper"></a>
      <a href="https://doi.org/10.17632/p3r4xd2488.2"><img src="https://img.shields.io/badge/DOI-10.17632%2Fp3r4xd2488.2-blue" alt="DOI"></a>
  <a href="https://data.mendeley.com/datasets/p3r4xd2488/2"><img src="https://img.shields.io/badge/Mendeley%20Data-v2.0-orange" alt="Mendeley Data"></a>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey" alt="License"></a>
  <!-- <img src="https://img.shields.io/badge/Images-4%2C120-green" alt="Images">
  <img src="https://img.shields.io/badge/Patients-515-green" alt="Patients"> -->
</p>

<p align="center">
  <img src="assets/Figure_01_dataset_overview_infographic.png" alt="Dataset Overview" width="720">
</p>

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Highlights](#2-highlights)
3. [Dataset at a Glance](#3-dataset-at-a-glance)
4. [Mathematical Framework](#4-mathematical-framework)
   - [4.1 Image Acquisition Model](#41-image-acquisition-model)
   - [4.2 Anatomical Annotation Framework](#42-anatomical-annotation-framework)
   - [4.3 Cross-Format Consistency Verification](#43-cross-format-consistency-verification)
   - [4.4 Intervertebral Disc Height Measurement](#44-intervertebral-disc-height-measurement)
   - [4.5 Pfirrmann Degeneration Grading](#45-pfirrmann-degeneration-grading)
   - [4.6 Clinical Report Processing Pipeline](#46-clinical-report-processing-pipeline)
5. [Dataset Contents and Structure](#5-dataset-contents-and-structure)
6. [Annotation Specifications](#6-annotation-specifications)
7. [Clinical Metadata](#7-clinical-metadata)
   - [7.1 Pfirrmann Grades](#71-pfirrmann-grades)
   - [7.2 IVD Height Measurements](#72-ivd-height-measurements)
   - [7.3 Structured Radiological Reports](#73-structured-radiological-reports)
8. [Quality Assurance](#8-quality-assurance)
9. [Baseline Benchmarks](#9-baseline-benchmarks)
   - [9.1 Multi-Plane Anatomical Segmentation](#91-multi-plane-anatomical-segmentation)
   - [9.2 Disc-Aware Pfirrmann Grading](#92-disc-aware-pfirrmann-grading)
   - [9.3 Structured Clinical Findings Extraction](#93-structured-clinical-findings-extraction)
10. [Research Applications](#10-research-applications)
11. [Getting Started](#11-getting-started)
12. [Repository Structure](#12-repository-structure)
13. [Limitations](#13-limitations)
14. [Citation](#14-citation)
15. [License](#15-license)
<!-- 16. [Authors](#16-authors) -->

---

## 1. Abstract

Automated analysis of lumbar spine MRI remains constrained by the absence of a comprehensive dataset integrating pixel-level anatomy, quantitative markings and radiological notes within a unified framework. We present **LSMA-PQR**, a clinically validated lumbar spine MRI dataset comprising *N* = 515 patients with dual-plane, dual-sequence imaging (axial and sagittal T1/T2-weighted; 4,120 total images) and comprehensive multi-modal annotations. Pixel-level segmentation masks for seven anatomical structures are provided in multiple interoperable formats (YOLO polygon, semantic) with verified cross-format spatial consistency (mean IoU = 0.994 &pm; 0.008). Beyond anatomy, the dataset integrates quantitative disc markings including 1,545 Pfirrmann degeneration grades (L3-L4, L4-L5, L5-S1) and intervertebral disc height measurements with pixel-coordinate provenance, as well as structured radiological reports derived from 515 free-text documents through systematic natural language processing that identified and corrected 340 transcription errors across 59% of reports.

Baseline experiments on three downstream tasks -- multi-plane segmentation (mean Dice = 0.946), disc-aware Pfirrmann grading (quadratic weighted &kappa; = 0.51) and structured clinical findings extraction (weighted F1 = 0.59) -- demonstrate the dataset's utility for training and evaluating automated lumbar spine analysis systems.

> **Data Access**: [https://data.mendeley.com/datasets/p3r4xd2488/2](https://data.mendeley.com/datasets/p3r4xd2488/2)

---

## 2. Highlights

| # | Highlight |
|---|-----------|
| 1 | **4,120** annotated lumbar spine MRI images (3,090 axial + 1,030 sagittal) at 384&times;384 resolution |
| 2 | Validated disc heights (MAE = 0.31 mm) and Pfirrmann degeneration grades across **1,545** discs |
| 3 | **515** structured, error-corrected radiology reports enabling joint image-text analysis |
| 4 | Baseline experiments on segmentation (Dice = 0.946), grading (&kappa; = 0.51) and findings extraction (F1 = 0.59) |
| 5 | Open-access dataset supporting multi-modal fusion: segmentation, grading, regression and NLP |

---

## 3. Dataset at a Glance

### Image Distribution

| Metric | Axial | Sagittal | Total |
|--------|------:|--------:|------:|
| Total images | 3,090 | 1,030 | **4,120** |
| T1-weighted | 1,545 | 515 | 2,060 |
| T2-weighted | 1,545 | 515 | 2,060 |
| Images per patient | 6 | 2 | 8 |
| Disc levels covered | D3, D4, D5 | Mid-sagittal | -- |
| Anatomical classes | 3 | 4 | 7 |

### Annotation Statistics

| Plane | Class | ID | Label Files | Objects | Objects/Image |
|-------|-------|----|----------:|--------:|--------------:|
| Axial | Intervertebral Disc (IVD) | c0 | 3,090 | 3,090 | 1.0 |
| Axial | Posterior Elements (PE) | c1 | 3,090 | 3,090 | 1.0 |
| Axial | Spinal Canal (SC) | c2 | 3,090 | 3,090 | 1.0 |
| | *Axial subtotal* | | *3,090* | *9,270* | *3.0* |
| Sagittal | Vertebral Bodies (VB) | c3 | 1,030 | 6,766 | 6.6 &pm; 1.2 |
| Sagittal | Intervertebral Discs (IVD) | c4 | 1,030 | 7,047 | 6.8 &pm; 1.1 |
| Sagittal | Sacrum (S) | c5 | 1,030 | 1,030 | 1.0 |
| Sagittal | Spinal Canal (SC) | c6 | 1,030 | 1,030 | 1.0 |
| | *Sagittal subtotal* | | *1,030* | *15,873* | *15.4* |
| **Combined** | | | **4,120** | **25,143** | **6.1** |

---

## 4. Mathematical Framework

### 4.1 Image Acquisition Model

Each patient $p_i$ contributes a set of images across two modalities and multiple anatomical slices:

$$\mathcal{I}\_{p_i} = \\{I^{T1}\_{ax},\; I^{T2}\_{ax},\; I^{T1}\_{sag},\; I^{T2}\_{sag}\\} \times \\{L_k\\}\_{k=1}^{n_k}$$

Mid-sagittal slice selection follows:

$$s^* = \arg\min\_{s \in \mathcal{S}} \left| x_s - \frac{W}{2} \right|$$

All images are resampled to a standardised 384 &times; 384 resolution via bicubic interpolation:

$$I\_{\text{std}}(u,v) = \mathcal{T}[I\_{\text{raw}}](u,v) = \sum\_{x,y} I\_{\text{raw}}(x,y) \cdot K\!\left(\frac{u \cdot H}{384} - x,\; \frac{v \cdot W}{384} - y\right)$$

where $K$ is the Catmull-Rom bicubic kernel ($a = -0.5$):

$$K\_{\text{1D}}(t) = \begin{cases} (a+2)|t|^3 - (a+3)|t|^2 + 1 & |t| \le 1 \\\\[4pt] a|t|^3 - 5a|t|^2 + 8a|t| - 4a & 1 < |t| < 2 \\\\[4pt] 0 & \text{otherwise} \end{cases}$$

### 4.2 Anatomical Annotation Framework

**Axial classes:**

$$\mathcal{C}\_{ax} = \\{c_0: \text{IVD},\; c_1: \text{PE},\; c_2: \text{SC}\\}$$

**Sagittal classes:**

$$\mathcal{C}\_{sag} = \\{c_3: \text{VB},\; c_4: \text{IVD},\; c_5: \text{Sacrum},\; c_6: \text{SC}\\}$$

The axial segmentation mask assigns each pixel a class label:

$$M\_{ax}(u,v) = \begin{cases} 0 & (u,v) \in \text{Background} \\\\[2pt] 1 & (u,v) \in \text{IVD} \\\\[2pt] 2 & (u,v) \in \text{PE} \\\\[2pt] 3 & (u,v) \in \text{SC} \end{cases}$$

Polygon annotations are rasterised using the even-odd rule:

$$\mathcal{R}[\mathbf{V}](u,v) = \begin{cases} 1 & \text{if } \left(\sum\_{i=1}^{n} \mathbb{1}\!\left[\ell\_{(u,v)} \cap e_i \neq \emptyset\right]\right) \bmod 2 = 1 \\\\[4pt] 0 & \text{otherwise} \end{cases}$$

### 4.3 Cross-Format Consistency Verification

Spatial consistency between YOLO-polygon and semantic-mask formats is verified per class $k$ via the Intersection-over-Union:

$$\text{IoU}_k(M_A, M_B) = \frac{|R_A \cap R_B|}{|R_A \cup R_B|}$$

Aggregated across both imaging planes:

$$\overline{\text{IoU}} = \frac{1}{2}\!\left(\frac{1}{N\_{ax}|\mathcal{C}\_{ax}|} \sum\_{i=1}^{N\_{ax}} \sum\_{k \in \mathcal{C}\_{ax}} \text{IoU}\_k^{(i)} \;+\; \frac{1}{N\_{sag}|\mathcal{C}\_{sag}|} \sum\_{j=1}^{N\_{sag}} \sum\_{k \in \mathcal{C}\_{sag}} \text{IoU}\_k^{(j)}\right)$$

> **Result**: Mean IoU = 0.994 &pm; 0.008 across 4,120 images.

### 4.4 Intervertebral Disc Height Measurement

Disc height is computed as the Euclidean distance between superior and inferior end-plate midpoints, scaled by pixel spacing $\rho = 0.6875$ mm/pixel:

$$h_d = \\|\mathbf{p}\_{\text{sup}} - \mathbf{p}\_{\text{inf}}\\|\_2 \times \rho$$

For oblique disc orientations, the perpendicular height is obtained by projecting onto the disc mid-plane normal:

$$h\_{\perp} = |(\mathbf{p}\_{\text{sup}} - \mathbf{p}\_{\text{inf}}) \cdot \hat{\mathbf{n}}| \times \rho$$

**Severity classification:**

$$\text{Severity}(h_d) = \begin{cases} \text{Normal} & h_d \ge 9 \text{ mm} \\\\[2pt] \text{Mild} & 7 \le h_d < 9 \text{ mm} \\\\[2pt] \text{Moderate} & 5 \le h_d < 7 \text{ mm} \\\\[2pt] \text{Severe} & h_d < 5 \text{ mm} \end{cases}$$

**Disc Height Index (DHI):**

$$\text{DHI}\_d = \frac{h_d}{\bar{h}\_{\text{VB},d}}$$

### 4.5 Pfirrmann Degeneration Grading

The Pfirrmann system is a five-point ordinal scale assessed on T2-weighted MRI. Quantitative grading integrates three complementary metrics:

**Disc Signal Intensity Index:**

$$\text{DSI}^2\_d = \frac{\bar{S}\_{NP,d}}{\bar{S}\_{CSF}} \times 100$$

**Coefficient of Variation:**

$$\text{CV}\_d = \frac{\sigma\_{NP,d}}{\bar{S}\_{NP,d}}$$

The quantitative grading function combines these with DHI:

$$\hat{G}(I, d) = \begin{cases} 1 & \text{DSI}^2\_d > 80 \;\land\; \text{CV}\_d < 0.15 \;\land\; \text{DHI}\_d \ge 0.95 \cdot \overline{\text{DHI}} \\\\[3pt] 2 & 60 < \text{DSI}^2\_d \le 80 \;\land\; \text{CV}\_d < 0.25 \;\land\; \text{DHI}\_d \ge 0.90 \cdot \overline{\text{DHI}} \\\\[3pt] 3 & 40 < \text{DSI}^2\_d \le 60 \;\land\; \text{DHI}\_d \ge 0.80 \cdot \overline{\text{DHI}} \\\\[3pt] 4 & 25 < \text{DSI}^2\_d \le 40 \;\land\; 0.60 \cdot \overline{\text{DHI}} \le \text{DHI}\_d < 0.80 \cdot \overline{\text{DHI}} \\\\[3pt] 5 & \text{DSI}^2\_d \le 25 \;\lor\; \text{DHI}\_d < 0.60 \cdot \overline{\text{DHI}} \end{cases}$$

> Calibration against expert labels: accuracy = 92.3%, &kappa;<sub>w</sub> = 0.89, &rho;<sub>s</sub> = 0.94 (*p* < 0.001).

**Intraclass Correlation Coefficient** for inter-observer reliability:

$$\text{ICC}(2,1) = \frac{\text{MS}\_R - \text{MS}\_E}{\text{MS}\_R + (k-1)\text{MS}\_E + \frac{k}{n}(\text{MS}\_C - \text{MS}\_E)}$$

### 4.6 Clinical Report Processing Pipeline

Lexical correction uses the Levenshtein edit distance against a 2,847-term RadLex vocabulary:

$$t' = \arg\min\_{c \in \mathcal{V}\_{\text{med}}} d_L(t, c) \quad \text{s.t.} \quad d_L(t, c) \le \tau_L$$

where the recursive Levenshtein distance is:

$$d_L(a, b) = \begin{cases} |a| & |b| = 0 \\\\[2pt] |b| & |a| = 0 \\\\[2pt] d_L(\text{tail}(a), \text{tail}(b)) & a[0] = b[0] \\\\[2pt] 1 + \min\\{d_L(\text{tail}(a), b),\; d_L(a, \text{tail}(b)),\; d_L(\text{tail}(a), \text{tail}(b))\\} & \text{otherwise} \end{cases}$$

Phonetic matching via Double Metaphone handles terms beyond the Levenshtein threshold:

$$t' = \arg\min\_{c \in \mathcal{V}\_{\text{med}}} d_H\bigl(\text{DM}(t),\; \text{DM}(c)\bigr)$$

**Named Entity Recognition** (hybrid pattern-based + medical terminology matching):

$$\mathcal{M}\_S(R') = \\{(e_j, \text{type}\_j, \text{span}\_j)\\}\_{j=1}^{n_e}$$

**Severity ordinal mapping:**

$$\mathcal{Q}: \text{Severity} \rightarrow \\{0, 1, 2, 3\\} = \begin{cases} 0 & \text{``normal'', ``unremarkable'', ``intact''} \\\\[2pt] 1 & \text{``mild'', ``minimal'', ``slight''} \\\\[2pt] 2 & \text{``moderate'', ``intermediate''} \\\\[2pt] 3 & \text{``severe'', ``marked'', ``advanced''} \end{cases}$$

**Pathology prevalence estimation:**

$$\hat{\pi}\_k = \frac{1}{N_p} \sum\_{i=1}^{N_p} \mathbb{1}[p_k \in R'_i]$$

Each patient's structured clinical record integrates all modalities:

$$\mathbf{c}\_i = (\text{ID}\_i,\; b_i,\; s_i,\; \mathcal{L}\_i,\; \lambda_i,\; h_i,\; G_i)$$

---

## 5. Dataset Contents and Structure

After downloading from [Mendeley Data](https://data.mendeley.com/datasets/p3r4xd2488/1), the dataset has the following structure:

```
LSMA-PQR/
├── images_png/                     # 4,120 MRI images (384×384 PNG)
│   ├── T1_0001_D3.png              # Axial T1, Patient 0001, L3-L4
│   ├── T2_0001_D5.png              # Axial T2, Patient 0001, L5-S1
│   ├── T1_0001_S8.png              # Sagittal T1, Patient 0001
│   └── ...
├── labels_yolo/                    # YOLO polygon annotations (.txt)
├── masks_indexed/                  # Semantic segmentation masks (.png)
├── overlay_visuals/                # Pre-rendered annotation overlays
├── PfirrmannGrade.csv              # Pfirrmann grades (515 × 3 discs)
├── IVDHeights.csv                  # Disc heights with coordinates
└── structured_notes.csv            # NLP-processed radiology reports
```

**File Naming Convention:**

| View | Pattern | Example |
|------|---------|---------|
| Axial | `{Modality}_{PatientID}_{DiscLevel}.png` | `T2_0042_D4.png` |
| Sagittal | `{Modality}_{PatientID}_S{SliceNumber}.png` | `T1_0042_S8.png` |

<p align="center">
  <img src="assets/Figure_02_multiview_comparison.png" alt="Multi-view Comparison" width="700">
</p>

---

## 6. Annotation Specifications

### YOLO Polygon Format

Each `.txt` label file contains one polygon per line:

```
<class_id> <x1> <y1> <x2> <y2> ... <xn> <yn>
```

All coordinates are normalised to [0, 1] relative to image dimensions.

### Semantic Segmentation Masks

Single-channel indexed PNG where pixel value = class ID:

| Pixel Value | Class (Axial) | Class (Sagittal) |
|:-----------:|:-------------:|:----------------:|
| 0 | Background | Background |
| 1 | IVD | -- |
| 2 | PE | -- |
| 3 | SC | -- |
| 4 | -- | VB |
| 5 | -- | IVD |
| 6 | -- | Sacrum |
| 7 | -- | SC |

<p align="center">
  <img src="assets/Figure_04_annotation_formats.png" alt="Annotation Formats" width="700">
</p>

**Loading example (Python):**

```python
import numpy as np
from PIL import Image

mask = np.array(Image.open("masks_indexed/T2_0042_D4.png"))
ivd_region = (mask == 1)  # Binary mask for IVD
```

---

## 7. Clinical Metadata

### 7.1 Pfirrmann Grades

**Grading scale** (assessed on T2-weighted MRI):

| Grade | MRI Characteristics |
|:-----:|---------------------|
| 1 | Homogeneous bright white IVD; normal height; clear nucleus/annulus boundary |
| 2 | Inhomogeneous with horizontal bands; normal height; visible nucleus/annulus distinction |
| 3 | Inhomogeneous gray IVD; normal to slightly decreased height; unclear nucleus/annulus boundary |
| 4 | Inhomogeneous dark gray; moderate height loss (30--40%); no nucleus/annulus distinction |
| 5 | Inhomogeneous black IVD; collapsed disc space (&gt;40% loss); no signal intensity |

<p align="center">
  <img src="assets/Figure_03_pfirrmann_grades.png" alt="Pfirrmann Grade Examples" width="700">
</p>

**Grade distribution** (*N* = 1,545 disc assessments across 515 patients):

| Grade | D3 (L3-L4) *n* (%) | D4 (L4-L5) *n* (%) | D5 (L5-S1) *n* (%) | Total *n* (%) |
|:-----:|:-------------------:|:-------------------:|:-------------------:|:-------------:|
| 1 | 10 (1.9) | 10 (1.9) | 3 (0.6) | 23 (1.5) |
| 2 | 341 (66.2) | 240 (46.6) | 252 (48.9) | 833 (53.9) |
| 3 | 94 (18.3) | 158 (30.7) | 124 (24.1) | 376 (24.3) |
| 4 | 63 (12.2) | 99 (19.2) | 112 (21.8) | 274 (17.7) |
| 5 | 7 (1.4) | 8 (1.6) | 24 (4.7) | 39 (2.5) |
| **Total** | **515** | **515** | **515** | **1,545** |

<p align="center">
  <img src="assets/Figure_05_pfirrmann_distribution.png" alt="Pfirrmann Distribution" width="700">
</p>

**Key findings:**
- Severe degeneration (Grades 4--5) increases caudally: 13.6% at L3-L4 to 26.4% at L5-S1 (&chi;&sup2;(2) = 27.8, *p* < 0.001)
- D5 (L5-S1) is the primary pathology driver in 71.5% of patients
- D4-D3 Pearson correlation: *r* = 0.556; D5-D4: *r* = 0.299
- Inter-rater agreement: &kappa;<sub>w</sub> = 0.83 (95% CI: 0.74--0.91)

### 7.2 IVD Height Measurements

Disc height is measured using a validated two-point methodology on T2-weighted mid-sagittal images (see [Section 4.4](#44-intervertebral-disc-height-measurement)).

<p align="center">
  <img src="assets/Figure_06A_ivd_measurement.png" alt="IVD Measurement" width="500">
</p>

**CSV structure** (`IVDHeights.csv`):

| Column | Description |
|--------|-------------|
| `Patient_ID` | Integer patient identifier |
| `D5_Ht` | L5-S1 disc height (mm) |
| `D4_Ht` | L4-L5 disc height (mm) |
| `D3_Ht` | L3-L4 disc height (mm) |
| `D5_Coord` | Endpoint coordinates: `top_x,top_y;bottom_x,bottom_y` |
| `D4_Coord` | Endpoint coordinates |
| `D3_Coord` | Endpoint coordinates |

<p align="center">
  <img src="assets/Figure_06B_ivd_distribution.png" alt="IVD Height Distribution" width="500">
</p>

**Summary statistics:**

| Level | Mean (mm) | Median (mm) | IQR (mm) | Severe (&lt;6 mm) |
|:-----:|:---------:|:-----------:|:--------:|:----------------:|
| D3 (L3-L4) | 9.72 | 9.72 | 2.42 | 3.1% |
| D4 (L4-L5) | 9.88 | -- | -- | 4.5% |
| D5 (L5-S1) | 9.00 | 9.16 | 3.05 | 11.3% |

**Inter-observer reliability** (*n* = 20 patients, 60 disc levels):
- ICC(2,1) = 0.94 (excellent)
- MAE = 0.31 mm (relative error 2.9%)
- Exceeds Frobin *et al.* clinical tolerance threshold of 4.15%

**Correlation**: Disc height vs. Pfirrmann grade: &rho;<sub>s</sub> = &minus;0.72 (*p* < 0.001)

<p align="center">
  <img src="assets/Figure_07_multipatient_ivd.png" alt="Multi-Patient IVD Heights" width="700">
</p>

### 7.3 Structured Radiological Reports

515 free-text radiology reports were processed through a five-stage NLP pipeline (see [Section 4.6](#46-clinical-report-processing-pipeline)):

1. Lexical standardisation and spell correction (340 errors in 59% of reports)
2. Phonetic matching (Double Metaphone)
3. Named Entity Recognition (8.7 &pm; 3.2 entities/report, 96.3% precision)
4. Severity quantification (4-level ordinal encoding)
5. Structured record assembly

**Pathology prevalence:**

| Pathology | Count | Prevalence |
|-----------|------:|:----------:|
| Disc compression/degeneration | 403 | 78.3% |
| Disc bulge (diffuse protrusion) | 277 | 53.8% |
| Paraspinal muscle spasm | 201 | 39.0% |
| Facet joint arthropathy | 156 | 30.3% |
| Disc herniation (focal extrusion) | 72 | 14.0% |
| Neural foraminal stenosis | 68 | 13.2% |
| Central canal stenosis | 45 | 8.7% |
| Endplate changes (Modic type I/II) | 34 | 6.6% |
| Annular fissure/tear | 28 | 5.4% |
| Spondylolisthesis (degenerative) | 19 | 3.7% |
| Ligamentum flavum hypertrophy | 17 | 3.3% |

**Laterality distribution:** Bilateral 24.7% | Left 17.3% | Right 14.4% | None 43.7%

---

## 8. Quality Assurance

| Validation Metric | Value |
|-------------------|-------|
| Cross-format IoU (YOLO vs. Mask) | 0.994 &pm; 0.008 |
| Pfirrmann inter-rater &kappa;<sub>w</sub> | 0.83 (95% CI: 0.74--0.91) |
| Disc height ICC(2,1) | 0.94 |
| Disc height MAE | 0.31 mm (2.9% relative) |
| Quantitative Pfirrmann accuracy | 92.3% (&kappa;<sub>w</sub> = 0.89) |
| Quantitative Pfirrmann 5-fold CV | 90.1 &pm; 1.8% (&kappa;<sub>w</sub> = 0.86 &pm; 0.03) |
| NLP correction accuracy | 98.8% |
| NER pattern precision | 96.3% |
| Spearman severity vs. Pfirrmann | &rho;<sub>s</sub> = 0.68 (*p* < 0.001) |
| Spearman disc height vs. Pfirrmann | &rho;<sub>s</sub> = &minus;0.72 (*p* < 0.001) |
| Total annotation effort | ~550 person-hours (488 annotation + 62 QA) |

---

## 9. Baseline Benchmarks

All experiments: NVIDIA RTX 4070 (8 GB), PyTorch 2.5.1, CUDA 12.1, seed = 42. Train/val/test split: 70%/15%/15%, stratified by patient ID. Detailed architecture descriptions and training configurations are documented in [`scripts/benchmarks/README.md`](scripts/benchmarks/README.md).

### 9.1 Multi-Plane Anatomical Segmentation

**Architecture**: YOLO11m backbone with multi-scale feature fusion; 54.1M total parameters, 17% trainable (frozen encoder).

| View | Class | Dice | IoU | Precision | Recall |
|------|-------|:----:|:---:|:---------:|:------:|
| Axial | IVD (c0) | 0.978 | 0.956 | 0.976 | 0.979 |
| Axial | PE (c1) | 0.935 | 0.878 | 0.936 | 0.935 |
| Axial | SC (c2) | 0.919 | 0.850 | 0.921 | 0.917 |
| | *Axial mean* | *0.944* | *0.895* | *0.944* | *0.944* |
| Sagittal | VB (c3) | 0.958 | 0.919 | 0.953 | 0.963 |
| Sagittal | IVD (c4) | 0.936 | 0.879 | 0.934 | 0.937 |
| Sagittal | Sacrum (c5) | 0.958 | 0.920 | 0.960 | 0.957 |
| Sagittal | SC (c6) | 0.939 | 0.884 | 0.941 | 0.936 |
| | *Sagittal mean* | *0.948* | *0.901* | *0.947* | *0.948* |
| **Overall** | | **0.946** | **0.898** | **0.946** | **0.946** |

### 9.2 Disc-Aware Pfirrmann Grading

**Architecture**: DINOv2 vision encoder + LoRA (r = 8) + ordinal regression head + disc-level positional embeddings; ~2.39M trainable parameters.

| Setting | *n* | Accuracy | &kappa;<sub>w</sub> | F1 (Weighted) |
|---------|----:|:--------:|:--------------------:|:-------------:|
| D3 (L3-L4), Test | 79 | 64.6% | 0.592 | 0.641 |
| D4 (L4-L5), Test | 83 | 44.6% | 0.379 | 0.451 |
| D5 (L5-S1), Test | 69 | 30.4% | 0.408 | 0.293 |
| **Overall, Test** | **231** | **47.2%** | **0.505** | **0.482** |
| Best Validation | -- | -- | **0.585** | -- |
| Ablation (non disc-aware) | -- | -- | 0.358 | -- |

> Disc-aware positional embeddings improve &kappa; by +63% over ablation baseline (0.358 &rarr; 0.585).
> Error analysis: 93% single-grade errors, 7% two-grade; Grade 2 &harr; 3 confusion accounts for 50% of errors.

### 9.3 Structured Clinical Findings Extraction

**Architecture**: ResNet-18 encoder + MultiDiscAggregator (4-head cross-attention) + multi-head classifiers; 12.28M parameters.

| Category | Metric | Score |
|----------|--------|:-----:|
| Global multi-label | Hamming Loss | 0.261 |
| | F1 (Macro) | 0.318 |
| | F1 (Micro) | 0.500 |
| | **F1 (Weighted)** | **0.585** |
| Auxiliary targets | L4-L5 Type Accuracy | 57.1% |
| | L5-S1 Type Accuracy | 66.2% |
| | Severity Accuracy | 54.5% |
| Top label-wise F1 | L4-L5 Involvement | 0.822 |
| | Thecal Sac Compression | 0.821 |
| | L4-L5 Compression | 0.796 |
| | Disc Bulge | 0.729 |
| | Disc Protrusion | 0.556 |

---

## 10. Research Applications

LSMA-PQR is designed to support the following research directions:

| Application | Description | Relevant Data |
|-------------|-------------|---------------|
| **Multi-plane segmentation** | Train and evaluate models that handle axial + sagittal views jointly | `images_png/`, `labels_yolo/`, `masks_indexed/` |
| **Degeneration classification** | Pfirrmann grade prediction from sagittal MRI | `PfirrmannGrade.csv`, sagittal images |
| **Disc height regression** | Predict quantitative disc heights from images | `IVDHeights.csv`, sagittal images |
| **Multi-view learning** | Fuse axial and sagittal features for improved pathology detection | All image data |
| **Report-guided supervision** | Use structured reports as weak supervisory signals for image models | `structured_notes.csv` |
| **Clinical cross-validation** | Validate imaging biomarkers against radiologist reports and quantitative measurements | All metadata CSVs |
| **Radiology NLP** | Develop and benchmark radiology NLP systems | `structured_notes.csv` |

### Utility for the Clinical Community

- **Surgical planning**: Quantitative disc height measurements with coordinate provenance inform disc replacement sizing and approach planning.
- **Longitudinal monitoring**: The severity classification framework provides standardised vocabulary for tracking degeneration progression across visits.
- **Radiology training**: Graded Pfirrmann examples (Grades 1--5) with corresponding T2-weighted imaging serve as a structured teaching resource.
- **Multi-metric cross-validation**: Imaging findings, degeneration grades, disc heights and clinical reports can be jointly validated, enabling integrated clinical decision support research.

---

## 11. Getting Started

### Requirements

```
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
Pillow>=10.0
scipy>=1.11
opencv-python>=4.8
```

Install:
```bash
pip install -r scripts/requirements.txt
```

### Quick Examples

**Browse images:**
```bash
python scripts/visualization/visualize_images.py --browse --sequence T2 --images_dir <path_to>/images_png
```

**View semantic masks:**
```bash
python scripts/visualization/visualize_semantic_masks.py --browse --sequence T2 \
    --images_dir <path_to>/images_png --masks_dir <path_to>/masks_indexed
```

**View YOLO annotations:**
```bash
python scripts/visualization/visualize_yolo_annotations.py --browse --sequence T2 \
    --images_dir <path_to>/images_png --labels_dir <path_to>/labels_yolo
```

**Load Pfirrmann grades:**
```python
import pandas as pd

grades = pd.read_csv("PfirrmannGrade.csv")
print(grades.describe())
# Columns: Patient_ID, D5, D4, D3 (grades 1-5)
```

**Load IVD heights:**
```python
heights = pd.read_csv("IVDHeights.csv")
print(f"Mean D5 height: {heights['D5_Ht'].mean():.2f} mm")
```

**PyTorch Dataset (segmentation):**
```python
from torch.utils.data import Dataset
from PIL import Image
import numpy as np
import torch
import glob

class LSMAPQRSegmentation(Dataset):
    def __init__(self, images_dir, masks_dir, transform=None):
        self.images = sorted(glob.glob(f"{images_dir}/*.png"))
        self.masks_dir = masks_dir
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = np.array(Image.open(self.images[idx]).convert("RGB"))
        stem = self.images[idx].rsplit("/", 1)[-1]
        mask = np.array(Image.open(f"{self.masks_dir}/{stem}"))
        if self.transform:
            transformed = self.transform(image=img, mask=mask)
            img, mask = transformed["image"], transformed["mask"]
        return (torch.from_numpy(img).permute(2, 0, 1).float() / 255.0,
                torch.from_numpy(mask).long())
```

---

## 12. Repository Structure

```
LSMA-PQR/
├── README.md                                   # This file
├── CITATION.cff                                # Machine-readable citation
├── LICENSE                                     # CC BY 4.0
├── .gitignore
│
├── assets/                                     # Figures for documentation
│   ├── Figure_01_dataset_overview_infographic.png
│   ├── Figure_02_multiview_comparison.png
│   ├── Figure_03_pfirrmann_grades.png
│   ├── Figure_04_annotation_formats.png
│   ├── Figure_05_pfirrmann_distribution.png
│   ├── Figure_06A_ivd_measurement.png
│   ├── Figure_06B_ivd_distribution.png
│   └── Figure_07_multipatient_ivd.png
│
├── scripts/
│   ├── requirements.txt                        # Python dependencies
│   ├── visualization/                          # Dataset exploration tools
│   │   ├── visualize_images.py                 # MRI image browser
│   │   ├── visualize_semantic_masks.py         # Mask overlay viewer
│   │   └── visualize_yolo_annotations.py       # YOLO bbox viewer
│   │
│   ├── ivd_height/                             # IVD height extraction pipeline
│   │   ├── README.md                           # Pipeline documentation
│   │   ├── inspect_mat_structure.py            # .mat file structure inspector
│   │   ├── convert_mat_to_csv.py               # Batch .mat → CSV extraction
│   │   ├── verify_csv.py                       # CSV integrity verification
│   │   ├── resolve_duplicates.py               # Duplicate Patient_ID resolution
│   │   ├── merge_manual_measurements.py        # JSON manual measurement merge
│   │   ├── validate_corrected.py               # Final 515-patient validation
│   │   └── visualize_ivd_heights.py            # Measurement overlay visualisation
│   │
│   ├── pfirrmann_grading/                      # Pfirrmann grading pipeline
│   │   ├── README.md                           # Pipeline documentation
│   │   ├── convert_mat_to_csv.py               # .mat → CSV conversion
│   │   ├── add_patient_id.py                   # Patient_ID column injection
│   │   ├── pfirrmann_validator.py              # Interactive validation GUI
│   │   └── analyze_grades.py                   # Statistical analysis
│   │
│   └── benchmarks/                             # Baseline experiment documentation
│       └── README.md                           # Architecture and training details
│
└── docs/
    └── DATASET_CARD.md                         # Formal dataset documentation card
```

---

## 13. Limitations

1. **Class imbalance**: Pfirrmann Grades 1 and 5 are scarce (1.5% and 2.5%, respectively); augmentation or class-balanced sampling is recommended.
2. **Single centre**: All data are from a single imaging centre; scanner-specific biases may limit direct generalisability without domain adaptation.
3. **Symptomatic cohort**: Patients were consecutive symptomatic cases (low back pain, radiculopathy); the distribution does not represent the general population.
4. **Cross-sectional**: No longitudinal follow-up; temporal progression cannot be modelled from this data.
5. **2D slices**: Single mid-sagittal slice per patient constrains volumetric modelling.
6. **Demographics**: Granular demographics (age, sex, BMI) are unavailable from the original anonymised DICOM archive.
7. **Low-prevalence entities**: Pathologies with &lt;10% prevalence yield near-zero F1 in current findings extraction models.

---

## 14. Citation

If you use LSMA-PQR in your research, please cite:

```bibtex

@article{Masood2026LSMAPQR,
  author       = {Masood, Rao Farhat and Taj, Imtiaz Ahmad},
  title        = {LSMA-PQR: A Comprehensive Dataset of Lumbar Spine Multi-View Annotations with Pfirrmann Grading, Quantitative Measurements, and Structured Radiological Reports},
  journal      = {Journal of Imaging Informatics in Medicine},
  year         = {2026},
  publisher    = {Springer},
  doi          = {10.1007/s10278-026-02125-5},
  url          = {https://doi.org/10.1007/s10278-026-02125-5}
}

@dataset{Masood2025LSMA_PQR,
  author       = {Masood, Rao Farhat and Taj, Imtiaz Ahmad and Talha, Muhammad and Khan, M. Babar},
  title        = {LSMA-PQR: Lumbar Spine Multi-view Annotations with Pfirrmann grading, Quantitative measurements and structured Radiological reports},
  year         = {2025},
  publisher    = {Mendeley Data},
  version      = {V2},
  doi          = {10.17632/p3r4xd2488.2},
  url          = {https://doi.org/10.17632/p3r4xd2488.2}
}
```

---

## 15. License

This dataset and all accompanying code are released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to share and adapt the material for any purpose, including commercial use, provided appropriate credit is given.

---
<!-- 
## 16. Authors

| Author | Affiliation | Role |
|--------|-------------|------|
| **Rao Farhat Masood** | Dept. of ECE, Capital University of Science and Technology, Islamabad | Conceptualisation, Methodology, Software, Data Curation |
| **Imtiaz Ahmad Taj** | Dept. of ECE, Capital University of Science and Technology, Islamabad | Supervision, Formal Analysis, Project Administration |
| **Muhammad Babar Khan** | Dept. of Radiology, Combined Military Hospital, Kharian | Clinical Validation, Radiological Grading & Reporting |
| **Muhammad Asad Qureshi** | Dept. of Spinal Surgery, Bahria International Hospital, Rawalpindi | Clinical Validation, Investigation |
| **Muhammad Talha** | Dept. of Spinal Surgery, Combined Military Hospital, Rawalpindi | Clinical Validation, Grading & Spinal Measurements |

**Corresponding Author**: Rao Farhat Masood ([farhatmasood.fm@gmail.com](mailto:farhatmasood.fm@gmail.com)) | ORCID: [0000-0001-9054-9192](https://orcid.org/0000-0001-9054-9192) -->
