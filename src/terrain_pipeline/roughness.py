import numpy as np
from terrain_pipeline.processor import BaseRasterProcessor
from osgeo import gdal


class RoughnessCalculator(BaseRasterProcessor):
    """
    TODO: add documentation
    """
    def __init__(self, input_path: str):
        super().__init__(input_path)
        self.mannings_n = {
            10: 0.02,  # Tree cover
            20: 0.08,  # Shrubland
            30: 0.032,  # Grassland
            40: 0.035,  # Cropland
            # 50: 0.0,  # Built-Up
            60: 0.025,  # Bare / Sparse vegetation
            # 70: 0.0,  # Snow and ice
            # 80: 0.9,  # Permanent water bodies
            90: 0.06,  # Herbaceous wetland
            # 95: 0.0,  # Mangroves
            100: 0.03,  # Moss and lichen
        }

    def from_landcover(self, output_path) -> None:
        """
        TODO: add documentation
        """
        print(f"[RoughnessGenerator] Generating roughness raster from {self.input_path} ...")

        # create and write data to a raster
        driver_gtiff = gdal.GetDriverByName('GTiff')  # instantiate a driver for the GeoTiff file format

        # create a new raster
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

        # set the same raster projection
        new_dataset.SetProjection(self.ds.GetProjection())

        # set the same geotransform
        new_dataset.SetGeoTransform(self.ds.GetGeoTransform())

        # create and write data values to the raster
        landcover_data = self.ds.GetRasterBand(1).ReadAsArray()
        nodata_val = self.ds.GetRasterBand(1).GetNoDataValue()

        # replace land cover categories with corresponding mannings roughness values
        # if the category is not known, replace with the nodata value
        replace_func = np.vectorize(lambda x: self.mannings_n.get(x, nodata_val))

        roughness_data = replace_func(landcover_data)

        new_dataset.GetRasterBand(1).WriteArray(roughness_data)  # write the numpy array to the raster
        new_dataset.GetRasterBand(1).SetNoDataValue(nodata_val)  # set the no data value

        print(f"Output saved to: {output_path}")

        new_dataset = None  # properly close dataset
