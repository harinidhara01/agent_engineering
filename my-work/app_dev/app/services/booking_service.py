from app.agents.booking_agent import BookingAgent
import json
import os

class BookingService:
    def __init__(self):
        self.booking_agent = BookingAgent()

    def create_booking(self, provider_id: str, service_request: dict) -> dict:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')
        with open(data_path, 'r') as f:
            providers = json.load(f)
            
        provider_name = None
        for p in providers:
            if p.get("provider_id") == provider_id:
                provider_name = p.get("provider_name")
                break
                
        if not provider_name:
            return {"success": False, "error": "Provider not found."}
            
        return self.booking_agent.process(provider_id, provider_name, service_request)
