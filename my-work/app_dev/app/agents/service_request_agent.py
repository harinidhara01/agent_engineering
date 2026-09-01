class ServiceRequestAgent:
    def process(self, intake_data: dict, classification_data: dict) -> dict:
        return {
            "service_category": classification_data.get("service_category"),
            "issue_type": classification_data.get("issue_type"),
            "location": intake_data.get("location"),
            "preferred_date": intake_data.get("preferred_date"),
            "preferred_time": intake_data.get("preferred_time"),
            "urgency": classification_data.get("urgency")
        }
