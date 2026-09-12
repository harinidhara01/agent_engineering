# Class 6 Homework

## Starting checkpoint

`../class-05/golden-solution/` (or your own Class 5 submission)

## Required (30–45 minutes)

1. Build the three tools (`get_account_profile`, `get_widgetware_product`, `get_icp_policy`) and `calculate_fit_score()`.
2. Attach the three read tools to the agent, and update its instruction to use them instead of assuming facts.
3. Confirm the agent's qualification results now carry real, traceable evidence references — pointing at facts the tools actually returned, not assumed values.
4. Get `./scripts/check.sh` passing, offline tests included.

## Diagnostic (targeted fix)

The provided test suite includes a case where a `QualificationResult` is constructed with `status=QUALIFIED` and an `evidence_refs` entry — but that entry doesn't actually correspond to any fact a tool returned; it was invented. Nothing in Class 5's contract validation catches that, because the contract only checks that the *field is non-empty*, not that its contents are *real*. Write a test that would catch a fabricated evidence reference, and explain in one sentence why the contract layer alone (Class 5) can't fully solve this — what layer would need to?

## Extension (optional)

Pick one tool and write the full seven-item test list from §7.8, including the three this checkpoint's own tests skip (dependency failure, permission failure, redaction of prohibited fields) — you'll need to invent a plausible way each could apply even though this checkpoint's tools don't currently have that failure mode for real. Document your reasoning, not just the test code.

## Submission

- `./scripts/check.sh` output, all green.
- One full `QualificationResult` JSON output for the Acme Manufacturing account, with `evidence_refs` populated and traceable to tool calls.
- Your one-sentence answer to the Diagnostic's question about contract vs. semantic validation.

## Constraints

- Tools remain read-only. No send action, no CRM write — still Book 1's standing boundary from Class 1.
- `calculate_fit_score()` must not be exposed to the model as a callable tool — it's application code the workflow calls directly, not something the model invokes.

## What "done" looks like

You can point at any `evidence_refs` entry in a qualification result and trace it back to a specific tool call the agent actually made — never an assumed or invented fact.
