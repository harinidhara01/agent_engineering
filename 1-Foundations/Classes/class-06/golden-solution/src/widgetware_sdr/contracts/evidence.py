"""The EvidenceItem contract — Book 1, Chapter 6.

A qualification result refers to evidence by stable identifiers rather
than copying large passages. This is the typed shape of one such item.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class SourceType(str, Enum):
    account_note = "account_note"
    internal_record = "internal_record"
    public_web = "public_web"
    enterprise_document = "enterprise_document"


class EvidenceItem(BaseModel):
    """One piece of evidence a qualification claim can point to.

    `source_uri` and `source_name` are both optional individually, but
    at least one should be set in practice — internal records may only
    have a name, while public web evidence should have a URI.
    """

    model_config = {"extra": "forbid"}

    evidence_id: str
    source_type: SourceType
    source_uri: str | None = None
    source_name: str | None = None
    retrieved_at: str
    claim: str
    excerpt: str
    freshness: str | None = None
    reliability: str | None = None
