# stockJEDI Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Kubernetes Cluster (Optional, for prod scale)
- API Keys: Groq API Key

## Local Development
1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in secrets (DB, Redis, Groq).
3. Run: `docker compose up --build`
4. Access Frontend at `http://localhost:3000` and API at `http://localhost:8000`.

## Production Deployment (Kubernetes)
1. Apply secrets:
   `kubectl create secret generic stockjedi-secrets --from-literal=GROQ_API_KEY=...`
2. Apply deployments:
   `kubectl apply -f deployment/kubernetes.yaml`
3. Ensure Nginx Ingress is configured using `deployment/nginx.conf` logic.

## CI/CD
- GitHub Actions are configured in `.github/workflows/main.yml`.
- Pushes to `main` will trigger `pytest`, Docker builds, and push to the defined container registry.
