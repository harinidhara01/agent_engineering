Branch / commit: main / 4eb62be# Class 02A Submission

## Student
- Name: Nagadhara Harini Kanakala
- GitHub: harinidhara01
- Branch / commit: main / 4eb62be

---

# Baseline observations

## L1

The available specialist skill was `renewal-advisor`. Before editing `SKILL.md`, its description was a placeholder and did not provide enough information for reliable skill discovery or routing.

## L2

The L2 operating procedure was incomplete. It did not clearly define when to use the skill, required inputs, exact resource paths, minimum-resource loading, citation requirements, or unsupported-question handling.

## L3

The starter skill could not reliably route a discount request to the correct policy. It attempted to load `references/policy.md`, which did not exist, instead of `references/discount-policy.md`.

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
- Unnecessary resources loaded: None observed.

## Case D
- Predicted L3: `assets/renewal-brief-template.md` plus the policy references required by the request.
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `assets/renewal-brief-template.md`, `references/discount-policy.md`, `references/renewal-process.md`, `references/risk-escalation.md`
- Final result: Approval-ready renewal brief using the official format without fabricating missing information.
- Unnecessary resources loaded: None observed.

## Case E
- Predicted L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `scripts/calculate_quote.py`, `references/discount-policy.md`
- Final result: Deterministic calculation plus the correct approval path.
- Unnecessary resources loaded: None observed.

## Case F
- Predicted L3: `references/risk-escalation.md`
- Observed L1: `renewal-advisor`
- Observed L2: Yes
- Observed L3: `references/risk-escalation.md`
- Final result: Safely handled the unsupported SOC 2 control request and provided the escalation route.
- Unnecessary resources loaded: None observed.

---

# What I learned

## Skill vs resource

A skill is a reusable procedure that tells the agent when and how to handle a request and which resources to use. A resource contains detailed information loaded only when needed.

## L1 → L2 → L3 progressive disclosure

L1 provides lightweight metadata for skill discovery. L2 provides the operating procedure and exact routing instructions. L3 contains detailed policies, processes, templates, and execution logic that are loaded only when required.

## Why minimum-resource loading matters

Loading only the resources needed for a request reduces unnecessary context and lowers the risk of irrelevant information affecting the answer. For example, a discount approval question only needs `references/discount-policy.md`.

## Why deterministic math belongs in a script

Deterministic calculations such as discount amount and net ARR should be performed by `scripts/calculate_quote.py` so arithmetic is reliable and reproducible.

## Why safe abstention can be a correct answer

When the supplied sources do not establish the requested information, the agent should not guess or invent an answer. It should state that the information is unsupported and use the appropriate escalation route.
