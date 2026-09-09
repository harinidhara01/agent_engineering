import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class IntakeResponse(BaseModel):
    problem: str = Field(description="The customer's problem description")
    location: str = Field(description="The customer's location")
    preferred_date: str = Field(description="The customer's preferred date")
    preferred_time: str = Field(description="The customer's preferred time")

class IntakeAgent:
    """
    Intake AI Agent: Normalizes the raw user input into a structured payload.
    """
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        # Using gemini-1.5-flash as the standard fast model
        self.model = os.environ.get("MODEL", "gemini-1.5-flash")

    def process(self, request_text: str, location: str, preferred_date: str, preferred_time: str) -> dict:
        prompt = f"""
        You are an Intake AI Agent for a Home Service Concierge.
        Your job is to cleanly extract and organize the user's information.
        
        Customer Problem: {request_text}
        Location: {location}
        Preferred Date: {preferred_date}
        Preferred Time: {preferred_time}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IntakeResponse,
                    temperature=0.1
                ),
            )
            # The parsed property contains the Pydantic object
            return response.parsed.model_dump()
        except Exception as e:
            # Fallback for errors or older SDKs
            print(f"IntakeAgent LLM Error: {e}")
            return {
                "problem": request_text,
                "location": location,
                "preferred_date": preferred_date,
                "preferred_time": preferred_time
            }
