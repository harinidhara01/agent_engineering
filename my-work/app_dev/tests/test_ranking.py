from app.agents.ranking_agent import RankingAgent

def test_ranking_logic():
    agent = RankingAgent()
    data = {
        "eligible_providers": [
            {"provider_name": "A", "rating": 4.0, "distance_miles": 10, "price": 100},
            {"provider_name": "B", "rating": 4.9, "distance_miles": 5, "price": 120},
            {"provider_name": "C", "rating": 4.9, "distance_miles": 2, "price": 150}
        ]
    }
    ranked = agent.process(data)
    # Highest rating wins, tiebreaker is distance
    assert ranked[0]["provider_name"] == "C"
    assert ranked[1]["provider_name"] == "B"
    assert ranked[2]["provider_name"] == "A"
