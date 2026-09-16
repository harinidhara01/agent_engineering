# Class 9 Slides — Evaluation and the Release Gate

12 slides, ~2 minutes of speaking notes each, for the 0:20–0:45 segment.

---

## Slide 1 — Current WidgetWare state: complete, but only manually checked

**On slide:** Class 8's workflow runs correctly — every time someone has watched it run.

**Say:** "It works. We've all seen it work. That's not the same claim as 'it will keep working.'"

---

## Slide 2 — Today's dependency

**On slide:** The state machine and contracts from Classes 5 through 8 don't change — today wraps them in a repeatable, automatic check.

**Say:** "Nothing about the workflow itself changes today. We're building the thing that watches it, systematically, instead of us watching it by hand."

---

## Slide 3 — Business objective

**On slide:** A mechanical yes/no answer to "is this system good enough to ship right now?"

**Say:** "Not a vibe. Not 'it looked fine in the demo.' A specific, repeatable, automated answer."

---

## Slide 4 — Core concept: a golden dataset (§10.2)

**On slide:** A fixed, representative, version-controlled set of cases with known-correct outcomes.

**Say:** "The dataset itself is the specification. If it's not checked into version control the same way the code is, you can't tell whether a passing gate today means the same thing it meant last week."

---

## Slide 5 — Terminology: metric vs. release gate (§10.3–10.4)

**On slide:** A metric measures. A gate decides, based on thresholds applied to metrics.

**Say:** "You can have a hundred good metrics and no way to say 'ship' or 'don't ship.' The gate is what turns measurement into a decision."

---

## Slide 6 — Architecture: the golden dataset's required categories (§10.2)

**On slide:** Qualified, disqualified, ambiguous, conflicting-evidence, injection-attempt — each represented on purpose, not by accident.

**Say:** "Every one of these categories exists because we've already seen it break something, somewhere in this course. A golden dataset that only covers the easy cases isn't testing anything hard."

---

## Slide 7 — Seven Steps mapping: Evaluate & Govern deepens

**On slide:** Class 5 validated one result. Today validates the whole system's behavior across representative cases.

**Say:** "Same step, wider lens. We went from 'is this one output trustworthy' to 'is this whole system, across everything it's likely to see, trustworthy.'"

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** Evaluation itself is entirely deterministic — no model call is needed to know whether the system met its own golden dataset's expectations.

**Say:** "The workflow being evaluated may call a model. The evaluation that checks it never needs to. That distinction matters — a flaky judge is worse than no judge."

---

## Slide 9 — Security: a gate that fails loudly (§10.5)

**On slide:** `ReleaseGateResult` reports every unmet condition, not just the first one found.

**Say:** "If three things are broken and the gate only tells you about one, you'll fix that one, re-run, and get surprised by the second. Report everything, every time."

---

## Slide 10 — Today's increment

**On slide:** `eval/golden_dataset.py`, `eval/metrics.py`, `eval/release_gate.py`, `eval/observability.py`.

**Say:** "Ten representative cases, a handful of metrics computed from running them, one function that turns all of it into pass or fail with named reasons."

---

## Slide 11 — Lab architecture: running the dataset, not one case at a time

**On slide:** The full golden dataset runs through the real workflow every time, using deterministic stub agents.

**Say:** "We use stub agents today so the evaluation itself is fast and repeatable — not because live model behavior doesn't matter, but because *this* layer's job is to catch structural regressions, every single run, without waiting on an API call."

---

## Slide 12 — Acceptance criteria: a gate that's actually calibrated

**On slide:** A gate too easy to pass is as useless as one too strict to ever pass — both need to be argued, not assumed.

**Say:** "Anyone can write a gate that always passes, or one that never does. The actual work today is making one that's calibrated to a real bar — and being able to explain, out loud, why that bar is the right one."
