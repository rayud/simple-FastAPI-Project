"""
This module contains a single function named calculate_distance
which is used to calculate the distance between two points on the Earth.
"""

from math import radians, cos, sin, asin, sqrt

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    This function calculates the distance between two sets of geographic coordinates
    using the Haversine formula.

    For complete details, please visit the geeksforgeeks article:
    https://www.geeksforgeeks.org/program-distance-two-points-earth/

    Parameters:
    - lat1 (float): Latitude of the first point in degrees.
    - lon1 (float): Longitude of the first point in degrees.
    - lat2 (float): Latitude of the second point in degrees.
    - lon2 (float): Longitude of the second point in degrees.

    Returns:
    - float: The calculated distance between the two points in kilometers.
    """

    # Convert degrees to radians
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # Radius of the Earth in kilometers
    r = 6371

    # Calculate the result
    return c * r
