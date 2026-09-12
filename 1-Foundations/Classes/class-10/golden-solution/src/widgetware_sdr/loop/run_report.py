"""The batch run report — Book 1, Chapter 11 (§11.11): every run
produces a report a person can audit after the fact, always including
its stop_reason and per-status totals.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from widgetware_sdr.workflow.state_machine import WorkflowState


@dataclass
class RunReport:
    run_id: str
    stop_reason: str
    accounts_processed: int
    status_totals: dict[str, int] = field(default_factory=dict)

    @classmethod
    def build(cls, run_id: str, stop_reason: str, final_states: list[WorkflowState]) -> "RunReport":
        totals = Counter(state.value for state in final_states)
        return cls(
            run_id=run_id,
            stop_reason=stop_reason,
            accounts_processed=len(final_states),
            status_totals=dict(totals),
        )
