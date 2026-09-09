class AggregatorAgent:
    def process(self, provider_results: list) -> dict:
        eligible_providers = []
        for result in provider_results:
            # We skip None results in case an agent failed completely
            if not result:
                continue
                
            if result.get("eligible"):
                eligible_providers.append(result)
                
        return {
            "eligible_providers": eligible_providers
        }
