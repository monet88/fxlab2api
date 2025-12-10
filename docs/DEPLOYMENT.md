# Flow2API Deployment Guide

## 🎯 Overview

This guide covers deploying Flow2API in production environments, from single-server setups to high-availability configurations.

## 📋 Pre-Deployment Checklist

### Security
- [ ] Change default API key
- [ ] Change default admin credentials
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS certificates
- [ ] Review proxy configuration
- [ ] Disable debug mode

### Performance
- [ ] Configure appropriate timeouts
- [ ] Set up monitoring and alerting
- [ ] Plan for scaling needs
- [ ] Configure caching strategy
- [ ] Test load balancing

### Reliability
- [ ] Set up database backups
- [ ] Configure log rotation
- [ ] Plan for failover scenarios
- [ ] Test recovery procedures
- [ ] Document deployment

## 🚀 Deployment Options

### 1. Single Server Deployment

Best for: Small to medium workloads, testing, development

#### Using Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  flow2api:
    image: flow2api:latest
    container_name: flow2api
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./tmp:/app/tmp
      - ./config:/app/config
    environment:
      - FLOW2API_HOST=0.0.0.0
      - FLOW2API_PORT=8000
      - FLOW2API_DEBUG=false
    networks:
      - flow2api-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  flow2api-network:
    driver: bridge

volumes:
  data:
  tmp:
```

#### Deployment Steps

1. **Prepare the server**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Install Docker Compose
   sudo apt install docker-compose-plugin
   ```

2. **Create deployment directory**
   ```bash
   sudo mkdir -p /opt/flow2api
   cd /opt/flow2api
   ```

3. **Copy configuration files**
   ```bash
   # Copy your configuration
   sudo cp /path/to/your/config/setting.toml ./

   # Set proper permissions
   sudo chown -R $USER:$USER /opt/flow2api
   ```

4. **Deploy the service**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

5. **Set up reverse proxy (Nginx)**
   ```nginx
   # /etc/nginx/sites-available/flow2api
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;

           # WebSocket support
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

### 2. Multi-Server Deployment

Best for: High availability, load distribution

#### Architecture

```
Load Balancer (Nginx/HAProxy)
    ↓
App Server 1 ← → Shared Storage
    ↓              (Database/Cache)
App Server 2
```

#### Docker Swarm Deployment

```yaml
# docker-stack.yml
version: '3.8'

services:
  flow2api:
    image: flow2api:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - "8000"
    volumes:
      - flow2api-data:/app/data
      - flow2api-tmp:/app/tmp
    networks:
      - flow2api-network
    environment:
      - FLOW2API_REDIS_URL=redis://redis:6379

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    networks:
      - flow2api-network
    depends_on:
      - flow2api

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - flow2api-network

networks:
  flow2api-network:
    driver: overlay

volumes:
  flow2api-data:
  flow2api-tmp:
  redis-data:
```

#### Deploy Stack

```bash
# Initialize swarm
sudo docker swarm init

# Deploy stack
docker stack deploy -c docker-stack.yml flow2api

# Check status
docker stack services flow2api
```

### 3. Kubernetes Deployment

Best for: Enterprise environments, auto-scaling

#### Deployment Manifest

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flow2api
  labels:
    app: flow2api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flow2api
  template:
    metadata:
      labels:
        app: flow2api
    spec:
      containers:
      - name: flow2api
        image: flow2api:latest
        ports:
        - containerPort: 8000
        env:
        - name: FLOW2API_HOST
          value: "0.0.0.0"
        - name: FLOW2API_PORT
          value: "8000"
        - name: FLOW2API_REDIS_URL
          value: "redis://redis-service:6379"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: config
        configMap:
          name: flow2api-config
      - name: data
        persistentVolumeClaim:
          claimName: flow2api-pvc
```

#### Service Manifest

```yaml
# k8s-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: flow2api-service
spec:
  selector:
    app: flow2api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```

#### ConfigMap

```yaml
# k8s-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flow2api-config
data:
  setting.toml: |
    [global]
    api_key = "your-production-api-key"
    admin_username = "admin"
    admin_password = "your-secure-password"

    [server]
    host = "0.0.0.0"
    port = 8000

    [flow]
    labs_base_url = "https://labs.google/fx/api"
    api_base_url = "https://aisandbox-pa.googleapis.com/v1"
    timeout = 120
    poll_interval = 3.0
    max_poll_attempts = 200
```

#### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace flow2api

# Apply configurations
kubectl apply -f k8s-configmap.yaml -n flow2api
kubectl apply -f k8s-pvc.yaml -n flow2api
kubectl apply -f k8s-deployment.yaml -n flow2api
kubectl apply -f k8s-service.yaml -n flow2api

# Check deployment
kubectl get pods -n flow2api
kubectl get services -n flow2api
```

## 🏗️ Production Architecture

### High-Availability Setup

```
Internet
    ↓
Cloud Load Balancer (AWS ALB/GCP CLB)
    ↓
CDN (CloudFront/Cloud CDN)
    ↓

Region 1                          Region 2
┌─────────────┐                   ┌─────────────┐
│  Nginx x2   │                   │  Nginx x2   │
└──────┬──────┘                   └──────┬──────┘
       ↓                                 ↓
┌─────────────┐                   ┌─────────────┐
│Flow2API x3  │                   │Flow2API x3  │
└──────┬──────┘                   └──────┬──────┘
       ↓                                 ↓
┌─────────────┐                   ┌─────────────┐
│PostgreSQL   │←── Replication ──→│PostgreSQL   │
│Primary      │                   │Standby      │
└─────────────┘                   └─────────────┘
       ↓                                 ↓
┌─────────────┐                   ┌─────────────┐
│Redis Cluster│←─── Sync ────────→│Redis Cluster│
└─────────────┘                   └─────────────┘
```

### Database Scaling

#### PostgreSQL Setup

```yaml
# docker-compose.postgres.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: flow2api
      POSTGRES_USER: flow2api
      POSTGRES_PASSWORD: secure-password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "8080:80"
```

#### Migration from SQLite

```python
# migration_script.py
import sqlite3
import psycopg2
import pandas as pd

# Connect to SQLite
sqlite_conn = sqlite3.connect('data/flow2api.db')

# Connect to PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    database="flow2api",
    user="flow2api",
    password="secure-password"
)

# Migrate tables
tables = ['tokens', 'projects', 'tasks', 'request_logs']

for table in tables:
    # Read from SQLite
    df = pd.read_sql(f"SELECT * FROM {table}", sqlite_conn)

    # Write to PostgreSQL
    df.to_sql(table, pg_conn, if_exists='replace', index=False)

print("Migration completed!")
```

### Caching Strategy

#### Redis Configuration

```yaml
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000

# docker-compose.redis.yml
redis:
  image: redis:7-alpine
  command: redis-server /usr/local/etc/redis/redis.conf
  volumes:
    - ./redis.conf:/usr/local/etc/redis/redis.conf
    - redis-data:/data
  ports:
    - "6379:6379"
```

#### Redis Cluster

```bash
# Create Redis cluster
docker run -d --name redis-1 redis:7-alpine

docker run -d --name redis-2 redis:7-alpine

docker run -d --name redis-3 redis:7-alpine

# Configure cluster
docker exec -it redis-1 redis-cli --cluster create \
  redis-1:6379 redis-2:6379 redis-3:6379
```

## 📊 Monitoring and Observability

### Prometheus Metrics

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter('flow2api_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('flow2api_request_duration_seconds', 'Request duration')

# Token metrics
token_count = Gauge('flow2api_tokens_total', 'Total tokens', ['status'])
token_errors = Counter('flow2api_token_errors_total', 'Token errors', ['token_id'])

# Generation metrics
generation_count = Counter('flow2api_generations_total', 'Total generations', ['model', 'status'])
generation_duration = Histogram('flow2api_generation_duration_seconds', 'Generation duration', ['model'])
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Flow2API Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(flow2api_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Token Health",
        "targets": [
          {
            "expr": "flow2api_tokens_total"
          }
        ]
      },
      {
        "title": "Generation Success Rate",
        "targets": [
          {
            "expr": "rate(flow2api_generations_total{status='success'}[5m]) / rate(flow2api_generations_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### Health Checks

```python
# health.py
from fastapi import APIRouter
from src.core.database import Database
from src.services.token_manager import TokenManager

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy"}

@router.get("/ready")
async def readiness_check():
    """Readiness check with dependencies."""
    try:
        # Check database
        db = Database()
        await db.execute("SELECT 1")

        # Check token availability
        token_manager = TokenManager(db, None)
        active_tokens = await token_manager.get_active_tokens()

        if not active_tokens:
            return {"status": "not_ready", "reason": "No active tokens"}

        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "reason": str(e)}
```

## 🔒 Security Hardening

### Network Security

```yaml
# docker-compose.security.yml
services:
  flow2api:
    networks:
      - frontend
      - backend
    expose:
      - "8000"  # Only expose to internal network

  nginx:
    networks:
      - frontend
    ports:
      - "80:80"
      - "443:443"

  postgres:
    networks:
      - backend
    expose:
      - "5432"

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No internet access
```

### Application Security

```python
# security.py
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("100/minute")
async def protected_endpoint():
    return {"message": "Success"}
```

### Secrets Management

```bash
# Use Docker secrets
echo "your-api-key" | docker secret create flow2api_api_key -
echo "admin-password" | docker secret create flow2api_admin_password -

# Reference in compose
docker-compose -f docker-compose.secrets.yml up -d
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: |
          docker build -t flow2api:${{ github.sha }} .
          docker tag flow2api:${{ github.sha }} flow2api:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /opt/flow2api
            docker-compose pull
            docker-compose up -d
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_REGISTRY: registry.gitlab.com
  IMAGE_NAME: $DOCKER_REGISTRY/your-group/flow2api

test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - pip install -r requirements-test.txt
    - pytest

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $IMAGE_NAME:$CI_COMMIT_SHA .
    - docker tag $IMAGE_NAME:$CI_COMMIT_SHA $IMAGE_NAME:latest
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
    - docker push $IMAGE_NAME:latest

deploy:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache openssh
    - ssh $DEPLOY_USER@$DEPLOY_HOST "docker pull $IMAGE_NAME:latest && docker-compose up -d"
  only:
    - main
```

## 🚨 Rollback Strategy

### Blue-Green Deployment

```bash
#!/bin/bash
# rollback.sh

# Switch traffic to blue environment
docker-compose -f docker-compose.blue.yml up -d

# Wait for health check
sleep 30

# Update nginx configuration
cp nginx.blue.conf /etc/nginx/nginx.conf
nginx -s reload

# Stop green environment
docker-compose -f docker-compose.green.yml down
```

### Database Rollback

```bash
#!/bin/bash
# db-rollback.sh

# Restore from backup
docker exec -i postgres pg_restore -U flow2api -d flow2api < backup.sql

# Notify application
curl -X POST http://localhost:8000/admin/reload-config
```

## 📋 Production Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Documentation updated
- [ ] Monitoring configured
- [ ] Backup procedures tested
- [ ] Rollback plan documented

### Launch Day
- [ ] Deploy during low-traffic window
- [ ] Monitor all metrics closely
- [ ] Have rollback ready
- [ ] Team on standby

### Post-Launch
- [ ] Monitor error rates
- [ ] Check resource usage
- [ ] Verify all features work
- [ ] Update documentation
- [ ] Schedule first review

## 🔧 Maintenance

### Regular Tasks

```bash
#!/bin/bash
# maintenance.sh

# Backup database
docker exec postgres pg_dump -U flow2api flow2api > backup-$(date +%Y%m%d).sql

# Clean old logs
docker exec flow2api find /var/log -name "*.log" -mtime +7 -delete

# Update images
docker-compose pull
docker-compose up -d

# System updates
sudo apt update && sudo apt upgrade -y
```

### Monitoring Alerts

```yaml
# alerts.yml
groups:
- name: flow2api
  rules:
  - alert: HighErrorRate
    expr: rate(flow2api_requests_total{status="error"}[5m]) > 0.1
    for: 5m
    annotations:
      summary: "High error rate detected"

  - alert: TokenExhausted
    expr: flow2api_tokens_total{status="active"} == 0
    for: 1m
    annotations:
      summary: "No active tokens available"
```

---

**Next Steps**: After deployment, monitor your service closely. For troubleshooting issues, see the [Troubleshooting Guide](./TROUBLESHOOTING.md)."}