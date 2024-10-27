# ASL to Text Converter

## About The Project - SignSense

This project implements an American Sign Language (ASL) to text converter that leverages video frame extraction and classification to recognize ASL glosses and convert them into text. The converter uses a combination of CNN (Convolutional Neural Network) layers for spatial feature extraction and an LSTM (Long Short-Term Memory) network for temporal sequence learning, processing video frames to recognize ASL signs with high accuracy.

### Innovative Elements:

- Frame-by-Frame Processing: Real-time feature extraction enables accurate spatial recognition of hand gestures.
- Temporal Consistency: The LSTM module preserves temporal order, ensuring gesture sequences are accurately interpreted across video frames.
- Applications Beyond Translation: From assistive devices to educational tools, this model provides real-time transcription support and has potential for bi-directional communication when combined with speech recognition.

The ASL to Text Converter holds promise for improving accessibility in everyday communication and education, with future potential to support multi-language translation and real-time ASL recognition in various environments.

---

### Built With
- **OpenCV**: For video processing, resizing, and frame extraction
- **NumPy**: For handling and storing frame arrays
- **PyTorch**: For building the CNN and LSTM networks
- **Flask**: For the web interface to upload images and receive ASL predictions
- **Flask-CORS**: To enable CORS in the Flask API for cross-origin requests
- **JSON**: For loading WLASL gloss data

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
- Python 3.x: Ensure Python is installed on your system.
- OpenCV: Install using `pip install opencv-python`
- NumPy: Install with `pip install numpy`
- PyTorch: Install the appropriate PyTorch version from https://pytorch.org/get-started/locally/
- Flask: Install with `pip install Flask`
- Flask-CORS: Install with `pip install Flask-CORS`
- JSON: Included in the Python Standard Library (used for loading ASL gloss data)

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

- **Additional Sign Language Support**: Extend functionality to recognize more sign languages beyond ASL.
- **Enhanced Real-Time Processing**: Optimize the model for faster processing to achieve real-time ASL recognition and conversion.
- **Bi-Directional Communication**: Integrate a speech-to-sign component for fluid two-way communication.
- **Multi-Language Output**: Enable the model to translate ASL glosses into various spoken languages, broadening its accessibility.
- **Mobile and Web Integration**: Adapt the model for use on mobile devices and web applications, expanding its reach and practical usage.

---

## Acknowledgments

Special thanks to resources that made this project possible:

- [WLASL Dataset](https://dxli94.github.io/WLASL/): For providing the video dataset of ASL glosses used to train and validate the model.
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html): For offering extensive resources and tools for deep learning model development.
- [OpenCV Documentation](https://docs.opencv.org/master/): For guidance on using computer vision techniques for video frame processing.
- [Flask Documentation](https://flask.palletsprojects.com/): For facilitating the API setup to enable ASL translation in real-time applications.
