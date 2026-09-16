"""The EvidenceReview contract — Book 1, Chapter 9 (§9.5).

The Evidence Reviewer's typed output: which claims are approved for
drafting, which were rejected as unsupported, and whether the sources
are current enough to trust. The Outreach Drafting Agent will only ever
see `approved_claims` — never the full research brief — so it
structurally cannot draft from a claim the reviewer rejected.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class EvidenceReview(BaseModel):
    model_config = {"extra": "forbid"}

    account_id: str
    approved_claims: list[str] = Field(default_factory=list)
    rejected_claims: list[str] = Field(default_factory=list)
    contradictions_noted: list[str] = Field(default_factory=list)
    sources_current: bool
    uncertainty_notes: list[str] = Field(default_factory=list)
    approved_for_drafting: bool

    @model_validator(mode="after")
    def approval_requires_at_least_one_approved_claim(self) -> "EvidenceReview":
        """Book 1 §9.5: the reviewer verifies decisive claims are cited
        and approved before drafting may proceed. Approving drafting
        with nothing actually approved is a contradiction, not a valid
        review.
        """
        if self.approved_for_drafting and not self.approved_claims:
            raise ValueError("approved_for_drafting requires at least one approved claim")
        return self
