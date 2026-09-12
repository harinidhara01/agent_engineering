"""Schema validation and business-invariant tests — Book 1 §6.

Two distinct layers, kept in separate test files per §6.6: this file
checks the contract itself (format, required fields, invariants). It
does not check whether a given qualification decision was *correct* —
that's semantic evaluation, and belongs elsewhere.
"""

import pytest
from pydantic import ValidationError

from widgetware_sdr.contracts.qualification import (
    QualificationResult,
    QualificationStatus,
    parse_qualification_result,
)


def test_a_well_formed_qualified_result_validates() -> None:
    result = QualificationResult(
        account_id="acme-001",
        status=QualificationStatus.QUALIFIED,
        rationale="Matches industry, size, and region; concrete pain signal present.",
        matched_criteria=["industry", "employee_count", "region"],
        evidence_refs=["ev-001"],
        confidence=0.9,
    )
    assert result.status is QualificationStatus.QUALIFIED


def test_qualified_without_evidence_refs_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="acme-001",
            status=QualificationStatus.QUALIFIED,
            rationale="Looks like a good fit.",
            evidence_refs=[],
        )


def test_not_qualified_without_exclusion_reasons_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="brightleaf-002",
            status=QualificationStatus.NOT_QUALIFIED,
            rationale="Not a fit.",
            exclusion_reasons=[],
        )


def test_needs_research_without_missing_information_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="meridian-003",
            status=QualificationStatus.NEEDS_RESEARCH,
            rationale="Unclear.",
            missing_information=[],
        )


def test_blocked_without_errors_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="acme-001",
            status=QualificationStatus.BLOCKED,
            rationale="Something went wrong.",
            errors=[],
        )


def test_unknown_status_value_is_rejected() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="acme-001",
            status="MAYBE_QUALIFIED",
            rationale="Ambiguous status value.",
        )


def test_extra_fields_are_rejected_not_silently_dropped() -> None:
    with pytest.raises(ValidationError):
        QualificationResult(
            account_id="acme-001",
            status=QualificationStatus.QUALIFIED,
            rationale="Fits.",
            evidence_refs=["ev-001"],
            made_up_field="should not be allowed",
        )


def test_parse_qualification_result_fails_safely_to_blocked() -> None:
    """§6.5: a materially invalid result fails safely — never a guess."""
    raw = {
        "account_id": "acme-001",
        "status": "QUALIFIED",
        "rationale": "Fits.",
        "evidence_refs": [],
    }
    result = parse_qualification_result(raw, account_id="acme-001")
    assert result.status is QualificationStatus.BLOCKED
    assert result.errors


def test_parse_qualification_result_passes_through_a_valid_result() -> None:
    raw = {
        "account_id": "brightleaf-002",
        "status": "NOT_QUALIFIED",
        "rationale": "Excluded industry.",
        "exclusion_reasons": ["industry: financial_services is excluded"],
    }
    result = parse_qualification_result(raw, account_id="brightleaf-002")
    assert result.status is QualificationStatus.NOT_QUALIFIED
    assert not result.errors
