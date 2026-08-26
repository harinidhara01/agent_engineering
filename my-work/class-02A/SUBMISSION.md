# Class 02A Submission

## Student
- Name: Nagadhara Harini Kanakala
- GitHub: https://github.com/harinidhara01
- Branch / commit: main / 4eb62be

---

# Baseline observations

## L1

The available specialist skill was `renewal-advisor`. Before editing `SKILL.md`, its L1 description was only a placeholder and did not provide enough information for reliable skill discovery or routing. It did not clearly indicate that the skill handled renewal timing, discounts, risk, quotes, approvals, or renewal briefs.

## L2

Before completing the skill, the L2 operating procedure was incomplete. It did not provide clear instructions for when to use the skill, required inputs, exact resource routing, minimum-resource loading, citation requirements, or unsupported-question handling.

## L3

The starter skill could not reliably route a renewal discount question to the correct policy. It attempted to use `references/policy.md`, which did not exist, instead of the actual resource `references/discount-policy.md`. As a result, the agent could not reliably determine the discount approval procedure.

---

# Final trace evidence

## Case A
- Predicted L3: `references/discount-policy.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `references/discount-policy.md`
- Final result: Correct approval path for a 12% discount.
- Unnecessary resources loaded: None observed.

## Case B
- Predicted L3: `references/renewal-process.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `references/renewal-process.md`
- Final result: Correct action for a renewal 75 days away.
- Unnecessary resources loaded: None observed.

## Case C
- Predicted L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Final result: Combined action plan covering discount approval, renewal timing, high churn risk, and Legal escalation for auto-renewal removal.
- Unnecessary resources loaded: `assets/renewal-brief-template.md` and `scripts/calculate_quote.py` were avoided.

## Case D
- Predicted L3: `assets/renewal-brief-template.md` plus the policy references required by the facts in the request.
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: Verify the exact paths from your Case D trace before submission.
- Final result: Approval-ready renewal brief using the official format without fabricating missing information.
- Unnecessary resources loaded: Verify from the trace.

## Case E
- Predicted L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Final result: Deterministic calculation of dollar discount and net ARR plus the correct approval path.
- Unnecessary resources loaded: `references/renewal-process.md`, `references/risk-escalation.md`, and `assets/renewal-brief-template.md` were avoided.

## Case F
- Predicted L3: `references/risk-escalation.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `references/risk-escalation.md`
- Final result: Safely stated that the supplied sources do not support the requested SOC 2 control ID or recovery-time promise and provided the proper escalation route.
- Unnecessary resources loaded: `references/discount-policy.md`, `references/renewal-process.md`, `assets/renewal-brief-template.md`, and `scripts/calculate_quote.py` were avoided.

---

# What I learned

## Skill vs resource

A skill is a reusable procedure that tells the agent when to use it, how to handle a request, and which resources to load. A resource contains detailed information that the skill loads only when needed. In this lab, `renewal-advisor` is the skill, while the policy files, template, and calculator provide supporting evidence or execution.

## L1 → L2 → L3 progressive disclosure

L1 provides lightweight metadata for skill discovery and routing. After the skill is selected, L2 provides the operating procedure and tells the agent where to look. L3 contains the detailed policy, process, escalation guidance, templates, and executable logic needed for the specific request. This allows the agent to load detailed information only when necessary.

## Why minimum-resource loading matters

Loading only the resources required for a question reduces unnecessary context and lowers the chance that irrelevant information influences the answer. For example, a discount approval question can be answered using only `references/discount-policy.md` without loading renewal timing, risk escalation, the brief template, or the calculator.

## Why deterministic math belongs in a script

Dollar discount and net ARR calculations should use `scripts/calculate_quote.py` because deterministic arithmetic is more reliable when performed by a dedicated script. The skill can use the script output while keeping policy reasoning separate from mathematical execution.

## Why safe abstention can be a correct answer

When the supplied sources do not establish a requested fact, control ID, certification statement, or customer commitment, the agent should not invent an answer. It should clearly state that the sources do not support the request and use the appropriate escalation route. This is safer and more reliable than guessing.
