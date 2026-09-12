# Class 7 — MCP and Evidence-Backed Research

**Manuscript source:** Book 1, Chapter 8
**Seven-Step mapping:** Primary: Design Agent Capabilities / Supporting: Build Context, Evaluate & Govern
**Starting checkpoint:** [`../class-06/golden-solution/`](../class-06/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 60 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:10–0:20 | Talking points on Class 6 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference: research pipeline, `ResearchBrief`, Research Agent, `KNOWN_FAILURE_CASES.md` |
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

Expected: 60 tests pass offline (including the deliberate conflicting-sources and injection-attempt tests); 3 live-model tests skip without credentials.

## Facilitator checklist

- [ ] Run `build_research_brief` for `acme-001` live and show the conflict object on screen — both values, both sources
- [ ] Print the injection-attempt evidence item and walk through exactly why it's safe: it's data in a field, never code, never an instruction
- [ ] Be explicit that the research source is a local mock — name this honestly rather than letting the room assume it's a real web search
