from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import math

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

    return location1.address, location2.address, azimuth_degrees

if __name__ == "__main__":
    # Input coordinates for the two positions (latitude and longitude)
    lat1 = float(input("Enter Latitude 1: "))
    lon1 = float(input("Enter Longitude 1: "))
    lat2 = float(input("Enter Latitude 2: "))
    lon2 = float(input("Enter Longitude 2: "))

    # Calculate the azimuth and get location names
    location1_name, location2_name, azimuth = get_azimuth(lat1, lon1, lat2, lon2)

    # Print results
    print(f"Location 1: {location1_name}")
    print(f"Location 2: {location2_name}")
    print(f"Azimuth (degrees): {azimuth}")
