import subprocess
import json

# Function to extract EXIF data using exiftool
def extract_drone_metadata(image_path):
    try:
        # Call exiftool and retrieve all metadata as JSON
        result = subprocess.run(['./exiftool-12.96_64/exiftool.exe','-j','-GPSLatitude','-GPSLongitude','-Pitch', '-Roll', "-Yaw",image_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #print(type(result))
        metadata = json.loads(result.stdout)[0]
        print(metadata['Pitch'])
        print(metadata['Roll'])
        print(metadata['Yaw'])
        print(metadata['GPSLongitude'])
        print(metadata['GPSLatitude'])
        
        
    except Exception as e:
        print(f"Error occurred: {e}")

# Replace 'your_image.jpg' with the path to your image file
extract_drone_metadata(r'h:\UAV\IX-12-99082_0041_0601.jpg')
