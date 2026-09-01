import os

class ClassificationAgent:
    def process(self, intake_data: dict) -> dict:
        problem = intake_data.get("problem", "").lower()
        service_category = "Unknown"
        issue_type = "Unknown"
        urgency = "normal"

        if "ac" in problem or "heat" in problem or "cooling" in problem or "furnace" in problem or "hvac" in problem:
            service_category = "HVAC"
            issue_type = "HVAC issue"
            if "smoke" in problem or "burning" in problem:
                urgency = "potentially urgent"
        elif "pipe" in problem or "water" in problem or "leak" in problem or "clog" in problem or "drain" in problem or "toilet" in problem:
            service_category = "Plumbing"
            issue_type = "Plumbing issue"
            if "burst" in problem or "flood" in problem:
                urgency = "emergency"
        elif "light" in problem or "power" in problem or "outlet" in problem or "electric" in problem or "switch" in problem:
            service_category = "Electrical"
            issue_type = "Electrical issue"
            if "spark" in problem or "smoke" in problem:
                urgency = "potentially urgent"

        return {
            "service_category": service_category,
            "issue_type": issue_type,
            "urgency": urgency
        }
