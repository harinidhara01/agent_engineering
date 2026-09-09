import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class ClassificationResponse(BaseModel):
    service_category: str = Field(description="One of: 'Plumbing', 'HVAC', 'Electrical', or 'Unknown'")
    urgency: str = Field(description="One of: 'emergency' or 'normal'")
    reasoning: str = Field(description="Brief explanation for the classification and urgency")

class ClassificationAgent:
    """
    Classification AI Agent: Uses an LLM to categorize the service request and determine urgency
    based on the domain reference files.
    """
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        self.model = os.environ.get("MODEL", "gemini-1.5-flash")
        
        # Load reference materials
        self.references = ""
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'references')
        for ref_file in ['plumbing.md', 'hvac.md', 'electrical.md']:
            path = os.path.join(base_dir, ref_file)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self.references += f"\n--- {ref_file} ---\n"
                    self.references += f.read()

    def process(self, intake_data: dict) -> dict:
        prompt = f"""
        You are a Classification AI Agent for a Home Service Concierge.
        Classify the customer's problem into a service category and determine the urgency 
        strictly based on the rules in the provided reference materials.
        
        Customer Problem: {intake_data.get('problem')}
        
        Reference Materials:
        {self.references}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ClassificationResponse,
                    temperature=0.1
                ),
            )
            result = response.parsed.model_dump()
            
            # Merge with original data
            intake_data["service_category"] = result["service_category"]
            intake_data["urgency"] = result["urgency"]
            intake_data["classification_reasoning"] = result["reasoning"]
            return intake_data
            
        except Exception as e:
            print(f"ClassificationAgent LLM Error: {e}")
            intake_data["service_category"] = "Unknown"
            intake_data["urgency"] = "normal"
            return intake_data
