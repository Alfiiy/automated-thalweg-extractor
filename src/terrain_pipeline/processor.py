import os
from osgeo import gdal, osr

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

    def reproject(self, target_epsg: int, output_path: str):
        """
        [Architecture Placeholder]
        Ayan, please implement the reprojection logic here or call this method 
        once the data is downloaded.
        
        Args:
            target_epsg (int): The target UTM EPSG code.
            output_path (str): Where to save the reprojected file.
        """
        # TODO: Implement gdal.Warp logic here to meet Requirement F2
        print(f"[System] Reprojecting {self.input_path} to EPSG:{target_epsg}...")
        
        # Placeholder logic for Ayan to fill or use:
        # gdal.Warp(output_path, self.ds, dstSRS=f'EPSG:{target_epsg}')
        pass