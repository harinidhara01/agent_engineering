from widgetware_sdr.agents.drafting_agent import build_agent_instruction as drafting_instruction
from widgetware_sdr.agents.drafting_agent import create_drafting_agent
from widgetware_sdr.agents.evidence_reviewer import build_agent_instruction as reviewer_instruction
from widgetware_sdr.agents.evidence_reviewer import create_evidence_reviewer_agent


def test_evidence_reviewer_constructs_with_no_tools() -> None:
    agent = create_evidence_reviewer_agent()
    assert agent.name == "evidence_reviewer"
    assert not agent.tools


def test_evidence_reviewer_instruction_forbids_independent_browsing() -> None:
    instruction = reviewer_instruction()
    assert (
        "not independently browse" in instruction.lower()
        or "do not independently browse" in instruction.lower()
    )


def test_drafting_agent_constructs_with_no_tools() -> None:
    agent = create_drafting_agent()
    assert agent.name == "drafting_agent"
    assert not agent.tools


def test_drafting_agent_description_never_claims_send_capability() -> None:
    agent = create_drafting_agent()
    assert "never sends" in agent.description.lower() or "no send" in agent.description.lower()


def test_drafting_agent_instruction_restricts_to_approved_claims() -> None:
    instruction = drafting_instruction()
    normalized = " ".join(instruction.lower().split())
    assert "only these claims" in normalized or "approved claims" in normalized
