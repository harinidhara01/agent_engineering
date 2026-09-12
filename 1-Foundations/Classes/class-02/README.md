# Class 2 — Gemini Context and Instruction Architecture

**Manuscript source:** Book 1, Chapter 3
**Seven-Step mapping:** Primary: Build Context / Supporting: Frame the Use Case, Evaluate & Govern
**Starting checkpoint:** [`../class-01/golden-solution/`](../class-01/golden-solution/)
**This class's golden solution:** [`golden-solution/`](golden-solution/) — verified runnable (`pytest`: 8 passed)

## In this folder

| File | Used during | Purpose |
| --- | --- | --- |
| [`lesson-plan.md`](lesson-plan.md) | reference | Full narrative lesson plan: cadence, rationale, and section-by-section detail |
| [`common-mistakes.md`](common-mistakes.md) | 0:10–0:20 | Talking points on Class 1 homework's recurring issues |
| [`slides.md`](slides.md) | 0:30–0:55 | 12-slide deck with full speaking notes |
| [`kahoot.md`](kahoot.md) | 0:55–1:05 | 8 quiz questions, Kahoot-ready, with answer key |
| [`golden-solution/`](golden-solution/) | 0:20–0:30 reveal and 1:50–1:57 comparison | Runnable reference: `config/*.yaml`, `instructions.py`, `context_builder.py`, 5 context tests, fixtures, `KNOWN_FAILURE_CASES.md` |
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

Expected: `ruff format --check`, `ruff check`, and `pytest` (8 tests: 3 health-check + 5 context) all pass.

To see the assembled context directly:

```bash
python3 -c "
from widgetware_sdr.context_builder import build_context
ctx = build_context({'account_id': 'acme-001', 'company_name': 'Acme Manufacturing', 'industry': 'manufacturing', 'employee_count': 22000, 'region': 'united_states'})
print(ctx.assembled_prompt)
"
```

## Facilitator checklist

- [ ] Build the malicious-note test live and let it fail first if you deliberately skip the delimiting step, so participants see the failure mode before the fix
- [ ] Print an assembled context on screen at least once and read it end to end — the class's own acceptance criterion is that it stays inspectable at a glance
- [ ] Be explicit that today's injection "resistance" is structural (no model call exists yet), not a claim about real model behavior — that gets tested for real starting Class 3
