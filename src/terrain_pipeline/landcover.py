import geopandas as gpd
import requests
import os
import gc

from datetime import datetime
from shapely.geometry import box
from typing import Tuple
from terrain_pipeline.processor import BaseRasterProcessor


class LandCoverFetcher:
    """
    Downloads ESA WorldCover data for a specified bounding box, 
    merges the required tiles, and clips the result to the exact AOI.
    """
    def __init__(self, valid_aoi: Tuple[float, float, float, float], output_dir: str):
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = valid_aoi
        self.output_dir = output_dir

    def get_land_cover(self) -> str:
        """
        Executes the download, merge, and clip operations.
        Returns the path to the final clipped raster.
        """
        print("[LandCoverFetcher] Downloading land cover data from esa-worldcover.org ...")
        start_time = datetime.now()

        s3_url_prefix = "https://esa-worldcover.s3.eu-central-1.amazonaws.com"

        try:
            grid = gpd.read_file(f"{s3_url_prefix}/esa_worldcover_grid.geojson")
        except Exception as e:
            raise RuntimeError(f"An exception occured while downloading the resource "
                               f"{s3_url_prefix}/esa_worldcover_grid.geojson : \n", e)

        bounding_box = gpd.GeoSeries([box(self.min_lon, self.min_lat, self.max_lon, self.max_lat)])
        tiles = grid[grid.intersects(bounding_box.union_all())]

        year = 2021
        version = {2020: "v100", 2021: "v200"}[year]

        temp_dir = os.path.join(self.output_dir, "temp")

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        successful_files = []

        print(f"[LandCoverFetcher] {len(tiles.ll_tile)} tiles to download...")

        for tile in tiles.ll_tile:
            url = f"{s3_url_prefix}/{version}/{year}/map/ESA_WorldCover_10m_{year}_{version}_{tile}_Map.tif"
            print(f"GET {url}")

            try:
                response = requests.get(url, allow_redirects=True, stream=True)
                output_filename = os.path.join(temp_dir, f"{tile}.tif")

                with open(output_filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=128):
                        f.write(chunk)

            except Exception as e:
                raise RuntimeError(f"An exception occurred while downloading the resource {url} :\n", e)

            successful_files.append(output_filename)

        end_time = datetime.now()
        print(f"Downloaded {len(tiles.ll_tile)} files in {(end_time - start_time).total_seconds()} seconds")

        merged_output_filename = os.path.join(temp_dir, "merged.tif")
        try:
            BaseRasterProcessor.merge(
                temp_dir,
                successful_files,
                merged_output_filename
            )
        except RuntimeError as e:
            raise RuntimeError("LandCoverFetcher: ", e)

        clipped_output_filename = os.path.join(self.output_dir, "landcover.tif")

        merged_landcover = BaseRasterProcessor(merged_output_filename)
        try:
            merged_landcover.clip(
                (self.min_lon, self.min_lat, self.max_lon, self.max_lat),
                clipped_output_filename
            )
        except RuntimeError as e:
            raise RuntimeError("LandCoverFetcher: ", e)

        # ==============================================================
        # Explicit Memory Release to prevent Windows WinError 32
        # ==============================================================
        # 1. Manually release the GDAL dataset lock
        merged_landcover.close()
        
        # 2. Delete the Python instance reference
        del merged_landcover
        
        # 3. Force garbage collection to clear underlying C++ pointers
        gc.collect()
        # ==============================================================

        # Cleanup temp files
        try:
            for f in successful_files:
                os.remove(f)
            os.remove(merged_output_filename)
            os.rmdir(temp_dir)

        except OSError as e:
            # Fallback exception handling
            print(f"LandCoverFetcher: failed to remove files from {temp_dir} :\n", e)

        return clipped_output_filename