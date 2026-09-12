# Known Failure Cases — Class 1 Checkpoint

This checkpoint is genuinely runnable — `pip install -e ".[dev]"` and `./scripts/check.sh` both actually execute, and both actually pass. What follows is not "why this doesn't work"; it is an honest account of what this checkpoint deliberately does not yet prove, so a later class doesn't mistake a real gap for a regression.

## 1. No Gemini call exists yet

The health check makes no model call, by design. Nothing in this checkpoint can demonstrate that Gemini reasoning works, because nothing here invokes it. That starts Class 3 (Book 1, Chapter 4).

## 2. No ADK agent exists yet

There is no `google.adk.agents.Agent`, no session, no runner. `tests/unit/test_repository_contract.py` actively checks for the *absence* of an ADK import — that's a feature of this checkpoint, not an oversight to fix.

## 3. No live account research exists

`tests/fixtures/accounts/` and `tests/fixtures/expected/` describe three accounts and their expected qualification direction, but nothing in this codebase retrieves, researches, or evaluates them. There is no research pipeline until Class 6–7 (Book 1, Chapters 7–8).

## 4. Qualification directions are fixture expectations, not generated agent results

`expected_qualification_direction` in each `tests/fixtures/expected/*.yaml` file is a human's hand-applied reading of `docs/widgetware-business-brief.md`'s ICP, written down before any code exists to check it against. `tests/unit/test_repository_contract.py` verifies the *structure* of these fixtures (matching account IDs, an allowed direction value) — it does not and cannot verify that the *direction itself* is correct, because there is no independent qualification logic yet to check it against. Treat these values as a considered prediction, not a verified fact, until a real qualification agent exists (starting Class 3) and a contract enforces it (Class 5).

## 5. Product-level acceptance criteria are not yet implemented

`docs/acceptance-criteria.md` Section B (schema conformance, evidence citation, no drafting on insufficient evidence, explainability, usability) describes the finished system, not this checkpoint. None of Section B is tested here, and none of it should be — there is nothing yet for those criteria to apply to. Section A is what this checkpoint is actually held to, and Section A is fully enforced by `./scripts/check.sh`.

## 6. Antigravity GUI installation cannot be proven by portable repository tests

`verify_environment.py` deliberately does not check whether Antigravity is installed, authenticated, or configured on the machine running it — that's real state, but it's local, GUI-based state, not something a committed Python script run in someone else's environment could verify. A facilitator confirms this once, for a room, at the start of Class 1; a self-paced learner confirms it against `SETUP.md`. This is a considered scope boundary, not a gap to close later.

## 7. Only a small, illustrative scenario set exists

`tests/fixtures/accounts/` covers exactly one qualifying, one disqualifying, and one ambiguous account. This is enough to exercise the three qualification directions once code exists to check them, but it is not a representative dataset — Class 9's golden dataset (Book 1, Chapter 10) is where breadth actually gets addressed.

## 8. The no-send boundary is currently guaranteed by absence, not by a runtime check

`docs/architecture-decisions/0002-no-outbound-send.md` explains the reasoning: there is no send-capable function anywhere in `src/` for a policy check to gate, because the capability itself does not exist in code. `tests/unit/test_repository_contract.py` verifies this by scanning for send-shaped code, not by exercising a permission check at runtime — there is no runtime workflow yet for such a check to sit inside.

## 9. The health check proves the harness, not SDR intelligence

`health_check()` returning `{"status": "ok", ...}` proves the package installs, imports, and runs in a clean environment. It says nothing about whether WidgetWare's actual business problem is being solved — that claim doesn't become testable until real qualification logic exists, starting Class 3.
