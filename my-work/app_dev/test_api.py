"""
Quick test to verify your Gemini API key is working.
Run: python3 test_api.py
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Check what keys are set
google_key = os.environ.get("GOOGLE_API_KEY")
gemini_key = os.environ.get("GEMINI_API_KEY")

print("=== API Key Check ===")
print(f"GOOGLE_API_KEY: {'SET (' + google_key[:8] + '...)' if google_key else 'NOT SET'}")
print(f"GEMINI_API_KEY: {'SET (' + gemini_key[:8] + '...)' if gemini_key else 'NOT SET'}")
print()

# Use GEMINI_API_KEY explicitly
api_key = gemini_key or google_key
if not api_key:
    print("ERROR: No API key found in .env file!")
    exit(1)

model = os.environ.get("MODEL", "gemini-2.0-flash")
print(f"Model: {model}")
print()

print("=== Testing Gemini API ===")
from google import genai

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model,
        contents="Say 'API is working!' in exactly those words."
    )
    print(f"SUCCESS: {response.text.strip()}")
except Exception as e:
    print(f"FAILED: {e}")
