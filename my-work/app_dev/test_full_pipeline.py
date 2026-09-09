"""
Debug the full pipeline end-to-end to find where eligible providers get lost.
"""
import os
import json
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))

import sys
sys.path.insert(0, ".")

from app.workflows.sequential_pipeline import SequentialPipeline
from app.workflows.parallel_provider_workflow import ParallelProviderWorkflow

print("=== Step 1: Sequential Pipeline ===")
seq = SequentialPipeline()
result = seq.run(
    request_text="My AC is not cooling",
    location="Columbus, OH",
    preferred_date="Tomorrow",
    preferred_time="Morning"
)
print(f"Success: {result.get('success')}")
print(f"Service Request: {json.dumps(result.get('service_request'), indent=2)}")
if not result.get("success"):
    print(f"Error: {result.get('error')}")
    print(f"Missing: {result.get('missing')}")
    exit(1)

print("\n=== Step 2: Parallel Provider Workflow ===")
service_request = result.get("service_request")
parallel = ParallelProviderWorkflow()
ranked = parallel.run(service_request)
print(f"Ranked Providers Count: {len(ranked)}")
for p in ranked:
    print(f"  - {p.get('provider_name')}: eligible={p.get('eligible')}, reason={p.get('reason')}")
