import cv2
import os
import json
import numpy as np

def process_sign_language_videos():
    # Paths to the dataset
    VIDEOS_PATH = 'C:\\Users\\abhir\\helloWorld\\RealTimeObjectDetection\\Tensorflow\\workspace\\dataset'

    # Load the WLASL glossary and instances from JSON file
    with open('C:\\Users\\abhir\\OneDrive\\Documents\\GitHub\\HelloWorld\\WLASL_v0.3.json', 'r') as f:
        wlasl_data = json.load(f)

    # Number of frames to extract per video
    number_imgs = 25

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
                continue

            cap = cv2.VideoCapture(video_file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            sample_rate = fps
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

    # Structure of the Output
    # - List of lists of frames: [[all frames of video1], [all frames of video2], ...]
    # - List of glosses: [glossOfVideo1, glossOfVideo2, ...]

    return frames_list, glosses_list

def createFile():

    # Call the function to process the videos
    frames_list, glosses_list = process_sign_language_videos()

    # Save frames_list to one .npz file
    np.savez("frames_data.npz", *frames_list)

    # Save glosses_list to another .npz file
    with open('glosses_data.txt', 'w') as f:
        for line in glosses_list:
            f.write(line + '\n')

def load_data():
    frame_numpy_dict = np.load("frames_data.npz")
    print(frame_numpy_dict)

    frames_list = []
    glosses_list = []

    keys = frame_numpy_dict.files
    
    for key in keys:
        frames_list.append(frame_numpy_dict[key])

    with open('glosses_data.txt', 'r') as file:
        glosses_list = file.readlines()
    glosses_list = [line.strip() for line in glosses_list]

    # print(frames_list, glosses_list)
    # print(len(frames_list), len(glosses_list))

    print("Arrays in the .npz file:")

    for array_name in frame_numpy_dict.files:
        # print(array_name)
        # print(frame_numpy_dict[array_name])  # This will print the entire array

        # Optional: Print the shape of each array
        print(f"Shape of {array_name}: {frame_numpy_dict[array_name].shape}")

    return frames_list, glosses_list

load_data()