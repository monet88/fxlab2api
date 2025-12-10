# 📚 Flow2API Documentation

> A comprehensive guide for understanding, developing, and deploying Flow2API

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [API Reference](#api-reference)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Development Guide](#development-guide)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**Flow2API** is a full-featured OpenAI-compatible API service that provides a unified interface for Google's Flow (Labs) services, specifically focused on AI-generated content including images and videos.

### ✨ Key Features

- **🎨 Text-to-Image Generation**: Convert text descriptions to images
- **🎬 Text-to-Video Generation**: Create videos from text descriptions
- **🎞️ Image-to-Video Generation**: Transform images into videos
- **🔄 Automatic Token Refresh**: Handles token expiration automatically
- **📊 Credit Balance Display**: Real-time credit monitoring
- **🚀 Load Balancing**: Multi-token support with intelligent distribution
- **🌐 Proxy Support**: HTTP/SOCKS5 proxy compatibility
- **📱 Web Management Interface**: User-friendly admin panel

### 🏗️ Technology Stack

```
Backend: Python 3.8+ with FastAPI 0.119.0
Database: SQLite with aiosqlite
Authentication: Bearer token with bcrypt
HTTP Client: curl-cffi for enhanced requests
Deployment: Docker & Docker Compose
```

---

## 🏗️ Architecture

### 📁 Project Structure

```
flow2api/
├── src/                          # Main source code
│   ├── api/                      # API endpoints
│   │   ├── routes.py            # OpenAI-compatible endpoints
│   │   └── admin.py             # Admin panel APIs
│   ├── core/                     # Core functionality
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database operations
│   │   ├── auth.py              # Authentication logic
│   │   └── models.py            # Data models
│   └── services/                 # Business logic
│       ├── flow_client.py       # Flow Labs API client
│       ├── token_manager.py     # Token lifecycle management
│       ├── load_balancer.py     # Load balancing logic
│       └── generation_handler.py # Content generation orchestration
├── static/                       # Web UI (HTML/CSS/JS)
├── config/                       # Configuration files
└── main.py                       # Application entry point
```

### 🔗 Data Flow

```
Client Request → API Router → Generation Handler → Token Manager → Flow Client → Response
                    ↓
              Load Balancer → Best Token Selection
```

### 💾 Database Schema

Key tables:
- **tokens**: Stores API tokens with metadata
- **admin_config**: Admin user configuration
- **generation_logs**: Request/response logging

---

## 📡 API Reference

### Authentication

All API requests require a Bearer token in the Authorization header:
```
Authorization: Bearer your-api-token
```

### Endpoints

#### 1. List Available Models
```http
GET /v1/models
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "gemini-2.5-flash-image-landscape",
      "object": "model",
      "owned_by": "flow2api",
      "description": "Image generation - gemini-2.5-flash-image-landscape"
    }
  ]
}
```

#### 2. Generate Content (Chat Completions)
```http
POST /v1/chat/completions
```

**Request Body:**
```json
{
  "model": "gemini-2.5-flash-image-landscape",
  "messages": [
    {
      "role": "user",
      "content": "A beautiful sunset over mountains"
    }
  ],
  "stream": true
}
```

**Response:** Streaming response with generated content

### Supported Models

#### Image Generation Models
- `gemini-2.5-flash-image-landscape`
- `gemini-2.5-flash-image-portrait`
- `gemini-3.0-pro-image-landscape`
- `imagen-4.0-generate-preview-landscape`

#### Video Generation Models
- `veo_3_1_t2v_fast_landscape` (Text-to-Video)
- `veo_3_1_i2v_s_fast_fl_landscape` (First/Last Frame)
- `veo_3_0_r2v_fast_landscape` (Multi-image Reference)

---

## 🚀 Installation Guide

### Prerequisites

- Python 3.8+ or Docker
- pip package manager
- Git

### Method 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Start with Docker
docker-compose up -d

# View logs
docker-compose logs -f
```

### Method 2: Local Installation

```bash
# Clone the repository
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

# Run the application
python main.py
```

### Access the Application

- **API Base URL**: http://localhost:8000
- **Admin Panel**: http://localhost:8000
- **Default Credentials**: admin/admin (change immediately!)

---

## ⚙️ Configuration

### Configuration File: `config/setting.toml`

```toml
[global]
server_host = "0.0.0.0"
server_port = 8000
admin_username = "admin"
admin_password = "admin"

[flow]
labs_base_url = "https://labs.google.com"
# Add your API tokens here
tokens = ["your-token-1", "your-token-2"]

[proxy]
# Optional proxy configuration
enabled = false
url = "http://proxy:port"
```

### Environment Variables

- `FLOW2API_CONFIG_PATH`: Custom config file path
- `FLOW2API_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

---

## 💻 Development Guide

### Setting Up Development Environment

1. Fork and clone the repository
2. Create a virtual environment
3. Install development dependencies
4. Configure your IDE/editor

### Code Structure

```python
# Example: Adding a new endpoint
@router.post("/v1/new-endpoint")
async def new_endpoint(request: RequestModel):
    # Your logic here
    pass
```

### Adding New Models

1. Update `MODEL_CONFIG` in `services/generation_handler.py`
2. Add model-specific logic if needed
3. Test the integration

### Testing

```bash
# Run basic tests
python -m pytest tests/

# Test specific module
python -m pytest tests/test_auth.py
```

---

## 🐳 Deployment

### Docker Deployment

The project includes pre-configured Docker files:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

### Docker Compose Services

```yaml
# docker-compose.yml
version: '3.8'
services:
  flow2api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
```

### Production Deployment

1. **Security Hardening**:
   - Change default admin credentials
   - Enable HTTPS with reverse proxy
   - Configure firewall rules

2. **Performance Optimization**:
   - Use production ASGI server
   - Enable connection pooling
   - Configure caching

3. **Monitoring**:
   - Set up logging aggregation
   - Monitor resource usage
   - Configure alerts

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Token Authentication Failed
```
Error: 401 Unauthorized
```
**Solution**: Check your API token in the admin panel

#### 2. Model Not Found
```
Error: Model 'model-name' not found
```
**Solution**: Verify the model name in the supported models list

#### 3. Generation Timeout
```
Error: Request timeout after 60s
```
**Solution**: Check proxy settings and network connectivity

#### 4. Database Locked
```
Error: database is locked
```
**Solution**: Restart the application, check file permissions

### Debug Mode

Enable debug mode for detailed logging:
```bash
export FLOW2API_LOG_LEVEL=DEBUG
python main.py
```

### Getting Help

- Check logs: `docker-compose logs -f`
- Review configuration: `config/setting.toml`
- Check GitHub Issues for known problems
- Create a new issue with detailed error information

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

**📚 Documentation Generated**: 2025-12-10
**📝 Version**: 1.0.0
**🔗 Project**: https://github.com/TheSmallHanCat/flow2api

---

*This documentation covers the essential aspects of Flow2API. For more detailed information about specific components, refer to the inline code comments and docstrings.*