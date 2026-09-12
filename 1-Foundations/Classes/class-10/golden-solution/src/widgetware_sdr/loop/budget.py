"""Loop budgets — Book 1, Chapter 11 (§11.8).

State every limit before the loop starts running, not after it has
already spent the budget. Any one of these being reached is a
legitimate reason to stop, alongside simply running out of eligible
accounts.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Budget:
    max_accounts_per_run: int
    max_attempts_per_account: int
    max_wall_clock_seconds: float
    max_tool_calls: int
    max_consecutive_failures: int


@dataclass
class BudgetUsage:
    accounts_processed: int = 0
    tool_calls: int = 0
    consecutive_failures: int = 0
    elapsed_seconds: float = 0.0


def budget_exceeded(budget: Budget, usage: BudgetUsage) -> str | None:
    """Return the specific reason the budget was exceeded, or None if
    the loop may continue. Checking every dimension, not just the
    first one hit, matters for an honest stop_reason later.
    """
    if usage.accounts_processed >= budget.max_accounts_per_run:
        return f"reached max_accounts_per_run ({budget.max_accounts_per_run})"
    if usage.tool_calls >= budget.max_tool_calls:
        return f"reached max_tool_calls ({budget.max_tool_calls})"
    if usage.consecutive_failures >= budget.max_consecutive_failures:
        return f"reached max_consecutive_failures ({budget.max_consecutive_failures})"
    if usage.elapsed_seconds >= budget.max_wall_clock_seconds:
        return f"reached max_wall_clock_seconds ({budget.max_wall_clock_seconds})"
    return None
