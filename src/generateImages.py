import cv2
import os
import json
import numpy as np

def process_sign_language_videos():
    # Paths to the dataset
    VIDEOS_PATH = 'C:\\Users\\abhir\\helloWorld\\RealTimeObjectDetection\\Tensorflow\\workspace\\video-dataset'
    OUTPUT_PATH = 'C:\\Users\\abhir\\helloWorld\\RealTimeObjectDetection\\Tensorflow\\workspace\\images\\collectedImages'

    # Load the WLASL glossary and instances from JSON file
    with open('C:\\Users\\abhir\\helloWorld\\RealTimeObjectDetection\\Tensorflow\\scripts\\WLASL_v0.3.json', 'r') as f:
        wlasl_data = json.load(f)

    # Number of frames to extract per video
    number_imgs = 60

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Initialize lists to store frames and glosses
    frames_list = []
    glosses_list = []

    # Process each video in the dataset
    for entry in wlasl_data:
        gloss = entry['gloss']
        for instance in entry['instances']:
            video_id = instance['video_id']
            video_file = os.path.join(VIDEOS_PATH, f"{video_id}.mp4")
            if not os.path.isfile(video_file):
                print(f"Video file {video_file} not found, skipping.")
                continue

            cap = cv2.VideoCapture(video_file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            sample_rate = fps

            print(f"Collecting frames from video_id {video_id}")
            img_count = 0
            frame_count = 0

            # List to hold the frames for the current video
            video_frames = []

            # Loop through frames in the video
            while cap.isOpened() and img_count < number_imgs:
                ret, frame = cap.read()
                if not ret:
                    break

                # Sample every nth frame to achieve 1 fps
                if frame_count % sample_rate == 0:
                    # Resize the frame to 180x120 pixels
                    resized_frame = cv2.resize(frame, (180, 120))

                    # Convert the frame to numpy array and add to list
                    video_frames.append(resized_frame)
                    img_count += 1

                frame_count += 1
            cap.release()

            # Remove the first and last frames
            if len(video_frames) > 2:
                video_frames = video_frames[1:-1]

            # Append frames and gloss to respective lists
            frames_list.append(np.array(video_frames))
            glosses_list.append(gloss)

    print("Data collection complete.")
    return frames_list, glosses_list

# Store the output
frames_data, glosses_data = process_sign_language_videos()

# Structure of the Output
# - List of lists of frames: [[all frames of video1], [all frames of video2], ...]
# - List of glosses: [glossOfVideo1, glossOfVideo2, ...]
