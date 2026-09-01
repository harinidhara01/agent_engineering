# HVAC Service Reference

## Purpose

This document provides reference information for classifying HVAC requests and identifying common HVAC service requirements.

This file is **read-only**. Agents must not modify it.

---

## Service Category

Primary category:

**HVAC**

---

## Common HVAC Issues

| Issue               | Description                                       | Typical Service          |
| ------------------- | ------------------------------------------------- | ------------------------ |
| AC not cooling      | Air conditioner runs but does not adequately cool | AC diagnosis/repair      |
| AC not turning on   | Air conditioner does not start                    | AC diagnosis/repair      |
| Weak airflow        | Airflow from vents is unusually weak              | HVAC diagnosis           |
| Furnace not heating | Heating system does not provide heat              | Furnace diagnosis/repair |
| HVAC unusual noise  | System produces unusual sounds                    | HVAC diagnosis           |
| HVAC unusual smell  | System produces an unusual odor                   | HVAC diagnosis           |
| Thermostat issue    | Thermostat does not operate as expected           | Thermostat diagnosis     |
| HVAC maintenance    | Customer requests routine maintenance             | HVAC maintenance         |
| Air quality issue   | Customer reports indoor air-quality concerns      | HVAC/air-quality service |

---

## Urgency Guidelines

### Potentially urgent

Consider elevated urgency when the customer reports:

* complete loss of heating during dangerous cold conditions
* complete loss of cooling during dangerous heat conditions
* burning smell associated with equipment
* smoke
* other conditions that indicate an immediate safety concern

Do not make a safety determination beyond the information provided.

### Normal

Examples:

* AC not cooling adequately
* weak airflow
* thermostat problem
* routine maintenance
* unusual but non-dangerous HVAC noise

---

## Required Information for Provider Search

A provider search normally requires:

* problem description
* service category
* service location
* preferred appointment date
* preferred appointment time

Useful optional information may include:

* equipment type
* system age
* symptoms
* whether the system is currently operating

Do not invent optional information.

---

## Classification Examples

### Example 1

Customer:

> My AC is running but my house isn't getting cold.

Classification:

```text
Service: HVAC
Issue: AC not cooling
Urgency: Normal
```

### Example 2

Customer:

> My furnace isn't producing heat.

Classification:

```text
Service: HVAC
Issue: Furnace not heating
Urgency: Normal
```

### Example 3

Customer:

> My thermostat isn't working correctly.

Classification:

```text
Service: HVAC
Issue: Thermostat issue
Urgency: Normal
```

---

## Classification Rules

* Use HVAC when the primary problem concerns heating, cooling, ventilation, or related HVAC equipment.
* Do not infer equipment type unless the customer provides it.
* Preserve the customer's actual symptoms.
* Do not diagnose a technical failure that cannot be established from the description.
* If the service cannot be confidently classified, request clarification.
