# Class 2 Homework

## Starting checkpoint

`../class-01/golden-solution/` (or your own Class 1 submission)

## Required (30–45 minutes)

1. Add `config/products.yaml`, `config/icp.yaml`, `config/policies.yaml` with WidgetWare's real business facts (see `docs/widgetware-business-brief.md`).
2. Add `src/widgetware_sdr/instructions.py` (fixed system instructions, centralized model selection) and `src/widgetware_sdr/context_builder.py` (assembles the four context layers, with account content always confined to a delimited, labeled evidence section).
3. Add all four required context tests: a clearly qualified account, a clearly unqualified account, an account with insufficient evidence, and a malicious note that attempts to override policy.
4. Confirm `./scripts/check.sh` passes with all tests green.

## Diagnostic (targeted fix)

The provided `malicious-note` test case in `golden-solution/` currently only checks that the note text is *present* in the assembled prompt. Strengthen it to also confirm the note text does not appear anywhere before `=== BEGIN EVIDENCE ===` — i.e., prove positionally, not just by presence, that it never reached the instructions or business-context sections.

## Extension (optional)

Add a fifth context quality failure test from §3.6's list not covered in class — for example, "stale data presented as current": construct an account profile where one field is explicitly marked with an old `retrieved_at` date, and confirm the assembled context surfaces that staleness rather than presenting it as equally current with fresher fields.

## Submission

- Test output showing all context tests passing.
- The assembled-context printout (`context.assembled_prompt`) for the malicious-note case, so the delimiting is visible.

## Constraints

- No ADK `Agent` object yet. This chapter builds the context an agent will receive, not the agent itself — resist the urge to jump ahead to Class 3's territory.
- Business facts in `config/icp.yaml` must match `docs/widgetware-business-brief.md` exactly — drift here will silently break Class 3's sample account profiles.

## What "done" looks like

You can print `context.assembled_prompt` for any of the four scenario accounts, read it top to bottom, and understand exactly what a model would see and why — including exactly where the untrusted content begins and ends.
