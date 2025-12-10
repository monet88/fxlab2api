# Project Index: Flow2API

Generated: 2025-12-10 02:28:15

## 📁 Project Structure

```
flow2api/
├── .beads/                    # Beads workflow tracking
├── .serena/                   # Serena project config
├── config/                    # Configuration files
│   ├── setting.toml          # Main configuration
│   └── setting_warp.toml     # WARP proxy configuration
├── docs/                      # Documentation (generated)
├── src/                       # Source code
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   └── services/             # Business logic
├── static/                    # Web UI files
├── docker-compose.yml         # Docker configuration
├── main.py                    # Entry point
└── requirements.txt           # Python dependencies
```

## 🚀 Entry Points

- **CLI**: `main.py` - Application startup with uvicorn server
- **API**: `src/main.py` - FastAPI application initialization
- **Config**: `config/setting.toml` - Main configuration file

## 📦 Core Modules

### Module: API
- **Path**: `src/api/`
- **Files**:
  - `routes.py` - OpenAI-compatible endpoints (/v1/models, /v1/chat/completions)
  - `admin.py` - Admin panel endpoints
  - `__init__.py` - Module initialization
- **Purpose**: HTTP API interface for external clients

### Module: Core
- **Path**: `src/core/`
- **Files**:
  - `config.py` - Configuration management (TOML-based)
  - `database.py` - SQLite database operations
  - `auth.py` - Bearer token authentication
  - `models.py` - Pydantic data models
  - `logger.py` - Logging configuration
- **Purpose**: Core infrastructure and shared utilities

### Module: Services
- **Path**: `src/services/`
- **Files**:
  - `flow_client.py` - Google Labs API client wrapper
  - `token_manager.py` - Token lifecycle management
  - `load_balancer.py` - Multi-token load balancing
  - `generation_handler.py` - Content generation orchestration
  - `concurrency_manager.py` - Request concurrency control
  - `proxy_manager.py` - HTTP/SOCKS5 proxy support
  - `file_cache.py` - File caching system
- **Purpose**: Business logic and external service integration

## 🔧 Configuration

- `config/setting.toml` - Main configuration (server, auth, tokens)
- `config/setting_warp.toml` - WARP proxy configuration
- `docker-compose.yml` - Docker service definition
- `docker-compose.proxy.yml` - Proxy-enabled Docker setup

## 📚 Documentation

- `README.md` - Project overview and quick start
- `DOCUMENTATION.md` - Comprehensive documentation
- `docs/` - Generated documentation sections
  - `API.md` - API reference
  - `ARCHITECTURE.md` - System architecture
  - `CONFIGURATION.md` - Configuration guide
  - `DEPLOYMENT.md` - Deployment instructions
  - `DEVELOPMENT.md` - Development guide
  - `SETUP.md` - Installation guide
  - `TROUBLESHOOTING.md` - Common issues

## 🧪 Test Coverage

- **Unit Tests**: Not present (opportunity for improvement)
- **Integration Tests**: Not present
- **Manual Testing**: Via API endpoints and web UI

## 🔗 Key Dependencies

- **fastapi 0.119.0** - Web framework
- **uvicorn 0.32.1** - ASGI server
- **pydantic 2.10.4** - Data validation
- **aiosqlite 0.20.0** - Async SQLite
- **curl-cffi** - HTTP client with enhanced features
- **bcrypt 4.2.1** - Password hashing

## 📝 Quick Start

1. **Setup**:
   ```bash
   git clone https://github.com/TheSmallHanCat/flow2api.git
   cd flow2api
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up -d
   ```

3. **Access**:
   - API: http://localhost:8000/v1/
   - Admin: http://localhost:8000/
   - Login: admin/admin

4. **Test API**:
   ```bash
   curl -H "Authorization: Bearer your-token" \
        -H "Content-Type: application/json" \
        http://localhost:8000/v1/models
   ```

## 🎯 Key Features

- OpenAI-compatible API endpoints
- Text-to-Image generation
- Text-to-Video generation
- Image-to-Video generation
- Multi-token load balancing
- Automatic token refresh
- Web management interface
- Docker support

## 🔐 Security

- Bearer token authentication
- Bcrypt password hashing
- Configurable admin credentials
- Token-based API access

## 📊 Performance

- Async/await throughout
- Connection pooling
- Request queuing
- Load balancing across tokens
- File caching system

## 🚀 Next Steps

1. Add comprehensive test suite
2. Implement monitoring/metrics
3. Add rate limiting
4. Enhance error handling
5. Add more model support

---

**Index Last Updated**: 49 files, 20 Python files
**Languages**: Python, TOML, YAML, Markdown
**Framework**: FastAPI with async SQLite
