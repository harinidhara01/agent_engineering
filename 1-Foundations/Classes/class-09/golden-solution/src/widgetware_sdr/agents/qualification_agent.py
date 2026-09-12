"""The Account Qualification Assistant — Book 1, Chapters 4 through 7.

Chapter 4 gave this agent a narrow boundary: reason about a supplied
account profile and recommend an outcome in prose. It may not search
the internet, update CRM data, or draft outreach — none of those
capabilities exist anywhere in this codebase yet.

Chapter 5 moved the qualification procedure itself out of this file and
into skills/icp_qualification/skill.md. This module assembles the
agent's *static* instruction from the fixed system instructions,
WidgetWare's business configuration, and the Skill's procedure — it
contains no qualification logic of its own.

Chapter 6 replaced the agent's free-form prose output with the
`QualificationResult` contract (see contracts/qualification.py) —
enforced by the caller after the model responds, not by this module.

Chapter 7 attaches the agent's first real tools: three narrow, read-only
functions for retrieving account, product, and ICP data, so the model
stops being asked to already know facts that belong in a system of
record.
"""

from __future__ import annotations

from google.adk.agents import Agent

from widgetware_sdr.context_builder import load_config
from widgetware_sdr.instructions import SYSTEM_INSTRUCTIONS, get_model_id
from widgetware_sdr.skills import load_skill
from widgetware_sdr.tools.account_data import (
    get_account_profile,
    get_icp_policy,
    get_widgetware_product,
)


def build_agent_instruction() -> str:
    """Assemble the agent's static instruction.

    Includes: fixed system instructions, WidgetWare's ICP and escalation
    policy (rendered from config, not restated by hand), the ICP
    Qualification Skill's procedure, and — new this chapter — an
    instruction to use the attached tools rather than assume account or
    product facts. Deliberately excludes any specific account.
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
            "=== TOOLS ===",
            "Use get_account_profile, get_widgetware_product, and get_icp_policy "
            "to retrieve current facts. Do not state an account, product, or ICP "
            "fact from memory when a tool exists to look it up.",
            "=== OUTPUT FORMAT ===",
            "State your final answer as one of QUALIFY, DO_NOT_QUALIFY, or "
            "NEEDS_RESEARCH, with your rationale.",
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
            "customer profile, using only the account and product data "
            "it retrieves through its tools."
        ),
        instruction=build_agent_instruction(),
        tools=[get_account_profile, get_widgetware_product, get_icp_policy],
    )
