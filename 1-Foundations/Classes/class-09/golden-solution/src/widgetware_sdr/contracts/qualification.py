"""The QualificationResult contract — Book 1, Chapter 6.

Replaces Class 4's free-form prose result ("Acme looks like a strong
opportunity") with a machine-validated interface. Software can now
reliably determine the final status, decisive criteria, supporting
evidence, missing information, and next step — none of which a prose
sentence guarantees.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class QualificationStatus(str, Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    NEEDS_RESEARCH = "NEEDS_RESEARCH"
    BLOCKED = "BLOCKED"


class QualificationResult(BaseModel):
    model_config = {"extra": "forbid"}

    account_id: str
    status: QualificationStatus
    score: float | None = None
    rationale: str
    matched_criteria: list[str] = Field(default_factory=list)
    exclusion_reasons: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    confidence: float | None = None
    recommended_next_step: str | None = None
    errors: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_business_invariants(self) -> "QualificationResult":
        """Deterministic rules enforced after model output, per Book 1
        §6.2's Hands-on Lab — never encode workflow state in prose alone.
        """
        if self.status is QualificationStatus.NOT_QUALIFIED and not self.exclusion_reasons:
            raise ValueError("NOT_QUALIFIED requires at least one exclusion or failed criterion")
        if self.status is QualificationStatus.QUALIFIED and not self.evidence_refs:
            raise ValueError("QUALIFIED requires at least one evidence reference")
        if self.status is QualificationStatus.NEEDS_RESEARCH and not self.missing_information:
            raise ValueError("NEEDS_RESEARCH requires at least one missing-information item")
        if self.status is QualificationStatus.BLOCKED and not self.errors:
            raise ValueError("BLOCKED requires at least one recorded error")
        return self


def parse_qualification_result(raw: dict, account_id: str) -> QualificationResult:
    """Validate-and-repair pipeline entry point (Book 1 §6.5).

    Parses and validates `raw` against the contract and its business
    invariants. On any failure — malformed shape, a missing required
    field, or a violated invariant — this fails *safely* to a `BLOCKED`
    result carrying the validation error, rather than raising or
    silently coercing an ambiguous status. Never guesses.
    """
    try:
        return QualificationResult.model_validate(raw)
    except ValidationError as exc:
        return QualificationResult(
            account_id=raw.get("account_id", account_id),
            status=QualificationStatus.BLOCKED,
            rationale="Result failed schema or business-invariant validation.",
            errors=[str(exc)],
        )
