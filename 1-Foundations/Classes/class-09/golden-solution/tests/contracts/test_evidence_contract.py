import pytest
from pydantic import ValidationError

from widgetware_sdr.contracts.evidence import EvidenceItem, SourceType


def test_a_well_formed_evidence_item_validates() -> None:
    item = EvidenceItem(
        evidence_id="ev-001",
        source_type=SourceType.account_note,
        source_name="customer_note",
        retrieved_at="2026-01-15",
        claim="The operations team still runs approvals through paper checklists.",
        excerpt="...paper checklists...",
    )
    assert item.evidence_id == "ev-001"


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvidenceItem(
            evidence_id="ev-001",
            source_type=SourceType.account_note,
            retrieved_at="2026-01-15",
            claim="Missing excerpt.",
        )


def test_unknown_source_type_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvidenceItem(
            evidence_id="ev-001",
            source_type="rumor",
            retrieved_at="2026-01-15",
            claim="A claim.",
            excerpt="An excerpt.",
        )
