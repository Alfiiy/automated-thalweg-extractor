import math
from typing import Tuple, List

class AOIValidator:
    """
    Validates the Area of Interest (AOI) provided by the user.
    Ensures coordinates are geographically valid and the total area 
    does not exceed the processing limit (e.g., 100 sq km).
    """

    def __init__(self, bbox_str: str):
        """
        Initialize with a comma-separated string: 'min_lon,min_lat,max_lon,max_lat'
        """
        self.bbox_str = bbox_str
        self.min_lon = 0.0
        self.min_lat = 0.0
        self.max_lon = 0.0
        self.max_lat = 0.0

    def validate(self) -> Tuple[float, float, float, float]:
        """
        Main execution method to run all checks.
        Returns:
            Tuple[float, float, float, float]: The validated (min_lon, min_lat, max_lon, max_lat)
        Raises:
            ValueError: If any validation rule is violated.
        """
        self._parse_input()
        self._check_geographic_bounds()
        self._check_logical_order()
        self._check_area_limit()
        
        print(f"[INFO] AOI Validated: {self.min_lon}, {self.min_lat}, {self.max_lon}, {self.max_lat}")
        return (self.min_lon, self.min_lat, self.max_lon, self.max_lat)

    def _parse_input(self):
        """Parses the string input into four float coordinates."""
        try:
            parts = [float(x.strip()) for x in self.bbox_str.split(',')]
            if len(parts) != 4:
                raise ValueError(f"Input must contain exactly 4 coordinates. Received: {len(parts)}")
            
            self.min_lon, self.min_lat, self.max_lon, self.max_lat = parts
        except ValueError as e:
            # Re-raising with a clear English message for the CLI user
            raise ValueError(f"Invalid format. Expected 'min_lon,min_lat,max_lon,max_lat'. Error: {e}")

    def _check_geographic_bounds(self):
        """Checks if coordinates are within Earth's physical limits."""
        if not (-180 <= self.min_lon <= 180) or not (-180 <= self.max_lon <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees.")
        
        if not (-90 <= self.min_lat <= 90) or not (-90 <= self.max_lat <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees.")

    def _check_logical_order(self):
        """Ensures min values are strictly less than max values."""
        if self.min_lon >= self.max_lon:
            raise ValueError(f"West/Min Longitude ({self.min_lon}) must be less than East/Max Longitude ({self.max_lon}).")
        
        if self.min_lat >= self.max_lat:
            raise ValueError(f"South/Min Latitude ({self.min_lat}) must be less than North/Max Latitude ({self.max_lat}).")

    def _check_area_limit(self, max_sq_km: float = 100.0):
        """
        Approximates the area to prevent excessive server load.
        Limit is set to 100 square kilometers.
        """
        # Approximation: 1 deg lat ~= 111 km
        # 1 deg lon ~= 111 km * cos(avg_lat)
        avg_lat_rad = math.radians((self.min_lat + self.max_lat) / 2)
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(avg_lat_rad)

        width_km = (self.max_lon - self.min_lon) * km_per_deg_lon
        height_km = (self.max_lat - self.min_lat) * km_per_deg_lat

        area_sq_km = width_km * height_km

        if area_sq_km > max_sq_km:
            raise ValueError(f"AOI is too large ({area_sq_km:.2f} sq km). Limit is {max_sq_km} sq km.")