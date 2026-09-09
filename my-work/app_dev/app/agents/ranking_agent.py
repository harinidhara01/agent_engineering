class RankingAgent:
    def process(self, aggregator_data: dict) -> list:
        providers = aggregator_data.get("eligible_providers", [])
        
        def sort_key(p):
            # 1. Rating (descending) -> use negative for ascending sort
            rating = p.get("rating")
            sort_rating = -rating if rating is not None else 0
            
            # 2. Distance (ascending)
            distance = p.get("distance_miles")
            sort_distance = distance if distance is not None else float('inf')
            
            # 3. Price (ascending)
            price = p.get("price_estimate")
            sort_price = price if price is not None else float('inf')
            
            return (sort_rating, sort_distance, sort_price)

        ranked = sorted(providers, key=sort_key)
        
        # Add explanation
        if ranked:
            best = ranked[0]
            if best.get("rating") and best.get("rating") >= 4.5:
                best["reason"] = "Recommended because it is highly rated and matches your request."
            elif best.get("price_estimate") and all(p.get("price_estimate", float('inf')) >= best["price_estimate"] for p in ranked):
                best["reason"] = "Lowest available price among eligible providers."
            else:
                best["reason"] = "Best match based on availability, rating, distance, and price."
                
        return ranked
