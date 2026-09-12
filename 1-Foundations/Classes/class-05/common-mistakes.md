# Class 5 — Common Mistakes to Discuss (0:00–0:20)

Reviewing Class 4's homework before revealing `golden-solution/`.

## In the required build (Skill extraction)

- **A Skill that still leaves a "just in case" copy of the procedure in Python.** The point of the refactor was full extraction — a submission that keeps the old embedded string commented out, or duplicated as a fallback, hasn't actually completed Class 4's work, and it will bite today when the contract layer has two possibly-divergent sources of truth to validate against.

## In the diagnostic (Evidence Classification ambiguous case)

- **A category choice with no stated reasoning.** "I chose inference" without explaining *why* the modernization-initiatives note is inference rather than unknown doesn't demonstrate the judgment the diagnostic was testing for.

## Talking points to set up today's class

- Ask: "If I asked your production system to route on the agent's response right now, in code, how would you do it?" — most answers involve some form of string matching, which is exactly the fragility today's class removes.
- Preview the fail-safe principle before revealing it: ask what a parsing function *should* do when handed malformed input — crash, silently accept it, or something else. Most will land on "something else" without being able to name it yet; today gives it a name.

## Golden solution reveal

Run Class 4's agent live, print its raw prose response for the Acme account, then ask: "This looks right. How do you prove it, mechanically, to something that isn't a human reading it?" Walk to `parse_qualification_result` and show it converting that same reasoning into a validated `QualificationResult` — or, on a deliberately broken input, into a `BLOCKED` result with the error preserved. That's the whole gap this class closes.
