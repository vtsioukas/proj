import pyproj

def wgs84_to_epsg2100(latitude, longitude):
    # Define the WGS 84 (EPSG 4326) and EPSG 2100 projection strings
    wgs84 = pyproj.Proj(init="epsg:4326")
    epsg2100 = pyproj.Proj(init="epsg:2100")

    # Convert the coordinates from WGS 84 to EPSG 2100
    epsg2100_x, epsg2100_y = pyproj.transform(wgs84, epsg2100, longitude, latitude)

    return epsg2100_x, epsg2100_y

# Example usage:
latitude = 48.858844
longitude = 2.294351
epsg2100_x, epsg2100_y = wgs84_to_epsg2100(latitude, longitude)

print(f"Latitude: {latitude}, Longitude: {longitude}")
print(f"EPSG 2100 X: {epsg2100_x}, EPSG 2100 Y: {epsg2100_y}")
