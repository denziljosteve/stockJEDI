# stockJEDI Production Deployment Guide

This guide details the steps required to deploy **stockJEDI** to a production environment using Docker, Kubernetes, and Nginx.

---

## 1. Infrastructure Overview

The system architecture for production follows a highly available, containerized flow:

**Users** → **Nginx (Reverse Proxy & SSL)** → **Frontend (Next.js)** → **Backend (FastAPI)** → **Redis (Cache)** → **PostgreSQL (DB)** → **ML Models & Groq API**

---

## 2. Server Requirements

### Minimum Specifications
- **CPU:** 2 Cores
- **RAM:** 4GB
- **Storage:** 20GB SSD
- **OS:** Ubuntu 22.04 LTS (Recommended)

### Recommended Specifications (Scaling)
- **CPU:** 4+ Cores
- **RAM:** 8GB+
- **Storage:** 50GB+ SSD

---

## 3. Domain & SSL Setup

### DNS Configuration
Configure your DNS provider with the following A records:
- `app.stockjedi.ai` → Server IP (Frontend)
- `api.stockjedi.ai` → Server IP (Backend)

### SSL with Let's Encrypt
Use Certbot to generate certificates:
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d app.stockjedi.ai -d api.stockjedi.ai
```

---

## 4. Production Environment Variables

Ensure your production `.env` is securely managed (e.g., via Kubernetes Secrets or HashiCorp Vault).

| Key | Value Description |
| :--- | :--- |
| `GROQ_API_KEY` | High-throughput production key from Groq. |
| `DATABASE_URL` | Connection string to a managed Postgres instance (e.g., RDS). |
| `REDIS_URL` | Connection string to a secure Redis instance (e.g., ElastiCache). |
| `JWT_SECRET` | Strong, 64-character random string. |
| `BACKEND_CORS_ORIGINS` | `["https://app.stockjedi.ai"]` |

---

## 5. Docker Deployment

### Building Images
```bash
docker build -t stockjedi-backend:latest ./backend
docker build -t stockjedi-frontend:latest ./frontend
```

> **Note on ML Models:** Before building the backend image, ensure models are trained and present in `ml/saved_models/`, or configure a persistent volume mount in Kubernetes to store these artifacts. The `data_collector.py` and `train_*.py` scripts should be executed periodically to keep the intelligence layer fresh.

### Running with Docker Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 6. Kubernetes Deployment (Scale)

Apply the production manifests:
```bash
kubectl apply -f deployment/kubernetes.yaml
kubectl get pods
kubectl get services
```

---

## 7. Nginx Setup (Reverse Proxy)

Configure Nginx to handle WebSockets and SSL termination.

```nginx
server {
    listen 443 ssl;
    server_name api.stockjedi.ai;

    location / {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 8. Database & Redis Management

### Backup Procedure (PostgreSQL)
Schedule a daily cron job:
```bash
pg_dump -U user -h db_host stockjedi > backup_$(date +%F).sql
```

### Redis Persistence
Ensure `appendonly yes` is enabled in your `redis.conf` to prevent data loss on restarts.

---

## 9. CI/CD Pipeline

Pushes to the `main` branch trigger the GitHub Actions workflow (`.github/workflows/main.yml`):
1. **Linting & Unit Testing**
2. **Security Scanning** (Secret detection)
3. **Docker Build & Push** to Registry
4. **K8s Rolling Update**

---

## 10. Monitoring & Security

### Metrics
Monitor the `/metrics` endpoint using **Prometheus** and visualize performance in **Grafana**.

### Security Checklist
- [ ] Disable `DEBUG` modes in FastAPI and Next.js.
- [ ] Rotate `JWT_SECRET` every 90 days.
- [ ] Use a Firewall (UFW) to block all ports except 80, 443, and 22.
- [ ] Enable `CORS_ORIGINS` to allow only your production domain.

---

## 11. Rollback & Maintenance

### Rollback Strategy
If a deployment fails:
```bash
kubectl rollout undo deployment/stockjedi-backend
```

### Maintenance Mode
Set a `503 Service Unavailable` page in Nginx during database migrations or major upgrades.
