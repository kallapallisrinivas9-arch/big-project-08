# WeatherGuard AI

## SIH 2026

Problem Statement:

SIH26073

AI/ML-Based Intelligent Anomaly Detection
for Automatic Weather Stations (AWS)

---

## Objective

WeatherGuard AI detects abnormal AWS sensor
observations and attempts to distinguish:

- Normal observation
- Sensor fault
- Communication fault
- Genuine weather event
- Uncertain observation

The system also provides:

- Explainable evidence
- Root cause
- Confidence
- Conservative correction decision
- Sensor health
- Alerts

---

## Architecture

AWS / Simulator
        |
        v
Data Validation
        |
        v
Feature Engineering
        |
        v
Physics / Statistical Checks
        |
        v
Isolation Forest
        |
        v
Evidence Fusion
        |
        v
Root Cause
        |
        v
Confidence
        |
        v
Correction Engine
        |
        v
Sensor Health
        |
        v
Alert Service
        |
        v
FastAPI
        |
        v
React Dashboard

---

## Supported Fault Types

1. SPIKE
2. FROZEN_SENSOR
3. DRIFT
4. NOISE
5. COMMUNICATION_FAILURE
6. DATA_CORRUPTION
7. MULTIVARIATE_INCONSISTENCY

---

## Backend Installation

Create virtual environment:

Windows:

    python -m venv .venv

Activate:

    .venv\Scripts\activate

Install:

    pip install -r backend/requirements.txt

---

## Run Backend

From project root:

    python -m uvicorn backend.main:app --reload

API:

    http://127.0.0.1:8000

Swagger:

    http://127.0.0.1:8000/docs

---

## Run Tests

    python -m pytest -q

---

## Frontend

Open terminal:

    cd frontend

Install:

    npm install

Run:

    npm run dev

The dashboard uses `http://127.0.0.1:8000` by default. To point it at
another backend, set `VITE_API_URL` before starting Vite:

        $env:VITE_API_URL="http://localhost:8000"
        npm run dev

---

## Demo

1. Start backend.
2. Start frontend.
3. Open frontend URL.
4. Click "Run AI Simulation".
5. Synthetic AWS observations are generated.
6. Seven fault scenarios are injected.
7. Feature engineering is performed.
8. Isolation Forest detects anomalies.
9. Evidence fusion determines operational state.
10. Correction engine makes a conservative decision.
11. Sensor health is calculated.
12. Alerts are displayed.

---

## Important

The simulator is a demonstration component.

It does not represent real-world weather
validation.

No real-world ML accuracy should be claimed
until the model is evaluated on an appropriate
real AWS dataset.

---

## Database

Default local database:

SQLite

Database file:

weatherguard.db

The DATABASE_URL environment variable can
later be used to configure PostgreSQL.