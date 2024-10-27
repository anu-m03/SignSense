from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import os


app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = 'src\\uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    
    # Ensure image data is provided
    if 'image' not in request.files:
        return jsonify({'error': 'No image data found'}), 400
    
    image_file = request.files['image']

    save_path = os.path.join(UPLOAD_FOLDER, "received_image.png")

    image_file.save(save_path)
    print(image_file)
    
    return jsonify({'message': 'image saved successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

