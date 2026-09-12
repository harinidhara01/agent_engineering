# Class 8 — Common Mistakes to Discuss (0:10–0:20)

Reviewing Class 7's homework before revealing `golden-solution/`.

## In the undetected-conflict diagnostic

- **"Documented" used as a substitute for a real decision.** The diagnostic explicitly allowed either fixing the gap or documenting it — watch for submissions that pick "document" as an easy exit without actually engaging with whether it's the right call for this specific gap.

## In the freshness-check extension

- **A flag that never changes behavior.** A staleness flag that gets set but that nothing downstream reads is the same failure pattern flagged after Class 2 — recurring because it's a genuinely easy trap, not because anyone's being careless.

## In the "research remains read-only" constraint

- **A stray draft-outreach function appearing early, "to save time later."** Some participants, excited by the research pipeline, start sketching an outreach drafter in Class 7's homework. Redirect firmly — that's this week's actual lesson, and building it early skips the state-machine discipline that makes it safe.

## Talking points to set up today's class

- Ask: "We now have a Research Agent and a Qualification Agent. What decides which one runs first, and what happens between them?" — the honest answer right now is "nothing does," and that's exactly the gap.
- Preview the send-tool grep before doing it: ask the room to predict what the grep will find. The predicted answer ("nothing") landing correctly is worth pausing on.

## Golden solution reveal

Walk `class-07/`'s `ResearchBrief` output one more time, then ask: "If I asked you to hand this brief to the qualification agent and only proceed to a draft if a specific reviewer approved specific claims, could you point to the code that enforces that today?" There isn't any yet — that's the whole class.
