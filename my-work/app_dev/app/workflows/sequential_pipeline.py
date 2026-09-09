from app.agents.intake_agent import IntakeAgent
from app.agents.classification_agent import ClassificationAgent
from app.agents.requirements_agent import RequirementsAgent
from app.agents.service_request_agent import ServiceRequestAgent

class SequentialPipeline:
    def __init__(self):
        self.intake_agent = IntakeAgent()
        self.classification_agent = ClassificationAgent()
        self.requirements_agent = RequirementsAgent()
        self.service_request_agent = ServiceRequestAgent()

    def run(self, request_text: str, location: str, preferred_date: str, preferred_time: str) -> dict:
        # Step 1: Intake
        intake_data = self.intake_agent.process(request_text, location, preferred_date, preferred_time)
        
        # Step 2: Classification
        classification_data = self.classification_agent.process(intake_data)
        
        # Step 3: Requirements
        requirements_data = self.requirements_agent.process(classification_data)
        
        if not requirements_data.get("is_complete"):
            return {
                "success": False,
                "error": "Missing required information.",
                "missing": requirements_data.get("missing", [])
            }
            
        # Step 4: Service Request
        final_data = self.service_request_agent.process(requirements_data)
        
        return {
            "success": True,
            "service_request": final_data.get("service_request")
        }
