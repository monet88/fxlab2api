# Flow2API Configuration Guide

## 🎯 Overview

This guide covers all configuration options for Flow2API, from basic setup to advanced features like proxy support, caching, and token management.

## 📁 Configuration Files

Flow2API uses TOML format for configuration files:

- `config/setting.toml` - Main configuration file
- `config/setting_warp.toml` - WARP proxy configuration template

## 🔧 Basic Configuration

### Global Settings

```toml
[global]
api_key = "your-secret-api-key"          # API key for authentication
admin_username = "admin"                 # Admin dashboard username
admin_password = "your-secure-password"  # Admin dashboard password
```

**Important Security Notes:**
- Change the default API key immediately
- Use a strong, unique password for admin access
- Consider using environment variables for sensitive data

### Server Configuration

```toml
[server]
host = "0.0.0.0"    # Bind address (0.0.0.0 for all interfaces)
port = 8000         # Port number
```

**Recommendations:**
- Use `127.0.0.1` for local-only access
- Use `0.0.0.0` only if the service needs to be accessible from other machines
- Ensure the port is not blocked by firewall rules

### Flow API Configuration

```toml
[flow]
labs_base_url = "https://labs.google/fx/api"          # Google Labs base URL
api_base_url = "https://aisandbox-pa.googleapis.com/v1"  # AI Sandbox API URL
timeout = 120                                          # Request timeout in seconds
poll_interval = 3.0                                    # Polling interval for status checks
max_poll_attempts = 200                                # Maximum polling attempts
```

**Timeout Guidelines:**
- Image generation: 120-300 seconds
- Video generation: 300-1500 seconds
- Adjust based on your network and model performance

## 🔐 Token Management Configuration

### Adding Tokens

Tokens are managed through the web interface or API. Here's the token structure:

```json
{
  "st": "your-session-token",
  "project_id": "optional-project-id",
  "project_name": "optional-project-name",
  "remark": "Description of this token",
  "image_enabled": true,
  "video_enabled": true,
  "image_concurrency": 2,
  "video_concurrency": 1
}
```

### Token Fields Explained

| Field | Description | Default | Notes |
|-------|-------------|---------|-------|
| `st` | Session Token | Required | Google session token |
| `project_id` | Project ID | Auto-generated | Leave empty to auto-create |
| `project_name` | Project Name | Auto-generated | Custom name for the project |
| `remark` | Description | Empty | For your reference only |
| `image_enabled` | Enable images | true | Allow image generation |
| `video_enabled` | Enable videos | true | Allow video generation |
| `image_concurrency` | Image limit | -1 | -1 = unlimited, 0 = disabled |
| `video_concurrency` | Video limit | -1 | -1 = unlimited, 0 = disabled |

### Concurrency Configuration

```toml
# Global concurrency settings (can be overridden per token)
[generation]
image_timeout = 300   # Image generation timeout (seconds)
video_timeout = 1500  # Video generation timeout (seconds)
```

**Concurrency Best Practices:**
- Start with low limits (1-2) and increase based on usage
- Monitor token performance and error rates
- Balance between speed and account safety

## 🌐 Proxy Configuration

### Basic Proxy Setup

```toml
[proxy]
proxy_enabled = true
proxy_url = "http://username:password@proxy-server:port"
```

### Proxy URL Formats

```toml
# HTTP Proxy
proxy_url = "http://proxy.example.com:8080"

# HTTP Proxy with authentication
proxy_url = "http://user:pass@proxy.example.com:8080"

# SOCKS5 Proxy
proxy_url = "socks5://proxy.example.com:1080"

# SOCKS5 with authentication
proxy_url = "socks5://user:pass@proxy.example.com:1080"
```

### Per-Token Proxy

Configure different proxies for different tokens through the web interface:

1. Access the admin panel
2. Edit a token
3. Set the proxy URL in the token settings
4. Save changes

### Proxy Failover

Flow2API automatically handles proxy failures:
- Retries with different proxies if available
- Falls back to direct connection if proxy fails
- Logs all proxy-related errors for debugging

## 💾 Caching Configuration

### Enable File Caching

```toml
[cache]
enabled = true                    # Enable/disable caching
timeout = 7200                    # Cache TTL in seconds (2 hours)
base_url = ""                     # Optional: Custom base URL for cached files
```

### Cache Directory

Cached files are stored in the `tmp/` directory by default. Ensure:
- Sufficient disk space (videos can be large)
- Write permissions for the application
- Regular cleanup (automatic)

### Custom Cache URL

```toml
[cache]
base_url = "https://cdn.yourdomain.com"  # Serve cached files from CDN
```

This allows you to:
- Use a CDN for faster file delivery
- Mask the origin server URL
- Implement custom caching strategies

## 🐛 Debug Configuration

### Enable Debug Mode

```toml
[debug]
enabled = true          # Enable debug mode
log_requests = true     # Log all incoming requests
log_responses = true    # Log all responses
mask_token = true       # Mask sensitive token data in logs
```

### Debug Output

When debug mode is enabled, you'll see:
- Detailed request/response logs
- Token selection process
- Error stack traces
- Performance metrics

**Warning**: Debug mode can generate large log files. Use only for troubleshooting.

### Log Locations

- Docker: View logs with `docker-compose logs -f`
- Local: Logs are printed to console
- Custom: Configure your logging system to capture stdout

## ⚙️ Advanced Configuration

### Error Handling

```toml
[admin]
error_ban_threshold = 3    # Disable token after N consecutive errors
```

**Error Threshold Guidelines:**
- 3-5 for stable production environments
- Higher values (10+) for testing environments
- 0 to disable auto-disabling

### Database Configuration

Flow2API uses SQLite by default. The database is created automatically:

- Location: `data/flow2api.db`
- Type: SQLite 3
- Migration: Automatic on startup

### Environment Variables

Override configuration with environment variables:

```bash
# API Configuration
export FLOW2API_API_KEY="your-secret-key"
export FLOW2API_ADMIN_PASSWORD="secure-password"

# Server Configuration
export FLOW2API_HOST="0.0.0.0"
export FLOW2API_PORT="8000"

# Debug Configuration
export FLOW2API_DEBUG="true"
```

## 🔄 Configuration Reload

Flow2API supports hot-reloading of certain configurations:

### Through Web Interface
1. Login to admin panel
2. Navigate to Settings
3. Modify configuration
4. Click "Save & Apply"

### Through API
```bash
curl -X POST http://localhost:8000/admin/reload-config \
  -H "Authorization: Bearer your-api-key"
```

### What Can Be Reloaded
- ✅ Token settings
- ✅ Cache configuration
- ✅ Debug settings
- ✅ Generation timeouts
- ❌ Server host/port (requires restart)
- ❌ Database settings (requires restart)

## 📊 Performance Tuning

### Optimizing for Image Generation

```toml
[generation]
image_timeout = 180        # Reduce timeout for faster failures

[flow]
poll_interval = 2.0        # Faster polling for images
max_poll_attempts = 100    # Fewer attempts for images
```

### Optimizing for Video Generation

```toml
[generation]
video_timeout = 1200       # Longer timeout for videos

[flow]
poll_interval = 5.0        # Slower polling for videos
max_poll_attempts = 300    # More attempts for videos
```

### Memory Optimization

```toml
[cache]
enabled = false            # Disable caching to save memory

# Or reduce cache timeout
[cache]
timeout = 3600             # 1 hour instead of 2
```

## 🔍 Monitoring Configuration

### Key Metrics to Monitor

1. **Token Health**
   - Error rates per token
   - Concurrency usage
   - Balance/credits remaining

2. **System Performance**
   - Response times
   - Queue lengths
   - Memory usage

3. **Generation Stats**
   - Success/failure rates
   - Average generation time
   - Cache hit rates

### Setting Up Alerts

Configure alerts for:
- Token errors exceeding threshold
- High response times
- Low token balances
- System resource exhaustion

## 🛡️ Security Configuration

### Production Security Checklist

```toml
# Change all defaults
[global]
api_key = "complex-random-string-123!@#"
admin_username = "not-admin"
admin_password = "very-secure-password-456$%"

[server]
host = "127.0.0.1"  # Bind to localhost only
port = 8000         # Use non-default port
```

### Additional Security Measures

1. **Use HTTPS**: Set up reverse proxy with SSL
2. **Rate Limiting**: Implement rate limiting at proxy level
3. **IP Whitelisting**: Restrict access by IP address
4. **Regular Updates**: Keep dependencies updated

## 🔄 Migration from Other Systems

### From OpenAI API

Flow2API is designed to be compatible with OpenAI's API:

1. Replace `api.openai.com` with your Flow2API server
2. Update the API key
3. Use compatible model names
4. Most existing code should work without changes

### From Other VideoFX Proxies

1. Export your token list
2. Add tokens through Flow2API interface
3. Update your application endpoints
4. Test with a few requests first

## 📚 Configuration Examples

### Development Environment

```toml
[global]
api_key = "dev-key-123"
admin_username = "dev"
admin_password = "dev-pass"

[debug]
enabled = true
log_requests = true
log_responses = true

[cache]
enabled = false
```

### Production Environment

```toml
[global]
api_key = "prod-key-very-secure-456!@#"
admin_username = "admin-prod"
admin_password = "prod-password-789$%"

[server]
host = "0.0.0.0"
port = 8080

[debug]
enabled = false

[cache]
enabled = true
timeout = 3600
base_url = "https://cdn.yourdomain.com"

[proxy]
proxy_enabled = true
proxy_url = "http://proxy.yourcompany.com:8080"
```

### High-Performance Setup

```toml
[flow]
timeout = 60
poll_interval = 1.0
max_poll_attempts = 50

[generation]
image_timeout = 120
video_timeout = 600

[admin]
error_ban_threshold = 5
```

---

**Next Steps**: After configuration, learn about development practices in the [Development Guide](./DEVELOPMENT.md). For deployment strategies, see the [Deployment Guide](./DEPLOYMENT.md). For issues, check the [Troubleshooting Guide](./TROUBLESHOOTING.md)."""""","file_path":"F:/CodeBase/flow2api/docs/CONFIGURATION.md"}