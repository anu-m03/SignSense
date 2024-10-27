from flask import Flask, request, jsonify
import base64
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get the JSON data
    data = request.form.get('data')
    
    # Ensure image data is provided
    if 'image' not in data:
        return jsonify({'error': 'No image data found'}), 400
    
    # Get the base64 image string
    image_b64 = data['image']
    
    # Convert Base64 string to a NumPy array
    np_image = convert_base64_to_uint8(image_b64)
    
    # For example purposes, we can return the shape of the array
    return jsonify({'shape': np_image.shape})

def convert_base64_to_uint8(image_b64):
    # Decode the Base64 string
    image_data = base64.b64decode(image_b64.split(',')[1])  # Split at comma if it contains data type prefix
    image = Image.open(BytesIO(image_data)).convert('RGB')
    
    # Convert image to NumPy array
    np_image = np.array(image, dtype=np.uint8)
    return np_image

if __name__ == '__main__':
    app.run(debug=True)