---
name: renewal-advisor
description: Advises on customer subscription renewals, including renewal timing, discount requests, quote calculations, approval and escalation questions, renewal risk, contract-change requests, and preparation of renewal briefs. Use for questions about renewal timing, discounts, quotes, required approvals, escalations, renewal risks, auto-renewal changes, or official renewal briefs. Do not use for unrelated product troubleshooting or general product support.
---

# Renewal Advisor

## When to use

Use this skill for questions involving:

- Customer subscription renewals.
- Renewal timing or required renewal actions.
- Renewal discount requests or required discount approvals.
- Churn risk or renewal escalation.
- Regulated customers requesting new security, privacy, resilience, or compliance commitments.
- Requests to remove or rewrite auto-renewal language.
- Preparation of an official renewal or approval brief.
- Deterministic calculation of discount amount or net ARR when part of a renewal request.

## When not to use

Do not use this skill for:

- Product troubleshooting that does not involve a renewal.
- General product support or how-to questions.
- Requests unrelated to renewal work.
- Situations where the user's intent is ambiguous and the correct skill is unclear.

For unsupported questions, do not invent an answer. Follow the escalation behavior below.

## Required inputs

Determine which inputs are required for the specific request.

Possible required inputs include:

- Current ARR.
- Requested discount percentage.
- Renewal date or days remaining.
- Churn risk.
- Customer type or regulated status.
- Requested contract changes.
- Customer name when preparing a renewal brief.

If a required input is missing, ask for the missing input rather than assuming a value.

Do not request inputs that are unnecessary for the question being answered.

## Procedure

1. Analyze the request and identify the core question, such as discount approval, renewal timing, escalation, renewal brief, or calculation.
2. Determine the minimum required inputs. If a required input is missing, ask for it rather than assuming it.
3. Use the exact routing map below to load only the minimum necessary L3 resource, asset, or script.
4. Apply only facts supported by the loaded resources or deterministic script output.
5. Provide the answer with the required citation and clearly distinguish requested, routed, and approved states.

## Resource routing map

| Question type | Exact minimum resource or tool |
| --- | --- |
| Discount approval path | `references/discount-policy.md` |
| Renewal timing or required renewal actions | `references/renewal-process.md` |
| High churn risk with limited time remaining | `references/risk-escalation.md` |
| Regulated customer requesting a new security, privacy, resilience, or compliance commitment | `references/risk-escalation.md` |
| Guaranteed recovery time or unsupported service-level commitment | `references/risk-escalation.md` |
| Remove or rewrite auto-renewal language | `references/renewal-process.md` and/or `references/risk-escalation.md` only when both process and escalation guidance are needed |
| Official renewal or approval brief | `assets/renewal-brief-template.md` plus only the policy references required by the facts in the request |
| Dollar discount or net ARR calculation | `scripts/calculate_quote.py` |
| Calculation plus discount approval path | `scripts/calculate_quote.py` and `references/discount-policy.md` |
| Missing source or policy conflict | `references/risk-escalation.md` |

Minimum resource rule: load the fewest resources necessary to answer the request. Do not load a reference, asset, or script merely because it exists or because it might be generally relevant.

## Output contract

The response must:

- Answer only using facts supported by the loaded resources or deterministic script output.
- Cite the exact resource path used for policy or process guidance.
- Use deterministic calculator output for dollar discount and net ARR when those values are requested.
- Clearly identify required approvals or escalation routes when supported by the loaded resources.
- Clearly distinguish between `requested`, `routed`, and `approved`.
- For a renewal brief, follow the official structure in `assets/renewal-brief-template.md`.
- Identify missing required information instead of fabricating it.

## Unsupported and missing-source behavior

If a request requires a fact, policy, control ID, certification statement, recovery-time guarantee, or other commitment that is not established by the supplied resources:

- State that the provided sources do not support or establish the requested information.
- Do not invent a control ID, policy rule, approval, or customer commitment.
- Use the escalation route specified in `references/risk-escalation.md` when applicable.
- If a required resource is missing or a policy conflict exists, route the issue to the policy owner and do not guess.

## Examples

### Positive

- "The renewal ARR is $92,000 and the requested discount is 12%. Which approval path is required?"
- "The renewal date is 75 days away. What should the CSM do now?"
- "The customer is high risk and the renewal is in 10 days. What escalation is required?"
- "Create an approval-ready renewal brief using the official format."
- "Calculate the dollar discount and net ARR for $92,000 at 12%, then state the approval path."

### Negative

- "My product is showing an error. How do I fix it?"
- "How do I configure WidgetWare?"
- "Why is the application failing to start?"

### Ambiguous

- "I need help with a renewal."
- "Can you tell me about discounts?"
- "The customer has a question about our service."
- "What should I do next?"

For ambiguous cases, ask clarifying questions to determine the user's intent before loading resources or executing scripts.
