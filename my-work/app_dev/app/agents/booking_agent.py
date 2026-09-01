import uuid

class BookingAgent:
    def process(self, provider_id: str, provider_name: str, service_request: dict) -> dict:
        # Generate mock booking confirmation
        booking_id = f"BKG-{str(uuid.uuid4())[:8].upper()}"
        
        return {
            "success": True,
            "booking_id": booking_id,
            "provider_id": provider_id,
            "provider_name": provider_name,
            "service_category": service_request.get("service_category"),
            "appointment_date": service_request.get("preferred_date"),
            "appointment_time": service_request.get("preferred_time"),
            "location": service_request.get("location")
        }
