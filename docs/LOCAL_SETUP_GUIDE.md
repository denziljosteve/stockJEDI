# stockJEDI Local Setup Guide

This guide provides a comprehensive walk-through for setting up **stockJEDI** on your local machine for development and testing.

---

## 1. Introduction
**stockJEDI** is an AI-powered stock intelligence platform that aggregates market data, calculates technical indicators, performs sentiment analysis, and generates institutional-grade investment reports using LLMs (Groq) and Machine Learning ensembles (XGBoost, LSTM, Prophet).

### Architecture Overview
- **Frontend:** Next.js 14, React, TailwindCSS, Lucide.
- **Backend:** FastAPI (Python 3.12).
- **Database:** PostgreSQL (Primary storage).
- **Cache/Broker:** Redis (Caching & Task Queue).
- **AI/ML:** Groq API & Custom Python ML models.

---

## 2. Prerequisites
Ensure you have the following software installed:
- **Git:** [Download](https://git-scm.com/)
- **Docker & Docker Compose:** [Download](https://www.docker.com/products/docker-desktop/)
- **Python 3.12+:** [Download](https://www.python.org/downloads/)
- **Node.js 18+:** [Download](https://nodejs.org/)
- **PostgreSQL 15+:** [Download](https://www.postgresql.org/download/)
- **Redis:** [Download](https://redis.io/docs/getting-started/)

---

## 3. Clone the Project
```bash
git clone https://github.com/your-username/stockJEDI.git
cd stockJEDI
```

---

## 4. Environment Setup
The application requires several environment variables to function correctly.

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure Variables:**
   | Variable | Description | Example |
   | :--- | :--- | :--- |
   | `GROQ_API_KEY` | API key from Groq Console | `gsk_v8...` |
   | `NEWS_API_KEY` | Key for financial news | `a1b2c3...` |
   | `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/stockjedi` |
   | `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
   | `JWT_SECRET` | Secret for signing auth tokens | `openssl rand -hex 32` |
   | `GOOGLE_CLIENT_ID`| For OAuth login | `12345-abc.apps.googleusercontent.com` |

---

## 5. Local Database Setup
1. **Initialize PostgreSQL:**
   Ensure the service is running.
2. **Create Database:**
   ```sql
   CREATE DATABASE stockjedi;
   ```
3. **Run Initial Schemas:**
   The backend will automatically handle table creation on the first startup via SQLAlchemy's `Base.metadata.create_all`.

---

## 6. Backend Setup (FastAPI)
1. **Create Virtual Environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)*

---

## 7. Intelligence Engine Setup (Cold Start)
To enable real predictions instead of structural fallbacks:

1. **Collect Historical Data:**
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python3 ml/datasets/data_collector.py
   ```
   This will create a `historical_data.csv` in `ml/datasets/training/`.

2. **Train Models:**
   Run the following scripts sequentially:
   ```bash
   python3 ml/training/train_xgboost.py
   python3 ml/training/train_lstm.py
   python3 ml/training/train_prophet.py
   python3 ml/training/train_ensemble.py
   ```
   This will populate `ml/saved_models/` with `.pkl` and `.h5` files required by the `PredictionService`.

---

## 8. Frontend Setup (Next.js)
1. **Install Dependencies:**
   ```bash
   cd frontend
   npm install
   ```
2. **Start Development Server:**
   ```bash
   npm run dev
   ```
   *Access UI at [http://localhost:3000](http://localhost:3000)*

---

## 8. Docker Setup (Recommended)
If you prefer not to install local services, use Docker Compose to spin up everything:
```bash
docker-compose up --build
```
This starts:
- **Backend:** Port 8000
- **Frontend:** Port 3000
- **Database:** Port 5432
- **Redis:** Port 6379

---

## 9. Troubleshooting
- **Redis Connection Failure:** Ensure Redis is running (`redis-cli ping` should return `PONG`). Check `REDIS_URL` in `.env`.
- **Database Connection Failure:** Verify PostgreSQL credentials. Ensure the `stockjedi` database exists.
- **Config Validation Error:** If the backend fails to start with "Missing required environment variables", check that your `.env` file is in the `stockJEDI/` root and contains real keys instead of placeholders.

---

## 10. Development Workflow
1. **Edit:** Make changes to code.
2. **Validate:** Check Swagger UI for API updates.
3. **Test:** Run `pytest backend/app/tests`.
4. **Push:** Commit your changes and push to your branch.
