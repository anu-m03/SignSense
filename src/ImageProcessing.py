import numpy
import cv2
import torch
import numpy as np
import json
import os
from CNN_LSTM_Model import CNN_LSTM_Model

frames = []
def build_frames_list(self, input_frame):
    frames.insert(0, input_frame)
    if len(frames) > 28:
        frames.pop(29)

def test_model_with_frames(model, frames_list, gloss_to_label):
    # Ensure frames_list is capped at 28 frames (or whatever is appropriate)
    if len(frames_list) > 28:
        frames_list = frames_list[-28:]  # Keep only the last 28 frames

    # Convert the list of frames to a PyTorch tensor
    frames_tensor = torch.tensor(frames_list, dtype=torch.float32)  # Shape: (num_frames, channels, height, width)
    
    # Add batch dimension
    frames_tensor = frames_tensor.unsqueeze(0)  # Shape: (1, num_frames, channels, height, width)

    # Make prediction
    with torch.no_grad():
        outputs = model(frames_tensor)
        _, predicted = torch.max(outputs, 1)  # Get the predicted class index

    # Map predicted class index to ASL gloss
    label_to_gloss = {v: k for k, v in gloss_to_label.items()}
    predicted_gloss = label_to_gloss[predicted.item()]  # Get the corresponding ASL sign
    
    return predicted_gloss

def process_sign_language_video():
    # Paths to the dataset
    VIDEOS_PATH = 'C:\\Users\\henry\\OneDrive\\Documents\\VideosHelloWorldTwo'
    # Load the WLASL glossary and instances from JSON file
    with open('C:\\Users\\henry\\OneDrive\\Documents\\GitHub\\HelloWorld\\WLASL_v0.3.json', 'r') as f:
        wlasl_data = json.load(f)

    # Number of frames to extract per video
    number_imgs = 30

    # Initialize lists to store frames and glosses
    frames_list = []
    glosses_list = []

    common_glosses = []
    with open('common_glosses.txt', 'r') as file:
        common_glosses = file.readlines()
    common_glosses = [line.strip() for line in common_glosses]

    # Process each video in the dataset
    video_num = 1
    for entry in wlasl_data:
        gloss = entry['gloss']
        if gloss in common_glosses:
            for instance in entry['instances']:
                video_id = instance['video_id']
                video_file = os.path.join(VIDEOS_PATH, f"{video_id}.mp4")
                if not os.path.isfile(video_file):
                    continue

                cap = cv2.VideoCapture(video_file)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                sample_rate = fps
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                img_count = 0
                frame_count = 0

                # List to hold the frames for the current video
                video_frames = []

                # Loop through frames in the video
                while cap.isOpened() and img_count < number_imgs:
                    # print(img_count)
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Sample every nth frame to achieve 1 fps
                    # if frame_count % sample_rate == 0:
                    if int(frame_count / total_frames) % total_frames / 35 == 0:
                        # Resize the frame to 180x120 pixels
                        resized_frame = cv2.resize(frame, (180, 120))

                        # Convert the frame to numpy array and add to list
                        video_frames.append(resized_frame)
                        img_count += 1

                    frame_count += 1
                cap.release()

                if len(video_frames) == 30:
                    # Remove the first and last frames
                    if len(video_frames) > 2:
                        video_frames = video_frames[1:-1]

                    # Append frames and gloss to respective lists
                    frames_list.append(np.array(video_frames))
                    glosses_list.append(gloss)

            video_num += 1
            print(f"Gloss {video_num} Processed")

    # Structure of the Output
    # - List of lists of frames: [[all frames of video1], [all frames of video2], ...]
    # - List of glosses: [glossOfVideo1, glossOfVideo2, ...]

    return frames_list, glosses_list