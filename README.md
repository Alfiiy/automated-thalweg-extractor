# Terrain Analysis Pipeline

A Python-based CLI tool for automated DEM processing, roughness calculation, and D8 thalweg extraction using GDAL and NumPy vectorization.

## 📂 Project Structure

This project follows a strict **Modular Object-Oriented Design**:

    terrain-analysis-pipeline/
    ├── environment.yml            # Reproducible Conda environment
    ├── src/
    │   ├── terrain_pipeline/      # Core Algorithm Package
    │   │   ├── __init__.py
    │   │   ├── aoi.py             # Bounds validation & Area checks
    │   │   ├── processor.py       # Base class for GDAL I/O & Reprojection
    │   │   └── ... (modules in development)
    │   └── main_test.py           # CLI Entry point (Prototype)
    ├── data/                      # Raw inputs (ignored by Git)
    └── results/                   # Processed outputs (ignored by Git)

Here is a clean, professionally formatted version of your README. I have optimized the hierarchy, used standard Markdown code blocks that are easy to copy-paste, and improved the visual flow while keeping it entirely in English.

Terrain Analysis Pipeline
A robust framework for geographic data processing with built-in validation and reproducibility.

# 🛠️ Installation & Setup

To ensure reproducibility (Requirement F1) and proper GDAL bindings, please follow these steps:

### 1. Clone the repository
```bash
git clone <repository-url>
cd terrain-analysis-pipeline
```

### 2. Create the environment
```bash
conda env create -f environment.yml
```

### 3. Activate the environment
```bash
conda activate terrain_pipeline
```

## 🚀 Usage

### 1. Data Validation

The system currently supports strict AOI (Area of Interest) validation to prevent excessive server load and ensure data integrity.
```python
from terrain_pipeline.aoi import AOIValidator

# Example: Validate a bounding box
try:
    validator = AOIValidator("7.0,50.0,7.1,50.1")
    bbox = validator.validate()
    print(f"Processing region: {bbox}")
except ValueError as e:
    print(f"Error: {e}")
```

### 2. Architecture Overview

The pipeline is built on modular components designed for stability:

- **AOIValidator**: Enforces geographic limits and area caps (maximum 100 km²).
- **BaseRasterProcessor**: Handles safe loading of GeoTIFFs and enforces memory management during large-scale processing.

## 📅 Roadmap

- [x] Phase 1: Environment Setup & Modular Scaffolding (Completed)
- [ ] Phase 2: Automated API Data Pipeline (In Progress)
- [ ] Phase 3: Core Hydro-Algorithms (Upcoming)

## 📄 License

This project is licensed under the MIT License.
