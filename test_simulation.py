import requests
import time

API_URL = "http://localhost:8000/analyze"

def trigger_accident():
    print("Triggering Accident Alert...")
    response = requests.post(API_URL, data={
        "text_report": "Massive car crash blockading the intersection!",
        "lat": 37.7749,
        "lng": -122.4194
    })
    print(response.json())

def trigger_fire():
    print("Triggering Fire Alert...")
    response = requests.post(API_URL, data={
        "text_report": "Fire spreading rapidly near the central park!",
        "lat": 37.7800,
        "lng": -122.4200
    })
    print(response.json())

if __name__ == "__main__":
    trigger_accident()
    time.sleep(2)
    trigger_fire()
