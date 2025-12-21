# Flow2API Code Standards

> Last Updated: 2025-12-22
> Version: 1.0.0

## Overview

This document defines the coding standards, conventions, and best practices for the Flow2API project. All contributors should follow these guidelines to maintain code consistency and quality.

---

## Project Structure

### Directory Organization

```
flow2api/
├── src/                      # All source code
│   ├── main.py               # Application entry point
│   ├── api/                  # API layer (routes, endpoints)
│   ├── core/                 # Core infrastructure (db, config, auth)
│   └── services/             # Business logic services
├── config/                   # Configuration files (TOML)
├── static/                   # Static web assets
├── docs/                     # Documentation
├── data/                     # Runtime data (database)
├── tmp/                      # Temporary/cache files
└── tests/                    # Test files (future)
```

### Layer Responsibilities

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| Entry | `src/main.py` | App initialization, lifespan, middleware |
| API | `src/api/` | HTTP endpoints, request/response handling |
| Core | `src/core/` | Infrastructure: database, config, auth, logging |
| Services | `src/services/` | Business logic, external API clients |

---

## Python Standards

### Version and Style

- **Python Version**: 3.8+ (3.11 for Docker)
- **Style Guide**: PEP 8
- **Line Length**: 120 characters max
- **Indentation**: 4 spaces (no tabs)

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules | snake_case | `token_manager.py` |
| Classes | PascalCase | `TokenManager` |
| Functions | snake_case | `get_active_tokens()` |
| Variables | snake_case | `token_count` |
| Constants | UPPER_SNAKE_CASE | `MAX_POLL_ATTEMPTS` |
| Private | Leading underscore | `_internal_method()` |

### Type Annotations

Use type hints for all function signatures:

```python
# Good
async def add_token(
    self,
    st: str,
    email: str,
    remark: Optional[str] = None
) -> Token:
    ...

# Avoid
async def add_token(self, st, email, remark=None):
    ...
```

### Docstrings

Use Google-style docstrings for public functions:

```python
async def generate_image(
    self,
    prompt: str,
    model: str
) -> str:
    """Generate an image from a text prompt.

    Args:
        prompt: The text description for image generation.
        model: The model ID to use for generation.

    Returns:
        URL of the generated image.

    Raises:
        GenerationError: If image generation fails.
    """
```

---

## Async Programming

### Async/Await Requirements

All I/O operations MUST be async:

```python
# Good - async database operation
async def get_token(self, token_id: int) -> Optional[Token]:
    async with aiosqlite.connect(self.db_path) as db:
        cursor = await db.execute("SELECT * FROM tokens WHERE id = ?", (token_id,))
        row = await cursor.fetchone()
        return Token(**dict(row)) if row else None

# Avoid - blocking I/O
def get_token(self, token_id: int) -> Optional[Token]:
    conn = sqlite3.connect(self.db_path)  # Blocks!
    ...
```

### Async Context Managers

Use `async with` for resource management:

```python
async with aiosqlite.connect(self.db_path) as db:
    async with db.execute("SELECT * FROM tokens") as cursor:
        rows = await cursor.fetchall()
```

---

## Error Handling

### Exception Hierarchy

```python
# Custom exceptions in src/core/exceptions.py (if created)
class Flow2APIError(Exception):
    """Base exception for Flow2API."""
    pass

class TokenError(Flow2APIError):
    """Token-related errors."""
    pass

class GenerationError(Flow2APIError):
    """Generation-related errors."""
    pass
```

### Error Handling Pattern

```python
async def generate(self, request: GenerationRequest) -> str:
    try:
        token = await self.load_balancer.select_token(request.model)
        if not token:
            raise HTTPException(status_code=503, detail="No available tokens")

        result = await self.flow_client.generate(token, request)
        return result

    except HTTPException:
        raise  # Re-raise HTTP exceptions

    except TokenError as e:
        logger.error(f"Token error: {e}")
        raise HTTPException(status_code=401, detail=str(e))

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## API Design

### Endpoint Conventions

| HTTP Method | Operation | Example |
|-------------|-----------|---------|
| GET | Retrieve | `GET /v1/models` |
| POST | Create/Action | `POST /v1/chat/completions` |
| PUT | Update (full) | `PUT /admin/tokens/{id}` |
| PATCH | Update (partial) | `PATCH /admin/config` |
| DELETE | Delete | `DELETE /admin/tokens/{id}` |

### Response Format

Use consistent response structures:

```python
# Success response
{
    "success": True,
    "data": {...}
}

# Error response
{
    "detail": "Error message"
}

# List response (OpenAI-compatible)
{
    "object": "list",
    "data": [...]
}
```

### OpenAI Compatibility

For `/v1/` endpoints, follow OpenAI's API format exactly:

```python
# Models endpoint response
{
    "object": "list",
    "data": [
        {
            "id": "gemini-2.5-flash-image-landscape",
            "object": "model",
            "owned_by": "flow2api"
        }
    ]
}

# Chat completions streaming response
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","choices":[...]}
```

---

## Database Standards

### Table Naming

- Use snake_case for table names
- Use plural nouns: `tokens`, `projects`, `tasks`
- Use `_config` suffix for configuration tables

### Column Naming

- Use snake_case: `created_at`, `is_active`
- Use `_at` suffix for timestamps: `created_at`, `updated_at`
- Use `is_` prefix for booleans: `is_active`, `is_enabled`
- Use `_id` suffix for foreign keys: `token_id`, `project_id`

### SQL Patterns

```python
# Use parameterized queries (prevent SQL injection)
await db.execute(
    "SELECT * FROM tokens WHERE id = ?",
    (token_id,)
)

# Use transactions for multi-step operations
async with db.execute("BEGIN"):
    await db.execute("UPDATE tokens SET use_count = use_count + 1 WHERE id = ?", (token_id,))
    await db.execute("INSERT INTO usage_logs ...")
    await db.commit()
```

---

## Configuration Standards

### TOML Structure

```toml
# Use sections for logical grouping
[global]
api_key = "..."

[server]
host = "0.0.0.0"
port = 8000

[flow]
timeout = 120
poll_interval = 3.0
```

### Configuration Access

```python
# Use the Config class, not direct file access
from src.core.config import Config

config = Config()
api_key = config.get("global", "api_key")
```

---

## Logging Standards

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed debugging info (token values masked) |
| INFO | General operational events |
| WARNING | Unexpected but handled situations |
| ERROR | Errors that affect specific requests |
| CRITICAL | System-wide failures |

### Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

# Use structured logging
logger.info(f"Token {token_id} refreshed successfully")
logger.error(f"Generation failed for model {model}: {error}")

# Mask sensitive data
logger.debug(f"Using token: {mask_token(token.st)}")
```

---

## Pydantic Models

### Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """Token data model."""

    id: int
    st: str = Field(..., description="Session token")
    at: Optional[str] = Field(None, description="Access token")
    at_expires: Optional[datetime] = None
    email: str
    name: Optional[str] = None
    remark: Optional[str] = None
    is_active: bool = True
    image_enabled: bool = True
    video_enabled: bool = True
    image_concurrency: int = -1  # -1 = unlimited
    video_concurrency: int = -1

    class Config:
        from_attributes = True  # For ORM compatibility
```

### Request/Response Models

```python
class ChatCompletionRequest(BaseModel):
    """OpenAI-compatible chat completion request."""

    model: str
    messages: List[Message]
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ChatCompletionChunk(BaseModel):
    """Streaming response chunk."""

    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChunkChoice]
```

---

## Service Layer Patterns

### Dependency Injection

```python
class GenerationHandler:
    """Orchestrates generation requests."""

    def __init__(
        self,
        flow_client: FlowClient,
        token_manager: TokenManager,
        load_balancer: LoadBalancer,
        concurrency_manager: ConcurrencyManager
    ):
        self.flow_client = flow_client
        self.token_manager = token_manager
        self.load_balancer = load_balancer
        self.concurrency_manager = concurrency_manager
```

### Service Initialization

Services are initialized in `src/main.py` lifespan:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    database = Database()
    await database.initialize()

    config = Config()
    flow_client = FlowClient(config)
    token_manager = TokenManager(database, flow_client)
    # ... more services

    app.state.services = {
        "database": database,
        "token_manager": token_manager,
        # ...
    }

    yield

    # Shutdown
    await database.close()
```

---

## Testing Standards (Future)

### Test File Naming

```
tests/
├── test_api_routes.py
├── test_token_manager.py
├── test_generation_handler.py
└── conftest.py
```

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch

class TestTokenManager:
    """Tests for TokenManager service."""

    @pytest.fixture
    def token_manager(self):
        """Create a TokenManager with mocked dependencies."""
        database = AsyncMock()
        flow_client = AsyncMock()
        return TokenManager(database, flow_client)

    @pytest.mark.asyncio
    async def test_add_token_success(self, token_manager):
        """Test successful token addition."""
        token_manager.database.add_token.return_value = Token(...)

        result = await token_manager.add_token("st", "email@test.com")

        assert result.email == "email@test.com"
        token_manager.database.add_token.assert_called_once()
```

---

## Git Conventions

### Commit Messages

Use conventional commits format:

```
feat: add support for Veo 3.1 models
fix: token refresh not triggering before expiry
docs: update API documentation
refactor: extract token validation logic
chore: update dependencies
```

### Branch Naming

```
feature/add-veo-3-1-support
fix/token-refresh-timing
docs/update-readme
```

---

## Security Guidelines

### Sensitive Data

1. **Never log tokens in plain text** - use masking
2. **Never hardcode secrets** - use configuration
3. **Hash passwords with bcrypt** - no plain text storage
4. **Validate all input** - use Pydantic models

### Token Masking

```python
def mask_token(token: str) -> str:
    """Mask a token for safe logging."""
    if len(token) <= 8:
        return "***"
    return f"{token[:4]}...{token[-4:]}"
```

---

## Documentation Standards

### Code Comments

- Use comments sparingly - code should be self-documenting
- Comment "why", not "what"
- Keep comments up to date

```python
# Good - explains why
# Refresh AT 1 hour before expiry to avoid generation failures
if at_expires - now < timedelta(hours=1):
    await self._refresh_at(token)

# Avoid - states the obvious
# Increment counter
counter += 1
```

### README Updates

Update relevant documentation when:
- Adding new features
- Changing API endpoints
- Modifying configuration options
- Adding dependencies

---

*This document should be updated as the project evolves and new patterns emerge.*
