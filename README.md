# Terrain Analysis Pipeline

A Python-based CLI tool for automated DEM processing, roughness calculation, and D8 thalweg extraction using GDAL and NumPy vectorization.

## 📂 Project Structure

This project follows a strict **Modular Object-Oriented Design**:

```text
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

🛠️ Installation & Setup
To ensure reproducibility (Requirement F1) and proper GDAL bindings:

Clone the repository:

Bash
git clone <your-repo-url>
cd terrain-analysis-pipeline
Create the Environment: Run the following command to install dependencies (GDAL, NumPy, etc.):

Bash
conda env create -f environment.yml
Activate:

Bash
conda activate terrain_pipeline
🚀 Usage
1. Data Validation (Current Capability)
The system currently supports strict AOI (Area of Interest) validation to prevent excessive server load.

Python
from terrain_pipeline.aoi import AOIValidator

# Example: Validate a bounding box
try:
    validator = AOIValidator("7.0,50.0,7.1,50.1")
    bbox = validator.validate()
    print(f"Processing region: {bbox}")
except ValueError as e:
    print(f"Error: {e}")
2. Architecture Overview
AOIValidator: Enforces geographic limits and area caps (100 km²).

BaseRasterProcessor: Handles safe loading of GeoTIFFs and enforces memory management.

📅 Roadmap
[x] Phase 1: Environment Setup & Modular Scaffolding (Completed)

[ ] Phase 2: Automated API Data Pipeline (In Progress)

[ ] Phase 3: Core Hydro-Algorithms (Upcoming)

📄 License
MIT License
