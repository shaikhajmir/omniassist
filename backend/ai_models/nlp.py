class NLPModel:
    def __init__(self):
        # Initializing without downloading thick models to ensure ultra-fast startup for the demo
        self.classifier = None

    def analyze(self, text):
        return self._mock_analyze(text)

    def _mock_analyze(self, text):
        text_lower = text.lower()
        if "fire" in text_lower:
            return {"crisis": True, "event_type": "fire", "confidence": 0.9, "severity": "HIGH"}
        elif "accident" in text_lower or "crash" in text_lower:
            return {"crisis": True, "event_type": "accident", "confidence": 0.9, "severity": "HIGH"}
        elif "fall" in text_lower or "help" in text_lower:
            return {"crisis": True, "event_type": "medical or fall", "confidence": 0.8, "severity": "MEDIUM"}
        else:
            return {"crisis": False, "event_type": "safe situation", "confidence": 0.9, "severity": "LOW"}

nlp_model = NLPModel()
