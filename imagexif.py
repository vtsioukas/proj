from PIL import Image
import exifread
import pyproj

def extract_geotagging_info(image_path):
    # Open the image
    with open(image_path, 'rb') as image_file:
        # Open the image using Pillow
        img = Image.open(image_file)

        # Extract EXIF metadata from the image
        exif_data = exifread.process_file(image_file)

        # Check if GPS information is available in the EXIF data
        if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data:
            latitude = exif_data['GPS GPSLatitude'].values
            longitude = exif_data['GPS GPSLongitude'].values

            # Convert the GPS coordinates to decimal degrees
            latitude = float(latitude[0]) + float(latitude[1]) / 60 + float(latitude[2]) / 3600
            longitude = float(longitude[0]) + float(longitude[1]) / 60 + float(longitude[2]) / 3600

            return latitude, longitude
        else:
            print("No GPS information found in the image.")
            return None

# Example usage:
image_path = 'your_image.jpg'
coordinates = extract_geotagging_info(r"H:\pithio\Drone_Photos\DJI_0027.jpg")

def wgs84_to_epsg2100(latitude, longitude):
    # Define the WGS 84 (EPSG 4326) and EPSG 2100 projection strings
    wgs84 = pyproj.Proj(init="epsg:4326")
    epsg2100 = pyproj.Proj(init="epsg:2100")

    # Convert the coordinates from WGS 84 to EPSG 2100
    epsg2100_x, epsg2100_y = pyproj.transform(wgs84, epsg2100, longitude, latitude)

    return epsg2100_x, epsg2100_y

# Example usage:
if coordinates:
    latitude = coordinates[0]
    longitude = coordinates[1]
    epsg2100_x, epsg2100_y = wgs84_to_epsg2100(latitude, longitude)

    print(f"Latitude: {latitude}, Longitude: {longitude}")
    print(f"EPSG 2100 X: {epsg2100_x}, EPSG 2100 Y: {epsg2100_y}")

