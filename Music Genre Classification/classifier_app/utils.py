import os
import librosa
import numpy as np
import tensorflow as tf
from tensorflow.image import resize
from django.conf import settings

# Load model globally to avoid loading it on every request
MODEL_PATH = os.path.join(settings.BASE_DIR, "Trained_model.keras")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

CLASSES = ['blues', 'classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

def load_and_preprocess_data(file_path, target_shape=(150, 150)):
    data = []
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    
    chunk_duration = 4  # seconds
    overlap_duration = 2  # seconds
                
    chunk_samples = chunk_duration * sample_rate
    overlap_samples = overlap_duration * sample_rate
                
    num_chunks = int(np.ceil((len(audio_data) - chunk_samples) / (chunk_samples - overlap_samples))) + 1
                
    for i in range(num_chunks):
        start = i * (chunk_samples - overlap_samples)
        end = start + chunk_samples
                    
        chunk = audio_data[start:end]
                    
        mel_spectrogram = librosa.feature.melspectrogram(y=chunk, sr=sample_rate)
        mel_spectrogram = resize(np.expand_dims(mel_spectrogram, axis=-1), target_shape)
        data.append(mel_spectrogram)
    
    return np.array(data)

def model_prediction(X_test):
    if model is None:
        raise ValueError("Model is not loaded.")
        
    y_pred = model.predict(X_test, verbose=0)
    predicted_categories = np.argmax(y_pred,axis=1)
    unique_elements, counts = np.unique(predicted_categories, return_counts=True)
    max_count = np.max(counts)
    max_elements = unique_elements[counts == max_count]
    c_index = max_elements[0]
    return CLASSES[c_index]

def predict_genre(audio_path):
    X_test = load_and_preprocess_data(audio_path)
    genre = model_prediction(X_test)
    return genre
