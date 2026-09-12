from widgetware_sdr.loop.batch_runner import create_batch_loop_agent


def test_batch_loop_agent_constructs_with_the_configured_max_iterations() -> None:
    agent = create_batch_loop_agent(max_iterations=50)
    assert agent.max_iterations == 50
    assert agent.name == "widgetware_batch_loop"
    assert len(agent.sub_agents) == 1
