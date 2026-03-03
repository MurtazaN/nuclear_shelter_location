import numpy as np
from shapely.geometry import Point
from shapely.ops import transform
from functools import partial
import pyproj

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in miles."""
    R = 3959  # Earth radius in miles
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    
    a = np.sin(delta_phi/2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    
    return R * c

def create_safety_mask(zip_codes, targets, exclusion_radius_miles=15):
    """
    Returns a boolean mask where True means the zip code is SAFE 
    (outside the exclusion radius of any target).
    """
    mask = np.ones(len(zip_codes), dtype=bool)
    
    for i, zip_row in zip_codes.iterrows():
        z_lat, z_lon = zip_row['lat'], zip_row['lon']
        for target in targets:
            dist = haversine_distance(z_lat, z_lon, target['lat'], target['lon'])
            if dist < exclusion_radius_miles:
                mask[i] = False
                break
    return mask