# Flow2API System Architecture

> Last Updated: 2025-12-22
> Version: 1.0.0

## Overview

Flow2API is built on a modular, layered architecture designed for maintainability, scalability, and high performance. The system uses Python's FastAPI framework with full async/await support.

---

## High-Level Architecture

```
                                    EXTERNAL
                                    --------
                                         |
                              +----------+----------+
                              |   Google VideoFX   |
                              |      Platform      |
                              +----------+----------+
                                         ^
                                         | HTTPS
                                         |
+------------------------+    +----------+----------+    +------------------+
|    Client Layer        |    |    Flow2API        |    |   Data Layer     |
|------------------------|    |    Server          |    |------------------|
| - Web Browser          |    |                    |    | - SQLite DB      |
| - API Clients          |--->|  FastAPI App       |--->| - File Cache     |
| - CLI Tools            |    |  (Async)           |    | - Config Files   |
+------------------------+    +--------------------+    +------------------+
        |                              |
        |       HTTP/HTTPS             |
        +------------------------------+
```

---

## Layered Architecture

### Layer Diagram

```
+------------------------------------------------------------------+
|                       CLIENT LAYER                                |
|   Web Browser    |    API Clients    |    Command Line Tools     |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                    FASTAPI APPLICATION LAYER                      |
|------------------------------------------------------------------|
|  API Routes       |   Admin Routes    |   Static File Serving    |
|  (/v1/*)          |   (/admin/*)      |   (Login/Management UI)  |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                    SERVICE LAYER (Business Logic)                 |
|------------------------------------------------------------------|
| Generation        | Token Manager     | Load Balancer            |
| Handler           |                   |                          |
|------------------------------------------------------------------|
| Flow Client       | Concurrency       | File Cache               |
| (API Wrapper)     | Manager           |                          |
|------------------------------------------------------------------|
| Proxy Manager     | Authentication    | Request Logger           |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                    DATA ACCESS LAYER                              |
|------------------------------------------------------------------|
|   Database        |   Configuration   |   Token Management       |
|   (SQLite)        |   Manager         |   Operations             |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                    EXTERNAL SERVICES LAYER                        |
|------------------------------------------------------------------|
| Google VideoFX    |   Proxy Servers   |   File System (Cache)    |
|   APIs            |   (HTTP/SOCKS5)   |                          |
+------------------------------------------------------------------+
```

---

## Core Components

### 1. Application Layer (`src/main.py`)

The main FastAPI application that orchestrates all components.

**Responsibilities:**
- Initialize all service components
- Configure middleware (CORS, static files)
- Set up routing
- Manage application lifecycle (startup/shutdown)

**Key Features:**
- Async lifespan management for clean startup/shutdown
- Automatic database migration on startup
- Static file serving for web UI and cached content
- CORS configuration for cross-origin requests

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services
    database = Database()
    await database.initialize()
    # ... more initialization

    yield

    # Shutdown: Cleanup
    await database.close()
```

### 2. API Routes (`src/api/routes.py`)

OpenAI-compatible API endpoints.

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/models` | List available models |
| POST | `/v1/chat/completions` | Unified generation endpoint |

**Features:**
- Full OpenAI API compatibility
- Multimodal input support (text + images)
- Streaming and non-streaming responses
- Comprehensive error handling

### 3. Admin Routes (`src/api/admin.py`)

Administrative endpoints for management.

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/admin/login` | Admin authentication |
| GET | `/admin/tokens` | List all tokens |
| POST | `/admin/tokens` | Add new token |
| PUT | `/admin/tokens/{id}` | Update token |
| DELETE | `/admin/tokens/{id}` | Delete token |
| GET | `/admin/stats` | Get statistics |
| GET/PUT | `/admin/config/*` | Configuration management |

---

## Service Layer Components

### Generation Handler (`src/services/generation_handler.py`)

The core orchestrator for all generation requests.

**Responsibilities:**
- Model validation and configuration
- Token selection via load balancer
- AT token validation and refresh
- Project management
- Concurrency control
- Response formatting (streaming/non-streaming)
- Error handling and recovery

```
Request Flow:
1. Validate model and parameters
2. Select token via LoadBalancer
3. Validate/refresh AT via TokenManager
4. Acquire concurrency slot
5. Call FlowClient for generation
6. Format and stream response
7. Release concurrency slot
8. Record usage statistics
```

### Token Manager (`src/services/token_manager.py`)

Manages the complete token lifecycle.

**Responsibilities:**
- ST to AT conversion
- Proactive AT refresh (1 hour before expiry)
- Token health monitoring
- Usage statistics tracking
- Error-based auto-disabling

**Token State Machine:**
```
                +--------+
                | ACTIVE |<----+
                +--------+     |
                    |          |
            error   |          | refresh/recovery
                    v          |
                +--------+     |
                | ERROR  |-----+
                +--------+
                    |
            threshold exceeded
                    v
                +---------+
                | DISABLED|
                +---------+
```

### Load Balancer (`src/services/load_balancer.py`)

Intelligent token selection.

**Selection Criteria:**
1. Token is active and healthy
2. Token supports required generation type (image/video)
3. Token supports required model (e.g., Gemini 3.0 needs paid accounts)
4. Token has available concurrency slots
5. Random selection from qualified pool

### Flow Client (`src/services/flow_client.py`)

Google VideoFX API wrapper.

**API Operations:**
- `st_to_at()` - Convert session to access token
- `generate_image()` - Synchronous image generation
- `generate_video_*()` - Various video generation methods
- `check_video_status()` - Poll for video completion
- `upload_image()` - Image upload for reference

**Features:**
- Unified request handling with retry logic
- Automatic proxy rotation
- Comprehensive error handling
- Request/response logging

### Concurrency Manager (`src/services/concurrency_manager.py`)

Prevents overloading tokens.

**Pattern:**
```python
# Acquire before generation
await concurrency_manager.acquire_image(token_id)
try:
    result = await generate()
finally:
    # Always release after
    await concurrency_manager.release_image(token_id)
```

**Limits:**
- Per-token limits for image and video separately
- -1 = unlimited, 0 = disabled
- Configurable per token

### File Cache (`src/services/file_cache.py`)

Optional caching system.

**Features:**
- Download and cache generated media locally
- Configurable TTL (default: 2 hours)
- Automatic cleanup of expired files
- Custom base URL support for CDN

### Proxy Manager (`src/services/proxy_manager.py`)

Proxy configuration and routing.

**Supported Formats:**
- HTTP: `http://host:port`
- HTTP with auth: `http://user:pass@host:port`
- SOCKS5: `socks5://host:port`
- SOCKS5 with auth: `socks5://user:pass@host:port`

---

## Core Layer Components

### Configuration (`src/core/config.py`)

Centralized configuration management.

**Sources (priority order):**
1. Environment variables
2. Database-backed settings
3. TOML configuration file

**Hot-Reload Support:**
- Token settings
- Cache configuration
- Debug settings
- Generation timeouts

**Requires Restart:**
- Server host/port
- Database settings

### Database (`src/core/database.py`)

SQLite database operations.

**Tables:**
| Table | Purpose |
|-------|---------|
| `tokens` | Token storage and management |
| `token_stats` | Usage statistics per token |
| `projects` | VideoFX project tracking |
| `tasks` | Generation task status |
| `request_logs` | API request logging |
| `admin_config` | Admin settings |
| `proxy_config` | Proxy configuration |
| `cache_config` | Cache settings |
| `generation_config` | Timeout settings |
| `debug_config` | Debug settings |

**Features:**
- Automatic schema migration on startup
- Async operations with aiosqlite
- Transaction support

### Models (`src/core/models.py`)

Pydantic data models for type safety.

**Key Models:**
- `Token` - Token information
- `Project` - VideoFX project data
- `Task` - Generation task
- `TokenStats` - Usage statistics
- `ChatCompletionRequest` - OpenAI-compatible request
- Various config models

### Authentication (`src/core/auth.py`)

API and admin authentication.

**Methods:**
- API key verification (Bearer token)
- Admin password verification (bcrypt hashed)

### Logger (`src/core/logger.py`)

Debug and request logging.

**Features:**
- Request/response logging
- Token masking for security
- Configurable log levels
- File-based debug logs

---

## Data Flow

### Image Generation Flow

```
1. Client Request
   POST /v1/chat/completions
   {model: "gemini-2.5-flash-image-*", messages: [...]}

2. API Routes
   - Validate request
   - Extract model and messages

3. Generation Handler
   - Validate model type (image)
   - Select token via LoadBalancer

4. Token Manager
   - Validate AT token
   - Refresh if expiring soon

5. Concurrency Manager
   - Acquire image slot

6. Flow Client
   - Upload input images (if any)
   - Call generate_image()
   - Return image URL

7. Generation Handler
   - Format response (markdown image)
   - Stream to client

8. Cleanup
   - Release concurrency slot
   - Record usage statistics
```

### Video Generation Flow

```
1. Client Request
   POST /v1/chat/completions
   {model: "veo_*", messages: [...]}

2. API Routes
   - Validate request
   - Extract model and messages

3. Generation Handler
   - Validate model type (video)
   - Validate image count for model type
   - Select token via LoadBalancer

4. Token Manager
   - Validate AT token
   - Ensure project exists

5. Concurrency Manager
   - Acquire video slot

6. Flow Client
   - Upload images (if any)
   - Call appropriate video generation method
   - Create task in database

7. Polling Loop
   - Check video status periodically
   - Stream progress updates to client

8. Completion
   - Return video URL
   - Release concurrency slot
   - Record usage statistics
```

---

## Database Schema

### Tokens Table

```sql
CREATE TABLE tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    st TEXT NOT NULL UNIQUE,
    at TEXT,
    at_expires TIMESTAMP,
    email TEXT NOT NULL,
    name TEXT,
    remark TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    use_count INTEGER DEFAULT 0,
    credits INTEGER DEFAULT 0,
    user_paygate_tier TEXT,
    current_project_id TEXT,
    current_project_name TEXT,
    image_enabled BOOLEAN DEFAULT 1,
    video_enabled BOOLEAN DEFAULT 1,
    image_concurrency INTEGER DEFAULT -1,
    video_concurrency INTEGER DEFAULT -1
);
```

### Token Statistics Table

```sql
CREATE TABLE token_stats (
    token_id INTEGER PRIMARY KEY,
    image_count INTEGER DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    last_success_at TIMESTAMP,
    last_error_at TIMESTAMP,
    today_image_count INTEGER DEFAULT 0,
    today_video_count INTEGER DEFAULT 0,
    today_error_count INTEGER DEFAULT 0,
    today_date TEXT,
    consecutive_error_count INTEGER DEFAULT 0,
    FOREIGN KEY (token_id) REFERENCES tokens(id)
);
```

---

## Security Architecture

### Authentication Flow

```
Client Request
      |
      v
+------------------+
| API Key Check    |---> Invalid: 401 Unauthorized
+------------------+
      |
      | Valid
      v
+------------------+
| Process Request  |
+------------------+
```

### Token Security

1. **Session Tokens (ST)**: Stored in database, never exposed via API
2. **Access Tokens (AT)**: Derived from ST, short-lived, auto-refreshed
3. **Masking**: Tokens are masked in logs (`abc...xyz`)
4. **Database**: File-based SQLite (no network exposure)

### Admin Authentication

1. Password stored as bcrypt hash
2. Session-based authentication for web UI
3. Bearer token for API access

---

## Performance Architecture

### Async Design

```
                 +----------------+
                 |   FastAPI      |
                 |   (uvicorn)    |
                 +-------+--------+
                         |
           +-------------+-------------+
           |             |             |
           v             v             v
    +------+------+ +----+----+ +------+------+
    | HTTP Client | | Database | | File I/O   |
    | (curl-cffi) | | (aiosql) | | (aiofiles) |
    +-------------+ +----------+ +-------------+
           |             |             |
           +---------+---+-------------+
                     |
                     v
              All async/await
              (no blocking)
```

### Concurrency Model

- **Single Process**: uvicorn with async workers
- **Per-Token Limits**: Prevent overloading accounts
- **Connection Pooling**: HTTP client reuses connections

### Caching Strategy

```
Request
    |
    v
+--------+
| Cache  |---> Hit: Return cached file
| Check  |
+--------+
    |
    | Miss
    v
+--------+
| Fetch  |
| Media  |
+--------+
    |
    v
+--------+
| Cache  |
| Store  |
+--------+
    |
    v
Return to client
```

---

## Deployment Architecture

### Docker Deployment

```
+---------------------+
|   Flow2API          |
|   Container         |
|---------------------|
|   Python 3.11       |
|   FastAPI           |
|   uvicorn           |
+---------------------+
        |
        | Volumes
        v
+-------+-------+
|    data/      |  <- SQLite DB
+---------------+
|    config/    |  <- TOML config
+---------------+
|    tmp/       |  <- Cache files
+---------------+
```

### WARP Proxy Mode

```
+----------------+        +----------------+
|   Flow2API     |------->|   WARP         |
|   Container    |  proxy |   Container    |
+----------------+        +----------------+
                                  |
                                  | Cloudflare
                                  v
                          +----------------+
                          | Google VideoFX |
                          +----------------+
```

---

## Extensibility Points

### Adding New Models

1. Update `MODEL_CONFIG` in `generation_handler.py`
2. Add model-specific logic if needed
3. Update API documentation

### Custom Authentication

1. Implement new auth provider in `auth.py`
2. Add configuration options in `config.py`
3. Update admin interface

### New Generation Types

1. Extend `GenerationHandler` with new methods
2. Add model configurations
3. Implement client methods in `FlowClient`

---

## Monitoring Points

### Health Check Endpoints

- `GET /health` - Basic health check (future)
- `GET /admin/stats` - Detailed statistics

### Key Metrics

| Metric | Description |
|--------|-------------|
| Token count | Active/inactive tokens |
| Generation count | Images/videos generated |
| Error rate | Errors per token |
| Response time | API latency |
| Cache hit rate | Cache effectiveness |

---

*This architecture document should be updated as the system evolves.*
