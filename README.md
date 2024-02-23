
# `giso` - Basic GIS Interface <img src="./giso_logo.png" style="width:120px" align="right">


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This package provides a set of utilities for interacting with the Mapbox API, allowing users to geocode addresses to latitude and longitude coordinates, and generate isochrones to visualize areas accessible within specific time frames by various modes of transportation.

## Installation
Before you can use the package, ensure you have Python installed on your system. This package requires requests, json, and numpy libraries. If not already installed, you can install them using pip:

```
pip install requests numpy json
```

## Setting Up Your Mapbox API Token
To use the Mapbox API, you need a valid Mapbox API token. You can obtain one by signing up at Mapbox.

Once you have your token, use the set_token function to configure it for use with the API calls:
```
from giso import set_token

set_token('YOUR_MAPBOX_API_TOKEN_HERE')
```

Replace 'YOUR_MAPBOX_API_TOKEN_HERE' with your actual Mapbox API token.

## Usage
### Geocoding an Address
To convert an address to its corresponding latitude and longitude:
```
from giso import get_coordinates

address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
latitude, longitude = get_coordinates(address)
print(f"Latitude: {latitude}, Longitude: {longitude}")
```
### Generating an Isochrone
To generate an isochrone map based on travel time:

```
from giso import get_isochrone

lat = 38.8977  # Latitude of the White House
lon = -77.0365  # Longitude of the White House
mins = 10  # Time in minutes

isochrone_shape = get_isochrone(lat, lon, mins, "walking")
# This returns a numpy array of coordinates for the isochrone shape
```

### Fetching Multiple Isochrones
To fetch multiple isochrones for different durations:
```
from giso import get_isochrones

lat = 38.8977  # Latitude
lon = -77.0365  # Longitude
mins_list = [5, 10, 15]  # Time in minutes for multiple isochrones

isochrones_shapes = get_isochrones(lat, lon, mins_list, "cycling")
# This returns a list of numpy arrays, each representing an isochrone shape
```

### Error Handling
The functions in this package are designed to raise exceptions in case of errors, such as invalid API tokens, network issues, or invalid parameters. It's recommended to handle these exceptions gracefully in your application to ensure a smooth user experience.

Here's an example of handling exceptions when geocoding an address:

```
try:
    latitude, longitude = get_coordinates("An invalid address")
except Exception as e:
    print(f"An error occurred: {e}")
```
## Additional Information
For more details on the Mapbox API and its capabilities, visit the [Mapbox documentation](https://docs.mapbox.com/).