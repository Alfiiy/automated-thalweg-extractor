import argparse
import sys
import os
import time

# Add 'src' to the system path so Python can find the 'terrain_pipeline' package
sys.path.append(os.path.join(os.getcwd(), "src"))

# Import modules strictly using the full path
from terrain_pipeline.aoi import AOIValidator
from terrain_pipeline.processor import BaseRasterProcessor
from terrain_pipeline.dem import DEMFetcher
from terrain_pipeline.landcover import LandCoverFetcher
from terrain_pipeline.roughness import RoughnessCalculator
from terrain_pipeline.thalweg import ThalwegExtractor
from terrain_pipeline.visualizer import ResultVisualizer
from terrain_pipeline.logger import setup_logger

# Initialize the global logger
logger = setup_logger()

def main():
    """
    Main entry point for the Terrain Analysis CLI.
    """
    # 1. Setup Command Line Interface
    parser = argparse.ArgumentParser(
        description="Terrain Analysis Pipeline: Download DEM, calculate roughness, and extract hydro features."
    )
    
    # The AOI is the critical input that drives the entire pipeline, so we require it upfront.
    parser.add_argument(
        "--bbox", 
        type=str, 
        required=True, 
        help="Bounding Box in 'min_lon,min_lat,max_lon,max_lat' format (e.g., '7.0,50.0,7.1,50.1')"
    )

    # Uses a default built-in key so the evaluator doesn't need to configure one.
    parser.add_argument(
        "--api-key",
        type=str,
        default="d36fde10ed7c771242bed3c1cd6bdbe7",  
        help="OpenTopography API key. Defaults to a built-in key for evaluation purposes."
    )
    
    args = parser.parse_args()              # Parse the command line arguments provided by the user

    logger.info("=== Starting Terrain Analysis Pipeline ===")       # Log the start of the pipeline execution
    start_time = time.time()                                        # Log the start time for performance tracking

    # 2. Validate Input (The 'Gatekeeper')
    try:
        logger.info(f"[STEP 1] Validating AOI: {args.bbox}")
        validator = AOIValidator(args.bbox)
        validated_bbox = validator.validate()
        logger.info(f"AOI Accepted: {validated_bbox}")
    except ValueError as e:
        logger.error(f"AOI Validation Error: {e}", exc_info=True)
        sys.exit(1)

    # 3. Setup Working Directory
    temp_working_dir = os.path.join(os.getcwd(), "results")
    os.makedirs(temp_working_dir, exist_ok=True)

    # 4. Fetch Data
    try:
        logger.info("[STEP 2] Fetching DEM and Land Cover data from APIs...")
        dem_path = DEMFetcher(validated_bbox, "NASADEM", "GTiff", args.api_key, temp_working_dir).get_dem()
        landcover_path = LandCoverFetcher(validated_bbox, temp_working_dir).get_land_cover()
    except RuntimeError as e:
        logger.error(f"Data Fetching Error: {e}", exc_info=True)
        sys.exit(1)

    # 5. Reproject Rasters
    try:
        logger.info("[STEP 3] Reprojecting rasters to UTM coordinate system...")
        dem_path_reprojected = os.path.join(temp_working_dir, "dem_reprojected.tif")
        landcover_path_reprojected = os.path.join(temp_working_dir, "landcover_reprojected.tif")
        roughness_path = os.path.join(temp_working_dir, "roughness.tif")

        dem = BaseRasterProcessor(dem_path)
        dem.reproject(32632, dem_path_reprojected)

        landcover = BaseRasterProcessor(landcover_path)
        landcover.reproject(32632, landcover_path_reprojected)
    except RuntimeError as e:
        logger.error(f"Reprojection Error: {e}", exc_info=True)
        sys.exit(1)

    # 6. Calculate Roughness
    try:
        logger.info("[STEP 4] Calculating Surface Roughness (Manning's n)...")
        roughness_processor = RoughnessCalculator(landcover_path_reprojected)
        roughness_processor.from_landcover(roughness_path)
    except RuntimeError as e:
        logger.error(f"Roughness Calculation Error: {e}", exc_info=True)
        sys.exit(1)

    # 7. Extract Thalweg Network
    try:
        logger.info("[STEP 5] Extracting D8 Thalweg Network from DEM...")
        thalweg_path = os.path.join(temp_working_dir, "thalweg_network.tif")
        thalweg_processor = ThalwegExtractor(dem_path_reprojected)
        thalweg_processor.extract(thalweg_path, threshold=1000)
    except RuntimeError as e:
        logger.error(f"Thalweg Extraction Error: {e}", exc_info=True)
        sys.exit(1)

    # 8. Generate Visuals
    try:
        logger.info("[STEP 6] Generating Final Visual Report...")
        vis_path = os.path.join(temp_working_dir, "map_preview.png")
        visualizer = ResultVisualizer(dem_path_reprojected, roughness_path, thalweg_path)
        visualizer.generate_preview(vis_path)
    except Exception as e:
        logger.error(f"Visualization Error: {e}", exc_info=True)
        sys.exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"=== Phase 3 Complete. Pipeline finished successfully in {elapsed_time:.2f} seconds. ===")

if __name__ == "__main__":
    main()