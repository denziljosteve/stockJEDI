# stockJEDI System Architecture

## Overview
stockJEDI follows a microservices-inspired monolithic architecture using FastAPI (Backend) and Next.js (Frontend), orchestrated via Docker and Kubernetes.

## Core Layers
1. **Frontend (Next.js + React + Tailwind):**
   - Handles UI, client-side routing, and caching via React Query.
2. **API Gateway (Nginx):**
   - Manages reverse proxying, WebSockets upgrade, and security headers.
3. **Backend Engine (FastAPI):**
   - **Data Aggregator:** Fetches from Yahoo Finance, News APIs, etc.
   - **Technical Engine:** Calculates RSI, MACD, etc., using pandas/ta.
   - **ML Prediction Engine:** Uses XGBoost, LSTM, and Prophet to output probabilities.
   - **AI Layer:** Interfaces with Groq API to convert data into narrative reports.
4. **Data Layer (PostgreSQL):**
   - Stores users, portfolios, watchlists, and cached historical data.
5. **Caching & Message Broker (Redis):**
   - Backs the Celery task queue and caches heavily-hit API responses.

## Background Processing
- **Celery Workers:** Handle periodic price synchronization and model retraining.
- **Prometheus:** Scrapes `/metrics` for application health and request latencies.
