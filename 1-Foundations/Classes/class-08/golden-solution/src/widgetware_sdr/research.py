"""Account research pipeline — Book 1, Chapter 8.

Builds a ResearchBrief from a research source's raw output: normalizes
records into EvidenceItem contracts, detects conflicts between sources,
and never lets a claim exist without a citation. Every step here is
deterministic — no model call happens in this module. The agent that
uses a model to actually *interpret* this evidence is
`agents/research_agent.py`.
"""

from __future__ import annotations

import re
from typing import Any

from widgetware_sdr.contracts.evidence import EvidenceItem, SourceType
from widgetware_sdr.contracts.research_brief import Claim, Conflict, ResearchBrief
from widgetware_sdr.tools.research_tools import search_public_records

DEFAULT_RESEARCH_QUESTIONS = [
    "What industry does the company operate in?",
    "Approximately how large is it?",
    "Does it show evidence of legacy plant-floor systems or automation gaps?",
    "Has it announced a digital-transformation or AI initiative?",
    "Is there a recent trigger event relevant to WidgetWare?",
]

_EMPLOYEE_COUNT_PATTERN = re.compile(r"approximately ([\d,]+) employees")


def normalize_evidence(raw_records: list[dict[str, Any]], account_id: str) -> list[EvidenceItem]:
    """Turn raw research-tool output into typed, sourced EvidenceItems.

    Every item is preserved, including one containing an injection
    attempt — normalization records evidence, it does not judge it.
    """
    items = []
    for index, record in enumerate(raw_records):
        items.append(
            EvidenceItem(
                evidence_id=f"{account_id}-ev-{index + 1:03d}",
                source_type=SourceType(record.get("source_type", "public_web")),
                source_name=record["source"],
                retrieved_at=record["retrieved_at"],
                claim=record["text"],
                excerpt=record["text"][:200],
            )
        )
    return items


def detect_employee_count_conflict(evidence_items: list[EvidenceItem]) -> Conflict | None:
    """A narrow, rule-based conflict detector: looks specifically for
    differing "approximately N employees" figures across evidence.

    Book 1 §8.4 does not specify a general algorithm for detecting
    conflicts across arbitrary claims — a real implementation would
    need much more than a regular expression. This is a deliberate
    simplification, documented in KNOWN_FAILURE_CASES.md, not a general
    solution.
    """
    values_by_evidence_id: dict[str, str] = {}
    for item in evidence_items:
        match = _EMPLOYEE_COUNT_PATTERN.search(item.claim)
        if match:
            values_by_evidence_id[item.evidence_id] = match.group(1)

    distinct_values = sorted(set(values_by_evidence_id.values()))
    if len(distinct_values) > 1:
        return Conflict(
            field="employee_count",
            values=distinct_values,
            evidence_refs=list(values_by_evidence_id.keys()),
            likely_explanation="sources report different dates",
            affects_qualification=True,
        )
    return None


def build_research_brief(
    account: dict[str, Any], research_questions: list[str] | None = None
) -> ResearchBrief:
    """Build a complete ResearchBrief for one account, deterministically.

    Any evidence item involved in a detected conflict is excluded from
    `claims[]` — the conflict itself is surfaced in `conflicts[]`
    instead, never silently resolved by picking one value.
    """
    account_id = account["account_id"]
    raw_records = search_public_records(account_id)
    evidence_items = normalize_evidence(raw_records, account_id)

    conflicts: list[Conflict] = []
    employee_count_conflict = detect_employee_count_conflict(evidence_items)
    if employee_count_conflict:
        conflicts.append(employee_count_conflict)

    conflicting_evidence_ids = {ref for conflict in conflicts for ref in conflict.evidence_refs}

    claims = [
        Claim(text=item.claim, evidence_refs=[item.evidence_id], classification="verified_fact")
        for item in evidence_items
        if item.evidence_id not in conflicting_evidence_ids
    ]

    unknowns = [] if evidence_items else ["no public evidence found for this account"]

    summary = (
        f"{len(evidence_items)} evidence item(s) gathered; {len(conflicts)} conflict(s) detected."
    )
    recommended_next_step = (
        "NEEDS_RESEARCH" if (not evidence_items or conflicts) else "proceed to qualification"
    )

    return ResearchBrief(
        account_id=account_id,
        research_questions=research_questions or list(DEFAULT_RESEARCH_QUESTIONS),
        evidence_items=evidence_items,
        claims=claims,
        conflicts=conflicts,
        unknowns=unknowns,
        trigger_events=[],
        summary=summary,
        recommended_next_step=recommended_next_step,
    )
