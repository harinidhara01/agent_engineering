class ProviderAgent:
    def __init__(self, provider_data: dict):
        self.provider = provider_data

    def evaluate(self, service_request: dict) -> dict:
        eligible = True
        available = True
        reason = ""

        # Check service compatibility
        if self.provider.get("service_type") != service_request.get("service_category"):
            eligible = False
            reason = "Service type mismatch."

        # Check location
        req_location = service_request.get("location")
        if req_location and req_location not in self.provider.get("service_area", []):
            eligible = False
            reason = "Outside service area."

        # Check availability
        # We assume preferred_time is somewhat mapped to availability array loosely for V1
        req_time = service_request.get("preferred_time", "").lower()
        provider_availability = [a.lower() for a in self.provider.get("availability", [])]
        
        # Simple string match logic for mock data
        if not provider_availability:
            available = False
            eligible = False
            reason = "No availability."
        else:
            time_match = False
            if req_time:
                for avail in provider_availability:
                    if avail in req_time or req_time in avail:
                        time_match = True
                        break
                # If no direct match but has some availability, we'll mark available but maybe note it.
                # Actually, provider rules say "A provider is available only when the provider data indicates availability for the requested appointment window."
                # Let's do a basic intersection. If req_time isn't matched exactly by keyword, we might just fail them if we are strict.
                # For simplicity, if we find 'morning', 'afternoon', 'evening' in req_time, require it in provider.
                time_keywords = ["morning", "afternoon", "evening"]
                req_keys = [k for k in time_keywords if k in req_time]
                if req_keys:
                    if not any(k in provider_availability for k in req_keys):
                        available = False
                        eligible = False
                        reason = f"Not available during {', '.join(req_keys)}."
            if available and eligible:
                reason = "Available and matches service requirements."

        return {
            "provider_id": self.provider.get("provider_id"),
            "provider_name": self.provider.get("provider_name"),
            "eligible": eligible,
            "available": available,
            "price": self.provider.get("price_estimate"),
            "distance_miles": self.provider.get("distance_miles"),
            "rating": self.provider.get("rating"),
            "reason": reason
        }
