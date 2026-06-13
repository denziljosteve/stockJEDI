# Running stockJEDI on a Fresh Linux System

This guide explains how to run the stockJEDI project on a clean Linux system (Ubuntu/Debian-based) where nothing is installed.

---

## Prerequisites

Before starting, ensure you have:
- A **Groq API Key** (free from [Groq Console](https://console.groq.com/))
- A **News API Key** (from [NewsAPI](https://newsapi.org/))
- A **Finnhub API Key** (from [Finnhub](https://finnhub.io/))
- **Google OAuth credentials** (optional, for Google login)

---

## Step 1: Update System and Install Basic Tools

```bash
# Update package lists and upgrade existing packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools and utilities
sudo apt install -y curl wget git build-essential software-properties-common apt-transport-https ca-certificates gnupg lsb-release
```

---

## Step 2: Install Python 3.12

```bash
# Add Python PPA repository
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12 and related tools
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
```

---

## Step 3: Install Node.js and npm

```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version
```

---

## Step 4: Install Docker and Docker Compose

```bash
# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Docker Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group (avoid using sudo for docker commands)
sudo usermod -aG docker $USER

# Log out and log back in for group changes to take effect
# Or run: newgrp docker
```

**Important:** After adding yourself to the docker group, log out and log back in, or run `newgrp docker` before proceeding.

---

## Step 5: Clone the Repository

```bash
# Navigate to your desired directory
cd ~

# Clone the repository (replace with actual repo URL)
git clone https://github.com/your-username/stockJEDI.git

# Enter the project directory
cd stockJEDI
```

---

## Step 6: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env
```

Fill in the following values in the `.env` file:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
NEWS_API_KEY=your_news_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here

# Database (will be set up by Docker)
DATABASE_URL=postgresql://user:password@localhost:5432/stockjedi
REDIS_URL=redis://localhost:6379

# JWT Secret (generate a strong random string)
JWT_SECRET=your_strong_random_secret_here

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## Step 7: Train ML Models (Required Before First Run)

The project requires trained machine learning models to function properly. You must train them before starting the application.

### 7.1 Setup Python Virtual Environment

```bash
# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

### 7.2 Collect Historical Data

```bash
# Set Python path to include project root
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Collect historical stock data
python3 ml/datasets/data_collector.py
```

### 7.3 Train ML Models

```bash
# Train XGBoost model
python3 ml/training/train_xgboost.py

# Train LSTM model
python3 ml/training/train_lstm.py

# Train Prophet model
python3 ml/training/train_prophet.py

# Train Ensemble model (combines all models)
python3 ml/training/train_ensemble.py
```

**Verification:** After training, verify that `ml/saved_models/` contains `.pkl` and `.h5` files.

```bash
ls -la ml/saved_models/
```

You should see files like:
- `xgboost_model.pkl`
- `lstm_model.h5`
- `prophet_model.pkl`
- `ensemble_model.pkl`

---

## Step 8: Run with Docker (Recommended)

The easiest way to run the entire stack is using Docker Compose.

```bash
# From the project root directory
docker-compose up --build
```

This will:
- Run database migrations automatically
- Build and start the backend API (port 8000)
- Build and start the frontend UI (port 3000)
- Start PostgreSQL database (port 5432)
- Start Redis cache (port 6379)

**To run in detached mode (background):**
```bash
docker-compose up --build -d
```

**To view logs:**
```bash
docker-compose logs -f
```

---

## Step 9: Run Manually (Development Mode)

If you prefer to run components separately for development:

### 9.1 Start Database and Redis Services

```bash
# Start PostgreSQL database
docker run -d --name stock-db \
  -p 5432:5432 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=stockjedi \
  postgres:15-alpine

# Start Redis cache
docker run -d --name stock-redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 9.2 Run Backend

```bash
# Open a new terminal
cd stockJEDI

# Activate virtual environment
source venv/bin/activate

# Navigate to backend directory
cd backend

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 9.3 Run Frontend

```bash
# Open another terminal
cd stockJEDI/frontend

# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

---

## Step 10: Access the Application

Once everything is running, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend UI** | http://localhost:3000 | Main web interface |
| **Backend API** | http://localhost:8000 | API endpoint |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs (Swagger UI) |
| **Prometheus Metrics** | http://localhost:8000/metrics | Monitoring metrics |

---

## Database Migrations

Alembic is configured for database migrations. Here are common commands:

### Running Migrations

```bash
cd backend

# Apply all pending migrations
alembic upgrade head

# Check current migration status
alembic current

# View migration history
alembic history
```

### Creating New Migrations

When you modify models, generate a new migration:

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Review the generated migration in alembic/versions/
# Then apply it
alembic upgrade head
```

### Rolling Back Migrations

```bash
cd backend

# Rollback one migration
alembic downgrade -1

# Rollback to a specific revision
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base
```

### Docker Migration Commands

```bash
# Run migrations manually in Docker
docker-compose run --rm migrate alembic upgrade head

# Generate new migration in Docker
docker-compose run --rm migrate alembic revision --autogenerate -m "description"

# Check current migration status in Docker
docker-compose run --rm migrate alembic current
```

---

## Step 11: Verify Installation

### Check Backend Health
```bash
curl http://localhost:8000/api/v1/health
```

### Check Frontend
Open http://localhost:3000 in your browser. You should see the stockJEDI dashboard.

### Check ML Models
Navigate to the prediction feature in the UI and try analyzing a stock ticker (e.g., "AAPL" or "TSLA").

---

## Stopping the Application

### If using Docker Compose:
```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (database data)
docker-compose down -v
```

### If running manually:
```bash
# Stop backend (Ctrl+C in the terminal running uvicorn)
# Stop frontend (Ctrl+C in the terminal running npm run dev)

# Stop database and Redis containers
docker stop stock-db stock-redis
docker rm stock-db stock-redis
```

---

## Troubleshooting

### Common Issues

**1. "Permission denied" for Docker commands**
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER
# Log out and log back in, or run:
newgrp docker
```

**2. "Port already in use" errors**
```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :3000
sudo lsof -i :5432

# Kill the process using the port
sudo kill -9 <PID>
```

**3. ML models not found**
```bash
# Ensure you ran the training steps in Step 7
# Check if models exist:
ls -la ml/saved_models/

# If not, retrain:
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 ml/datasets/data_collector.py
python3 ml/training/train_xgboost.py
python3 ml/training/train_lstm.py
python3 ml/training/train_prophet.py
python3 ml/training/train_ensemble.py
```

**4. Database connection errors**
```bash
# Check if PostgreSQL is running
docker ps | grep stock-db

# Check database logs
docker logs stock-db

# Restart database if needed
docker restart stock-db
```

**5. Python version issues**
```bash
# Ensure you're using Python 3.12
python3 --version

# If not, install Python 3.12 (see Step 2)
```

**6. Node.js version issues**
```bash
# Ensure you're using Node.js 20+
node --version

# If not, install Node.js 20 (see Step 3)
```

---

## System Requirements

- **OS:** Ubuntu 20.04+ or similar Linux distribution
- **RAM:** Minimum 8GB (16GB recommended for ML training)
- **Storage:** At least 10GB free space
- **CPU:** Multi-core processor recommended for ML training

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Author

**Denzil Josteve Fernandes**

- 📧 Email: [denziljosteve@gmail.com](mailto:denziljosteve@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/denziljosteve](https://www.linkedin.com/in/denziljosteve)
- 🐙 GitHub: [github.com/denziljosteve](https://github.com/denziljosteve)

---

**Last Updated:** June 2026
