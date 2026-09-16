# Configuration

Empty at this checkpoint. This directory exists now, ahead of having anything to put in it, so the repository's shape doesn't change later — only its contents do.

Starting Class 2 (Book 1, Chapter 3), this directory holds WidgetWare's business configuration as data, not prose: `products.yaml`, `icp.yaml`, and `policies.yaml`. The reasoning is Book 1 §3.4's — stable business rules belong in explicit configuration that both a person and a test can read, not buried in a prompt string somewhere in `src/`.

## What belongs here (starting Class 2)

- Ideal-customer-profile thresholds and criteria.
- Product and offering definitions.
- Evidence and approval policy.

## What must never belong here

- Credentials, API keys, or tokens of any kind. Those belong in `.env` (never committed) or a managed secret store in a real deployment — never in a YAML file that gets checked into version control.
- Anything that changes per environment (a project ID, a model endpoint). That's `.env.example` territory, documented but not filled in.
