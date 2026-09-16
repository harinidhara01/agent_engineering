# Class 6 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check partially.

1. **Tool descriptions would actually work on a model that's never seen the code.** Read each tool's docstring as if you were an LLM deciding whether to call it. Does it say when to use it *and* when not to? A description that only states what the function returns, with no usage guidance, is weaker than Book 1 §7.2 asks for.

2. **`calculate_fit_score` is not reachable by the model.** Check the agent's `tools=[...]` list — `calculate_fit_score` should not be in it. If it is, the submission has undone the chapter's own point about keeping deterministic calculation outside model reasoning.

3. **Tool tests are genuinely independent of the agent.** A strong submission's tool tests never construct an `Agent` or make a model call — they call the tool function directly. A test that goes through the agent to exercise a tool has conflated two different kinds of bugs (reasoning vs. implementation) that this chapter deliberately keeps separate.

4. **Missing-record and invalid-input handling return typed errors, not exceptions or silent defaults.** Grep for any bare `raise` inside a tool function, or any place a missing record silently returns a plausible-looking default instead of an explicit error. Both undermine the fail-safe principle Class 5 established at the contract layer.

5. **The honesty about untested tool-failure categories is present, not glossed over.** A strong submission's own `KNOWN_FAILURE_CASES.md` (or equivalent) says plainly that dependency failure, permission failure, and redaction aren't tested because they don't apply yet — not that they're "covered" by the existing valid/invalid/missing tests, which is a different claim.

6. **Independent understanding, not a copy.** If the submission's tools and their tests are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
