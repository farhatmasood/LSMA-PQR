# Dataset Card: LSMA-PQR

## Dataset Description

- **Name**: LSMA-PQR (Lumbar Spine Multi-view Annotations with Pfirrmann Grading, Quantitative Measurements and Structured Radiological Reports)
- **Version**: 1.0
- **Homepage**: [https://data.mendeley.com/datasets/p3r4xd2488/1](https://data.mendeley.com/datasets/p3r4xd2488/1)
- **Repository**: [https://github.com/farhatmasood/LSMA-PQR](https://github.com/farhatmasood/LSMA-PQR)
- **DOI**: [10.17632/p3r4xd2488.1](https://doi.org/10.17632/p3r4xd2488.1)
- **License**: CC BY 4.0
- **Size**: ~2.59 GB (compressed)

## Dataset Summary

LSMA-PQR is a clinically validated lumbar spine MRI dataset containing 4,120 images from 515 symptomatic patients. It integrates pixel-level segmentation annotations for 7 anatomical structures, 1,545 Pfirrmann degeneration grades, quantitative IVD height measurements with pixel-coordinate provenance, and 515 structured radiology reports. Annotations are provided in multiple formats (YOLO polygon + semantic masks) with verified spatial consistency (mean IoU = 0.994).

## Languages

English (structured reports and metadata).

## Dataset Structure

### Data Instances

Each patient contributes 8 images: 6 axial (3 disc levels x 2 modalities) and 2 sagittal (1 mid-sagittal slice x 2 modalities), each at 384 x 384 resolution.

### Data Fields

**Images**: 384 x 384 PNG, grayscale MRI
**Labels (YOLO)**: Normalised polygon coordinates per class
**Masks**: Single-channel indexed PNG (pixel value = class ID)
**PfirrmannGrade.csv**: Patient_ID, D5, D4, D3 (grades 1-5)
**IVDHeights.csv**: Patient_ID, D5_Ht, D4_Ht, D3_Ht (mm), D5_Coord, D4_Coord, D3_Coord
**structured_notes.csv**: Binary pathology labels, disc types, severity, laterality

### Data Splits

Recommended: 70% train / 15% validation / 15% test, stratified by patient ID with seed = 42.

## Dataset Creation

### Source Data

Original DICOM archive from Sudirman *et al.* (single-centre, consecutive symptomatic patients). From 575 original studies, 60 were excluded (28 incomplete series, 19 motion artefacts, 13 non-standard protocols), yielding 515 patients.

### Annotations

- **Tool**: MATLAB R2025a Image Labeler Application
- **Annotators**: 2 expert annotators (radiologist + spinal surgeon)
- **Effort**: ~550 person-hours (488 annotation + 62 QA)
- **Throughput**: 3.3 min/axial image, 18.5 min/sagittal image

### Clinical Validation

- Pfirrmann inter-rater kappa: 0.83 (95% CI: 0.74-0.91)
- IVD height ICC(2,1): 0.94; MAE: 0.31 mm
- NLP spell-correction accuracy: 98.8%
- NER precision: 96.3%

## Considerations

### Social Impact

This dataset supports research toward automated lumbar spine analysis, which may improve diagnostic efficiency and reduce radiologist workload. However, it should not be used as a standalone diagnostic tool.

### Biases

- Single imaging centre (potential scanner-specific bias)
- Symptomatic cohort only (no healthy controls)
- Demographics unavailable (age, sex, BMI)
- Class imbalance in Pfirrmann grades (Grade 2 dominant at 53.9%)

### Limitations

- Cross-sectional design (no longitudinal data)
- 2D slices only (single mid-sagittal per patient)
- Low-prevalence pathologies are underrepresented

## Citation

```bibtex
@article{masood2025lsmapqr,
  title   = {{LSMA-PQR}: A Comprehensive Dataset of Lumbar Spine Multi-view
             Annotations with {Pfirrmann} Grading, Quantitative Measurements
             and Structured Radiological Reports},
  author  = {Masood, Rao Farhat and Taj, Imtiaz Ahmad and Khan, Muhammad Babar
             and Qureshi, Muhammad Asad and Talha, Muhammad},
  journal = {Artificial Intelligence in Medicine},
  year    = {2025},
  doi     = {10.17632/p3r4xd2488.1}
}
```
