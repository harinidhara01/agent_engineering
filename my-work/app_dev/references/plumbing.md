# Plumbing Service Reference

## Purpose

This document provides reference information for classifying plumbing requests and identifying common plumbing service requirements.

This file is **read-only**. Agents must not modify it.

---

## Service Category

Primary category:

**Plumbing**

---

## Common Plumbing Issues

| Issue              | Description                                           | Typical Service          |
| ------------------ | ----------------------------------------------------- | ------------------------ |
| Leaking faucet     | Water leaking from a faucet or fixture                | Faucet repair            |
| Leaking pipe       | Water leaking from a visible or concealed pipe        | Pipe repair              |
| Clogged drain      | Water drains slowly or does not drain                 | Drain cleaning           |
| Clogged toilet     | Toilet does not drain properly                        | Toilet unclogging        |
| Running toilet     | Toilet continues running after flushing               | Toilet repair            |
| Low water pressure | Water pressure is unusually low                       | Water-pressure diagnosis |
| Water heater issue | Water heater is not producing expected hot water      | Water-heater service     |
| Burst pipe         | Significant pipe failure causing active water leakage | Emergency plumbing       |
| Sewer backup       | Wastewater backing up into the property               | Emergency plumbing       |

---

## Urgency Guidelines

### Emergency

Consider a plumbing request potentially urgent when the description indicates:

* burst pipe
* major active water leak
* sewer backup
* flooding
* inability to shut off a significant water leak

The agent should communicate the urgency based on the customer's description.

Do not declare an emergency when the information does not support it.

### Normal

Examples:

* dripping faucet
* slow drain
* running toilet
* minor leak
* low water pressure

---

## Required Information for Provider Search

A plumbing provider search normally requires:

* problem description
* service category
* service location
* preferred appointment date
* preferred appointment time

Additional information may improve provider matching but should not be invented.

---

## Classification Examples

### Example 1

Customer:

> My kitchen sink is clogged.

Classification:

```text
Service: Plumbing
Issue: Clogged drain
Urgency: Normal
```

### Example 2

Customer:

> A pipe burst in my basement and water is everywhere.

Classification:

```text
Service: Plumbing
Issue: Burst pipe
Urgency: Emergency
```

### Example 3

Customer:

> My toilet keeps running after I flush.

Classification:

```text
Service: Plumbing
Issue: Running toilet
Urgency: Normal
```

---

## Classification Rules

* Classify only from information supported by the customer's description.
* Do not assume a specific plumbing component when the customer does not identify it.
* If multiple plumbing issues are described, preserve all relevant issues.
* If the request clearly belongs to another supported service category, do not classify it as plumbing merely because plumbing is mentioned.
* If classification is uncertain, request clarification rather than guessing.
