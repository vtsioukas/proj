import subprocess
import json
import pyproj
import re
import numpy as np
import cv2

def strip_unit(value_str):
    # Regular expression to remove units (e.g., 'mm', 'cm', 'm', etc.) at the end of the string
    # \d+(\.\d+)? matches digits (with optional decimal)
    # \s* matches any whitespace before the unit
    # \w+ matches the unit itself
    stripped_value = re.sub(r'\s*\w+$', '', value_str)
    return float(stripped_value.strip())

def dms_to_decimal(dms_str):
    """
    Convert a string in DMS (Degrees, Minutes, Seconds) format to decimal degrees.
    
    Example of input: "123° 45' 56.7\" W" or "45° 30' 15\" N"
    """
    # Split the string into degrees, minutes, and seconds
    dms_str = dms_str.strip()
    
    # Identify the direction (N/S/E/W)
    direction = dms_str[-1]
    dms_str = dms_str[:-1].strip()  # Remove the direction
    
    # Split into degrees, minutes, and seconds
    parts = dms_str.split("deg")
    degrees = float(parts[0].strip())
    
    minutes_seconds = parts[1].split("'")
    minutes = float(minutes_seconds[0].strip())
    seconds = float(minutes_seconds[1].replace('"', '').strip())
    
    # Convert to decimal degrees
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    
    # If the direction is West or South, make the value negative
    if direction in ['W', 'S']:
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

def wgs84_to_epsg2100(latitude, longitude):
    # Define the WGS 84 (EPSG 4326) and EPSG 2100 projection strings
    wgs84 = pyproj.Proj(init="epsg:4326")
    epsg2100 = pyproj.Proj(init="epsg:2100")
    # Convert the coordinates from WGS 84 to EPSG 2100
    epsg2100_x, epsg2100_y = pyproj.transform(wgs84, epsg2100, longitude, latitude)

    return epsg2100_x, epsg2100_y
# Function to extract EXIF data using exiftool

# Function to calculate the rotation matrix R from omega, phi, kappa
def compute_rotation_matrix(omega, phi, kappa):
    """
    Compute the rotation matrix from the given Rodrigues angles (omega, phi, kappa).
    
    Angles are in radians.
    """
    # Rotation matrix around X-axis (omega)
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(omega), -np.sin(omega)],
                    [0, np.sin(omega), np.cos(omega)]])
    
    # Rotation matrix around Y-axis (phi)
    R_y = np.array([[np.cos(phi), 0, np.sin(phi)],
                    [0, 1, 0],
                    [-np.sin(phi), 0, np.cos(phi)]])
    
    # Rotation matrix around Z-axis (kappa)
    R_z = np.array([[np.cos(kappa), -np.sin(kappa), 0],
                    [np.sin(kappa), np.cos(kappa), 0],
                    [0, 0, 1]])
    
    # Combined rotation matrix R = R_z * R_y * R_x
    R = R_z @ R_y @ R_x
    return R

# Function to calculate the image coordinates x, y using the collinearity equations
def compute_image_coordinates(X, Y, Z, X0, Y0, Z0, omega, phi, kappa, f):
    """
    Compute the image coordinates (x, y) on the camera plane given the ground point (X, Y, Z),
    the camera center (X0, Y0, Z0), and the rotation angles (omega, phi, kappa).
    
    :param X: Ground X-coordinate of the point
    :param Y: Ground Y-coordinate of the point
    :param Z: Ground Z-coordinate of the point
    :param X0: X-coordinate of the camera center
    :param Y0: Y-coordinate of the camera center
    :param Z0: Z-coordinate of the camera center
    :param omega: Rotation angle omega (in radians)
    :param phi: Rotation angle phi (in radians)
    :param kappa: Rotation angle kappa (in radians)
    :param f: Focal length of the camera
    
    :return: Image coordinates (x, y)
    """
    # Compute the rotation matrix R
    R = compute_rotation_matrix(omega, phi, kappa)
    
    # Compute the relative position vector (X - X0, Y - Y0, Z - Z0)
    relative_position = np.array([X - X0, Y - Y0, Z - Z0])
    
    # Apply the collinearity equations
    r1 = R[0, :] @ relative_position
    r2 = R[1, :] @ relative_position
    r3 = R[2, :] @ relative_position
    
    # Compute image coordinates
    x = -f * (r1 / r3)
    y = -f * (r2 / r3)
    
    return x, y

import math
def calculate_sensor_size(focal_length, focal_length_35mm, image_width_px, image_height_px):
    # Step 1: Calculate the crop factor
    crop_factor = focal_length_35mm / focal_length

    # Step 2: Calculate the sensor diagonal in mm
    full_frame_diagonal_mm = 43.3  # Diagonal of a full-frame sensor in mm
    sensor_diagonal_mm = full_frame_diagonal_mm / crop_factor

    # Step 3: Calculate the aspect ratio of the image (width / height)
    aspect_ratio = image_width_px / image_height_px

    # Step 4: Calculate the height of the sensor in mm using the diagonal and aspect ratio
    sensor_height_mm = sensor_diagonal_mm / math.sqrt(1 + aspect_ratio**2)

    # Step 5: Calculate the width of the sensor in mm
    sensor_width_mm = aspect_ratio * sensor_height_mm

    return sensor_width_mm, sensor_height_mm, sensor_diagonal_mm

def sensor_dimensions(diagonal_inch, aspect_ratio_width, aspect_ratio_height):
    # Convert diagonal size from inches to millimeters (1 inch = 25.4 mm)
    diagonal_mm = diagonal_inch * 25.4

    # Calculate aspect ratio
    aspect_ratio = aspect_ratio_width / aspect_ratio_height

    # Calculate height in mm using the formula for height
    height_mm = diagonal_mm / math.sqrt(1 + aspect_ratio**2)

    # Calculate width in mm
    width_mm = aspect_ratio * height_mm

    return width_mm, height_mm

def extract_float_from_string(input_str):
    """
    Extract the first floating point number from a given string.

    Example input: "385.8 m Above Sea Level"
    Example output: 385.8
    """
    # Use regex to search for the first floating point number in the string
    match = re.search(r'[-+]?\d*\.\d+|\d+', input_str)
    
    if match:
        # Convert the matched string to a float and return
        return float(match.group())
    else:
        return None  # Return None if no match is found

def extract_drone_metadata(image_path):
    try:
        # Call exiftool and retrieve all metadata as JSON
        result = subprocess.run(['./exiftool-12.96_64/exiftool.exe','-j','-FocalLength','-ImageHeight','-ImageWidth','-GPSLatitude','-GPSAltitude','-GPSLongitude','-Pitch', '-Roll', "-Yaw",image_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #print(type(result))
        metadata = json.loads(result.stdout)[0]
        kappa=np.radians(metadata['Pitch'])
        phi=np.radians(metadata['Roll'])
        omega=np.radians(metadata['Yaw'])
        print(metadata['GPSLongitude'])
        f=strip_unit(metadata['FocalLength'])
        width=float(metadata['ImageWidth'])
        height=float(metadata['ImageHeight'])
        alt=extract_float_from_string(metadata['GPSAltitude'])
        lat=dms_to_decimal(metadata['GPSLatitude'])
        long=dms_to_decimal(metadata['GPSLongitude'])
        X,Y=wgs84_to_epsg2100(lat,long)
        Z=alt
        print(X,Y,Z)
        Xp=400556.656	
        Yp=4540821.991	
        Zp=182.506
        xx,yy,d=calculate_sensor_size(f,28,width,height)
        pixel_size=xx/width
        x,y=compute_image_coordinates(Xp,Yp,Zp,X,Y,Z,omega,phi,kappa,f)
        j = (x / pixel_size) + (width / 2)
        i = (y / pixel_size) + (height / 2)
        print(j,i)
    except Exception as e:
        print(f"Error occurred: {e}")
    return j,i

# Replace 'your_image.jpg' with the path to your image file
j,i=extract_drone_metadata(r'h:\UAV\IX-12-99082_0041_0602.jpg')
im=cv2.imread(r'h:\UAV\IX-12-99082_0041_0602.jpg')
cv2.circle(im,(int(j),int(i)),40,(255,0,0),10)
win=cv2.namedWindow("text",0)
cv2.imshow("text",im)
cv2.waitKey()
cv2.destroyAllWindows()