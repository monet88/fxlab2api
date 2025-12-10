# Code Style and Conventions - Flow2API

## Python Version
- Python 3.8+
- Use async/await for all I/O operations (no blocking code)

## Type Hints
- Use type hints throughout the codebase
- Import types from `typing` module when needed
- Example: `def function(param: str) -> Dict[str, Any]:`

## Naming Conventions
- **Classes**: PascalCase (e.g., `TokenManager`, `FlowClient`)
- **Functions/Methods**: snake_case (e.g., `get_token()`, `validate_request`)
- **Variables**: snake_case (e.g., `api_key`, `flow_timeout`)
- **Constants**: UPPER_SNAKE_CASE (rarely used in this project)
- **Private Methods**: Prefix with underscore (e.g., `_internal_method`)

## Docstrings
- Use triple-quoted docstrings for modules, classes, and functions
- Format: Brief description on first line, details on following lines
- Example:
```python
"""Brief description of function purpose.

Args:
    param1: Description of parameter 1
    param2: Description of parameter 2

Returns:
    Description of return value
"""
```

## Import Style
- Group imports: standard library → third-party → local modules
- Use absolute imports for project modules: `from src.core.config import Config`
- Within `__init__.py` files, use `from .module import Class` for local imports

## Error Handling
- Use try/except for external API calls and I/O operations
- Log errors with appropriate logging level (debug, info, warning, error)
- Graceful degradation for non-critical errors
- Auto-disable tokens after consecutive failures (configurable threshold)

## Logging
- Use appropriate log levels:
  - DEBUG: Detailed information for debugging
  - INFO: General operational events
  - WARNING: Potential issues
  - ERROR: Failed operations
- Format: Clear, descriptive messages with relevant context

## Configuration Management
- TOML format for configuration files
- Use Pydantic models for configuration validation
- Support hot-reload for runtime configuration changes
- Database-backed configuration for dynamic values

## Database
- SQLite with async support via aiosqlite
- Automatic migrations on startup
- Use parameterized queries to prevent SQL injection
- Store database at: `data/flow2api.db`

## Security
- Bearer token authentication for API access
- Bcrypt hashing for passwords
- Token masking in logs (configurable)
- Never commit sensitive data (tokens, passwords)

## Async/Await Patterns
- All I/O operations must be async
- Use `await` for database queries, API calls, file operations
- Never use blocking operations (e.g., `time.sleep`, synchronous file I/O)
- Use `async with` for context managers when available

## Service Layer Pattern
- Each service has a single responsibility
- Dependency injection for service dependencies
- Clear separation between API, Service, and Core layers
- Service initialization in FastAPI lifespan context
