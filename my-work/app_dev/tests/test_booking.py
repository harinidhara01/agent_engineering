from app.services.booking_service import BookingService

def test_booking_success():
    service = BookingService()
    req = {"service_category": "HVAC", "location": "Columbus, OH"}
    res = service.create_booking("provider_001", req)
    assert res["success"] == True
    assert "BKG-" in res["booking_id"]
    assert res["provider_name"] == "ABC HVAC Services"
    
def test_booking_invalid_provider():
    service = BookingService()
    req = {"service_category": "HVAC", "location": "Columbus, OH"}
    res = service.create_booking("invalid_id", req)
    assert res["success"] == False
    assert "error" in res
