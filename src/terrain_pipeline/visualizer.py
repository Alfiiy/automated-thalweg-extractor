import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from osgeo import gdal

class ResultVisualizer:
    """
    Generates high-fidelity cartographic map previews from the output raster files.
    """

    def __init__(self, dem_path: str, roughness_path: str, thalweg_path: str):
        self.dem_path = dem_path
        self.roughness_path = roughness_path
        self.thalweg_path = thalweg_path

    def _read_raster_with_extent(self, file_path: str) -> tuple:
        """
        Internal helper to safely read a single band raster into a NumPy array,
        and extract its physical spatial extent for accurate mapping.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file for visualization: {file_path}")
        
        ds = gdal.Open(file_path)
        band = ds.GetRasterBand(1)
        array = band.ReadAsArray()
        nodata = band.GetNoDataValue()
        
        # Extract physical coordinates from GDAL GeoTransform
        gt = ds.GetGeoTransform()
        cols = ds.RasterXSize
        rows = ds.RasterYSize
        
        # extent format required by matplotlib: [left, right, bottom, top]
        # gt[0]: top-left X, gt[1]: W-E resolution
        # gt[3]: top-left Y, gt[5]: N-S resolution (negative)
        left = gt[0]
        right = gt[0] + (cols * gt[1])
        top = gt[3]
        bottom = gt[3] + (rows * gt[5])
        extent = [left, right, bottom, top]
        
        # Apply NaN to nodata pixels for transparent plotting
        if nodata is not None:
            array = np.where(array == float(nodata), np.nan, array)
            
        return array, extent

    def _add_cartographic_elements(self, ax, extent: list) -> None:
        """
        Adds physical border, coordinates, North Arrow, and a high-contrast
        alternating black-and-white scale bar with a white background plate.
        """
        left, right, bottom, top = extent
        x_range = right - left
        y_range = top - bottom

        # 1. Enforce Bounding Box (Spines)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(1.0)

        # 2. Add North Arrow (Top Right)
        ax.annotate('N', xy=(0.95, 0.95), xytext=(0.95, 0.85),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(facecolor='black', width=3, headwidth=10, shrink=0.05),
                    ha='center', va='top', fontsize=14, fontweight='bold', zorder=10)

        # 3. Add Professional Checkered Scale Bar with Background (Bottom Left)
        total_scale_m = 2000
        num_segments = 4
        segment_len_m = total_scale_m / num_segments
        
        # Define anchor position (shifted slightly to accommodate the background box)
        x_anchor = left + (x_range * 0.05)
        y_anchor = bottom + (y_range * 0.08)
        
        bar_height = y_range * 0.015
        label_y_pos = y_anchor - (y_range * 0.015)

        # --- NEW: Draw Solid White Background Plate (zorder=9) ---
        # Calculate padding in raw meters to enclose both the bar and the text
        bg_left = x_anchor - (x_range * 0.03)
        bg_right = x_anchor + total_scale_m + (x_range * 0.08) 
        bg_bottom = label_y_pos - (y_range * 0.04)             
        bg_top = y_anchor + bar_height + (y_range * 0.03)      

        bg_rect = Rectangle(
            (bg_left, bg_bottom), bg_right - bg_left, bg_top - bg_bottom,
            facecolor='white', edgecolor='black', linewidth=1.0, zorder=9
        )
        ax.add_patch(bg_rect)
        # ---------------------------------------------------------

        # --- Draw Alternating Segments (zorder=10) ---
        colors = ['black', 'white']
        for i in range(num_segments):
            x_pos = x_anchor + (i * segment_len_m)
            color = colors[i % 2]
            
            linewidth = 0.5 if color == 'white' else 0
            rect = Rectangle(
                (x_pos, y_anchor), segment_len_m, bar_height,
                facecolor=color, edgecolor='black', linewidth=linewidth, zorder=10
            )
            ax.add_patch(rect)

        # --- Add Scale Labels (zorder=10) ---
        text_kwargs = dict(ha='center', va='top', fontsize=9, fontweight='bold', color='black', zorder=10)
        ax.text(x_anchor, label_y_pos, '0', **text_kwargs)
        ax.text(x_anchor + (total_scale_m / 2), label_y_pos, '1', **text_kwargs)
        ax.text(x_anchor + total_scale_m, label_y_pos, '2 km', **text_kwargs)

    def generate_preview(self, output_path: str) -> None:
        """
        Reads the 3 core outputs and generates a side-by-side comparative cartographic plot.
        """
        print("[Visualizer] Generating Cartographically Correct Map Preview...")
        
        dem_data, dem_extent = self._read_raster_with_extent(self.dem_path)
        rough_data, rough_extent = self._read_raster_with_extent(self.roughness_path)
        thalweg_data, thalweg_extent = self._read_raster_with_extent(self.thalweg_path)

        thalweg_data = np.where(thalweg_data == 0, np.nan, thalweg_data)

        # Setup plotting figure with slightly wider dimension for explicit coordinates
        fig, axes = plt.subplots(1, 3, figsize=(24, 8))

        # 1. DEM Plot
        im1 = axes[0].imshow(dem_data, cmap='terrain', extent=dem_extent)
        axes[0].set_title('Digital Elevation Model')
        fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04, label='Elevation (m)')
        self._add_cartographic_elements(axes[0], dem_extent)

        # 2. Roughness Plot (Changed to 'viridis' for absolute contrast against white)
        im2 = axes[1].imshow(rough_data, cmap='viridis', extent=rough_extent)
        axes[1].set_title('Surface Roughness')
        fig.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04, label="Manning's n")
        self._add_cartographic_elements(axes[1], rough_extent)

        # 3. Thalweg Plot (Overlay)
        axes[2].imshow(dem_data, cmap='Greys', alpha=0.6, extent=dem_extent) 
        river_cmap = mcolors.ListedColormap(['#0000FF']) 
        axes[2].imshow(thalweg_data, cmap=river_cmap, extent=thalweg_extent)
        axes[2].set_title('D8 Thalweg Network')
        self._add_cartographic_elements(axes[2], dem_extent)
        
        # Explicit Legend for Thalweg
        custom_lines = [Line2D([0], [0], color='#0000FF', lw=2)]
        axes[2].legend(custom_lines, ['Thalweg (River Network)'], loc='upper left', framealpha=0.9)

        # Format Coordinate Ticks for all axes
        for ax in axes:
            ax.tick_params(axis='both', which='major', labelsize=8)
            plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

        # Save to file
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        print(f"✅ Visualization saved successfully to: {output_path}")