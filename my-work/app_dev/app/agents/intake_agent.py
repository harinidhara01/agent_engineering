class IntakeAgent:
    def process(self, request_text: str, location: str, preferred_date: str, preferred_time: str) -> dict:
        return {
            "problem": request_text,
            "location": location,
            "preferred_date": preferred_date,
            "preferred_time": preferred_time,
        }
