
from pyproj import Transformer

# Define the CRS systems
source_crs = "EPSG:2100"  # GGRS87 / Greek Grid
target_crs = "EPSG:4326"  # WGS84 (to use with global datasets)

# Create a transformer for geographic transformation
transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

# Example coordinates (Easting, Northing, height in meters)
easting, northing, ellipsoidal_height = 411843.554, 4497640.90, 25.0
# Perform the transformation to geographic coordinates (lat, lon)
longitude, latitude, _ = transformer.transform(easting, northing, ellipsoidal_height)

# Assume we have obtained the geoid height from a dataset (e.g., HGM2019)
geoid_height = 1.0  # Example geoid height in meters

# Calculate orthometric height (height above mean sea level)
orthometric_height = ellipsoidal_height - geoid_height

print(f"Longitude: {longitude}, Latitude: {latitude}, Orthometric Height (HGM2019): {orthometric_height} meters")
