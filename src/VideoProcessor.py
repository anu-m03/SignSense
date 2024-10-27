# video_processor.py

import numpy as np
import cv2
import json
import os
from ASLModel import create_gloss_to_label, ASLModel

class VideoProcessor:
    def __init__(self, videos_path, common_glosses, number_imgs=30):
        self.videos_path = videos_path
        self.common_glosses = common_glosses
        self.number_imgs = number_imgs

    def process_sign_language_video(self):
        # Load the WLASL glossary and instances from JSON file
        with open('C:\Users\abhir\OneDrive\Documents\GitHub\HelloWorld', 'r') as f:
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
    gloss_to_label = create_gloss_to_label("common_glosses.txt")

    asl_model = ASLModel(model_path, gloss_to_label)

    # Paths to the dataset
    VIDEOS_PATH = 'C:\Users\abhir\OneDrive\Documents\GitHub\HelloWorld\dataset'

    # Load common glosses
    with open('common_glosses.txt', 'r') as file:
        common_glosses = [line.strip() for line in file.readlines()]

    # Create VideoProcessor instance
    video_processor = VideoProcessor(VIDEOS_PATH, common_glosses)

    # Process videos to get frames and glosses
    frames_list, glosses_list = video_processor.process_sign_language_video()
    print(frames_list[0].shape)

    # Make predictions for each set of frames
    for frames in frames_list:
        predicted_sign = asl_model.predict_sign(frames)
        print(f"The predicted ASL sign is: {predicted_sign}")
