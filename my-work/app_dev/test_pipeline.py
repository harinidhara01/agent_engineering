import os
import sys

# Fake API key if not set
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "fake_key_for_testing"

# Mock the genai client to not actually make network calls if it fails, or just let it fail and print the traceback
from app.workflows.sequential_pipeline import SequentialPipeline

def test():
    pipeline = SequentialPipeline()
    try:
        res = pipeline.run("my AC is broken", "Columbus, OH", "Tomorrow", "Morning")
        print("Pipeline result:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
