import cv2
import os
import sys
from PIL import Image

input_folder = sys.argv[1]
output_folder = sys.argv[2]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def detect_orientation_with_metadata(image_path):
    image = Image.open(image_path)
    
    width, height = image.size
    
    try:
        exif = image._getexif()
        orientation = exif.get(274)
        if orientation == 6 or orientation == 8:
            width, height = height, width
    except (AttributeError, KeyError, TypeError):
        pass
    
    if width > height:
        return 'Landscape'
    else:
        return 'Portrait'

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace('.jpg', '_processed.jpg'))
        
        image = cv2.imread(input_path, 0)
        
        orientation = detect_orientation_with_metadata(input_path)
        
        if orientation == 'Landscape':
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        processed_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        processed_image = cv2.bitwise_not(processed_image)
        processed_image = cv2.resize(processed_image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        
        cv2.imwrite(output_path, processed_image)

print("Processing.")
