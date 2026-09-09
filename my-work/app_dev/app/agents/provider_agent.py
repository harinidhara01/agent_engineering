import os
import json
from google import genai
from google.genai import types

class ProviderAgent:
    """
    Provider AI Agent: Evaluates a single provider's capability to fulfill a service request
    using an LLM grounded by provider_rules.md.
    """
    def __init__(self, provider_data: dict):
        self.provider = provider_data
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        self.model = os.environ.get("MODEL", "gemini-1.5-flash")
        
        # Load provider rules
        self.rules = ""
        rules_path = os.path.join(os.path.dirname(__file__), '..', '..', 'references', 'provider_rules.md')
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                self.rules = f.read()

    def evaluate(self, service_request: dict) -> dict:
        prompt = f"""
        You are a Provider AI Agent for a Home Service Concierge.
        Evaluate if the following Provider can fulfill the Service Request.
        
        Strictly apply the rules from the Provider Rules Document.
        
        --- Provider Rules ---
        {self.rules}
        
        Important Matching Instructions:
        1. If the provider's `service_type` matches the `Category`, consider them compatible.
        2. If the provider's `service_area` includes the city in the `Location`, consider them in-area.
        3. If the provider's `availability` includes the time of day (e.g., 'morning') requested in the `Appointment Window`, consider them available.
        
        --- Service Request ---
        Category: {service_request.get('service_category')}
        Urgency: {service_request.get('urgency')}
        Location: {service_request.get('location')}
        Appointment Window: {service_request.get('appointment_window')}
        Problem Summary: {service_request.get('problem_summary')}
        
        --- Provider Details ---
        {json.dumps(self.provider, indent=2)}
        
        Respond ONLY with a raw JSON object with this exact structure, no markdown formatting:
        {{
            "eligible": true,
            "reason": "Brief explanation"
        }}
        """
        
        result_dict = dict(self.provider)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # json is imported at top of file
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
            
            result = json.loads(text.strip())
            
            result_dict["eligible"] = result.get("eligible", False)
            result_dict["reason"] = result.get("reason", "No reason provided")
            return result_dict
            
        except Exception as e:
            print(f"ProviderAgent LLM Error for {self.provider.get('provider_name')}: {e}")
            result_dict["eligible"] = False
            result_dict["reason"] = "Evaluation failed due to LLM error."
            return result_dict
