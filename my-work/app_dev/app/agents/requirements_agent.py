class RequirementsAgent:
    def process(self, intake_data: dict, classification_data: dict) -> dict:
        required_fields = ["location", "preferred_date", "preferred_time"]
        missing_fields = []
        
        for field in required_fields:
            if not intake_data.get(field) or not str(intake_data.get(field)).strip():
                missing_fields.append(field)
                
        if classification_data.get("service_category") == "Unknown":
            missing_fields.append("service_category")
            
        complete = len(missing_fields) == 0
        
        return {
            "complete": complete,
            "required_information": required_fields + ["service_category", "problem"],
            "missing_information": missing_fields
        }
