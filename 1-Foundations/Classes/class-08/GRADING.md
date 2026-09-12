# Class 6 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check with stubs.

1. **The state machine was designed before the agents, not after.** Ask the submitter to walk through the transition table without looking at `coordinator.py`. If they can explain every legal and illegal transition from the table alone, §9.3's actual point landed. If they can only explain it by tracing through `run_workflow()`'s code, the state machine is documentation of what the code happens to do, not a design that constrains it.

2. **The Drafting Agent's isolation is structural, not just instructed.** Check what `run_workflow()` actually passes to `draft()` — it should be the `EvidenceReview`'s approved claims, or an equivalent narrow projection, not the full `ResearchBrief` or `QualificationResult`. An instruction telling the model to "only use approved claims" is weaker than an input that structurally excludes everything else.

3. **Partial-failure tests actually assert on preserved state, not just the final status.** A test that only checks `run.state == BLOCKED` after a mid-workflow failure hasn't verified §9.7's actual claim — that prior successful work isn't lost. It should also assert the earlier stage's result (e.g., `run.research_brief`) is still populated.

4. **The stub-vs-real distinction is stated honestly.** A strong submission's own documentation says plainly that the five scenario tests use stub `qualify`/`review`/`draft` functions, not the real agents — and doesn't imply the workflow has been proven correct with live model reasoning when it hasn't.

5. **`ApprovalPackage` is actually populated from the workflow's real state, not hand-typed placeholder strings.** If a submission's approval-package construction hardcodes `qualification_summary="looks good"` instead of deriving it from an actual `QualificationResult`, the contract exists but isn't wired to anything real yet.

6. **Independent understanding, not a copy.** If the submission's state machine, workflow, and agents are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
