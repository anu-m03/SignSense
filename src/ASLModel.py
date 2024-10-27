import torch
import numpy as np
from CNN_LSTM_Model import CNN_LSTM_Model

class ASLModel:
    def __init__(self, model_path, gloss_to_label):
        self.model = self.load_model(model_path, len(gloss_to_label))
        self.gloss_to_label = gloss_to_label
        self.label_to_gloss = {v: k for k, v in gloss_to_label.items()}

    def load_model(self, model_path, num_classes):
        model = CNN_LSTM_Model(num_classes)
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model

    def preprocess_frames(self, frames):
        # Convert frames to tensor and reshape
        frames_tensor = torch.tensor(frames, dtype=torch.float32).permute(0, 3, 1, 2).unsqueeze(0)
        return frames_tensor

    def predict_sign(self, frames):
        frames_tensor = self.preprocess_frames(frames)
        with torch.no_grad():
            outputs = self.model(frames_tensor)
            _, predicted = torch.max(outputs, 1)
        predicted_gloss = self.label_to_gloss[predicted.item()]
        return predicted_gloss

def create_gloss_to_label(file_path):
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

# Example usage
model_path = 'asl_model.pth'
gloss_to_label = create_gloss_to_label("common_glosses.txt")

asl_model = ASLModel(model_path, gloss_to_label)

# Example frames input
frames = np.random.rand(28, 180, 120, 3)  # Replace with actual frame data
predicted_sign = asl_model.predict_sign(frames)
print(f"The predicted ASL sign is: {predicted_sign}")