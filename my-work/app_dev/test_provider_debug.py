"""
Debug script: tests ProviderAgent with a real LLM call using the actual providers.json
Run: python3 test_provider_debug.py
"""
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Patch so agents pick up GOOGLE_API_KEY
os.environ.setdefault("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

import sys
sys.path.insert(0, ".")

from app.agents.provider_agent import ProviderAgent

# Load providers
with open("app/data/providers.json") as f:
    providers = json.load(f)

# Simulated service request (what ServiceRequestAgent would produce)
service_request = {
    "service_category": "HVAC",
    "urgency": "normal",
    "location": "Columbus, OH",
    "appointment_window": "Tomorrow Morning",
    "problem_summary": "The customer's AC is not cooling the house."
}

print(f"Testing {len(providers)} providers...\n")

for provider in providers:
    agent = ProviderAgent(provider)
    result = agent.evaluate(service_request)
    status = "✅ ELIGIBLE" if result.get("eligible") else "❌ NOT ELIGIBLE"
    print(f"{status} | {provider['provider_name']}")
    print(f"       Reason: {result.get('reason')}")
    print()
