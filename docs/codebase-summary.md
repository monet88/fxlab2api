# Flow2API Codebase Summary

> Last Updated: 2025-12-22
> Generated from: repomix-output.xml (39,618 tokens, 23 files)

## Overview

Flow2API is a middleware service providing an OpenAI-compatible API interface for Google's VideoFX (Veo) platform. It bridges Google's AI generation services with developers through a standardized API for image and video generation.

## Codebase Statistics

| Metric | Value |
|--------|-------|
| Total Files | 23 |
| Total Tokens | ~39,600 |
| Total Characters | ~194,000 |
| Primary Language | Python |
| Python Version | 3.11 (Docker) / 3.8+ (local) |
| Framework | FastAPI |

## Directory Structure

```
flow2api/
├── src/                          # Source code (~5,180 lines)
│   ├── main.py                   # Application entry point
│   ├── api/                      # API layer
│   │   ├── routes.py             # OpenAI-compatible endpoints
│   │   └── admin.py              # Admin management endpoints
│   ├── core/                     # Core infrastructure
│   │   ├── models.py             # Pydantic data models
│   │   ├── database.py           # SQLite database layer
│   │   ├── config.py             # TOML configuration
│   │   ├── auth.py               # Authentication manager
│   │   └── logger.py             # Debug logging
│   └── services/                 # Business logic
│       ├── flow_client.py        # Google VideoFX API client
│       ├── token_manager.py      # Token lifecycle management
│       ├── generation_handler.py # Generation orchestrator
│       ├── load_balancer.py      # Token selection
│       ├── concurrency_manager.py# Rate limiting
│       ├── proxy_manager.py      # Proxy configuration
│       └── file_cache.py         # Media caching
├── config/                       # Configuration files
│   ├── setting.toml              # Main configuration
│   └── setting_warp.toml         # WARP proxy mode config
├── static/                       # Web UI assets
│   ├── login.html                # Admin login page
│   ├── manage.html               # Admin dashboard
│   └── favicon.ico               # Favicon
├── data/                         # Runtime data (created on first run)
│   └── flow2api.db               # SQLite database
├── tmp/                          # Cache directory (optional)
├── docs/                         # Documentation
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Standard deployment
├── docker-compose.proxy.yml      # WARP proxy deployment
├── requirements.txt              # Python dependencies
└── main.py                       # Entry point wrapper
```

## Top Files by Complexity (Token Count)

| Rank | File | Tokens | Share |
|------|------|--------|-------|
| 1 | src/core/database.py | 8,811 | 22.2% |
| 2 | src/services/generation_handler.py | 6,615 | 16.7% |
| 3 | src/api/admin.py | 5,021 | 12.7% |
| 4 | src/services/flow_client.py | 4,035 | 10.2% |
| 5 | src/services/token_manager.py | 3,099 | 7.8% |

## Architecture Layers

### 1. Entry Point (`src/main.py`)

- FastAPI application initialization
- Lifespan management (startup/shutdown)
- CORS and static file middleware
- Route registration

### 2. API Layer (`src/api/`)

**routes.py** (~148 lines)
- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Unified generation endpoint (OpenAI-compatible)

**admin.py** (~720 lines)
- 30+ admin endpoints for token, config, and system management
- Token CRUD operations
- Configuration management
- Statistics and logging

### 3. Core Layer (`src/core/`)

**models.py** (~160 lines)
- Pydantic models: Token, Project, TokenStats, Task, RequestLog
- Configuration models for all settings
- Request/response schemas

**database.py** (~1,045 lines)
- SQLite with aiosqlite (async)
- Automatic schema migration on startup
- CRUD operations for tokens, stats, config
- Tables: tokens, projects, tasks, request_logs, admin_config, proxy_config, cache_config, generation_config, debug_config

**config.py** (~184 lines)
- TOML configuration loading
- Runtime configuration management
- Database-backed settings

**auth.py** (~40 lines)
- AuthManager class
- API key verification
- Admin password verification (bcrypt)

**logger.py** (~253 lines)
- Debug file logging
- Token masking for security
- Request/response logging

### 4. Service Layer (`src/services/`)

**flow_client.py** (~658 lines)
- Google VideoFX API client wrapper
- ST/AT token authentication
- Image generation (text-to-image, image-to-image)
- Video generation (T2V, I2V, R2V)
- Status polling for async operations

**token_manager.py** (~410 lines)
- Token lifecycle management
- Automatic AT refresh (1 hour before expiry)
- Usage tracking and statistics
- Error-based auto-disabling

**generation_handler.py** (~871 lines)
- Generation orchestrator for 34 models
- Model configuration and validation
- Request routing based on model type
- Streaming response generation
- Error handling and recovery

**load_balancer.py** (~96 lines)
- Random token selection with availability checks
- Model-specific filtering
- Concurrency-aware selection

**concurrency_manager.py** (~191 lines)
- Per-token rate limiting
- Separate limits for image/video
- Acquire/release pattern

**proxy_manager.py** (~26 lines)
- Proxy URL configuration wrapper
- HTTP/SOCKS5 support

**file_cache.py** (~200 lines)
- Local media caching
- Configurable TTL
- Auto-cleanup task

## Supported Models (34 Total)

### Image Models (6)
| Model ID | Type |
|----------|------|
| gemini-2.5-flash-image-landscape | Text/Image-to-Image |
| gemini-2.5-flash-image-portrait | Text/Image-to-Image |
| gemini-3.0-pro-image-landscape | Text/Image-to-Image |
| gemini-3.0-pro-image-portrait | Text/Image-to-Image |
| imagen-4.0-generate-preview-landscape | Text/Image-to-Image |
| imagen-4.0-generate-preview-portrait | Text/Image-to-Image |

### Video Models - Text-to-Video (6)
| Model ID | Type |
|----------|------|
| veo_3_1_t2v_fast_landscape | T2V |
| veo_3_1_t2v_fast_portrait | T2V |
| veo_2_1_fast_d_15_t2v_landscape | T2V |
| veo_2_1_fast_d_15_t2v_portrait | T2V |
| veo_2_0_t2v_landscape | T2V |
| veo_2_0_t2v_portrait | T2V |

### Video Models - Image-to-Video (6)
| Model ID | Images |
|----------|--------|
| veo_3_1_i2v_s_fast_fl_landscape | 1-2 (first/last frame) |
| veo_3_1_i2v_s_fast_fl_portrait | 1-2 (first/last frame) |
| veo_2_1_fast_d_15_i2v_landscape | 1-2 (first/last frame) |
| veo_2_1_fast_d_15_i2v_portrait | 1-2 (first/last frame) |
| veo_2_0_i2v_landscape | 1-2 (first/last frame) |
| veo_2_0_i2v_portrait | 1-2 (first/last frame) |

### Video Models - Reference-to-Video (2)
| Model ID | Images |
|----------|--------|
| veo_3_0_r2v_fast_landscape | Unlimited |
| veo_3_0_r2v_fast_portrait | Unlimited |

## Token System

Flow2API uses Google's token system (NOT JWT):

- **ST (Session Token)**: Google session cookie for authentication
- **AT (Access Token)**: Bearer token for API calls, auto-refreshed 1 hour before expiry

### Token Lifecycle

1. User adds ST via admin panel
2. System converts ST to AT automatically
3. AT used for all API calls
4. AT refreshed proactively before expiry
5. Errors tracked; token auto-disabled after threshold

## Dependencies

From `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.119.0 | Web framework |
| uvicorn | 0.32.1 | ASGI server |
| aiosqlite | 0.20.0 | Async SQLite |
| pydantic | 2.10.4 | Data validation |
| curl-cffi | latest | HTTP client with browser impersonation |
| tomli | 2.2.1 | TOML parsing |
| bcrypt | 4.2.1 | Password hashing |
| python-multipart | 0.0.20 | File uploads |
| python-dateutil | 2.8.2 | Date utilities |

## Configuration

Primary configuration: `config/setting.toml`

```toml
[global]
api_key = "..."              # API key for client authentication
admin_username = "admin"     # Admin panel username
admin_password = "admin"     # Admin panel password (bcrypt hashed)

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

## Docker Support

- **Dockerfile**: Python 3.11-slim base image
- **docker-compose.yml**: Standard deployment
- **docker-compose.proxy.yml**: WARP proxy mode with Cloudflare WARP

## Request Flow

```
Client Request
    |
    v
API Routes (/v1/chat/completions)
    |
    v
Generation Handler
    |-- Model Validation
    |-- Load Balancer (select token)
    |-- Token Manager (validate/refresh AT)
    |
    v
Flow Client (Google VideoFX API)
    |-- Image: Direct generation
    |-- Video: Create task + polling
    |
    v
Response Formatting (SSE streaming)
    |
    v
Client Response
```

## Key Design Decisions

1. **OpenAI Compatibility**: Uses familiar chat completions API format
2. **Async Throughout**: All I/O operations use async/await
3. **Token Abstraction**: Hides Google's ST/AT complexity from users
4. **Automatic Recovery**: Token refresh, error handling, auto-disable
5. **Streaming First**: SSE streaming for real-time progress updates
6. **Database-Backed Config**: Runtime configuration changes without restart

## Known Limitations

1. No test suite - manual testing required
2. SQLite only - no PostgreSQL/MySQL support
3. Single-instance - no distributed deployment support
4. No rate limiting at API level (only per-token concurrency)

---

*Generated by docs-manager subagent*
