# Flow2API Development Guide

## 🎯 Overview

This guide is for developers who want to contribute to Flow2API, understand its architecture, or extend its functionality.

## 🏗️ Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- Code editor (VS Code, PyCharm, etc.)
- Docker (optional, for testing)

### Setting Up Development Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TheSmallHanCat/flow2api.git
   cd flow2api
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

4. **Install Development Tools**
   ```bash
   pip install black isort flake8 mypy pytest pytest-asyncio
   ```

5. **Set Up Pre-commit Hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 📁 Project Structure

```
flow2api/
├── src/                          # Source code
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py            # OpenAI-compatible endpoints
│   │   └── admin.py             # Admin panel endpoints
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database operations
│   │   ├── logger.py            # Logging utilities
│   │   └── models.py            # Data models
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── concurrency_manager.py     # Rate limiting
│   │   ├── file_cache.py             # File caching
│   │   ├── flow_client.py            # VideoFX API client
│   │   ├── generation_handler.py     # Request handling
│   │   ├── load_balancer.py          # Token selection
│   │   ├── proxy_manager.py          # Proxy management
│   │   └── token_manager.py          # Token lifecycle
│   └── main.py                  # Application entry point
├── static/                       # Web interface
│   ├── login.html
│   └── manage.html
├── config/                       # Configuration
│   ├── setting.toml
│   └── setting_warp.toml
├── tests/                        # Test files
├── docs/                         # Documentation
└── main.py                      # CLI entry point
```

## 🔧 Code Architecture

### Core Components

#### 1. FastAPI Application (`src/main.py`)
- Application initialization
- Lifespan management
- Dependency injection
- Route registration

#### 2. API Layer (`src/api/`)
- **routes.py**: OpenAI-compatible endpoints
- **admin.py**: Management interface endpoints
- Authentication middleware
- Request/response validation

#### 3. Service Layer (`src/services/`)
- **Token Manager**: Token lifecycle, refresh, validation
- **Load Balancer**: Intelligent token selection
- **Concurrency Manager**: Rate limiting per token
- **Flow Client**: VideoFX API wrapper
- **Generation Handler**: Request processing logic
- **File Cache**: Local file caching system
- **Proxy Manager**: Proxy configuration and failover

#### 4. Core Layer (`src/core/`)
- **Config**: Configuration management
- **Database**: SQLite operations
- **Models**: Pydantic data models
- **Auth**: Authentication utilities
- **Logger**: Debug logging

### Data Flow

```
Client Request → Auth Middleware → Route Handler → Generation Handler
                                                           ↓
                                                    Load Balancer → Token Manager
                                                           ↓
                                                    Concurrency Manager
                                                           ↓
                                                    Flow Client → VideoFX API
                                                           ↓
Response ← Generation Handler ← File Cache ← VideoFX Response
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_token_manager.py

# Run async tests
pytest -k "async" --asyncio-mode=auto
```

### Writing Tests

```python
# Example test structure
import pytest
from src.services.token_manager import TokenManager

@pytest.mark.asyncio
async def test_token_refresh():
    # Arrange
    token_manager = TokenManager(db, flow_client)

    # Act
    result = await token_manager.refresh_token(token_id)

    # Assert
    assert result.success is True
    assert result.new_at is not None
```

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **API Tests**: Endpoint testing
4. **Load Tests**: Performance testing

## 📝 Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Good
class TokenManager:
    """Manages token lifecycle with automatic refresh."""

    async def refresh_token(self, token_id: int) -> bool:
        """Refresh access token for given token ID."""
        try:
            token = await self.db.get_token(token_id)
            if not token:
                return False

            new_at = await self.flow_client.refresh_at(token.st)
            await self.db.update_token(token_id, at=new_at)
            return True

        except Exception as e:
            logger.error(f"Failed to refresh token {token_id}: {e}")
            return False

# Bad
class tokenManager:
    def refreshToken(self,token_id):
        token=self.db.get_token(token_id)
        if token==None:
            return False
        new_at=self.flow_client.refresh_at(token.st)
        self.db.update_token(token_id,at=new_at)
        return True
```

### Naming Conventions

- **Classes**: PascalCase (`TokenManager`)
- **Functions/Methods**: snake_case (`refresh_token`)
- **Variables**: snake_case (`access_token`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **Private**: Leading underscore (`_internal_method`)

### Documentation

```python
def calculate_concurrency(self, token_id: int) -> int:
    """Calculate available concurrency for a token.

    Args:
        token_id: The token ID to check

    Returns:
        Number of available concurrent slots

    Raises:
        TokenNotFound: If token doesn't exist

    Example:
        ```python
        available = await manager.calculate_concurrency(123)
        if available > 0:
            await manager.use_slot(123)
        ```
    """
```

## 🔍 Debugging

### Debug Mode

Enable debug mode in configuration:

```toml
[debug]
enabled = true
log_requests = true
log_responses = true
mask_token = true
```

### Debug Logging

```python
from src.core.logger import debug_logger

# Log information
debug_logger.log_info("Token refresh initiated", token_id=token_id)

# Log errors
debug_logger.log_error("Token refresh failed", error=str(e))

# Log requests/responses
debug_logger.log_request(method="POST", url=url, headers=headers)
debug_logger.log_response(status_code=200, body=response_body)
```

### Common Debugging Scenarios

1. **Token Authentication Issues**
   - Check ST to AT conversion
   - Verify token expiration
   - Review proxy settings

2. **Generation Failures**
   - Enable request/response logging
   - Check VideoFX API responses
   - Verify model availability

3. **Performance Issues**
   - Monitor concurrency usage
   - Check token selection logic
   - Profile database queries

## 🚀 Adding New Features

### Adding a New Model

1. Update `MODEL_CONFIG` in `generation_handler.py`:
   ```python
   "new-model-name": {
       "type": "image",  # or "video"
       "model_name": "ACTUAL_MODEL_NAME",
       "aspect_ratio": "IMAGE_ASPECT_RATIO_LANDSCAPE"
   }
   ```

2. Add model-specific logic if needed:
   ```python
   if model_config["type"] == "video" and "special_feature" in model_config:
       # Handle special feature
   ```

3. Update model list endpoint
4. Add tests for the new model

### Adding a New Service

1. Create service file in `src/services/`:
   ```python
   # src/services/new_service.py
   class NewService:
       """Description of the service."""

       def __init__(self, dependency1, dependency2):
           self.dependency1 = dependency1
           self.dependency2 = dependency2
   ```

2. Register in `main.py`:
   ```python
   from src.services.new_service import NewService

   new_service = NewService(dep1, dep2)
   ```

3. Inject dependencies where needed
4. Add configuration if required

### Adding New API Endpoints

1. Add route in appropriate file:
   ```python
   @router.post("/v1/new-endpoint")
   async def new_endpoint(request: RequestModel):
       """New endpoint description."""
       result = await service.handle_request(request)
       return {"result": result}
   ```

2. Create request/response models
3. Add authentication if needed
4. Write tests
5. Update documentation

## 🔄 Database Schema

### Current Schema

```sql
-- Tokens table
CREATE TABLE tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    st TEXT NOT NULL,
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
    video_concurrency INTEGER DEFAULT -1,
    proxy_url TEXT
);

-- Projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    token_id INTEGER,
    project_name TEXT NOT NULL,
    tool_name TEXT DEFAULT 'PINHOLE',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    token_id INTEGER,
    model TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    result_urls TEXT,
    error_message TEXT,
    scene_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Migration Guidelines

When modifying the schema:

1. Create migration script
2. Test on development database
3. Ensure backward compatibility
4. Document changes

## 📊 Performance Optimization

### Async Best Practices

```python
# Good - Concurrent execution
tasks = []
for token in tokens:
    tasks.append(refresh_token(token))
results = await asyncio.gather(*tasks)

# Bad - Sequential execution
for token in tokens:
    await refresh_token(token)
```

### Database Optimization

1. **Use indexes** on frequently queried columns
2. **Batch operations** when possible
3. **Use connection pooling** for high concurrency
4. **Optimize queries** with EXPLAIN

### Memory Management

1. **Stream large responses** instead of loading into memory
2. **Use generators** for large datasets
3. **Implement pagination** for list endpoints
4. **Clean up** unused objects

## 🔒 Security Guidelines

### Input Validation

```python
from pydantic import BaseModel, validator

class TokenRequest(BaseModel):
    st: str

    @validator('st')
    def validate_st(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Invalid session token')
        return v
```

### SQL Injection Prevention

```python
# Good - Parameterized queries
await db.execute(
    "SELECT * FROM tokens WHERE id = ?",
    (token_id,)
)

# Bad - String concatenation
await db.execute(
    f"SELECT * FROM tokens WHERE id = {token_id}"
)
```

### Authentication

```python
# Always verify API key
async def verify_api_key(api_key: str):
    if api_key != config.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
```

## 📚 Documentation

### Code Documentation

```python
def refresh_token(self, token_id: int) -> bool:
    """Refresh access token for a given token ID.

    This method attempts to refresh the access token by:
    1. Retrieving the current token from database
    2. Converting ST to new AT using Flow API
    3. Updating the database with new AT
    4. Handling any errors that occur

    Args:
        token_id: The ID of the token to refresh

    Returns:
        True if refresh successful, False otherwise

    Raises:
        TokenNotFound: If token doesn't exist in database
        FlowAPIError: If VideoFX API returns an error

    Example:
        ```python
        success = await token_manager.refresh_token(123)
        if success:
            print("Token refreshed successfully")
        ```

    See Also:
        - `get_token()`: For retrieving tokens
        - `update_token()`: For updating token data
        - `FlowClient.st_to_at()`: For ST conversion
    """
```

### API Documentation

Update OpenAPI documentation:

```python
@router.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    summary="Create chat completion",
    description="""
    Create a chat completion for image or video generation.

    This endpoint supports:
    - Text-to-image generation
    - Image-to-image transformation
    - Text-to-video generation
    - Image-to-video with reference frames

    ## Examples

    ### Text-to-Image
    ```json
    {
        "model": "gemini-2.5-flash-image-landscape",
        "messages": [{
            "role": "user",
            "content": "A beautiful sunset"
        }],
        "stream": true
    }
    ```
    """
)
```

## 🚀 Deployment for Development

### Local Development

```bash
# Run with auto-reload
python main.py --host 0.0.0.0 --port 8000

# Run with debug mode
DEBUG=true python main.py
```

### Docker Development

```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

```bash
# Build and run
docker build -f Dockerfile.dev -t flow2api:dev .
docker run -p 8000:8000 -v $(pwd):/app flow2api:dev
```

## 🤝 Contributing

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact considered
- [ ] Security implications reviewed

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build process or auxiliary tool changes

Example:
```
feat(token): add automatic retry on AT refresh failure

Implement exponential backoff retry mechanism when refreshing
access tokens fails due to temporary network issues.

Closes #123
```

## 📋 Development Roadmap

### Planned Features

1. **Multi-Language Support**
   - Node.js client library
   - Go client library
   - Python async client

2. **Advanced Features**
   - Webhook support
   - Batch processing
   - Queue management
   - Priority scheduling

3. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Health check endpoints
   - Performance profiling

4. **Scaling**
   - Redis support for distributed caching
   - PostgreSQL support
   - Kubernetes deployment
   - Auto-scaling

## 📞 Getting Help

### Development Resources

- **Code Documentation**: Inline docstrings
- **API Documentation**: Auto-generated at `/docs`
- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)

### Debugging Tools

```python
# Python debugger
import pdb; pdb.set_trace()

# Async debugger
import aiomonitor

# Memory profiler
import memory_profiler

# Performance profiler
import cProfile
```

### Community

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions

---

**Next Steps**: Once you're familiar with development, check out the [Deployment Guide](./DEPLOYMENT.md) for production deployment strategies. For issues, see the [Troubleshooting Guide](./TROUBLESHOOTING.md)."