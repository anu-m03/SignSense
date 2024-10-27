from flask import Flask, request, jsonify
from flask_cors import CORS
import base64



app = Flask(__name__)
CORS(app)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get the JSON data
    data = request.form.get('data')
    
    # Ensure image data is provided
    if 'image' not in data:
        return jsonify({'error': 'No image data found'}), 400
    
    # Get the base64 image string
    image_b64 = data
    
    return jsonify(image_b64)

if __name__ == '__main__':
    app.run(debug=True)

