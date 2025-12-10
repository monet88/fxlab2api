# Development Workflow - Flow2API

## Getting Started

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/TheSmallHanCat/flow2api.git
cd flow2api

# Set up virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Docker (Recommended)
```bash
# Standard mode
docker-compose up -d

# WARP proxy mode
docker-compose -f docker-compose.warp.yml up -d

# View logs
docker-compose logs -f
```

#### Option 2: Local Development
```bash
python main.py
# Service runs on http://localhost:8000
```

### First Access
- Admin Panel: http://localhost:8000
- Default credentials: admin/admin
- ⚠️ **IMPORTANT**: Change password immediately!

## Development Environment

### Python Version
- Minimum: Python 3.8
- Recommended: Python 3.10+

### Key Dependencies
- fastapi==0.119.0 (Web framework)
- uvicorn[standard]==0.32.1 (ASGI server)
- pydantic==2.10.4 (Data validation)
- aiosqlite==0.20.0 (Async SQLite)
- curl-cffi (HTTP client)
- bcrypt==4.2.1 (Password hashing)

### Development Tools
- **No test framework** currently configured
- **No linting** tools configured
- **No formatter** enforced
- Manual testing via API endpoints and web UI

## Code Organization

```
src/
├── main.py                 # FastAPI app initialization
├── api/                    # API endpoints
│   ├── routes.py          # OpenAI-compatible routes
│   └── admin.py           # Admin panel routes
├── core/                  # Core infrastructure
│   ├── config.py          # Configuration management
│   ├── database.py        # Database operations
│   ├── auth.py            # Authentication
│   ├── models.py          # Pydantic models
│   └── logger.py          # Logging setup
└── services/              # Business logic
    ├── flow_client.py     # Google Labs API client
    ├── token_manager.py   # Token management
    ├── load_balancer.py   # Multi-token balancing
    ├── generation_handler.py  # Request orchestration
    ├── concurrency_manager.py  # Rate limiting
    ├── proxy_manager.py   # Proxy support
    └── file_cache.py      # File caching
```

## Configuration Management

### Configuration Files
- `config/setting.toml` - Main configuration
- `config/setting_warp.toml` - WARP proxy configuration

### Key Settings
```toml
[global]
api_key = "han1234"              # API authentication key
admin_username = "admin"         # Admin panel username
admin_password = "admin"         # Admin panel password

[flow]
labs_base_url = "https://labs.google/fx/api"
api_base_url = "https://aisandbox-pa.googleapis.com/v1"
timeout = 120
poll_interval = 3.0
max_poll_attempts = 200

[server]
host = "0.0.0.0"
port = 8000

[debug]
enabled = false
log_requests = true
log_responses = true
mask_token = true

[admin]
error_ban_threshold = 3
```

### Runtime Configuration
- Some settings can be changed via admin panel
- Hot-reload supported for certain configurations
- Database stores runtime settings

## Database

### SQLite Database
- Location: `data/flow2api.db`
- Uses aiosqlite for async operations
- Automatic migrations on startup
- Tables: tokens, settings, usage_stats

### Database Operations
- All database operations are async
- Use `await` for queries
- Connection pooling handled automatically

## API Usage

### Testing API Endpoints
```bash
# List models
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer han1234"

# Generate image
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash-image-landscape",
    "messages": [{"role": "user", "content": "A cute cat"}],
    "stream": true
  }'
```

### Admin Panel
- URL: http://localhost:8000
- Login: admin/admin (change immediately)
- Functions:
  - Token management
  - Configuration updates
  - Usage statistics
  - System monitoring

## Common Development Tasks

### Adding New Features
1. Identify the layer (API, Service, Core)
2. Follow existing patterns and conventions
3. Use async/await for all I/O
4. Add appropriate docstrings
5. Test manually via API or web UI
6. Update repository index: `python scripts/update_index.py`

### Debugging
1. Enable debug mode in config: `debug.enabled = true`
2. Check logs in console or docker logs
3. Use token masking to hide sensitive data
4. Monitor admin panel for real-time status

### Database Changes
1. Modify `src/core/database.py` if needed
2. Migrations are automatic on startup
3. Test with sample data

### Configuration Changes
1. Update `config/setting.toml`
2. Some changes require restart
3. Some can be updated via admin panel

## Best Practices

### Code Style
- Use type hints throughout
- Write descriptive docstrings
- Follow naming conventions (PascalCase for classes, snake_case for functions/variables)
- Keep functions focused and single-purpose

### Error Handling
- Use try/except for external API calls
- Log errors appropriately
- Provide graceful degradation
- Auto-disable failing tokens

### Security
- Never commit sensitive data
- Change default admin credentials
- Use token masking in logs
- Validate all inputs

### Performance
- Use async/await consistently
- Monitor concurrency limits
- Optimize token usage
- Cache when appropriate

## Troubleshooting

### Common Issues
1. **Token errors**: Check token validity in admin panel
2. **Database locks**: Ensure proper async handling
3. **Memory issues**: Monitor resource usage
4. **Connection errors**: Check proxy settings if enabled

### Log Locations
- Docker: `docker-compose logs -f`
- Local: Console output
- File: Logs may be written to `logs.txt`

## Deployment

### Production Checklist
- [ ] Change admin credentials
- [ ] Use strong API key
- [ ] Configure appropriate timeouts
- [ ] Set up monitoring
- [ ] Enable caching if needed
- [ ] Configure proxy if required
- [ ] Test all endpoints
- [ ] Verify token management

### Docker Deployment
```bash
# Build and run
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f flow2api
```
