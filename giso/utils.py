import requests
import json
import numpy as np

TOKEN = None

def set_token(token):
    '''
    Sets the Mapbox API token for use in subsequent API calls.
    Argument(s):
    -- token (str): The Mapbox API token.
    '''
    global TOKEN
    TOKEN = token   

def get_coordinates(address):
    '''
    Geocodes an address to its corresponding latitude and longitude coordinates.

    This function sends a request to the Mapbox Geocoding API using the provided address. It then extracts the latitude and longitude from the response and returns them. 
    The function assumes that the first feature returned by the Mapbox API is the correct match for the given address. 
    Visit https://docs.mapbox.com/ for more information.

    Parameters:
    - address (str): The physical address that needs to be geocoded. Spaces in the address are URL-encoded to ensure a valid request URL.

    Returns:
    - tuple: A tuple containing two float values representing the latitude and longitude of the given address, in that order.

    Raises:
    - requests.exceptions.RequestException: If there is a problem with the network connection or the Mapbox API request fails.
    - json.JSONDecodeError: If the response from the Mapbox API cannot be decoded.
    - IndexError: If the response from the Mapbox API does not contain any features, indicating that the address could not be geocoded.

    Note:
    - This function requires a valid Mapbox API access token set in the `TOKEN` variable.
    - It is recommended to handle exceptions gracefully when calling this function, especially for production environments.
    '''
    if TOKEN is None:
        raise ValueError("Mapbox API token has not been set. Please set the token using set_token(token).")

    try:
        req = requests.get(f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address.replace(' ', '%20')}.json?access_token={TOKEN}&autocomplete=true")
        req.raise_for_status()  # Raises a requests.exceptions.HTTPError if the response was unsuccessful.
        content = json.loads(req.content)
        lon, lat = content["features"][0]["center"]
        return lat, lon
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to get coordinates for address '{address}': {e}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Failed to decode the response from Mapbox API.")
    except IndexError:
        raise IndexError(f"No geocoding result found for the address: '{address}'")

def get_isochrone(lat, lon, mins, v="driving"):
    '''
    Generates and returns a polygon representing an isochrone for a given geographic location, duration, 
    and travel mode. An isochrone is a contour that connects points of equal travel time from a starting 
    location. This function utilizes the Mapbox Isochrone API to calculate and retrieve the isochrone. 
    Visit https://docs.mapbox.com/ for more information.

    Parameters:
    - lat (float): Latitude of the starting point.
    - lon (float): Longitude of the starting point.
    - mins (int): Duration in minutes for which the isochrone is to be generated. The isochrone will 
                  represent all locations that can be reached within this duration from the starting point.
    - v (str, optional): Mode of travel for which the isochrone is to be calculated. Default is "driving". 
                         Supported modes depend on the capabilities of the Mapbox Isochrone API and may 
                         include "walking", "cycling", etc.

    Returns:
    - numpy.ndarray: A 2D numpy array of coordinates that form the polygon of the isochrone. The coordinates 
                     are ordered as [[latitude, longitude], [latitude, longitude], ...].

    Note:
    - This function requires a valid Mapbox API access token specified by the `TOKEN` variable.
    - The function performs a network request to the Mapbox API, parses the JSON response to extract the 
      isochrone geometry, and then processes the geometry to format it as a numpy array with latitude and 
      longitude coordinates.
    - The coordinates of the returned polygon are flipped to comply with typical latitude and longitude 
      ordering, as opposed to the longitude and latitude ordering used by the Mapbox API.
    '''
    try:
        req = requests.get(f"https://api.mapbox.com/isochrone/v1/mapbox/{v}/{lon}%2C{lat}?contours_minutes={mins}&contours_colors=54278f&polygons=true&generalize=0&access_token={TOKEN}")
        req.raise_for_status()  # Raises a requests.exceptions.HTTPError if the response was unsuccessful.
        content = json.loads(req.content)
        shp = content['features'][0]['geometry']['coordinates']
        shp = np.flip(np.array(shp[0]), axis=1)  # Flipping the array to match desired orientation
        return shp
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to get isochrone shape: {e}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Failed to decode the response from the Mapbox API.")
    except IndexError:
        raise IndexError("No isochrone shape found for the given parameters.")


def get_isochrones(lat, lon, mins, v="driving"):
    '''
    Generates and returns a list of polygons representing isochrones for given geographic coordinates
    and specified durations. Isochrones are contours that connect points of equal travel time from 
    a starting location. This function allows for the calculation of isochrones based on various travel 
    modes. Visit https://docs.mapbox.com/ for more information.

    Parameters:
    - lat (float): Latitude of the starting point.
    - lon (float): Longitude of the starting point.
    - mins (list[int]): A list of durations in minutes for which the isochrones are to be generated. 
                        The isochrones will be calculated for each duration specified in this list.
    - v (str, optional): Mode of travel. Default is "driving". Other modes could include "walking", 
                         "cycling", etc., depending on the capabilities of the underlying isochrone 
                         generation service.

    Returns:
    - list: A list of polygon objects, where each polygon corresponds to an isochrone for the respective 
            duration specified in `mins`. The polygons are returned in the order of the durations 
            provided, sorted in descending order.

    Note:
    The function relies on an external function `get_isochrone(lat, lon, duration, mode)` to generate 
    each isochrone polygon for the specified latitude, longitude, duration, and travel mode.
    '''
    shp = []
    mins.sort(reverse=True)
    for m in mins:
        try:
            shape = get_isochrone(lon, lat, mins, v)
            shp.append(shape)
        except Exception as e:
            print(f"Error retrieving isochrone for {m} minutes: {e}")
            continue
    return shp
