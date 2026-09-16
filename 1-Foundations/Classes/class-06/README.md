# Class 6 — Tool Engineering

**Manuscript source:** Book 1, Chapter 7
**Seven-Step mapping:** Primary: Design Agent Capabilities / Supporting: Build the Harness, Evaluate & Govern
**Starting checkpoint:** [`../class-05/golden-solution/`](../class-05/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 44 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:00–0:20 | Talking points on Class 5 homework's recurring issues |
| [`slides.md`](slides.md) | 0:20–0:45 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:45–0:55 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:10–0:20 reveal and 1:50–1:57 comparison | Runnable reference: `tools/`, updated agent, `KNOWN_FAILURE_CASES.md` |
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

Expected: 44 tests pass offline (contracts, tools, agent construction, message rendering); 3 live-model tests skip without credentials.

## Facilitator checklist

- [ ] Run Class 5's agent live and print a valid `QualificationResult`, then ask where each fact actually came from — sets up the whole class
- [ ] Live-demo a tool call with a malformed argument and show it returns a typed error, never raises
- [ ] Confirm out loud that `calculate_fit_score()` is not in the agent's `tools=[...]` list — deterministic calculation stays outside model reasoning
