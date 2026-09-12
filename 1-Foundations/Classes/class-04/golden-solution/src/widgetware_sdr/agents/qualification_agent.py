"""The Account Qualification Assistant — Book 1, Chapters 4 and 5.

Chapter 4 gave this agent a narrow boundary: reason about a supplied
account profile, recommend QUALIFY / DO_NOT_QUALIFY / NEEDS_RESEARCH in
prose, and explain the reasoning. It may not search the internet, call
external services, update CRM data, or draft outreach — none of those
capabilities exist anywhere in this codebase yet.

Chapter 5 moved the qualification procedure itself out of this file and
into skills/icp_qualification/skill.md. This module assembles the
agent's *static* instruction from the fixed system instructions,
WidgetWare's business configuration, and the Skill's procedure — it
contains no qualification logic of its own. The specific account being
evaluated is never part of this static instruction; it arrives per-call
as the user message (see app.py), the same instruction-hierarchy
discipline Class 3 established.
"""

from __future__ import annotations

from google.adk.agents import Agent

from widgetware_sdr.context_builder import load_config
from widgetware_sdr.instructions import SYSTEM_INSTRUCTIONS, get_model_id
from widgetware_sdr.skills import load_skill


def build_agent_instruction() -> str:
    """Assemble the agent's static instruction.

    Includes: fixed system instructions, WidgetWare's ICP and escalation
    policy (rendered from config, not restated by hand), and the ICP
    Qualification Skill's procedure. Deliberately excludes any specific
    account — that would make this "static" instruction actually
    per-request, defeating the whole point of separating it from task
    context (Book 1 §3.2).
    """
    icp = load_config("icp.yaml")
    policies = load_config("policies.yaml")
    skill = load_skill("icp_qualification")

    return "\n\n".join(
        [
            SYSTEM_INSTRUCTIONS.strip(),
            "=== WIDGETWARE ICP ===",
            f"Minimum employee count: {icp['minimum_employee_count']}",
            f"Preferred industries: {', '.join(icp['preferred_industries'])}",
            f"Excluded industries: {', '.join(icp['excluded_industries'])}",
            f"Preferred regions: {', '.join(icp['preferred_regions'])}",
            f"Buying signals: {', '.join(icp['buying_signals'])}",
            "=== ESCALATION RULE ===",
            policies["escalation_rule"].strip(),
            "=== PROCEDURE (ICP Qualification Skill) ===",
            skill.strip(),
        ]
    )


def create_qualification_agent() -> Agent:
    """Construct the qualification agent. No network call happens here —
    only when the returned agent is actually run does a live Gemini
    call occur.
    """
    return Agent(
        name="qualification_agent",
        model=get_model_id(),
        description=(
            "Evaluates whether a target account fits WidgetWare's ideal "
            "customer profile, using only the account data it is given."
        ),
        instruction=build_agent_instruction(),
    )
