import pytest

from widgetware_sdr.workflow.state_machine import (
    IllegalTransitionError,
    WorkflowState,
    transition,
    validate_transition,
)


def test_legal_transition_succeeds() -> None:
    assert (
        transition(WorkflowState.RECEIVED, WorkflowState.RESEARCHING) is WorkflowState.RESEARCHING
    )


def test_illegal_transition_raises() -> None:
    with pytest.raises(IllegalTransitionError):
        transition(WorkflowState.RECEIVED, WorkflowState.AWAITING_APPROVAL)


def test_terminal_states_have_no_outgoing_transitions() -> None:
    for terminal in (WorkflowState.APPROVED, WorkflowState.REJECTED, WorkflowState.BLOCKED):
        for candidate in WorkflowState:
            assert not validate_transition(terminal, candidate)


def test_sent_is_not_a_state_that_exists() -> None:
    """The structural version of Book 1's standing boundary: there is
    no state to reach that means "sent," because no such state exists
    in this enum at all.
    """
    state_names = {s.value for s in WorkflowState}
    assert "SENT" not in state_names
    assert "SENDING" not in state_names


def test_revise_returns_to_draft_ready_not_a_dead_end() -> None:
    assert validate_transition(WorkflowState.AWAITING_APPROVAL, WorkflowState.DRAFT_READY)


def test_the_full_happy_path_is_reachable_in_order() -> None:
    path = [
        WorkflowState.RECEIVED,
        WorkflowState.RESEARCHING,
        WorkflowState.RESEARCH_COMPLETE,
        WorkflowState.QUALIFYING,
        WorkflowState.REVIEW_REQUIRED,
        WorkflowState.DRAFT_READY,
        WorkflowState.AWAITING_APPROVAL,
        WorkflowState.APPROVED,
    ]
    current = path[0]
    for next_state in path[1:]:
        current = transition(current, next_state)
    assert current is WorkflowState.APPROVED
