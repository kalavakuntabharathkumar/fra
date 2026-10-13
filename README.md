# ML Fraud Scoring Service (Starter Implementation)

A local demo that trains a scikit-learn classifier, serves scores through FastAPI,
uses Redis for short-lived idempotent score caching, persists transaction outcomes in
PostgreSQL, and includes Docker Compose, Kubernetes manifests, tests, and API docs.

## Run locally
Requirements: Docker + Docker Compose.

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs
Health: GET /health
Score transaction: POST /v1/score
Example:
```json
{"transaction_id":"tx-1001","amount":125.5,"merchant_category":"electronics","country":"IN","account_age_days":240,"transactions_last_hour":2}
```

The training script creates a synthetic demonstration dataset at startup if no model exists.
Synthetic data is for engineering demonstration only, not production fraud detection.
Before deployment, use validated, privacy-reviewed historical data, monitor drift and calibration,
secure endpoints, and establish an explicit human/operations review process.

> Resume metrics are illustrative targets from the brief; this repository does not claim they
> have been measured or achieved.
