# Flow2API Architecture Documentation

## 🏗️ System Architecture Overview

Flow2API follows a modular, layered architecture designed for scalability, maintainability, and high performance. The system is built using Python's FastAPI framework with full async/await support.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
├─────────────────┬───────────────────┬───────────────────────────┤
│   Web Browser   │   API Clients     │   Command Line Tools      │
└─────────────────┴───────────────────┴───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application Layer                     │
├─────────────────┬───────────────────┬───────────────────────────┤
│   API Routes    │   Admin Routes    │   Static File Serving     │
│   (/v1/*)       │   (/admin/*)      │   (Login/Management UI)   │
└─────────────────┴───────────────────┴───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer (Business Logic)                │
├─────────────────┬───────────────────┬───────────────────────────┤
│ Generation      │ Token Manager     │ Load Balancer             │
│ Handler         │                   │                           │
├─────────────────┼───────────────────┼───────────────────────────┤
│ Flow Client     │ Concurrency       │ File Cache                │
│ (API Wrapper)   │ Manager           │                           │
├─────────────────┼───────────────────┼───────────────────────────┤
│ Proxy Manager   │ Authentication    │ Request Logger            │
└─────────────────┴───────────────────┴───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Access Layer                           │
├─────────────────┬───────────────────┬───────────────────────────┤
│   Database      │   Configuration   │   Token Management        │
│   (SQLite)      │   Manager         │   Operations              │
└─────────────────┴───────────────────┴───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   External Services Layer                        │
├─────────────────┬───────────────────┬───────────────────────────┤
│ Google VideoFX  │   Proxy Servers   │   File System (Cache)     │
│   APIs          │   (HTTP/SOCKS5)   │                           │
└─────────────────┴───────────────────┴───────────────────────────┘
```

## 🔧 Core Components

### 1. Application Layer (`src/main.py`)

The main FastAPI application that orchestrates all components:

```python
# Key responsibilities:
- Initialize all service components
- Configure middleware (CORS, static files)
- Set up routing
- Manage application lifecycle
```

**Key Features:**
- Async lifespan management for clean startup/shutdown
- Automatic database migration on startup
- Static file serving for web UI and cached content
- CORS configuration for cross-origin requests

### 2. API Routes (`src/api/routes.py`)

OpenAI-compatible API endpoints:

```python
# Main endpoints:
GET  /v1/models              # List available models
POST /v1/chat/completions   # Unified generation endpoint
```

**Features:**
- Full OpenAI API compatibility
- Multimodal input support (text + images)
- Streaming and non-streaming responses
- Comprehensive error handling

### 3. Admin Routes (`src/api/admin.py`)

Administrative endpoints for management:

```python
# Admin operations:
POST /admin/login           # Admin authentication
GET  /admin/tokens          # List all tokens
POST /admin/tokens          # Add new token
PUT  /admin/tokens/{id}     # Update token
DELETE /admin/tokens/{id}   # Delete token
GET  /admin/stats           # Get statistics
```

### 4. Service Layer Components

#### Generation Handler (`src/services/generation_handler.py`)

The core orchestrator for all generation requests:

```python
class GenerationHandler:
    # Key methods:
    - handle_generation()      # Main entry point
    - _handle_image_generation()   # Image-specific logic
    - _handle_video_generation()   # Video-specific logic
    - _poll_video_result()     # Async video polling
```

**Responsibilities:**
- Model validation and configuration
- Token selection via load balancer
- AT token validation and refresh
- Project management
- Concurrency control
- Response formatting (streaming/non-streaming)
- Error handling and recovery

#### Token Manager (`src/services/token_manager.py`)

Manages the complete token lifecycle:

```python
class TokenManager:
    # Core functions:
    - add_token()              # Add new token with project creation
    - is_at_valid()            # Check AT validity, auto-refresh if needed
    - _refresh_at()            # Internal AT refresh logic
    - record_usage()           # Track token usage statistics
    - record_error()           # Handle errors and auto-disable
```

**Key Features:**
- Automatic ST to AT conversion
- Proactive AT refresh (1 hour before expiry)
- Token health monitoring
- Usage statistics tracking
- Error-based auto-disabling

#### Load Balancer (`src/services/load_balancer.py`)

Intelligent token selection:

```python
class LoadBalancer:
    # Main method:
    - select_token()           # Choose optimal token for request
```

**Selection Criteria:**
- Token availability and health
- Generation type (image/video) support
- Model-specific requirements (e.g., Gemini 3.0 needs paid accounts)
- Concurrency limits
- Random selection from available pool

#### Flow Client (`src/services/flow_client.py`)

Google VideoFX API wrapper:

```python
class FlowClient:
    # Key methods:
    - st_to_at()               # Convert session to access token
    - generate_image()         # Synchronous image generation
    - generate_video_*()       # Various video generation methods
    - check_video_status()     # Poll for video completion
    - upload_image()           # Image upload for reference
```

**Features:**
- Unified request handling with retry logic
- Automatic proxy rotation
- Comprehensive error handling
- Request/response logging

#### Concurrency Manager (`src/services/concurrency_manager.py`)

Prevents overloading tokens:

```python
class ConcurrencyManager:
    # Key methods:
    - acquire_image()/release_image()
    - acquire_video()/release_video()
    - can_use_image()/can_use_video()
```

#### File Cache (`src/services/file_cache.py`)

Optional caching system:

```python
class FileCache:
    # Key methods:
    - download_and_cache()     # Cache remote files
    - start_cleanup_task()     # Periodic cleanup
```

#### Proxy Manager (`src/services/proxy_manager.py`)

Proxy configuration and rotation:

```python
class ProxyManager:
    # Key methods:
    - get_proxy_url()          # Get next available proxy
    - validate_proxy()         # Test proxy connectivity
```

### 5. Core Layer (`src/core/`)

#### Configuration (`src/core/config.py`)

Centralized configuration management:

```python
class Config:
    # Manages:
    - TOML file loading
    - Runtime configuration updates
    - Database-backed settings
```

#### Database (`src/core/database.py`)

SQLite database operations:

```python
class Database:
    # Tables:
    - tokens          # Token storage and management
    - projects        # VideoFX project tracking
    - tasks           # Generation task status
    - request_logs    # API request logging
    - admin_config    # Admin settings
    - proxy_config    # Proxy configuration
    - cache_config    # Cache settings
    - generation_config # Timeout settings
    - debug_config    # Debug settings
```

#### Models (`src/core/models.py`)

Pydantic data models for type safety:

```python
# Key models:
- Token              # Token information
- Project            # VideoFX project data
- Task               # Generation task
- ChatCompletionRequest  # OpenAI-compatible request
```

#### Authentication (`src/core/auth.py`)

API key authentication:

```python
# Functions:
- verify_api_key_header()   # Validate API key
- verify_admin_credentials() # Admin login verification
```

#### Logger (`src/core/logger.py`)

Debug and request logging:

```python
class DebugLogger:
    # Features:
    - Request/response logging
    - Token masking for security
    - Configurable log levels
```

## 🔄 Data Flow

### Image Generation Flow

```
1. Client Request → API Routes
2. Model Validation → Generation Handler
3. Token Selection → Load Balancer
4. AT Validation → Token Manager
5. Project Check → Token Manager
6. Image Upload (if needed) → Flow Client
7. Generation Request → Flow Client
8. Response Formatting → Generation Handler
9. Return to Client → API Routes
```

### Video Generation Flow

```
1. Client Request → API Routes
2. Model Validation → Generation Handler
3. Token Selection → Load Balancer
4. AT Validation → Token Manager
5. Project Check → Token Manager
6. Image Processing (upload if needed)
7. Video Generation Request → Flow Client
8. Task Creation → Database
9. Polling Loop → Flow Client
10. Response Streaming → Generation Handler
11. Return to Client → API Routes
```

## 🗄️ Database Schema

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
    consecutive_error_count INTEGER DEFAULT 0
);
```

## 🔒 Security Considerations

### Token Security
- Tokens are masked in logs when debug mode is enabled
- Database connections use file-based SQLite (no network exposure)
- API keys are hashed using bcrypt for admin authentication

### Request Security
- CORS configuration for cross-origin requests
- API key validation on all endpoints
- Rate limiting through concurrency controls

### Data Protection
- No sensitive data stored in plain text
- Automatic cleanup of old request logs
- Configurable data retention policies

## ⚡ Performance Optimizations

### Async Architecture
- All I/O operations are async
- Database operations use aiosqlite
- HTTP requests use curl-cffi with impersonation

### Caching Strategies
- Optional file caching for generated content
- In-memory concurrency tracking
- Database query optimization with indexes

### Resource Management
- Connection pooling for HTTP requests
- Automatic cleanup of temporary files
- Graceful shutdown handling

## 🧪 Testing Strategy

### Unit Testing
- Individual service component testing
- Mock external dependencies
- Test data validation

### Integration Testing
- End-to-end API flow testing
- Database operation verification
- Error handling validation

### Load Testing
- Concurrency limit validation
- Token rotation testing
- Performance benchmarking

## 🚀 Deployment Architecture

### Docker Deployment
```
┌─────────────────┐
│   Flow2API      │
│   Container     │
├─────────────────┤
│   SQLite DB     │
│   (Volume)      │
├─────────────────┤
│   Cache Files   │
│   (Volume)      │
└─────────────────┘
```

### Production Considerations
- Use external database for multi-instance deployments
- Implement proper backup strategies
- Monitor resource usage and performance
- Set up log aggregation and alerting

## 🔧 Extensibility

### Adding New Models
1. Update MODEL_CONFIG in generation_handler.py
2. Add model-specific logic if needed
3. Update API documentation

### Custom Authentication
- Implement new auth providers in auth.py
- Add configuration options in config.py
- Update admin interface for management

### New Generation Types
- Extend GenerationHandler with new methods
- Add model configurations
- Implement client methods in FlowClient

---

*This architecture provides a solid foundation for AI generation services while maintaining flexibility for future enhancements.*