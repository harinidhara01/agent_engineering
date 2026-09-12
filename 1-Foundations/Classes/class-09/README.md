# Class 9 — Evaluation and the Release Gate

**Manuscript source:** Book 1, Chapter 10
**Seven-Step mapping:** Primary: Evaluate & Govern / Supporting: Orchestrate Workflows
**Starting checkpoint:** [`../class-08/golden-solution/`](../class-08/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 109 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:00–0:20 | Talking points on Class 8 homework's recurring issues |
| [`slides.md`](slides.md) | 0:20–0:45 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:45–0:55 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:10–0:20 reveal and 1:50–1:57 comparison | Runnable reference: golden dataset, metrics, release gate, `KNOWN_FAILURE_CASES.md` |
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

Expected: 109 tests pass offline; 3 live-model tests in `tests/integration/` skip automatically unless `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT` is set.

## Facilitator checklist

- [ ] Run Class 8's full workflow live for one account, then ask how the room would know it still works after the next code change, for accounts nobody watched by hand — sets up the whole class
- [ ] Deliberately break one business rule live and show the release gate catching it and naming the specific failing category
- [ ] Point out `approval_compliance_rate()`'s documented limitation (only four states recognized) as an honest, deliberate gap — not a bug — that Class 10 will need to close
