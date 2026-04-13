import librosa
import numpy as np

class AudioModel:
    def __init__(self):
        # We would typically load a whisper model or a custom audio classifier here
        # For memory/speed in this hackathon setup, we mock the heavy whisper load and use keyword matching
        self.emergency_keywords = ["help", "fire", "accident", "emergency", "police", "ambulance"]

    def analyze(self, audio_path):
        # In a real implementation:
        # 1. Load audio with librosa: y, sr = librosa.load(audio_path)
        # 2. Extract features or pass to Whisper for transcription 
        # text = whisper_model.transcribe(audio_path)
        
        # Dummy mock output for demonstration:
        # Assuming the audio gets transcribed to:
        transcription = "help there is a fire here" 
        
        detected_keywords = [word for word in self.emergency_keywords if word in transcription.lower()]
        
        crisis_found = len(detected_keywords) > 0
        severity = "HIGH" if crisis_found else "LOW"
        
        return {
            "crisis": crisis_found,
            "transcription": transcription,
            "detected_keywords": detected_keywords,
            "severity": severity
        }

audio_model = AudioModel()
