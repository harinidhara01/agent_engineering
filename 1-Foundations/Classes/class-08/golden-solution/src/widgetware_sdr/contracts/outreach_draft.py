"""The OutreachDraft contract — Book 1, Chapter 9 (§9.4).

The Outreach Drafting Agent's typed output. `used_claims` must be a
subset of the EvidenceReview that produced this draft — enforced by the
builder that constructs a draft (see workflow/coordinator.py), not by
this model in isolation, since a bare OutreachDraft has no way to know
which review it came from.

No send capability exists anywhere near this contract. It is a draft, a
request, never an action.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class OutreachDraft(BaseModel):
    model_config = {"extra": "forbid"}

    account_id: str
    message: str
    used_claims: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    requested_action: str = "send_outreach"
