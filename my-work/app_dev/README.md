# Home Service Concierge

This is a Flask-based web application that connects customers with home service providers (Plumbing, HVAC, Electrical). It uses a sequential pipeline to process user requests, followed by a parallel workflow to search and rank available service providers using mock data.

## Requirements

- Python 3.11

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

## Running the Application

Start the Flask development server:
```bash
flask --app app run --debug
```

The app will be available at `http://127.0.0.1:5000/`.

## Running Tests

Run the pytest suite to verify the application workflows and agent logic:
```bash
pytest tests/
```

## Architecture

- **Sequential Pipeline**: Intake -> Classification -> Requirements -> Service Request
- **Parallel Workflow**: The system evaluates multiple providers concurrently using `concurrent.futures`, then passes them to an `AggregatorAgent` and finally ranks them with a `RankingAgent`.
