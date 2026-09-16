# Class 1 — Common Mistakes to Watch For (0:20–0:30)

Class 1 has no previous homework to review — this is the first class. Use this segment instead to preview the mistakes participants are about to make, live, in the next hour, drawing on what's recurred across past cohorts.

## In the charter (acceptance criteria, `SPEC.md`, business brief)

- **Desired-behavior language, not a checkable signal.** "The system should be helpful" or "the system explains itself well" survives into a first draft unchanged. Push for: what would a person actually *check* — a specific field present, a specific string absent, a specific test passing?
- **Marketing copy instead of constraints in `SPEC.md`.** A common first draft reads like a product pitch ("WidgetWare's intelligent system will..."). Redirect to falsifiable statements: required behavior, prohibited behavior, error behavior.
- **Missing or vague prohibited-behavior list.** "The system should be safe" is not a prohibited-behavior list. "The system must never send an outbound message autonomously" is.
- **Scenarios that are actually easy, dressed up as hard.** An "ambiguous" account that's obviously disqualified once you read closely doesn't exercise `NEEDS_RESEARCH`. Push participants to make it genuinely ambiguous — missing exactly one decisive fact, not missing everything.
- **ICP details drifting from the canonical WidgetWare facts.** Watch for employee-count thresholds, industries, or regions that don't match `docs/widgetware-business-brief.md` exactly — small transcription drift here compounds once Class 2 turns these numbers into `config/icp.yaml`.

## In the harness

- **Skipping the bad-task/good-task comparison.** A pair that jumps straight to the properly-scoped Antigravity prompt has skipped the actual lesson of Book 1 §2.6 — the *difference* between an unscoped and a scoped task, not just knowing how to write a scoped one. Look for evidence the comparison happened: a note, a kept transcript, a sentence in the README.
- **A health check that isn't actually deterministic.** No network call, no model call, no dependency on an environment variable with no default. If `health_check()` would behave differently on a clean clone versus the author's own machine, that's a real defect — it directly contradicts this checkpoint's own evaluation criterion.
- **`scripts/check.sh` that silently narrows what "all checks" means.** A script that only runs `pytest`, dropping the format, lint, and type-check stages, has narrowed the gate without saying so. Run it and confirm all five stages actually execute.
- **`.agents/` rules that restate good intentions instead of stating checkable rules.** "Write high-quality code" isn't a rule an agent — or a person — can act on differently than they already would. "Every function in `src/` has a type annotation" is something `mypy` can actually enforce.

## Talking points to set up the build segment

- Ask: "If nothing in this repository could be run by a stranger, would you trust that it works?" Most will correctly say no — that's the whole reason this class now includes the harness, not just the charter.
- Preview the credential-shape test before revealing it: ask what should happen if someone accidentally pastes a real API key into a config file. The expected answer ("a test should catch it") sets up the live demonstration in "Test and diagnose."

## Golden solution reveal

There is no prior golden solution to walk through — instead, once the room has drafted its own charter and harness, open `golden-solution/README.md` and read the Quick Start sequence together. Run `./scripts/check.sh` live and let the room watch all five stages actually pass. Ask: "Is this the same thing we just built, or does it do more?" The expected answer is "the same shape, possibly different wording" — not "this does something ours doesn't," which would mean the class's own build segment under-scoped the task.
