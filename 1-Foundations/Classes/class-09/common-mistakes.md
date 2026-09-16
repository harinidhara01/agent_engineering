# Class 9 — Common Mistakes to Discuss (0:00–0:20)

Reviewing Class 8's homework before revealing `golden-solution/`.

## In the required build (workflow state machine)

- **State machine tests that only exercise the happy path.** A submission with a passing test for RECEIVED → ... → APPROVED but no test asserting an illegal transition (e.g., RECEIVED directly to APPROVED) actually raises `IllegalTransitionError` hasn't proven the state machine enforces anything — it's proven the correct path is possible, which was never in doubt.

## In the approval boundary

- **Approval logic duplicated in more than one place.** Watch for a check like "has this been approved?" implemented once in the coordinator and again, slightly differently, in a test helper or the drafting agent. Two copies of a security-relevant check are two chances for them to silently disagree.

## Talking points to set up today's class

- Ask: "We just watched the full workflow run correctly for one account. How do you know it'll still work after the next code change, for the hundred accounts nobody's going to watch by hand?" — most will land on "you'd need to test it automatically," without yet being able to describe what that looks like at a system level. Today gives it a name and a shape.
- Preview the golden-dataset idea before revealing it: ask what a "representative" set of test accounts would need to include, beyond just "one that qualifies and one that doesn't." Push toward the harder cases this course has already demonstrated break things — conflicting evidence, injection attempts.

## Golden solution reveal

Run Class 8's full workflow live for the Acme account, end to end, and let the room watch it succeed. Then ask: "I could run this by hand for every account WidgetWare has. Should I?" Walk through why that doesn't scale, and why a golden dataset plus a release gate is what actually does. That's the whole gap this class closes.
