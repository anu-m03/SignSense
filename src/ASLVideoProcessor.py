from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import json
import os
import torch
from CNN_LSTM_Model import CNN_LSTM_Model
import threading

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'src/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ASLVideoProcessor:
    def __init__(self, model_path, gloss_file_path, common_glosses, number_imgs=28):
        self.model, self.label_to_gloss = self.load_model(model_path, gloss_file_path)
        self.common_glosses = common_glosses
        self.number_imgs = number_imgs

    def create_gloss_to_label(self, file_path):
        glosses = set()  # Use a set to ensure uniqueness
        
        # Read the glosses from the file
        with open(file_path, 'r') as file:
            for line in file:
                gloss = line.strip()  # Remove any leading/trailing whitespace
                if gloss:  # Ensure the line is not empty
                    glosses.add(gloss)
        
        # Create the mapping from glosses to integer labels
        gloss_to_label = {gloss: idx for idx, gloss in enumerate(sorted(glosses))}
        print(gloss_to_label)
        
        return gloss_to_label

    def load_model(self, model_path, gloss_file_path):
        gloss_to_label = self.create_gloss_to_label(gloss_file_path)
        label_to_gloss = {v: k for k, v in gloss_to_label.items()}
        
        model = CNN_LSTM_Model(len(gloss_to_label))
        model.load_state_dict(torch.load(model_path))
        model.eval()
        
        return model, label_to_gloss

    def preprocess_frames(self, frames):
        # print("\nProcessing Frames...\n")
        frames_tensor = torch.from_numpy(frames).float() / 255.0  # Normalize to [0, 1]
        #print("Shape of frames_tensor before permute:", frames_tensor.shape)
        frames_tensor = frames_tensor.permute(3, 0, 1, 2)  # Change to (channels, num_frames, height, width)
        frames_tensor = frames_tensor.unsqueeze(0)  # Add batch dimension
        return frames_tensor

    def predict_sign(self, frames):
        frames_tensor = self.preprocess_frames(frames)
        with torch.no_grad():
            outputs = self.model(frames_tensor)
            # print("Model outputs (logits):", outputs)
            _, predicted = torch.max(outputs, 1)
    
        predicted_gloss = self.label_to_gloss[predicted.item()]
        return predicted_gloss

    def process_received_image(self, image_path='src/uploads/received_image.png'):
        if os.path.isfile(image_path):
            frame = cv2.imread(image_path)
            resized_frame = cv2.resize(frame, (180, 120))
            return resized_frame
        
        return None  # Return None if the image is not found

    def run_infinite_loop(self):
        video_frames = []
        
        while True:
            frame = self.process_received_image()
            if frame is not None:
                video_frames.append(frame)
                
                if len(video_frames) == self.number_imgs:
                    frames_array = np.array(video_frames)
                    predicted_sign = self.predict_sign(frames_array)
                    print(f"The predicted ASL sign is: {predicted_sign}")
                    video_frames.clear()

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image data found'}), 400
    
    image_file = request.files['image']
    save_path = os.path.join(UPLOAD_FOLDER, "received_image.png")
    image_file.save(save_path)
    # print(f"Image saved to {save_path}")
    
    # return jsonify({'message': 'Image saved successfully!'}), 200

def run_flask_app():
    app.run(debug=True)

if __name__ == "__main__":
    model_path = 'asl_model.pth'
    gloss_file_path = 'common_glosses.txt'
    
    # Load common glosses
    with open(gloss_file_path, 'r') as file:
        common_glosses = [line.strip() for line in file.readlines()]
    
    # Create ASLVideoProcessor instance
    asl_video_processor = ASLVideoProcessor(model_path, gloss_file_path, common_glosses)
    
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask_app, daemon=True).start()

    # Start the infinite loop to process images
    asl_video_processor.run_infinite_loop()

def process_folder_images(self, folder_path):
    video_frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            frame = cv2.imread(image_path)
            if frame is not None:
                resized_frame = cv2.resize(frame, (180, 120))
                video_frames.append(resized_frame)
                
                if len(video_frames) == self.number_imgs:
                    frames_array = np.array(video_frames)
                    predicted_sign = self.predict_sign(frames_array)
                    print(f"The predicted ASL sign is: {predicted_sign}")
                    video_frames.clear()
    return video_frames
