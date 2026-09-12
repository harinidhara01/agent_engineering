"""Deterministic fit-score calculation — Book 1, Chapter 7.

`calculate_fit_score` is deliberately NOT exposed to the model as a
tool. It is application code the qualification workflow calls directly.
The chapter's own point: a calculation with a fixed, auditable formula
belongs in deterministic code, not in a model's reasoning, even though
the model still decides how to *use* the resulting number.
"""

from __future__ import annotations

from typing import Any

_WEIGHT_INDUSTRY = 0.4
_WEIGHT_SIZE = 0.3
_WEIGHT_REGION = 0.2
_WEIGHT_SIGNAL = 0.1


def calculate_fit_score(account: dict[str, Any], icp: dict[str, Any]) -> float:
    """Compute a deterministic 0.0-1.0 fit score for an account against
    an ICP configuration.

    An explicitly excluded industry always scores 0.0, regardless of
    any other attribute — exclusions override positive heuristics, the
    same rule the ICP Qualification Skill states in prose.

    A `None` employee_count contributes nothing to the score (neither a
    pass nor a fail) — it is unknown, not zero and not disqualifying.
    """
    if account.get("industry") in icp.get("excluded_industries", []):
        return 0.0

    score = 0.0
    if account.get("industry") in icp.get("preferred_industries", []):
        score += _WEIGHT_INDUSTRY

    employee_count = account.get("employee_count")
    if employee_count is not None and employee_count >= icp["minimum_employee_count"]:
        score += _WEIGHT_SIZE

    if account.get("region") in icp.get("preferred_regions", []):
        score += _WEIGHT_REGION

    if account.get("known_challenges"):
        score += _WEIGHT_SIGNAL

    return round(score, 2)
