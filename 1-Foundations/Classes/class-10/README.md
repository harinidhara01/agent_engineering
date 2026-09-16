# Class 10 — Loop Engineering with ADK

**Manuscript source:** Book 1, Chapter 11
**Seven-Step mapping:** Primary: Engineer Loops / Supporting: Orchestrate Workflows, Evaluate & Govern
**Starting checkpoint:** [`../class-09/golden-solution/`](../class-09/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 140 passed, 3 skipped without live credentials)

This class closes Book 1. The single-account workflow this loop wraps is unchanged from Class 9 — evaluate first, automate second.

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:00–0:20 | Talking points on Class 9 homework's recurring issues |
| [`slides.md`](slides.md) | 0:20–0:45 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:45–0:55 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:10–0:20 reveal and 1:50–1:57 comparison | Runnable reference: extended state machine, full batch loop, `KNOWN_FAILURE_CASES.md` |
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

Expected: 140 tests pass offline; 3 live-model tests in `tests/integration/` skip automatically unless `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT` is set. Watch for a `LoopAgent` deprecation warning from `google-adk` — it's real, and `KNOWN_FAILURE_CASES.md` documents it honestly rather than suppressing it.

## Facilitator checklist

- [ ] Run Class 9's release gate live against the Class 9 checkpoint and watch it pass, then ask what happens the moment WidgetWare hands over a hundred accounts unattended — sets up the whole class
- [ ] Live-demo a mid-batch restart and show the loop resuming from durable session state instead of reprocessing a settled account
- [ ] Make §11.10 concrete: confirm out loud that an account processed inside an unattended batch gets exactly the same approval scrutiny as one processed live
- [ ] Close Book 1 explicitly — name what this system still can't do (multi-user, long-term memory, planning over ambiguous goals, collaborating with agents it doesn't own) as the on-ramp to Book 2
