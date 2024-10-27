# ASL to Text Converter

## About The Project - SignSense

This project implements an American Sign Language (ASL) to text converter that leverages video frame extraction and classification to recognize ASL glosses and convert them into text. The converter uses a combination of CNN (Convolutional Neural Network) layers for spatial feature extraction and an LSTM (Long Short-Term Memory) network for temporal sequence learning, processing video frames to recognize ASL signs with high accuracy.

### Innovative Elements:

- Frame-by-Frame Processing: Real-time feature extraction enables accurate spatial recognition of hand gestures.
- Temporal Consistency: The LSTM module preserves temporal order, ensuring gesture sequences are accurately interpreted across video frames.
- Applications Beyond Translation: From assistive devices to educational tools, this model provides real-time transcription support and has potential for bi-directional communication when combined with speech recognition.

The ASL to Text Converter holds promise for improving accessibility in everyday communication and education, with future potential to support multi-language translation and real-time ASL recognition in various environments.

---

## Built With

This project utilizes several Python libraries and frameworks:
- **OpenCV** for video processing
- **NumPy** for data handling and matrix operations
- **PyTorch** for deep learning (CNN and LSTM networks)
- **JSON** for loading ASL gloss data
  
---

## Applications

### Current Applications
1. **ASL Transcription Tools**: Transcribes ASL signs into text. It provides support for non-ASL speakers to better understand the DHH community.
2. **Assistive Technologies**: Can be integrated into devices like phones or tablets to provide on-the-go ASL translation.
3. **Educational Resources**: Enhances language learning for both ASL learners and the hearing community by visualizing translations in real time.

### Future Potential
1. **Real-time Translation**: With further optimization, this model could provide real-time translation, making it highly useful in classrooms, workplaces, and public spaces.
2. **Speech-to-Sign Conversion**: By integrating speech recognition, this project could eventually support bi-directional communication.
3. **Multi-Language Support**: Future versions could recognize additional sign languages and output translated text in multiple spoken languages.

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system.
- **OpenCV**: Install using `pip install opencv-python`
- **PyTorch**: Install the appropriate PyTorch version from [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)
- **NumPy**: Install with `pip install numpy`

### Installation

1. **Clone the Repository**  
   ```
   git clone https://github.com/your_username/ASL_Text_Converter.git
   cd ASL_Text_Converter
   ```

2. **Set up the WLASL Dataset**  
   Download the WLASL dataset and place it in the specified path:
   ```bash
   VIDEOS_PATH = 'C:\\Users\\abhir\\helloWorld\\RealTimeObjectDetection\\Tensorflow\\workspace\\dataset'
   ```

3. **Load Gloss Data**  
   Place the `WLASL_v0.3.json` file in the repository to access gloss information:
   ```bash
   with open('C:\\Users\\abhir\\OneDrive\\Documents\\GitHub\\HelloWorld\\WLASL_v0.3.json', 'r') as f:
       wlasl_data = json.load(f)
   ```

4. **Prepare Data for Training**  
   Run `createFile()` in the code to preprocess and save video frames and gloss data into `.npz` and `.txt` files.

---

## Usage

This ASL to text converter can be trained and tested using the provided code. 

### Model Training

1. **Load Data**  
   Use `load_data()` to load the preprocessed frame and gloss data for training.

2. **Train the Model**  
   Use the training loop provided to train the CNN-LSTM model over a specified number of epochs. Training is configured with:
   - **Cross Entropy Loss** for classification
   - **Adam Optimizer** with a learning rate of 0.0007

3. **Monitor Model Performance**  
   The model prints the loss per epoch, providing insight into model convergence.

### Example Output

Upon successful training, the model outputs predicted glosses corresponding to ASL signs in the videos. These glosses can then be post-processed to form coherent English statements.

---

## Roadmap

- Add support for additional sign languages
- Implement real-time ASL detection and conversion
- Add multi-language text output

---

## Acknowledgments

Special thanks to resources that made this project possible:
- [WLASL Dataset](https://example.com)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [OpenCV Documentation](https://docs.opencv.org/master/)
