import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class ServiceRequestSchema(BaseModel):
    normalized_problem: str = Field(description="A clean, professional summary of the customer's problem")
    service_category: str = Field(description="The determined service category")
    urgency: str = Field(description="The determined urgency (e.g. 'emergency' or 'normal')")
    location: str = Field(description="The customer's location")
    appointment_window: str = Field(description="Combined date and time preference")

class ServiceRequestAgent:
    """
    Service Request AI Agent: Synthesizes the final request payload to be sent to providers.
    Uses the LLM to write a professional summary of the problem.
    """
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        self.model = os.environ.get("MODEL", "gemini-1.5-flash")

    def process(self, validated_data: dict) -> dict:
        if not validated_data.get("is_complete"):
            return validated_data
            
        prompt = f"""
        You are a Service Request AI Agent for a Home Service Concierge.
        Your task is to convert the internal customer request data into a clean, 
        professional service request suitable for broadcasting to third-party contractors.
        
        Raw Problem: {validated_data.get('problem')}
        Category: {validated_data.get('service_category')}
        Urgency: {validated_data.get('urgency')}
        Date: {validated_data.get('preferred_date')}
        Time: {validated_data.get('preferred_time')}
        Location: {validated_data.get('location')}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ServiceRequestSchema,
                    temperature=0.2
                ),
            )
            result = response.parsed.model_dump()
            
            validated_data["service_request"] = {
                "service_category": result["service_category"],
                "urgency": result["urgency"],
                "location": result["location"],
                "appointment_window": result["appointment_window"],
                "problem_summary": result["normalized_problem"]
            }
            return validated_data
            
        except Exception as e:
            print(f"ServiceRequestAgent LLM Error: {e}")
            validated_data["service_request"] = {
                "service_category": validated_data.get("service_category"),
                "urgency": validated_data.get("urgency"),
                "location": validated_data.get("location"),
                "appointment_window": f"{validated_data.get('preferred_date')} {validated_data.get('preferred_time')}",
                "problem_summary": validated_data.get("problem")
            }
            return validated_data
