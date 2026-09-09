import os
from google import genai
from google.genai import types
from app.workflows.sequential_pipeline import SequentialPipeline
from app.workflows.parallel_provider_workflow import ParallelProviderWorkflow


class OrchestratorAgent:
    """
    Root Orchestrator Agent: The top-level entry point for the Home Service Concierge.

    This agent is responsible for:
    1. Receiving a raw customer service request.
    2. Using the LLM to perform an initial triage and decide if the request is valid.
    3. Delegating to the SequentialPipeline for intake, classification, and request creation.
    4. Delegating to the ParallelProviderWorkflow for provider matching and ranking.
    5. Returning the final consolidated result to the caller (Flask routes).
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        )
        self.model = os.environ.get("MODEL", "gemini-2.0-flash")
        self.sequential_pipeline = SequentialPipeline()
        self.parallel_workflow = ParallelProviderWorkflow()

    def _triage(self, problem: str) -> dict:
        """
        LLM call: Decide if the request is a valid home service request before
        passing it through the full pipeline.
        """
        prompt = f"""
        You are the Root Orchestrator Agent for a Home Service Concierge.
        Your first task is to triage an incoming customer request.

        Determine if the following text describes a legitimate home service need
        (plumbing, HVAC, or electrical problem). If it is not clearly a home service
        request, or if it is spam/abusive/off-topic, reject it.

        Customer Request: "{problem}"

        Respond ONLY with a raw JSON object:
        {{
            "valid": true,
            "rejection_reason": ""
        }}

        Set "valid" to false and provide a brief "rejection_reason" if the request
        should not be processed.
        """
        import json
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
            return json.loads(text.strip())
        except Exception as e:
            print(f"OrchestratorAgent triage LLM error: {e}")
            # On error, allow the request through — the downstream agents will handle it
            return {"valid": True, "rejection_reason": ""}

    def run(self, problem: str, location: str, preferred_date: str, preferred_time: str) -> dict:
        """
        Main orchestration method. Coordinates the full multi-agent workflow:
        1. Triage (LLM)
        2. Sequential Pipeline (Intake → Classification → Requirements → ServiceRequest)
        3. Parallel Provider Workflow (ProviderAgents → Aggregator → Ranking)
        """
        print(f"[OrchestratorAgent] Received request: {problem[:80]}...")

        # Step 1: Triage — LLM decides if request is valid
        triage_result = self._triage(problem)
        print(f"[OrchestratorAgent] Triage result: valid={triage_result.get('valid')}")

        if not triage_result.get("valid"):
            return {
                "success": False,
                "stage": "triage",
                "error": triage_result.get(
                    "rejection_reason", "Request could not be processed."
                ),
            }

        # Step 2: Sequential pipeline
        print("[OrchestratorAgent] Delegating to SequentialPipeline...")
        seq_result = self.sequential_pipeline.run(
            request_text=problem,
            location=location,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
        )

        if not seq_result.get("success"):
            return {
                "success": False,
                "stage": "sequential_pipeline",
                "error": seq_result.get("error", "Failed to process request."),
                "missing": seq_result.get("missing", []),
            }

        service_request = seq_result.get("service_request")
        print(f"[OrchestratorAgent] Service request created: {service_request}")

        # Step 3: Parallel provider workflow
        print("[OrchestratorAgent] Delegating to ParallelProviderWorkflow...")
        ranked_providers = self.parallel_workflow.run(service_request)
        print(f"[OrchestratorAgent] Found {len(ranked_providers)} eligible provider(s).")

        return {
            "success": True,
            "service_request": service_request,
            "providers": ranked_providers,
        }
