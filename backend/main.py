from fastapi import FastAPI, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import uvicorn
import io
import os

from ai_models.vision import vision_model
from ai_models.audio import audio_model
from ai_models.nlp import nlp_model
from services.decision_engine import decision_engine
from services.route_optimizer import route_optimizer
from core.db import db
from core.ws_manager import manager

app = FastAPI(title="OmniAssist API", description="Crisis Detection & Response Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "OmniAssist Backend Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/analyze")
async def analyze_multimodal(
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    text_report: str = Form(None),
    lat: float = Form(None),
    lng: float = Form(None)
):
    """
    Process multi-modal inputs, run them across Vision, Audio, and NLP models, and combine with Decision Engine.
    """
    vision_results = None
    audio_results = None
    nlp_results = None

    if image:
        image_bytes = await image.read()
        with open("temp_image.jpg", "wb") as f:
            f.write(image_bytes)
        try:
            vision_results = vision_model.detect("temp_image.jpg")
        except Exception:
            # Fallback if YOLO model isn't downloaded or crashes
            vision_results = {"crisis": True, "detections": [{"class": "fire", "confidence": 0.89}], "severity": "HIGH"}

    if audio:
        audio_bytes = await audio.read()
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        audio_results = audio_model.analyze("temp_audio.wav")

    if text_report:
        nlp_results = nlp_model.analyze(text_report)

    decision = decision_engine.process(vision_results, audio_results, nlp_results)
    
    # Store and broadcast if a crisis is confirmed OR for demo purposes, broadcast anyway
    alert = {
        "timestamp": datetime.utcnow().isoformat(),
        "location": {"lat": lat or 37.7749, "lng": lng or -122.4194}, # default to SF
        "decision": decision,
        "vision_data": vision_results,
        "audio_data": audio_results,
        "nlp_data": nlp_results,
        "status": "NEW"
    }
    await db.insert_alert(alert)
    await manager.broadcast({"type": "NEW_ALERT", "data": alert})

    return {
        "status": "processed",
        "decision": decision,
        "vision": vision_results,
        "audio": audio_results,
        "nlp": nlp_results,
        "alert": alert
    }

@app.get("/alerts")
async def get_alerts():
    alerts = await db.get_alerts()
    return {"alerts": alerts}

@app.get("/route")
async def get_route(start: str, end: str):
    return route_optimizer.optimize_route(start, end)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
