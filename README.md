# OmniAssist – Crisis Detection & Response System

OmniAssist is a scalable, multi-modal AI system combining Computer Vision, Audio Processing, and NLP to detect real-time emergency situations (accidents, fires, distress signals). 

## Architecture
- **Backend:** FastAPI (Python), Motor (MongoDB Async), WebSockets
- **Models:** YOLOv8 (Vision), Whisper/Librosa (Audio Mocked), BERT/Pipelines (NLP)
- **Frontend:** React, Vite, Tailwind CSS, Leaflet

## Features
- Scalable microservice structure
- Intelligent Decision Engine for multimodal fusion
- Event Mapping using React-Leaflet
- Dijkstra Route Optimization

## Setup Instructions

### 1. MongoDB Setup
Ensure you have MongoDB running locally on port `27017` or change the `MONGO_URL` in `backend/core/db.py`.
(Note: By default the system will fallback to an in-memory mock if MongoDB is unreachable)

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run server
python main.py
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Run Simulation
Open the Dashboard in your browser (`http://localhost:5173`).
In a new terminal:
```bash
python test_simulation.py
```
This script acts as the IoT input layer pushing multi-modal updates directly to the analysis engine!

Enjoy the production-ready prototype UI!
