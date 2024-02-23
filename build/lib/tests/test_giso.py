import unittest
from unittest.mock import patch
from giso.utils import get_coordinates, get_isochrone, get_isochrones, set_token
import os

TOKEN = os.getenv('MAPBOX_API_KEY')

class TestMapboxModule(unittest.TestCase):
    def test_get_coordinates_success(self):
        with patch('requests.get') as mocked_get:
            # Setup mock response
            mocked_get.return_value.ok = True
            mocked_get.return_value.json.return_value = {
                "features": [{
                    "center": [100.0, 0.5]
                }]
            }
            
            expected = (0.5, 100.0)
            set_token(TOKEN)
            result = get_coordinates("buckingham palace, london, uk")
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
