"""Work discovery and selection — Book 1, Chapter 11 (§11.5, §11.11).

The next account is whichever eligible one hasn't already reached a
settled status — never one already finished, whether by success or by
a terminal failure.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from widgetware_sdr.workflow.state_machine import WorkflowState

SETTLED_STATES = {
    WorkflowState.APPROVED,
    WorkflowState.REJECTED,
    WorkflowState.NEEDS_HUMAN_REVIEW,
}

ELIGIBLE_STATES = {
    WorkflowState.RECEIVED,
    WorkflowState.RETRY_PENDING,
}


@dataclass
class QueuedAccount:
    account_id: str
    state: WorkflowState = WorkflowState.RECEIVED
    attempts: int = 0


@dataclass
class AccountQueue:
    accounts: list[QueuedAccount] = field(default_factory=list)

    def select_next(self, exclude: set[str] | None = None) -> QueuedAccount | None:
        """Return the next eligible account, or None if the queue has
        no more eligible work. Never returns an account whose state is
        already settled. `exclude` lets a caller skip accounts already
        deferred earlier in the same run, without changing their state.
        """
        exclude = exclude or set()
        for account in self.accounts:
            if account.account_id in exclude:
                continue
            if account.state in ELIGIBLE_STATES:
                return account
        return None

    def is_settled(self, account_id: str) -> bool:
        for account in self.accounts:
            if account.account_id == account_id:
                return account.state in SETTLED_STATES
        return False

    def remaining_eligible_count(self) -> int:
        return sum(1 for a in self.accounts if a.state in ELIGIBLE_STATES)
