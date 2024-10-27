import requests
import numpy as np
from PIL import Image
from io import BytesIO

def convert_url_to_uint8(url):
    # Fetch the image from the URL
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    # Convert to a NumPy array and ensure it is of type uint8
    uint8_array = np.array(image, dtype=np.uint8)

    return uint8_array


file_path = 'path/to/your/file.html'  # Replace with the actual file path

# Open the file and read its content
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()


