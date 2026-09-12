# Class 5 — Structured Outputs and Agent Contracts

**Manuscript source:** Book 1, Chapter 6
**Seven-Step mapping:** Primary: Evaluate & Govern / Supporting: Design Agent Capabilities, Build the Harness
**Starting checkpoint:** [`../class-04/golden-solution/`](../class-04/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 29 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:00–0:20 | Talking points on Class 4 homework's recurring issues |
| [`slides.md`](slides.md) | 0:20–0:45 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:45–0:55 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:10–0:20 reveal and 1:50–1:57 comparison | Runnable reference: `QualificationResult`/`EvidenceItem` contracts, fail-safe parsing pipeline, `KNOWN_FAILURE_CASES.md` |
| [`homework.md`](homework.md) | 1:57–2:00 | The three-level homework assignment |
| [`BUILD.md`](BUILD.md) | self-paced track | Step-by-step instructions to build this checkpoint yourself with Antigravity |
| [`GRADING.md`](GRADING.md) | self-paced track (or facilitator supplement) | Class-specific LLM-judge criteria, used with `../GRADING-RUBRIC-TEMPLATE.md` |

## Running the golden solution

```bash
cd golden-solution
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expected: 29 tests pass offline; 3 live-model tests in `tests/integration/` skip automatically unless `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT` is set.

## Facilitator checklist

- [ ] Run Class 4's agent live and print its raw prose response, then ask how the room would safely route on it in code today — sets up the whole class
- [ ] Live-demo `parse_qualification_result` against a deliberately malformed dict and show it returns `BLOCKED` with the error preserved, never a crash
- [ ] Confirm out loud that `qualification_agent.py` is untouched this class — this is a validation layer, not a rewiring
