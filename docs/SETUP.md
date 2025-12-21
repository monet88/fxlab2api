# Flow2API Setup and Installation Guide

## 🎯 Overview

This guide will walk you through setting up Flow2API on your system. We provide multiple installation methods to suit different environments and preferences.

## 📋 Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Memory**: Minimum 2GB RAM (4GB+ recommended for production)
- **Storage**: At least 5GB free space
- **Network**: Stable internet connection for downloading dependencies

### Software Requirements

#### Option 1: Docker (Recommended)
- Docker Engine 20.10+
- Docker Compose 2.0+

#### Option 2: Local Python Installation
- Python 3.8 or higher
- pip package manager
- Virtual environment support

## 🚀 Installation Methods

### Method 1: Docker Installation (Recommended)

Docker provides the easiest and most consistent installation experience.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api
```

#### Step 2: Choose Your Deployment Mode

##### Standard Mode (No Proxy)

For environments with direct internet access:

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

##### WARP Mode (With Proxy)

For environments requiring proxy support:

```bash
# Start with WARP proxy
docker-compose -f docker-compose.proxy.yml up -d

# View logs
docker-compose -f docker-compose.proxy.yml logs -f
```

#### Step 3: Verify Installation

Check if the service is running:

```bash
# Check container status
docker ps

# Test the API endpoint
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer han1234"
```

#### Step 4: Access the Web Interface

Open your browser and navigate to:
- **URL**: http://localhost:8000
- **Username**: admin
- **Password**: admin

⚠️ **Important**: Change the default password immediately after first login!

### Method 2: Local Python Installation

For developers who prefer local installation or need to customize the code.

#### Step 1: Install Python

Ensure Python 3.8+ is installed:

```bash
# Check Python version
python --version

# If Python is not installed, download from:
# https://www.python.org/downloads/
```

#### Step 2: Clone the Repository

```bash
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

#### Step 5: Configure the Application

Edit the configuration file:

```bash
# Copy example configuration (if needed)
cp config/setting.toml.example config/setting.toml

# Edit configuration
nano config/setting.toml
```

#### Step 6: Start the Service

```bash
# Run the application
python main.py
```

## 🔧 Configuration

### Basic Configuration

Edit `config/setting.toml` to customize your setup:

```toml
[global]
api_key = "your-secret-api-key"  # Change this!
admin_username = "admin"
admin_password = "your-secure-password"  # Change this!

[server]
host = "0.0.0.0"
port = 8000

[flow]
# Google API endpoints
labs_base_url = "https://labs.google/fx/api"
api_base_url = "https://aisandbox-pa.googleapis.com/v1"
```

### Proxy Configuration (Optional)

If you need to use a proxy:

```toml
[proxy]
proxy_enabled = true
proxy_url = "http://your-proxy-server:port"
```

### Cache Configuration (Optional)

To enable file caching:

```toml
[cache]
enabled = true
timeout = 7200  # 2 hours
base_url = "https://your-domain.com"  # Optional
```

## 🧪 Testing Your Installation

### Test API Access

```bash
# List available models
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer your-api-key"

# Test image generation
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "A beautiful sunset"}],
    "stream": true
  }'
```

### Test Web Interface

1. Open http://localhost:8000 in your browser
2. Login with your admin credentials
3. Navigate to the management dashboard
4. Verify that you can view and manage tokens

## 📁 Directory Structure

After installation, your Flow2API directory structure should look like:

```
flow2api/
├── config/                    # Configuration files
│   ├── setting.toml          # Main configuration
│   └── setting_warp.toml     # WARP proxy configuration
├── src/                      # Source code
│   ├── api/                  # API routes
│   ├── core/                 # Core functionality
│   └── services/             # Business logic
├── static/                   # Web interface files
│   ├── login.html           # Login page
│   └── manage.html          # Management dashboard
├── tmp/                     # Cache directory (created automatically)
├── docs/                    # Documentation
├── docker-compose.yml       # Docker configuration
├── requirements.txt         # Python dependencies
└── main.py                  # Entry point
```

## 🔒 Security Considerations

### Immediate Actions

1. **Change Default Credentials**: Update admin username and password
2. **Change API Key**: Use a strong, unique API key
3. **Configure Firewall**: Restrict access to necessary ports only
4. **Use HTTPS**: Set up SSL/TLS for production deployments

### Production Deployment

1. **Use Environment Variables**: Store sensitive data in environment variables
2. **Regular Updates**: Keep the application and dependencies updated
3. **Monitoring**: Set up logging and monitoring
4. **Backup**: Regularly backup your database and configuration

## 🐳 Docker Commands Reference

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart

# Update to latest version
git pull
docker-compose pull
docker-compose up -d
```

### Advanced Operations

```bash
# Rebuild containers
docker-compose build --no-cache

# Run with specific configuration
docker-compose -f docker-compose.proxy.yml up -d

# Access container shell
docker-compose exec flow2api bash

# View container stats
docker stats
```

## 🐛 Troubleshooting Installation

### Docker Issues

#### Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

#### Permission Issues
```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
# Log out and back in
```

#### Container Won't Start
```bash
# Check logs
docker-compose logs flow2api

# Rebuild container
docker-compose build --no-cache
```

### Python Issues

#### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Port Access Denied
```bash
# Use a different port
# Edit config/setting.toml and change port number
```

#### Database Errors
```bash
# Delete database and restart
rm data/flow2api.db
python main.py
```

## 🔄 Next Steps

After successful installation:

1. **Add Tokens**: Learn how to add Google session tokens in the [Configuration Guide](./CONFIGURATION.md)
2. **Configure Models**: Set up model-specific settings
3. **Set Up Proxy**: If needed, configure proxy settings
4. **Monitor Usage**: Use the web interface to monitor token usage
5. **Scale Up**: Learn about load balancing and concurrency in the [Architecture Guide](./ARCHITECTURE.md)

## 📞 Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
2. Review Docker and application logs
3. Search existing issues on GitHub
4. Create a new issue with detailed error information

---

**Next Step**: Once installed, proceed to the [Configuration Guide](./CONFIGURATION.md) to set up your tokens and customize the service.