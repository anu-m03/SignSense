from flask import Flask, request, jsonify
import numpy as np
import io
import base64
from PIL import Image

app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get image data from the request
    data = request.json  # Assuming JSON payload
    image_data = data['image']  # Base64 or raw image data

    # If image data is base64, decode it
    if image_data.startswith('data:image/png;base64,'):
        image_data = image_data.split(',')[1]  # Strip off the prefix
        image_data = io.BytesIO(base64.b64decode(image_data))

    # Convert image data to PIL Image
    image = Image.open(image_data)

    # Convert image to uint8 numpy array
    image_array = np.array(image, dtype=np.uint8)

    # You can now process the image_array as needed

    return jsonify({"status": "success", "message": "Image processed"})

if __name__ == '__main__':
    app.run(debug=True)