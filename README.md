# stockJEDI

AI-Powered Stock Intelligence and Investment Analysis Platform

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14.0-000000?style=flat&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-06B6D4?style=flat&logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&logoColor=white)

---

## Overview

stockJEDI is an AI-powered stock intelligence platform that accepts stock URLs, ticker symbols, or company names from financial platforms and produces institutional-style investment analysis. The platform combines machine learning models (XGBoost, LSTM, Prophet) with AI-powered report generation to deliver comprehensive stock analysis.

### Key Features

- **Multi-source Input**: Accepts stock URLs, ticker symbols, or company names from 8+ financial platforms
- **AI-Powered Analysis**: Institutional-grade investment reports generated using Groq API
- **ML Predictions**: Ensemble model combining XGBoost, LSTM, and Prophet for price predictions
- **Technical Analysis**: RSI, MACD, Bollinger Bands, ATR, VWAP, and more
- **Sentiment Analysis**: News and social media sentiment scoring
- **Real-time Dashboard**: Interactive frontend with charts and recommendations
- **Portfolio Management**: Track holdings and analyze portfolio performance
- **Watchlist**: Monitor favorite stocks with real-time updates

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14, React 18, TypeScript, TailwindCSS |
| **Backend** | FastAPI, Python 3.12, SQLAlchemy, Pydantic |
| **Database** | PostgreSQL 15, Redis 7 |
| **ML/AI** | XGBoost, TensorFlow (LSTM), Prophet, Groq API |
| **Infrastructure** | Docker Compose, Nginx, Alembic Migrations |
| **Monitoring** | Prometheus, Structured Logging (Loguru) |

---

## Project Structure

```
stockJEDI/
├── backend/                    # FastAPI backend application
│   ├── app/                    # Application code
│   │   ├── api/               # API endpoints
│   │   ├── auth/              # Authentication (JWT)
│   │   ├── core/              # Configuration
│   │   ├── db/                # Database session
│   │   ├── middleware/        # Error handling, logging, rate limiting
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   ├── alembic/               # Database migrations
│   ├── Dockerfile             # Backend container
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── app/               # Pages and routes
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── types/             # TypeScript types
│   ├── package.json           # Node.js dependencies
│   └── *.config.js            # Configuration files
├── ml/                         # Machine learning pipeline
│   ├── datasets/              # Data collection and processing
│   ├── training/              # Model training scripts
│   ├── models/                # Model implementations
│   ├── features/              # Feature engineering
│   ├── evaluation/            # Model evaluation metrics
│   └── saved_models/          # Trained model files
├── deployment/                 # Deployment configurations
│   ├── nginx.conf             # Nginx configuration
│   └── kubernetes.yaml        # Kubernetes manifests
├── docker-compose.yml         # Docker orchestration
├── docker-compose.dev.yml     # Development overrides
└── .env.example               # Environment variables template
```

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git
- Groq API Key (free from [console.groq.com](https://console.groq.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/denziljosteve/stockJEDI.git
cd stockJEDI
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Start with Docker

```bash
docker-compose up --build
```

### 4. Access the Application

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |
| **Prometheus Metrics** | http://localhost:8000/metrics |

---

## Development Setup

### Option 1: Docker Setup (Recommended)

The easiest way to run the full project is with Docker Compose. This sets up all services automatically.

#### Prerequisites

- Docker and Docker Compose installed
- Groq API Key

#### Quick Start with Docker

```bash
# 1. Clone the repository
git clone https://github.com/denziljosteve/stockJEDI.git
cd stockJEDI

# 2. Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. Start all services (Backend, Frontend, PostgreSQL, Redis)
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Docker Development Mode

For development with hot-reload and debugging:

```bash
# Start with development overrides (hot-reload, debug ports)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Or run in background
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

#### Docker Services Included

| Service | Port | Description |
|---------|------|-------------|
| **backend** | 8000 | FastAPI application |
| **frontend** | 3000 | Next.js application |
| **db** | 5432 | PostgreSQL database |
| **redis** | 6379 | Redis cache |
| **migrate** | - | Database migrations (runs once) |

#### Docker Commands Reference

```bash
# Start all services
docker-compose up --build

# Start in background
docker-compose up --build -d

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend

# Rebuild specific service
docker-compose build backend

# Run database migrations manually
docker-compose run --rm migrate alembic upgrade head

# Access backend container shell
docker-compose exec backend bash

# Access database
docker-compose exec db psql -U user -d stockjedi
```

---

### Option 2: Manual Setup (Without Docker)

If you prefer to run services manually or don't have Docker installed.

#### Prerequisites

- Python 3.12
- Node.js 20+
- PostgreSQL 15
- Redis 7
- Groq API Key

#### Backend Setup

```bash
# Create virtual environment
cd backend
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Make sure DATABASE_URL, REDIS_URL, JWT_SECRET are set in .env

# Run database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Access at http://localhost:3000
```

#### ML Models Setup

```bash
# Set Python path (from project root)
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Collect historical data (5 years for 10 tickers)
python3 ml/datasets/data_collector.py

# Train models (in order)
python3 ml/training/train_xgboost.py
python3 ml/training/train_lstm.py
python3 ml/training/train_prophet.py
python3 ml/training/train_ensemble.py

# Verify models exist
ls -la ml/saved_models/
# Should contain: xgboost.pkl, lstm.h5, prophet.pkl, ensemble.pkl
```

#### Database Setup (Manual)

```bash
# Create PostgreSQL database
createdb stockjedi

# Or with Docker just the database
docker run -d --name stock-db \
  -p 5432:5432 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=stockjedi \
  postgres:15-alpine

# Create Redis instance
docker run -d --name stock-redis \
  -p 6379:6379 \
  redis:7-alpine
```

---

### Option 3: Hybrid Setup

Run databases with Docker, application manually:

```bash
# Start only databases
docker-compose up -d db redis

# Run backend manually
cd backend
source venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Run frontend manually
cd frontend
npm run dev
```

---

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health/` | Health check |
| GET | `/api/v1/stock/search?q={query}` | Search stocks |
| POST | `/api/v1/stock/extract` | Extract ticker from URL |
| POST | `/api/v1/stock/analyze?ticker={ticker}` | Analyze stock |
| GET | `/api/v1/stock/{ticker}/historical` | Get historical data |

### Protected Endpoints (Require JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/prediction/{ticker}` | Get ML predictions |
| GET | `/api/v1/report/{ticker}` | Get AI report |
| POST | `/api/v1/report/{ticker}` | Generate AI report |
| GET | `/api/v1/sentiment/{ticker}` | Get sentiment analysis |
| GET | `/api/v1/portfolio/` | Get portfolio |
| POST | `/api/v1/portfolio/add` | Add to portfolio |
| DELETE | `/api/v1/portfolio/remove` | Remove from portfolio |
| GET | `/api/v1/watchlist/` | Get watchlist |
| POST | `/api/v1/watchlist/add` | Add to watchlist |
| DELETE | `/api/v1/watchlist/remove` | Remove from watchlist |

---

## ML Pipeline

### Models

1. **XGBoost**: Gradient boosting for classification (Bullish/Neutral/Bearish)
2. **LSTM**: Deep learning for time series prediction
3. **Prophet**: Facebook's time series forecasting
4. **Ensemble**: Meta-model combining all three using stacking

### Training

```bash
# Collect 5 years of historical data for 10 major tickers
python3 ml/datasets/data_collector.py

# Train individual models
python3 ml/training/train_xgboost.py
python3 ml/training/train_lstm.py
python3 ml/training/train_prophet.py

# Train ensemble meta-model (uses out-of-fold predictions)
python3 ml/training/train_ensemble.py
```

### Features

- Technical indicators: RSI, MACD, SMA, EMA, ATR, VWAP, ADX, Bollinger Bands
- Price data: OHLCV with multiple timeframes
- Fundamentals: P/E ratio, EPS, Revenue Growth, ROE, Debt/Equity
- Sentiment: News and social media analysis (placeholder)

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI reports | Yes |
| `NEWS_API_KEY` | News API for sentiment analysis | Yes |
| `FINNHUB_API_KEY` | Finnhub API for market data | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `JWT_SECRET` | Secret for JWT token signing | Yes |
| `POSTGRES_USER` | PostgreSQL username | Yes |
| `POSTGRES_PASSWORD` | PostgreSQL password | Yes |
| `POSTGRES_DB` | PostgreSQL database name | Yes |

---

## Security Features

- ✅ JWT authentication on protected endpoints
- ✅ Password hashing with bcrypt
- ✅ Rate limiting with SlowAPI
- ✅ CORS configuration
- ✅ Non-root Docker containers
- ✅ TLS/SSL ready (Nginx)
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ Environment variable validation on startup
- ✅ Structured logging with Loguru

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Denzil Josteve Fernandes**

- 📧 Email: [denziljosteve@gmail.com](mailto:denziljosteve@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/denziljosteve](https://www.linkedin.com/in/denziljosteve)
- 🐙 GitHub: [github.com/denziljosteve](https://github.com/denziljosteve)

---

## Acknowledgments

- [Groq](https://groq.com/) for AI API
- [Yahoo Finance](https://finance.yahoo.com/) for market data
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

---

**Built with by Denzil Josteve Fernandes**
