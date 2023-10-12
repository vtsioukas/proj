from PIL import Image
import exifread
import pyproj
import os
import rasterio
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import math

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

import os

def list_jpg_files(folder_path):
    jpg_files = []
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return jpg_files

    # Iterate through the files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                jpg_files.append(os.path.join(root, file))
    
    return jpg_files

def get_azimuth(lat1, lon1, lat2, lon2):
    # Create geopy geocoder
    geolocator = Nominatim(user_agent="azimuth_calculator")

    # Define locations based on latitude and longitude
    location1 = geolocator.reverse((lat1, lon1))
    location2 = geolocator.reverse((lat2, lon2))

    # Calculate the azimuth using great-circle distance
    distance = great_circle((lat1, lon1), (lat2, lon2)).miles
    delta_lon = lon2 - lon1
    radian_azimuth = math.atan2(delta_lon, distance)

    # Convert azimuth from radians to degrees
    azimuth_degrees = math.degrees(radian_azimuth)

    #return location1.address, location2.address, azimuth_degrees

    return azimuth_degrees

if __name__=="__main__":
    folder_path = input("Enter the folder path: ")

    jpg_files = list_jpg_files(folder_path)
    
    if jpg_files:
        #print(jpg_files)
        Lat1,Lon1=0,0
        print("List of JPG files:")
        for jpg_file in jpg_files:
            #print(jpg_file)
            Lat1,Lon1=extract_geotagging_info(jpg_file)
            try:
                Lat2
            except NameError:
                print("well, it WASN'T defined after all!")
            else:
                A=get_azimuth(Lat1,Lon1,Lat2,Lon2)
                print(A)
            Lat2,Lon2=Lat1,Lon1
    else:
        print("No JPG files found in the specified folder.")
    # if coordinates:
    #     latitude = coordinates[0]
    #     longitude = coordinates[1]
    #     epsg2100_x, epsg2100_y = wgs84_to_epsg2100(latitude, longitude)

    #     print(f"Latitude: {latitude}, Longitude: {longitude}")
    #     print(f"EPSG 2100 X: {epsg2100_x}, EPSG 2100 Y: {epsg2100_y}")

