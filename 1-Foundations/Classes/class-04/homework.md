# Class 4 Homework

## Starting checkpoint

`../class-03/golden-solution/` (or your own Class 3 submission)

## Required (30–45 minutes)

1. Build `skills/icp_qualification/` (skill.md, three examples, cases.yaml) and `skills/evidence_classification/skill.md`.
2. Build `src/widgetware_sdr/skills.py` and refactor `qualification_agent.py` to load its procedure via `load_skill()`.
3. Confirm the agent's instruction is assembled entirely from fixed instructions + config + Skill content — no embedded procedure left in Python.
4. Get all offline unit tests passing (`./scripts/check.sh`); if you have live credentials, also run `pytest tests/integration -v` and read the three responses.

## Diagnostic (targeted fix)

The provided Evidence Classification Skill's examples are correct, but one deliberately ambiguous fact in `tests/fixtures/accounts/meridian-003.yaml`'s notes ("recently discussed modernization initiatives") is genuinely borderline between "inference" and "unknown." Write down which category you think it should be, why, and add that reasoning as a fourth example to `skills/evidence_classification/skill.md`.

## Extension (optional)

Write a second, independent Skill consumer — a small standalone script (not `qualification_agent.py`) that calls `load_skill("icp_qualification")` and prints its procedure. This proves the Skill is genuinely reusable outside the one agent that currently uses it, which is the whole point of today's refactor.

## Submission

- `./scripts/check.sh` output showing all offline tests passing.
- If you ran the live integration tests: the printed event sequence for one scenario, and one sentence on whether the response avoided inventing missing data.
- If you didn't have credentials available: say so explicitly rather than silently skipping this part.

## Constraints

- No structured/typed output yet — the agent's result stays prose at this stage, on purpose. Class 5 replaces it with a contract.
- No tools yet. The agent still only reasons over what it's directly given. Class 6 adds tools.
- The agent's static instruction must never contain a specific account's data — verify with `test_instruction_contains_no_specific_account_data`.

## What "done" looks like

You can point at `skills/icp_qualification/skill.md` and say "this, not the Python file, is where the qualification logic actually lives" — and prove it by editing only the Skill to fix a reasoning gap, never the agent code.
