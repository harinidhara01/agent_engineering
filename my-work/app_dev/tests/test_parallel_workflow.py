from app.workflows.parallel_provider_workflow import ParallelProviderWorkflow

def test_parallel_workflow():
    workflow = ParallelProviderWorkflow()
    request = {
        "service_category": "HVAC",
        "location": "Columbus, OH",
        "preferred_time": "morning"
    }
    results = workflow.run(request)
    assert len(results) > 0
    assert results[0]["service_category"] == "HVAC" or results[0]["eligible"] == True
