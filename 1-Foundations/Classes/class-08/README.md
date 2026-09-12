# Class 8 — Multi-Agent Workflow and Human Approval

**Manuscript source:** Book 1, Chapter 9
**Seven-Step mapping:** Primary: Orchestrate Workflows / Supporting: Design Agent Capabilities, Evaluate & Govern
**Starting checkpoint:** [`../class-07/golden-solution/`](../class-07/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 90 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:10–0:20 | Talking points on Class 7 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference: state machine, workflow coordinator, approval, two new agents, `KNOWN_FAILURE_CASES.md` |
| [`homework.md`](homework.md) | 1:57–2:00 | The three-level homework assignment |
| [`BUILD.md`](BUILD.md) | self-paced track | Step-by-step instructions to build this checkpoint yourself with Antigravity |
| [`GRADING.md`](GRADING.md) | self-paced track (or facilitator supplement) | Class-specific LLM-judge criteria |

## Running the golden solution

```bash
cd golden-solution
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expected: 90 tests pass offline (state machine, approval, contracts, all five required scenarios, checkpointing); 3 live-model tests skip without credentials.

## Facilitator checklist

- [ ] Run the full workflow live for `acme-001`, print `run.state` at each stage, and stop on `AWAITING_APPROVAL`
- [ ] Kill a run mid-workflow (or simulate it) and show the checkpoint file with prior stages intact
- [ ] Run `grep -ri "send\|smtp" src/` live and confirm, with the class watching, that it returns nothing
