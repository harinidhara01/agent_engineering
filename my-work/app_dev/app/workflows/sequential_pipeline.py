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
        requirements_data = self.requirements_agent.process(intake_data, classification_data)
        
        if not requirements_data.get("complete"):
            return {
                "success": False,
                "error": "Missing required information.",
                "missing": requirements_data.get("missing_information")
            }
            
        # Step 4: Service Request
        service_request = self.service_request_agent.process(intake_data, classification_data)
        
        return {
            "success": True,
            "service_request": service_request
        }
