# Engineering Rules

Always-on rules for any coding agent (Antigravity or otherwise) working in this repository.

## Non-negotiable

- Use clear, conventional Python. Prefer explicit types and small functions over clever ones.
- Every function in `src/` has a type annotation on its signature and return value.
- Write or update a test with every behavior change. No behavior change ships untested.
- Do not add a dependency without stating, in the same task, why the standard library or an existing dependency is insufficient.
- Do not implement outbound message sending, CRM writes, or any external network call in this codebase. That boundary does not move because a task seems to need it — it means the task is scoped wrong for this stage of the course.
- Do not add a Gemini model call or an ADK agent at this checkpoint. That capability belongs to a later class; adding it early defeats the point of this one.
- Update documentation (`README.md`, `SPEC.md`, this rules file) when the behavior or commands they describe change. Stale docs are a defect, not a low-priority cleanup.
- Do not claim a task is complete without returning verification evidence — the actual output of `./scripts/check.sh`, not a description of what it would probably show.

## Preferred conventions

- Business policy belongs in `config/` as data, once `config/` starts being populated (Class 2 / Book 1, Chapter 3) — not as a string constant buried in application code.
- Prefer a failing test that names the gap over a comment that describes it.
- When a generated plan does more than the stated objective, trim it before implementation, not after.
