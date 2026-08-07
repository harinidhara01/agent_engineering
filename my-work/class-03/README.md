# WidgetWare SDR Context Package — Class 3

This repository contains the deterministic, testable context package for the WidgetWare Sales Development Representative (SDR) domain. It forms the foundational context assembly engine for future AI agent automation.

## Project Structure

```text
.
├── README.md                          # Setup and overview documentation
├── SPEC.md                            # Class 3 technical specification
├── LAB.md                             # Class 3 lab guide
├── pyproject.toml                     # Python package and dependency configuration
├── .env.example                       # Environment secrets reference (none required)
├── config/
│   ├── products.yaml                  # WidgetWare product catalog & approved claims
│   ├── icp.yaml                       # Ideal Customer Profile criteria & thresholds
│   └── policies.yaml                  # Operating policies, safety boundaries, & evidence rules
├── docs/
│   ├── widgetware-business-brief.md   # Executive summary & domain context
│   └── acceptance-criteria.md         # Observable project verification criteria
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py                # Package declaration
│       ├── instructions.py            # Stable future-agent system instructions
│       └── context_builder.py         # Deterministic 5-layer context assembler
└── tests/
    ├── unit/
    │   ├── test_starter.py            # Baseline environment test
    │   └── test_context_builder.py    # Context builder, config, & scenario unit tests
    └── scenarios/
        ├── qualified_account.yaml     # Scenario 1: Qualified account fixture
        ├── unqualified_account.yaml   # Scenario 2: Unqualified account fixture
        ├── insufficient_evidence.yaml # Scenario 3: Missing information fixture
        └── prompt_injection.yaml      # Scenario 4: Untrusted override attempt fixture
```

## The Five Context Layers

The `context_builder.py` module assembles and enforces separation across five distinct layers:

1. **System Instructions** (`system_instructions`): Immutable, observable behavioral instructions that define agent role, evidence handling rules, stopping criteria, and safety prohibitions.
2. **Business Context** (`business_context`): Loaded from YAML files (`products.yaml`, `icp.yaml`, `policies.yaml`). Defines offerings, target customer parameters, evidence requirements, and human approval rules.
3. **Task Context** (`task_context`): Specific assignment data including target `account` details and task `objective`. All account notes and retrieved content are isolated here as untrusted input.
4. **Retrieved Evidence** (`retrieved_evidence`): Supplied evidence records preserving strict provenance (`claim`, `classification`, `source.name`, `source.url`, `source.retrieved_at`, `excerpt`).
5. **Workflow State** (`state`): Reserved execution state tracking (e.g., `current_step`, `approval_status`), defaulting to `{}` if unprovided.

## Setup & Running Tests

### 1. Installation

Install the package in editable mode with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

### 2. Run Tests

Run the full automated pytest suite:

```bash
python -m pytest -v
```

## Safety Boundaries & Scope

This package strictly provides structured, deterministic context assembly:
- **No Google ADK agent** is built.
- **No LLM or Gemini API** calls are made.
- **No external network calls** or live web scraping.
- **No emails or social messages** are sent.
- **No CRM records** are modified.
- **No database persistence** or deployment infrastructure is added.
