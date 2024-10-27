# import torch
# from CNN_LSTM_Model import CNN_LSTM_Model

# class ASLModel:
#     def __init__(self, model_path, gloss_to_label):
#         self.model = self.load_model(model_path, len(gloss_to_label))
#         self.gloss_to_label = gloss_to_label
#         self.label_to_gloss = {v: k for k, v in gloss_to_label.items()}

#     def load_model(self, model_path, num_classes):
#         model = CNN_LSTM_Model(num_classes)
#         model.load_state_dict(torch.load(model_path))
#         model.eval()
#         return model

#     def preprocess_frames(self, frames):
#         print("\nAAAA\n")
#         # Convert frames to tensor
#         frames_tensor = torch.from_numpy(frames)
#         print("Shape of frames_tensor 1:", frames_tensor.shape)
#         frames_tensor = frames_tensor.permute(3, 0, 1, 2)
#         # 1 28 3 120 180
#         frames_tensor = frames_tensor.flatten(0)
#         return frames_tensor

#     def predict_sign(self, frames):
#         frames_tensor = self.preprocess_frames(frames)
#         print("Shape of frames_tensor 2:", frames_tensor.shape)  # Should print (1, 28, 3, 120, 180)

#         with torch.no_grad():
#             outputs = self.model(frames_tensor)
#             _, predicted = torch.max(outputs, 1)
        
#         predicted_gloss = self.label_to_gloss[predicted.item()]
#         return predicted_gloss

# def create_gloss_to_label(file_path):
#     glosses = set()  # Use a set to ensure uniqueness
    
#     # Read the glosses from the file
#     with open(file_path, 'r') as file:
#         for line in file:
#             gloss = line.strip()  # Remove any leading/trailing whitespace
#             if gloss:  # Ensure the line is not empty
#                 glosses.add(gloss)
    
#     # Create the mapping from glosses to integer labels
#     gloss_to_label = {gloss: idx for idx, gloss in enumerate(sorted(glosses))}
    
#     return gloss_to_label