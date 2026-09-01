# Home Service Concierge — Setup Instructions

## 1. Project Objective

Build a web application called **Home Service Concierge**.

The application allows a customer to submit a home-service request and receive provider recommendations.

Version 1 supports:

* Plumbing
* HVAC
* Electrical

The application must demonstrate both:

1. Sequential agent pipeline
2. Parallel agent fan-out/gather architecture

The application should use mock provider data for Version 1.

---

# 2. Required Technology Stack

Use the following technology stack unless there is a strong technical reason that prevents implementation.

### Backend

* Python **3.11**
* **Flask**
* Jinja2 templates
* Python standard library wherever practical

### Frontend

Use:

* HTML5
* CSS3
* Vanilla JavaScript

Do not introduce React, Vue, Angular, or another frontend framework for Version 1.

### Testing

Use:

* pytest

### Configuration

Use:

* `.env` for environment-specific configuration
* `.env.example` as a template
* Never commit real secrets

### Data

Use local JSON/mock data for Version 1.

Do not introduce a database unless explicitly requested.

---

# 3. Python Environment

The project must use a Python virtual environment named:

```text
.venv
```

Create the environment using Python 3.11.

The project must not rely on globally installed Python packages.

All Python dependencies must be declared in:

```text
requirements.txt
```

The application should be runnable after:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, provide the equivalent activation command where appropriate.

---

# 4. Required Dependencies

At minimum, use:

```text
Flask
python-dotenv
pytest
```

Add other dependencies only when they are actually required.

Do not add unnecessary packages.

Pin dependency versions where appropriate for reproducibility.

---

# 5. Environment Configuration

Create:

```text
.env.example
```

The file should contain placeholders for configuration values that may be needed.

Example:

```text
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=change-me
```

Do not place real credentials or API keys in source code.

If an LLM provider is introduced later, its API key must be read from an environment variable.

---

# 6. Application Structure

Create a clean modular structure similar to:

```text
home-service-concierge/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── intake_agent.py
│   │   ├── classification_agent.py
│   │   ├── requirements_agent.py
│   │   ├── service_request_agent.py
│   │   ├── provider_agent.py
│   │   ├── aggregator_agent.py
│   │   ├── ranking_agent.py
│   │   └── booking_agent.py
│   │
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── sequential_pipeline.py
│   │   └── parallel_provider_workflow.py
│   │
│   ├── services/
│   │   └── booking_service.py
│   │
│   ├── data/
│   │   └── providers.json
│   │
│   └── models/
│       └── ...
│
├── references/
│   ├── plumbing.md
│   ├── hvac.md
│   ├── electrical.md
│   ├── provider_rules.md
│   └── response_examples.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── processing.html
│   ├── recommendations.html
│   └── confirmation.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── tests/
│   ├── test_agents.py
│   ├── test_sequential_pipeline.py
│   ├── test_parallel_workflow.py
│   ├── test_ranking.py
│   └── test_booking.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── SKILL.md
├── SETUP.md
└── README.md
```

The exact structure may be adjusted if necessary, but maintain clear separation between:

* Flask application
* agents
* workflows
* services
* data
* references
* templates
* static assets
* tests

---

# 7. Flask Application

Create a Flask application that can be started in development mode.

Provide a clear entry point.

The application should support:

```bash
flask --app app run --debug
```

or an equivalent documented command.

The README must explain exactly how to start the application.

---

# 8. Application Routes

Implement routes appropriate for the user workflow.

At minimum:

```text
GET  /
POST /request
GET  /processing
GET  /recommendations
POST /book
GET  /confirmation/<booking_id>
```

The exact routing design may be adjusted if the implementation benefits from a different structure.

---

# 9. Sequential Agent Architecture

Implement the following workflow:

```text
Customer Request
       ↓
Intake Agent
       ↓
Classification Agent
       ↓
Requirements Agent
       ↓
Service Request Agent
```

The implementation must make the sequential nature explicit.

Each agent receives the output from the previous agent.

Do not simply call all agents independently and label the workflow "sequential."

---

# 10. Parallel Agent Architecture

After a valid service request has been created, evaluate multiple providers concurrently.

Use a Python concurrency mechanism appropriate for this application, such as:

* `concurrent.futures`
* `asyncio`

Choose the simplest reliable approach.

The architecture must demonstrate genuine fan-out/gather behavior:

```text
              Service Request
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Provider A   Provider B   Provider C
        │            │            │
        └────────────┼────────────┘
                     ↓
                Aggregator
                     ↓
                  Ranking
```

Provider evaluations must be independent.

The workflow must gather the completed provider results before ranking.

---

# 11. Mock Provider Data

Create a JSON provider dataset containing enough records to demonstrate the workflow.

Include providers for:

* Plumbing
* HVAC
* Electrical

Include variation in:

* service type
* availability
* rating
* price
* distance
* specialties
* service area

Include cases where:

* provider matches
* provider does not match
* provider is unavailable
* provider has missing optional information

Do not use real personal information.

---

# 12. Agent Implementation

Each agent must have one clearly defined responsibility.

Do not create a single large agent that performs the entire workflow.

Use structured Python objects/dictionaries for agent-to-agent communication.

The implementation should make it easy to inspect:

```text
Input → Agent → Output
```

for every stage.

---

# 13. Reference Files

The following files will be provided:

```text
references/
├── plumbing.md
├── hvac.md
├── electrical.md
├── provider_rules.md
└── response_examples.md
```

These are authoritative reference files.

They are **read-only**.

Do not modify them during implementation or application execution.

Use them to guide:

* service classification
* service requirements
* provider eligibility
* ranking
* customer-facing response style

---

# 14. UI Requirements

Build a clean, simple Flask/Jinja web interface.

Do not over-engineer the UI.

### Request page

Include:

* problem description
* service category
* location
* preferred date
* preferred time
* submit button

### Processing page

Show the workflow progress.

Clearly distinguish:

**Sequential processing**

from:

**Parallel provider evaluation**

For example:

```text
✓ Understanding request
✓ Classifying service
✓ Checking requirements
✓ Preparing service request

Provider evaluation

✓ Provider A
✓ Provider B
✓ Provider C

✓ Comparing providers
```

### Recommendation page

Show provider cards containing available information:

* provider name
* rating
* price
* distance
* availability
* service
* recommendation reason

Include a booking button.

### Confirmation page

Show:

* provider
* service
* appointment
* location
* confirmation ID
* booking status

---

# 15. Error Handling

Handle:

* missing required information
* unsupported service
* no eligible providers
* provider-agent failure
* all provider-agent failures
* booking failure

Never fabricate:

* providers
* prices
* ratings
* availability
* booking confirmations

---

# 16. Testing

Use pytest.

Tests must cover:

### Agents

* intake
* classification
* requirements
* service request
* provider evaluation
* aggregation
* ranking
* booking

### Sequential workflow

Verify that:

```text
Intake
→ Classification
→ Requirements
→ Service Request
```

executes in the correct order.

### Parallel workflow

Verify:

* multiple providers are evaluated
* results are gathered
* one provider failure does not necessarily fail the entire workflow
* aggregation works
* ranking receives aggregated results

### Booking

Verify:

* valid provider can be booked
* invalid provider cannot be booked
* unavailable provider cannot be booked
* failed booking does not produce a false confirmation

---

# 17. README

Create a README containing:

1. Project overview
2. Technology stack
3. Python version
4. Installation instructions
5. Virtual environment setup
6. Dependency installation
7. Environment configuration
8. How to run Flask
9. How to run tests
10. Project architecture
11. Sequential workflow
12. Parallel workflow

---

# 18. Git and Generated Files

Create an appropriate `.gitignore`.

At minimum, ignore:

```text
.venv/
__pycache__/
.pytest_cache/
.env
*.pyc
```

Do not commit:

* virtual environment
* `.env`
* secrets
* generated temporary files

---

# 19. Development Behavior

Before writing code:

1. Read `SKILL.md`.
2. Read all reference files.
3. Inspect the complete project structure.
4. Plan the implementation.
5. Implement incrementally.
6. Run tests.
7. Review the final diff.

Follow the minimal-change and style-preservation rules in `SKILL.md`.

Reference files must remain unchanged.

---

# 20. Definition of Done

The application is complete only when:

* Python 3.11 is supported.
* Flask application starts successfully.
* Dependencies are documented.
* Virtual environment setup is documented.
* `.env.example` exists.
* The request workflow works.
* Sequential agent pipeline works.
* Parallel provider evaluation works.
* Aggregation works.
* Ranking works.
* Booking works using mock data.
* UI works end-to-end.
* Error cases are handled.
* Tests pass.
* Reference files remain unchanged.
* README contains complete setup and run instructions.


# UI/UX Requirements

## Design Goal

Create a modern, clean, professional service-booking interface.

The application should feel like a real consumer service product rather than a technical AI demonstration.

The UI must be responsive and usable on both desktop and mobile screens.

---

## Frontend Technology

Use:

* HTML5
* CSS3
* Vanilla JavaScript
* Flask/Jinja templates

Do not use React, Vue, Angular, or another frontend framework.

Avoid unnecessary frontend dependencies.

---

## Visual Style

Use a clean and trustworthy visual design.

The interface should have:

* clear typography
* generous spacing
* readable form controls
* consistent buttons
* cards for provider information
* clear visual hierarchy
* responsive layouts
* accessible contrast
* clear success and error states

Do not make the UI overly technical.

Do not expose internal Python implementation details to customers.

---

## Screen 1 — Service Request

Create a landing/request page containing:

* Application name: Home Service Concierge
* Short description
* Problem description textarea
* Service category
* Location
* Preferred date
* Preferred time range
* Submit button

The problem description should be the primary input.

Allow the customer to describe the problem naturally.

Example:

> My AC is running but the house isn't getting cold.

---

## Screen 2 — Processing

Display a workflow-progress interface while the request is being processed.

Show sequential processing as completed steps:

```text
✓ Understanding your request
✓ Identifying service
✓ Checking requirements
✓ Preparing service request
```

Then display provider evaluation:

```text
Finding providers

✓ Provider A
✓ Provider B
✓ Provider C
✓ Provider D
```

The UI should visually communicate that provider evaluation is a parallel stage.

Do not expose internal code, function names, stack traces, or implementation details.

---

## Screen 3 — Recommendations

Display eligible providers as visually distinct cards.

Each card may contain:

* Provider name
* Service
* Rating
* Estimated price
* Distance
* Availability
* Specialty
* Recommendation explanation

Clearly identify the highest-ranked recommendation.

Provide:

**Book Service**

for eligible available providers.

Do not display information that is not present in the provider data.

---

## Screen 4 — Booking Confirmation

Before creating a booking, show:

* Provider
* Service
* Date
* Time
* Location
* Estimated price

Provide:

**Confirm Booking**

and:

**Go Back**

---

## Screen 5 — Booking Success

After successful booking, display:

* Success indicator
* Provider
* Service
* Appointment date
* Appointment time
* Location
* Confirmation ID

Example:

```text
Service Booked!

ABC HVAC Services

AC Repair
September 1, 2026
6:00 PM
Columbus, OH

Confirmation: BKG-001
```

Only display a successful booking state after the booking operation succeeds.

---

## Error States

Provide clear user-friendly error states for:

* missing information
* unsupported service
* no matching providers
* provider evaluation failure
* booking failure

Do not display raw exceptions or stack traces to the customer.

---

## Responsive Design

The application must work on:

* desktop
* tablet
* mobile

Provider cards should stack vertically on smaller screens.

Forms should remain usable without horizontal scrolling.

---

## UI and Agent Separation

The UI should present the service workflow in simple customer-friendly language.

The internal agent architecture must remain separate from the presentation layer.

The UI may visualize workflow progress, but should not expose:

* agent implementation details
* internal prompts
* internal reasoning
* stack traces
* raw model responses
* internal data structures

---

## Accessibility

Use:

* semantic HTML
* labels for form controls
* keyboard-accessible controls
* appropriate button states
* readable text
* clear error messages

Do not rely solely on color to communicate status.

---

## UI Completion Criteria

The UI is complete when a user can:

1. Submit a service request.
2. See processing progress.
3. View provider recommendations.
4. Select a provider.
5. Review booking details.
6. Confirm the booking.
7. See the booking confirmation.
8. Understand errors when something fails.

The UI should feel like one coherent application rather than separate technical screens.
