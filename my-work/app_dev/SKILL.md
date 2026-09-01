# Home Service Concierge — Agent Skill

## 1. Purpose

This skill defines how the Home Service Concierge agents must operate when processing customer home-service requests.

The system must use a combination of:

* Sequential agent processing
* Parallel agent processing
* Reference-file knowledge
* Structured agent outputs
* Result aggregation
* Provider ranking
* Validation

The system must prioritize correctness, consistency, minimal unnecessary changes, and clear separation of responsibilities between agents.

---

# 2. Core Agent Rules

All agents must follow these rules:

1. Perform only the responsibility assigned to the agent.
2. Do not duplicate another agent's responsibility.
3. Use information from previous agents rather than reinterpreting it unnecessarily.
4. Do not invent customer information.
5. Do not invent provider information.
6. Do not invent availability, pricing, ratings, distance, or other provider attributes.
7. Use reference files as the source of truth for service-domain rules.
8. Treat reference files as read-only.
9. Never modify reference files during normal application execution.
10. Preserve the existing project architecture and implementation style.
11. Make the minimum necessary change when modifying existing files.
12. Do not refactor unrelated code.
13. Do not introduce unnecessary abstractions.
14. Validate outputs before passing them to the next stage.

---

# 3. Reference Files

Reference files contain domain knowledge and examples that agents should use when processing requests.

Expected reference files include:

```text
references/
├── plumbing.md
├── hvac.md
├── electrical.md
├── provider_rules.md
└── response_examples.md
```

## Reference-file policy

Reference files are **read-only**.

Agents may:

* Read them
* Search them
* Extract relevant information
* Use their rules
* Use their examples as guidance

Agents must NOT:

* Edit them
* Rewrite them
* Reformat them
* Add information to them
* Delete information from them

Reference files must remain unchanged after application execution.

---

# 4. Style Preservation

When working with existing project files, preserve the existing style.

Preserve:

* naming conventions
* formatting
* indentation
* import conventions
* function structure
* class structure
* comments
* logging patterns
* error-handling patterns
* data structures
* existing architectural conventions

Do not rewrite existing code merely to make it look cleaner.

Do not reformat an entire file when only a small change is required.

Do not introduce a different programming style unless explicitly required.

---

# 5. Sequential Pipeline

The initial request-processing workflow must execute sequentially.

The sequence is:

```text
Customer Request
       ↓
Intake Agent
       ↓
Service Classification Agent
       ↓
Requirements Agent
       ↓
Service Request Agent
```

Each agent must receive the output of the preceding agent.

An agent must not skip a preceding stage unless the workflow explicitly supports that behavior.

---

# 6. Intake Agent

## Responsibility

Convert the user's natural-language request into a structured representation.

The Intake Agent should identify information such as:

* customer problem
* requested service
* preferred date
* preferred time
* location
* urgency
* additional information supplied by the customer

The agent must not guess missing information.

## Output

Return a structured request containing the information that was actually provided.

Example:

```json
{
  "problem": "AC is running but not cooling",
  "preferred_date": "tomorrow",
  "preferred_time": "5 PM - 8 PM",
  "location": "Columbus, OH"
}
```

---

# 7. Service Classification Agent

## Responsibility

Determine the appropriate service category using the available reference material.

Supported V1 categories:

* Plumbing
* HVAC
* Electrical

The classification must be based on the customer's description and the applicable reference file.

## Output

Return:

```json
{
  "service_category": "HVAC",
  "issue_type": "AC cooling failure",
  "urgency": "normal"
}
```

If the service cannot be confidently classified, do not invent a category.

Return an appropriate clarification state.

---

# 8. Requirements Agent

## Responsibility

Determine whether enough information exists to search for providers.

Check required information such as:

* service category
* problem description
* location
* preferred date
* preferred time

Use the relevant reference material to determine whether additional information is required.

## Output

Return:

```json
{
  "complete": true,
  "required_information": [],
  "missing_information": []
}
```

If information is missing:

```json
{
  "complete": false,
  "required_information": [
    "location"
  ],
  "missing_information": [
    "location"
  ]
}
```

Do not proceed to provider matching when required information is missing.

---

# 9. Service Request Agent

## Responsibility

Create the normalized request that will be provided to the parallel provider agents.

The Service Request Agent should combine validated information from the preceding stages.

Example:

```json
{
  "service_category": "HVAC",
  "issue_type": "AC cooling failure",
  "location": "Columbus, OH",
  "preferred_date": "tomorrow",
  "preferred_time": "5 PM - 8 PM",
  "urgency": "normal"
}
```

This object becomes the input to the parallel provider evaluation stage.

---

# 10. Parallel Provider Evaluation

After the sequential pipeline completes successfully, provider evaluation must execute in parallel.

Example:

```text
                  Service Request
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
     Provider A     Provider B     Provider C
       Agent           Agent           Agent
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                   Aggregator
                         ↓
                     Ranking
```

Each provider agent must work independently.

Provider agents must not depend on the output of another provider agent.

---

# 11. Provider Agents

Each provider agent evaluates one provider using the normalized service request.

Evaluate only attributes supported by the provider data.

Possible attributes include:

* service capability
* availability
* price
* distance
* rating
* specialty
* other explicitly provided provider information

Do not invent missing attributes.

## Output

Each provider agent must return a consistent structured result.

Example:

```json
{
  "provider_id": "provider_001",
  "provider_name": "ABC HVAC Services",
  "eligible": true,
  "available": true,
  "price": 120,
  "distance_miles": 4.2,
  "rating": 4.8,
  "reason": "Available during the requested time and provides HVAC cooling repair."
}
```

If the provider is not suitable:

```json
{
  "provider_id": "provider_002",
  "provider_name": "XYZ Services",
  "eligible": false,
  "available": false,
  "reason": "No availability during the requested time."
}
```

---

# 12. Aggregator Agent

## Responsibility

Collect the results from all parallel provider agents.

The Aggregator must:

* wait for the provider evaluations
* combine the results
* preserve provider information
* remove invalid results
* identify eligible providers
* pass the combined result to the Ranking Agent

The Aggregator must not invent missing provider information.

Example:

```json
{
  "eligible_providers": [
    {
      "provider_id": "provider_001",
      "provider_name": "ABC HVAC Services",
      "price": 120,
      "distance_miles": 4.2,
      "rating": 4.8
    },
    {
      "provider_id": "provider_003",
      "provider_name": "Cool Air Experts",
      "price": 110,
      "distance_miles": 6.1,
      "rating": 4.7
    }
  ]
}
```

---

# 13. Ranking Agent

## Responsibility

Rank eligible providers based only on available data.

The ranking should consider:

1. Availability
2. Service compatibility
3. Customer requirements
4. Rating
5. Distance
6. Price

The ranking criteria must be deterministic whenever sufficient information is available.

The Ranking Agent must not create providers or modify provider attributes.

## Output

Return the recommended providers in ranked order.

Include a concise explanation for why each provider was ranked.

---

# 14. Booking Agent

The Booking Agent operates only after the customer selects a provider.

It must:

1. Confirm the selected provider exists in the aggregated results.
2. Confirm the provider is eligible.
3. Confirm the requested appointment information.
4. Create a booking record using the available application data.
5. Return a booking confirmation.

The Booking Agent must not book a provider that was not returned by the provider evaluation workflow.

For V1, booking may use mock application data rather than a real external booking system.

---

# 15. Error Handling

Agents must handle failures explicitly.

If a sequential agent fails:

```text
Stop the pipeline.
Report the failure.
Do not pass invalid output to the next agent.
```

If one parallel provider agent fails:

```text
Do not fail the entire provider search unnecessarily.
Record the failed provider evaluation.
Allow other provider agents to complete.
```

The Aggregator should continue using successfully evaluated providers.

If all provider evaluations fail:

```text
Return a clear message that no provider recommendations
could be generated.
```

Never fabricate a fallback provider.

---

# 16. Missing Information

If required customer information is missing, do not guess.

Ask the customer for the missing information.

Example:

```text
To find an available HVAC provider, I need your service location.
```

Do not continue to provider matching until required information is available.

---

# 17. Output Consistency

Agents should use structured outputs when communicating with other agents.

Do not rely on free-form text for internal agent-to-agent communication when structured data can be used.

Internal agent outputs should be:

* predictable
* machine-readable
* concise
* validated

The final customer-facing response may be natural language.

---

# 18. Minimal-Change Development Rule

When implementing or modifying the application:

1. Inspect the existing implementation first.
2. Identify the smallest change needed.
3. Modify only necessary files.
4. Preserve existing style.
5. Do not rewrite working code unnecessarily.
6. Do not modify reference files.
7. Do not modify unrelated functionality.
8. Review the final diff.
9. Remove unrelated changes before completion.

---

# 19. Validation

Before considering a workflow complete, validate:

### Sequential workflow

* Intake Agent executes first.
* Classification receives Intake output.
* Requirements receives Classification output.
* Service Request receives validated information.
* Invalid/incomplete data does not proceed.

### Parallel workflow

* Multiple provider agents execute independently.
* Provider results use a consistent schema.
* Aggregator waits for the parallel results.
* Failed provider evaluations do not corrupt successful results.
* Ranking operates only on aggregated provider results.

### Booking

* Only an eligible provider can be booked.
* Booking information matches the selected provider.
* A confirmation is returned.

---

# 20. Final Quality Checklist

Before completing any implementation or modification:

* [ ] Reference files were not modified.
* [ ] Only required application files were changed.
* [ ] Existing style was preserved.
* [ ] No unnecessary refactoring was introduced.
* [ ] Sequential pipeline executes in the required order.
* [ ] Parallel provider agents execute independently.
* [ ] Aggregator correctly gathers parallel results.
* [ ] Ranking uses only available provider information.
* [ ] Missing information is handled explicitly.
* [ ] Agent failures are handled gracefully.
* [ ] No information is fabricated.
* [ ] Relevant tests or validation checks pass.
* [ ] Final changes are minimal and focused.
