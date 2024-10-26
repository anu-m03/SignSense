import torch
from torch.utils.data import Dataset

class VideoDataset(Dataset):
    def __init__(self, videos, labels, transform=None):
        self.videos = videos  # List of lists of frames for each video
        self.labels = labels  # List of integer labels corresponding to each video
        self.transform = transform

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, idx):
        video_frames = self.videos[idx]  # Get list of frames for one video
        label = self.labels[idx]

        # Convert each frame in the video sequence to a tensor
        frames = [torch.tensor(frame, dtype=torch.float32) for frame in video_frames]
        
        # Stack frames along the time dimension: (num_frames, height, width, channels)
        video_tensor = torch.stack(frames)
        
        # Permute dimensions to match PyTorch format (channels, num_frames, height, width)
        video_tensor = video_tensor.permute(3, 0, 1, 2)

        # Apply any transformations if provided
        if self.transform:
            video_tensor = self.transform(video_tensor)
        
        return video_tensor, label