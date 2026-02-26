# Data Sources and Licenses

This project relies on automated API retrieval for geospatial data. Raw files are not tracked in Git due to size limits, but are dynamically fetched via the pipeline.

## 1. Topographic Data (NASADEM)
* **Source:** OpenTopography API
* **Resolution:** 30m (SRTM-derived)
* **License:** Public Domain
* **Retrieval Method:** Automated via `src/terrain_pipeline/processor.py` (GeoTiff format)

## 2. Land Cover Data (ESA WorldCover 2021)
* **Source:** OpenTopography API / European Space Agency (ESA)
* **Resolution:** 10m
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Retrieval Method:** Automated via `src/terrain_pipeline/landcover.py` (GeoTiff format)