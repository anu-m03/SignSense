import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import utils
from CNN_LSTM_Model import CNN_LSTM_Model
import generateImages

# Given data
video_frames_list, glosses_list = generateImages.load_data()

# Create a mapping from glosses to integer labels
gloss_to_label = {gloss: idx for idx, gloss in enumerate(set(glosses_list))}
labels_list = [gloss_to_label[gloss] for gloss in glosses_list]  # Convert glosses to integer labels
num_classes = len(gloss_to_label)  # Number of unique glosses

# Initialize dataset and DataLoader
full_dataset = utils.VideoDataset(videos=video_frames_list, labels=labels_list, transform=None)

# Split the dataset into training and validation sets (80% train, 20% val)
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

# Initialize model, loss function, and optimizer
model = CNN_LSTM_Model(num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Initialize the learning rate scheduler
# Initialize the learning rate scheduler
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)

# Training Loop
num_epochs = 10
print("Start Training:")
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
    avg_loss = running_loss / len(train_loader)
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

    # Validation Phase
    model.eval()  # Set the model to evaluation mode
    val_loss = 0.0
    with torch.no_grad():  # Disable gradient computation
        for videos, labels in val_loader:
            videos = videos.to(device)
            labels = labels.to(device)
            outputs = model(videos)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

    avg_val_loss = val_loss / len(val_loader)
    print(f"Validation Loss: {avg_val_loss:.4f}")

    # Step the scheduler based on validation loss
    scheduler.step(avg_val_loss)

    # Print the current learning rate
    current_lr = scheduler.optimizer.param_groups[0]['lr']
    print(f"Learning Rate: {current_lr:.6f}")

print("Training complete!")
