"""The five-way loop decision — Book 1, Chapter 11 (§11.8).

After each account, the loop makes exactly one explicit decision —
never an implicit fallthrough.
"""

from __future__ import annotations

from enum import Enum

from widgetware_sdr.workflow.state_machine import WorkflowState


class LoopDecision(str, Enum):
    CONTINUE = "CONTINUE"
    RETRY = "RETRY"
    STOP = "STOP"
    DEFER = "DEFER"
    ESCALATE = "ESCALATE"


def decide(
    *,
    account_state: WorkflowState,
    attempts: int,
    max_attempts_per_account: int,
    budget_exceeded_reason: str | None,
    dependency_available: bool = True,
) -> LoopDecision:
    """Return exactly one decision for this account, this iteration.

    Order matters: a budget limit always wins, even over an otherwise
    retryable account — the loop must not spend past its stated limits
    trying to rescue one account.
    """
    if budget_exceeded_reason is not None:
        return LoopDecision.STOP

    if account_state in (
        WorkflowState.AWAITING_APPROVAL,
        WorkflowState.APPROVED,
        WorkflowState.REJECTED,
    ):
        return LoopDecision.CONTINUE

    if account_state is WorkflowState.NEEDS_HUMAN_REVIEW:
        return LoopDecision.ESCALATE

    if not dependency_available:
        return LoopDecision.DEFER

    if account_state is WorkflowState.BLOCKED:
        if attempts < max_attempts_per_account:
            return LoopDecision.RETRY
        return LoopDecision.ESCALATE

    # Any other in-progress state reached here is itself a defect —
    # the loop should never be asked to decide about an account still
    # mid-workflow. Fail loudly rather than silently picking CONTINUE.
    raise ValueError(f"decide() called on an unexpected in-progress state: {account_state.value}")
