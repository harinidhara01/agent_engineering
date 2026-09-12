import pytest

from widgetware_sdr.loop.decision import LoopDecision, decide
from widgetware_sdr.workflow.state_machine import WorkflowState


def test_budget_exceeded_always_stops_even_if_account_would_otherwise_retry() -> None:
    decision = decide(
        account_state=WorkflowState.BLOCKED,
        attempts=1,
        max_attempts_per_account=5,
        budget_exceeded_reason="reached max_accounts_per_run (10)",
    )
    assert decision is LoopDecision.STOP


def test_awaiting_approval_continues() -> None:
    decision = decide(
        account_state=WorkflowState.AWAITING_APPROVAL,
        attempts=1,
        max_attempts_per_account=3,
        budget_exceeded_reason=None,
    )
    assert decision is LoopDecision.CONTINUE


def test_blocked_with_attempts_remaining_retries() -> None:
    decision = decide(
        account_state=WorkflowState.BLOCKED,
        attempts=1,
        max_attempts_per_account=3,
        budget_exceeded_reason=None,
    )
    assert decision is LoopDecision.RETRY


def test_blocked_with_no_attempts_remaining_escalates() -> None:
    decision = decide(
        account_state=WorkflowState.BLOCKED,
        attempts=3,
        max_attempts_per_account=3,
        budget_exceeded_reason=None,
    )
    assert decision is LoopDecision.ESCALATE


def test_needs_human_review_escalates() -> None:
    decision = decide(
        account_state=WorkflowState.NEEDS_HUMAN_REVIEW,
        attempts=1,
        max_attempts_per_account=3,
        budget_exceeded_reason=None,
    )
    assert decision is LoopDecision.ESCALATE


def test_unavailable_dependency_defers() -> None:
    decision = decide(
        account_state=WorkflowState.BLOCKED,
        attempts=1,
        max_attempts_per_account=3,
        budget_exceeded_reason=None,
        dependency_available=False,
    )
    assert decision is LoopDecision.DEFER


def test_an_in_progress_state_raises_rather_than_guessing() -> None:
    with pytest.raises(ValueError):
        decide(
            account_state=WorkflowState.RESEARCHING,
            attempts=1,
            max_attempts_per_account=3,
            budget_exceeded_reason=None,
        )
