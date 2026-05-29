# How to Run stockJEDI

This guide provides a step-by-step walkthrough to get the **stockJEDI** platform up and running on your machine, covering dependency installation across all major operating systems.

---

## 1. Prerequisites

Before starting, ensure you have a **Groq API Key**. You can get one for free from the [Groq Console](https://console.groq.com/).

---

## 2. OS-Specific Dependency Installation

### A. Linux (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Git, Python, and Node.js
sudo apt install git python3 python3-pip python3-venv nodejs npm -y

# Install Docker & Compose
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER  # Log out and back in after this
```

### B. Linux (Fedora)
```bash
# Install Git, Python, and Node.js
sudo dnf install git python3 python3-pip nodejs npm -y

# Install Docker & Compose
sudo dnf install docker docker-compose -y
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### C. Linux (Arch)
```bash
# Install Git, Python, and Node.js
sudo pacman -S git python python-pip nodejs npm --noconfirm

# Install Docker & Compose
sudo pacman -S docker docker-compose --noconfirm
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### D. macOS
Using [Homebrew](https://brew.sh/):
```bash
# Install dependencies
brew install git python node docker docker-compose

# Note: For Apple Silicon (M1/M2/M3), ensure you have Docker Desktop installed.
```

### E. Windows
Using [Winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):
```powershell
# Open PowerShell as Administrator
winget install -e --id Git.Git
winget install -e --id Python.Python.3.12
winget install -e --id OpenJS.NodeJS.LTS
winget install -e --id Docker.DockerDesktop
```

---

## 3. Clone and Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/stockJEDI.git
   cd stockJEDI
   ```

2. **Setup environment variables:**
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and enter your `GROQ_API_KEY`.

---

## 4. Initializing the "Brain" (ML Training)

**Important:** The project uses real ML models. You must train them before the prediction features will work.

1. **Setup Python Environment:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

2. **Run Data Collection & Training:**
   ```bash
   # Add root to python path so it can find the ml package
   export PYTHONPATH=$PYTHONPATH:. 

   # 1. Collect real historical data
   python3 ml/datasets/data_collector.py

   # 2. Train the models
   python3 ml/training/train_xgboost.py
   python3 ml/training/train_lstm.py
   python3 ml/training/train_prophet.py
   python3 ml/training/train_ensemble.py
   ```
   *Verify that `ml/saved_models/` now contains `.pkl` and `.h5` files.*

---

## 5. Running the Project (Recommended: Docker)

The easiest way to run the entire stack (Frontend, Backend, Postgres, Redis) is using Docker Compose:

```bash
# From the project root
docker-compose up --build
```

---

## 6. Running Manually (Development Mode)

If you prefer to run components separately:

### A. Start Services (Postgres & Redis)
Ensure you have local instances running or use Docker just for the services:
```bash
docker run -d --name stock-db -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:15-alpine
docker run -d --name stock-redis -p 6379:6379 redis:7-alpine
```

### B. Run Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### C. Run Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 7. Access URLs

| Service | URL |
| :--- | :--- |
| **Frontend UI** | [http://localhost:3000](http://localhost:3000) |
| **API Backend** | [http://localhost:8000](http://localhost:8000) |
| **API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Metrics** | [http://localhost:8000/metrics](http://localhost:8000/metrics) |

---

## 8. Stopping the Project
If using Docker:
```bash
docker-compose down
```
