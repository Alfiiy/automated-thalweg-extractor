import numpy as np
from terrain_pipeline.processor import BaseRasterProcessor
from osgeo import gdal


class RoughnessCalculator(BaseRasterProcessor):
    """
    Calculates surface roughness (Manning's n) based on ESA WorldCover classifications.
    Ensures that all valid land cover classes are mapped to prevent NoData holes.
    """
    def __init__(self, input_path: str):
        super().__init__(input_path)
        
        # Comprehensive mapping of ESA WorldCover classes to Manning's n values.
        self.mannings_n = {
            10: 0.100,  # Tree cover (High flow resistance)
            20: 0.080,  # Shrubland
            30: 0.035,  # Grassland
            40: 0.040,  # Cropland
            50: 0.050,  # Built-Up (Urban areas, roads, buildings)
            60: 0.025,  # Bare / Sparse vegetation
            70: 0.020,  # Snow and ice (Smooth surface)
            80: 0.030,  # Permanent water bodies (River channels have low resistance)
            90: 0.060,  # Herbaceous wetland
            95: 0.100,  # Mangroves (High flow resistance)
            100: 0.030, # Moss and lichen
        }

    def from_landcover(self, output_path) -> None:
        """
        Reads the categorical land cover raster and maps it to a continuous 
        friction surface. Handles NoData propagation explicitly.
        """
        print(f"[RoughnessGenerator] Generating roughness raster from {self.input_path} ...")

        # Instantiate a driver for the GeoTiff file format
        driver_gtiff = gdal.GetDriverByName('GTiff')

        # Create a new raster dataset
        try:
            new_dataset = driver_gtiff.Create(
                output_path,
                xsize=self.ds.RasterXSize,
                ysize=self.ds.RasterYSize,
                bands=1,
                eType=gdal.GDT_Float32
            )
        except Exception as e:
            raise RuntimeError("An exception occurred while creating the roughness raster file:\n", e)

        # Inherit projection and geotransform from the source landcover data
        new_dataset.SetProjection(self.ds.GetProjection())
        new_dataset.SetGeoTransform(self.ds.GetGeoTransform())

        # Read array data and the designated NoData value
        landcover_data = self.ds.GetRasterBand(1).ReadAsArray()
        nodata_val = self.ds.GetRasterBand(1).GetNoDataValue()

        # Execute dictionary mapping across the entire NumPy matrix
        # Any missing class is safely caught and assigned the NoData value
        replace_func = np.vectorize(lambda x: self.mannings_n.get(x, nodata_val))
        roughness_data = replace_func(landcover_data)

        # Write the physical roughness parameters back to the raster
        new_dataset.GetRasterBand(1).WriteArray(roughness_data)
        new_dataset.GetRasterBand(1).SetNoDataValue(nodata_val)

        print(f"Output saved to: {output_path}")

        # Explicitly close datasets to release memory
        new_dataset = None