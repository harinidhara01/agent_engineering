# Class 9 — Evaluation and the Release Gate

**Manuscript source:** Book 1, Chapter 10 — Evaluation and the Release Gate
**Seven-Step mapping:** Primary: Evaluate & Govern / Supporting: Orchestrate Workflows
**Golden solution produced:** `class-09/golden-solution/`
**Starting checkpoint:** `class-08/golden-solution/`

## 0:00–0:20 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to show the approval-boundary test they added and explain, in one sentence, what state transition it proves is impossible.
- **Common mistakes to flag:** state machine tests that only exercise the happy path (RECEIVED → ... → APPROVED) with no illegal-transition test; approval logic that lives in more than one place.
- **Golden solution reveal:** run Class 8's full workflow live for one account end to end, then ask: "This worked. How do you know it'll keep working after the next code change, for accounts you didn't just watch by hand?" (Answer: you don't, yet. That's today's gap.)

## Slide outline (0:20–0:45)

1. Current WidgetWare state: a complete bounded workflow that's only ever been checked by watching it run
2. Today's dependency: the state machine and contracts from Classes 5–8 don't change — today wraps them in a repeatable, automatic check
3. Business objective: a mechanical yes/no answer to "is this system good enough to ship right now?"
4. Core concept: a golden dataset (§10.2) — a fixed, representative, version-controlled set of cases with known-correct outcomes
5. Terminology: metric vs. release gate (§10.3–10.4) — a metric measures; a gate decides, based on thresholds applied to metrics
6. Architecture: `GOLDEN_DATASET`'s required categories (§10.2) — qualified, disqualified, ambiguous, conflicting-evidence, injection-attempt, and more, each represented on purpose
7. Seven Steps mapping: Evaluate & Govern deepens — Class 5 validated one result; today validates the whole system's behavior across representative cases
8. Gemini vs. deterministic code: evaluation itself is entirely deterministic — no model call is needed to know whether the system met its own golden dataset's expectations
9. Security: a gate that fails loudly (§10.5) — `ReleaseGateResult` reports every unmet condition, not just the first one found
10. Today's increment: `eval/golden_dataset.py`, `eval/metrics.py`, `eval/release_gate.py`, `eval/observability.py`
11. Lab architecture: running the full golden dataset through the real workflow and computing pass/fail per category
12. Acceptance criteria: a release gate that's too easy to pass is as useless as one that's too strict to ever pass — both need to be argued, not assumed

## Kahoot (8 questions)

- Terminology: What is the difference between a metric and a release gate (§10.3–10.4)?
- Terminology: Why does a golden dataset need to be version-controlled, not regenerated fresh each run?
- Architecture: Why does `GOLDEN_DATASET` deliberately include an injection-attempt case and a conflicting-evidence case, not just qualified/disqualified pairs?
- Architecture: Why does `check_release_gate()` collect and report every failing reason instead of stopping at the first one?
- Failure analysis: A release gate passes, but a real account later breaks the system in a way the golden dataset never covered — is the gate wrong?
- Security/governance: What does "fails loudly" mean for a release gate, concretely, and why does that matter more than "fails accurately"?
- WidgetWare scenario: `approval_compliance_rate()` only recognizes four workflow states at this checkpoint — what happens to that metric once Class 10 adds two more states?
- Connecting back: How does the release gate's category-by-category structure reuse the same "many small checkable things beat one large trust-it verdict" idea from Class 5's business invariants?

## Build together (0:55–1:35)

- `eval/golden_dataset.py` — `GOLDEN_DATASET`, 10 `GoldenCase` entries spanning `REQUIRED_CATEGORIES`
- `eval/metrics.py` — deterministic metrics computed from a batch of workflow runs, including `approval_compliance_rate()`
- `eval/release_gate.py` — `check_release_gate(...)` returning `ReleaseGateResult(passed, reasons)`, reporting all failures
- `eval/observability.py` — structured run logging sufficient to reconstruct why a case passed or failed after the fact

## Test and diagnose (1:35–1:50)

1. Run the full golden dataset through the real workflow (using deterministic stub agents, not live credentials) and confirm each category's expected outcome.
2. Deliberately break one business rule (e.g., allow `QUALIFIED` with no evidence) and confirm the release gate catches it and names the specific failing category.
3. Confirm the gate reports *every* unmet condition when multiple things are broken at once, not just the first.
4. Inspect `approval_compliance_rate()`'s known limitation: it only recognizes the four states that exist through Class 8 — flag this as this checkpoint's own documented gap, not a bug to silently patch today.
5. Diagnose using the Framework's seven categories — this class's failures are almost always **evaluation design** (a category the golden dataset doesn't cover) rather than a workflow bug.
6. Apply the smallest fix — usually adding a missing golden-dataset case, not rewriting the gate logic.
7. Re-run the full golden dataset and confirm the gate result is stable across repeated runs.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | `GOLDEN_DATASET` covers all required categories, `check_release_gate()` correctly passes a healthy system and fails an unhealthy one with named reasons |
| **Diagnostic** | The provided release gate currently stops evaluating after the first golden-dataset case fails, instead of running all ten and reporting every failure. Find the early-return and fix it so a single run always reports the complete picture |
| **Extension** | Add an eleventh golden-dataset case of your own devising that covers a realistic WidgetWare scenario none of the existing ten categories represent, and show it changes the gate's outcome when deliberately broken |

- **Starting checkpoint:** `class-08/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/eval/`, `tests/`
- **Expected behavior:** the release gate is a single, repeatable, automatic answer to "does this system currently meet its own bar" — never a manual judgment call
- **Tests that must pass:** golden-dataset category tests, release-gate pass/fail tests, the "reports every failure" test
- **Submission:** one full `ReleaseGateResult` output showing a deliberately broken system correctly failing with all reasons named
- **Constraints:** no loop yet — this checkpoint evaluates a single run of the workflow per golden-dataset case, not a batch or retry loop (that's Class 10)

## Golden solution: `class-09/`

Adds the evaluation and release-gate layer on top of `class-08/` without changing the workflow itself. README states plainly: "This checkpoint proves the Class 8 workflow is good enough to ship... No loop yet — that's Class 10, deliberately after this one."

## Bridge to Class 10

Class 10 wraps the workflow in a bounded, unattended loop — processing a queue of accounts under a budget, with retry, escalation, and stop conditions — and extends the state machine with two new states that `approval_compliance_rate()` doesn't yet recognize, which this checkpoint's own `KNOWN_FAILURE_CASES.md` flags as the very next thing to fix.
