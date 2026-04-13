class DecisionEngine:
    def process(self, vision_data, audio_data, nlp_data):
        """
        Combines outputs from Vision, Audio, and NLP models to make a final decision.
        """
        severity_score = 0
        crisis = False
        findings = []

        if vision_data and vision_data.get("crisis"):
            severity_score += 4
            crisis = True
            findings.append("Visual evidence of crisis")

        if audio_data and audio_data.get("crisis"):
            severity_score += 3
            crisis = True
            findings.append(f"Audio evidence: {', '.join(audio_data.get('detected_keywords', []))}")

        if nlp_data and nlp_data.get("crisis"):
            severity_score += 3
            crisis = True
            findings.append(f"Text reports indicate: {nlp_data.get('event_type')}")
            
        severity = "LOW"
        if severity_score >= 6:
            severity = "CRITICAL"
        elif severity_score >= 3:
            severity = "HIGH"
        elif severity_score > 0:
            severity = "MEDIUM"

        return {
            "crisis_confirmed": crisis,
            "severity": severity,
            "confidence_score": severity_score * 10, # Mock up to 100
            "summary": " | ".join(findings) if findings else "No immediate crisis detected."
        }

decision_engine = DecisionEngine()
