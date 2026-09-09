import os
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "fake_key_for_testing"

from app.agents.provider_agent import ProviderAgent

provider_data = {
    "provider_id": "provider_001",
    "provider_name": "ABC HVAC Services",
    "service_type": "HVAC",
    "service_area": ["Columbus, OH", "Dublin, OH"],
    "rating": 4.8,
    "price_estimate": 120,
    "distance_miles": 4.2,
    "availability": ["morning", "afternoon", "evening"]
}

service_request = {
    "service_category": "HVAC",
    "urgency": "normal",
    "location": "Columbus, OH",
    "appointment_window": "Tomorrow Morning",
    "problem_summary": "AC is broken"
}

def test():
    agent = ProviderAgent(provider_data)
    res = agent.evaluate(service_request)
    print("Provider Agent Result:")
    import pprint
    pprint.pprint(res)

if __name__ == "__main__":
    test()
