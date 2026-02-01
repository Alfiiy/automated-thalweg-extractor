import argparse
import sys
import os

# Add 'src' to the system path so Python can find the 'terrain_pipeline' package
# This is necessary because the code is in a subdirectory
sys.path.append(os.path.join(os.getcwd(), "src"))

# Import modules strictly using the full path (since __init__.py is empty)
from terrain_pipeline.aoi import AOIValidator
from terrain_pipeline.processor import BaseRasterProcessor
from terrain_pipeline.dem import DEMFetcher
from terrain_pipeline.landcover import LandCoverFetcher
from terrain_pipeline.roughness import RoughnessCalculator

def main():
    """
    Main entry point for the Terrain Analysis CLI.
    """
    # 1. Setup Command Line Interface
    parser = argparse.ArgumentParser(
        description="Terrain Analysis Pipeline: Download DEM, calculate roughness, and extract hydro features."
    )
    
    parser.add_argument(
        "--bbox", 
        type=str, 
        required=True, 
        help="Bounding Box in 'min_lon,min_lat,max_lon,max_lat' format (e.g., '7.0,50.0,7.1,50.1')"
    )

    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="OpenTopography API key"
    )
    
    args = parser.parse_args()

    print("--- Starting Terrain Analysis Pipeline ---")

    # 2. Validate Input (The 'Gatekeeper')
    try:
        print(f"[STEP 1] Validating AOI: {args.bbox}")
        validator = AOIValidator(args.bbox)
        validated_bbox = validator.validate()
        print(f"✅ AOI Accepted: {validated_bbox}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # 3. Handover Point for Teammate
    # TODO: temporary working directory, we should pass this as a commandline argument
    temp_working_dir = os.path.join(os.getcwd(), "results")

    try:
        # download DEM and landcover rasters into working directory
        dem_path = DEMFetcher(validated_bbox, "NASADEM", "GTiff", args.api_key, temp_working_dir).get_dem()
        landcover_path = LandCoverFetcher(validated_bbox, temp_working_dir).get_land_cover()
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    try:
        # set up output paths for the reprojected rasters and the roughness raster
        dem_path_reprojected = os.path.join(temp_working_dir, "dem_reprojected.tif")
        landcover_path_reprojected = os.path.join(temp_working_dir, "landcover_reprojected.tif")
        roughness_path = os.path.join(temp_working_dir, "roughness.tif")

        # reproject DEM and landcover rasters
        dem = BaseRasterProcessor(dem_path)
        dem.reproject(32632, dem_path_reprojected)

        landcover = BaseRasterProcessor(landcover_path)
        landcover.reproject(32632, landcover_path_reprojected)
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    try:
        # generate roughness raster
        roughness_processor = RoughnessCalculator(landcover_path_reprojected)
        roughness_processor.from_landcover(roughness_path)
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    print("[INFO] Phase 2 checks complete. Waiting for Phase 3 (Data Pipeline) implementation.")

if __name__ == "__main__":
    main()
