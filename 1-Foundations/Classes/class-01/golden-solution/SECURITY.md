# Security

## Reporting

This is a teaching checkpoint, not a production system with a live attack surface. If you find a real security issue in the course infrastructure itself (not in the intentionally-illustrative WidgetWare scenarios), open an issue against the course repository.

## What this checkpoint actually protects against

At this stage there is no model call, no network access, no external tool, and no credential that does anything real. The security posture here is about habits that must already be in place before any of that exists — not about defending a live system yet.

## Secrets

- Real credentials, tokens, project IDs, and API keys never appear in source, configuration, fixtures, tests, or committed documentation — only in a local, uncommitted `.env`.
- `.env.example` documents every variable name a future class will read, with an obviously fake placeholder value, never a real one.
- `.gitignore` excludes `.env` from the very first commit, before there is anything real to leak. See `docs/architecture-decisions/0003-repository-harness.md` for why this is a Class 1 concern and not deferred to whichever class first needs a real secret.

## Permissions

- A development agent (Antigravity, or any coding assistant) operating on this repository should be treated as a capable collaborator, not an unquestioned authority. Review its plan before permitting implementation; review its diff before accepting.
- No task given to a development agent in this checkpoint requires production credentials, cloud IAM roles, or access to real customer data. If a future task seems to require one, that is a signal to stop and re-scope, not to grant it.

## What this checkpoint deliberately cannot do (by absence, not by policy)

- No outbound message of any kind — the capability does not exist in code, so there is nothing to authorize or misconfigure.
- No CRM write, no external API call, no live account research.

A capability that does not exist cannot be misused. Where possible, this course prefers that guarantee over a policy check that could theoretically be bypassed.

## Reporting a real vulnerability in the course tooling

Open an issue at the repository's issue tracker with reproduction steps. Do not include real credentials or personal data in the report.
