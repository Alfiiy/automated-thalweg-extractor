import numpy as np
from osgeo import gdal
from pysheds.grid import Grid
from terrain_pipeline.processor import BaseRasterProcessor

class ThalwegExtractor(BaseRasterProcessor):
    """
    Extracts hydrological features (Thalweg) from a DEM using the D8 routing algorithm.
    Utilizes pysheds for optimized matrix operations and inherits BaseRasterProcessor for standard I/O.
    """

    def __init__(self, input_path: str):
        super().__init__(input_path)
        # Initialize the pysheds Grid object directly from the file path
        self.grid = Grid.from_raster(self.input_path)
        # Read the DEM data into the grid
        self.dem = self.grid.read_raster(self.input_path)
        self.nodata = self.dem.nodata

    def extract(self, output_path: str, threshold: int = 1000) -> None:
        """
        Executes the D8 extraction pipeline: Fill -> Direction -> Accumulation -> Threshold.
        
        Args:
            output_path (str): The file path to save the resulting GeoTIFF.
            threshold (int): The minimum flow accumulation value to be considered a river/thalweg.
        """
        print("[ThalwegExtractor] Starting Thalweg extraction pipeline via pysheds...")
        
        # Step 1: Detect and fill depressions in the DEM
        print("[ThalwegExtractor] Step 1: Filling sinks...")
        filled_dem = self.grid.fill_depressions(self.dem)

        # Step 2: Resolve flats and calculate D8 flow direction
        print("[ThalwegExtractor] Step 2: Resolving flats and calculating D8 Flow Direction...")
        inflated_dem = self.grid.resolve_flats(filled_dem)
        # Standard D8 directional mapping
        dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
        flow_dir = self.grid.flowdir(inflated_dem, dirmap=dirmap)

        # Step 3: Calculate flow accumulation
        print("[ThalwegExtractor] Step 3: Calculating Flow Accumulation...")
        flow_acc = self.grid.accumulation(flow_dir, dirmap=dirmap)

        # Step 4: Apply threshold to extract the network
        print(f"[ThalwegExtractor] Step 4: Applying accumulation threshold ({threshold})...")
        # Extract the underlying numpy array from the pysheds Raster object
        acc_array = np.asarray(flow_acc)
        
        # Create a binary mask: 1.0 for Thalweg, 0.0 for non-Thalweg
        thalweg_mask = np.where(acc_array > threshold, 1.0, 0.0)
        
        # Re-apply NoData values to the edges/outside the bounding box
        if self.nodata is not None:
            dem_array = np.asarray(self.dem)
            thalweg_mask[dem_array == self.nodata] = self.nodata

        # Step 5: Save using the inherited functionality
        self._save_array_to_raster(thalweg_mask, output_path)

    def _save_array_to_raster(self, data_array: np.ndarray, output_path: str) -> None:
        """
        Saves the processed numpy array as a GeoTIFF using the parent's spatial reference.
        """
        driver = gdal.GetDriverByName("GTiff")
        rows, cols = data_array.shape
        out_ds = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
        
        out_ds.SetGeoTransform(self.ds.GetGeoTransform())
        out_ds.SetProjection(self.ds.GetProjection())
        
        out_band = out_ds.GetRasterBand(1)
        out_band.WriteArray(data_array)
        if self.nodata is not None:
            out_band.SetNoDataValue(float(self.nodata)) 
            
        out_band.FlushCache()
        out_ds = None
        print(f"✅ Thalweg network successfully saved to: {output_path}")