# Task Completion Workflow - Flow2API

## When a Task is Completed

### 1. Testing
- Manually test the implemented feature or fix
- Verify API endpoints work correctly:
  ```bash
  # Test models endpoint
  curl http://localhost:8000/v1/models -H "Authorization: Bearer han1234"
  
  # Test generation endpoint (with streaming)
  curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Authorization: Bearer han1234" \
    -H "Content-Type: application/json" \
    -d '{"model": "gemini-2.5-flash-image-landscape", "messages": [{"role": "user", "content": "test"}], "stream": true}'
  ```
- Verify admin panel functionality at http://localhost:8000
- Test token management functions

### 2. Code Quality Checks
- Ensure all functions have proper docstrings
- Verify type hints are present
- Check for proper error handling
- Ensure async/await used for all I/O
- Confirm logging is appropriate

### 3. Update Repository Index
After any code changes, update the project index:
```bash
python scripts/update_index.py
```

## Deployment Steps

### Docker Deployment
```bash
# Rebuild and restart containers
docker-compose down
docker-compose up --build -d

# Verify logs
docker-compose logs -f
```

### Local Development
```bash
# Restart service
python main.py

# Check logs in console
```

## Database Management
- Database migrations are automatic on startup
- No manual migration commands needed
- Database file: `data/flow2api.db`
- Backup database before major changes

## Configuration Changes
- Main config: `config/setting.toml`
- Changes take effect after restart
- Some settings support hot-reload via admin panel
- Never commit sensitive credentials

## Security Checklist
- [ ] No sensitive data (tokens, passwords) committed
- [ ] Bearer tokens validated properly
- [ ] Password hashing with bcrypt
- [ ] Token masking enabled in debug logs
- [ ] Admin credentials changed from defaults

## Performance Considerations
- Verify concurrency limits are appropriate
- Check token load balancing works correctly
- Monitor response times
- Ensure cache settings are optimized (if enabled)

## Documentation Updates
- Update relevant docstrings
- Update PROJECT_INDEX.md if structure changed
- Update README.md if user-facing changes
- Add CHANGELOG entry for major changes

## Common Issues to Watch For
1. **Token errors**: Check token validity and refresh status
2. **Database locks**: Ensure proper async handling
3. **Memory leaks**: Monitor resource usage
4. **Concurrent request handling**: Test under load
5. **CORS issues**: Check API client configurations

## Pre-Commit Checklist
- [ ] Code tested manually
- [ ] No print statements (use logging instead)
- [ ] Type hints present
- [ ] Docstrings updated
- [ ] Repository index updated
- [ ] Sensitive data not committed
- [ ] Admin panel functionality verified
- [ ] API endpoints responding correctly

## Post-Deployment Verification
- [ ] Service starts without errors
- [ ] Admin panel accessible
- [ ] API endpoints responding
- [ ] Token management working
- [ ] Generation requests successful
- [ ] Logs show no critical errors
