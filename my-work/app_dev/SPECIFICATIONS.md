# Home Service Concierge — Condensed Specifications

## 1. Flask Application Structure
- The application must use Flask and Python 3.11 with a modular structure (app/routes, agents, workflows, services).
- There must be no external frontend framework; only vanilla HTML, CSS, and JS.

## 2. Sequential Agent Workflow
- The app must execute a sequence: Intake Agent -> Classification Agent -> Requirements Agent -> Service Request Agent.
- The pipeline must accurately classify issues into HVAC, Plumbing, or Electrical and handle missing information gracefully.

## 3. Parallel Provider Workflow
- The app must evaluate providers in parallel using independent ProviderAgent instances.
- The AggregatorAgent must gather the valid results without crashing if a single provider fails.
- The RankingAgent must deterministically sort eligible providers by rating, distance, and price.

## 4. Booking and UI
- The UI must visually indicate the workflow steps, clearly separating sequential and parallel tasks.
- A valid provider can be booked via the BookingAgent, generating a confirmation ID.
- The app must not fabricate missing provider data or generate fake bookings if criteria are not met.
