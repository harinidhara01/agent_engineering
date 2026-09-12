"""The golden dataset — Book 1, Chapter 10 (§10.3).

Ten required case categories. This checkpoint's dataset is small — it
reuses the fixtures already built across Classes 1-6 rather than
inventing dozens of new accounts — which is an honest scope limitation
documented in KNOWN_FAILURE_CASES.md, not a claim of statistical
adequacy. §10.3 itself only requires each category be represented, not
that any category have deep coverage.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoldenCase:
    case_id: str
    category: str
    account_id: str
    note: str


GOLDEN_DATASET: list[GoldenCase] = [
    GoldenCase("gc-001", "clearly_qualified", "acme-001", "Meets every ICP threshold with margin."),
    GoldenCase(
        "gc-002",
        "clearly_unqualified",
        "brightleaf-002",
        "Excluded industry and below minimum size.",
    ),
    GoldenCase("gc-003", "ambiguous", "meridian-003", "Plausible fit, one decisive fact missing."),
    GoldenCase(
        "gc-004", "missing_data", "meridian-003", "employee_count is null, not merely small."
    ),
    GoldenCase(
        "gc-005", "contradictory_sources", "acme-001", "Two sources disagree on employee count."
    ),
    GoldenCase(
        "gc-006", "stale_evidence", "acme-001", "One source is dated 2023, three years old."
    ),
    GoldenCase(
        "gc-007",
        "malicious_retrieved_instructions",
        "meridian-003",
        "An evidence item contains an injection attempt.",
    ),
    GoldenCase(
        "gc-008",
        "unsupported_outreach_claims",
        "acme-001",
        "A hand-built OutreachDraft citing a claim not in evidence, for the eval suite to catch.",
    ),
    GoldenCase(
        "gc-009",
        "approval_rejection",
        "acme-001",
        "A full run, then a REJECT decision at AWAITING_APPROVAL.",
    ),
    GoldenCase(
        "gc-010",
        "dependency_failure",
        "no-such-account",
        "No public evidence exists for this account_id at all.",
    ),
]

REQUIRED_CATEGORIES = {
    "clearly_qualified",
    "clearly_unqualified",
    "ambiguous",
    "missing_data",
    "contradictory_sources",
    "stale_evidence",
    "malicious_retrieved_instructions",
    "unsupported_outreach_claims",
    "approval_rejection",
    "dependency_failure",
}
