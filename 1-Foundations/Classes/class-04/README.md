# Class 4 — Skills and Reusable Agent Capabilities

**Manuscript source:** Book 1, Chapter 5
**Seven-Step mapping:** Primary: Design Agent Capabilities / Supporting: Build Context, Build the Harness, Evaluate & Govern
**Starting checkpoint:** [`../class-03/golden-solution/`](../class-03/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 17 passed, 3 skipped without live credentials)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan |
| [`common-mistakes.md`](common-mistakes.md) | 0:00–0:30 | Talking points on Class 3 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference: real ADK `Agent` refactored onto Skills, `skills/`, `skills.py`, `KNOWN_FAILURE_CASES.md` |
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

Expected: 17 tests pass offline; 3 live-model tests in `tests/integration/` skip automatically unless `GOOGLE_API_KEY` or `GOOGLE_CLOUD_PROJECT` is set.

## Facilitator checklist

- [ ] Run `class-03/`'s agent live first, then ask "if a second agent needed this exact reasoning, what would you have to do right now?" — sets up the whole class
- [ ] Show the assembled instruction before and after the refactor, side by side, so the room sees the Skill's text arriving via `load_skill()` rather than being retyped
- [ ] Make the Skill-vs-agent-code distinction concrete: fix the Diagnostic homework bug by editing only `skill.md`, live, and show the agent's behavior change without touching Python
- [ ] Confirm out loud that the agent's result is still prose, not structured output — that's Class 5, deliberately
