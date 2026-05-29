# stockJEDI

AI-Powered Stock Intelligence and Investment Analysis Platform.

## Overview

stockJEDI is an AI-powered stock intelligence platform that accepts stock URLs, ticker symbols, or company names from financial platforms and produces institutional-style investment analysis.

## Project Structure

- `frontend/`: Next.js, React, TailwindCSS, TypeScript.
- `backend/`: FastAPI, Python.
- `ml/`: XGBoost, LSTM, Prophet models, along with training and data collection scripts.
...
## Intelligence Engine Initialization

To move from structural prototype to a live intelligence engine, the following steps must be executed:

1. **Collect Historical Data:**
   ```bash
   python3 ml/datasets/data_collector.py
   ```
2. **Train ML Models:**
   ```bash
   python3 ml/training/train_xgboost.py
   # Repeat for train_lstm.py, train_prophet.py, and train_ensemble.py
   ```

This will populate `ml/saved_models/` and enable real probability-based predictions.
- `prompts/`: AI analysis prompts.
- `jobs/`: Background tasks (Celery).
- `database/`: Database schemas and migrations.
- `docs/`: Documentation.
- `deployment/`: Docker and deployment scripts.
- `monitoring/`: Monitoring configurations.
- `logs/`: Application logs.

## Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure your credentials:**
   Open the `.env` file and replace the placeholders with your actual API keys and connection strings:
   - `GROQ_API_KEY`: Get this from the Groq console.
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `REDIS_URL`: Your Redis connection string.
   - `JWT_SECRET`: A strong random string for signing tokens.

The application includes a startup validator that will prevent the backend from running if these required secrets are missing or still contain the default placeholders.

## Setup

(Instructions to be added)
