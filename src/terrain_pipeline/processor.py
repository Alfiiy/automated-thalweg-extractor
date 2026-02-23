import os
from osgeo import gdal, osr
from typing import List, Tuple


class BaseRasterProcessor:
    """
    Base class that defines the contract for all raster operations.
    Zijun Zhang enforces standard I/O and CRS handling here.
    """

    def __init__(self, input_path: str):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Enforce Error Handling
        gdal.UseExceptions()
        
        self.input_path = input_path
        self.ds = gdal.Open(input_path, gdal.GA_ReadOnly)
        if self.ds is None:
            raise RuntimeError(f"Could not open {input_path}")

    def get_raster_data(self):
        """Standard method to fetch array data."""
        band = self.ds.GetRasterBand(1)
        return band.ReadAsArray(), band.GetNoDataValue(), self.ds.GetGeoTransform(), self.ds.GetProjection()

    def reproject(self, target_epsg: int, output_path: str) -> None:
        """
        TODO: add documentation
        """
        print(f"[System] Reprojecting {self.input_path} to EPSG:{target_epsg}...")

        try:
            gdal.Warp(
                output_path,
                self.ds,
                dstSRS=f"EPSG:{target_epsg}"
            )
        except Exception as e:
            raise RuntimeError("An exception occurred while running gdal.Warp():\n", e)

        print(f"Output saved to: {output_path}")

    def clip(self, bbox: Tuple[float, float, float, float], output_path: str) -> None:
        """
        TODO: add documentation
        """
        print(f"[System] Clipping {self.input_path} to bounding box: {bbox}...")
        left, bottom, right, top = bbox

        try:
            gdal.Translate(
                output_path,
                self.ds,
                projWin=[left, top, right, bottom]
            )
        except Exception as e:
            raise RuntimeError("An exception occurred while running gdal.Translate():\n", e)

        print(f"Output saved to: {output_path}")

    def close(self):
        """
        Explicitly release the GDAL dataset handle to free the file lock on Windows.
        """
        self.ds = None

    def __del__(self):
        self.ds = None  # properly close the dataset

    @staticmethod
    def merge(src_dir: str, tiles: List[str], output_path: str) -> None:
        """
        TODO: add documentation
        """
        gdal.UseExceptions()  # redeclare UseExceptions as this is a static method

        print(f"[System] Merging {len(tiles)} tiles...")
        vrt_path = os.path.join(src_dir, "merged.vrt")

        # Create a Virtual Dataset (VRT)
        try:
            gdal.BuildVRT(vrt_path, tiles)
        except Exception as e:
            raise RuntimeError("An exception occurred while building the VRT:\n", e)

        # Convert VRT to final compressed GeoTIFF
        try:
            gdal.Translate(
                output_path,
                vrt_path,
                creationOptions=["TILED=YES", "COMPRESS=LZW", "BIGTIFF=IF_NEEDED"]
            )
        except Exception as e:
            raise RuntimeError("An exception occurred while merging the VRT tiles with gdal.Translate():\n", e)

        try:
            os.remove(vrt_path)  # cleanup unneeded VRT file
        except OSError as e:
            # this is a non-critical error, we can continue processing
            print(f"BaseRasterProcessor: failed to remove file {vrt_path} :\n", e)

        print(f"Output saved to: {output_path}")
