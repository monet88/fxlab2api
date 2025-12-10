# Flow2API Troubleshooting Guide

## 🎯 Overview

This guide helps you diagnose and resolve common issues with Flow2API. Follow the steps systematically to identify and fix problems.

## 🔍 Quick Diagnostics

### Health Check Commands

```bash
# Check if service is running
curl -f http://localhost:8000/health

# Check service status (Docker)
docker ps | grep flow2api

# Check logs
docker logs flow2api
# or
docker-compose logs -f

# Check port availability
sudo lsof -i :8000

# Check disk space
df -h

# Check memory usage
free -h
```

### Log Analysis

```bash
# View recent logs
tail -n 100 /var/log/flow2api.log

# Search for errors
grep -i error /var/log/flow2api.log

# Filter by timestamp
grep "2024-01-15" /var/log/flow2api.log | grep -i error

# Follow logs in real-time
tail -f /var/log/flow2api.log
```

## 🚨 Common Issues

### 1. Service Won't Start

#### Symptoms
- Docker container exits immediately
- Port binding errors
- Configuration errors

#### Solutions

**Port Already in Use**
```bash
# Find process using port
sudo lsof -i :8000
sudo netstat -tulpn | grep :8000

# Kill process or change port
sudo kill -9 <PID>
# Or edit config/setting.toml to use different port
```

**Configuration Errors**
```bash
# Validate TOML syntax
cat config/setting.toml | python -c "import tomli, sys; tomli.load(sys.stdin.buffer)"

# Check file permissions
ls -la config/setting.toml
chmod 644 config/setting.toml

# Verify required fields
grep -E "^\[|^\w+\s*=" config/setting.toml
```

**Docker Issues**
```bash
# Rebuild container
docker-compose build --no-cache

# Check Docker daemon
sudo systemctl status docker

# Check disk space
docker system df
docker system prune -a  # Clean unused images
```

### 2. Authentication Failures

#### Symptoms
- "Invalid API key" errors
- Can't access admin panel
- 401 Unauthorized responses

#### Solutions

**API Key Issues**
```bash
# Verify API key in request
curl -v http://localhost:8000/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check configured API key
grep api_key config/setting.toml

# Test with default key
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer han1234"
```

**Admin Login Issues**
```bash
# Reset admin credentials
docker-compose exec flow2api python -c "
from src.core.database import Database
import asyncio
async def reset():
    db = Database()
    await db.update_admin_config(username='admin', password='new-password')
asyncio.run(reset())
"
```

### 3. Token Issues

#### Symptoms
- "No available tokens" errors
- Token refresh failures
- Generation requests failing

#### Solutions

**Check Token Status**
```bash
# Via API
curl http://localhost:8000/admin/tokens \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check token count
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT COUNT(*) FROM tokens WHERE is_active = 1;"
```

**Token Refresh Issues**
```bash
# Check token expiration
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT id, email, at_expires FROM tokens WHERE is_active = 1;"

# Manual token refresh
curl -X POST http://localhost:8000/admin/tokens/<token-id>/refresh \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check ST validity
# Login to Google Labs and verify session token
```

**Token Error Threshold**
```bash
# Check error counts
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT id, email, consecutive_error_count FROM tokens;"

# Reset error count
curl -X POST http://localhost:8000/admin/tokens/<token-id>/reset-errors \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 4. Generation Failures

#### Symptoms
- "Generation failed" errors
- Streaming stops abruptly
- No output from models

#### Solutions

**Enable Debug Mode**
```toml
# Edit config/setting.toml
[debug]
enabled = true
log_requests = true
log_responses = true
```

**Check Model Availability**
```bash
# List available models
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Test specific model
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "test"}],
    "stream": false
  }'
```

**Check Token Permissions**
```bash
# Verify token capabilities
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT image_enabled, video_enabled FROM tokens WHERE id = <token-id>;"

# Check credits (for VideoFX)
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT credits FROM tokens WHERE id = <token-id>;"
```

### 5. Proxy Issues

#### Symptoms
- Connection timeouts
- SSL errors
- "Cannot connect to proxy" errors

#### Solutions

**Test Proxy Connection**
```bash
# Test proxy directly
curl -x http://proxy-server:port https://www.google.com

# Test with authentication
curl -x http://user:pass@proxy-server:port https://www.google.com

# Check proxy configuration
grep proxy_url config/setting.toml
```

**Debug Proxy Issues**
```toml
# Enable proxy debug logging
[debug]
enabled = true
log_requests = true
```

**Proxy URL Format**
```bash
# Correct formats:
http://proxy.example.com:8080
http://user:pass@proxy.example.com:8080
socks5://proxy.example.com:1080
socks5://user:pass@proxy.example.com:1080
```

### 6. Performance Issues

#### Symptoms
- Slow response times
- High memory usage
- Database locks

#### Solutions

**Monitor Performance**
```bash
# Check resource usage
docker stats

# Check database performance
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "SELECT COUNT(*) FROM request_logs WHERE created_at > datetime('now', '-1 hour');"

# Check active connections
netstat -an | grep :8000 | wc -l
```

**Optimize Configuration**
```toml
# Reduce concurrency
[flow]
poll_interval = 5.0  # Increase from 3.0
max_poll_attempts = 100  # Reduce from 200

# Enable caching
[cache]
enabled = true
timeout = 3600  # 1 hour
```

**Database Maintenance**
```bash
# Vacuum database (reduces size)
docker-compose exec flow2api sqlite3 data/flow2api.db "VACUUM;"

# Clear old logs
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "DELETE FROM request_logs WHERE created_at < datetime('now', '-7 days');"
```

### 7. Database Issues

#### Symptoms
- "Database is locked" errors
- Data corruption
- Migration failures

#### Solutions

**Database Lock Issues**
```bash
# Check for long-running queries
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "PRAGMA lock_status;"

# Enable WAL mode for better concurrency
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "PRAGMA journal_mode=WAL;"
```

**Corruption Recovery**
```bash
# Backup current database
cp data/flow2api.db data/flow2api.db.backup

# Try to dump data
sqlite3 data/flow2api.db ".dump" > backup.sql

# Create new database
sqlite3 data/flow2api_new.db < backup.sql

# Replace database
mv data/flow2api_new.db data/flow2api.db
```

**Migration Issues**
```bash
# Check database version
docker-compose exec flow2api sqlite3 data/flow2api.db \
  "PRAGMA user_version;"

# Manual migration (backup first!)
docker-compose exec flow2api sqlite3 data/flow2api.db < migration.sql
```

## 🔧 Advanced Troubleshooting

### Network Issues

```bash
# Test connectivity to Google APIs
curl -I https://labs.google/fx/api
curl -I https://aisandbox-pa.googleapis.com/v1

# Check DNS resolution
nslookup labs.google.com

# Trace route
traceroute labs.google.com

# Check SSL certificates
echo | openssl s_client -connect labs.google.com:443 -servername labs.google.com | openssl x509 -text -noout
```

### Memory Issues

```bash
# Check memory usage
free -h
cat /proc/meminfo

# Monitor Python memory
python -m tracemalloc -q your_script.py

# Check for memory leaks
docker stats --no-stream

# Generate memory profile
python -m memory_profiler your_script.py
```

### CPU Issues

```bash
# Check CPU usage
top -p $(pgrep -f flow2api)

# Profile Python code
python -m cProfile -o profile.stats your_script.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

### Disk Issues

```bash
# Check disk usage
df -h
du -sh /var/lib/docker/

# Find large files
find / -type f -size +100M -exec ls -lh {} \;

# Clean Docker
docker system prune -a
docker volume prune
```

## 📝 Log Analysis

### Common Error Patterns

```bash
# Token errors
grep -i "token.*error" flow2api.log | tail -20

# Generation failures
grep -i "generation.*failed" flow2api.log | tail -20

# Proxy errors
grep -i "proxy.*error" flow2api.log | tail -20

# Timeout errors
grep -i "timeout" flow2api.log | tail -20
```

### Creating Debug Logs

```python
# Add to your code for debugging
import logging
import traceback

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Log exceptions
try:
    # Your code here
    pass
except Exception as e:
    logging.error(f"Error: {e}")
    logging.error(traceback.format_exc())
```

## 🐛 Known Issues

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Solution:**
```bash
# Update CA certificates
sudo apt-get update ca-certificates

# For Python requests
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Disable SSL verification (not recommended for production)
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```

### Issue: "Database is locked"

**Solution:**
```bash
# Enable WAL mode
sqlite3 data/flow2api.db "PRAGMA journal_mode=WAL;"

# Increase timeout
sqlite3 data/flow2api.db "PRAGMA busy_timeout=5000;"

# Check for concurrent access
lsof data/flow2api.db
```

### Issue: "No module named 'curl_cffi'"

**Solution:**
```bash
# Install system dependencies
sudo apt-get install libcurl4-openssl-dev libssl-dev

# Reinstall package
pip uninstall curl_cffi
pip install curl-cffi
```

### Issue: "Address already in use"

**Solution:**
```bash
# Find process using port
sudo lsof -i :8000
sudo netstat -tulpn | grep 8000

# Kill process
sudo kill -9 <PID>

# Or change port in config
sed -i 's/port = 8000/port = 8001/' config/setting.toml
```

## 📞 Getting Help

### Before Asking for Help

1. Check this troubleshooting guide
2. Search existing GitHub issues
3. Enable debug mode and collect logs
4. Document the exact error messages
5. Note the steps to reproduce

### Information to Provide

When reporting issues, include:

```markdown
**Environment:**
- OS: Ubuntu 20.04
- Docker version: 20.10.21
- Flow2API version: 1.0.0

**Configuration:**
- Number of tokens: 5
- Proxy enabled: Yes
- Cache enabled: No

**Error Details:**
- Error message: "Generation failed: No available tokens"
- Frequency: Every 5 minutes
- Logs: [attach relevant logs]

**Steps to Reproduce:**
1. Start service with docker-compose up -d
2. Send request to /v1/chat/completions
3. Observe error response

**What I've Tried:**
- Restarted service
- Added new tokens
- Checked token status (all active)
```

### Community Resources

- **GitHub Issues**: https://github.com/TheSmallHanCat/flow2api/issues
- **GitHub Discussions**: https://github.com/TheSmallHanCat/flow2api/discussions
- **Documentation**: Check all guides in the docs/ folder

### Professional Support

For production deployments or urgent issues:

1. Provide detailed system information
2. Include configuration files (sanitize sensitive data)
3. Share complete error logs
4. Describe impact and urgency
5. Be prepared for remote access if needed

## 🔄 Recovery Procedures

### Complete Service Recovery

```bash
#!/bin/bash
# full-recovery.sh

# 1. Stop service
docker-compose down

# 2. Backup current state
cp -r data data.backup.$(date +%Y%m%d_%H%M%S)
cp config/setting.toml config.toml.backup

# 3. Clean up
docker system prune -f
docker volume prune -f
rm -rf tmp/*

# 4. Start fresh
docker-compose up -d

# 5. Restore tokens from backup
# [Manual step - re-add tokens through UI]
```

### Database Recovery

```bash
#!/bin/bash
# db-recovery.sh

# 1. Stop service
docker-compose stop flow2api

# 2. Backup corrupted DB
cp data/flow2api.db data/flow2api.db.corrupt

# 3. Try to recover
echo ".dump" | sqlite3 data/flow2api.db.corrupt > recovery.sql
sqlite3 data/flow2api_new.db < recovery.sql

# 4. Replace database
mv data/flow2api_new.db data/flow2api.db

# 5. Restart service
docker-compose start flow2api
```

---

**Still need help?** Create an issue on GitHub with all relevant information and logs. The community will help you resolve the problem."}