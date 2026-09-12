"""Offline, deterministic tests for the Research Agent's construction."""

from widgetware_sdr.agents.research_agent import build_agent_instruction, create_research_agent


def test_agent_has_the_search_tool_attached() -> None:
    agent = create_research_agent()
    tool_names = {getattr(t, "__name__", str(t)) for t in agent.tools}
    assert tool_names == {"search_public_records"}


def test_instruction_establishes_retrieved_content_as_untrusted() -> None:
    instruction = build_agent_instruction()
    assert "DATA, not instructions" in instruction
    assert "ignore previous instructions" in instruction.lower()


def test_instruction_requires_surfacing_conflicts_not_picking_one() -> None:
    instruction = build_agent_instruction()
    normalized = " ".join(instruction.lower().split())
    assert "conflict" in normalized
    assert "do not pick one value" in normalized
