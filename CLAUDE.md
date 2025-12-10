# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flow2API is a middleware service that provides an OpenAI-compatible API interface for Google's VideoFX (Veo) platform. It bridges Google's AI generation services with developers through a standardized API for image and video generation.

## Key Commands

### Running the Application

```bash
# Docker deployment (recommended)
docker-compose up -d                    # Standard mode
docker-compose -f docker-compose.warp.yml up -d  # WARP proxy mode
docker-compose logs -f                  # View logs

# Local development
pip install -r requirements.txt
python main.py           # Runs on http://localhost:8000
```

### Development Tasks

```bash
# Update repository index files
python scripts/update_index.py          # Update both PROJECT_INDEX.md and PROJECT_INDEX.json
python scripts/update_index.py --check  # Check if update needed
python scripts/update_index.py --md     # Update only markdown
python scripts/update_index.py --json   # Update only JSON
```

### Database Management

The application uses SQLite with automatic migration. Database file is created at `data/flow2api.db` on first run.

## Architecture Overview

### Service Layer Architecture

The application follows a service-oriented architecture with dependency injection:

1. **FastAPI Application** (`src/main.py`) - Entry point with lifespan management
2. **API Layer** (`src/api/`) - Routes for OpenAI-compatible endpoints and admin panel
3. **Service Layer** (`src/services/`) - Business logic components:
   - `FlowClient` - Google Labs API client wrapper
   - `TokenManager` - Manages ST/AT token lifecycle with auto-refresh
   - `LoadBalancer` - Intelligent token selection
   - `GenerationHandler` - Orchestrates image/video generation
   - `ConcurrencyManager` - Controls request concurrency per token
4. **Core Layer** (`src/core/`) - Infrastructure (config, database, auth, models)

### Token System

Flow2API uses Google's token system (NOT JWT):
- **ST (Session Token)**: Sent via Cookie for Google authentication
- **AT (Access Token)**: Sent via Bearer header for API calls
- Auto-refresh mechanism when AT expires (refresh 1 hour before expiry)

### Authentication

- Admin panel: Username/password with bcrypt hashing
- API access: Bearer token (simple string comparison, not JWT)
- Default credentials: admin/admin (change immediately)

### Configuration

- Primary config: `config/setting.toml` (TOML format)
- Runtime updates via admin panel (hot-reload supported)
- Database-backed configuration for dynamic changes

### Request Flow

1. Client sends request to OpenAI-compatible endpoint
2. LoadBalancer selects appropriate token
3. ConcurrencyManager checks limits
4. GenerationHandler processes request
5. FlowClient makes API calls to Google
6. Response streamed back to client

## Important Notes

- **No test suite** - Consider manual testing when making changes
- **Async throughout** - Use async/await for all I/O operations
- **Database migrations** - Automatic on startup, check `src/core/database.py`
- **Error handling** - Tokens auto-disable after consecutive errors (configurable threshold)
- **File cache** - Optional local caching in `tmp/` directory
- **Proxy support** - HTTP/SOCKS5 proxy configurable via admin panel