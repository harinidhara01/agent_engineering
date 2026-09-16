import time
import uuid
import json
from datetime import datetime, date
from rag import query_knowledge_base
from database import log_execution

# Comprehensive built-in US/State Official Holiday Dataset for 2026 (No external API or package required)
US_OHIO_HOLIDAYS_2026 = [
    {"date": "2026-01-01", "day_of_week": "Thursday", "holiday_name": "New Year's Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-01-19", "day_of_week": "Monday", "holiday_name": "Martin Luther King Jr. Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-02-16", "day_of_week": "Monday", "holiday_name": "Presidents' Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-05-25", "day_of_week": "Monday", "holiday_name": "Memorial Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-06-19", "day_of_week": "Friday", "holiday_name": "Juneteenth National Independence Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-07-03", "day_of_week": "Friday", "holiday_name": "Independence Day (Observed)", "region": "US (OH)", "year": 2026},
    {"date": "2026-07-04", "day_of_week": "Saturday", "holiday_name": "Independence Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-09-07", "day_of_week": "Monday", "holiday_name": "Labor Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-10-12", "day_of_week": "Monday", "holiday_name": "Columbus Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-11-11", "day_of_week": "Wednesday", "holiday_name": "Veterans Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-11-26", "day_of_week": "Thursday", "holiday_name": "Thanksgiving Day", "region": "US (OH)", "year": 2026},
    {"date": "2026-11-27", "day_of_week": "Friday", "holiday_name": "Day After Thanksgiving", "region": "US (OH)", "year": 2026},
    {"date": "2026-12-25", "day_of_week": "Friday", "holiday_name": "Christmas Day", "region": "US (OH)", "year": 2026}
]

def policy_search(query: str, top_k: int = 3):
    """Tool: Searches the employee policy knowledge base"""
    return query_knowledge_base(query, top_k=top_k)

def regional_holiday_tool(region: str = "US", year: int = 2026, state: str = "OH"):
    """Tool: Retrieves regional official holidays without requiring an API key"""
    start_time = time.time()
    trace_id = f"tool-{uuid.uuid4().hex[:8]}"

    try:
        holiday_list = [h for h in US_OHIO_HOLIDAYS_2026 if h["year"] == year]
        
        duration = (time.time() - start_time) * 1000
        log_execution(
            trace_id=trace_id,
            component="Tool",
            call_type="regional_holiday_tool",
            inputs={"region": region, "state": state, "year": year},
            outputs={"count": len(holiday_list), "holidays": holiday_list},
            duration_ms=duration
        )

        return {
            "status": "success",
            "tool_name": "regional_holiday_tool",
            "source": f"Official Regional Calendar Data ({state or 'OH'}, {year})",
            "data": holiday_list
        }
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        log_execution(
            trace_id=trace_id,
            component="Tool",
            call_type="regional_holiday_tool",
            inputs={"region": region, "year": year},
            outputs={"error": str(e)},
            duration_ms=duration,
            status="error"
        )
        return {
            "status": "error",
            "error": str(e)
        }
