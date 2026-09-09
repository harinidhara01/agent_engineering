import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class RequirementsResponse(BaseModel):
    is_complete: bool = Field(description="True if the request has sufficient information to proceed, False otherwise")
    missing_fields: list[str] = Field(description="List of required fields that are missing or ambiguous (empty list if complete)")
    reasoning: str = Field(description="Explanation of the completeness evaluation")

class RequirementsAgent:
    """
    Requirements AI Agent: Uses an LLM to evaluate if the collected data has all
    necessary fields to book the identified service category.
    """
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        self.model = os.environ.get("MODEL", "gemini-1.5-flash")

    def process(self, classified_data: dict) -> dict:
        prompt = f"""
        You are a Requirements AI Agent for a Home Service Concierge.
        Evaluate if the following service request has all the necessary components to proceed.
        
        A complete request must have a clearly defined problem, a location, a preferred_date, 
        a preferred_time, and a recognized service_category (cannot be 'Unknown').
        
        Current Request Data:
        Problem: {classified_data.get('problem')}
        Location: {classified_data.get('location')}
        Preferred Date: {classified_data.get('preferred_date')}
        Preferred Time: {classified_data.get('preferred_time')}
        Service Category: {classified_data.get('service_category')}
        Urgency: {classified_data.get('urgency')}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RequirementsResponse,
                    temperature=0.1
                ),
            )
            result = response.parsed.model_dump()
            
            classified_data["is_complete"] = result["is_complete"]
            classified_data["missing"] = result["missing_fields"]
            classified_data["requirements_reasoning"] = result["reasoning"]
            return classified_data
            
        except Exception as e:
            print(f"RequirementsAgent LLM Error: {e}")
            classified_data["is_complete"] = False
            classified_data["missing"] = ["LLM Error occurred during validation"]
            return classified_data
