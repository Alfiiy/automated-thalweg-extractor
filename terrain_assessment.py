import argparse
import sys
import os

# Add 'src' to the system path so Python can find the 'terrain_pipeline' package
# This is necessary because the code is in a subdirectory
sys.path.append(os.path.join(os.getcwd(), "src"))

# Import modules strictly using the full path (since __init__.py is empty)
from terrain_pipeline.aoi import AOIValidator
from terrain_pipeline.processor import BaseRasterProcessor

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
    # ---------------------------------------------------------
    # TODO: [Ayan] Insert your DEM download logic here.
    # Use the 'validated_bbox' variable from above.
    # Example:
    #   dem_path = DEMFetcher(validated_bbox).download()
    #   processor = BaseRasterProcessor(dem_path)
    #   processor.reproject(target_epsg=32632, output_path="...")
    # ---------------------------------------------------------
    print("[INFO] Phase 1 checks complete. Waiting for Phase 2 (Data Pipeline) implementation.")

if __name__ == "__main__":
    main()