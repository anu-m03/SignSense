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
            nn.MaxPool2d(kernel_size=2, stride=2)    # Output: 32 x 45 x 30
        )

        # Flattened feature size: 32 * 45 * 30 = 43200
        # LSTM for temporal feature learning
        self.lstm = nn.LSTM(input_size=43200, hidden_size=128, batch_first=True)
        
        # Fully connected layer for classification
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        batch_size, channels, num_frames, height, width = x.size()
        
        # Apply CNN to each frame in the sequence
        cnn_features = []
        for t in range(num_frames):
            # Extract features from the t-th frame
            cnn_out = self.cnn(x[:, :, t, :, :])  # Shape: (batch_size, 32, 45, 30)
            cnn_out = cnn_out.view(batch_size, -1)  # Flatten: (batch_size, 43200)
            cnn_features.append(cnn_out)

        # Stack features across time steps to create a sequence for LSTM
        cnn_features = torch.stack(cnn_features, dim=1)  # Shape: (batch_size, num_frames, 43200)
        
        # LSTM processing
        lstm_out, _ = self.lstm(cnn_features)
        
        # Final classification based on the last LSTM output
        output = self.fc(lstm_out[:, -1, :])  # Shape: (batch_size, num_classes)
        
        return output