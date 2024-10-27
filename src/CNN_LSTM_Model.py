import torch
import torch.nn as nn

class CNN_LSTM_Model(nn.Module):
    def __init__(self, num_classes):
        super(CNN_LSTM_Model, self).__init__()
        
        # CNN layers for spatial feature extraction from each frame
        self.cnn = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),   # Output: 16 x 90 x 60
            
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),   # Output: 32 x 45 x 30
            
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),   # Output: 64 x 22 x 15
            
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),   # Output: 128 x 11 x 7
            
            nn.AdaptiveAvgPool2d((1, 1))             # Output: 128 x 1 x 1
        )

        # Flatten layer to convert 128 x 1 x 1 to a 128-dimensional vector
        self.flatten = nn.Flatten()
        
        # Additional fully connected layer to reduce dimensionality to 512
        self.fc_reduce = nn.Linear(128, 512)

        # LSTM for temporal feature learning
        self.lstm = nn.LSTM(input_size=512, hidden_size=128, batch_first=True)
        
        # Fully connected layer for classification
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        batch_size, channels, num_frames, height, width = x.size()
        
        # Apply CNN to each frame in the sequence
        cnn_features = []
        for t in range(num_frames):
            # Extract features from the t-th frame
            cnn_out = self.cnn(x[:, :, t, :, :])  # Shape: (batch_size, 128, 1, 1)
            cnn_out = self.flatten(cnn_out)         # Shape: (batch_size, 128)
            cnn_out = self.fc_reduce(cnn_out)       # Reduce to 512 dimensions
            cnn_features.append(cnn_out)

        # Stack features across time steps to create a sequence for LSTM
        cnn_features = torch.stack(cnn_features, dim=1)  # Shape: (batch_size, num_frames, 512)
        
        # LSTM processing
        lstm_out, _ = self.lstm(cnn_features)
        
        # Final classification based on the last LSTM output
        output = self.fc(lstm_out[:, -1, :])  # Shape: (batch_size, num_classes)
        
        return output
