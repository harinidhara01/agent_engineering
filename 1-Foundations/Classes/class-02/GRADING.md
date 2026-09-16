# Class 2 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check.

1. **System instructions are genuinely fixed, not fixed-looking.** `instructions.py`'s `SYSTEM_INSTRUCTIONS` should be a constant with no string formatting, f-string interpolation, or concatenation involving account data, notes, or config values anywhere near it. A submission that builds the "system instructions" by starting from the constant and appending account-derived text has reintroduced exactly the failure mode this chapter exists to prevent, even if the malicious-note test happens to still pass.

2. **The malicious-note test checks position, not just presence.** A test that only asserts the injected text appears somewhere in the assembled prompt is weaker than one that asserts it appears strictly after the evidence marker and nowhere before it. If the submission's test only checks presence, that's a partial-met on this chapter's central safety claim, regardless of whether the test is green.

3. **Business configuration is genuinely used, not restated as prose elsewhere.** The ICP thresholds, excluded industries, and evidence categories should exist in exactly one place — the YAML files — and `context_builder.py` should read them, not hardcode a second copy for convenience. Check for a stray `if industry == "manufacturing"` type hardcoded rule sitting next to `config/icp.yaml`'s equivalent value.

4. **The assembled prompt is actually readable, not merely well-structured in code.** Ask the submitter to show you a printed `assembled_prompt` for one scenario. If it's excessively verbose, duplicates information across sections, or would be hard for a person to sanity-check by eye, that's a real defect against Book 1 §3's own evaluation criterion ("is the context compact enough to inspect manually?") — even though nothing in the test suite measures verbosity directly.

5. **The submission is honest about what this checkpoint does and doesn't prove.** A strong submission (in a README note, a comment, or just in conversation) recognizes that "the malicious note can't override system instructions" is a structural claim about *this code*, not yet a claim about how a real Gemini call would actually behave — that's untestable until Class 3. A submission that overclaims ("this defeats prompt injection") has missed the chapter's own distinction between architectural guarantees and model behavior.

6. **Independent understanding, not a copy.** If the submission's YAML files, `instructions.py`, and `context_builder.py` are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
