# Class 01 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check structurally. Passing `./scripts/check.sh` is necessary but not sufficient; the deterministic gate and this qualitative review are separate, and both matter.

## Deterministic gate (recap — not the subject of this file)

`verify_environment.py` passes; `ruff format --check`, `ruff check`, and `mypy` pass; all `pytest` tests pass; required files exist; no secrets or prohibited capabilities are present. If any of this fails, stop here — there's nothing to qualitatively grade yet.

## Qualitative review

1. **The business objective is a real decision, not a restated brief.** `SPEC.md`'s objective sentence should read like something a stakeholder could be held to, not a paraphrase of the WidgetWare product description. A submission that just repeats "help manufacturing companies modernize" without naming what the *system* is responsible for hasn't yet separated the business pitch from the system's job.

2. **Acceptance criteria Section A is testable, not merely testable-sounding — and Section B is honestly labeled as not-yet-implemented.** "The repository is well organized" reads like a criterion but isn't one. A passing submission names a specific, inspectable signal for every Section A criterion, and never lets a Section B (future-product) criterion get evaluated as if this checkpoint already satisfies it.

3. **The three scenarios are structurally distinct, not cosmetically distinct.** A "disqualifying" and an "ambiguous" scenario that differ only in company name and both obviously fail the same way haven't exercised the boundary between `NOT_QUALIFIED` and `NEEDS_RESEARCH`. The ambiguous scenario specifically should be missing exactly one decisive fact.

4. **The architecture decision records explain reasoning, not just outcomes.** An ADR that states "we decided X" without stating what else was considered and why it lost isn't a decision record — it's a decision announcement. Ask the submitter to defend one alternative they rejected.

5. **The `.agents/` rules are concrete enough to actually change what a coding agent does.** "Write good code" is not a rule an agent can act on. "Every function in `src/` has a type annotation" is. Check whether the rules would have caught a real mistake if they'd existed before that mistake happened.

6. **The out-of-scope reasoning shows understanding of *why*, not just *what*.** A submission that lists the same prohibitions from the chapter without any sign the author understands why *this* system, at *this* trust level, draws the line here — versus a system that's already earned more autonomy — is pattern-matching, not reasoning.

7. **The harness is genuinely reproducible, not just working on the author's machine.** Clone the submission fresh (or ask the submitter to describe doing so) and run `./scripts/check.sh`. A submission that only works after an undocumented local fix has a real defect, not a minor one — this is precisely what a "known-good baseline" claims not to have.

8. **Independent understanding, not a copy.** If the submission's `SPEC.md`, business brief, architecture docs, and repository structure are near-identical to the gold reference in wording and structure with no evidence of independent construction — different company names chosen for scenarios, an ADR reasoned differently but equally rigorously — note that explicitly per the anti-gaming guidance in the generic template.
