class VisionModel:
    def __init__(self):
        # We mock YOLOv8 to guarantee zero-lag initialization for the demo
        self.model = None
        
    def detect(self, image_path_or_bytes):
        # Consider specific classes as potential crisis signals if found out of context (e.g. fire, car, person falling)
        crisis_found = True
        return {"crisis": crisis_found, "detections": [{"class": "fire/accident", "confidence": 0.95}], "severity": "HIGH"}

vision_model = VisionModel()
