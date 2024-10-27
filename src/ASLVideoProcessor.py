import numpy as np
import cv2
import json
import os
import torch
from CNN_LSTM_Model import CNN_LSTM_Model

class ASLVideoProcessor:
    def __init__(self, model_path, gloss_file_path, videos_path, common_glosses, number_imgs=30):
        self.model = self.load_model(model_path, gloss_file_path)
        self.videos_path = videos_path
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
        
        return gloss_to_label

    def load_model(self, model_path, gloss_file_path):
        gloss_to_label = self.create_gloss_to_label(gloss_file_path)
        label_to_gloss = {v: k for k, v in gloss_to_label.items()}
        
        model = CNN_LSTM_Model(len(gloss_to_label))
        model.load_state_dict(torch.load(model_path))
        model.eval()
        
        return model, label_to_gloss

    def preprocess_frames(self, frames):
        print("\nProcessing Frames...\n")
        # Convert frames to tensor
        frames_tensor = torch.from_numpy(frames)
        print("Shape of frames_tensor before permute:", frames_tensor.shape)
        frames_tensor = frames_tensor.permute(3, 0, 1, 2)  # Change to (channels, num_frames, height, width)
        frames_tensor = frames_tensor.unsqueeze(0)  # Add batch dimension
        return frames_tensor

    def predict_sign(self, frames):
        frames_tensor = self.preprocess_frames(frames)
        print("Shape of frames_tensor after preprocessing:", frames_tensor.shape)  # Should print (1, 3, 28, 120, 180)

        with torch.no_grad():
            outputs = self.model(frames_tensor)
            _, predicted = torch.max(outputs, 1)
        
        predicted_gloss = self.label_to_gloss[predicted.item()]
        return predicted_gloss

    def process_sign_language_video(self):
        # Load the WLASL glossary and instances from JSON file
        with open('C:\\Users\\henry\\OneDrive\\Documents\\GitHub\\HelloWorld\\WLASL_v0.3.json', 'r') as f:
            wlasl_data = json.load(f)

        # Initialize lists to store frames and glosses
        frames_list = []
        glosses_list = []

        # Process each video in the dataset
        for entry in wlasl_data:
            gloss = entry['gloss']
            if gloss in self.common_glosses:
                for instance in entry['instances']:
                    video_id = instance['video_id']
                    video_file = os.path.join(self.videos_path, f"{video_id}.mp4")
                    if not os.path.isfile(video_file):
                        continue

                    cap = cv2.VideoCapture(video_file)
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    img_count = 0
                    frame_count = 0

                    # List to hold the frames for the current video
                    video_frames = []

                    # Loop through frames in the video
                    while cap.isOpened() and img_count < self.number_imgs:
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # Sample every nth frame to achieve 1 fps
                        if frame_count % (total_frames // self.number_imgs) == 0:
                            # Resize the frame to 180x120 pixels
                            resized_frame = cv2.resize(frame, (180, 120))
                            video_frames.append(resized_frame)
                            img_count += 1

                        frame_count += 1
                    cap.release()

                    if len(video_frames) == self.number_imgs:
                        # Remove the first and last frames
                        if len(video_frames) > 2:
                            video_frames = video_frames[1:-1]

                        # Append frames and gloss to respective lists
                        frames_list.append(np.array(video_frames))
                        glosses_list.append(gloss)

        return frames_list, glosses_list

# Example usage
if __name__ == "__main__":
    model_path = 'asl_model.pth'
    gloss_file_path = 'common_glosses.txt'
    VIDEOS_PATH = 'C:\\Users\\henry\\OneDrive\\Documents\\VideosHelloWorldTwo'

    # Load common glosses
    with open(gloss_file_path, 'r') as file:
        common_glosses = [line.strip() for line in file.readlines()]

    # Create ASLVideoProcessor instance
    asl_video_processor = ASLVideoProcessor(model_path, gloss_file_path, VIDEOS_PATH, common_glosses)

    # Process videos to get frames and glosses
    frames_list, glosses_list = asl_video_processor.process_sign_language_video()
    print(frames_list[0].shape)

    # Make predictions for each set of frames
    for frames in frames_list:
        predicted_sign = asl_video_processor.predict_sign(frames)
        print(f"The predicted ASL sign is: {predicted_sign}")
