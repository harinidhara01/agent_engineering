"""The workflow state machine — Book 1, Chapter 9 (§9.3).

State transitions are validated here, deterministically, before any
agent's own prose or reasoning is consulted. A model may recommend the
next step; only this module decides whether the transition is legal.

Deliberately, `SENT` is not a state that exists anywhere in this enum.
Book 1 contains no send-capable tool, and this state machine cannot
reach a state that doesn't exist — the boundary from Class 1 holds
structurally, not just by convention.
"""

from __future__ import annotations

from enum import Enum


class WorkflowState(str, Enum):
    RECEIVED = "RECEIVED"
    RESEARCHING = "RESEARCHING"
    RESEARCH_COMPLETE = "RESEARCH_COMPLETE"
    QUALIFYING = "QUALIFYING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    DRAFT_READY = "DRAFT_READY"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"


ALLOWED_TRANSITIONS: dict[WorkflowState, set[WorkflowState]] = {
    WorkflowState.RECEIVED: {WorkflowState.RESEARCHING},
    WorkflowState.RESEARCHING: {WorkflowState.RESEARCH_COMPLETE, WorkflowState.BLOCKED},
    WorkflowState.RESEARCH_COMPLETE: {WorkflowState.QUALIFYING},
    WorkflowState.QUALIFYING: {WorkflowState.REVIEW_REQUIRED, WorkflowState.BLOCKED},
    WorkflowState.REVIEW_REQUIRED: {WorkflowState.DRAFT_READY, WorkflowState.BLOCKED},
    WorkflowState.DRAFT_READY: {WorkflowState.AWAITING_APPROVAL},
    WorkflowState.AWAITING_APPROVAL: {
        WorkflowState.APPROVED,
        WorkflowState.REJECTED,
        WorkflowState.DRAFT_READY,
    },
    WorkflowState.APPROVED: set(),
    WorkflowState.REJECTED: set(),
    WorkflowState.BLOCKED: set(),
}


class IllegalTransitionError(ValueError):
    pass


def validate_transition(current: WorkflowState, next_state: WorkflowState) -> bool:
    return next_state in ALLOWED_TRANSITIONS.get(current, set())


def transition(current: WorkflowState, next_state: WorkflowState) -> WorkflowState:
    """Advance to `next_state`, or raise if that transition isn't legal
    from `current`. This is the one function every stage of the
    workflow must call — no code path should mutate state directly.
    """
    if not validate_transition(current, next_state):
        raise IllegalTransitionError(f"illegal transition: {current.value} -> {next_state.value}")
    return next_state
