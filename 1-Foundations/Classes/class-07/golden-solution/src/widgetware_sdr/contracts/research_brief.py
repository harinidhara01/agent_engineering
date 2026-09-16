"""The ResearchBrief contract — Book 1, Chapter 8's evidence ledger (§8.7).

A durable structure that never contains a floating factual claim whose
source has been lost, and never silently resolves a conflict between
sources.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from widgetware_sdr.contracts.evidence import EvidenceItem


class Claim(BaseModel):
    """One claim the research produced, always tied to its evidence."""

    model_config = {"extra": "forbid"}

    text: str
    evidence_refs: list[str] = Field(default_factory=list)
    classification: str = "verified_fact"  # Book 1 §3.5's five evidence categories


class Conflict(BaseModel):
    """Two or more sources disagreeing — surfaced, never silently resolved."""

    model_config = {"extra": "forbid"}

    field: str
    values: list[str]
    evidence_refs: list[str]
    likely_explanation: str | None = None
    affects_qualification: bool = False


class ResearchBrief(BaseModel):
    model_config = {"extra": "forbid"}

    account_id: str
    research_questions: list[str] = Field(default_factory=list)
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    conflicts: list[Conflict] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    trigger_events: list[str] = Field(default_factory=list)
    summary: str
    recommended_next_step: str

    @model_validator(mode="after")
    def reject_uncited_material_claims(self) -> "ResearchBrief":
        """Book 1 §8.7: 'a research brief should never contain a floating
        factual assertion whose source has been lost.' A material claim
        (verified_fact or derived_fact) with no evidence_refs, or one
        pointing at an evidence_id that doesn't exist in this brief, is
        rejected here rather than allowed to pass silently.
        """
        evidence_ids = {item.evidence_id for item in self.evidence_items}
        for claim in self.claims:
            if (
                claim.classification in ("verified_fact", "derived_fact")
                and not claim.evidence_refs
            ):
                raise ValueError(f"material claim {claim.text!r} has no evidence reference")
            for ref in claim.evidence_refs:
                if ref not in evidence_ids:
                    raise ValueError(f"claim references unknown evidence_id {ref!r}")
        return self
