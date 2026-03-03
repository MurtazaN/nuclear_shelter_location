import pandas as pd
import numpy as np
# import geopandas as gpd # Uncomment when using real shapefiles

def load_census_data():
    """
    Loads US Census Zip Code data.
    TODO: Replace mock data with actual Census Bureau CSV/Shapefile loading.
    """
    print("Loading Census Data...")
    # Mocking 100 zip codes for testing logic before scaling to 30k
    n = 100 
    data = {
        'zip_code': np.arange(10000, 10000 + n),
        'population': np.random.randint(1000, 50000, n),
        'lat': np.random.uniform(25, 48, n),
        'lon': np.random.uniform(-125, -70, n)
    }
    return pd.DataFrame(data)

def load_urban_targets():
    """
    Loads major urban targets (e.g., top 50 US cities).
    TODO: Replace with actual list of high-value targets.
    """
    print("Loading Urban Targets...")
    targets = [
        {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
        {'name': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437},
        # Add more targets...
    ]
    return targets

def load_infrastructure_data():
    """
    Loads power grid or road network scores per zip code.
    TODO: Replace with OSMnx or Power Grid data processing.
    """
    print("Loading Infrastructure Data...")
    # Mocking accessibility score (0 to 1)
    return np.random.rand(100) 