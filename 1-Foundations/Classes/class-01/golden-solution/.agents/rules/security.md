# Security Rules

Always-on rules for any coding agent working in this repository. See `../../SECURITY.md` for the full policy; this file is the short version an agent should hold in context on every task.

## Non-negotiable

- Never place a real credential, API key, token, or project identifier in source code, configuration, tests, fixtures, or documentation. `.env.example` gets a placeholder; `.env` (never committed) gets the real value, locally, on the developer's own machine.
- Never widen a tool's or a script's permissions beyond what the current task actually requires. If a generated plan requests broader file, network, or command access than the stated objective needs, flag it before implementation, not after.
- Never add a send-capable function, an outbound API client, or any code path that could transmit data outside this repository's own process. This checkpoint's security model relies on that capability not existing in code — not on a runtime check catching it.
- Never commit `.env`, `__pycache__/`, `.venv/`, or any other generated artifact. `.gitignore` names them; treat an accidental `git add` of one of them as a defect to fix, not a formatting nit.

## Before accepting any agent-generated diff

- Read it. A diff that "probably looks fine" is not the same as a reviewed diff.
- Check specifically for: a new dependency you didn't ask for, a broadened permission, a hardcoded value that should have come from configuration or environment, and any string that resembles a real credential.
