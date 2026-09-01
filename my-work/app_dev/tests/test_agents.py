from app.agents.intake_agent import IntakeAgent
from app.agents.classification_agent import ClassificationAgent

def test_intake_agent():
    agent = IntakeAgent()
    res = agent.process("My AC is broken", "Columbus, OH", "tomorrow", "evening")
    assert res["problem"] == "My AC is broken"
    assert res["location"] == "Columbus, OH"

def test_classification_agent():
    agent = ClassificationAgent()
    res = agent.process({"problem": "pipe is leaking"})
    assert res["service_category"] == "Plumbing"
    assert res["urgency"] == "normal"
    
    res = agent.process({"problem": "pipe burst"})
    assert res["service_category"] == "Plumbing"
    assert res["urgency"] == "emergency"
