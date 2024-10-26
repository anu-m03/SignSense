import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import utils
import CNN_LSTM_Model
import generateImages

# Given data
video_frames_list, glosses_list = generateImages.process_sign_language_videos()

# Create a mapping from glosses to integer labels
gloss_to_label = {gloss: idx for idx, gloss in enumerate(set(glosses_list))}
labels_list = [gloss_to_label[gloss] for gloss in glosses_list]  # Convert glosses to integer labels
num_classes = len(gloss_to_label)  # Number of unique glosses

# Initialize dataset and DataLoader
train_dataset = utils.VideoDataset(videos=video_frames_list, labels=labels_list, transform=None)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

# Initialize model, loss function, and optimizer
model = CNN_LSTM_Model(num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Training Loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for i, (videos, labels) in enumerate(train_loader):
        # Move data to the configured device
        videos = videos.to(device)
        labels = labels.to(device)
        
        # Forward pass
        outputs = model(videos)
        loss = criterion(outputs, labels)
        
        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Track the running loss
        running_loss += loss.item()
    
    # Print average loss for the epoch
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}")

print("Training complete!")