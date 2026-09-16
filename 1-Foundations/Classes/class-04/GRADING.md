# Class 4 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check offline.

1. **The Skill's procedure is a real procedure, not generic advice.** "Consider the evidence carefully and make a good judgment" is not a procedure — it's a restatement of the goal. A strong `skill.md` has ordered, checkable steps (check exclusions first, then thresholds, then pain signals) that two different people would apply the same way.

2. **The agent's Python file contains no qualification logic.** If `qualification_agent.py` has an `if industry == "financial_services": return "DO_NOT_QUALIFY"` anywhere, the Skill split didn't actually happen — it just moved a copy of the reasoning into two places. Grep for any conditional referencing ICP field names inside the agent file; there should be none.

3. **The instruction-construction test is testing the right thing.** A submission's `test_instruction_contains_no_specific_account_data` (or equivalent) should check for account-specific values (a company name, a specific employee count), not just the string "account" — a test that only checks the word "account" doesn't appear would pass even if a real account's data leaked in under a different label.

4. **The evidence-classification examples show real judgment, not just the five category names repeated.** A strong Skill's examples include at least one genuinely debatable case (like the ambiguous "modernization initiatives" note) with reasoning for why it landed where it did — not five trivially obvious one-liners.

5. **If integration tests exist but weren't run, that's stated honestly.** A submission that includes `tests/integration/` but never actually ran them (no credentials, or simply skipped) should say so in its README or homework note — silently presenting untested code as if it were verified is a real defect this class's own `KNOWN_FAILURE_CASES.md` #1 exists to prevent.

6. **Independent understanding, not a copy.** If the submission's `skill.md`, `qualification_agent.py`, and `app.py` are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
