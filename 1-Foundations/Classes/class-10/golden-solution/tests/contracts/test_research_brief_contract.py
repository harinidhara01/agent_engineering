import pytest
from pydantic import ValidationError

from widgetware_sdr.contracts.evidence import EvidenceItem, SourceType
from widgetware_sdr.contracts.research_brief import Claim, ResearchBrief


def _evidence_item(evidence_id: str = "ev-001") -> EvidenceItem:
    return EvidenceItem(
        evidence_id=evidence_id,
        source_type=SourceType.public_web,
        source_name="Test Source",
        retrieved_at="2026-01-01",
        claim="A claim.",
        excerpt="A claim.",
    )


def test_a_well_formed_brief_validates() -> None:
    brief = ResearchBrief(
        account_id="acme-001",
        evidence_items=[_evidence_item()],
        claims=[Claim(text="A claim.", evidence_refs=["ev-001"])],
        summary="One item gathered.",
        recommended_next_step="proceed to qualification",
    )
    assert brief.account_id == "acme-001"


def test_material_claim_with_no_evidence_refs_is_rejected() -> None:
    """Book 1 §8.7: 'a research brief should never contain a floating
    factual assertion whose source has been lost.'
    """
    with pytest.raises(ValidationError):
        ResearchBrief(
            account_id="acme-001",
            evidence_items=[_evidence_item()],
            claims=[
                Claim(text="An uncited claim.", evidence_refs=[], classification="verified_fact")
            ],
            summary="Bad brief.",
            recommended_next_step="proceed to qualification",
        )


def test_claim_referencing_a_nonexistent_evidence_id_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ResearchBrief(
            account_id="acme-001",
            evidence_items=[_evidence_item("ev-001")],
            claims=[Claim(text="A claim.", evidence_refs=["ev-999"])],
            summary="Bad brief.",
            recommended_next_step="proceed to qualification",
        )


def test_an_inference_classified_claim_may_have_no_direct_evidence_ref() -> None:
    """Only verified_fact and derived_fact are 'material' in the sense
    §8.7 means — an inference is allowed to exist without a citation,
    as long as it's labeled as an inference, not a fact.
    """
    brief = ResearchBrief(
        account_id="acme-001",
        evidence_items=[_evidence_item()],
        claims=[
            Claim(
                text="This company is likely well-funded.",
                evidence_refs=[],
                classification="inference",
            )
        ],
        summary="One inference, unlinked but labeled.",
        recommended_next_step="NEEDS_RESEARCH",
    )
    assert brief.claims[0].classification == "inference"
