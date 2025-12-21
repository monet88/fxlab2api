# Flow2API Deployment Guide

> Last Updated: 2025-12-22
> Version: 1.0.0

## Overview

This guide covers deploying Flow2API in various environments, from local development to production deployments.

---

## Quick Reference

| Deployment Method | Use Case | Complexity |
|-------------------|----------|------------|
| Docker Compose (Standard) | Most users | Low |
| Docker Compose (WARP Proxy) | Users needing proxy | Low |
| Local Python | Development | Low |
| Docker Swarm | High availability | Medium |
| Kubernetes | Enterprise | High |

---

## Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| CPU | 1 core | 2+ cores |
| RAM | 2 GB | 4+ GB |
| Storage | 5 GB | 20+ GB (with cache) |
| Network | Stable internet | Low latency to Google |

### Software Requirements

**Docker Deployment:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**Local Python:**
- Python 3.8+ (3.11 recommended)
- pip package manager

---

## Deployment Options

### Option 1: Docker Compose (Recommended)

#### Standard Mode

For environments with direct internet access to Google APIs.

```bash
# Clone repository
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  flow2api:
    image: thesmallhancat/flow2api:latest
    container_name: flow2api
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./config/setting.toml:/app/config/setting.toml
      - ./static:/app/static
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

#### WARP Proxy Mode

For environments requiring Cloudflare WARP proxy.

```bash
# Start with WARP proxy
docker-compose -f docker-compose.proxy.yml up -d

# View logs
docker-compose -f docker-compose.proxy.yml logs -f
```

**docker-compose.proxy.yml:**
```yaml
version: '3.8'

services:
  flow2api:
    image: thesmallhancat/flow2api:latest
    container_name: flow2api
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./config/setting_warp.toml:/app/config/setting.toml
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    depends_on:
      - warp

  warp:
    image: caomingjun/warp
    container_name: warp
    restart: always
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
      - "1080:1080"
    environment:
      - WARP_SLEEP=2
    cap_add:
      - MKNOD
      - AUDIT_WRITE
      - NET_ADMIN
    sysctls:
      - net.ipv6.conf.all.disable_ipv6=0
      - net.ipv4.conf.all.src_valid_mark=1
    volumes:
      - ./data:/var/lib/cloudflare-warp
```

### Option 2: Local Python Installation

For development or environments without Docker.

```bash
# Clone repository
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start service
python main.py
```

---

## Configuration

### Initial Configuration

Edit `config/setting.toml` before first run:

```toml
[global]
api_key = "your-secure-api-key-here"    # Change this!
admin_username = "admin"
admin_password = "your-secure-password"  # Change this!

[server]
host = "0.0.0.0"
port = 8000

[flow]
labs_base_url = "https://labs.google/fx/api"
api_base_url = "https://aisandbox-pa.googleapis.com/v1"
timeout = 120
poll_interval = 3.0
max_poll_attempts = 200

[proxy]
proxy_enabled = false
proxy_url = ""

[cache]
enabled = false
timeout = 7200
base_url = ""

[debug]
enabled = false
log_requests = false
log_responses = false
mask_token = true

[admin]
error_ban_threshold = 3

[generation]
image_timeout = 300
video_timeout = 1500
```

### WARP Proxy Configuration

For WARP mode, use `config/setting_warp.toml`:

```toml
[global]
api_key = "your-secure-api-key-here"
admin_username = "admin"
admin_password = "your-secure-password"

[proxy]
proxy_enabled = true
proxy_url = "socks5://warp:1080"
```

---

## Post-Deployment Steps

### 1. Verify Installation

```bash
# Check container status (Docker)
docker ps

# Test API endpoint
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer your-api-key"

# Expected response:
# {"object":"list","data":[...]}
```

### 2. Access Admin Panel

- **URL**: http://localhost:8000
- **Username**: admin (or configured value)
- **Password**: admin (or configured value)

**IMPORTANT**: Change the default password immediately!

### 3. Add Tokens

1. Login to admin panel
2. Navigate to Tokens tab
3. Click "Add Token"
4. Enter your Google session token (ST)
5. Configure token settings
6. Save

### 4. Test Generation

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "A cute cat"}],
    "stream": true
  }'
```

---

## Production Deployment

### Security Checklist

- [ ] Change default API key
- [ ] Change default admin password
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS (reverse proxy)
- [ ] Disable debug mode
- [ ] Review proxy configuration

### Reverse Proxy Setup (Nginx)

```nginx
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

        # SSE support
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;

        # Timeouts for long-running generation
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
    }
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

---

## Docker Management

### Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f flow2api

# Restart service
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Pull latest image
docker-compose pull
docker-compose up -d
```

### Data Persistence

Docker volumes for persistent data:

| Volume | Container Path | Purpose |
|--------|----------------|---------|
| `./data` | `/app/data` | SQLite database |
| `./config` | `/app/config` | Configuration files |
| `./static` | `/app/static` | Custom static files |
| `./tmp` | `/app/tmp` | Cache directory (optional) |

### Backup and Restore

```bash
# Backup database
cp data/flow2api.db data/flow2api.db.backup

# Backup configuration
cp config/setting.toml config/setting.toml.backup

# Restore
docker-compose down
cp data/flow2api.db.backup data/flow2api.db
cp config/setting.toml.backup config/setting.toml
docker-compose up -d
```

---

## Exposing to Internet

### Cloudflare Tunnel (Temporary)

For sharing your local instance temporarily:

```bash
# Install cloudflared
# Windows:
winget install Cloudflare.cloudflared

# Linux:
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Mac:
brew install cloudflared

# Start tunnel (Flow2API must be running)
cloudflared tunnel --url http://localhost:8000
```

You'll get a public URL like: `https://xxx-xxx-xxx.trycloudflare.com`

**Notes:**
- URL changes on each restart
- Computer must stay on
- Admin panel should only be accessed via localhost

---

## Monitoring

### Health Checks

```bash
# Basic connectivity
curl http://localhost:8000/v1/models -H "Authorization: Bearer your-api-key"

# Check admin panel
curl http://localhost:8000/admin/stats -H "Authorization: Bearer your-api-key"
```

### Log Analysis

```bash
# Docker logs
docker-compose logs -f --tail=100

# Filter errors
docker-compose logs 2>&1 | grep -i error

# Follow specific service
docker-compose logs -f flow2api
```

### Resource Monitoring

```bash
# Container stats
docker stats flow2api

# Disk usage
docker system df
du -sh data/
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs flow2api

# Common issues:
# - Port 8000 already in use
# - Volume permission errors
# - Invalid configuration
```

### Port Already in Use

```bash
# Find process using port
# Linux/Mac:
sudo lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process or change port in docker-compose.yml
```

### Database Errors

```bash
# Reset database (WARNING: loses all data)
docker-compose down
rm data/flow2api.db
docker-compose up -d
```

### Token Refresh Failures

1. Check token validity in admin panel
2. Verify network connectivity to Google
3. Check proxy configuration if using proxy
4. Review logs for specific errors

### Generation Timeouts

Increase timeouts in configuration:

```toml
[generation]
image_timeout = 600    # 10 minutes
video_timeout = 3000   # 50 minutes

[flow]
timeout = 300          # 5 minutes per request
max_poll_attempts = 500
```

---

## Upgrade Guide

### Upgrading Docker Deployment

```bash
# Pull latest image
docker-compose pull

# Restart with new image
docker-compose up -d

# Verify version
docker-compose logs | head -20
```

### Upgrading Local Installation

```bash
# Pull latest code
git pull

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
python main.py
```

### Database Migration

Migrations run automatically on startup. If issues occur:

1. Backup database: `cp data/flow2api.db data/flow2api.db.backup`
2. Start service and check logs
3. If migration fails, restore backup and report issue

---

## Environment Variables

Override configuration via environment variables:

| Variable | Description |
|----------|-------------|
| `FLOW2API_API_KEY` | API key for authentication |
| `FLOW2API_HOST` | Server bind address |
| `FLOW2API_PORT` | Server port |
| `FLOW2API_DEBUG` | Enable debug mode |

Example in docker-compose.yml:

```yaml
environment:
  - FLOW2API_API_KEY=your-api-key
  - FLOW2API_DEBUG=false
```

---

*For additional help, see the [Troubleshooting Guide](./TROUBLESHOOTING.md) or open an issue on GitHub.*
