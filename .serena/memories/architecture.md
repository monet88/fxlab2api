# Flow2API Architecture Overview

## Project Purpose
Flow2API is a middleware service that provides an OpenAI-compatible API interface for Google's VideoFX (Veo) platform. It bridges Google's AI generation services with developers through a standardized API for image and video generation.

## System Architecture

### Component Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                      │
├─────────────────────────────────────────────────────────────┤
│              OpenAI-Compatible API Endpoints                │
│  (src/api/routes.py - /v1/models, /v1/chat/completions)   │
├─────────────────────────────────────────────────────────────┤
│                  Generation Handler                         │
│         (src/services/generation_handler.py)                │
├─────────────────────────────────────────────────────────────┤
│      Load Balancer      │      Concurrency Manager        │
│  (Multi-token selection)│  (Per-token request limits)    │
├─────────────────────────────────────────────────────────────┤
│                    Token Manager                            │
│         (ST/AT token lifecycle management)                  │
├─────────────────────────────────────────────────────────────┤
│                    Flow Client                              │
│           (Google Labs API wrapper)                        │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. FastAPI Application (src/main.py)
- Entry point with lifespan management
- Dependency injection setup
- Static file serving for admin panel
- Router mounting

#### 2. API Layer (src/api/)
- **routes.py**: OpenAI-compatible endpoints
  - GET /v1/models - List available models
  - POST /v1/chat/completions - Generate content (streaming)
- **admin.py**: Web management interface endpoints

#### 3. Service Layer (src/services/)
- **FlowClient**: Direct Google Labs API communication
- **TokenManager**: ST/AT token management with auto-refresh
- **LoadBalancer**: Intelligent token selection
- **GenerationHandler**: Request orchestration
- **ConcurrencyManager**: Rate limiting per token
- **ProxyManager**: HTTP/SOCKS5 proxy support
- **FileCache**: Optional local file caching

#### 4. Core Layer (src/core/)
- **config.py**: TOML-based configuration management
- **database.py**: SQLite with async operations
- **auth.py**: Bearer token authentication
- **models.py**: Pydantic data models
- **logger.py**: Logging configuration

### Request Flow

1. **Client Request** → OpenAI-compatible endpoint
2. **Router** validates and forwards to GenerationHandler
3. **LoadBalancer** selects appropriate token
4. **ConcurrencyManager** checks rate limits
5. **TokenManager** ensures token validity (auto-refresh if needed)
6. **FlowClient** makes API call to Google Labs
7. **Response Streaming** back to client

### Token System

Google's Token System (NOT JWT):
- **ST (Session Token)**: Cookie-based authentication
- **AT (Access Token)**: Bearer token for API calls
- **Auto-refresh**: 1 hour before AT expiry
- **Error handling**: Tokens auto-disable after N consecutive errors

### Configuration System

- **Primary**: `config/setting.toml` (TOML format)
- **Runtime**: Admin panel with hot-reload support
- **Dynamic**: Database-backed for some settings
- **Structure**:
```toml
[global]
api_key = "han1234"
admin_username = "admin"
admin_password = "admin"

[flow]
labs_base_url = "https://labs.google/fx/api"
api_base_url = "https://aisandbox-pa.googleapis.com/v1"
timeout = 120
poll_interval = 3.0

[server]
host = "0.0.0.0"
port = 8000
```

### Supported Models

**Image Generation:**
- gemini-2.5-flash-image-landscape/portrait
- gemini-3.0-pro-image-landscape/portrait  
- imagen-4.0-generate-preview-landscape/portrait

**Video Generation:**
- Text-to-Video (T2V): veo_3_1_t2v_fast, veo_2_1_fast_d_15, veo_2_0
- Image-to-Video (I2V - First/Last Frame): veo_3_1_i2v_s_fast_fl, veo_2_1_fast_d_15, veo_2_0
- Multi-image (R2V): veo_3_0_r2v_fast

### Data Storage

- **SQLite Database**: `data/flow2api.db`
- **Tables**:
  - tokens (token management)
  - settings (runtime configuration)
  - usage_stats (generation statistics)
- **Automatic migrations** on startup

### Security Features

- Bearer token authentication for API
- Bcrypt password hashing for admin
- Token masking in logs (configurable)
- CORS support for web clients
- No sensitive data in version control

### Deployment Options

1. **Docker** (recommended):
   - Standard: `docker-compose up -d`
   - WARP proxy: `docker-compose -f docker-compose.warp.yml up -d`

2. **Local Development**:
   - Virtual environment
   - Direct Python execution: `python main.py`

### Performance Features

- Async/await throughout
- Connection pooling
- Request queuing
- Multi-token load balancing
- File caching system (optional)
- Concurrency limits per token
- Streaming responses

### Monitoring & Debugging

- Debug mode with request/response logging
- Token status tracking
- Error thresholds with auto-disable
- Admin panel for real-time monitoring
- Log files for troubleshooting
