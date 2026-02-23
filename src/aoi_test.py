import unittest
from terrain_pipeline.aoi import AOIValidator

class TestAOIValidator(unittest.TestCase):
    """
    Unit tests for the AOIValidator class.
    Ensures that invalid bounding box inputs are correctly intercepted
    before triggering expensive API calls.
    """

    def test_valid_bbox(self):
        # Should pass and return a tuple of 4 floats
        validator = AOIValidator("9.10,48.70,9.20,48.80")
        result = validator.validate()
        self.assertEqual(result, (9.10, 48.70, 9.20, 48.80))

    def test_missing_coordinates(self):
        # Only 3 coordinates provided instead of 4
        validator = AOIValidator("9.10,48.70,9.20")
        with self.assertRaises(ValueError):
            validator.validate()

    def test_invalid_characters(self):
        # Letters provided instead of numeric floats
        validator = AOIValidator("9.10,abc,9.20,48.80")
        with self.assertRaises(ValueError):
            validator.validate()

    def test_out_of_bounds_longitude(self):
        # Longitude strictly outside the -180 to 180 range
        validator = AOIValidator("-190.00,48.70,9.20,48.80")
        with self.assertRaises(ValueError):
            validator.validate()

    def test_out_of_bounds_latitude(self):
        # Latitude strictly outside the -90 to 90 range
        validator = AOIValidator("9.10,-95.00,9.20,48.80")
        with self.assertRaises(ValueError):
            validator.validate()

if __name__ == '__main__':
    unittest.main()