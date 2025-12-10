# Suggested Commands for Flow2API

## Project Overview
Flow2API is an OpenAI-compatible API service that bridges Google VideoFX (Veo) with developers through a standardized API for AI content generation.

## Essential Development Commands

### Running the Application
```bash
# Docker deployment (recommended)
docker-compose up -d                    # Standard mode
docker-compose -f docker-compose.warp.yml up -d  # WARP proxy mode
docker-compose logs -f                  # View logs

# Local development
python -m venv venv                     # Create virtual environment
venv\Scripts\activate                   # Activate (Windows) - source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt         # Install dependencies
python main.py                         # Start service on http://localhost:8000
```

### Development Tasks
```bash
# Update repository index files
python scripts/update_index.py          # Update both PROJECT_INDEX.md and PROJECT_INDEX.json
python scripts/update_index.py --check  # Check if update needed
python scripts/update_index.py --md     # Update only markdown
python scripts/update_index.py --json   # Update only json
```

### Git Commands (Windows)
```bash
git status                              # Check working tree status
git add .                              # Stage all changes
git commit -m "<message>"              # Commit with message
git log                                # View commit history
git diff                               # View staged/unstaged changes
```

### Database Management
```bash
# Database file created at: data/flow2api.db
# Database migrations are automatic on startup
python main.py                         # Triggers automatic migration
```

## Project Architecture

### Service Layer
1. **FastAPI Application** (src/main.py) - Entry point with lifespan management
2. **API Layer** (src/api/) - OpenAI-compatible endpoints and admin panel
3. **Service Layer** (src/services/) - Business logic components
4. **Core Layer** (src/core/) - Infrastructure (config, database, auth, models)

### Key Modules
- `FlowClient` - Google Labs API client wrapper
- `TokenManager` - Manages ST/AT token lifecycle with auto-refresh
- `LoadBalancer` - Intelligent token selection
- `GenerationHandler` - Orchestrates image/video generation
- `ConcurrencyManager` - Controls request concurrency per token

## Important Files
- `config/setting.toml` - Main configuration file (TOML format)
- `main.py` - Application entry point
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker configuration
- `data/flow2api.db` - SQLite database

## Configuration Notes
- Database migrations happen automatically on startup
- Tokens auto-disable after consecutive errors (configurable threshold)
- File caching is optional in `tmp/` directory
- Proxy support via HTTP/SOCKS5 configurable through admin panel

## Testing Approach
- No test suite currently present
- Manual testing via API endpoints and web UI
- First access: http://localhost:8000 (admin/admin - change immediately)
