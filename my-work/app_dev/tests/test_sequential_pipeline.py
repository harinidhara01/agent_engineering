from app.workflows.sequential_pipeline import SequentialPipeline

def test_sequential_pipeline_success():
    pipeline = SequentialPipeline()
    res = pipeline.run("AC not cooling", "Columbus, OH", "Tomorrow", "Morning")
    assert res["success"] == True
    assert res["service_request"]["service_category"] == "HVAC"
    
def test_sequential_pipeline_missing_data():
    pipeline = SequentialPipeline()
    res = pipeline.run("AC not cooling", "", "Tomorrow", "Morning")
    assert res["success"] == False
    assert "location" in res["missing"]
