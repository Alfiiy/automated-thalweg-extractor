import requests
import os
from typing import Tuple
from datetime import datetime


class DEMFetcher:
    """
    TODO: add documentation
    """
    def __init__(self, valid_aoi: Tuple[float, float, float, float], dem_type: str, output_format: str, api_key: str, output_dir: str):
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = valid_aoi
        self.dem_type = dem_type
        self.output_format = output_format
        self.api_key = api_key
        self.output_dir = output_dir

    def get_dem(self) -> str:
        """
        TODO: add documentation
        """
        print(f"[DEMFetcher] Downloading DEM from OpenTopography...")
        start_time = datetime.now()

        url = "https://portal.opentopography.org/API/globaldem"

        querystring = {
            "demtype": self.dem_type,
            "south": str(self.min_lat),
            "north": str(self.max_lat),
            "west": str(self.min_lon),
            "east": str(self.max_lon),
            "outputFormat": self.output_format,
            "API_Key": self.api_key
        }

        output_path = os.path.join(self.output_dir, "dem.tif")

        try:
            response = requests.get(url, params=querystring, stream=True)

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)

        except Exception as e:
            raise RuntimeError("Unable to complete get request or save raster file:\n", e)

        end_time = datetime.now()
        print(f"Saved 1 file in {(end_time - start_time).total_seconds()} seconds")
        print(f"Output saved to: {output_path}")

        return output_path
