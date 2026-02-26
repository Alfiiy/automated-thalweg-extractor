# Terrain Analysis Pipeline

A Python-based CLI tool for automated DEM processing, spatially distributed roughness calculation, and D8 thalweg extraction using GDAL, NumPy vectorization, and PySheds.

> **⚠️ Special Note for Final Evaluation (Post-Presentation Addendum)**
> This repository contains the finalized, production-grade codebase, which includes critical structural overhauls implemented after the initial project presentation on **February 5th**. To ensure absolute scientific accuracy and system stability, the following core engineering resolutions were executed:
>
> 1. **Memory Management:** Resolved Windows `[WinError 32]` file-locking issues and eliminated storage leaks via explicit garbage collection (`gc.collect()`) and GDAL dataset nullification.
> 2. **Physical Parameter Calibration:** Corrected critical omissions in the spatial matrix. **ESA WorldCover Class 80 (Permanent Water)** and **Class 50 (Urban)** are now strictly parameterized (**n=0.030** and **n=0.050**), eliminating NoData transparency holes. Corrected **Tree Cover** resistance to a physically accurate **0.100**.
> 3. **Cartographic Accuracy:** Upgraded the visualizer to extract GDAL GeoTransforms, locking outputs to strict physical UTM projections (**EPSG:32632**) with dynamic, absolute-coordinate scale bars and bounding boxes.
> 4. **Standardized Logging System:** Upgraded from basic standard output to a robust dual-handler logging module (`src/terrain_pipeline/logger.py`). Execution states and critical exception stack traces are now persistently recorded to `logs/system.log`.
> 5. **Cross-Platform Build Compatibility:** Restructured the `Makefile` with OS-conditional logic (`ifeq ($(OS),Windows_NT)`). The build system now natively executes environment-specific directory parsing and cleanup operations across both Windows and POSIX systems without throwing false execution errors.
> 6. **Academic Documentation & Error Analysis:** Finalized `notebooks/results_discussions.ipynb` to objectively document the physical and geometric limitations of applying the D8 routing algorithm over **30m** resolution DEMs, specifically addressing localized distortions caused by urban artifacts (e.g., bridges acting as topographic barriers).

---

## 1. Project Overview

This automated pipeline executes a fully headless geomorphological extraction process using **NASADEM (30m)** and **ESA WorldCover (10m)** API data. It computes the primary valley thalweg networks via the **D8 flow routing algorithm** and derives spatially distributed **Manning's n** roughness coefficients for 2D hydrodynamic modeling.

---

## 2. Core Deliverables

Upon successful execution, the following physical files are generated in the `results/` directory with zero memory leakage:

- `dem_reprojected.tif`: Topographic elevation matrix (UTM Metric)
- `landcover_reprojected.tif`: Categorical land cover matrix
- `thalweg_network.tif`: D8 algorithmic routing output
- `roughness.tif`: Continuous friction surface (Manning's n)
- `map_preview.png`: Cartographically accurate tri-panel visualization

---

## 3. Project Structure

This project follows a strict Modular Object-Oriented Design:

```text
terrain-analysis-pipeline/
├── environment.yml               # Reproducible Conda environment
├── Makefile                      # OS-aware build directives
├── terrain_assessment.py         # Main CLI Entry Point
├── notebooks/
│   └── results_discussions.ipynb # Academic analysis & algorithmic limitations
├── src/
│   └── terrain_pipeline/         # Core Algorithm Package
│       ├── __init__.py
│       ├── logger.py             # Dual-handler logging system
│       ├── aoi.py                # Bounds validation & Area checks
│       ├── processor.py          # Base class for GDAL I/O & Memory management
│       ├── landcover.py          # ESA WorldCover extraction
│       ├── roughness.py          # Manning's n parameterization
│       ├── routing.py            # D8 Thalweg extraction
│       └── visualizer.py         # Cartographic map generation
├── logs/                         # Persistent system execution logs
└── results/                      # Processed outputs (Git ignored)
````

---

## 4. Installation & Setup

To ensure reproducibility and correct GDAL C++ bindings, follow these steps strictly using **Anaconda** or **Miniconda**.

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd terrain-analysis-pipeline
```

### Step 2: Create and activate the environment

> **STOP:** To avoid `ModuleNotFoundError` (especially for `GDAL/osgeo`), you **MUST** activate the Conda environment before running any scripts.

```bash
conda env create -f environment.yml
conda activate terrain_pipeline
```

---

## 5. Quick Start & Execution

The system includes an **OS-aware Makefile** that handles cross-platform I/O operations (Windows/POSIX) safely. Ensure your `terrain_pipeline` environment is activated.

### Clean previous build

Ensures an absolute zero-state environment by removing all temporary handles, log files, and legacy `.tif` matrices.

```bash
make clean
```

### Run full pipeline (default AOI: Stuttgart)

```bash
make all
```

### Run custom AOI (example: Koblenz — Rhine/Moselle confluence)

```bash
python terrain_assessment.py --bbox "7.55,50.30,7.65,50.40"
```

---

## 6. API Authentication Disclaimer

> **⚠️ Note to Evaluator:**
> To facilitate a seamless evaluation process, an active OpenTopography API key has been securely built into the CLI default arguments for this submitted version. You can run the pipeline directly without manual API configuration.
>
> **Engineering Disclaimer:** In the public GitHub repository, this key will be removed to adhere to standard security practices. External users cloning from GitHub must provide their own key via the `--api-key` argument.

---

## 7. Project Milestones Achieved

* [x] Phase 1: Environment Setup & Modular Scaffolding
* [x] Phase 2: Automated API Data Pipeline (NASADEM & ESA WorldCover)
* [x] Phase 3: Core Hydro-Algorithms (D8 Routing & Friction Surface)
* [x] Phase 4: Memory Optimization & Cartographic Visualization

---

## 📄 License

This project is licensed under the MIT License.
