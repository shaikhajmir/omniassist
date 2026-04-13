from ultralytics import YOLO

class VisionModel:
    def __init__(self):
        # We use yolov8n.pt for fast inference
        # In a real deployed app, you would load this from a specific weights file tuned for crisis
        self.model = YOLO('yolov8n.pt') 
        
    def detect(self, image_path_or_bytes):
        # Returns a dict of detected objects and a flag for crisis
        results = self.model(image_path_or_bytes)
        detections = []
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0])
                if confidence > 0.4:
                    detections.append({"class": class_name, "confidence": confidence})
        
        # Consider specific classes as potential crisis signals if found out of context (e.g. fire, car, person falling)
        crisis_keywords = ['fire', 'smoke', 'car', 'person'] # Simplified for demo purposes
        crisis_found = any(d['class'] in crisis_keywords for d in detections)
        return {"crisis": crisis_found, "detections": detections, "severity": "HIGH" if crisis_found else "LOW"}

vision_model = VisionModel()
