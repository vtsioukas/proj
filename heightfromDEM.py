import rasterio

# Load the DEM file with georeferencing information
def load_dem_file(file_path):
    try:
        with rasterio.open(file_path) as src:
            return src
    except Exception as e:
        print(f"Error loading DEM file: {e}")
        return None

# Extract height information at a specific location
def extract_height(dem, easting, northing):
    try:
        # Transform the Easting and Northing coordinates to the DEM's CRS
        lon, lat = dem.xy(easting, northing)
        
        # Read the pixel value at the transformed coordinates
        row, col = dem.index(lon, lat)
        height = dem.read(1, window=((row, row+1), (col, col+1)))[0][0]
        
        return height
    except Exception as e:
        print(f"Error extracting height information: {e}")
        return None

if __name__ == "__main__":
    # Specify the path to your DEM file (TIFF format)
    dem_file_path = "greece.tif"
    
    # Load the DEM file
    dem = load_dem_file(dem_file_path)
    
    if dem:
        # Input the Easting and Northing coordinates (in the same reference system as the DEM)
        easting = float(input("Enter Easting (X coordinate): "))
        northing = float(input("Enter Northing (Y coordinate): "))
        
        # Extract height information
        height = extract_height(dem, easting, northing)
        
        if height is not None:
            print(f"Height at Easting {easting}, Northing {northing}: {height} meters")
    else:
        print("Failed to load the DEM file.")
