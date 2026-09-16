# Building Class 4 with Antigravity

Goal: refactor the Account Qualification Assistant so its entire qualification procedure lives in a reusable Skill, not embedded in Python. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-04/`, then diff.

## Prerequisites

- **`../SETUP.md` complete**, including a way to actually call Gemini: `GOOGLE_API_KEY`, or `GOOGLE_CLOUD_PROJECT` + Vertex AI access. You can build and test most of this class without one (agent construction is fully offline), but you can't observe real reasoning without it.
- Your Class 3 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Write the Skill first, by hand, before touching the agent's Python. `skills/icp_qualification/skill.md` should contain: identity (name, version, owner, purpose), inputs, an ordered procedure (check exclusions first, compare thresholds, identify pain signals, identify missing evidence, distinguish fact from inference, select a provisional outcome, explain it), quality criteria, and a pointer to three worked examples. This procedure should be lifted directly out of Class 3's embedded string — same reasoning, new home. Write the three examples (`examples/qualified.md`, `unqualified.md`, `needs_research.md`) using the three fixture accounts already in the repo.

2. Write `src/widgetware_sdr/skills.py` yourself: a small, deterministic `load_skill(name: str) -> str` that reads `skills/<name>/skill.md` off disk and returns its text. No model call, no caching complexity — this is boring on purpose.

3. Ask Antigravity to refactor the existing agent, not rewrite it from scratch:

   > "Refactor `src/widgetware_sdr/agents/qualification_agent.py` so its instruction is assembled from `SYSTEM_INSTRUCTIONS`, the rendered ICP and escalation-rule config, and the full text of `skills/icp_qualification/skill.md`, loaded via `load_skill()` — not retyped as a Python string. Remove the embedded procedure constant entirely. The instruction must still never include any specific account's data."

4. Add the second Skill, `skills/evidence_classification/skill.md` — lightweight, five categories (verified fact / derived fact / inference / unknown / conflict), a handful of worked examples.

5. Update the offline tests: agent name and model unchanged, instruction contains the real ICP figures and the Skill's procedure text (not the old embedded string), instruction contains **no** specific account data, agent has no tools, and — specifically for this checkpoint — no qualification logic remains as a string literal anywhere in `qualification_agent.py`.

6. If you have credentials, re-run the three semantic scenario tests (qualified, unqualified, insufficient-evidence) against the refactored agent and confirm the reasoning is materially unchanged from Class 3's — only its source moved. If you don't have credentials, confirm the tests still exist and are correctly skip-guarded.

## Verify

```
cd my-work/gemini-book-1/class-04
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect offline tests to pass and integration tests to skip (without credentials) or pass (with them).

## Compare against the reference

`golden-solution/tests/unit/test_qualification_agent_construction.py` is the reference for what "constructs correctly" means here. Pay attention to the test confirming the instruction contains the Skill's loaded text, not a retyped copy — a submission that keeps a parallel embedded string "just in case" hasn't actually completed the extraction.

## Grade it

Passing construction tests doesn't prove the Skill's procedure is actually good, or that it's genuinely reusable outside this one agent. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
