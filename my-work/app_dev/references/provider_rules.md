# Provider Matching and Ranking Reference

## Purpose

This document defines the rules for evaluating, filtering, and ranking service providers.

This file is **read-only**. Agents must not modify it.

---

# Provider Eligibility

A provider is eligible only when the available provider data indicates that the provider can satisfy the customer's service request.

Evaluate:

1. Service compatibility
2. Availability
3. Service location
4. Other explicitly defined provider constraints

A provider that does not meet a required condition must not be recommended.

---

# Service Compatibility

The provider's `service_type` must match the requested service category.

Supported categories:

* Plumbing
* HVAC
* Electrical

Example:

```text
Customer Service: HVAC
Provider Service: HVAC
Result: Compatible
```

Example:

```text
Customer Service: HVAC
Provider Service: Plumbing
Result: Not compatible
```

Do not infer compatibility from the provider's name.

---

# Availability

A provider is available only when the provider data indicates availability for the requested appointment window.

If the provider has no availability:

```text
eligible = false
available = false
```

Do not recommend an unavailable provider as the primary booking option.

---

# Location

Use the provider's available service-area or location information.

Do not assume that a provider serves an area simply because the provider name suggests it.

If service-area information is unavailable, do not fabricate it.

---

# Price

Use the provider's available price information.

Do not estimate or invent a provider's price.

If price is unavailable, preserve it as unavailable rather than substituting an assumed value.

---

# Rating

Use the provider's recorded rating.

Do not create or modify ratings.

A missing rating must remain missing.

---

# Distance

Use the distance supplied by the application.

Do not invent distance.

If distance is unavailable, do not estimate it.

---

# Provider Evaluation Output

Provider agents should return a consistent structure containing, where available:

```json
{
  "provider_id": "",
  "provider_name": "",
  "eligible": false,
  "available": false,
  "price": null,
  "distance_miles": null,
  "rating": null,
  "reason": ""
}
```

Only populate values supported by provider data or the provider request.

---

# Ranking Rules

Rank eligible providers using this priority order:

1. Service compatibility
2. Availability
3. Match to requested appointment window
4. Rating
5. Distance
6. Price

Only eligible providers should be ranked.

Do not rank providers that fail a required eligibility condition.

---

# Ranking Transparency

Every recommended provider should have a concise explanation.

Examples:

```text
Available during the requested appointment window and highly rated.
```

```text
Available at the requested time and closer than other eligible providers.
```

```text
Lowest available price among eligible providers.
```

The explanation must be supported by actual provider data.

---

# Ties

When providers are otherwise equivalent:

1. Prefer the higher rating when available.
2. Then prefer the shorter distance when available.
3. Then prefer the lower price when available.
4. If still tied, preserve the provider ordering from the aggregated input.

Do not invent additional ranking criteria.

---

# Missing Provider Information

Missing optional information must not automatically make a provider ineligible.

For example:

```text
rating = null
```

does not mean:

```text
rating = 0
```

Do not replace missing information with assumed values.

---

# Provider-Agent Independence

Each provider agent must evaluate its assigned provider independently.

A provider agent must not:

* compare itself against another provider
* modify another provider's result
* depend on another provider agent's output
* perform final ranking

The Aggregator and Ranking Agent are responsible for combining and comparing results.
