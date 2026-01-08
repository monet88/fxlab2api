# Scout Report: src/ Directory Analysis

**Date:** 2025-12-22  
**Scope:** f:\CodeBase\flow2api\src\  
**Total Files:** 18 Python files  
**Total Lines:** ~5,180 (estimated)

---

## Directory Structure

src/
+-- main.py                        # Application entry point (176 lines)
+-- api/                           # API Layer
|   +-- __init__.py                # Exports: api_router, admin_router
|   +-- routes.py                  # OpenAI-compatible endpoints (148 lines)
|   +-- admin.py                   # Admin management endpoints (720 lines)
+-- core/                          # Core Infrastructure
|   +-- __init__.py                # Exports: config, AuthManager, debug_logger
|   +-- models.py                  # Pydantic data models (160 lines)
|   +-- database.py                # SQLite async layer (1,045 lines)
|   +-- config.py                  # TOML config management (184 lines)
|   +-- auth.py                    # Authentication (40 lines)
|   +-- logger.py                  # Debug file logging (253 lines)
+-- services/                      # Business Logic Layer
    +-- __init__.py                # Exports all service classes
    +-- flow_client.py             # Google VideoFX API client (658 lines)
    +-- token_manager.py           # Token lifecycle management (410 lines)
    +-- generation_handler.py      # Generation orchestrator (871 lines)
    +-- load_balancer.py           # Token selection (96 lines)
    +-- concurrency_manager.py     # Rate limiting (191 lines)
    +-- proxy_manager.py           # Proxy configuration (26 lines)
    +-- file_cache.py              # Media caching (200 lines)

---

## File Descriptions

### Entry Point
- src/main.py: FastAPI app init, lifespan management, dependency wiring, CORS, static files

### API Layer (src/api/)
- routes.py: OpenAI-compatible endpoints (GET /v1/models, POST /v1/chat/completions)
- admin.py: 30+ admin endpoints for token CRUD, config, stats, logging, cache control

### Core Layer (src/core/)
- models.py: Pydantic models (Token, Project, TokenStats, Task, RequestLog, configs)
- database.py: Async SQLite with aiosqlite, CRUD ops, schema migration
- config.py: TOML config + runtime updates, global config instance
- auth.py: AuthManager (verify_api_key, verify_admin, password hashing)
- logger.py: DebugLogger (file logging with token masking)

### Services Layer (src/services/)
- flow_client.py: Google VideoFX API wrapper (st_to_at, create_project, generate_image/video, check_status)
- token_manager.py: Token lifecycle, AT auto-refresh 1hr before expiry
- generation_handler.py: Generation orchestrator, MODEL_CONFIG (34 models)
- load_balancer.py: Random token selection with image/video filtering
- concurrency_manager.py: Per-token rate limiting (acquire/release slots)
- proxy_manager.py: Proxy config wrapper
- file_cache.py: Local media caching with TTL-based expiry

---

## Dependency Graph

main.py
+-- core/config (Config singleton)
+-- core/database (Database)
+-- services/proxy_manager <-- Database
+-- services/flow_client <-- ProxyManager
+-- services/token_manager <-- Database, FlowClient
+-- services/concurrency_manager
+-- services/load_balancer <-- TokenManager, ConcurrencyManager
+-- services/generation_handler <-- FlowClient, TokenManager, LoadBalancer, Database, ConcurrencyManager, ProxyManager
|   +-- services/file_cache <-- ProxyManager
+-- api/routes, api/admin (routers)

---

## Key Architectural Patterns

1. Service-Oriented Architecture: API -> Services -> Core
2. Token System (NOT JWT): ST (session cookie) + AT (bearer token), auto-refresh
3. Async Throughout: aiosqlite, curl_cffi.AsyncSession
4. Database-Backed Config: Initial from TOML, runtime updates in SQLite
5. Streaming-First: SSE for real-time progress updates
6. Error Handling: Consecutive error tracking, auto-disable threshold
7. Model Config: 34 models (image: GEM_PIX/GEM_PIX_2/IMAGEN_3_5, video: T2V/I2V/R2V)

---

## Database Schema (9 tables)

tokens, projects, token_stats, tasks, request_logs, admin_config, proxy_config, generation_config, cache_config, debug_config

---

## API Endpoints

Public: GET /v1/models, POST /v1/chat/completions
Admin: /api/admin/*, /api/tokens/*, /api/config/*, /api/cache/*, /api/stats, /api/logs
Static: /, /login, /manage, /tmp/*

---

## Unresolved Questions

1. No test suite exists
2. Hardcoded default credentials (admin/admin)
3. Single-instance only, no distributed support
4. No global API rate limiting
