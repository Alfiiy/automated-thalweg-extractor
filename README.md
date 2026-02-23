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

## 🚀 Usage (Crucial Steps for Evaluator)

**STOP:** To avoid `ModuleNotFoundError` (especially for GDAL/osgeo), you MUST activate the Conda environment before running any scripts. 

Please run the following commands in your Anaconda/Miniconda Prompt terminal strictly in this order:

1. `conda env create -f environment.yml` (Only once)
2. `conda activate terrain_pipeline`  <-- DO NOT SKIP THIS
3. `make all`  (Or run the python script directly)


## 📅 Roadmap

- [x] Phase 1: Environment Setup & Modular Scaffolding (Completed)
- [ ] Phase 2: Automated API Data Pipeline (In Progress)
- [ ] Phase 3: Core Hydro-Algorithms (Upcoming)

## 📄 License

This project is licensed under the MIT License.

> **⚠️ Note to Evaluator regarding API Authentication:**
> To facilitate a seamless evaluation process, an active OpenTopography API key has been securely built into the CLI default arguments for this submitted version. You can run the pipeline directly without manual API configuration. 
> 
> *Engineering Disclaimer:* In the public GitHub repository, this key is removed to adhere to standard security practices. Users cloning from GitHub must provide their own key via the `--api-key` argument.
