import json
import os
import concurrent.futures
from app.agents.provider_agent import ProviderAgent
from app.agents.aggregator_agent import AggregatorAgent
from app.agents.ranking_agent import RankingAgent

class ParallelProviderWorkflow:
    def __init__(self):
        self.aggregator = AggregatorAgent()
        self.ranker = RankingAgent()
        self._load_providers()

    def _load_providers(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'providers.json')
        with open(data_path, 'r') as f:
            self.providers_data = json.load(f)

    def _evaluate_provider(self, provider_data, service_request):
        try:
            agent = ProviderAgent(provider_data)
            return agent.evaluate(service_request)
        except Exception as e:
            print(f"Provider {provider_data.get('provider_name')} failed evaluation: {e}")
            return None

    def run(self, service_request: dict) -> list:
        provider_results = []
        
        # Parallel fan-out
        # Using max_workers=1 to prevent hitting Gemini API free tier concurrent limits
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [
                executor.submit(self._evaluate_provider, provider, service_request)
                for provider in self.providers_data
            ]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    provider_results.append(result)

        # Aggregation
        aggregated_data = self.aggregator.process(provider_results)
        
        # Ranking
        ranked_results = self.ranker.process(aggregated_data)
        
        return ranked_results
