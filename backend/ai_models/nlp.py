from transformers import pipeline

class NLPModel:
    def __init__(self):
        # Using a small zero-shot classifier to determine crisis elements
        try:
            self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        except:
            self.classifier = None # Fallback if no internet / memory

    def analyze(self, text):
        if not self.classifier:
            return self._mock_analyze(text)
            
        candidate_labels = ["accident", "fire", "medical emergency", "robbery", "safe situation"]
        
        try:
            result = self.classifier(text, candidate_labels)
            top_label = result['labels'][0]
            confidence = result['scores'][0]
            
            severity = "HIGH" if top_label != "safe situation" and confidence > 0.6 else "LOW"
            crisis = severity == "HIGH"
            
            return {
                "crisis": crisis,
                "event_type": top_label,
                "confidence": confidence,
                "severity": severity
            }
        except Exception as e:
            return self._mock_analyze(text)

    def _mock_analyze(self, text):
        text_lower = text.lower()
        if "fire" in text_lower:
            return {"crisis": True, "event_type": "fire", "confidence": 0.9, "severity": "HIGH"}
        elif "accident" in text_lower:
            return {"crisis": True, "event_type": "accident", "confidence": 0.9, "severity": "HIGH"}
        else:
            return {"crisis": False, "event_type": "safe situation", "confidence": 0.9, "severity": "LOW"}

nlp_model = NLPModel()
